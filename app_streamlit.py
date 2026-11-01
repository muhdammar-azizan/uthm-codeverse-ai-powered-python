"""Web version of the AI Study Assistant, built with Streamlit.

Run from the repo root:  streamlit run app_streamlit.py
"""

import streamlit as st
from groq import APIConnectionError, APIStatusError, RateLimitError

from groq_client import chat, get_client
from study_assistant import SECTIONS, build_messages, split_card

st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="centered")


@st.cache_resource
def load_client():
    return get_client()


def code_from_block(text: str) -> str:
    """Strip the ``` fences the model puts around the example, if any."""
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("```")]
    return "\n".join(lines).strip()


def show_card(card: str) -> None:
    parts = split_card(card)
    if not all(name in parts for name in SECTIONS):
        st.markdown(card)  # layout was unexpected, so just show the text
        return
    for name in SECTIONS:
        st.subheader(name.title())
        if name == "EXAMPLE":
            st.code(code_from_block(parts[name]), language="python")
        else:
            st.markdown(parts[name])


st.title("📚 AI Study Assistant")
st.caption("Type a tech topic and get a beginner-friendly study card.")

client = load_client()
if client is None:
    st.error(
        "No API key found. Copy `.env.example` to `.env`, put your key after "
        "`GROQ_API_KEY=`, then restart the app. "
        "You can get a free key at https://console.groq.com."
    )
    st.stop()

with st.form("topic_form"):
    topic = st.text_input("Topic", placeholder="e.g. recursion, REST API, list vs dictionary")
    submitted = st.form_submit_button("Make study card")

if submitted:
    topic = topic.strip()
    if not topic:
        st.warning("Please type a topic first.")
    else:
        try:
            with st.spinner("Writing your study card..."):
                card = chat(client, build_messages(topic))
            show_card(card)
        except RateLimitError:
            st.error("Rate limit reached (HTTP 429). Wait a few seconds and try again.")
        except APIConnectionError:
            st.error("Could not reach Groq. Check your internet connection and try again.")
        except APIStatusError as e:
            if e.status_code == 401:
                st.error("Groq rejected the API key. Check GROQ_API_KEY in your .env file.")
            else:
                st.error(f"Groq returned an error (HTTP {e.status_code}). Try again later.")
        except ValueError as e:
            st.error(str(e))

st.divider()
st.caption("AI can be wrong. Check anything you plan to rely on.")
