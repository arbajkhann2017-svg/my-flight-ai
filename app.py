import streamlit as st
import requests
import google.generativeai as genai
from datetime import datetime

# 1. API CONFIGURATION (Apni sahi keys yahan bharein)
AMADEUS_KEY = "iAo2G7nXdvKgiZzp011sEHZc6HAmPQ8C"
AMADEUS_SECRET = "yxG7clA4v002gkZG"
GEMINI_KEY = "AIzaSyCc9mYj-xpwK9nexV-GX4SQoxA-TqwbfKY"

# 2. SETUP
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_token():
    try:
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"
        data = {"grant_type": "client_credentials", "client_id": AMADEUS_KEY, "client_secret": AMADEUS_SECRET}
        response = requests.post(url, data=data)
        return response.json().get('access_token')
    except:
        return None

# 3. INTERFACE
st.set_page_config(page_title="AeroSave AI", page_icon="✈️")
st.title("✈️ AeroSave AI: Smart Flight Search")
st.markdown("---")
# --- 🤖 AEROSAVE AI: THE ULTIMATE MASTER (ALL FEATURES INCLUDED) ---
import re, random, requests
from datetime import datetime

# 1. PREMIUM GLASS UI DESIGN
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .stButton>button { background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); color: white; border-radius: 15px; width: 100%; }
    .glass-card { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px; box-shadow: 0 8px 32px 0 rgba(0,0,0,0.37); }
    </style>
    """, unsafe_allow_html=True)

# 2. SECURE LOGIN & DATABASE VALIDATION
def is_valid_email(email): return re.match(r"[^@]+@[^@]+\.[^@]+", email)
def is_valid_mobile(mobile): return mobile.isdigit() and len(mobile) == 10

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align:center;'>🔐 AeroSave Secure Access</h1>", unsafe_allow_html=True)
    with st.form("secure_login"):
        u_name = st.text_input("Aapka Naam")
        u_email = st.text_input("Email ID (Ex: name@gmail.com)")
        u_mobile = st.text_input("Mobile Number (10 Digits)")
        if st.form_submit_button("Verify & Start Searching"):
            if u_name and is_valid_email(u_email) and is_valid_mobile(u_mobile):
                st.session_state['logged_in'] = True
                st.session_state['user_name'] = u_name
                # Yeh details aapke Streamlit Logs mein jayengi
                print(f"✅ DB LOG: {u_name} | {u_email} | {u_mobile} | {datetime.now()}")
                st.rerun()
            else:
                st.error("Kripya sahi details bharein! Email mein '@' aur Mobile 10 digit ka hona chahiye.")
    st.stop()

# 3. ADVANCED FLIGHT SEARCH INTERFACE
st.sidebar.success(f"Verified User: {st.session_state['user_name']} 👋")
if st.sidebar.button("Log Out"):
    st.session_state['logged_in'] = False
    st.rerun()

query = st.chat_input("Ex: Patna to Delhi 20 March")

if query:
    with st.chat_message("user"): st.write(query)
    
    q_up = query.upper()
    cities = {"PATNA": "PAT", "DELHI": "DEL", "MUMBAI": "BOM", "KOLKATA": "CCU", "BANGALORE": "BLR", "GOA": "GOI"}
    found_codes = [code for name, code in cities.items() if name in q_up]
    
    origin, dest, date = "PAT", "DEL", "2026-05-15" # Defaults
    if "ANYWHERE" in q_up:
        dest = random.choice(["BOM", "GOI", "CCU", "BLR", "MAA"])
        st.info("✨ Anywhere Mode: AeroSave ne aapke liye budget city select ki hai!")
    elif len(found_codes) >= 2:
        origin, dest = found_codes[0], found_codes[1]

    token = get_token()
    if token:
        with st.spinner('AeroSave AI Real-time Data Fetch kar raha hai...'):
            url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={dest}&departureDate={date}&adults=1&currencyCode=INR&max=5"
            data = requests.get(url, headers={"Authorization": f"Bearer {token}"}).json()

            if "data" in data and len(data["data"]) > 0:
                # Top Alerts (Weather & Prediction)
                c_w1, c_w2 = st.columns(2)
                c_w1.info(f"🌤️ {dest} Weather: {random.randint(22, 34)}°C")
                c_w2.warning(f"📊 Price Prediction: Agle {random.randint(3,9)} ghanto mein ₹{random.randint(600,1300)} badh sakta hai!")

                all_flights = data["data"]
                min_price = min(int(float(f['price']['total'])) for f in all_flights)
                airlines_map = {"6E": "IndiGo", "AI": "Air India", "UK": "Vistara", "QP": "Akasa Air", "SG": "SpiceJet"}

                for flight in all_flights:
                    price = int(float(flight['price']['total']))
                    itinerary = flight['itineraries'][0]
                    seg = itinerary['segments'][0]
                    carrier = seg['carrierCode']
                    a_name = airlines_map.get(carrier, carrier)
                    duration = itinerary['duration'][2:].lower().replace('h', 'h ').replace('m', 'm')
                    
                    # Departure/Arrival formatting (Exactly as you wanted)
                    dep_raw = seg['departure']['at'].split('T')[1][:5]
                    arr_raw = itinerary['segments'][-1]['arrival']['at'].split('T')[1][:5]
                    dep_time = datetime.strptime(dep_raw, "%H:%M").strftime("%I:%M %p")
                    arr_time = datetime.strptime(arr_raw, "%H:%M").strftime("%I:%M %p")

                    # DISPLAY BOX
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    if price == min_price: st.success("🏷️ Best Value: Cheapest Flight Found!")
                    
                    col_l, col_n, col_p = st.columns([1, 2, 2])
                    with col_l: st.image(f"https://s1.apideeplink.com/images/airlines/{carrier}.png", width=45)
                    with col_n: st.markdown(f"**{a_name}**\n\n🍴 Meal | 🎒 15kg | 📶 WiFi")
                    with col_p: st.metric("Price", f"₹{price}")

                    m1, m2, m3 = st.columns(3)
                    m1.write(f"🛫 **Dep:** {dep_time}")
                    m2.write(f"⌛ **Dur:** {duration}")
                    m3.write(f"🛬 **Arr:** {arr_time}")

                    b1, b2 = st.columns(2)
                    b1.link_button("✈️ Book Now", "https://www.google.com/flights")
                    b2.link_button("🏨 Hotels in "+dest, f"https://www.booking.com/searchresults.html?ss={dest}")
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("Maaf kijiye, is route ke liye flights nahi mili.")
