

import asyncio


async def waitAsync(aysncAction):
    try:
        val = await asyncio.wait_for(aysncAction, timeout=1)
        return val
    except Exception:
        return None