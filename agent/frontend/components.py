import streamlit as st

def render_scan_progress(placeholder, domain, current_log, progress_percentage):
    placeholder.markdown(f"""
    <div style="
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.75) 100%);
        border: 1px solid rgba(34, 211, 238, 0.3);
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(34, 211, 238, 0.15);
        margin: 2rem 0;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    ">
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 1.5rem; gap: 1rem;">
            <div class="circular-spinner"></div>
            <h3 style="color: #22d3ee; font-size: 1.6rem; font-weight: 700; margin: 0; text-shadow: 0 0 10px rgba(34, 211, 238, 0.3);">
                Analyzing {domain}
            </h3>
        </div>
        <div style="color: #cbd5e1; font-size: 1rem; margin-bottom: 1.5rem; font-weight: 500; height: 24px; animation: pulse 2s infinite;">
            {current_log}
        </div>
        <div style="
            height: 12px;
            background: rgba(51, 65, 85, 0.5);
            border-radius: 6px;
            overflow: hidden;
            margin: 1.5rem 0;
            border: 1px solid rgba(255, 255, 255, 0.05);
        ">
            <div style="
                height: 100%;
                width: {progress_percentage}%;
                background: linear-gradient(90deg, #22d3ee 0%, #3b82f6 50%, #6366f1 100%);
                border-radius: 6px;
                box-shadow: 0 0 15px rgba(34, 211, 238, 0.6);
                transition: width 0.3s ease-out;
            "></div>
        </div>
        <div style="color: #f1f5f9; font-size: 1.1rem; font-weight: 700;">
            Crawl Engine Progress: <span style="color: #22d3ee;">{progress_percentage}%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_browser_preview(domain, screenshot_url):
    st.markdown(f"""
    <div class="browser-frame">
        <div class="browser-header">
            <span class="browser-dot red"></span>
            <span class="browser-dot yellow"></span>
            <span class="browser-dot green"></span>
            <span class="browser-address">{domain}</span>
        </div>
        <div style="width: 100%; height: 550px; overflow-y: auto; background: #0f172a; position: relative;">
            <img src="{screenshot_url}" style="width: 100%; height: auto; display: block;" />
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metric_cards(total_domains, total_issues, high_crit_issues):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Domains Analyzed</div>
            <div class="metric-value" style="color: #22d3ee;">{total_domains}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total SEO Issues</div>
            <div class="metric-value" style="color: #818cf8; text-shadow: 0 0 15px rgba(129, 140, 248, 0.2);">{total_issues}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">High & Critical Issues</div>
            <div class="metric-value" style="color: #f87171; text-shadow: 0 0 15px rgba(248, 113, 113, 0.2);">{high_crit_issues}</div>
        </div>
        """, unsafe_allow_html=True)


def render_ready_to_scan():
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 3rem !important; border: 1px dashed rgba(99, 102, 241, 0.2); margin-top: 2rem;">
        <h3 style="color: #22d3ee; margin-top: 0; font-weight: 700;">Ready to Run SEO Scan</h3>
        <p style="color: #94a3b8; max-width: 600px; margin: 0 auto 1.5rem auto; font-size: 1.05rem;">
            Provide one or more website URLs in the configuration card above, adjust your desired crawl limits, and launch the domain intelligence agent to start auditing.
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_download_section():
    st.markdown("""
    <div class="glass-card" style="text-align: center; border: 1px dashed rgba(34, 211, 238, 0.4); margin-bottom: 1rem;">
        <h4 style="color: #22d3ee; margin-top:0; font-size:1.2rem;">Export Crawl Intelligence Datasets</h4>
        <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0;">Download a consolidated Microsoft Excel spreadsheet containing Domain configurations, Crawled Pages, technical details and parsed SEO issues.</p>
    </div>
    """, unsafe_allow_html=True)
