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
# --- 🤖 POWERFUL SMART SEARCH (Timing + NLP) ---
query = st.chat_input("Ex: Patna to Delhi 20 March")

if query:
    with st.chat_message("user"):
        st.write(query)

    import re
    # 1. PEHLE DIRECT CODES AUR DATE NIKALNA (Bina AI ke)
    q_up = query.upper().replace("TO", " ")
    city_codes = re.findall(r'\b[A-Z]{3}\b', q_up) # PAT, DEL jaise codes dhoondna
    date_match = re.search(r'\d{4}-\d{2}-\d{2}', query) # 2026-03-20 dhoondna

    origin, dest, date = None, None, None

    # Agar user ne codes diye hain (Ex: PAT DEL 2026-03-20)
    if len(city_codes) >= 2:
        origin, dest = city_codes[0], city_codes[1]
        date = date_match.group(0) if date_match else "2026-03-20"
    
    # 2. AGAR CODES NAHI MILE, TOH AI SE HELP LENA
    if not origin:
        try:
            prompt = f"Extract only IATA codes and date (YYYY-MM-DD) from: '{query}'. Output: ORIGIN DEST DATE. Use 2026 if no year."
            ai_res = model.generate_content(prompt).text.strip().split()
            if len(ai_res) >= 3:
                origin, dest, date = ai_res[0].upper(), ai_res[1].upper(), ai_res[2]
        except:
            st.error("AI Busy hai, kripya codes use karein: PAT DEL 2026-03-20")

    # 3. FLIGHT RESULTS DIKHANA (With Timing)
    if origin and dest:
        with st.spinner(f'Searching {origin} ➔ {dest} for {date}...'):
            token = get_token()
            if token:
                url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={dest}&departureDate={date}&adults=1&currencyCode=INR&max=5"
                res = requests.get(url, headers={"Authorization": f"Bearer {token}"})
                data = res.json()

                if "data" in data and len(data["data"]) > 0:
                    st.success(f"✅ Flights mili hain! ({origin} to {dest})")
                    for flight in data["data"]:
                        price = int(float(flight['price']['total']))
                        seg = flight['itineraries'][0]['segments'][0]
                        # Flight timing nikalna
                        d_time = seg['departure']['at'].split('T')[1][:5]
                        a_time = seg['arrival']['at'].split('T')[1][:5]
                        
                        with st.container():
                            # UI ko sundar dikhana metrics ke saath
                            m1, m2, m3 = st.columns(3)
                            m1.metric("🛫 Udne ka Time", d_time)
                            m2.metric("🛬 Pahunchne ka Time", a_time)
                            m3.metric("💰 Kiraya", f"₹{price}")
                            
                            b1, b2 = st.columns(2)
                            b1.link_button("✈️ Ticket Book Karein", "https://www.google.com/flights")
                            b2.link_button("🏨 Hotel Dekhein", f"https://www.booking.com/searchresults.html?ss={dest}")
                            st.markdown("---")
                else:
                    st.warning(f"Maaf kijiye, {origin} se {dest} ke liye flights nahi mili.")
            else:
                st.error("API Key ka issue hai. Amadeus Keys check karein.")
