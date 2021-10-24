#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>

#define RESET 0
#define TOP_RIGHT 1
#define TOP 2
#define TOP_LEFT 3
#define BOTTOM_LEFT 4
#define BOTTOM 5
#define BOTTOM_RIGHT 6

#define LIMITER 100  // THIS NUMBER NEEDS CALIBRATION
#define RESET_LIMITER 380
#define DELAY_SECONDS 2

// RGB LED
#define RED 22
#define BLUE 24
#define GREEN 23

#define BLE_UUID_DATA_SERVICE "2BEEF31A-B10D-271C-C9EA-35D865C1F48A"
#define BLE_UUID_DATA "4664E7A1-5A13-BFFF-4636-7D0A4B16496C"

BLEService dataService(BLE_UUID_DATA_SERVICE);
BLEByteCharacteristic dataWriter(BLE_UUID_DATA,
                                 BLERead | BLENotify | BLEBroadcast);
// BLECharacteristic dataWriter(BLE_UUID_DATA, BLERead | BLENotify |
// BLEBroadcast, sizeof(uint8_t));

void setup() {
    Serial.begin(9600);
    while (!Serial)
        ;
    Serial.println("Started");

    if (!IMU.begin()) {
        Serial.println("Failed to initialize IMU!");
        while (1)
            ;
    }
    if (!BLE.begin()) {
        Serial.println("BLE failed!");
        while (1)
            ;
    } else {
        BLE.setDeviceName("Cyclical Dance");
        BLE.setLocalName("Cyclical Dance");
        BLE.setAdvertisedService(dataService);
        dataService.addCharacteristic(dataWriter);
        BLE.addService(dataService);
        dataWriter.writeValue(0);
        BLE.advertise();
        String address = BLE.address();

        Serial.print("Local address is: ");
        Serial.println(address);
    }

    // RGB LED
    pinMode(RED, OUTPUT);
    pinMode(BLUE, OUTPUT);
    pinMode(GREEN, OUTPUT);
    digitalWrite(RED, 1);
    digitalWrite(GREEN, 1);
    digitalWrite(BLUE, 1);
    dataWriter.writeValue(0);
}

uint8_t res;
uint8_t res_prev = 7;
unsigned long start_time = millis();
unsigned int red = 1;
unsigned int green = 1;
unsigned int blue = 1;

double normalizeValue(double input) { return (input / 400); }

int computeAngle(double x, double y) {
    double angle_radians = atan2(y, x);
    double angle = (angle_radians * 4068) / 71 + 270;
    int angle360 = (int)angle % 360;
    return angle360;
}

void loop() {
    float x, y, z;

    if (IMU.magneticFieldAvailable()) {
        IMU.readMagneticField(x, y, z);

        if (abs(x) > RESET_LIMITER && abs(y) > RESET_LIMITER &&
            abs(z) > RESET_LIMITER) {
            res = RESET;  // if you step on a magnet you reset the effects
            // Serial.println("RESET");
        } else if (abs(x) > LIMITER || abs(y) > LIMITER) {
            double normX, normY;
            int angle;
            normX = normalizeValue(x);
            normY = normalizeValue(y);
            angle = computeAngle(normX, normY);
            if (angle < 45) {
                res = TOP_RIGHT;
            } else if (angle < 135) {
                res = TOP;
            } else if (angle < 180) {
                res = TOP_LEFT;
            } else if (angle < 225) {
                res = BOTTOM_LEFT;
            } else if (angle < 315) {
                res = BOTTOM;
            } else if (angle < 360) {
                res = BOTTOM_RIGHT;
            }
        } else {
            res = res_prev;
        }
    }

    if (res != res_prev) {
        BLEDevice central = BLE.central();
        if (central && central.connected()) {
            // Serial.print("Central connected: ");
            // Serial.println(central.address());
            dataWriter.writeValue(res);
        }
        Serial.println(res);
        res_prev = res;
        if (res == 0 || res == 7) {
            digitalWrite(RED, 1);
            digitalWrite(GREEN, 1);
            digitalWrite(BLUE, 1);
            delay(DELAY_SECONDS * 1000);
        } else {
            red = (res == 1 || res == 2 || res == 6) ? 0 : 1;
            green = (res == 3 || res == 5 || res == 6) ? 0 : 1;  // 1, 3, 5
            blue = (res == 2 || res == 4 || res == 5) ? 0 : 1;
            digitalWrite(RED, red);
            digitalWrite(GREEN, green);
            digitalWrite(BLUE, blue);
        }
    }
}
