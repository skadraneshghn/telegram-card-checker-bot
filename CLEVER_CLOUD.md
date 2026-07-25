# Clever Cloud Deployment Guide

This Telegram Bot is configured for seamless deployment on **Clever Cloud** using Docker.

## Why Port 8080?
Clever Cloud requires containerized applications to bind to port `8080` (or the `$PORT` environment variable) to verify application health and route traffic. 

This repository includes `web_server.py`, a lightweight HTTP server running concurrently alongside the Telegram bot. It serves:
- **`GET /`**: A modern HTML status dashboard displaying bot uptime and system state.
- **`GET /health`**: A JSON endpoint (`{"status": "ok"}`) for Clever Cloud health checks.

---

## Deployment Steps

### 1. Create a Docker Application on Clever Cloud
1. Log in to your [Clever Cloud Console](https://console.clever-cloud.com/).
2. Click **Create...** > **An application**.
3. Select **Docker** as the runtime.
4. Select your deployment strategy (e.g. Git deployment or Clever Tools CLI).

### 2. Configure Environment Variables
In the Clever Cloud Console, navigate to **Environment Variables** for your application and set the following required variables:

| Variable | Description | Example |
| :--- | :--- | :--- |
| `TELEGRAM_API_ID` | Your Telegram API ID from my.telegram.org | `1234567` |
| `TELEGRAM_API_HASH` | Your Telegram API Hash from my.telegram.org | `0123456789abcdef0123456789abcdef` |
| `TELEGRAM_BOT_TOKEN` | Your Bot Token from @BotFather | `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ` |
| `PORT` | Set automatically by Clever Cloud (defaults to 8080) | `8080` |
| `CC_HEALTHCHECK_PATH` | (Optional) Custom path for health checks | `/health` |

### 3. Persistent Data (Optional)
If you want the SQLite database (`assets/db_bot.db`) to persist across container restarts:
1. In Clever Cloud Console, add a **Cellar S3** or **FS Bucket** (File System Bucket).
2. Mount the bucket to `/app/assets`.

### 4. Deploy
Push your code to the Clever Cloud Git remote:
```bash
git remote add clever <your-clever-cloud-git-url>
git push clever main
```

Clever Cloud will automatically detect the `Dockerfile`, build the image, expose port `8080`, pass the health checks, and run your Telegram bot 24/7.
