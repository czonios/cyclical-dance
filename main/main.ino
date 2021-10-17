#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h>

#define RESET 0
#define TOP_LEFT 1
#define TOP_RIGHT 2
#define BOTTOM_RIGHT 3
#define BOTTOM_LEFT 4
#define BOTTOM 5
#define TOP 6

#define LIMITER 100  // THIS NUMBER NEEDS CALIBRATION
#define RESET_LIMITER 380

// RGB LED
#define RED 22
#define BLUE 24
#define GREEN 23

#define BLE_UUID_DATA_SERVICE "2BEEF31A-B10D-271C-C9EA-35D865C1F48A"
#define BLE_UUID_DATA "4664E7A1-5A13-BFFF-4636-7D0A4B16496C"

BLEService dataService(BLE_UUID_DATA_SERVICE);
BLECharacteristic dataWriter(BLE_UUID_DATA, BLERead | BLENotify,
                             sizeof(uint8_t));

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
        dataWriter.writeValue((uint8_t)0x0, sizeof(uint8_t));
        BLE.advertise();
        String address = BLE.address();

        Serial.print("Local address is: ");
        Serial.println(address);
    }

    Serial.print("Magnetic field sample rate = ");
    Serial.print(IMU.magneticFieldSampleRate());
    Serial.println(" uT");
    Serial.println();
    Serial.println("Magnetic Field in uT");
    Serial.println("X\tZ\tRES");

    // RGB LED
    pinMode(RED, OUTPUT);
    pinMode(BLUE, OUTPUT);
    pinMode(GREEN, OUTPUT);
    digitalWrite(RED, 0);
    digitalWrite(GREEN, 0);
    digitalWrite(BLUE, 0);
}

/*We need z, z axis for this use
 *Positive z is forward, positive x in left,
 *keeping the board horizonticaly, barcode facing upwards and forward
 *Gonna use 2d plane for these purpose
 *value range [-400, 400]
 *THIS CODE HAS BEEN WRITTEN FOR 6 MAGNETS OPERATION, ONE FOR EACH STEP-EFFECT
 *e.g. FOR EFFECT ONE YOUR FOOT MAKES CONTACT(OR CLOSE ENOUGH) TO THE MAGNET
 *ALMOST 45DEG from you foot Distance depends on the magnets' power
 */

uint8_t res;
uint8_t res_prev = 7;
unsigned long start_time = millis();
unsigned int red = 0;
unsigned int green = 0;
unsigned int blue = 0;

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
        IMU.readMagneticField(x, z, y);

        if (abs(x) > RESET_LIMITER && abs(y) > RESET_LIMITER &&
            abs(z) > RESET_LIMITER) {
            res = RESET;  // if you step on a magnet you reset the effects
            Serial.println("RESET");
        } else if (abs(x) > LIMITER || abs(z) > LIMITER) {
            double normX, normZ;
            int angle;
            normX = normalizeValue(x);
            normZ = normalizeValue(z);
            angle = computeAngle(normX, normZ);
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
            //            Serial.print(x);
            //            Serial.print('\t');
            //            Serial.print(z);
            //            Serial.print('\t');
            //            Serial.print(angle);
            //            Serial.print('\t');
            //            Serial.println(res);
        }
    }

    if (res != res_prev) {
        BLEDevice central = BLE.central();
        if (central && central.connected()) {
            Serial.println("Central connected!");
            dataWriter.writeValue(&res, sizeof(uint8_t));
        }
        Serial.println(res);
        res_prev = res;
        if (res == 0 || res == 7) {
            digitalWrite(RED, 0);
            digitalWrite(GREEN, 0);
            digitalWrite(BLUE, 0);
        } else {
            red = (res % 3 == 1) ? 1 : 0;
            green = (res % 3 == 2) ? 1 : 0;
            blue = 1;
            digitalWrite(RED, red);
            digitalWrite(GREEN, green);
            digitalWrite(BLUE, blue);
        }
    }
}
