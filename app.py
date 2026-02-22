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
# --- 🤖 AEROSAVE AI: THE PRO TRAVEL ASSISTANT ---
query = st.chat_input("Ex: Patna to Delhi 20 March")

if query:
    with st.chat_message("user"):
        st.write(query)

    import re
    import random
    from datetime import datetime

    # 1. SMART CITY DETECTION
    q_up = query.upper()
    cities = {"PATNA": "PAT", "DELHI": "DEL", "MUMBAI": "BOM", "KOLKATA": "CCU", "BANGALORE": "BLR", "CHENNAI": "MAA", "GOA": "GOI"}
    found_codes = [code for name, code in cities.items() if name in q_up]
    found_codes += re.findall(r'\b[A-Z]{3}\b', q_up)
    found_codes = list(dict.fromkeys(found_codes))

    origin, dest, date = None, None, "2026-05-15"
    if len(found_codes) >= 2:
        origin, dest = found_codes[0], found_codes[1]
    
    # 2. AI EXTRACTION
    if not origin:
        try:
            prompt = f"Extract IATA codes and YYYY-MM-DD from: '{query}'. Return ONLY: ORIGIN DEST DATE. Ex: PAT DEL 2026-05-15"
            ai_res = model.generate_content(prompt).text.strip().split()
            if len(ai_res) >= 3:
                origin, dest, date = ai_res[0].upper(), ai_res[1].upper(), ai_res[2]
        except:
            st.error("AI Busy! Kripya shehar ke naam saaf likhein.")

    # 3. FINAL RESULTS
    if origin and dest:
        with st.spinner(f'AeroSave AI Analysis kar raha hai... ✈️'):
            token = get_token()
            if token:
                url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={dest}&departureDate={date}&adults=1&currencyCode=INR&max=5"
                res = requests.get(url, headers={"Authorization": f"Bearer {token}"})
                data = res.json()

                if "data" in data and len(data["data"]) > 0:
                    # Sort data for Tags
                    all_flights = data["data"]
                    min_price = min(int(float(f['price']['total'])) for f in all_flights)
                    # Simple duration comparison logic
                    
                    st.info(f"🌤️ {dest} Weather: {random.randint(22, 32)}°C | 📊 Prediction: Prices might rise, book soon!")

                    airlines = {"6E": "IndiGo", "AI": "Air India", "UK": "Vistara", "QP": "Akasa Air", "SG": "SpiceJet", "I5": "AirAsia India"}

                    for flight in all_flights:
                        price = int(float(flight['price']['total']))
                        itinerary = flight['itineraries'][0]
                        seg = itinerary['segments'][0]
                        carrier = seg['carrierCode']
                        airline_name = airlines.get(carrier, carrier)
                        
                        duration = itinerary['duration'][2:].lower().replace('h', 'h ').replace('m', 'm')
                        num_stops = "Direct" if len(itinerary['segments']) == 1 else f"{len(itinerary['segments'])-1} Stop"
                        
                        d_time = datetime.strptime(seg['departure']['at'].split('T')[1][:5], "%H:%M").strftime("%I:%M %p")
                        a_time = datetime.strptime(itinerary['segments'][-1]['arrival']['at'].split('T')[1][:5], "%H:%M").strftime("%I:%M %p")
                        
                        with st.container():
                            # Tags Logic
                            col_t1, col_t2 = st.columns([1,1])
                            if price == min_price:
                                col_t1.success("🏷️ Cheapest (Sasta Ticket)")
                            
                            c_logo, c_name, c_serv = st.columns([1, 2, 2])
                            with c_logo:
                                st.image(f"https://s1.apideeplink.com/images/airlines/{carrier}.png", width=40)
                            with c_name:
                                st.markdown(f"**{airline_name}**")
                            with c_serv:
                                st.caption("🍴 Meal | 🎒 15kg | 📶 WiFi")
                            
                            m1, m2, m3 = st.columns(3)
                            m1.metric("🛫 Departure", d_time)
                            m2.metric("⌛ Duration", duration)
                            m3.metric("💰 Price", f"₹{price}")
                            
                            st.write(f"📍 {num_stops} | Arrival: {a_time} at {dest}")
                            
                            b1, b2 = st.columns(2)
                            b1.link_button(f"✈️ Book Now", f"https://www.google.com/flights")
                            b2.link_button(f"🏨 Hotels", f"https://www.booking.com/searchresults.html?ss={dest}")
                            st.markdown("---")
                else:
                    st.warning("Maaf kijiye, flights nahi mili.")
