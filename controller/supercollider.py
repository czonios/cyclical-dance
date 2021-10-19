import pyOSC3

def init_supercollider():
    client = pyOSC3.OSCClient()
    client.connect(( '127.0.0.1', 57120 ))
    return client

def send_pos(position, sc):
    print(position)
    msg = pyOSC3.OSCMessage()
    msg.setAddress(f"/{position}")
    msg.append(500)
    sc.send(msg)

def reset_sc(sc):
    raise NotImplementedError