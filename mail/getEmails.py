import imaplib
import email
from email.header import decode_header
from sendApi import SendMail

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login("email", "password")
mail.select("inbox")

#  UNSEEN
status, messages = mail.search(None, "UNSEEN")
if status == "OK":
    print("Connexion réussie à la boîte de réception.")

mail_ids = messages[0].split()

if not mail_ids:
    print("Aucun email trouvé.")
else:
    for mail_id in mail_ids:
        status, msg_data = mail.fetch(mail_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                
                from_email = msg.get("From")
        
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode()
                            print(f"Email reçu de: {from_email}\nSujet: {subject}\nCorps: {body}\n")
                            data = {
                                "to":from_email,
                                "subject":subject,
                                "message":body
                               }

                            SendMail(data)
                            
                        elif "attachment" in content_disposition:
                            pass
                else:
                    body = msg.get_payload(decode=True).decode()
                    print(f"Email reçu de: {from_email}\nSujet: {subject}\nCorps: {body}\n")
                    data = {
                        "to":from_email,
                         "subject":subject,
                         "message":body
                    }

                    SendMail(data)

mail.logout()
