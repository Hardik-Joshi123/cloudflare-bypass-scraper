import sys
from utils.proxy_rotator import ProxyRotator
from utils.profile_checker import ProfileChecker
from targets.rajasthan_gov import RajasthanScraper

def main(target_url):
    # 1. Verify environment
    if not ProfileChecker("chrome_profiles/profile1").is_valid():
        print("Invalid Chrome profile! Run setup_chrome.py first")
        sys.exit(1)
    
    # 2. Get proxy
    proxy = ProxyRotator().get_valid_proxy()
    if not proxy:
        print("No working proxies found")
        sys.exit(1)
    
    # 3. Scrape using RajasthanScraper (with Flaresolverr)
    scraper = RajasthanScraper()
    scraper.proxy = proxy  # Set proxy for scraper
    content = scraper.scrape(target_url)
    with open("output.html", "w") as f:
        f.write(content)

if __name__ == "__main__":
    main("https://industries.rajasthan.gov.in")