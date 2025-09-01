import smtplib, ssl
from email.message import EmailMessage

def send_email(host: str, port: int, user: str, password: str,
               from_addr: str, to_addr: str, subject: str, body: str) -> bool:
    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        # Try plain (MailHog)
        with smtplib.SMTP(host, port, timeout=10) as server:
            server.send_message(msg)
            print("[email] Sent via plain SMTP (likely MailHog).")
            return True
    except Exception as e_plain:
        print(f"[email] Plain SMTP failed -> {e_plain}. Trying TLS/SSL...")

    # Try SSL or STARTTLS
    try:
        context = ssl.create_default_context()
        if port == 465:
            with smtplib.SMTP_SSL(host, port, context=context, timeout=10) as server:
                if user and password:
                    server.login(user, password)
                server.send_message(msg)
                print("[email] Sent via SMTP SSL.")
                return True
        else:
            with smtplib.SMTP(host, port, timeout=10) as server:
                server.starttls(context=context)
                if user and password:
                    server.login(user, password)
                server.send_message(msg)
                print("[email] Sent via SMTP STARTTLS.")
                return True
    except Exception as e_tls:
        print(f"[email] TLS/SSL send failed -> {e_tls}")
        return False
