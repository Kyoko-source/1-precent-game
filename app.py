import streamlit as st
from datetime import datetime
import random

# Symbole der Slotmaschine passend zum Rettungsdienst-Thema
SYMBOLS = ["❤️", "🚑", "⛑️", "💉", "🩺"]
REELS = 3  # Anzahl der Walzen

# Session-State Defaults
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

# Slotmaschine Spin Funktion
def spin_slots():
    st.session_state.reels = [random.choice(SYMBOLS) for _ in range(REELS)]
    # Gewinn prüfen: Alle Symbole gleich?
    if len(set(st.session_state.reels)) == 1:
        st.session_state.coins += 500
        st.session_state.message = f"🎉 Jackpot! Du hast 500 Coins gewonnen! {st.session_state.reels[0]} {st.session_state.reels[1]} {st.session_state.reels[2]}"
    elif len(set(st.session_state.reels)) == 2:
        st.session_state.coins += 100
        st.session_state.message = f"👍 Zweierreihe! 100 Coins gewonnen! {' '.join(st.session_state.reels)}"
    else:
        st.session_state.message = f"😞 Kein Gewinn diesmal. Versuch's nochmal! {' '.join(st.session_state.reels)}"

# Streamlit UI

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
        # Gewinne basieren auf Einsatz
        if len(set(st.session_state.reels)) == 1:
            st.session_state.coins += bet * 10
            st.session_state.message += f" Jackpot Gewinn: {bet * 10} Coins!"
        elif len(set(st.session_state.reels)) == 2:
            st.session_state.coins += bet * 3
            st.session_state.message += f" Zweier Gewinn: {bet * 3} Coins!"

st.markdown(f'<div class="slots">{" ".join(st.session_state.reels)}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="message">{st.session_state.message}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("👩‍⚕️ Viel Glück und bleib im Dienst fit! 🚑")

