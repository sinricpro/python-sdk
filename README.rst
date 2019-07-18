SINRIC  PRO
===============

This is a python library for alexa home automation skill
 SINRIC PRO ---> https://sinric.pro/

Functions:
----------
* Automate your home using alexa with sinricpro

Installation :
--------------

Python3
-------

::

    python3 -m pip install pysinric --user


Pro Switch Demo:
~~~~~~~~~~~~~~~~~

::

    from sinric import SinricPro
    from sinric import SinricProUdp
    from credentials import apiKey, deviceId


    def power_state(did, state):
        # Alexa, turn ON/OFF Device
        print(did, state['state'])
        return True, state['state']


    callbacks = {
    'powerState': power_state
    }

    if __name__ == '__main__':
        client = SinricPro(apiKey, deviceId, callbacks, enable_trace=False)
        udp_client = SinricProUdp(callbacks)
        udp_client.enableUdpPrint(False)  # Set it to True to start printing request UDP JSON
        client.handle_all(udp_client)
