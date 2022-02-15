from sinric import SinricPro 
import asyncio

APP_KEY = ''
APP_SECRET = ''
LOCK_ID = ''

def lock_state(device_id, state):
    print(device_id, state)
    return True, state


callbacks = {
    'setLockState': lock_state
}

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = SinricPro(APP_KEY, [LOCK_ID], callbacks, enable_log=True, restore_states=False, secretKey=APP_SECRET)
    loop.run_until_complete(client.connect())


# To update the lock state on server. 
# client.event_handler.raiseEvent(lockId, 'setLockState',data={'state': 'LOCKED'})
# client.event_handler.raiseEvent(lockId, 'setLockState',data={'state': 'UNLOCKED'})