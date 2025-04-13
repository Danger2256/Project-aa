import requests
import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def take_screenshot(domain):
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1920, 1080)
        driver.get(f"http://{domain}")
        timestamp = int(time.time())
        filename = f"screenshot_{domain}_{timestamp}.png".replace(":", "_")
        path = os.path.join("screenshots", filename)
        os.makedirs("screenshots", exist_ok=True)
        driver.save_screenshot(path)
        driver.quit()
        return path
    except Exception as e:
        print(f"Error taking screenshot for {domain}: {e}")
        return None

def check_domains():
    with open('domains.json', 'r') as f:
        domains = json.load(f)

    try:
        with open('status.json', 'r') as f:
            previous_status = json.load(f)
    except:
        previous_status = {}

    messages = []
    for domain in domains:
        try:
            response = requests.get(f"http://{domain}", timeout=10)
            status = 'up' if response.status_code == 200 else 'down'
        except:
            status = 'down'

        if domain in previous_status:
            if previous_status[domain] != status:
                messages.append(f"تغییر وضعیت دامنه {domain}: {previous_status[domain]} -> {status}")
        else:
            messages.append(f"وضعیت اولیه دامنه {domain}: {status}")

        previous_status[domain] = status

    with open('status.json', 'w') as f:
        json.dump(previous_status, f, indent=2)

    return messages
