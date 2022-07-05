# Imports modules
import variables        # Stores my Google Email & Password
from twilio.rest import Client            # Twilio
import smtplib                            # Send Email
from email.message import EmailMessage    # Send Email
import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep

# Static program vars
pin = 5  # Input pin of sensor (GPIO.BOARD)
Buttons = [0x300fd00ff, 0x300fd807f, 0x300fd40bf, 0x300fd20df, 0x300fda05f, 0x300fd609f, 0x300fd10ef, 0x300fd906f, 0x300fd50af, 0x300fd30cf, 0x300fdb04f, 0x300fd708f, 0x300fd08f7, 0x300fd8877, 0x300fd48b7, 0x300fd28d7, 0x300fda857, 0x300fd6897, 0x300fd18e7, 0x300fd9867, 0x300fd58a7]  # HEX code list
ButtonsNames = ["volumeDown", "playPause", "volumeUp", "setup", "previous", "stopMode", "channelDown", "enterSave", "channelNext", "zeroTen", "next", "previous", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]# String list in same order as HEX list

# Sets up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN)

# Gets binary value
def getBinary():
    # Internal vars
    num1s = 0  # Number of consecutive 1s read
    binary = 1  # The binary value
    command = []  # The list to store pulse times in
    previousValue = 0  # The last value
    value = GPIO.input(pin)  # The current value

    # Waits for the sensor to pull pin low
    while value:
        sleep(0.0001) # This sleep decreases CPU utilization immensely
        value = GPIO.input(pin)
        
    # Records start time
    startTime = datetime.now()
    
    while True:
        # If change detected in value
        if previousValue != value:
            now = datetime.now()
            pulseTime = now - startTime #Calculate the time of pulse
            startTime = now #Reset start time
            command.append((previousValue, pulseTime.microseconds)) #Store recorded data
            
        # Updates consecutive 1s variable
        if value:
            num1s += 1
        else:
            num1s = 0
        
        # Breaks program when the amount of 1s surpasses 10000
        if num1s > 10000:
            break
            
        # Re-reads pin
        previousValue = value
        value = GPIO.input(pin)
        
    # Converts times to binary
    for (typ, tme) in command:
        if typ == 1: #If looking at rest period
            if tme > 1000: #If pulse greater than 1000us
                binary = binary *10 +1 #Must be 1
            else:
                binary *= 10 #Must be 0
            
    if len(str(binary)) > 34: #Sometimes, there is some stray characters
        binary = int(str(binary)[:34])
        
    return binary
    
# Convert value to hex
def convertHex(binaryValue):
    tmpB2 = int(str(binaryValue),2) #Temporarely propper base 2
    return hex(tmpB2)



def send_email(subject, recipient, message):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = variables.EMAIL_USER
    msg['To'] = recipient
    msg.set_content(message)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(variables.EMAIL_USER, variables.EMAIL_PASS)
        smtp.send_message(msg)


def send_sms(recipient, message):
    client = Client(variables.TWILIO_ACCOUNT_SID, variables.TWILIO_AUTH_TOKEN)

    client.messages.create(
        body=message,
        from_=variables.number_twilio,
        to=recipient
    )
    return


while True:
    inData = convertHex(getBinary()) #Runs subs to get incoming hex value
    for button in range(len(Buttons)):#Runs through every value in list
        if hex(Buttons[button]) == inData: #Checks this against incoming
            print(ButtonsNames[button]) #Prints corresponding english name for button
            if (str(ButtonsNames[button]) == 'one'):
                message = "I need help"
                send_email(str(ButtonsNames[button]), variables.EMAIL_TO_EDIEL, message)
                send_sms(variables.number_ediel, message)
            elif (str(ButtonsNames[button]) == 'two'):
                message = "Call me"
                send_email(str(ButtonsNames[button]), variables.EMAIL_TO_EDIEL, message)
                send_sms(variables.number_ediel, message)
            elif (str(ButtonsNames[button]) == 'three'):
                message = "YouTube"
                send_email(str(ButtonsNames[button]), variables.EMAIL_TO_EDIEL, message)
                send_sms(variables.number_ediel, message)
