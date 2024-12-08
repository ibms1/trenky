import streamlit as st
from playwright.sync_api import sync_playwright
import os

try:
    with sync_playwright() as p:
        os.system("playwright install chromium")
        
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-software-rasterizer'
            ]
        )
        
        page = browser.new_page()
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        
        # Go to Google Trends
        url = 'https://trends.google.com/trends/trendingsearches/daily?geo=US'
        st.write(f"Accessing URL: {url}")
        page.goto(url, timeout=60000)
        
        # Wait for content to load
        page.wait_for_selector('.feed-item-header')
        
        # Try different selector
        data = page.locator('.feed-item-header').all_inner_texts()
        
        # Take screenshot for debugging
        page.screenshot(path="debug.png")
        browser.close()
        
        st.title("Trending Topics on Google")
        if data:
            for index, item in enumerate(data, 1):
                st.write(f"{index}. {item}")
        else:
            st.warning("No data found")
            st.write("Please check if:")
            st.write("1. The website structure has changed")
            st.write("2. Access is being blocked")
            st.write("3. The page is loading properly")
            
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Retrying... Please refresh the page")