import time
from board import SCL, SDA
import board
import adafruit_irremote
import pulseio
import busio
from adafruit_seesaw.seesaw import Seesaw

i2c_bus = busio.I2C(SCL, SDA)

pwm = pulseio.PWMOut(board.D4, frequency=38000, duty_cycle=2 ** 15)
pulseout = pulseio.PulseOut(pwm)
# Create an encoder that will take numbers and turn them into NEC IR pulses
encoder = adafruit_irremote.GenericTransmit(header=[9500, 4500], one=[550, 550],
                                            zero=[550, 1700], trail=0)
 
ss = Seesaw(i2c_bus)

ss.pin_mode(9, ss.INPUT_PULLUP)

last_x = 0
last_y = 0
 
while True:
    x = ss.analog_read(2)
    y = ss.analog_read(3)
    b = ss.digital_read(9)

    if not b:
            encoder.transmit(pulseout, [255, 2, 191, 64])
            time.sleep(.01)
    if (abs(x - last_x) > 3) or (abs(y - last_y) > 3):
        #  print(x, y)
        last_x = x
        last_y = y
        if x > 500 and y > 995:
            #  cpx.pixels.fill((50, 0, 0))
            encoder.transmit(pulseout, [255, 2, 255, 0])
            time.sleep(.01)
            #  forward
        if x < 10 and y > 500:
            #  cpx.pixels.fill((0, 50, 0))
            encoder.transmit(pulseout, [255, 2, 100, 22])
            time.sleep(.01)
            #  left
        if x > 995 and y > 500:
            #  cpx.pixels.fill((0, 0, 50))
            encoder.transmit(pulseout, [255, 2, 164, 0])
            time.sleep(.01)
            #  right
        if x > 500 and y < 10:
            #  cpx.pixels.fill((0, 0, 50))
            encoder.transmit(pulseout, [255, 2, 127, 128])
            time.sleep(.01)
            #  back