import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="AI Customer Support Bot", page_icon="🤖", layout="centered")

# 🤫 Anti-Sleep & Clean Layout (Top Options Mita Diye Hain)
anti_sleep_and_hide = """
            <meta http-equiv="refresh" content="300">
            <style>
            [data-testid="stToolbar"] {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            header {visibility: hidden !important;}
            #MainMenu {visibility: hidden !important;}
            </style>
            """
st.markdown(anti_sleep_and_hide, unsafe_allow_html=True)

# UptimeRobot Ping Handler
try:
    if "ping" in st.query_params:
        st.write("Jaag raha hoon bahi!")
        st.stop()
except AttributeError:
    pass

# 2. API Key Aur Model Configuration
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-3.5-flash')
except Exception as e:
    st.error("Yaar API Key ka masla ha! Streamlit Secrets mein 'GEMINI_API_KEY' check karein bahi.")

# 3. Session State for Lead Unlock (Check karne ke liye ke user ne data diya ya nahi)
if "lead_unlocked" not in st.session_state:
    st.session_state.lead_unlocked = False

st.title("🤖 Smart AI Customer Support Assistant")
st.write("Welcome! Chat with our 24/7 AI Support.")
st.markdown("---")

# 🚪 STEP 1: Agar user ne details nahi daalyein, toh pehle Form dikhao
if not st.session_state.lead_unlocked:
    st.subheader("📩 Please introduce yourself to start chatting")
    
    with st.form("lead_lock_form", clear_on_submit=False):
        user_name = st.text_input("Your Name", placeholder="John Doe")
        user_email = st.text_input("Your Email", placeholder="john@example.com")
        submit_btn = st.form_submit_button("Start AI Chat 🚀")
        
        if submit_btn:
            if user_name and user_email:
                st.session_state.lead_unlocked = True
                st.session_state.customer_name = user_name
                st.session_state.customer_email = user_email
                st.rerun()  # Page ko refresh kar ke chat kholne ke liye
            else:
                st.error("Bahi, apna Name aur Email laazmi likhein! ⚠️")

# 💬 STEP 2: Jab user form submit kar dega, toh Chatbot khul jayega bahi!
else:
    st.success(f"Welcome **{st.session_state.customer_name}**! AI Chat is now Active.")
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Hello {st.session_state.customer_name}! I am your AI Support Assistant. How can I help your business today?"}
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
        
        with st.chat_message("assistant"):
            with st.spinner("AI is thinking..."):
                try:
                    # Professional System Prompt ke sath call bahi
                    prompt = f"You are a professional customer support bot. Answer the user's question politely. User Name: {st.session_state.customer_name}. Question: {user_input}"
                    response = model.generate_content(prompt)
                    ai_response = response.text
                except Exception as e:
                    ai_response = "Sorry bahi, connection issue. Please try again."
                
                st.write(ai_response)
                
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
