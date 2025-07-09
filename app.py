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
    ("👩‍🚒", 3, 1.6, 5.5),   # Rettungssanitäter
    ("🩹", 3, 1.2, 4.2),      # Verband
    ("📟", 2, 1.1, 3.8),      # Pager
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
    "win": 0,
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

def spin_slots():
    st.session_state.reels = [random.choice(weighted_reel) for _ in range(REELS)]

# Styling mit Farbverläufen, Schatten, Glow & Animationen
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
    /* Glitzer-Glow für Gewinn-Symbole */
    .glow {
        text-shadow:
            0 0 5px #ff1744,
            0 0 10px #ff1744,
            0 0 20px #ff1744,
            0 0 30px #ff1744,
            0 0 40px #f50057;
        animation: flicker 1.5s infinite alternate;
    }
    @keyframes flicker {
        0% { text-shadow: 0 0 5px #ff1744, 0 0 10px #ff1744, 0 0 20px #ff1744, 0 0 30px #ff1744, 0 0 40px #f50057; }
        100% { text-shadow: 0 0 10px #ff1744, 0 0 20px #ff1744, 0 0 30px #ff1744, 0 0 40px #f50057, 0 0 50px #ff1744; }
    }
    /* Animierte Münzen */
    @keyframes coin-fall {
        0% {transform: translateY(-100px) rotate(0deg); opacity: 1;}
        100% {transform: translateY(200px) rotate(360deg); opacity: 0;}
    }
    .coin {
        font-size: 2em;
        position: fixed;
        top: 0;
        animation: coin-fall 2s ease-in forwards;
        pointer-events: none;
        z-index: 9999;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🚑 Rettungsdienst Slotmaschine 🚑</div>', unsafe_allow_html=True)
st.markdown(f'<div class="coins">💰 Coins: {st.session_state.coins}</div>', unsafe_allow_html=True)

bet = st.slider("Wähle deinen Einsatz (Coins):", min_value=10, max_value=min(200, st.session_state.coins), step=10)

spin_box = st.empty()

def render_reels(reels, glow=False):
    if glow:
        html_reels = " ".join([f'<span class="glow">{r}</span>' for r in reels])
    else:
        html_reels = " ".join(reels)
    spin_box.markdown(f"<div style='font-size:5em; text-align:center;'>{html_reels}</div>", unsafe_allow_html=True)

def show_coins_animation():
    for i in range(10):
        x = random.randint(10, 90)
        delay = i * 0.2
        st.markdown(f"""
            <div class="coin" style="left:{x}vw; animation-delay:{delay}s;">💰</div>
        """, unsafe_allow_html=True)

if st.button("🎰 Drehen!"):
    if bet > st.session_state.coins:
        st.warning("⚠️ Du hast nicht genug Coins für diesen Einsatz!")
    else:
        st.session_state.coins -= bet
        # Dreh-Animation
        for _ in range(10):
            random_reels = [random.choice(weighted_reel) for _ in range(REELS)]
            render_reels(random_reels)
            time.sleep(0.1)
        spin_slots()
        win, msg = calculate_win(bet)
        st.session_state.win = win
        st.session_state.message = msg
        render_reels(st.session_state.reels, glow=(win > 0))
        if win > 0:
            st.session_state.coins += win
            # Konfetti-GIF
            st.markdown(
                """
                <div style="text-align:center; margin-top: -20px;">
                    <img src="https://i.gifer.com/origin/3d/3d7a01674fef37120f47866a51248f1e.gif" width="200" />
                </div>
                """,
                unsafe_allow_html=True
            )
            # Münzanimation
            show_coins_animation()
else:
    render_reels(st.session_state.reels)

st.markdown(f'<div class="message">{st.session_state.message}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("## Gewinnübersicht pro Symbol")
table_html = """
<table>
<thead>
<tr><th>Symbol</th><th>Gewinn bei 2 gleichen</th><th>Gewinn bei 3 gleichen</th></tr>
</thead>
<tbody>
"""
for sym, _, val2, val3 in SYMBOLS:
    table_html += f"<tr><td style='font-size:1.8em;'>{sym}</td><td>{val2}× Einsatz</td><td>{val3}× Einsatz</td></tr>"
table_html += "</tbody></table>"

st.markdown(table_html, unsafe_allow_html=True)
