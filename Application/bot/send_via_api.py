#!/usr/bin/env python3
"""Send email via Gmail HTTPS API (port 443) using an OAuth refresh token.

Reads credentials from environment:
    GMAIL_USER            sending account email (e.g. antoshashakov@gmail.com)
    GMAIL_CLIENT_ID       OAuth 2.0 client id
    GMAIL_CLIENT_SECRET   OAuth 2.0 client secret
    GMAIL_REFRESH_TOKEN   long-lived refresh token

Avoids SMTP entirely (the Anthropic Cloud sandbox blocks outbound 465/587).
Talks to https://oauth2.googleapis.com/token + https://gmail.googleapis.com
on port 443, which is allowed.

Usage:
    python send_via_api.py --to <addr> --subject "<subj>" --body "<body>"
    python send_via_api.py --to <addr> --subject "<subj>" --body-file <path>
"""
import argparse
import base64
import json
import os
import sys
import urllib.parse
import urllib.request
from email.mime.text import MIMEText


def get_access_token(client_id: str, client_secret: str, refresh_token: str) -> str:
    data = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())["access_token"]


def send(access_token: str, sender: str, to_addr: str, subject: str,
         body: str, reply_to: str | None) -> dict:
    msg = MIMEText(body, "plain", "utf-8")
    msg["From"] = f"mathAI bot <{sender}>"
    msg["To"] = to_addr
    msg["Subject"] = subject
    if reply_to:
        msg["Reply-To"] = reply_to
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    payload = json.dumps({"raw": raw}).encode()
    req = urllib.request.Request(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        data=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--to", required=True)
    p.add_argument("--subject", required=True)
    p.add_argument("--reply-to", default=os.environ.get("REPLY_TO"))
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--body")
    g.add_argument("--body-file")
    args = p.parse_args()

    sender = os.environ.get("GMAIL_USER")
    client_id = os.environ.get("GMAIL_CLIENT_ID")
    client_secret = os.environ.get("GMAIL_CLIENT_SECRET")
    refresh_token = os.environ.get("GMAIL_REFRESH_TOKEN")
    missing = [k for k, v in [
        ("GMAIL_USER", sender),
        ("GMAIL_CLIENT_ID", client_id),
        ("GMAIL_CLIENT_SECRET", client_secret),
        ("GMAIL_REFRESH_TOKEN", refresh_token),
    ] if not v]
    if missing:
        print(json.dumps({"status": "error", "error": f"missing env vars: {missing}"}))
        sys.exit(1)

    body = args.body if args.body is not None else open(args.body_file, encoding="utf-8").read()

    try:
        token = get_access_token(client_id, client_secret, refresh_token)
        result = send(token, sender, args.to, args.subject, body, args.reply_to)
        print(json.dumps({"status": "sent", "transport": "gmail-api:https",
                          "id": result.get("id"), "threadId": result.get("threadId"),
                          "to": args.to, "from": sender}, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e),
                          "type": type(e).__name__}, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
