import streamlit as st
from playwright.sync_api import sync_playwright
import os

# تثبيت المتصفح عند أول تشغيل
if not os.path.exists("/usr/lib/chromium-browser"):
    os.system("playwright install chromium")

try:
    with sync_playwright() as p:
        # استخدام متصفح Chromium مع الإعدادات المناسبة للبيئة السحابية
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = browser.new_page()
        page.goto('https://trends.google.com/trending?geo=US&status=active&hours=168')
        data = page.locator('div.xrnccd div div div:nth-child(2) a h3').all_texts()
        browser.close()
        
        st.title("المواضيع الرائجة في Google")
        for index, item in enumerate(data, 1):
            st.write(f"{index}. {item}")
            
except Exception as e:
    st.error(f"حدث خطأ: {str(e)}")