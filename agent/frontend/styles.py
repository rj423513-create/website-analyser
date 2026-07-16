import streamlit as st

def inject_premium_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

        * {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }

        /* Background and global text color */
        .stApp {
            background: radial-gradient(circle at 50% 0%, #0f172a 0%, #080c14 100%) !important;
            color: #f1f5f9 !important;
        }

        /* Hide Streamlit components for a custom dashboard look */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 4rem !important;
            max-width: 95% !important;
        }

        /* Glassmorphic layout card styling */
        .glass-card, div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(30, 41, 59, 0.45) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px !important;
            padding: 1.8rem !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
            margin-bottom: 1.5rem !important;
        }

        /* Actionable recommendations lists */
        .recommendation-item {
            background: rgba(30, 41, 59, 0.3);
            border-left: 4px solid #475569;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.75rem 0;
            color: #cbd5e1;
            font-size: 0.95rem;
        }

        /* Custom premium stats metrics */
        .metric-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.6) 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-3px);
            border-color: rgba(34, 211, 238, 0.3);
        }
        .metric-label {
            font-size: 0.85rem;
            color: #94a3b8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.5rem;
        }
        .metric-value {
            font-size: 2.25rem;
            font-weight: 800;
            text-shadow: 0 0 15px rgba(34, 211, 238, 0.2);
        }

        /* Overwrite input textarea container styling */
        div[data-baseweb="textarea"] {
            background-color: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            padding: 5px !important;
            transition: all 0.3s ease !important;
        }
        div[data-baseweb="textarea"]:focus-within {
            border-color: #22d3ee !important;
            box-shadow: 0 0 15px rgba(34, 211, 238, 0.15) !important;
        }
        textarea {
            color: #f1f5f9 !important;
            font-size: 0.95rem !important;
        }

        /* Tab lists and buttons */
        div[role="tablist"], div[data-baseweb="tab-list"] {
            background-color: rgba(30, 41, 59, 0.3) !important;
            border-radius: 12px !important;
            padding: 6px !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            margin-bottom: 1.5rem !important;
        }
        button[role="tab"], button[data-baseweb="tab"], div[data-baseweb="tab"] {
            color: #94a3b8 !important;
            font-weight: 600 !important;
            padding: 10px 20px !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
            border: none !important;
            background: transparent !important;
        }
        button[role="tab"]:hover, button[data-baseweb="tab"]:hover, div[data-baseweb="tab"]:hover {
            color: #22d3ee !important;
            background-color: rgba(255, 255, 255, 0.03) !important;
        }
        button[role="tab"][aria-selected="true"], button[data-baseweb="tab"][aria-selected="true"], div[data-baseweb="tab"][aria-selected="true"] {
            background-color: rgba(34, 211, 238, 0.15) !important;
            color: #22d3ee !important;
            border: 1px solid rgba(34, 211, 238, 0.2) !important;
        }
        div[data-baseweb="tab-highlight"] {
            display: none !important;
        }

        /* Text readability overrides */
        label, p, li {
            color: #cbd5e1 !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #f1f5f9 !important;
        }
        div[data-testid="stWidgetLabel"] p {
            color: #f1f5f9 !important;
            font-weight: 600 !important;
        }
        div[data-testid="stSlider"] span {
            color: #cbd5e1 !important;
        }
        div[data-testid="stNotification"] p {
            color: #f1f5f9 !important;
        }

        /* Keyframe Animations */
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        @keyframes pulse {
            0%, 100% { opacity: 0.6; }
            50% { opacity: 1; }
        }

        /* Spinning element */
        .circular-spinner {
            width: 32px;
            height: 32px;
            border: 3px solid rgba(34, 211, 238, 0.1);
            border-radius: 50%;
            border-top: 3px solid #22d3ee;
            animation: spin 1s linear infinite;
            display: inline-block;
        }

        /* Button redesign */
        div.stButton > button {
            background: linear-gradient(135deg, #22d3ee 0%, #3b82f6 50%, #6366f1 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 14px 28px !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 25px rgba(59, 130, 246, 0.25) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            width: 100% !important;
            letter-spacing: 0.5px !important;
        }
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 30px rgba(59, 130, 246, 0.4) !important;
            filter: brightness(1.05) !important;
            color: white !important;
        }
        div.stButton > button:active {
            transform: translateY(0px) !important;
        }

        /* Download button redesign */
        div.stDownloadButton > button {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
            letter-spacing: 0.5px !important;
        }
        div.stDownloadButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(34, 211, 238, 0.2) !important;
            border-color: #22d3ee !important;
            color: white !important;
        }
        div.stDownloadButton > button:active {
            transform: translateY(0px) !important;
        }

        /* Browser Mockup Frame Styles */
        .browser-frame {
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            background: rgba(15, 23, 42, 0.45) !important;
            overflow: hidden !important;
            margin-bottom: 1.5rem !important;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            transition: transform 0.3s ease, border-color 0.3s ease !important;
        }
        .browser-frame:hover {
            transform: translateY(-3px) !important;
            border-color: rgba(34, 211, 238, 0.25) !important;
        }
        .browser-header {
            background: rgba(30, 41, 59, 0.7) !important;
            padding: 8px 12px !important;
            display: flex !important;
            align-items: center !important;
            gap: 6px !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
        }
        .browser-dot {
            width: 8px !important;
            height: 8px !important;
            border-radius: 50% !important;
            display: inline-block !important;
        }
        .browser-dot.red { background: #ef4444 !important; }
        .browser-dot.yellow { background: #f59e0b !important; }
        .browser-dot.green { background: #10b981 !important; }
        .browser-address {
            background: rgba(15, 23, 42, 0.4) !important;
            color: #94a3b8 !important;
            font-size: 0.75rem !important;
            padding: 2px 10px !important;
            border-radius: 6px !important;
            margin-left: 10px !important;
            flex-grow: 1 !important;
            font-family: monospace !important;
            text-overflow: ellipsis !important;
            overflow: hidden !important;
            white-space: nowrap !important;
        }
        .browser-content {
            padding: 12px !important;
        }
    </style>
    """, unsafe_allow_html=True)

def inject_header_element():
    st.markdown("<h1 style='font-weight:800; background: linear-gradient(135deg, #22d3ee 0%, #6366f1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 0.5rem; font-size: 3.2rem;'>SEO Domain Intelligence Agent</h1>", unsafe_allow_html=True)
    st.markdown('<p class="subtitle" style="text-align: center; color: #94a3b8; font-size: 1.15rem; margin-bottom: 2rem;">Multi-Website Enterprise SEO Analysis — Powered by Screaming Frog + Semrush + WebPageTest</p>', unsafe_allow_html=True)

def inject_footer_element():
    st.markdown("""
    <div style="
        text-align: center;
        padding: 2rem 0;
        margin-top: 3rem;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        color: #94a3b8;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    ">
        © 2026 Chronflow Made By Patel Rudra J. ,All Rights Reserved.
    </div>
    """, unsafe_allow_html=True)
