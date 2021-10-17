#!/usr/bin/env python3

import struct
import pygatt
import logging

logging.basicConfig()
logging.getLogger('pygatt').setLevel(logging.DEBUG)
import binascii

LUT = ["RESET", "TOP_LEFT", "TOP_RIGHT", "BOTTOM_RIGHT", "BOTTOM_LEFT", "BOTTOM", "TOP", "INVALID"]
BLE_UUID_DATA_SERVICE = "2BEEF31A-B10D-271C-C9EA-35D865C1F48A"
BLE_UUID_DATA =         "4664E7A1-5A13-BFFF-4636-7D0A4B16496C"
MAC_ADDR =              "c6:d3:74:98:41:c8"

def data_handler_cb(handle, value):
    """
        Indication and notification come asynchronously, we use this function to
        handle them either one at the time as they come.
    :param handle:
    :param value:
    :return:
    """
    print("Handle: {}".format(handle))
    print("Data: {}".format(value.hex()))

def connect_ble():
    
    adapter = pygatt.GATTToolBackend(search_window_size=2048)

    try:
        # Start the adapter
        adapter.start()
        # Connect to the device with that given parameter.
        device = adapter.connect(MAC_ADDR)
        # Set the security level to medium
        # device.bond()
        # Observes the given characteristics for indications.
        # When a response is available, calls data_handle_cb
        while(True):
            value = device.char_read(BLE_UUID_DATA)
            print('value:', value)
            
        device.subscribe(BLE_UUID_DATA,
                         callback=data_handler_cb,
                         indication=True)

        input("Press enter to stop program...\n")

    finally:
        # Stop the adapter session
        adapter.stop()
        pass
    raise NotImplementedError

def setup_supercollider():
    raise NotImplementedError

def read_data(device):
    raise NotImplementedError

def do_reset(device, supercollider):
    raise NotImplementedError

def send_pos(pos, supercollider):
    raise NotImplementedError


def main():
    device = connect_ble()
    supercollider = setup_supercollider()

    while(True):
        pos = read_data(device)
        if LUT[pos] == "RESET":
            do_reset(device, supercollider)
        elif LUT[pos] == "INVALID":
            continue
        else:
            send_pos(pos, supercollider)

if __name__ == "__main__":
    main()