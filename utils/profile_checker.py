import os
import sqlite3
from datetime import datetime

class ProfileChecker:
    def __init__(self, profile_path):
        self.profile_path = profile_path
        
    def is_valid(self):
        checks = [
            self._check_cookies_exist(),
            self._check_history_records(),
            self._check_visits_recency()
        ]
        return all(checks)
    
    def _check_cookies_exist(self):
        return os.path.exists(f"{self.profile_path}/Default/Cookies")
    
    def _check_history_records(self):
        history_db = f"{self.profile_path}/Default/History"
        if not os.path.exists(history_db):
            return False
            
        try:
            conn = sqlite3.connect(history_db)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM urls")
            return cursor.fetchone()[0] > 50  # At least 50 history records
        except:
            return False
    
    def _check_visits_recency(self):
        last_visit_file = f"{self.profile_path}/Default/Last Visit"
        if not os.path.exists(last_visit_file):
            return False
            
        modified_time = os.path.getmtime(last_visit_file)
        return (datetime.now().timestamp() - modified_time) < 604800  # Updated in last 7 days

# Usage:
checker = ProfileChecker("chrome_profiles/profile1")
print(checker.is_valid())  # Returns True/False