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
# --- 🤖 SMART HYBRID SEARCH ---
query = st.chat_input("Kahan jana hai? (Ex: Patna Delhi 25 May)")

if query:
    with st.chat_message("user"):
        st.write(query)

    # 1. PEHLE DIRECT CODES DHUNDNA (Fastest)
    import re
    words = query.upper().replace("TO", " ").split()
    codes = [w for w in words if len(w) == 3]
    date_match = re.search(r'\d{4}-\d{2}-\d{2}', query)
    
    origin, dest, date = None, None, None
    
    if len(codes) >= 2:
        origin, dest = codes[0], codes[1]
        date = date_match.group(0) if date_match else "2026-05-15"
    
    # 2. AGAR CODES NAHI MILE, TOH AI SE PUCHNA
    if not origin:
        try:
            prompt = f"Extract 'Origin Code', 'Dest Code', 'Date' (YYYY-MM-DD) from: '{query}'. Return ONLY 3 words. Ex: PAT DEL 2026-05-15"
            ai_response = model.generate_content(prompt).text.strip().split()
            if len(ai_response) >= 3:
                origin, dest, date = ai_response[0].upper()[:3], ai_response[1].upper()[:3], ai_response[2]
        except:
            # Agar AI fail ho jaye (Busy error), toh simple message dena
            st.error("Kripya shehar ke 3-letter codes likhein (Ex: PAT DEL 2026-05-15)")

    # 3. FLIGHTS SEARCH KARNA
    if origin and dest:
        with st.spinner(f'Searching flights for {origin} ➔ {dest}...'):
            token = get_token()
            if token:
                url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={dest}&departureDate={date}&adults=1&currencyCode=INR&max=5"
                res = requests.get(url, headers={"Authorization": f"Bearer {token}"})
                data = res.json()

                if "data" in data and len(data["data"]) > 0:
                    st.success(f"✅ {origin} se {dest} ki best deals:")
                    for flight in data["data"]:
                        price = flight['price']['total']
                        with st.container():
                            c1, c2 = st.columns([3, 1])
                            with c1:
                                st.markdown(f"#### ✈️ Flight Deal")
                                st.caption(f"📅 Date: {date} | {origin} ➔ {dest}")
                            with c2:
                                st.subheader(f"₹{price}")
                            
                            b1, b2 = st.columns(2)
                            with b1:
                                st.link_button("✈️ Book Flight", f"https://www.google.com/flights")
                            with b2:
                                st.link_button(f"🏨 Hotels in {dest}", f"https://www.booking.com/searchresults.html?ss={dest}")
                            st.markdown("---")
                else:
                    st.warning(f"Is date par {origin} se {dest} ke liye flights nahi mili.")
            else:
                st.error("API Key Issue! Please check Amadeus Keys.")
