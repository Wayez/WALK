import time
#import email seinding function
import smtplib
#imports code for generating emails
from email.mime.text import MIMEText


#creates a log in the users log file with a message and a timestamp
#returns True upon successful completion
def log(user, message):
    try:
        #open file at logs/user"
        logFile = open("logs/"+user+".txt","a")

        #generate timestamp
        currentTime = time.strftime("%c")

        #write message to file
        logFile.write(currentTime+": "+message+"\n")
        logFile.close()
        return True
    except:
        #you're actuall pretty screwed... you can't exactly read the log file if the log function is broken...
        return False

#sends an email from the addres: walksciencebowl@gmail.com to user
#returns True upon successful completion, otherwise returns false and makes a log in the user's logs file
def email(user, subject, message):
    try:
        #open connection to gmail login sever
        #ports may need to be updated if google updates their smtp server
        s = smtplib.SMTP('smtp.gmail.com',587)
        
        #sets mode to extended smtp
        s.ehlo()

        #start connection encryption
        s.starttls()
        
        #login to walksciencebowl@gmail.com
        s.login("walksciencebowl@gmail.com","wayezisthecooliest")
        
        
        message = MIMEText(message)
        message["Subject"] = subject
        sender = message["From"] = "walksciencebowl@gmail.com"
        recipient = message["To"] = user
        s.sendmail(sender, [recipient], message.as_string())
        
        s.quit()
        return True
    except:
        log(user,"unable to send message: "+message)
        return False
