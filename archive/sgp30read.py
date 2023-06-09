"""@package docstring
    @author Sabrina Button
    @date March 2023
    @description Read eCO2 data from Adafruit SGP30 and ROS publish

    Following this wiring scheme and tutorial: 
    https://learn.adafruit.com/adafruit-sgp30-gas-tvoc-eco2-mox-sensor/circuitpython-wiring-test

    Libraries
    - Adafruit Circuit Python
    - Adafruit Circuit Python SGP30
    - Adafruit Blinka
    
"""

# libraries for reading adafruit SGP30 sensor
import time
import board
import busio
import adafruit_sgp30

# libraries for publishing data via ros
import rospy
from std_msgs.msg import String

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Create library object on our I2C port
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

print("SGP30 serial #", [hex(i) for i in sgp30.serial])

sgp30.set_iaq_baseline(0x8973, 0x8AAE)
sgp30.set_iaq_relative_humidity(celsius=22.1, relative_humidity=44)

# FUNCTION PROVIDED WITH eCO2 SENSOR
# while True:
#     print("eCO2 = %d ppm \t TVOC = %d ppb" % (sgp30.eCO2, sgp30.TVOC))
#     time.sleep(1)
#     elapsed_sec += 1
#     if elapsed_sec > 10:
#         elapsed_sec = 0
#         print(
#             "**** Baseline values: eCO2 = 0x%x, TVOC = 0x%x"
#             % (sgp30.baseline_eCO2, sgp30.baseline_TVOC)
#         )


def CO2_publisher():
    pub = rospy.publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', Anonymous=False)
    rate = rospy.rate(10)
    while not rospy.is_shutdown():
        co2_now = sgp30.eCO2
        rospy.loginfo(co2_now)
        pub.publish(co2_now)
        rate.sleep()


if __name__ == '__main__':
    try:
        CO2_publisher()
    except rospy.ROSInterruptException:
        pass
