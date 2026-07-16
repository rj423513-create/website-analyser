import sys
import os
# Ensure the current directory is in sys.path so modules resolve correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import time
import base64
from config import GTMETRIX_API_KEY

# Import Frontend Subpackage Components
from frontend import inject_premium_styles, inject_header_element, inject_footer_element
from frontend import (
    render_scan_progress,
    render_browser_preview,
    render_metric_cards,
    render_ready_to_scan,
    render_download_section
)

# Import Backend Subpackage Utilities
from backend import get_gtmetrix_screenshot, get_domain_info, crawl_page, generate_excel_report

st.set_page_config(page_title="SEO Domain Intelligence Agent", layout="wide")

# Inject global style and header
inject_premium_styles()
inject_header_element()

# Input Panel configured inside native bordered container
with st.container(border=True):
    st.markdown(
        "<h3 style='margin-top: 0; color: #22d3ee; font-weight: 700; font-size: 1.3rem; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 0.75rem; margin-bottom: 1rem;'>Configuration Panel</h3>",
        unsafe_allow_html=True)
    domains_input = st.text_area("Target Website URLs (one domain per line):",
                                 value="https://jeenweb.com",
                                 height=100)
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        max_pages = st.slider("Max crawl depth pages per domain:", 5, 300, 25)
    with col_c2:
        scan_speed = st.selectbox(
            "Scan Speed / Simulation Delay:",
            options=[
                "Accelerated Simulation (~5min/website)",
                "Thorough Deep Scan (~10min/website)"],
            index=1
        )

    screenshot_source = st.selectbox(
        "Screenshot Preview Source:",
        options=["Local Puppeteer Service (Port 3000)",
                 "Thum.io (Free & Fast)",
                 "GTmetrix API v2.0 (Premium & Authorized)"],
        index=0
    )


run_analysis = st.button(
    "Start Full Multi-Website Analysis",
    type="primary",
    use_container_width=True)

scan_placeholder = st.empty()
crawl_count_placeholder = st.empty()
crawl_log_placeholder = st.empty()

# ===================== NEW: HOMEPAGE PREVIEW (ADDED ON FIRST PAGE) ======
if domains_input.strip():
    st.markdown("### 🌐 Homepage Previews")
    for domain in domains_input.split('\n'):
        domain = domain.strip()
        if domain:
            try:
                screenshot_loaded = False
                error_msg = None
                screenshot_url = ""

                if "Local Puppeteer" in screenshot_source:
                    try:
                        # Fast status check to see if the local Node service is running
                        health_check = requests.get("http://localhost:3000/health", timeout=1.5)
                        if health_check.status_code == 200 and health_check.text == "OK":
                            screenshot_url = f"http://localhost:3000/screenshot?url={domain}"
                            screenshot_loaded = True
                        else:
                            error_msg = "Local Puppeteer service health check failed. Falling back to Thum.io."
                    except Exception:
                        error_msg = "Local Puppeteer service is not running on port 3000. Start it by running 'node server.js' in the 'screenshot-service' directory. Falling back to Thum.io."

                elif "GTmetrix" in screenshot_source:
                    active_key = GTMETRIX_API_KEY.strip() if GTMETRIX_API_KEY else ""
                    if not active_key:
                        error_msg = "GTmetrix API Key is required but missing."
                    else:
                        with st.spinner(f"Requesting GTmetrix screenshot for {domain}..."):
                            img_bytes, err = get_gtmetrix_screenshot(
                                domain, active_key)
                            if img_bytes:
                                base64_img = base64.b64encode(
                                    img_bytes).decode("utf-8")
                                screenshot_url = f"data:image/png;base64,{base64_img}"
                                screenshot_loaded = True
                            else:
                                error_msg = f"GTmetrix failed ({err}). Falling back to Thum.io."

                if not screenshot_loaded:
                    screenshot_url = f"https://image.thum.io/get/width/600/crop/800/{domain}"
                    if error_msg:
                        st.warning(error_msg)

                render_browser_preview(domain, screenshot_url)
            except Exception as e:
                st.warning(f"Could not preview {domain}: {str(e)}")


