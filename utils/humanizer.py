import random
import time
from playwright.sync_api import Page
from typing import List, Tuple

class Humanizer:
    @staticmethod
    def random_movement(page: Page):
        """Realistic mouse trail with acceleration"""
        width, height = page.viewport_size["width"], page.viewport_size["height"]
        x, y = random.randint(0, width), random.randint(0, height)
        
        for _ in range(random.randint(3, 7)):
            # Sigmoid acceleration curve
            dx = random.randint(-100, 100) * (1 + 0.5 * random.random())
            dy = random.randint(-50, 50) * (1 + 0.3 * random.random())
            
            new_x = max(0, min(width, x + dx))
            new_y = max(0, min(height, y + dy))
            
            page.mouse.move(new_x, new_y)
            time.sleep(random.uniform(0.05, 0.2))
            x, y = new_x, new_y
    
    @staticmethod
    def human_typing(page: Page, selector: str, text: str):
        """Type with variable speed and errors"""
        for char in text:
            page.type(selector, char, delay=random.uniform(50, 250))
            if random.random() < 0.1:  # 10% chance to make&correct mistake
                page.keyboard.press("Backspace")
                time.sleep(random.uniform(0.2, 0.5))
                page.type(selector, char)

# Usage in your scraper:
humanizer = Humanizer()
humanizer.random_movement(page)
humanizer.human_typing(page, "#username", "rajasthan_gov_user")