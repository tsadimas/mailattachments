#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 10:03:57 2020

@author: thomas
"""

import sys, getopt
import csv
import smtplib, ssl
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

USAGE = 'Usage: python mailsubjects.py -i <inputcsvfile> -l <logfile> -e <emailbodyfile> -u <sender mail address>, -p <password> \
        -s <subject mail>'
        
EMAIL_INDEX = 6
ATTACHMENT_INDEX = 5
SMTP = 'mail.staff.hua.gr'
PORT = 587


def readCsv(filename, attachmentIndex, emailIndex):
    
    csvData = []
    with open(filename) as csvFile:
        lineCount = 0
        csvReader = csv.reader(csvFile, delimiter = ';')
        for row in csvReader:
            if lineCount > 0:
               
                csvData.append({'email' : row[emailIndex],
                                'attachment' : row[attachmentIndex]})
    
            lineCount += 1
        print('Read %d lines' % lineCount)
        
    return csvData

def mailLogin(sender_email, password, smtpServer, port):
    
    context = ssl.create_default_context()
    
    print('attempting login to %s' % smtpServer)
    
    try:
        server = smtplib.SMTP(smtpServer,port)        
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        print('Login successful')
    
    except Exception as e:
    # Print any error messages to stdout
        print(e)

    
    return server

def buildMail(sender, recipient, subject, body, attachment = None):
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body))
    if attachment is not None:
        with open(attachment,"rb") as fil:
            part = MIMEApplication( fil.read(), Name = basename(attachment) )
            
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(attachment)
        msg.attach(part)
    
    return msg

def parseConfigFile(fileName):
    
    d = {}
    with open(fileName) as f:
        line = f.readline()
        while line:
            if ': ' in line:
                s = line.split(': ')
                key = s[0]
                value = s[1].strip('\n')
                d[key] = value
            line = f.readline()
    return d

            
def sendMails(server, data, subject, body, sender, logFile):
    
    with open(logFile,'w') as f:
        for entry in data:
            recipient = entry['email']
            attachment = entry['attachment']
            now = datetime.now()
            outputStr = '[%s] Sending %s exam paper %s' %(now.strftime("%H:%M:%S.%f"), recipient, attachment)
            print(outputStr)
            print(outputStr, file = f)
            try:        
                msg = buildMail(sender, recipient, subject, body, attachment = attachment)
                server.sendmail(sender, recipient, msg.as_string())
                now = datetime.now()
                outputStr = '[%s] Message sent' % now.strftime("%H:%M:%S.%f")         
            except Exception as e:
                outputStr = '[%s] Message could not be sent : %s' % (now.strftime("%H:%M:%S.%f"), e)
                
            print(outputStr)
            print(outputStr, file = f)
            
    
    
def main(argv):
    print(argv)
    inputFile = ''
    logFile = ''
    emailBodyFile = ''
    subject = ''
    sender = ''
    password = ''
    configFile = ''
    smtp = SMTP
    port = PORT
    emailIndex = EMAIL_INDEX
    attachmentIndex = ATTACHMENT_INDEX
    
    try:
        opts, args = getopt.getopt(argv,"hc:i:l:e:s:u:p:",["config=","input=","logfile=","emailbody=",'subject=','sender=','password='])
    except getopt.GetoptError:
        
        print(USAGE)
        sys.exit(2)
        
    for opt, arg in opts:
        print(opt)
        if opt == '-h':
           print(USAGE)
           sys.exit()
        elif opt in ("-c", "--config"):
            configFile = arg
        elif opt in ("-i", "--input"):
            inputFile = arg
        elif opt in ("-l", "--logfile"):
            logFile = arg
        elif opt in ("-e", "--emailbody"):
            emailBodyFile = arg
        elif opt in ("-s", "--subject"):
            subject = arg
        elif opt in ("-u", "--sender"):
            sender = arg
        elif opt in ("-p", "--password"):
            password = arg
            
    
    if configFile != '':
        d = parseConfigFile(configFile)        
        inputFile = d['input']
        sender = d['sender']
        smtp = d['server']
        logFile = d['logfile']
        port = d['port']
        password = d['password']
        subject = d['subject']
        emailBodyFile = d['emailbody']
        emailIndex = int(d['emailindex'])
        attachmentIndex = int(d['attachmentindex'])
        
    if inputFile == '':
        print('You need to specify an input csv file')
        sys.exit(2)
    
    if logFile == '':
        print('You need to specify an output log file')
        sys.exit(2)
        
    if emailBodyFile == '':
        print('You need to specify an email body file')
        sys.exit(2)
    
    if subject == '':
        print('You need to specify a subject text')
        sys.exit(2)
        
    if sender == '':
        print('You need to specify a sender email account')
        sys.exit(2)
        
    if password == '':
        print('You need to specify a password for your email account')
        sys.exit(2)
    
    
    print("Beginning execution")
    print("Input csv file is ",inputFile)
    print("Output log file is ",logFile)
    print("Mail body file is ",emailBodyFile)
    
    with open(emailBodyFile,"r") as f:
        body = f.read()
    
    print("Message body reads:\n %s" %body)
    
    data = readCsv(inputFile, attachmentIndex, emailIndex)
    server = mailLogin(sender, password, smtp, port)
    
    sendMails( server, data, subject, body, sender, logFile )
    server.quit()
    
if __name__ == "__main__":
   main(sys.argv[1:])    
    
    