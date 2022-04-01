import smtplib, os, random

from dotenv import load_dotenv

load_dotenv()
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login('kunalbatham15@gmail.com', os.environ.get('password'))
class email_service:
    @staticmethod
    def send_otp(recevier_mail):
        try:
            otp = ""
            for i in range(4):
                otp += str(random.randint(1, 9))
            SUBJECT = "Welcome to Book Store Application"
            TEXT = "Hy,\n Your registration is successfully done.Otp for your Verification is this {}.".format(otp)
            message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
            server.sendmail('kunalbatham15@gmail.com', to_addrs=recevier_mail,msg=message)
        except  Exception as e:
            print(e)
            return "Exception occurred : {}".format(e)


