import time
import pygatt
import asyncio
from bleak import BleakClient

def connect_ble_linux(MAC_ADDR):
    adapter = pygatt.GATTToolBackend()

    # Start the adapter
    adapter.start(reset=False)
    
    # Connect to the device with that given parameter.
    device = adapter.connect(MAC_ADDR, timeout=1000)
    time.sleep(0.1)
    return device, adapter

def subscribe_ble_linux(MAC_ADDR, BLE_UUID_DATA, data_handler_cb):
    device, adapter = connect_ble_linux()
    # subscribe to data characteristic
    device.subscribe(BLE_UUID_DATA,
                callback=data_handler_cb)
    input("Press enter to stop program...\n")
    adapter.stop()

async def connect_ble_windows(MAC_ADDR, BLE_UUID_DATA, data_handler_cb):
    client = BleakClient(MAC_ADDR)
    try:
        print("Awaiting connection...")
        await client.connect(timeout=1000)
        asyncio.sleep(0.1)
        print("Connected to BLE")
        await client.start_notify(BLE_UUID_DATA, data_handler_cb)
        while 1:
            if not client.is_connected:
                break
            # d = await client.read_gatt_char(BLE_UUID_DATA, use_cached=False)
            # data_handler_cb(None, d)
            await asyncio.sleep(5.0)#, loop=asyncio.get_event_loop())
        print("Connection to BLE broken")
        await client.stop_notify(BLE_UUID_DATA)
        await client.disconnect()
    except Exception as e:
        print("An error occured in BLE connection:", e)
    finally:
        await client.disconnect()



def subscribe_ble_windows(MAC_ADDR, BLE_UUID_DATA, data_handler_cb):
    asyncio.run(connect_ble_windows(MAC_ADDR, BLE_UUID_DATA, data_handler_cb))