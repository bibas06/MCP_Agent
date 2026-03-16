import streamlit as st
import requests
import json

st.set_page_config(
    page_title="MCP AI Agent",
    page_icon="🤖",
    layout="wide"
)

API_URL = "http://localhost:8000/chat"

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.title("🤖 MCP AI Agent")
    st.markdown("---")
    st.markdown("### Available Tools")
    st.markdown("- 🔍 Web Search")
    st.markdown("- 📅 Calendar Events")
    st.markdown("- 🐙 GitHub Repositories")
    
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ Connected to API")
        else:
            st.error("❌ API connection issue")
    except:
        st.error("❌ API not reachable")
        st.info("Start the API gateway with: python api_gateway.py")

st.title("🎯 Multi MCP LangGraph Assistant")

for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.write(msg)

user_input = st.chat_input("Ask something...")

if user_input:
    st.session_state.history.append(("user", user_input))
    
    with st.chat_message("user"):
        st.write(user_input)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"query": user_input},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("response", "No response")
                else:
                    answer = f"Error: API returned status {response.status_code}"
            
            except requests.exceptions.ConnectionError:
                answer = "❌ Cannot connect to API. Make sure the gateway is running on port 8000"
            except Exception as e:
                answer = f"❌ Error: {str(e)}"
            
            st.write(answer)
    
    st.session_state.history.append(("assistant", answer))

if not st.session_state.history:
    st.info("👆 Start by typing a question above!")
