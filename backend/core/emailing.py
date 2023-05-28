from smtplib import SMTP
from smtplib import CRLF

class Email:
    def __init__(self, host : str, port : int, username : str, password : str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    
    def send_email(self, sender : str, receivers :list[str], subject : str, body : str) -> bool:
        try:
            smtp = SMTP(self.host, self.port)
            smtp.starttls()
            smtp.login(self.username, self.password)
            
            all_receivers = ", ".join(receivers)
            crlf = CRLF
            message = f"""From: {sender}{crlf}To: {all_receivers}{crlf}Subject: {subject}{crlf}{crlf}{body}"""

            smtp.sendmail(sender, receivers, message)
            smtp.quit()
            return True
        except Exception as ex:
            print(ex)
            return False


#how to use
""" from core.emailing import Email
from core.config import settings

email = Email(settings.EMAIL_HOST, settings.EMAIL_PORT, settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
result = email.send_email(settings.EMAIL_USERNAME, ["test1@gmail.com", "test2@gmail.com"], "test subject", "test body")
print(result) """