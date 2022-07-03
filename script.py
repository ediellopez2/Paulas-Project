import variables        # Stores my Google Email & Password
import requests                           # Web Scraping
from bs4 import BeautifulSoup             # Web Scraping
import smtplib                            # Send Email
from email.message import EmailMessage    # Send Email
from twilio.rest import Client            # Twilio
from datetime import datetime             # Display Time
import time                               # Go To Sleep


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


if __name__ == "__main__":
    while True:
        try:
            message = datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__() + ": Test Message"

            send_sms(variables.number_ediel, message)

            time.sleep(30)  # 30 seconds
            # =======================================================================
        except requests.exceptions.ConnectionError as errc:
            # In the event of a network problem (e.g. DNS failure, refused connection, etc),
            # Requests will raise a ConnectionError exception.
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.")
            print(errc.__str__())

            # Sleep for 1 minute and try to run the program again.
            time.sleep(60)  # 1 minute
            continue
        except Exception as exc:
            # This block will execute when an unexpected error that is unrelated to connection error occurs.
            errorMessage = "AN ERROR OCCURRED AT " + datetime.now().strftime('%Y-%m-%d %H:%M:%S').__str__() + "!\n"
            print(errorMessage + "Here is the specific error:\n" + exc.__str__())

            send_sms(variables.number_ediel, errorMessage)
            break
