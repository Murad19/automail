import time

from imap_tools import MailBox

import csv
#with open('testemail.csv', 'w+') as f:
 #   print()
class automail():


    def __init__(self):
        print('j')
        self.getcsvfile()
        self.setaccount()
        self.getallemailsfroM()

        


        #self.fromemail="hupelepup@astro.com"
    def getcsvfile(self):

        with open('testmail.csv',newline='') as csvfile:
            spamreader =csv.reader(csvfile, delimiter=' ')
            #for rows in spamreader:
             #   print(rows) as you pleased. like safe the msg.uid in csv so you will not check those you already have checked

                #self.rows=rows
    def setaccount(self):
        ORG_EMAIL = "@gmail.com"
        FROM_EMAIL = "youremailname" + ORG_EMAIL
        FROM_PWD = "Passwoord"#app
        SMTP_SERVER = "imap.gmail.com"
        SMTP_PORT = 993
        self.mailbox = MailBox('imap.gmail.com').login(FROM_EMAIL, FROM_PWD)

    def getallemailsfrom(self):
        print('hello')
        theid=[]
        #self.rows=int(self.rows)


        for msg in self.mailbox.fetch('FROM "searchmailsfromthisemail@astro.com"',charset='utf8'):
            theid=str([msg.uid])
            print(theid)
            theid =msg.uid
            while True:
                try:

                    if theid == self.rows[0::,]:
                        print('already')
                        break

                    elif theid !=self.rows[0::,]:
                        print(msg.uid)
                        break


                        #print(msg.uid)
                        klachtcode = msg.uid



                        time.sleep(.100)
                        #msg.flags(seen=False)

                except:
                    print("--")



    def gettext(self):

        for text in msg.subject:
            #print(msg.subject.)


            x=msg.subject.endswith('x')
            print('.')
            #print(msg.text)



            if msg.subject.endswith('x1'):
                #if

                print("=============")

            elif msg.subject.endswith(('invoice number 777')):
                print(' sauce')
                print("Message id:", msg.uid)
                print("Message Subject:", msg.subject)
                print("Message Date:", msg.date)
                print("=============")


                #MailBox.




automail()


