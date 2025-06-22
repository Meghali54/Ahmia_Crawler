# 🕸️ Ahmia Onion Link Crawler

A Python-based crawler that scrapes `.onion` links from [Ahmia.fi](https://ahmia.fi/onions/), checks for duplicates, and stores new links into a MongoDB Atlas database — all automated as a scheduled cron job on Render.com.

---

## 🚀 Features

- ✅ Automatically fetches `.onion` links from [Ahmia.fi](https://ahmia.fi/onions/)
- ✅ Stores only new/unseen links to avoid duplicates
- ✅ Saves metadata: source, crawled timestamp
- ✅ Hosted on [Render](https://render.com) with 24h daily cron job
- ✅ Runs independently — no local machine required

---

## 🗃️ Data Schema

Each document in MongoDB looks like:

```json
{
  "onionLink": "http://exampleonionlink.onion",
  "source": "Ahmia",
  "crawledTimestamp": "2025-06-20T00:00:00Z"
}
