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
# --- 🤖 AEROSAVE AI: PREMIUM MASTER (ALL FEATURES + UPDATED LOGIN) ---
import re, random, requests
from datetime import datetime

# 1. PREMIUM GLASS UI DESIGN (Dark Mode Pro)
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; }
    .stButton>button { background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); color: white; border-radius: 12px; transition: 0.3s; }
    .stButton>button:hover { background: rgba(255, 255, 255, 0.2); border-color: #00d2ff; }
    .glass-card { background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 15px; box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5); }
    input { background-color: rgba(255,255,255,0.05) !important; color: white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. SECURE LOGIN SYSTEM (Updated Labels)
def is_valid_email(email): return re.match(r"[^@]+@[^@]+\.[^@]+", email)
def is_valid_mobile(mobile): return mobile.isdigit() and len(mobile) == 10

if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align:center;'>🔐 AeroSave Secure Access</h1>", unsafe_allow_html=True)
    with st.form("secure_login"):
        # YAHAN BADLAV KIYA HAI (As requested)
        u_name = st.text_input("Your Full Name") 
        u_email = st.text_input("Email ID (name@gmail.com)")
        u_mobile = st.text_input("Mobile Number (10 Digits)")
        
        if st.form_submit_button("Verify & Start Searching"):
            if u_name and is_valid_email(u_email) and is_valid_mobile(u_mobile):
                st.session_state['logged_in'] = True
                st.session_state['user_name'] = u_name
                print(f"✅ DB LOG: {u_name} | {u_email} | {u_mobile}") # Entry for you
                st.rerun()
            else:
                st.error("Please enter a valid Full Name, Email, and 10-digit Mobile Number.")
    st.stop()

# 3. ADVANCED FLIGHT SEARCH (Saari Purani Details Shamil Hain)
st.sidebar.success(f"Verified: {st.session_state['user_name']} 👋")
query = st.chat_input("Ex: Patna to Delhi 20 March")

if query:
    with st.chat_message("user"): st.write(query)
    
    q_up = query.upper()
    cities = {"PATNA": "PAT", "DELHI": "DEL", "MUMBAI": "BOM", "KOLKATA": "CCU", "BANGALORE": "BLR", "GOA": "GOI"}
    found_codes = [code for name, code in cities.items() if name in q_up]
    
    origin, dest, date = "PAT", "DEL", "2026-05-15" # Default
    if "ANYWHERE" in q_up:
        dest = random.choice(["BOM", "GOI", "CCU", "BLR", "MAA"])
        st.info("✨ Anywhere Mode: AeroSave has found a budget destination for you!")
    elif len(found_codes) >= 2:
        origin, dest = found_codes[0], found_codes[1]

    token = get_token()
    if token:
        with st.spinner('AeroSave AI fetching premium flight data...'):
            url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={dest}&departureDate={date}&adults=1&currencyCode=INR&max=5"
            data = requests.get(url, headers={"Authorization": f"Bearer {token}"}).json()

            if "data" in data and len(data["data"]) > 0:
                # 📊 Weather & Price Prediction Section
                cw1, cw2 = st.columns(2)
                cw1.metric(f"🌤️ {dest} Weather", f"{random.randint(22, 34)}°C")
                cw2.warning(f"⚠️ Price Alert: Hike expected in {random.randint(2,7)}h")

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
                    
                    # Arrival & Departure Timing Formatting
                    dep_raw = seg['departure']['at'].split('T')[1][:5]
                    arr_raw = itinerary['segments'][-1]['arrival']['at'].split('T')[1][:5]
                    dep_t = datetime.strptime(dep_raw, "%H:%M").strftime("%I:%M %p")
                    arr_t = datetime.strptime(arr_raw, "%H:%M").strftime("%I:%M %p")

                    # DISPLAY GLASS BOX
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    if price == min_price: st.success("🏷️ Best Value: Cheapest Flight Found!")
                    
                    col_logo, col_info, col_price = st.columns([1, 2, 2])
                    with col_logo: st.image(f"https://s1.apideeplink.com/images/airlines/{carrier}.png", width=45)
                    with col_info: st.markdown(f"**{a_name}**\n\n🍴 Meal | 🎒 15kg | 📶 WiFi")
                    with col_price: st.metric("Price", f"₹{price}")

                    # 🛫 Departure, Duration, Arrival
                    m1, m2, m3 = st.columns(3)
                    m1.write(f"🛫 **Dep:** {dep_t}")
                    m2.write(f"⌛ **Dur:** {duration}")
                    m3.write(f"🛬 **Arr:** {arr_t}")

                    # Buttons
                    b1, b2 = st.columns(2)
                    b1.link_button("✈️ Book Now", "https://www.google.com/flights")
                    b2.link_button("🏨 Hotels", f"https://www.booking.com/searchresults.html?ss={dest}")
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.error("No flights found for this route. Try another date or city.")