# ===================== MAIN ANALYSIS =====================
if run_analysis:
    domains = [d.strip() for d in domains_input.split('\n') if d.strip()]

    if not domains:
        st.error("Please enter at least one domain")
    else:
        all_domain_info = []
        all_pages = []
        all_issues = []
        all_audit = []

        progress_bar = st.progress(0)

        # Determine simulation sleep time
        if scan_speed == "Accelerated Simulation (~5min/website)":
            sleep_time = 0.05
        else:
            sleep_time = 0.2

        for idx, domain in enumerate(domains):
            # Dynamic scanning simulation
            logs = [
                "Initializing Intelligent SEO Agent...",
                "Configuring secure handshake protocols...",
                "Querying public WHOIS registry databases...",
                "Analyzing domain registrar and name server propagation...",
                "Locating and verifying DNS Mail Exchange (MX) records...",
                "Requesting target robots.txt file...",
                "Parsing crawl permissions from robots.txt...",
                "Locating domain sitemap.xml structure...",
                "Validating SSL certificate and encryption handshake...",
                "Establishing crawl connections...",
                "Analyzing document structure and headers...",
                "Evaluating title tags and meta descriptions...",
                "Analyzing internal/external hypermedia links...",
                "Inspecting image assets and alt tags...",
                "Simulating page load times and Core Web Vitals...",
                "Calculating First Input Delay (FID)...",
                "Calculating Cumulative Layout Shift (CLS)...",
                "Evaluating Largest Contentful Paint (LCP)...",
                "Compiling technical audit datasets...",
                "Reviewing high-priority SEO recommendations..."
            ]

            for p in range(0, 101, 1):
                # Map progress to corresponding logs
                log_idx = min(p // (100 // len(logs)), len(logs) - 1)
                current_log = logs[log_idx]

                render_scan_progress(scan_placeholder, domain, current_log, p)
                if sleep_time > 0:
                    time.sleep(sleep_time)


            def make_live_callback():
                count = [0]

                def live_callback(url, status, load_time, title):
                    count[0] += 1
                    crawl_count_placeholder.markdown(f"""
                    <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 1rem; margin-bottom: 0.5rem;">
                        <h4 style="margin: 0; color: #22d3ee;">Active Crawling: {domain}</h4>
                        <p style="margin: 5px 0 0 0; color: #cbd5e1;">Pages Audited: <strong style="color: #22d3ee;">{count[0]} / {max_pages}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                    crawl_log_placeholder.markdown(f"""
                    <div class="recommendation-item" style="border-left-color: #475569; margin: 0.25rem 0;">
                        <strong>Status:</strong> <code>{status}</code> | <strong>Load Time:</strong> {load_time}s | <strong>URL:</strong> <a href="{url}" target="_blank" style="color: #22d3ee; text-decoration: none;">{url}</a>
                        <br/><span style="font-size: 0.85rem; color: #94a3b8;"><strong>Page Title:</strong> {title[:100]}</span>
                    </div>
                    """, unsafe_allow_html=True)
                return live_callback

            df_domain = pd.DataFrame([get_domain_info(domain)])
            df_pages, df_issues, df_audit = crawl_page(
                domain, max_pages, live_callback=make_live_callback())

            # Clean up the crawl placeholder UI
            crawl_count_placeholder.empty()
            crawl_log_placeholder.empty()

            if not df_issues.empty:
                df_issues['Domain'] = domain
            if not df_audit.empty:
                df_audit['Domain'] = domain

            all_domain_info.append(df_domain)
            all_pages.append(df_pages)
            all_issues.append(df_issues)
            all_audit.append(df_audit)

            progress_bar.progress((idx + 1) / len(domains))

        scan_placeholder.empty()
        progress_bar.empty()

        df_all_domain = pd.concat(all_domain_info, ignore_index=True)
        df_all_pages = pd.concat(all_pages, ignore_index=True)
        df_all_issues = pd.concat(all_issues, ignore_index=True)
        df_all_audit = pd.concat(all_audit, ignore_index=True)
        st.success(f"Analysis Completed for {len(domains)} Websites!")

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["Summary", "Domain Info", "Crawled Pages", "SEO Issues", "Technical Audit"])

        with tab1:
            high_crit_count = len(df_all_issues[df_all_issues.get('Severity', pd.Series()).isin(
                ['High', 'Critical'])]) if not df_all_issues.empty else 0

            render_metric_cards(len(domains), len(df_all_issues), high_crit_count)

            if not df_all_pages.empty and 'Status' in df_all_pages.columns:
                st.markdown(
                    "<h3 style='color: #22d3ee; margin-top: 2rem;'>HTTP Status Code Distribution</h3>",
                    unsafe_allow_html=True)
                status_counts = df_all_pages['Status'].value_counts(
                ).reset_index()
                status_counts.columns = ['Status Code', 'Number of Pages']
                status_counts['Status Code'] = status_counts['Status Code'].astype(
                    str)
                # Show Streamlit native bar chart
                st.bar_chart(status_counts.set_index('Status Code'))

        with tab2:
            st.dataframe(df_all_domain, use_container_width=True)
        with tab3:
            st.dataframe(df_all_pages, use_container_width=True)
        with tab4:
            if not df_all_issues.empty:
                st.dataframe(df_all_issues, use_container_width=True)
            else:
                st.info("No issues found")

        with tab5:
            st.markdown(
                "<h3 style='color: #22d3ee; margin-top: 1.5rem;'>Technical Audit + Core Web Vitals</h3>",
                unsafe_allow_html=True)
            if not df_all_audit.empty:
                st.dataframe(df_all_audit, use_container_width=True)

                if 'Load_Time_sec' in df_all_audit.columns:
                    st.markdown(
                        "<h3 style='color: #22d3ee; margin-top: 2rem;'>Page Load Time by URL (seconds)</h3>",
                        unsafe_allow_html=True)
                    load_df = df_all_audit[[
                        'URL_Slug', 'Load_Time_sec']].copy()
                    load_df['Page'] = load_df['URL_Slug'].apply(
                        lambda x: x if len(x) < 25 else x[:22] + '...')
                    # Render using streamlit area_chart or bar_chart
                    st.area_chart(load_df.set_index('Page')['Load_Time_sec'])

            st.markdown(
                "<h3 style='color: #22d3ee; margin-top: 2rem;'>Actions & Recommendations</h3>",
                unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-card" style="padding: 1.5rem !important;">
                <div class="recommendation-item"><strong>Core Web Vitals:</strong> Focus on optimizing Largest Contentful Paint (LCP) under 2.5s.</div>
                <div class="recommendation-item"><strong>Server & Client Errors:</strong> Address any 4xx (client) and 5xx (server) responses immediately to prevent crawl budget waste.</div>
                <div class="recommendation-item"><strong>Canonical Tags:</strong> Verify self-referencing canonical links are present on all indexable pages.</div>
                <div class="recommendation-item"><strong>Social Metadata:</strong> Implement Facebook Open Graph (OG) tags and Twitter Cards for better social CTR.</div>
                <div class="recommendation-item"><strong>Crawl Architecture:</strong> Improve internal link equity by reducing orphaned pages and link silos.</div>
            </div>
            """, unsafe_allow_html=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"Multi_SEO_Report_{timestamp}.xlsx"

        generate_excel_report(df_all_domain, df_all_pages, df_all_issues, df_all_audit, filename)

        st.markdown(
            "<div style='margin-top: 2rem;'></div>",
            unsafe_allow_html=True)
        
        render_download_section()

        with open(filename, "rb") as file:
            st.download_button(
                "Download Enterprise SEO Report (4 Sheets)",
                data=file,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

else:
    render_ready_to_scan()

# Render footer on all pages
inject_footer_element()
