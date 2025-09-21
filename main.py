import streamlit as st

from src.agent.agent_graph import get_agent_response

st.set_page_config(page_title="ChatBet Agent", page_icon="🤖")

st.title("🤖 ChatBet Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Escribe tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = str(get_agent_response(prompt))
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
