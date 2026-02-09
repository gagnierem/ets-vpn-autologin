
import os
import json
import sys
import time

from totp import get_totp
try:
    from playwright.sync_api import sync_playwright, TimeoutError
except ImportError:
    print("Playwright is not installed. Please run 'pip install playwright' and 'playwright install'.")
    exit(1)


# Replace with the URL of the service you want to access
SERVICE_URL = "https://accesvpn.etsmtl.ca"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(SERVICE_URL)

        # Get credentials from config
        with open('config.json') as f:
            config = json.load(f)

        username = config.get('username')
        password = config.get('password')
        totp_secret = config.get('totp_secret')

        totp = get_totp(totp_secret)

        if not username or not password:
            print("Error: Please set username and password in config.json.")
            browser.close()
            exit(1)

        if not totp_secret:
            print("Error: Please set totp_secret in config.json.")
            browser.close()
            exit(1)

        try:
            # Fill username
            page.wait_for_selector('#i0116', timeout=10000)
            page.fill('#i0116', username)
            page.click('input[type="submit"]')

            # Wait for password field
            page.wait_for_selector('#passwordInput', timeout=10000)
            page.fill('#passwordInput', password)
            page.click('#submitButton')

            # Wait for TOTP field and fill it
            page.wait_for_selector('#idTxtBx_SAOTCC_OTC', timeout=10000)
            page.fill('#idTxtBx_SAOTCC_OTC', totp)
            page.click('input[type="submit"]')

            # Click the "Yes" button to stay signed in (idSIButton9)
            page.wait_for_selector('#idSIButton9', timeout=10000)
            page.click('#idSIButton9')

            # Wait for navigation to complete
            page.wait_for_load_state('networkidle', timeout=15000)
        except Exception as e:
            print(f"Login automation failed: {e}")
            browser.close()
            exit(1)

        # Get all cookies
        cookies = context.cookies()

        webvpn_cookie = next((cookie for cookie in cookies if cookie['name'] == 'webvpn'), None)
        if webvpn_cookie:
            print(webvpn_cookie['value'])
        else:
            print("")

        browser.close()

if __name__ == "__main__":
    main()
