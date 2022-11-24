import time
import board
import busio
import adafruit_adxl34x

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)

def acel():
    
    #print("%f %f %f"%accelerometer.acceleration)
    time.sleep(0.1)
    acel = accelerometer.acceleration
    X = acel[0]
    Y = acel[1]
    Z = acel[2]
    #print(acel)
    time.sleep(1)
        
    return X, Y, Z,
