#!/usr/bin/env python3

import time
import pygatt
import os
from supercollider import *

LUT = ["RESET", "TOP_RIGHT", "TOP", "TOP_LEFT", "BOTTOM_LEFT", "BOTTOM", "BOTTOM_RIGHT", "INVALID"]
BLE_UUID_DATA_SERVICE = "2BEEF31A-B10D-271C-C9EA-35D865C1F48A"
BLE_UUID_DATA =         "4664E7A1-5A13-BFFF-4636-7D0A4B16496C"
MAC_ADDR =              "c6:d3:74:98:41:c8"
supercollider = None

def triggerEvent(checkdata):
   print(str(checkdata))

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
        supercollider.send_pos(position)

def connect_ble():
    adapter = pygatt.GATTToolBackend()

    # Start the adapter
    adapter.start(reset=False)
    
    # Connect to the device with that given parameter.
    device = adapter.connect(MAC_ADDR, timeout=1000)
    time.sleep(0.1)
    return device, adapter

def do_reset():
    # send reset to SC
    print("RESET")
    supercollider.reset()


def main():
    try:
        global supercollider
        supercollider = SuperCollider()
    except:
        print("Could not connect to supercollider server.")
        exit(1)

    try:
        # connect to Arduino
        if os.name == 'nt':
            print("Windows...")
            import asyncio
            from bleak import BleakClient


            async def test():
                async with BleakClient(MAC_ADDR) as client:
                    await asyncio.sleep(0.1)
                    print(f"Connected: {client.is_connected}")
                    while 1:
                        # d = await client.read_gatt_char(BLE_UUID_DATA)
                        # print('d:', d)
                        # data_handler_cb(None, d)
                        await client.start_notify(BLE_UUID_DATA, data_handler_cb)
                    input("Press enter to stop program...\n")
                    await client.stop_notify(BLE_UUID_DATA)

            asyncio.run(test())
        else:
            device, adapter = connect_ble()
            # subscribe to data characteristic
            device.subscribe(BLE_UUID_DATA,
                        callback=data_handler_cb)
            input("Press enter to stop program...\n")
            adapter.stop()
    finally:
        pass
        

if __name__ == "__main__":
    main()