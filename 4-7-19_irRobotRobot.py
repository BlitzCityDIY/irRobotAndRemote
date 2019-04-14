import pulseio
import board
import adafruit_irremote
import time
from adafruit_crickit import crickit

motor_1 = crickit.dc_motor_1
motor_2 = crickit.dc_motor_2

# Create a 'pulseio' input, to listen to infrared signals on the IR receiver
pulsein = pulseio.PulseIn(board.IR_RX, maxlen=120, idle_state=True)
# Create a decoder that will take pulses and turn them into numbers
decoder = adafruit_irremote.GenericDecode()

while True:
    pulses = decoder.read_pulses(pulsein)
    try:
        # Attempt to convert received pulses into numbers
        received_code = decoder.decode_bits(pulses, debug=False)
    except adafruit_irremote.IRNECRepeatException:
        # We got an unusual short code, probably a 'repeat' signal
        # print("NEC repeat!")
        continue
    except adafruit_irremote.IRDecodeException as e:
        # Something got distorted or maybe its not an NEC-type remote?
        # print("Failed to decode: ", e.args)
        continue

    #  print("NEC Infrared code received: ", received_code)
    if received_code == [255, 2, 255, 0]:
        #  print("forward")
        motor_1.throttle = -0.5
        motor_2.throttle = -0.5 # half speed backward
        time.sleep(0.001)
    if received_code == [255, 2, 127, 128]:
        #  print("back")
        motor_1.throttle = 0.5
        motor_2.throttle = 0.5 # half speed backward
        time.sleep(0.001)
    if received_code == [255, 2, 100, 22]:
        #  print("left")
        motor_1.throttle = -0.5
        motor_2.throttle = 0.5 # half speed backward
        time.sleep(0.001)
    if received_code == [255, 2, 164, 0]:
        #  print("right")
        motor_1.throttle = 0.5
        motor_2.throttle = -0.5 # half speed backward
        time.sleep(0.001)
    if received_code == [255, 2, 191, 64]:
        #  print("stop")
        motor_1.throttle = 0
        motor_2.throttle = 0 # stop
        time.sleep(0.001)