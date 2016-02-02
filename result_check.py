import urllib2
from bs4 import BeautifulSoup
import difflib
from twilio.rest import TwilioRestClient
import smtplib
from datetime import datetime


def send_email(recipient, body):
    import smtplib

    gmail_user = <your_email_id>        #edit your info
    gmail_pwd = <your_password>        #edit your info
    FROM = <from_email_id>        #edit your info
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = <subject_of_email>        #edit your info
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"



#SMS configuration
accountSid = <your_acc_sid>        #edit your info
authToken = <your_acc_auth_token>        #edit your info
twilioClient = TwilioRestClient(accountSid, authToken)
myTwilioNumber = <your_twilio_number>        #edit your info
destCellPhone = <registered_twilio_number>        #edit your info


url = <website_you_want_to_keep_an_eye_on>        #edit your info

#opening the webpage
res = urllib2.urlopen(url)
page = res.read()

#picking the name for the new file
a = open(<path_to_your_local_flag_text_file>, 'r+')        #edit your info
cont = int(a.read())
now = str(cont + 1)
a.seek(0)
a.write(str(now))
a.close()


#Send a message verifying a well running script and not at night
currhr = datetime.strftime(datetime.now(), '%H')
if(int(now)%6==0):
    if(currhr != 00 or currhr != 01 or currhr != 02 or currhr != 03 or currhr != 04 or currhr != 05):
        msg = "Script is running properly!"
        myMessage = twilioClient.messages.create(body = msg, from_=myTwilioNumber, to=destCellPhone)


#naming the new page and storing website's current state
f = open('results' + str(now) + '.html', 'w')
f.write(page)
f.close()

#converting pages to text
f = open('results' + str(cont) + '.html', 'r+')
fp = f.read()

s = open('results' + str(now) + '.html', 'r+')
sp = s.read()


#comparing text
comp = difflib.SequenceMatcher(None, fp, sp)
ratio = comp.ratio()

if(ratio!=1):
	msg = ("The page seems to have changed. The change ratio is: %f" % ratio)
	myMessage = twilioClient.messages.create(body = msg, from_=myTwilioNumber, to=destCellPhone)
	send_email(<receivers_email>, msg)     #edit your info
	print "Messages were sent!"
else:
	print "It's all the same most probably..."


os.system("D:/Py/wait_until_sleep.py")              #edit your own info