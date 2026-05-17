#!/usr/bin/env python3
"""Fetch unread Gmail replies to mathAI bot emails via Gmail HTTPS API.

Reads credentials from environment (same as bot/send_via_api.py):
    GMAIL_USER            account email (e.g. antoshashakov@gmail.com)
    GMAIL_CLIENT_ID       OAuth 2.0 client id
    GMAIL_CLIENT_SECRET   OAuth 2.0 client secret
    GMAIL_REFRESH_TOKEN   long-lived refresh token

Filters: unread messages whose Subject contains "[mathAI]".
Saves each as bot/inbox/<fetched_at>-<msg_id>.json then marks the message read.
Prints JSON summary of what was fetched.

Avoids IMAP entirely (the Anthropic Cloud sandbox blocks outbound IMAP).
Talks to https://oauth2.googleapis.com/token + https://gmail.googleapis.com
on port 443, which is allowed.
"""
import base64
import email
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from email.header import decode_header
from pathlib import Path

INBOX_DIR = Path(__file__).parent / "inbox"
GMAIL_API = "https://gmail.googleapis.com/gmail/v1/users/me"
INGESTED_LABEL = "mathai-ingested"


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


def api_get(token: str, path: str, params: dict | None = None) -> dict:
    url = f"{GMAIL_API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())


def api_post(token: str, path: str, body: dict) -> dict:
    req = urllib.request.Request(
        f"{GMAIL_API}{path}",
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())


def decode_str(value) -> str:
    if value is None:
        return ""
    parts = decode_header(value)
    out = []
    for p, c in parts:
        if isinstance(p, bytes):
            out.append(p.decode(c or "utf-8", errors="replace"))
        else:
            out.append(p)
    return "".join(out)


def get_text_body(msg) -> str:
    if msg.is_multipart():
        for part in msg.walk():
            disp = str(part.get("Content-Disposition") or "")
            if part.get_content_type() == "text/plain" and "attachment" not in disp:
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode(part.get_content_charset() or "utf-8", errors="replace")
        return ""
    payload = msg.get_payload(decode=True)
    if not payload:
        return ""
    return payload.decode(msg.get_content_charset() or "utf-8", errors="replace")


def ensure_label(token: str) -> str:
    labels = api_get(token, "/labels").get("labels", []) or []
    for lbl in labels:
        if lbl.get("name") == INGESTED_LABEL:
            return lbl["id"]
    new = api_post(token, "/labels", {
        "name": INGESTED_LABEL,
        "labelListVisibility": "labelHide",
        "messageListVisibility": "hide",
    })
    return new["id"]


def strip_quoted_reply(body: str) -> str:
    body = re.split(r"\nOn .+ wrote:\n", body, maxsplit=1)[0]
    body = re.split(r"\n-{2,}\s*Original Message\s*-{2,}", body, maxsplit=1)[0]
    body = re.split(r"\nFrom: .+\nSent: ", body, maxsplit=1)[0]
    return body.strip()


def main():
    client_id = os.environ.get("GMAIL_CLIENT_ID")
    client_secret = os.environ.get("GMAIL_CLIENT_SECRET")
    refresh_token = os.environ.get("GMAIL_REFRESH_TOKEN")
    missing = [k for k, v in [
        ("GMAIL_CLIENT_ID", client_id),
        ("GMAIL_CLIENT_SECRET", client_secret),
        ("GMAIL_REFRESH_TOKEN", refresh_token),
    ] if not v]
    if missing:
        print(json.dumps({"status": "error", "error": f"missing env vars: {missing}"}))
        sys.exit(1)

    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    fetched = []
    skipped_self = 0

    try:
        token = get_access_token(client_id, client_secret, refresh_token)
        label_id = ensure_label(token)
        listing = api_get(token, "/messages", {
            "q": f'subject:"[mathAI]" -label:{INGESTED_LABEL}',
            "maxResults": 50,
        })
        msgs = listing.get("messages", []) or []

        for m in msgs:
            msg_id = m["id"]
            full = api_get(token, f"/messages/{msg_id}", {"format": "raw"})
            raw_b64 = full.get("raw", "")
            raw_bytes = base64.urlsafe_b64decode(raw_b64.encode())
            msg = email.message_from_bytes(raw_bytes)
            subj = decode_str(msg.get("Subject"))
            sender = decode_str(msg.get("From"))
            date_hdr = decode_str(msg.get("Date"))

            is_bot_self = "mathAI bot" in sender
            if not is_bot_self:
                body = strip_quoted_reply(get_text_body(msg))
                fetched_at = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
                record = {
                    "id": msg_id,
                    "threadId": full.get("threadId"),
                    "from": sender,
                    "subject": subj,
                    "date": date_hdr,
                    "body": body,
                    "fetched_at": fetched_at,
                }
                path = INBOX_DIR / f"{fetched_at}-{msg_id}.json"
                path.write_text(json.dumps(record, indent=2), encoding="utf-8")
                fetched.append({
                    "path": str(path.relative_to(Path(__file__).parent.parent)).replace("\\", "/"),
                    "subject": subj,
                    "from": sender,
                    "date": date_hdr,
                })
            else:
                skipped_self += 1

            api_post(token, f"/messages/{msg_id}/modify", {"addLabelIds": [label_id]})
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e), "type": type(e).__name__}))
        sys.exit(1)

    print(json.dumps({
        "status": "ok",
        "transport": "gmail-api:https",
        "fetched": len(fetched),
        "skipped_bot_self": skipped_self,
        "messages": fetched,
    }, indent=2))


if __name__ == "__main__":
    main()
