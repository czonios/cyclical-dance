# cyclical-dance

## Usage

- Connect your Arduino Nano 33 BLE Sense
- Open serial monitor on Arduino IDE
- Note the mac address of the Arduino
- Enter it in the `main.py` file

```py
python main.py
```

## Prerequisites

### Hardware

- Arduino Nano 33 BLE Sense
- computer with Linux or Windows 10
- BLE dongle or embedded Bluetooth 5 (eg on laptops)


### Software

- Supercollider
- Arduino IDE
- Python 3.9+

Install the following libraries on Arduino IDE

- Arduino Nano 33 BLE boards
- ArduinoBLE
- Arduino_LSM9DS1

You also need these Python libraries:

```py
pip3 install pygatt bleak python-osc
```

or

```py
pip install pygatt bleak python-osc
```