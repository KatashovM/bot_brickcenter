
import aiosmtplib
from email.message import EmailMessage
async def send_mail(host: str, port: int, user: str, password: str,
                    mail_from: str, mail_to: str, subject: str, body: str):
    msg=EmailMessage(); msg["From"]=mail_from; msg["To"]=mail_to; msg["Subject"]=subject; msg.set_content(body)
    await aiosmtplib.send(msg, hostname=host, port=port, start_tls=True, username=user, password=password, timeout=20)
