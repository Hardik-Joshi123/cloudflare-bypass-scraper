# Cloudflare Bypass Scraper

A robust, stealthy, and fully automated web scraping framework designed to bypass Cloudflare and other anti-bot protections using Playwright, real browser profiles, proxy/user agent rotation, and the open-source Flaresolverr service.

---

## 🚀 Features

- **Cloudflare Bypass:** Uses Flaresolverr to automatically solve Cloudflare challenges and retrieve clearance cookies.
- **Real Browser Automation:** Leverages Playwright with real, aged Chrome profiles for maximum authenticity.
- **Proxy & User Agent Rotation:** Rotates proxies and user agents for each session to avoid detection and bans.
- **Advanced Stealth:** Randomizes viewport, timezone, language, Accept-Language, Referer, and patches browser fingerprinting properties.
- **Human-like Behavior:** Simulates mouse movement and scrolling to mimic real users.
- **Automatic Error Handling:** Retries with new proxies/user agents on failure, blacklists bad resources, and logs all actions.
- **Modular & Extensible:** Easily add new targets, stealth features, or scraping logic.

---

## 🛠️ Tech Stack

- **Python 3.8+**
- **Playwright**
- **Flaresolverr** (runs in Docker)
- **Docker** (for Flaresolverr)
- **Proxies & User Agents** (configurable)
- **Logging** (all actions and errors)

---

## ⚡ Quick Start

### 1. **Clone the Repository**
```sh
git clone https://github.com/YOUR_USERNAME/cloudflare-bypass-scraper.git
cd cloudflare-bypass-scraper
```

### 2. **Install Python Dependencies**
```sh
pip install -r requirements.txt
# Or manually install: playwright, requests, etc.
```

### 3. **Prepare Configs**
- Fill `config/proxies.txt` with your proxies (one per line).
- Fill `config/user_agents.txt` with real user agent strings (one per line).

### 4. **Set Up Chrome Profile**
- Place a real, aged Chrome profile in `chrome_profiles/profile1`.

### 5. **Start Flaresolverr**
```sh
cd services/flaresolverr
docker-compose up -d
```

### 6. **Run the Scraper**
```sh
python main.py/main.py
```

- Scraped HTML will be saved to `output.html`.
- Logs will be written to `scraper.log`.

---

## 🧠 How It Works

1. **Flaresolverr** solves Cloudflare and returns clearance cookies.
2. **Playwright** launches with a real Chrome profile, proxy, and randomized fingerprint.
3. **Cookies** are injected, headers and navigator properties are patched for stealth.
4. **Human-like actions** are performed, and the target page is scraped.
5. **Automatic retries** and blacklisting for failed proxies/user agents.

---

## 📝 Customization

- Add new targets in the `targets/` directory.
- Adjust stealth/fingerprint logic in `utils/`.
- Tune retry and blacklist logic in the scraper class.

---

## 🛡️ Disclaimer

This project is for educational and ethical research purposes only.  
**Do not use it to scrape sites without permission.**  
Always comply with the terms of service and legal requirements of target websites.

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE)  
Copyright (c) 2025 Hardik-Joshi123

---

## 🙏 Credits

- [Flaresolverr](https://github.com/FlareSolverr/FlareSolverr)
- [Playwright](https://playwright.dev/)
- [Python](https://www.python.org/)

---
