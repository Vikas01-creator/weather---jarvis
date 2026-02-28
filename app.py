import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from utils import get_live_weather, get_forecast_data 

# --- UI CONFIGURATION ---
st.set_page_config(page_title="J.A.R.V.I.S. | Weather Systems", layout="wide")

# --- TEXT TO SPEECH FUNCTION ---
def st_speak(text):
    """Injects JavaScript to trigger browser Text-to-Speech."""
    components.html(f"""
        <script>
        var msg = new SpeechSynthesisUtterance('{text}');
        msg.rate = 0.9;
        msg.pitch = 1.0;
        window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# --- CUSTOM GLASSMORPHISM CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), 
                    url('https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-attachment: fixed;
    }

    div[data-testid="stMetric"], .stMetric, div.stButton > button, .glass-card {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    h1, h2, h3, h4, p, span, label {
        color: white !important;
        font-family: 'Inter', sans-serif;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.5);
    }

    div[data-testid="stMetricValue"] {
        color: #00d4ff !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }

    .stTextInput input {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    .console-text { 
        font-family: 'Courier New', monospace; 
        color: #00ff41; 
        font-size: 0.85rem;
        background: rgba(0,0,0,0.4);
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>🛰️ ATMOSPHERIC DIAGNOSTICS</h1>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### SYSTEM LOG")
    log_area = st.empty()
    log_area.markdown('<p class="console-text">> SYSTEM ONLINE<br>> STACK: GLASS-V2</p>', unsafe_allow_html=True)

# --- INPUT SECTION ---
col_input, col_spacer = st.columns([2, 3])
with col_input:
    city = st.text_input("TARGET COORDINATES", "London")
    execute = st.button("INITIATE SCAN")

if execute:
    data = get_live_weather(city)
    forecast = get_forecast_data(city) 
    
    if data and forecast:
        # --- DATA PROCESSING FOR ANALYTICS ---
        df = pd.DataFrame(forecast)
        # Identify key days
        sunniest_idx = df['temp'].idxmax()
        sunniest_day = df.iloc[sunniest_idx]
        
        # Checking if 'wind' exists in your utility data, else defaulting to 0
        windiest_day = df.iloc[df['wind'].idxmax()] if 'wind' in df.columns else None

        # --- VOICE FEEDBACK ---
        temp_val = data['main']['temp']
        speech_text = f"Scanning {city}. 6-day projection uploaded. Peak temperature of {sunniest_day['temp']} degrees expected on {sunniest_day['time']}."
        st_speak(speech_text)

        # --- CURRENT STATS ---
        st.markdown(f"### LIVE FEED: {city.upper()}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("TEMP", f"{temp_val}°C")
        c2.metric("HUMIDITY", f"{data['main']['humidity']}%")
        c3.metric("WIND", f"{data.get('wind', {}).get('speed', 0)} km/h")
        c4.metric("PRESSURE", f"{data['main']['pressure']} hPa")

        # --- GRAPH & FORECAST SECTION ---
        col_graph, col_list = st.columns([3, 2])

        with col_graph:
            st.write("#### 📈 PREDICTIVE TREND")
            fig = px.line(df, x='time', y='temp', markers=True, template="plotly_dark")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='#ffffff',
                margin=dict(l=0, r=0, t=20, b=0),
                height=400
            )
            fig.update_traces(line_color='#00d4ff', line_width=4, fill='toself', fillcolor='rgba(0, 212, 255, 0.1)')
            st.plotly_chart(fig, use_container_width=True)

        with col_list:
            fig = px.line(df, x='time', y='temp', markers=True, template="plotly_dark")
            st.write("#### 📅 6-DAY PROJECTION")
            # Loop through 7 items specifically
            for i, day in df.head(7).iterrows():
                st.markdown(f"""
                <div class="glass-card" style="margin-bottom:8px; padding:10px !important; display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:0.9rem;">{day['time']}</span>
                    <span style="color:#00d4ff; font-weight:bold;">{day['temp']}°C</span>
                </div>
                """, unsafe_allow_html=True)

        # --- AI ANALYTICS: SUNNIEST & WINDIEST ---
        st.write("---")
        st.write("#### 🧠 NEURAL NETWORK ANALYSIS")
        
        an_col1, an_col2 = st.columns(2)
        
        with an_col1:
            st.markdown(f"""
                <div class="glass-card" style="text-align:center; border: 1px solid #ffaa0066;">
                    <small style="letter-spacing:2px; color:#ffaa00;">OPTIMAL SOLAR WINDOW</small>
                    <h2 style="color:#ffaa00 !important; margin:10px 0;">{sunniest_day['time']}</h2>
                    <p>Highest Thermal Activity: <b>{sunniest_day['temp']}°C</b></p>
                </div>
                """, unsafe_allow_html=True)

        with an_col2:
            w_speed = windiest_day['wind'] if windiest_day is not None else "N/A"
            w_time = windiest_day['time'] if windiest_day is not None else "N/A"
            st.markdown(f"""
                <div class="glass-card" style="text-align:center; border: 1px solid #00ff4166;">
                    <small style="letter-spacing:2px; color:#00ff41;">PEAK KINETIC VELOCITY</small>
                    <h2 style="color:#00ff41 !important; margin:10px 0;">{w_time}</h2>
                    <p>Max Wind Speed: <b>{w_speed} km/h</b></p>
                </div>
                """, unsafe_allow_html=True)
        
        log_area.markdown(f'<p class="console-text">> SCAN COMPLETE<br>> TARGET: {city}<br>> 7-DAY DATA RENDERED</p>', unsafe_allow_html=True)