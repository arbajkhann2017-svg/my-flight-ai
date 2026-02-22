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
# --- 🤖 ULTRA SMART SEARCH (AM/PM + Clear Examples) ---

# Chat box mein examples likhe hain taaki log dekh kar samajh sakein
query = st.chat_input("Ex: Patna to Delhi 20 March OR PAT BOM 2026-05-15")

if query:
    with st.chat_message("user"):
        st.write(query)

    import re
    from datetime import datetime

    # 1. PEHLE KHUD DHUNDNA (City Detection)
    q_up = query.upper()
    cities = {"PATNA": "PAT", "DELHI": "DEL", "MUMBAI": "BOM", "KOLKATA": "CCU", "BANGALORE": "BLR", "CHENNAI": "MAA", "GOA": "GOI", "PAT": "PAT", "DEL": "DEL", "BOM": "BOM"}
    
    found_codes = []
    for word in q_up.split():
        clean_word = word.strip(",.?!")
        if clean_word in cities:
            found_codes.append(cities[clean_word])
        elif len(clean_word) == 3 and clean_word.isalpha():
            found_codes.append(clean_word)

    found_codes = list(dict.fromkeys(found_codes))
    origin, dest, date = None, None, "2026-05-15"

    if len(found_codes) >= 2:
        origin, dest = found_codes[0], found_codes[1]
    
    # 2. AI SE POOCHNA (Agar shehar nahi mile)
    if not origin:
        try:
            prompt = f"Extract IATA codes and YYYY-MM-DD from: '{query}'. Return ONLY: ORIGIN DEST DATE. Ex: PAT DEL 2026-05-15"
            ai_res = model.generate_content(prompt).text.strip().split()
            if len(ai_res) >= 3:
                origin, dest, date = ai_res[0].upper(), ai_res[1].upper(), ai_res[2]
        except:
            st.error("Kripya shehar ke naam saaf likhein (Ex: Patna Delhi)")

    # 3. RESULTS DIKHANA
    if origin and dest:
        with st.spinner(f'Searching {origin} ➔ {dest}...'):
            token = get_token()
            if token:
                url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={dest}&departureDate={date}&adults=1&currencyCode=INR&max=5"
                res = requests.get(url, headers={"Authorization": f"Bearer {token}"})
                data = res.json()

                if "data" in data and len(data["data"]) > 0:
                    st.success(f"✅ Flights for {origin} to {dest} on {date}")
                    for flight in data["data"]:
                        price = int(float(flight['price']['total']))
                        seg = flight['itineraries'][0]['segments'][0]
                        
                        # --- TIME KO AM/PM MEIN BADALNA ---
                        d_raw = seg['departure']['at'].split('T')[1][:5]
                        a_raw = seg['arrival']['at'].split('T')[1][:5]
                        
                        dep_obj = datetime.strptime(d_raw, "%H:%M")
                        arr_obj = datetime.strptime(a_raw, "%H:%M")
                        
                        dep_time = dep_obj.strftime("%I:%M %p") # 02:30 PM format
                        arr_time = arr_obj.strftime("%I:%M %p")
                        
                        with st.container():
                            c1, c2, c3 = st.columns(3)
                            c1.metric("🛫 Departure", dep_time)
                            c2.metric("🛬 Arrival", arr_time)
                            c3.metric("💰 Price", f"₹{price}")
                            
                            b1, b2 = st.columns(2)
                            b1.link_button("✈️ Book Flight", "https://www.google.com/flights")
                            b2.link_button("🏨 Hotels", f"https://www.booking.com/searchresults.html?ss={dest}")
                            st.markdown("---")
                else:
                    st.warning("No flights found.")
