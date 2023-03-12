import csv
import email
import imaplib
import time
from contextlib import contextmanager
from imap_tools import MailBox
import json

class AutoMail:

    def __init__(self):

        self.csv_file_path = "testemail.csv"
        self.csv_columns = ['msg_ID', 'naam', 'titel', 'beschrijving', 'Casenummer', 'Casedatum']
        self.words_to_check = ['Vraag onderzoek:']
        self.words_to_check1 =[" Casenummer:"]
        self.get_csv_file()
        self.set_account()
        self.get_klachten()

    def get_csv_file(self):
        with open(self.csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.rows = [row for row in reader]

    def set_account(self):
        self.from_email = "@gmail.com"
        self.from_pwd = ""
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993
        self.mailbox = MailBox(self.imap_server).login(self.from_email, self.from_pwd)

    def get_klachten(self):
        with self.mailbox:
            # Search for emails from klachten@dummy.nl
            self.mailbox.folder.set('INBOX')
            #self.mailbox.fetch('FROM "klachten@dummy.nl"')


            # Get the 3 most recent emails
            for msg in self.mailbox.fetch('FROM "klachten@dummy.nl"',limit=10,charset='utf8', reverse=True):
                #print(msg.text)
                # Get the UID of the message
                self.msg_uid = msg.uid


                # Check if the UID is already in the CSV file
                if str(self.msg_uid) in [row['msg_ID'] for row in self.rows]:
                    continue

                # Get the subject of the message
                msg_subject = msg.subject

                # Get the name from the subject
                name = msg_subject.split("name ")[-1]

                # Search for "Vraag onderzoek" in the message body
                for word in self.words_to_check:
                    if word in msg.text:
                        #print(word)
                        self.titel=msg.subject
                        lines = msg.text.splitlines()
                        self.naam_chauffeur = msg.text.startswith('Actieformulier')
                        if self.naam_chauffeur== True:
                            self.naam_chauffeur=msg.text.splitlines()[0]
                            self.naam_chauffeur= self.naam_chauffeur.split()
                            self.naam_chauffeurindex= self.naam_chauffeur.index('name')
                            self.naam_chauffeurindex= self.naam_chauffeurindex+1
                            self.naam_chauffeur = self.naam_chauffeur[self.naam_chauffeurindex:]
                            self.naam_chauffeur=self.naam_chauffeur[0]+"\n" +self.naam_chauffeur[1]
                            print(self.naam_chauffeur)
                            time.sleep(1)


                        try:
                            index = lines.index(word)
                            stop = int(index) + 2
                            self.klacht_beschrijving = "\n".join(lines[index + 1:stop])
                            #print("Klachtbeschrijving: ",  self.klacht_beschrijving)
                            #print("Message after line", index + 1, ":")
                            #print("\n".join(lines[index + 1:stop]))
                            for line in lines:
                                if line.startswith("Casenummer: "):
                                    casenummer = line.split("Casenummer: ")[1].strip()
                                    #print("Casenummer: ", casenummer)
                                    self.caseinfo = casenummer
                                    self.casedatum = casenummer.split()[2]
                                    self.casenummer =casenummer.split()[0]
                                    print(self.casedatum, self.casenummer)
                                    self.writetocsv()

                        except ValueError:
                            print("Word not found in message")
            #print(self.words_to_check1)

    def writetocsv(self):
        # Write the data to the CSV file
        with open(self.csv_file_path, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.csv_columns)
            writer.writerow({'msg_ID': self.msg_uid,
                             'naam': self.naam_chauffeur,
                             'titel': self.titel,
                             'beschrijving': self.klacht_beschrijving,
                             'Casenummer': self.casenummer,
                             'Casedatum': self.casedatum})


if __name__ == "__main__":
    try:
        AutoMail()
    except ValueError as e:
        print(f"An error occurred: {e}")
