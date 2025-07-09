import streamlit as st
from datetime import datetime, timedelta
import random
import time

# Symbole: (Symbol, Gewichtung, Gewinn bei 2x, Gewinn bei 3x)
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
JACKPOT_START = 1000

# Reels bauen
weighted_reel = []
for symbol, weight, _, _ in SYMBOLS:
    weighted_reel.extend([symbol] * weight)

# Init Session
defaults = {
    "coins": 1000,
    "last_claim": datetime(2000, 1, 1),
    "reels": ["❓"] * REELS,
    "message": "",
    "win": 0,
    "jackpot": JACKPOT_START,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Bonus
now = datetime.now()
claim_ready = now.date() > st.session_state.last_claim.date()
if claim_ready:
    st.session_state.coins += 500
    st.session_state.last_claim = now
    st.success("🎁 Täglicher Bonus: +500 Coins")
else:
    next_claim = datetime.combine(st.session_state.last_claim.date() + timedelta(days=1), datetime.min.time())
    remaining = next_claim - now
    hours, remainder = divmod(int(remaining.total_seconds()), 3600)
    minutes = remainder // 60
    st.info(f"⏳ Nächster Bonus in {hours}h {minutes}min")

# Gewinnberechnung
def get_symbol_info(sym):
    for s, _, val2, val3 in SYMBOLS:
        if s == sym:
            return val2, val3
    return 1.0, 5.0

def calculate_win(bet):
    reels = st.session_state.reels
    unique = set(reels)
    if len(unique) == 1:
        val2, val3 = get_symbol_info(reels[0])
        base_win = int(bet * val3)
        jackpot = st.session_state.jackpot
        total_win = base_win + jackpot
        st.session_state.jackpot = JACKPOT_START
        message = f"🎉 JACKPOT! 3x {reels[0]}! Du gewinnst {base_win} + 🔥 {jackpot} = {total_win} Coins!"
        return total_win, message
    elif len(unique) == 2:
        for sym in unique:
            if reels.count(sym) == 2:
                val2, _ = get_symbol_info(sym)
                win = int(bet * val2)
                message = f"👍 Zwei gleiche {sym}! Du gewinnst {win} Coins!"
                return win, message
    # Bei Verlust wächst der Jackpot
    st.session_state.jackpot += int(bet * 0.1)
    return 0, "😞 Kein Gewinn – der Jackpot wächst weiter!"

def spin_slots():
    st.session_state.reels = [random.choice(weighted_reel) for _ in range(REELS)]

# Style
st.markdown("""
<style>
    .title {
        font-size: 3em;
        font-weight: 900;
        text-align: center;
        color: #b71c1c;
        text-shadow: 2px 2px 5px #7f0000;
    }
    .coins, .jackpot {
        font-size: 1.6em;
        text-align: center;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .coins { color: #d32f2f; }
    .jackpot { color: orange; text-shadow: 1px 1px 5px red; }
    .message {
        font-size: 1.4em;
        text-align: center;
        color: #b71c1c;
        min-height: 2em;
    }
</style>
""", unsafe_allow_html=True)

# Anzeige
st.markdown('<div class="title">🚑 Rettungsdienst Slotmaschine 🚑</div>', unsafe_allow_html=True)
st.markdown(f'<div class="coins">💰 Coins: {st.session_state.coins}</div>', unsafe_allow_html=True)

# Jackpot Visual
jackpot_value = st.session_state.jackpot
flames = "🔥" * (jackpot_value // 25)
st.markdown(f'<div class="jackpot">{flames}<br>Jackpot: {jackpot_value} Coins</div>', unsafe_allow_html=True)

# Einsatz
bet = st.slider("Einsatz wählen:", min_value=10, max_value=min(200, st.session_state.coins), step=10)
spin_box = st.empty()

def render_reels(reels):
    html = " ".join([f"<span style='font-size:5em;'>{r}</span>" for r in reels])
    spin_box.markdown(f"<div style='text-align:center;'>{html}</div>", unsafe_allow_html=True)

def show_coin_animation():
    for i in range(10):
        x = random.randint(10, 90)
        delay = i * 0.15
        st.markdown(f"""
            <div class="coin" style="left:{x}vw; animation-delay:{delay}s;">💰</div>
        """, unsafe_allow_html=True)

# Button
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
        st.session_state.coins += win
        render_reels(st.session_state.reels)
        st.markdown(f'<div class="message">{msg}</div>', unsafe_allow_html=True)
        if win > 0:
            show_coin_animation()
else:
    render_reels(st.session_state.reels)
    st.markdown(f'<div class="message">{st.session_state.message}</div>', unsafe_allow_html=True)

# Tabelle
st.markdown("---")
st.markdown("## Gewinnübersicht")
table_html = """
<table>
<thead>
<tr><th>Symbol</th><th>Gewinn (2x)</th><th>Gewinn (3x)</th></tr>
</thead><tbody>
"""
for sym, _, val2, val3 in SYMBOLS:
    table_html += f"<tr><td style='font-size:1.5em;'>{sym}</td><td>{val2}×</td><td>{val3}×</td></tr>"
table_html += "</tbody></table>"
st.markdown(table_html, unsafe_allow_html=True)
