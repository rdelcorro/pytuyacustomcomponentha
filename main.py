import pytuya

d = pytuya.OutletDevice('21821004b4e62d7b2754', '192.168.20.17', '8944e941cbd20eec')
data = d.status()  # NOTE this does NOT require a valid key
print('Dictionary %r' % data)
print('state (bool, true is ON) %r' % data['dps']['1'])  # Show status of first controlled switch on device

# Toggle switch state
switch_state = data['dps']['1']
data = d.set_status(not switch_state)  # This requires a valid key
if data:
    print('set_status() result %r' % data)

# on a switch that has 4 controllable ports, turn the fourth OFF (1 is the first)
data = d.set_status(False, 4)
if data:
    print('set_status() result %r' % data)
    print('set_status() extrat %r' % data[20:-8])