#!/usr/bin/env python

import random
import smtplib
from email.mime.text import MIMEText
import argparse
import re

parser = argparse.ArgumentParser(description="Sceret Santa Lottery")

def participant(str):
    ms = re.match("(.*) <(.*)>", str)
    if not ms:
        raise argparse.ArgumentTypeError("%s is not a person" % (str))
    return ms.groups()

def body_file(filename):
    try:
        body = open(filename, "r").read()
    except FileNotFoundError:
        raise argparse.ArgumentTypeError("unable to find file %s" % (filename))
    return body

parser.add_argument("persons", metavar="person", nargs="+",
    help="A participant in the lottery - \"Name <email>\"", type=participant)
parser.add_argument("--smtp", default="localhost", help="SMTP server")
parser.add_argument("--tls", action="store_true", help="Use TLS")
parser.add_argument("--port", type=int, default=25)
parser.add_argument("--username", help="Username for SMTP login")
parser.add_argument("--password", help="Password for SMTP login")
parser.add_argument("--sender", default="lottery@example.com",
    help="Sender email address")
parser.add_argument("--subject", default="Lottery!", help="Mail subject")
parser.add_argument("--message-file", type=body_file, help="Message file",
    dest="path", required=True)
parser.add_argument("--ignore-warnings", dest="ignore_warns", action="store_true",
    help="Ignore warnings about the message file")

args = parser.parse_args()

SMTP_SERVER = args.smtp
MAIL_SENDER = args.sender
MAIL_SUBJECT = args.subject
MAIL_BODY = args.path

if not args.ignore_warns:
    for p in ["{giver_name}", "{receiver_name}"]:
        if p not in MAIL_BODY:
            print("warning: '%s' not used in message." % (p,))
            exit(1)

givers = args.persons[:]
receivers = givers[:]

random.seed()

def get_receiver(giver):
    global receivers
    candidates = list(filter(lambda r: r != giver, receivers))
    if len(candidates) == 0:
        print("only one person left in lottery with noone to give to - try again.")
        exit(1)
    receiver = random.choice(candidates)
    receivers = list(filter(lambda r: r != receiver, receivers))
    return receiver

matches = {}
for giver in givers:
    receiver = get_receiver(giver)
    matches[giver] = receiver

def mail_person(giver, receiver):
    me = MAIL_SENDER
    body = MAIL_BODY.format(giver_name=giver[0], receiver_name=receiver[0])
    msg = MIMEText(body)
    msg['Subject'] = MAIL_SUBJECT
    msg['From'] = me
    msg['To'] = giver[1]

    s = smtplib.SMTP(host=SMTP_SERVER, port=args.port)
    s.ehlo()
    if args.tls:
        s.starttls()
    if args.username and args.password:
        s.login(args.username, args.password)
    s.sendmail(me, [giver[1]], msg.as_string())
    s.quit()

for g, r in matches.items():
    mail_person(g, r)

print("done.")
