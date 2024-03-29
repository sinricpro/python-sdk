"""
 *  Copyright (c) 2019-2023 Sinric. All rights reserved.
 *  Licensed under Creative Commons Attribution-Share Alike (CC BY-SA)
 *
 *  This file is part of the Sinric Pro (https://github.com/sinricpro/)
"""

import asyncio
import re
import sys

from loguru import logger
from ._sinricpro_websocket import SinricProSocket
from ._events import Events
from typing import (
    Any,
    Awaitable,
    Callable,
    Iterable as TypingIterable,
    List,
    Optional,
    Set,
    Type,
    Union,
    cast,
)

# logger.add("{}.log".format("sinricpro_logfile"), rotation="10 MB")


class SinricPro:
    def __init__(self, api, device_id, request_callbacks, event_callbacks=None, enable_log=False, restore_states=False,
                 secret_key="", loop_delay=0.5):
        try:
            assert (self.verify_device_ids(device_id))
            self.restore_states = restore_states
            self.app_key = api
            self.loop_delay = loop_delay if loop_delay > 0 else 0.5
            self.secret_key = secret_key
            self.device_id = device_id
            self.logger = logger
            self.request_callbacks = request_callbacks
            self.socket = SinricProSocket(self.app_key, self.device_id, self.request_callbacks, enable_log, self.logger,
                                          self.restore_states, self.secret_key, loop_delay=loop_delay)
            self.connection = None
            self.event_callbacks = event_callbacks
            self.event_handler = Events(
                self.connection, self.logger, self.secret_key)

        except AssertionError as e:
            logger.error("Device Id verification failed")
            sys.exit(0)

    def verify_device_ids(self, device_id_arr):
        arr = device_id_arr
        for i in arr:
            res = re.findall(r'^[a-fA-F0-9]{24}$', i)
            if len(res) == 0:
                return False
        return True

    async def connect(self, udp_client=None, sleep=0):
        try:
            self.connection = await self.socket.connect()
            receive_message_task = asyncio.create_task(self.socket.receive_message(connection=self.connection))
            handle_queue_task = asyncio.create_task(self.socket.handle_queue())

            if self.event_callbacks is not None:
                handle_event_queue_task = asyncio.create_task(
                    self.event_callbacks())
                await handle_event_queue_task

            await handle_queue_task
            await receive_message_task

        except KeyboardInterrupt:
            self.logger.error('Keyboard interrupt')
        except Exception as e:
            self.logger.error(e)

    # async def run_app(self, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
    #     """Run an app locally"""

    #     if loop is None:
    #         loop = asyncio.new_event_loop()
        
    #     #loop.set_debug(debug)
    #     self.connection = await self.socket.connect()

    #     receive_message_task = loop.create_task(self.socket.receive_message(connection=self.connection))
    #     handle_queue_task = loop.create_task(self.socket.handle_queue())
    #     #handle_event_queue_task = asyncio.create_task(self.event_callbacks())
                    
    #     try:
    #         asyncio.set_event_loop(loop)
    #         loop.run_until_complete([receive_message_task, handle_queue_task])
    #     except (KeyboardInterrupt):  # pragma: no cover GracefulExit
    #         pass
    #     finally:
    #         #_cancel_tasks({main_task}, loop)
    #         #_cancel_tasks(asyncio.all_tasks(loop), loop)
    #         loop.run_until_complete(loop.shutdown_asyncgens())
    #         loop.close()
    #         asyncio.set_event_loop(None)