# FRUiTIFY Outreach – complete code (n8n "super agent")

This repository holds the complete code of the FRUiTIFY vendor-outreach system. The system finds Indian fruit sellers on Instagram and Facebook and pitches them in their own language. It answers their comments and messages, and publishes marketing reels. Everything runs on **n8n Cloud** (fruitifyindia.app.n8n.cloud).

Secrets are **not** in these files. Credentials are stored inside n8n and are referenced here only by ID. The approval key and the webhook verify token are replaced by `<APPROVAL_KEY>` and `<WEBHOOK_VERIFY_TOKEN>`. To import a workflow, use **n8n → Workflows → Import from file** and re-select the credentials.

## Folder map

| Path | What it is |
|---|---|
| `n8n-workflows/01-daily-search-pitch-digest.json` | **Agents 1–3.** Mon–Sat 7:45 IST. Picks a random regional mix of hashtags, then runs the Apify Instagram hashtag scraper and profile scraper plus the Facebook search scraper. It keeps manual order-takers (no website, or WhatsApp/Linktree links), skips vendors already in the CRM, and caps the day at 90. Claude Sonnet writes a native-script DM and a voice script for each vendor. The rows are saved to the Google Sheet CRM, and a digest email with Approve / Skip / **Approve all** buttons goes to Ankur. |
| `n8n-workflows/02-approve-or-skip.json` | Webhook `fruitify-review`. Approve, Skip or Approve all, with a daily limit of 30. On approval it makes a Google TTS voice note (Chirp3-HD "Ankur" male voice, in the vendor's language), saves it to Drive and marks the row "Approved – in send queue". |
| `n8n-workflows/03-meta-inbound-comments-dms.json` | Webhook `fruitify-meta` (Instagram API with Instagram Login). **Any comment** on our posts triggers an automatic private-reply DM plus a public reply (once per person; rude or spam comments are skipped). Repeat comments and DMs get a Claude-drafted reply, which is emailed to Ankur for review. |
| `n8n-workflows/04-review-and-send.json` | Webhook `fruitify-send`. A one-tap page to edit and send a drafted reply, plus the reel in the vendor's language. It has double-send protection. |
| `n8n-workflows/05-reply-helper.json` | Agent 4: turns a pasted vendor reply into a native-script answer. |
| `n8n-workflows/06-reels-daily-email-and-post.json` | 8:05 IST email of the day's reels → Review & post → Instagram Graph API (REELS container, then publish). Exactly 5 hashtags, from rotating pools. |
| `n8n-workflows/07-privacy-page.json` | The privacy page needed by the Meta app. |
| `reel-maker/make.py`, `reel-maker/specs.py` | Python + ffmpeg reel generator. Each reel is a hook card, a clip segment with translated caption bands and screen labels, and an end card. Regional reels get a native-language voice-over made with Google TTS. |
| `reels/*.mp4`, `voice/*.mp3`, `plan.json` | The generated reels, their voice tracks and the posting plan. |

## Data and services

- **CRM:** Google Sheet `FRUiTIFY Vendor Outreach CRM`, with tab `Sheet1` for vendors and tab `Reels` for the reel plan.
- **APIs used:**
  - Apify (scraping);
  - Anthropic Claude Sonnet (writing);
  - Google Cloud Text-to-Speech (voice);
  - Google Sheets, Drive and Gmail;
  - Instagram Graph API with Instagram Login: `me/messages`, private replies, `/{comment}/replies`, `me/media`, `me/media_publish`;
  - GitHub contents API (voice files).

## Where the human is still in the loop, and why

| Step | Automated today? | Constraint |
|---|---|---|
| Find vendors, write pitches, voice notes | Yes | – |
| Reply to comments (first contact) | Yes, fully automatic | Instagram allows one private reply per comment, within 7 days |
| Reply to vendor messages | Draft is automatic; a person taps Send | This can be made fully automatic (24-hour window rule) |
| **First DM to a vendor who never contacted us** | **No – a person clicks Send** | Meta's messaging API **cannot start a conversation**. Business messages are only allowed after the user writes to the business (24-hour window) or comments. Bots that click "Send" in the Instagram web app break Instagram's Terms (automated activity) and put the account at risk of action blocks or a ban. |
| Post reels | One tap (could be fully automatic) | – |

## Proposed "blanket approval" design (for expert review)

1. **One morning approval:** a single "Approve today's plan" tap, or automatic approval when nothing is tapped by 9:00. This covers the vendor list, the reels and auto-replies.
2. **Turn cold outreach into inbound:**
   - daily reels in each language;
   - a ₹300/day Instagram ad with a "Send message" button;
   - comment-to-DM (already automatic).
   Every vendor who comments or messages is then handled **fully automatically through the official API**, including the language-matched reel.
3. **Automatic replies:** vendor messages are answered automatically within the 24-hour window. Only edge cases (complaints, pricing negotiations) are escalated to Ankur by email.
4. **Optional: WhatsApp Business Cloud API** with approved message templates. It is fully automatable, but WhatsApp policy needs the vendor's opt-in, so it is for vendors who reply, not for cold numbers.
5. **Cold DMs (if kept):** prepared in batches; a person sends them, 25–30 a day, spaced out.
