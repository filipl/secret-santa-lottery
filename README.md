Secret Santa Lottery
====================

Small utility to decide who to give presents to in a secret santa game.

Example Usage
-------------

```
python secret_santa.py --message-file example_message.txt "John Doe <john@example.com>" "Jane Doe <jane@example.com>"
```

Help
----

```
usage: secret_santa.py [-h] [--smtp SMTP] [--tls] [--port PORT]
                       [--username USERNAME] [--password PASSWORD]
                       [--sender SENDER] [--subject SUBJECT] --message-file
                       PATH [--ignore-warnings]
                       person [person ...]

Sceret Santa Lottery

positional arguments:
  person               A participant in the lottery - "Name <email>"

optional arguments:
  -h, --help           show this help message and exit
  --smtp SMTP          SMTP server
  --tls                Use TLS
  --port PORT
  --username USERNAME  Username for SMTP login
  --password PASSWORD  Password for SMTP login
  --sender SENDER      Sender email address
  --subject SUBJECT    Mail subject
  --message-file PATH  Message file
  --ignore-warnings    Ignore warnings about the message file
```
