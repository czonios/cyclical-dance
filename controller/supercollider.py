# import pyOSC3
from pythonosc import udp_client

class SuperCollider():
    def __init__(self):
        # super.__init__()
        self.client = udp_client.SimpleUDPClient('127.0.0.1', 57120)
        # self.client = pyOSC3.OSCClient()
        # self.client.connect(('127.0.0.1', 57110))

    def send_pos(self, position):
        print(position)
        # msg = pyOSC3.OSCMessage()
        # msg.setAddress("/handle")
        # msg.append(position)
        # self.client.send(msg)
        self.client.send_message("/handle", position)

    def reset(self):
        # msg = pyOSC3.OSCMessage()
        # msg.setAddress(f"/reset")
        # msg.append(0)
        # self.client.send(msg)
        self.client.send_message("/reset", 0)


if __name__ == "__main__":
    sc = SuperCollider()
    import time
    sc.send_pos(1)
    time.sleep(1)
    sc.send_pos(2)
    time.sleep(1)
    sc.send_pos(3)
    time.sleep(3)
    sc.reset()

