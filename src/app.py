
# First
import openai
import streamlit as st
from engine import ComparisonEngine


st.title("💬 シャンプー比較チャットボット")
if "engine" not in st.session_state:
    st.session_state["engine"] = ComparisonEngine()
    st.session_state.engine.ask_gpt(prompt="シャンプーを探してます。")
for msg in st.session_state.engine.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    msg = st.session_state.engine.ask_gpt(prompt=prompt)
    st.chat_message("assistant").write(msg)
