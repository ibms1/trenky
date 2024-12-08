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
        
        page.goto('https://trends.google.com/trending?geo=US&status=active&hours=168', 
                 timeout=60000)
        
        # Changed from all_texts() to all_inner_texts()
        data = page.locator('div.xrnccd div div div:nth-child(2) a h3').all_inner_texts()
        browser.close()
        
        st.title("Trending Topics on Google")
        if data:
            for index, item in enumerate(data, 1):
                st.write(f"{index}. {item}")
        else:
            st.warning("No data found")
            
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Retrying... Please refresh the page")