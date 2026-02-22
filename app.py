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
# --- 🤖 SMART AI SECTION (Enhanced) ---
query = st.chat_input("Kahan jana hai? (Ex: Patna to Delhi 25 May)")

if query:
    with st.chat_message("user"):
        st.write(query)

    # AI ko bilkul saaf instruction dena
    prompt = f"User query: '{query}'. Provide ONLY the 3-letter Origin code, 3-letter Destination code, and Date in YYYY-MM-DD. Example: PAT DEL 2026-05-15. Use 2026-05-15 if date is missing."
    
    try:
        with st.spinner('Aapki baat samajh raha hoon... ✨'):
            response = model.generate_content(prompt)
            # AI ke response ko saaf karna
            raw_text = response.text.strip().replace('"', '').replace("'", "")
            ai_response = raw_text.split()
            
            if len(ai_response) >= 3:
                origin, dest, date = ai_response[0][:3].upper(), ai_response[1][:3].upper(), ai_response[2]
                
                token = get_token()
                if token:
                    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={dest}&departureDate={date}&adults=1&currencyCode=INR&max=5"
                    res = requests.get(url, headers={"Authorization": f"Bearer {token}"})
                    data = res.json()

                    with st.chat_message("assistant"):
                        if "data" in data and len(data["data"]) > 0:
                            st.success(f"✅ {origin} ➔ {dest} ki deals:")
                            for flight in data["data"]:
                                price = flight['price']['total']
                                with st.container():
                                    c1, c2 = st.columns([3, 1])
                                    with c1:
                                        st.markdown(f"#### ✈️ Flight Deal")
                                        st.caption(f"📅 Date: {date}")
                                    with c2:
                                        st.subheader(f"₹{price}")
                                    st.link_button("✈️ Book Flight", "https://www.google.com/flights")
                                    st.markdown("---")
                        else:
                            st.warning(f"Maaf kijiye, {origin} to {dest} ki flight nahi mili.")
            else:
                st.error("Please provide city names clearly (e.g., Patna to Delhi).")
    except Exception as e:
        st.error("AI thoda slow hai, kripya direct likhein: PAT DEL 2026-05-15")
