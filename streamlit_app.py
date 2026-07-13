import os

import streamlit as st
from openai import OpenAI


st.set_page_config(
    page_title="Translator 9000",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


LANGUAGES = {
    "Spanish": "🇪🇸",
    "English": "🇺🇸",
    "Mandarin": "🇨🇳",
    "French": "🇫🇷",
    "Japanese": "🇯🇵",
}


def language_label(language: str) -> str:
    return f"{LANGUAGES[language]}  {language}"


def get_api_key() -> str | None:
    """Read the key from the environment or Streamlit secrets when available."""
    if key := os.getenv("OPENAI_API_KEY"):
        return key
    try:
        return st.secrets["OPENAI_API_KEY"]
    except Exception:
        return None


def translate(text: str, source_language: str, target_language: str) -> str:
    """Send the translation request to OpenAI."""
    client = OpenAI(api_key=get_api_key())
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a language translator. A user will give you an input "
                    "language, an output language, and text to translate. Output only "
                    "the translated text; do not add explanations or quotation marks."
                ),
            },
            {
                "role": "user",
                "content": f"{source_language}->{target_language}, my message is: {text}",
            },
        ],
    )
    return response.choices[0].message.content.strip()


st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at 8% 5%, rgba(125, 78, 255, .27), transparent 27rem),
                radial-gradient(circle at 93% 12%, rgba(0, 203, 168, .20), transparent 30rem),
                #0b1020;
            color: #f6f7ff;
        }
        .block-container { max-width: 1120px; padding-top: 4.5rem; padding-bottom: 3rem; }
        .hero { text-align: center; margin: 0 auto 2.8rem; }
        .eyebrow { color: #7eead6; font-size: .76rem; font-weight: 800; letter-spacing: .17em; text-transform: uppercase; }
        .hero h1 { font-size: clamp(3rem, 7vw, 5.8rem); line-height: .94; letter-spacing: -.075em; margin: .45rem 0 .85rem; }
        .hero h1 span { background: linear-gradient(105deg, #a995ff, #78ecd5 54%, #f3b6ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero p { color: #aeb8d6; font-size: 1.12rem; margin: 0; }
        .panel { background: rgba(18, 26, 49, .72); border: 1px solid rgba(196, 202, 255, .14); border-radius: 24px; padding: 1.35rem; box-shadow: 0 22px 55px rgba(0, 0, 0, .22); backdrop-filter: blur(18px); }
        .panel-title { color: #c5cce5; font-size: .75rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; margin-bottom: .5rem; }
        div[data-testid="stSelectbox"] label, div[data-testid="stTextArea"] label { color: #dce2f7 !important; font-weight: 700 !important; }
        div[data-baseweb="select"] > div { background: #121a31 !important; border-color: #35436b !important; border-radius: 12px !important; }
        textarea { background: #121a31 !important; border-color: #35436b !important; border-radius: 14px !important; color: #f6f7ff !important; font-size: 1.05rem !important; }
        .stButton > button { width: 100%; border: 0; border-radius: 14px; padding: .78rem 1rem; font-size: 1.05rem; font-weight: 800; color: #091226; background: linear-gradient(100deg, #8d7cff, #70e7d0); transition: transform .2s ease, box-shadow .2s ease; }
        .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(112, 231, 208, .25); }
        .output { min-height: 180px; background: linear-gradient(145deg, rgba(124, 108, 255, .14), rgba(112, 231, 208, .08)); border: 1px solid rgba(126, 234, 214, .25); border-radius: 16px; padding: 1.15rem; white-space: pre-wrap; font-size: 1.1rem; line-height: 1.65; }
        .empty { color: #8994b3; font-style: italic; }
        .footer { text-align: center; color: #75809d; font-size: .85rem; margin-top: 2rem; }
        [data-testid="stHeader"] { background: transparent; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">✦ Precision language studio</div>
        <h1>Translator <span>9000</span></h1>
        <p>Say it beautifully, anywhere in the world.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "translation" not in st.session_state:
    st.session_state.translation = ""

with st.container(border=False):
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    language_col, swap_col, target_col = st.columns([5, 1, 5], vertical_alignment="bottom")
    with language_col:
        source = st.selectbox("I’m writing in", ["Spanish", "English"], format_func=language_label)
    with swap_col:
        st.markdown("<div style='text-align:center;font-size:1.5rem;padding-bottom:.25rem'>→</div>", unsafe_allow_html=True)
    with target_col:
        target = st.selectbox("Translate to", ["Mandarin", "French", "Japanese"], format_func=language_label)

    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
    text = st.text_area(
        "Your message",
        placeholder=f"Write something in {source}…",
        height=170,
        label_visibility="visible",
    )
    submitted = st.button("Translate ✦", type="primary")
    st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    if not text.strip():
        st.warning("Write a message first, then I’ll translate it.")
    elif not get_api_key():
        st.error("Add an `OPENAI_API_KEY` to your environment or `.streamlit/secrets.toml` to enable translation.")
    else:
        try:
            with st.spinner("Finding just the right words…"):
                st.session_state.translation = translate(text, source, target)
        except Exception as error:
            st.error(f"Translation couldn’t be completed: {error}")

st.markdown("<div style='height:1.4rem'></div>", unsafe_allow_html=True)
st.markdown('<div class="panel">', unsafe_allow_html=True)
st.markdown(f'<div class="panel-title">{language_label(target)} translation</div>', unsafe_allow_html=True)
if st.session_state.translation:
    st.text_area(
        "Translation result",
        value=st.session_state.translation,
        height=180,
        disabled=True,
        label_visibility="collapsed",
    )
else:
    st.markdown('<div class="output empty">Your translation will appear here.</div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown('<div class="footer">Built for curious conversations across every border.</div>', unsafe_allow_html=True)
