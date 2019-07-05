# python-tuya based home assistant custom component

This custom component uses the python-tuya fork that can talk with Tuya version 3.3

## Key extraction

https://github.com/clach04/python-tuya/wiki has background information for how to get device id and local key.
(the device id can be seen in Jinvoo Smart App, under "Device Info").

### Instructions

Copy the folder localtuya into your home assistant custom_components folder (create the folder in the same place as your configuration.yaml lives

Set a config like so:

```
switch:
  - platform: localtuya
    host: 192.168.0.1
    local_key: 1234567891234567
    device_id: 12345678912345671234
    name: tuya_01
```

### Related Projects

  * https://github.com/sean6541/tuyaapi Python API to the web api
  * https://github.com/codetheweb/tuyapi node.js
  * https://github.com/Marcus-L/m4rcus.TuyaCore - .NET
  * https://github.com/SDNick484/rectec_status/ - RecTec pellet smokers control (with Alexa skill)

### Acknowledgements

  * Based on mytuya work (link missing)
