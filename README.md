# Paulas-Project
My mother, Paula, suffers from chronic health problems and it requires that I check up on her multiple times throughout the day. Since she does not own a cell phone, I have decided to build a solution that allows her to reach me at the push of a button. At this time, I have 3 requests set up. They are **1: I need help**, **2: Call me**, and **3: YouTube**. I included **3: YouTube** as a request because my mother likes to watch YouTube videos at the of the day. 

This solution gives my mother back her independence as I no longer have to hover over her shoulder throughout the day. This also allows me to focus more on my work as I work from home at this time.

## Hardware & Software Needed
- Raspberry Pi
- IR (Infrared) Receiver Sensor (TSOP38238) from Adafruit Industries
- Mini Remote Control from Adafruit Industries
- Twilio (https://www.twilio.com/sms/pricing/us)


## Resources & References
#### https://github.com/Lime-Parallelogram/pyIR
I used this program to get the HEX codes from the IR receiver. See remote.txt.

#### https://github.com/Lime-Parallelogram/IR-Code-Referencer
I used Final-From-Video.py from this repo to read any incoming button clicks. I simply added the email and sms functionality to that script. See script.py.


## Visuals
![Text Messages Screenshot](images/messages.jpg)
![Hardware](images/hardware.jpg)
