import streamlit as st
from playwright.sync_api import sync_playwright, TimeoutError
import os
import time

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
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        page = context.new_page()
        
        # Go to Google Trends with longer timeout
        url = 'https://trends.google.com/trends/trendingsearches/daily?geo=US'
        st.write(f"Loading page...")
        page.goto(url, wait_until='networkidle', timeout=90000)  # 90 seconds timeout
        
        # Wait for page to be fully loaded
        time.sleep(5)  # Give extra time for JavaScript to execute
        
        try:
            # Wait for content with longer timeout
            page.wait_for_selector('.feed-item-header', timeout=90000)
            
            # Get the trending topics
            items = page.query_selector_all('.feed-item-header')
            
            data = []
            for item in items:
                title = item.query_selector('a')
                if title:
                    data.append(title.inner_text())
            
            browser.close()
            
            st.title("Trending Topics on Google")
            if data:
                for index, item in enumerate(data, 1):
                    st.write(f"{index}. {item}")
            else:
                st.warning("No data found - Please try refreshing")
                
        except TimeoutError:
            st.error("Page took too long to load. Please try again.")
        except Exception as e:
            st.error(f"Error extracting data: {str(e)}")
            
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please try refreshing the page")