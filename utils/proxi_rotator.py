import random
import requests
from concurrent.futures import ThreadPoolExecutor

class ProxyRotator:
    def __init__(self):
        self.proxies = self._load_proxies()
        self.current_proxy = None
        
    def _load_proxies(self):
        with open("config/proxies.txt") as f:
            return [line.strip() for line in f if not line.startswith("#")]
    
    def _test_proxy(self, proxy):
        try:
            proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            resp = requests.get("https://api.ipify.org?format=json", 
                              proxies=proxies, 
                              timeout=10)
            return resp.json()["ip"] == proxy.split("@")[1].split(":")[0]
        except:
            return False
    
    def get_valid_proxy(self):
        # Test 3 random proxies in parallel
        with ThreadPoolExecutor(max_workers=3) as executor:
            test_results = list(executor.map(
                lambda p: (p, self._test_proxy(p)),
                random.sample(self.proxies, min(3, len(self.proxies)))
            ))
        
        valid_proxies = [p for p, is_valid in test_results if is_valid]
        self.current_proxy = random.choice(valid_proxies) if valid_proxies else None
        return self.current_proxy

# Usage:
rotator = ProxyRotator()
print(rotator.get_valid_proxy())  # Returns 'geo1.resproxy.com:12345:user:pass'