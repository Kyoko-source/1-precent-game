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

# Styling mit Hintergrundbild, Overlays, schöner Typografie und Animationen
st.markdown("""
<style>
    /* Hintergrundbild mit Fixierung und leichtem Overlay */
    body {
        background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1470&q=80');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #fff;
    }

    /* Halbdurchsichtiger Container für alles */
    .main-container {
        background: rgba(39, 39, 39, 0.8);
        max-width: 720px;
        margin: 40px auto 60px auto;
        padding: 25px 40px 40px 40px;
        border-radius: 15px;
        box-shadow: 0 0 20px 5px rgba(183, 28, 28, 0.7);
    }

    /* Titel mit Farbverlauf und Schatten */
    .title {
        font-size: 3.5em;
        font-weight: 900;
        background: linear-gradient(45deg, #ff1744, #ff7961);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 15px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.6);
        user-select: none;
    }

    /* Coins Anzeige */
    .coins {
        font-size: 1.8em;
        font-weight: 700;
        color: #ff5252;
        text-align: center;
        margin-bottom: 30px;
        text-shadow: 0 1px 5px rgba(0,0,0,0.5);
        user-select: none;
    }

    /* Message */
    .message {
        font-size: 1.6em;
        font-weight: 700;
        color: #ff7961;
        text-align: center;
        margin-top: 10px;
        min-height: 2.5em;
        text-shadow: 0 0 5px #ff5252;
        line-height: 1.2;
        user-select: none;
    }

    /* Reels Darstellung */
    .reels {
        font-size: 6em;
        text-align: center;
        letter-spacing: 15px;
        user-select: none;
        margin-bottom: 10px;
        text-shadow: 0 0 15px #ff1744, 0 0 30px #ff7961;
    }

    /* Glow Effekt für Gewinnsymbole */
    .glow {
        animation: flicker 1.5s infinite alternate;
        text-shadow:
            0 0 8px #ff1744,
            0 0 18px #ff1744,
            0 0 28px #ff1744,
            0 0 38px #ff7961,
            0 0 48px #ff7961;
    }
    @keyframes flicker {
        0% { text-shadow: 0 0 8px #ff1744, 0 0 18px #ff1744, 0 0 28px #ff1744, 0 0 38px #ff7961, 0 0 48px #ff7961; }
        100% { text-shadow: 0 0 12px #ff1744, 0 0 22px #ff1744, 0 0 32px #ff1744, 0 0 42px #ff7961, 0 0 52px #ff7961; }
    }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(45deg, #ff1744, #ff7961);
        border: none;
        padding: 12px 25px;
        border-radius: 12px;
        font-size: 1.3em;
        font-weight: 700;
        color: white;
        box-shadow: 0 0 15px #ff1744;
        cursor: pointer;
        transition: background 0.3s ease, box-shadow 0.3s ease;
        user-select: none;
        width: 100%;
    }
    div.stButton > button:hover {
        background: linear-gradient(45deg, #ff7961, #ff1744);
        box-shadow: 0 0 25px #ff5252;
    }

    /* Slider Styling */
    .stSlider > div {
        color: #ffbaba;
        font-weight: 700;
    }

    /* Tabelle Gewinnübersicht */
    table {
        margin-left: auto;
        margin-right: auto;
        border-collapse: collapse;
        width: 100%;
        font-family: Arial, sans-serif;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 0 25px rgba(255, 23, 68, 0.7);
        background: rgba(255, 255, 255, 0.1);
        color: #fff;
        user-select: none;
    }
    th, td {
        border: 1px solid #ff1744;
        padding: 12px 18px;
        text-align: center;
    }
    th {
        background: linear-gradient(90deg, #ff1744, #ff7961);
        color: white;
        font-size: 1.1em;
    }
    tr:nth-child(even) {
        background: rgba(255, 255, 255, 0.15);
    }
    tr:hover {
        background: rgba(255, 23, 68, 0.25);
        transition: background 0.3s ease;
    }

    /* Münzanimation */
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

st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="title">🚑 Rettungsdienst Slotmaschine 🚑</div>', unsafe_allow_html=True)
st.markdown(f'<div class="coins">💰 Coins: {st.session_state.coins}</div>', unsafe_allow_html=True)

bet = st.slider("Wähle deinen Einsatz (Coins):", min_value=10, max_value=min(200, st.session_state.coins), step=10)

spin_box = st.empty()

def render_reels(reels, glow=False):
    if glow:
        html_reels = " ".join([f'<span class="glow">{r}</span>' for r in reels])
    else:
        html_reels = " ".join(reels)
    spin_box.markdown(f"<div class='reels'>{html_reels}</div>", unsafe_allow_html=True)

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
        st.markdown(f'<div class="message">{st.session_state.message}</div>', unsafe_allow_html=True)
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
st.markdown('</div>', unsafe_allow_html=True)
