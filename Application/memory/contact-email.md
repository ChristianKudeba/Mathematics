---
name: Contact email
description: Canonical email address for the mathAI bot — both send and receive use antoshashakov@gmail.com
type: user
originSessionId: 842056e2-da72-4fb3-8c22-aa05bc783faa
---
All mathAI bot email — send AND receive — uses **antoshashakov@gmail.com**. The OAuth client (`mathai-gmail` in GCP project `mathai-495403`) is authenticated to this account.

- **Send FROM:** antoshashakov@gmail.com (Gmail HTTPS API, via `bot/send_via_api.py`)
- **TO and Reply-To:** antoshashakov@gmail.com
- **Inbox check:** Gmail HTTPS API, via `bot/check_inbox.py`. Filters by `subject:"[mathAI]" -label:mathai-ingested` (label-based dedup, not unread-status), excludes bot self-sends by checking for "mathAI bot" in From display name.
- **Replies from either of Anton's addresses** (antoshashakov@gmail.com or antonshakov1@gmail.com) are ingested as long as they land in antoshashakov's inbox — which they do whenever Anton clicks Reply, because Reply-To is antoshashakov.

History note: an earlier directive on 2026-05-03 briefly used antonshakov1 for SMTP send, but that path was abandoned (SMTP blocked in sandbox); 2026-05-05 cleanup standardized everything to antoshashakov via the HTTPS API.
