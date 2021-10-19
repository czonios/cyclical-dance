import pyOSC3
# import pythonosc

def init_supercollider():
    client = pyOSC3.OSCClient()
    client.connect('127.0.0.1', 57110)
    # client = pythonosc.udp_client.SimpleUDPClient('127.0.0.1', 57110)
    return client

def send_pos(position, sc):
    print(position)
    msg = pyOSC3.OSCMessage()
    msg.setAddress(f"/{position}")
    msg.append(500)
    sc.send(msg)
    # sc.send_message(f"/{position}", 0)

def reset_sc(sc):
    send_pos("reset", sc)

if __name__ == "__main__":
    sc = init_supercollider()
    import time
    send_pos(1, sc)
    time.sleep(0.5)
    send_pos(2, sc)
    time.sleep(0.5)
    send_pos(3, sc)
    time.sleep(0.5)
    send_pos(4, sc)
    time.sleep(0.5)
    send_pos(5, sc)
    time.sleep(0.5)
    reset_sc(sc)
