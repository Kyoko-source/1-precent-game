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
    ("🧑‍⚕️", 3, 1.6, 5.5),   # Rettungssanitäter
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

# Styling mit Hintergrund, Slot-Frame, Buttons, Animationen & Sound
st.markdown("""
<style>
  body {
    background: url('https://images.unsplash.com/photo-1571204697852-e562d8aa5a5a?auto=format&fit=crop&w=1350&q=80') no-repeat center center fixed;
    background-size: cover;
  }
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
  .slot-frame {
    background: rgba(255, 255, 255, 0.85);
    max-width: 400px;
    margin: 0 auto 20px auto;
    padding: 20px 40px;
    border-radius: 25px;
    box-shadow: 0 8px 30px rgba(183, 28, 28, 0.7);
    text-align: center;
  }
  .reels {
    font-size: 5em;
    letter-spacing: 15px;
    margin-bottom: 15px;
  }
  .glow {
    text-shadow:
      0 0 5px #ff1744,
      0 0 10px #ff1744,
      0 0 20px #ff1744,
      0 0 30px #ff1744,
      0 0 40px #f50057;
    animation: flicker 1.5s infinite alternate;
    display: inline-block;
  }
  @keyframes flicker {
    0% { text-shadow: 0 0 5px #ff1744, 0 0 10px #ff1744, 0 0 20px #ff1744, 0 0 30px #ff1744, 0 0 40px #f50057; }
    100% { text-shadow: 0 0 10px #ff1744, 0 0 20px #ff1744, 0 0 30px #ff1744, 0 0 40px #f50057, 0 0 50px #ff1744; }
  }
  button {
    background-color: #b71c1c;
    color: white;
    font-size: 1.3em;
    padding: 12px 35px;
    border-radius: 15px;
    border: none;
    cursor: pointer;
    box-shadow: 0 6px #7f0000;
    transition: background-color 0.3s ease;
    margin: 10px auto;
    display: block;
  }
  button:hover {
    background-color: #f44336;
  }
  button:active {
    box-shadow: 0 2px #7f0000;
    transform: translateY(4px);
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
    margin-top: 30px;
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

# Audio-Elemente für Soundeffekte (Start und Gewinn)
st.markdown("""
<audio id="spin-sound" src="https://actions.google.com/sounds/v1/casino/slot_machine_spin.ogg"></audio>
<audio id="win-sound" src="https://actions.google.com/sounds/v1/casino/slot_machine_win.ogg"></audio>
<script>
function playSpin() {
  document.getElementById("spin-sound").play();
}
function playWin() {
  document.getElementById("win-sound").play();
}
</script>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🚑 Rettungsdienst Slotmaschine 🚑</div>', unsafe_allow_html=True)
st.markdown(f'<div class="coins">💰 Coins: {st.session_state.coins}</div>', unsafe_allow_html=True)

bet = st.slider("Wähle deinen Einsatz (Coins):", min_value=10, max_value=min(200, st.session_state.coins), step=10)

slot_container = st.empty()

def render_reels(reels, glow=False):
    if glow:
        html_reels = " ".join([f'<span class="glow">{r}</span>' for r in reels])
    else:
        html_reels = " ".join(reels)
    slot_container.markdown(f"<div class='slot-frame'><div class='reels'>{html_reels}</div></div>", unsafe_allow_html=True)

def spin_animation():
    import streamlit.components.v1 as components
    # JS für Sound & Animation
    components.html("""
    <script>
    playSpin();
    </script>
    """, height=0)

def win_animation():
    import streamlit.components.v1 as components
    components.html("""
    <script>
    playWin();
    </script>
    """, height=0)

if st.button("🎰 Drehen!"):
    if bet > st.session_state.coins:
        st.warning("⚠️ Du hast nicht genug Coins für diesen Einsatz!")
    else:
        st.session_state.coins -= bet
        # Dreh-Animation (ohne time.sleep, dafür mit schnellem Update)
        for _ in range(10):
            random_reels = [random.choice(weighted_reel) for _ in range(REELS)]
            render_reels(random_reels)
            spin_animation()
            time.sleep(0.07)  # kurzes Delay, flüssiger als vorher
        spin_slots()
        win, msg = calculate_win(bet)
        st.session_state.win = win
        st.session_state.message = msg
        render_reels(st.session_state.reels, glow=(win > 0))
        if win > 0:
            st.session_state.coins += win
            win_animation()
            # Konfetti-GIF
            st.markdown(
                """
                <div style="text-align:center; margin-top: -20px;">
                    <img src="https://i.gifer.com/origin/3d/3d7a01674fef37120f47866a51248f1e.gif" width="200" />
                </div>
                """,
                unsafe_allow_html=True
            )
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
