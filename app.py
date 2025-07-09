import streamlit as st
from datetime import datetime
import random
import time

# Symbole mit Gewicht und Gewinnfaktoren (Thema Rettungsdienst)
SYMBOLS = [
    ("❤️", 10, 1.2, 4.5),     # Herz
    ("🚑", 8, 2.0, 6.0),      # Krankenwagen
    ("⛑️", 7, 1.5, 5.0),      # Helm
    ("💉", 6, 1.3, 4.0),      # Spritze
    ("🩺", 5, 1.1, 3.5),      # Stethoskop
    ("🚨", 4, 1.4, 4.8),      # Blaulicht
    ("👩‍🚒", 3, 1.6, 5.5),    # Rettungssanitäter
    ("🩹", 3, 1.2, 4.2),      # Verband
    ("📟", 2, 1.1, 3.8),      # Pager
]

REELS = 3

weighted_reel = []
for symbol, weight, _, _ in SYMBOLS:
    weighted_reel.extend([symbol] * weight)

defaults = {
    "coins": 1000,
    "last_claim": datetime(2000, 1, 1).date(),
    "reels": ["❓"] * REELS,
    "message": "",
    "win": 0,
    "spinning": False,
    "bet": 10,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def get_symbol_info(sym):
    for s, w, val2, val3 in SYMBOLS:
        if s == sym:
            return val2, val3
    return 1.0, 5.0

def calculate_win(bet):
    reels = st.session_state.reels
    unique = set(reels)
    if len(unique) == 1:
        val2, val3 = get_symbol_info(reels[0])
        win = int(bet * val3)
        message = f"🎉 Jackpot! 3x {reels[0]}! Du gewinnst {win} Coins!"
    elif len(unique) == 2:
        for sym in unique:
            if reels.count(sym) == 2:
                val2, val3 = get_symbol_info(sym)
                win = int(bet * val2)
                message = f"👍 Zwei gleiche {sym}! Du gewinnst {win} Coins!"
                break
        else:
            win = 0
            message = "😞 Leider kein Gewinn, versuch's nochmal!"
    else:
        win = 0
        message = "😞 Leider kein Gewinn, versuch's nochmal!"
    return win, message

def spin_once():
    st.session_state.reels = [random.choice(weighted_reel) for _ in range(REELS)]

def render_reels(reels, glow=False):
    if glow:
        html_reels = " ".join([f'<span style="color:#b71c1c; font-weight:bold; font-size:5em; text-shadow: 0 0 10px #ff1744;">{r}</span>' for r in reels])
    else:
        html_reels = " ".join([f'<span style="font-size:5em;">{r}</span>' for r in reels])
    st.markdown(f"<div style='text-align:center;'>{html_reels}</div>", unsafe_allow_html=True)

# --- UI ---
st.markdown("""
<style>
    .coins {
        font-size: 1.6em;
        font-weight: bold;
        color: #d32f2f;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 1px 1px 3px #9e0000;
    }
    .message {
        font-size: 1.5em;
        font-weight: 700;
        color: #b71c1c;
        text-align: center;
        margin-top: 15px;
        min-height: 2.5em;
        text-shadow: 1px 1px 3px #7f0000;
        line-height: 1.2;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 style="text-align:center; color:#b71c1c;">🚑 Rettungsdienst Slotmaschine 🚑</h1>', unsafe_allow_html=True)
st.markdown(f'<div class="coins">💰 Coins: {st.session_state.coins}</div>', unsafe_allow_html=True)

bet = st.slider("Wähle deinen Einsatz (Coins):", min_value=10, max_value=min(200, st.session_state.coins), step=10)
st.session_state.bet = bet

col1, col2 = st.columns(2)
with col1:
    start_button = st.button("▶️ Start Drehen")
with col2:
    stop_button = st.button("⏹️ Stopp")

if start_button and not st.session_state.spinning:
    if st.session_state.coins >= bet:
        st.session_state.coins -= bet
        st.session_state.spinning = True
        st.session_state.message = ""
        st.session_state.win = 0
    else:
        st.warning("⚠️ Nicht genug Coins!")

if st.session_state.spinning:
    spin_once()
    render_reels(st.session_state.reels)
    st.markdown('<div style="text-align:center; font-style: italic;">🎰 Slot dreht... Drücke "Stopp" um anzuhalten.</div>', unsafe_allow_html=True)
    time.sleep(0.1)
    st.experimental_rerun()

if stop_button and st.session_state.spinning:
    st.session_state.spinning = False
    win, msg = calculate_win(bet)
    st.session_state.win = win
    st.session_state.message = msg
    st.session_state.coins += win
    render_reels(st.session_state.reels, glow=(win > 0))
    st.markdown(f'<div class="message">{msg}</div>', unsafe_allow_html=True)

if not st.session_state.spinning and not stop_button:
    render_reels(st.session_state.reels)
    if st.session_state.message:
        st.markdown(f'<div class="message">{st.session_state.message}</div>', unsafe_allow_html=True)
