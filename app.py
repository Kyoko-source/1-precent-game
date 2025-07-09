import streamlit as st
from datetime import datetime
import random
import time

# Symbole mit Gewicht und Gewinnfaktoren
SYMBOLS = [
    ("❤️", 10, 1.2, 4.5),
    ("🚑", 6, 2.0, 6.0),
    ("⛑️", 4, 1.5, 5.0),
    ("💉", 3, 1.3, 4.0),
    ("🩺", 2, 1.1, 3.5),
]

REELS = 3

weighted_reel = []
for symbol, weight, _, _ in SYMBOLS:
    weighted_reel.extend([symbol]*weight)

defaults = {
    "coins": 1000,
    "last_claim": datetime(2000,1,1).date(),
    "reels": ["❓"]*REELS,
    "message": "",
}

for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

today = datetime.today().date()
if st.session_state.last_claim != today:
    st.session_state.coins += 500
    st.session_state.last_claim = today
    st.success("🎁 Täglicher Rettungsdienst-Bonus: +500 Coins")

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
    return win, message

def spin_animation(spin_box):
    # Simuliere Walzen-Drehung: 10 schnelle Updates mit zufälligen Symbolen
    for _ in range(10):
        random_reels = [random.choice(weighted_reel) for _ in range(REELS)]
        spin_box.markdown(f"<div style='font-size:5em; text-align:center;'>{' '.join(random_reels)}</div>", unsafe_allow_html=True)
        time.sleep(0.1)

def spin_slots():
    st.session_state.reels = [random.choice(weighted_reel) for _ in range(REELS)]

# Styling mit Farbverläufen, Schatten und schöner Schrift
st.markdown("""
<style>
    .title {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 3.5em;
        font-weight: 900;
        color: #b71c1c;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 2px 2px 5px #7f0000;
    }
    .coins {
        font-size: 1.6em;
        font-weight: bold;
        color: #d32f2f;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 1px 1px 3px #9e0000;
    }
    .button-container {
        display: flex;
        justify-content: center;
        margin-bottom: 30px;
    }
    .message {
        font-size: 1.3em;
        font-weight: 700;
        color: #b71c1c;
        text-align: center;
        margin-top: 20px;
        min-height: 2em;
        text-shadow: 1px 1px 2px #7f0000;
    }
    table {
        margin-left: auto;
        margin-right: auto;
        border-collapse: collapse;
        width: 75%;
        font-family: Arial, sans-serif;
        box-shadow: 0 4px 8px rgba(183, 28, 28, 0.5);
        border-radius: 8px;
        overflow: hidden;
    }
    th, td {
        border: 1px solid #b71c1c;
        padding: 12px 18px;
        text-align: center;
        background: linear-gradient(90deg, #ffebee, #ffcdd2);
    }
    th {
        background-color: #b71c1c;
        color: white;
        font-size: 1.1em;
    }
    tr:nth-child(even) td {
        background: linear-gradient(90deg, #ffcdd2, #ffebee);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🚑 Rettungsdienst Slotmaschine 🚑</div>', unsafe_allow_html=True)
st.markdown(f'<div class="coins">💰 Coins: {st.session_state.coins}</div>', unsafe_allow_html=True)

bet = st.slider("Wähle deinen Einsatz (Coins):", min_value=10, max_value=min(200, st.session_state.coins), step=10)

spin_box = st.empty()

if st.button("🎰 Drehen!"):
    if bet > st.session_state.coins:
        st.warning("⚠️ Du hast nicht genug Coins für diesen Einsatz!")
    else:
        st.session_state.coins -= bet
        spin_animation(spin_box)
        spin_slots()
        spin_box.markdown(f"<div style='font-size:5em; text-align:center;'>{' '.join(st.session_state.reels)}</div>", unsafe_allow_html=True)
        win, msg = calculate_win(bet)
        st.session_state.coins += win
        st.session_state.message = msg

else:
    spin_box.markdown(f"<div style='font-size:5em; text-align:center;'>{' '.join(st.session_state.reels)}</div>", unsafe_allow_html=True)

st.markdown(f'<div class="message">{st.session_state.message}</div>', unsafe_allow_html=True)

# Gewinnübersicht
st.markdown("---")
st.markdown("## Gewinnübersicht pro Symbol")
table_html = """
<table>
<thead>
<tr><th>Symbol</th><th>Gewinn bei 2 gleichen</th><th>Gewinn bei 3 gleichen</th></tr>
</thead><tbody>
"""
for sym, weight, val2, val3 in SYMBOLS:
    table_html += f"<tr><td style='font-size:2em'>{sym}</td><td>{val2}x Einsatz</td><td>{val3}x Einsatz</td></tr>"

table_html += "</tbody></table>"
st.markdown(table_html, unsafe_allow_html=True)

