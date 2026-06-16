import streamlit as st
import google.generativeai as genai  # <-- Line 2: Real Gemini library import ki

# 1. Page Configuration
st.set_page_config(page_title="AI Customer Support Bot", page_icon="🤖", layout="centered")

# UptimeRobot Ping Handler (Bot Ko 24 Ghante Zinda Rakhne Ke Liye)
try:
    if "ping" in st.query_params:
        st.write("Jaag raha hoon bahi!")
        st.stop()
except AttributeError:
    pass

# 2. API Key Aur Model Configuration (Yahan Se Bot Active Hoga)
# Streamlit Secrets se aapki Gemini API Key khud uthaye ga bahi
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Fiverr client ke liye best aur fast model
    model = genai.GenerativeModel('gemini-3.5-flash') 
except Exception as e:
    st.error("Yaar API Key ka masla ha! Streamlit Secrets mein 'GEMINI_API_KEY' check karein bahi.")

# 3. Layout & Styling
st.title("🤖 Smart AI Customer Support Assistant")
st.write("Welcome! This AI bot handles customer queries and captures leads 24/7.")
st.markdown("---")

# 4. Lead Generation Form (Sidebar)
with st.sidebar:
    st.header("📩 Contact Us / Drop Details")
    with st.form("lead_form", clear_on_submit=True):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        msg = st.text_area("Briefly describe your requirement")
        submit = st.form_submit_button("Submit Details")
        
        if submit:
            if name and email:
                st.success(f"Thank you {name}! Our team will contact you at {email}.")
            else:
                st.error("Please fill in your Name and Email bahi!")

# 5. Chatbot Core Logic
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI Support Assistant. How can I help your business today?"}
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input & Active AI Generation
if user_input := st.chat_input("Ask me anything about our services..."):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Real Gemini Model Response Generation (Line 61 se 67)
    with st.chat_message("assistant"):
        with st.spinner("AI is thinking..."):
            try:
                # Yeh line real model se jawab mangti hai bahi
                response = model.generate_content(user_input)
                ai_response = response.text
            except Exception as e:
                ai_response = "Sorry bahi, standard response error. Please check API quota or connection."
            
            st.write(ai_response)
            
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
