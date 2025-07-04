from playwright.sync_api import sync_playwright
#from services.captcha_solver import CaptchaSolver  # Removed
from utils.humanizer import human_scroll
from utils.flaresolverr import Flaresolverr
from utils.proxy_rotator import ProxyRotator
import random
import time
import json
import logging

# Setup logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

class RajasthanScraper:
    def __init__(self, max_retries=5):
        #self.captcha = CaptchaSolver("ANTICAPTCHA_KEY")  # Removed
        self.proxy_rotator = ProxyRotator()
        self.flaresolverr = Flaresolverr()
        self.max_retries = max_retries
        self.bad_proxies = set()
        self.bad_user_agents = set()
        self.viewport_sizes = [
            {"width": 1920, "height": 1080},
            {"width": 1366, "height": 768},
            {"width": 1536, "height": 864},
            {"width": 1440, "height": 900},
            {"width": 1600, "height": 900}
        ]
        self.timezones = ["Asia/Kolkata", "Europe/London", "America/New_York", "Asia/Singapore"]
        self.languages = ["en-US", "en-GB", "hi-IN", "fr-FR"]
        self.accept_languages = ["en-US,en;q=0.9", "en-GB,en;q=0.8", "hi-IN,hi;q=0.7", "fr-FR,fr;q=0.6"]
        self.referers = [
            "https://www.google.com/", "https://www.bing.com/", "https://duckduckgo.com/", "https://yandex.com/"
        ]
        self.proxy_failures = {}
        self.ua_failures = {}
        self.max_failures = 3
        
    def _get_user_agent(self):
        with open("config/user_agents.txt") as f:
            user_agents = [ua.strip() for ua in f if ua.strip() and ua.strip() not in self.bad_user_agents]
        return random.choice(user_agents) if user_agents else None

    def _get_proxy(self):
        proxies = [p for p in self.proxy_rotator.proxies if p not in self.bad_proxies]
        if not proxies:
            return None
        return random.choice(proxies)

    def _blacklist_proxy(self, proxy):
        self.bad_proxies.add(proxy)
        self.proxy_failures[proxy] = self.proxy_failures.get(proxy, 0) + 1
        if self.proxy_failures[proxy] >= self.max_failures:
            logging.warning(f"Proxy {proxy} blacklisted after {self.max_failures} failures.")

    def _blacklist_user_agent(self, ua):
        self.bad_user_agents.add(ua)
        self.ua_failures[ua] = self.ua_failures.get(ua, 0) + 1
        if self.ua_failures[ua] >= self.max_failures:
            logging.warning(f"User agent {ua} blacklisted after {self.max_failures} failures.")

    def scrape(self, url):
        last_exception = None
        for attempt in range(1, self.max_retries + 1):
            proxy = self._get_proxy() or self.proxy_rotator.get_valid_proxy()
            user_agent = self._get_user_agent()
            viewport = random.choice(self.viewport_sizes)
            timezone = random.choice(self.timezones)
            language = random.choice(self.languages)
            accept_language = random.choice(self.accept_languages)
            referer = random.choice(self.referers)
            try:
                # 1. Use Flaresolverr to bypass Cloudflare and get cookies
                cookies = self.flaresolverr.get_cookies(url, proxy=proxy)
                with sync_playwright() as p:
                    browser = p.chromium.launch_persistent_context(
                        "./chrome_profiles/profile1",
                        headless=False,
                        proxy={"server": proxy} if proxy else None,
                        args=["--disable-blink-features=AutomationControlled"]
                    )
                    page = browser.new_page(
                        user_agent=user_agent,
                        viewport=viewport,
                        locale=language
                    )
                    # Patch navigator properties for stealth
                    page.add_init_script(
                        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
                        "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});"
                        "Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});"
                        "Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 4});"
                    )
                    # Set timezone
                    page.emulate_timezone(timezone)
                    # Set Accept-Language and Referer headers
                    page.set_extra_http_headers({
                        "Accept-Language": accept_language,
                        "Referer": referer
                    })
                    # 2. Inject cookies from Flaresolverr (convert to Playwright format)
                    for cookie in cookies:
                        if "url" not in cookie and "domain" in cookie:
                            cookie["url"] = url
                        page.context.add_cookies([cookie])
                    page.goto(url, timeout=60000)
                    human_scroll(page)  # Human-like interaction
                    content = page.content()
                    # Basic check: if Cloudflare block page, retry
                    if "cf-chl-" in content or "Attention Required!" in content or "cloudflare" in content.lower():
                        raise Exception("Cloudflare challenge detected in content")
                    logging.info(f"Success with proxy {proxy} and user agent {user_agent}")
                    return content
            except Exception as e:
                last_exception = e
                logging.error(f"[Attempt {attempt}] Failed with proxy {proxy} and user agent {user_agent}: {e}")
                if proxy:
                    self._blacklist_proxy(proxy)
                if user_agent:
                    self._blacklist_user_agent(user_agent)
                time.sleep(2)
        raise Exception(f"All retries failed. Last error: {last_exception}")