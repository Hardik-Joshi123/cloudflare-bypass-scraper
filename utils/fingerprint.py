import random
from curl_cffi import requests

def get_tls_fingerprint():
    """Rotate TLS fingerprints every 3-5 requests"""
    browsers = [    
        "chrome110", "chrome107", 
        "safari15_5", "safari16_0"
    ]
    return random.choice(browsers)

def make_request(url):
    with requests.Session(
        impersonate=get_tls_fingerprint(),
        timeout=30
    ) as s:
        return s.get(url)
    
def rotate_fingerprint():
    return random.choice([
        {"http2": True, "headers": {...}},  # Chrome
        {"http2": False, "headers": {...}}  # Safari
    ])