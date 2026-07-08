import streamlit as st
from rag import ask   # reuse your same RAG engine

st.title("🎯 Polymarket Prediction Chatbot")
st.write("Ask me anything about current Polymarket prediction markets.")

# a text box for the question
question = st.text_input("Your question:", placeholder="e.g. what markets are about crypto?")

# when they type something and hit enter, answer it
if question:
    with st.spinner("Thinking..."):
        answer = ask(question)
    st.write("### Answer")
    st.write(answer)