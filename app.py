import streamlit as st
from datetime import datetime
import random

# Symbole & deren Gewichtung (Wahrscheinlichkeiten) - seltenere Symbole = kleinerer Wert
SYMBOLS = [
    ("❤️", 10),   # häufig
    ("🚑", 6),
    ("⛑️", 4),
    ("💉", 3),
    ("🩺", 2)     # selten
]
REELS = 3

# Erstelle Reel-Liste entsprechend der Gewichte
weighted_reel = []
for symbol, weight in SYMBOLS:
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

# Täglicher Coin-Bonus
today = datetime.today().date()
if st.session_state.last_claim != today:
    st.session_state.coins += 500
    st.session_state.last_claim = today
    st.success("🎁 Täglicher Rettungsdienst-Bonus: +500 Coins")

def spin_slots():
    st.session_state.reels = [random.choice(weighted_reel) for _ in range(REELS)]

def calculate_win(bet):
    reels = st.session_state.reels
    unique = set(reels)
    if len(unique) == 1:
        # Jackpot: alle 3 gleich
        win = bet * 5
        message = f"🎉 Jackpot! 3x {reels[0]}! Du gewinnst {win} Coins!"
    elif len(unique) == 2:
        # Zweierreihe
        win = int(bet * 1.5)
        message = f"👍 Zwei gleiche! Du gewinnst {win} Coins!"
    else:
        win = 0
        message = "😞 Leider kein Gewinn, versuch's nochmal!"
    return win, message

# UI Styling
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
        width: 60%;
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

# Gewinnübersicht unten
st.markdown("---")
st.markdown("## Gewinnübersicht")
st.markdown("""
<table>
<thead><tr><th>Kombination</th><th>Gewinnfaktor</th><th>Beispiel bei 100 Coins Einsatz</th></tr></thead>
<tbody>
<tr><td>3 gleiche Symbole (Jackpot)</td><td>5x Einsatz</td><td>500 Coins</td></tr>
<tr><td>2 gleiche Symbole</td><td>1.5x Einsatz</td><td>150 Coins</td></tr>
<tr><td>keine gleichen</td><td>0x Einsatz</td><td>0 Coins</td></tr>
</tbody>
</table>
""", unsafe_allow_html=True)


