#!/usr/bin/env python3
"""Send an email via Gmail SMTP using an App Password.

Reads credentials from environment:
    GMAIL_USER          sending account, defaults to antoshashakov@gmail.com
    GMAIL_APP_PASSWORD  Gmail App Password for that account (required)

Usage:
    python send_email.py --to <addr> --subject "<subj>" --body "<body>"
    python send_email.py --to <addr> --subject "<subj>" --body-file <path>
"""

import argparse
import json
import os
import socket
import sys
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Force IPv4 BEFORE importing smtplib. Some sandboxes (Anthropic Cloud, some
# CI runners) have an IPv6 stack that errors with [Errno 97] EAFNOSUPPORT
# when smtplib tries to open an AF_INET6 socket. Restricting getaddrinfo to
# AF_INET makes smtplib resolve to IPv4 and open AF_INET sockets only.
_orig_getaddrinfo = socket.getaddrinfo
def _ipv4_only_getaddrinfo(host, port, family=0, *args, **kwargs):
    return _orig_getaddrinfo(host, port, socket.AF_INET, *args, **kwargs)
socket.getaddrinfo = _ipv4_only_getaddrinfo

import smtplib  # noqa: E402  (import after monkey-patch)

SMTP_HOST = "smtp.gmail.com"
TIMEOUT = 20


def _build_msg(to_addr, subject, body, sender, reply_to):
    msg = MIMEMultipart()
    msg["From"] = f"mathAI bot <{sender}>"
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg["Date"] = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    if reply_to:
        msg["Reply-To"] = reply_to
    msg.attach(MIMEText(body, "plain", "utf-8"))
    return msg


def send(to_addr: str, subject: str, body: str, sender: str, password: str, reply_to: str = None) -> dict:
    """Try SMTPS:465, then STARTTLS:587, then plain SMTP:25 with STARTTLS.

    Many sandboxed networks (Anthropic Cloud's runner among them) silently
    drop outbound to 465. 587 is the canonical client-submission port and
    is more frequently allowed. We attempt them in order and report which
    transport succeeded.
    """
    msg = _build_msg(to_addr, subject, body, sender, reply_to)
    errors = []

    # 1. SMTPS on 465 (implicit TLS)
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, 465, timeout=TIMEOUT) as server:
            server.login(sender, password)
            server.send_message(msg, to_addrs=[to_addr])
        return {"status": "sent", "transport": "smtps:465", "to": to_addr,
                "subject": subject, "from": sender, "reply_to": reply_to}
    except Exception as e:
        errors.append(f"smtps:465 -> {type(e).__name__}: {e}")

    # 2. SMTP+STARTTLS on 587 (submission)
    try:
        with smtplib.SMTP(SMTP_HOST, 587, timeout=TIMEOUT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(sender, password)
            server.send_message(msg, to_addrs=[to_addr])
        return {"status": "sent", "transport": "starttls:587", "to": to_addr,
                "subject": subject, "from": sender, "reply_to": reply_to,
                "fallback_from": errors[0]}
    except Exception as e:
        errors.append(f"starttls:587 -> {type(e).__name__}: {e}")

    raise RuntimeError("All SMTP transports failed: " + " | ".join(errors))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--to", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--reply-to", default=os.environ.get("REPLY_TO"))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--body")
    group.add_argument("--body-file")
    args = parser.parse_args()

    sender = os.environ.get("GMAIL_USER", "antoshashakov@gmail.com")
    password = os.environ.get("GMAIL_APP_PASSWORD")
    if not password:
        print(json.dumps({"status": "error", "error": "GMAIL_APP_PASSWORD env var not set"}))
        sys.exit(1)

    body = args.body if args.body is not None else open(args.body_file, encoding="utf-8").read()

    try:
        result = send(args.to, args.subject, body, sender, password, reply_to=args.reply_to)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e), "type": type(e).__name__}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
