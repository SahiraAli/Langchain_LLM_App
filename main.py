# main.py

import streamlit as st
import langchain_helper as lh

st.title("Blog Title Generator")

# --- Sidebar Inputs ---
st.sidebar.header("Customize Your Request")

topic = st.sidebar.text_input("Enter blog topic:", placeholder="e.g., Artificial Intelligence")
adjective = st.sidebar.text_input(
    "Blog title style:",
    placeholder="e.g., creative, academic, funny, SEO-friendly"
)

# --- Button ---
if st.sidebar.button("Generate Titles"):
    if not topic or not adjective:
        st.error("Please enter BOTH a topic and a style (adjective).")
    else:
        st.write("### Generated Blog Titles")
        result = lh.generate_blog_titles(topic, adjective)
        st.write(result)
