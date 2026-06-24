import streamlit as st
from google import genai

# Setup the title of your web page
st.set_page_config(page_title="My Advanced AI Chatbot", page_icon="🤖", layout="wide")

# Use your saved Google Gemini API Key
API_KEY = "YOUR_API_KEY_HERE"

# --- SIDEBAR INTERFACE ---
with st.sidebar:
    st.title("⚙️ AI Configuration")
    st.write("Customize your AI behavior below:")
    
    # Dropdown menu to select AI role
    ai_role = st.selectbox(
        "Choose AI Personality:",
        ["Standard Assistant", "Technical Interview Coach", "Expert Code Debugger", "Resume & Profile Optimizer"]
    )
    
    st.divider()
    st.info("💡 Tip: Change the personality anytime to test different responses!")

# Define system instructions based on selection
system_prompts = {
    "Standard Assistant": "You are a helpful, clear, and polite AI assistant.",
    "Technical Interview Coach": "You are an elite tech interviewer. Ask sharp follow-up questions, critique code design, and evaluate data structures closely.",
    "Expert Code Debugger": "You are an expert software engineer. Review code, find logic bugs, and provide clean refactored solutions with brief explanations.",
    "Resume & Profile Optimizer": "You are an expert tech recruiter. Help engineering students rewrite their project summaries, skills sections, and LinkedIn bios to attract top IT companies. Always output clean, bulleted text that looks professional on a CV."
}

selected_instruction = system_prompts[ai_role]

# Display main page titles
st.title("🤖 Welcome to My Custom AI Engine")
st.write(f"Current Mode: **{ai_role}**")

# Initialize chat history if it doesn't exist yet
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me anything..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Connect to Google Gemini API
        client = genai.Client(api_key=API_KEY)
        
        # Pass the system prompt instruction directly into the configuration parameter
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={'system_instruction': selected_instruction}
        )
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"Error connecting to AI: {e}\nVerify that your server environment is active.")

