import streamlit as st
from datetime import datetime, timedelta
import random
import time

# Symbole mit Gewicht und höheren Gewinnfaktoren (Seltenheit bleibt gleich)
SYMBOLS = [
    ("❤️", 10, 1.8, 7.0),
    ("🚑", 8, 2.8, 9.0),
    ("⛑️", 7, 2.4, 8.0),
    ("💉", 6, 2.0, 7.0),
    ("🩺", 5, 1.6, 6.0),
    ("🚨", 4, 2.2, 8.5),
    ("👩‍🚒", 3, 2.8, 10.0),
    ("🩹", 3, 2.0, 8.0),
    ("📟", 2, 1.6, 7.5),
]

REELS = 3

# Gewichtete Symbolauswahl für die Walzen
weighted_reel = []
for symbol, weight, _, _ in SYMBOLS:
    weighted_reel.extend([symbol] * weight)

# Session-Zustand
defaults = {
    "coins": 1000,
    "last_claim": datetime(2000, 1, 1),
    "reels": ["❓"] * REELS,
    "message": "",
    "win": 0,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Zeitberechnung für Bonus
now = datetime.now()
claim_ready = now.date() > st.session_state.last_claim.date()

if claim_ready:
    st.session_state.coins += 500
    st.session_state.last_claim = now
    st.success("🎁 Täglicher Rettungsdienst-Bonus: +500 Coins")

# ⏳ Countdown anzeigen
else:
    next_claim = datetime.combine(st.session_state.last_claim.date() + timedelta(days=1), datetime.min.time())
    remaining = next_claim - now
    hours, remainder = divmod(int(remaining.total_seconds()), 3600)
    minutes = remainder // 60
    st.info(f"⏳ Nächster Bonus in {hours}h {minutes}min")

# Hilfsfunktion
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

# Styling
st.markdown("""
<style>
    .title {
        font-size: 3.2em;
        font-weight: 900;
        text-align: center;
        color: #b71c1c;
        text-shadow: 2px 2px 5px #7f0000;
    }
    .coins {
        font-size: 1.5em;
        text-align: center;
        color: #d32f2f;
        margin-bottom: 20px;
    }
    .message {
        font-size: 1.5em;
        text-align: center;
        color: #b71c1c;
        min-height: 2.5em;
    }
    .coin {
        font-size: 2em;
        position: fixed;
        top: 0;
        animation: coin-fall 2s ease-in forwards;
        pointer-events: none;
        z-index: 9999;
    }
    @keyframes coin-fall {
        0% {transform: translateY(-100px) rotate(0deg); opacity: 1;}
        100% {transform: translateY(200px) rotate(360deg); opacity: 0;}
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🚑 Rettungsdienst Slotmaschine 🚑</div>', unsafe_allow_html=True)
st.markdown(f'<div class="coins">💰 Coins: {st.session_state.coins}</div>', unsafe_allow_html=True)

# Einsatz wählen
bet = st.slider("Wähle deinen Einsatz (Coins):", min_value=10, max_value=min(200, st.session_state.coins), step=10)

spin_box = st.empty()

def render_reels(reels, highlight=False):
    html = " ".join([f"<span style='font-size:5em;'>{r}</span>" for r in reels])
    spin_box.markdown(f"<div style='text-align:center;'>{html}</div>", unsafe_allow_html=True)

def show_coin_animation():
    for i in range(10):
        x = random.randint(10, 90)
        delay = i * 0.2
        st.markdown(f"""
            <div class="coin" style="left:{x}vw; animation-delay:{delay}s;">💰</div>
        """, unsafe_allow_html=True)

# Drehen
if st.button("🎰 Drehen!"):
    if bet > st.session_state.coins:
        st.warning("⚠️ Nicht genug Coins!")
    else:
        st.session_state.coins -= bet
        for _ in range(10):
            tmp = [random.choice(weighted_reel) for _ in range(REELS)]
            render_reels(tmp)
            time.sleep(0.1)
        spin_slots()
        win, msg = calculate_win(bet)
        st.session_state.win = win
        st.session_state.message = msg
        render_reels(st.session_state.reels, highlight=(win > 0))
        st.markdown(f'<div class="message">{st.session_state.message}</div>', unsafe_allow_html=True)
        if win > 0:
            st.session_state.coins += win
            st.markdown('<div style="text-align:center;"><img src="https://i.gifer.com/origin/3d/3d7a01674fef37120f47866a51248f1e.gif" width="200" /></div>', unsafe_allow_html=True)
            show_coin_animation()
else:
    render_reels(st.session_state.reels)
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
for sym, _, val2, val3 in SYMBOLS:
    table_html += f"<tr><td style='font-size:1.8em;'>{sym}</td><td>{val2}× Einsatz</td><td>{val3}× Einsatz</td></tr>"
table_html += "</tbody></table>"

st.markdown(table_html, unsafe_allow_html=True)
