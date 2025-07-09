import streamlit as st
from datetime import datetime
import random

# Symbole mit Gewicht (für Wahrscheinlichkeiten) und Gewinnfaktoren
# Format: symbol, gewicht, gewinnfaktor bei 2 gleichen, bei 3 gleichen
SYMBOLS = [
    ("❤️", 10, 1.2, 4.5),   # häufig, kleiner Gewinn
    ("🚑", 6, 2.0, 6.0),    # Krankenwagen, hoher Gewinn
    ("⛑️", 4, 1.5, 5.0),    # Helm, mittlerer Gewinn
    ("💉", 3, 1.3, 4.0),    # Spritze
    ("🩺", 2, 1.1, 3.5),    # Stethoskop, selten und kleinster Gewinn
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

def spin_slots():
    st.session_state.reels = [random.choice(weighted_reel) for _ in range(REELS)]

def get_symbol_info(sym):
    for s, w, val2, val3 in SYMBOLS:
        if s == sym:
            return val2, val3
    return 1.0, 5.0  # Default (sollte nicht vorkommen)

def calculate_win(bet):
    reels = st.session_state.reels
    unique = set(reels)
    if len(unique) == 1:
        val2, val3 = get_symbol_info(reels[0])
        win = int(bet * val3)
        message = f"🎉 Jackpot! 3x {reels[0]}! Du gewinnst {win} Coins!"
    elif len(unique) == 2:
        # Finde welches Symbol doppelt ist
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

st.markdown(
    """
    <style>
    .title {
        color: #b71c1c;
        font-weight: bold;
        font-size: 3em;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-bottom: 20px;
    }
    .coins {
        font-size: 1.5em;
        color: #d32f2f;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
    }
    .slots {
        font-size: 5em;
        text-align: center;
        margin: 30px 0;
    }
    .message {
        font-size: 1.2em;
        text-align: center;
        margin-top: 20px;
        font-weight: 600;
        color: #b71c1c;
    }
    table {
        margin-left: auto;
        margin-right: auto;
        border-collapse: collapse;
        width: 75%;
        font-family: Arial, sans-serif;
    }
    th, td {
        border: 1px solid #b71c1c;
        padding: 8px 12px;
        text-align: center;
    }
    th {
        background-color: #f44336;
        color: white;
    }
    tr:nth-child(even) {
        background-color: #ffe6e6;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown('<div class="title">🚑 Rettungsdienst Slotmaschine 🚑</div>', unsafe_allow_html=True)
st.markdown(f'<div class="coins">💰 Coins: {st.session_state.coins}</div>', unsafe_allow_html=True)

bet = st.slider("Wähle deinen Einsatz (Coins):", min_value=10, max_value=min(200, st.session_state.coins), step=10)

if st.button("🎰 Drehen!"):
    if bet > st.session_state.coins:
        st.warning("⚠️ Du hast nicht genug Coins für diesen Einsatz!")
    else:
        st.session_state.coins -= bet
        spin_slots()
        win, msg = calculate_win(bet)
        st.session_state.coins += win
        st.session_state.message = msg

st.markdown(f'<div class="slots">{" ".join(st.session_state.reels)}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="message">{st.session_state.message}</div>', unsafe_allow_html=True)

# Gewinnübersicht Tabelle mit Symbolen und ihren Werten
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

