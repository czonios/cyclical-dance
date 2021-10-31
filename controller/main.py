#!/usr/bin/env python3

import os
from ble import subscribe_ble_linux, subscribe_ble_windows
from supercollider import *
from waveplayerloop import *

LUT = ["RESET", "TOP_RIGHT", "TOP", "TOP_LEFT", "BOTTOM_LEFT", "BOTTOM", "BOTTOM_RIGHT", "INVALID"]
BLE_UUID_DATA_SERVICE = "2BEEF31A-B10D-271C-C9EA-35D865C1F48A"
BLE_UUID_DATA =         "4664E7A1-5A13-BFFF-4636-7D0A4B16496C"
MAC_ADDR =              "c6:d3:74:98:41:c8"
supercollider = None
curr_sample = None


def sample_handler(pos):
    global curr_sample
    if curr_sample is not None:
        curr_sample.stop()
    curr_sample = WavePlayerLoop(filepath=f'../samples/{pos}.wav')
    curr_sample.play()

def data_handler_cb(handle, value):
    """
    Handles incoming notifications from BLE characteristic

    Parameters:
        handle (int): characteristic read handle the data was received on
        value (bytearray): the data returned in the notification
    """
    position = int.from_bytes(value, "big")
    if LUT[position] == "RESET" or LUT[position] == "INVALID":
        do_reset()
    else:
        # supercollider.send_pos(position)
        sample_handler(position)



def do_reset():
    # send reset to SC
    print("RESET")
    # supercollider.reset()
    global curr_sample
    curr_sample.stop()
    curr_sample = None

def main():
    # global supercollider
    # supercollider = SuperCollider()

    # connect to Arduino
    if os.name == 'nt':
        subscribe_ble_windows(MAC_ADDR, BLE_UUID_DATA, data_handler_cb)
    else:
        # subscribe_ble_windows(MAC_ADDR, BLE_UUID_DATA, data_handler_cb)
        subscribe_ble_linux(MAC_ADDR, BLE_UUID_DATA, data_handler_cb)
    
        

if __name__ == "__main__":
    main()