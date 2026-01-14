import streamlit as st
import time

# -----------------------
# Page
# -----------------------
st.set_page_config(page_title="Focusmato", page_icon="🍅")

st.markdown("""
<style>
div[data-testid="stStatusWidget"] { display: none; }
</style>
""", unsafe_allow_html=True)

# -----------------------
# Defaults
# -----------------------
if "work_minutes" not in st.session_state:
    st.session_state.work_minutes = 25
if "break_minutes" not in st.session_state:
    st.session_state.break_minutes = 5
if "screen_refresh" not in st.session_state:
    st.session_state.screen_refresh = 1
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

if "state" not in st.session_state:
    st.session_state.state = "ready"   # ready / running / paused
if "mode" not in st.session_state:
    st.session_state.mode = "work"    # work / break
if "end_time" not in st.session_state:
    st.session_state.end_time = None
if "session_duration" not in st.session_state:
    st.session_state.session_duration = st.session_state.work_minutes * 60
if "seconds_left" not in st.session_state:
    st.session_state.seconds_left = st.session_state.work_minutes * 60

# -----------------------
# Theme
# -----------------------
def apply_theme(theme):
    if theme == "Dark":
        st.markdown("""
        <style>
        .stApp { background-color:#0E1117; color:#FAFAFA; }
        .stButton>button { background:#262730; color:#FAFAFA; border:1px solid #444; }
        </style>
        """, unsafe_allow_html=True)

    elif theme == "Red":
        st.markdown("""
        <style>
        .stApp { background:#1a0f0f; color:#ffecec; }
        h1,h2,h3 { color:#ff4b4b; }
        .stButton>button { background:#ff4b4b; color:white; border:none; }
        .stProgress > div > div > div { background:#ff4b4b; }
        </style>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <style>
        .stApp { background:white; color:black; }
        .stButton>button { background:#f0f2f6; color:black; border:1px solid #ccc; }
        </style>
        """, unsafe_allow_html=True)

# -----------------------
# Helpers
# -----------------------
def start_timer():
    st.session_state.state = "running"
    st.session_state.session_duration = (
        st.session_state.work_minutes * 60
        if st.session_state.mode == "work"
        else st.session_state.break_minutes * 60
    )
    st.session_state.seconds_left = st.session_state.session_duration
    st.session_state.end_time = time.time() + st.session_state.seconds_left

def pause_timer():
    st.session_state.state = "paused"
    st.session_state.seconds_left = max(
        int(st.session_state.end_time - time.time()), 0
    )

def resume_timer():
    st.session_state.state = "running"
    st.session_state.end_time = time.time() + st.session_state.seconds_left

def next_timer():
    st.session_state.mode = "break" if st.session_state.mode == "work" else "work"
    start_timer()

def reset_timer():
    st.session_state.state = "ready"
    st.session_state.mode = "work"
    st.session_state.session_duration = st.session_state.work_minutes * 60
    st.session_state.seconds_left = st.session_state.session_duration
    st.session_state.end_time = None

# -----------------------
# Header
# -----------------------
col1, col2 = st.columns([6,1])
with col1:
    st.header("🍅 Focusmato")

with col2:
    st.space("small")
    with st.popover("⚙️", type="tertiary"):
        st.header("Timers")
        st.session_state.work_minutes = st.number_input(
            "Pomodoro (min)", 1, 90, st.session_state.work_minutes
        )
        st.session_state.break_minutes = st.number_input(
            "Break (min)", 1, 90, st.session_state.break_minutes
        )

        st.header("Theme")
        st.session_state.theme = st.selectbox(
            "Color mode",
            ["Light", "Dark", "Red"],
            index=["Light","Dark","Red"].index(st.session_state.theme)
        )

        st.session_state.screen_refresh = st.selectbox(
            "Refresh interval (sec)",
            [1,5,10,30,60],
            index=[1,5,10,30,60].index(st.session_state.screen_refresh)
        )

apply_theme(st.session_state.theme)
st.divider()

# -----------------------
# Tick
# -----------------------
if st.session_state.state == "running":
    st.session_state.seconds_left = max(
        int(st.session_state.end_time - time.time()), 0
    )

    if st.session_state.seconds_left == 0:  
        next_timer()
        st.rerun()

if st.session_state.state == "ready":
    st.session_state.session_duration = st.session_state.work_minutes * 60
    st.session_state.seconds_left = st.session_state.session_duration

# -----------------------
# Display
# -----------------------
label = "Focus time!" if st.session_state.mode == "work" else "Break time!"
m, s = divmod(st.session_state.seconds_left, 60)

st.title(label, text_alignment="center")
st.markdown(
    f"<h1 style='text-align:center; font-size:120px;'>{m:02d}:{s:02d}</h1>",
    unsafe_allow_html=True
)

progress = (
    (st.session_state.session_duration - st.session_state.seconds_left)
    / st.session_state.session_duration
)
st.progress(min(max(progress,0),1))

# -----------------------
# Buttons
# -----------------------
if st.session_state.state == "ready":
    if st.button("▶ Start", use_container_width=True):
        start_timer()
        st.rerun()

elif st.session_state.state == "running":
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("⏸ Pause", use_container_width=True):
            pause_timer()
            st.rerun()
    with c2:
        if st.button("⏭ Next", use_container_width=True):
            next_timer()
            st.rerun()
    with c3:
        if st.button("♻︎ Reset", use_container_width=True):
            reset_timer()
            st.rerun()

elif st.session_state.state == "paused":
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("▶ Resume", use_container_width=True):
            resume_timer()
            st.rerun()
    with c2:
        if st.button("⏭ Next", use_container_width=True):
            next_timer()
            st.rerun()
    with c3:
        if st.button("♻︎ Reset", use_container_width=True):
            reset_timer()
            st.rerun()

# -----------------------
# Auto refresh
# -----------------------
if st.session_state.state == "running":
    time.sleep(st.session_state.screen_refresh)
    st.rerun()