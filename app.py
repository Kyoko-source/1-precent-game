import streamlit as st
import random
from datetime import datetime

# --- Kartenwerte und Deck ---
CARD_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11
}
CARD_DECK = list(CARD_VALUES.keys()) * 4

# --- Hilfsfunktionen ---
def calculate_score(hand):
    score = sum(CARD_VALUES[card] for card in hand)
    aces = hand.count("A")
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

def draw_card():
    return random.choice(CARD_DECK)

def reset_game():
    st.session_state.deck = CARD_DECK[:]
    random.shuffle(st.session_state.deck)
    st.session_state.player = [draw_card(), draw_card()]
    st.session_state.dealer = [draw_card(), draw_card()]
    st.session_state.turn = "player"
    st.session_state.message = ""
    st.session_state.bet = 0

def give_daily_bonus():
    today = datetime.today().date()
    if st.session_state.last_claim != today:
        st.session_state.coins += 1000
        st.session_state.last_claim = today
        st.success("🎁 Täglicher Bonus: +1000 Coins")

# --- Initialisierung ---
if "coins" not in st.session_state:
    st.session_state.coins = 1000
    st.session_state.last_claim = datetime(2000,1,1).date()
    st.session_state.player = []
    st.session_state.dealer = []
    st.session_state.turn = "player"
    st.session_state.message = ""
    st.session_state.bet = 0
    reset_game()

# --- UI ---
st.title("🃏 Blackjack mit Coins")
st.caption("Nur virtuelle Coins. Spiel gegen die Bank.")

give_daily_bonus()
st.write(f"💰 Coins: **{st.session_state.coins}**")

if st.session_state.bet == 0 and st.session_state.turn == "player":
    bet = st.number_input("Einsatz wählen", min_value=10, max_value=st.session_state.coins, step=10)
    if st.button("🎲 Spiel starten"):
        st.session_state.bet = bet
        st.session_state.coins -= bet
        reset_game()

# --- Spielanzeige ---
if st.session_state.bet > 0:
    st.subheader("🧍 Deine Hand:")
    st.write(" | ".join(st.session_state.player))
    st.write(f"Punkte: **{calculate_score(st.session_state.player)}**")

    st.subheader("🏦 Bank:")
    if st.session_state.turn == "dealer":
        st.write(" | ".join(st.session_state.dealer))
        st.write(f"Punkte: **{calculate_score(st.session_state.dealer)}**")
    else:
        st.write(f"{st.session_state.dealer[0]} | ❓")

# --- Spieleraktion ---
if st.session_state.turn == "player" and st.session_state.bet > 0:
    col1, col2 = st.columns(2)
    if col1.button("🃕 Ziehen"):
        st.session_state.player.append(draw_card())
        if calculate_score(st.session_state.player) > 21:
            st.session_state.message = "💥 Überkauft! Verloren."
            st.session_state.turn = "end"
    if col2.button("✋ Halten"):
        st.session_state.turn = "dealer"
        # Dealer zieht Karten
        while calculate_score(st.session_state.dealer) < 17:
            st.session_state.dealer.append(draw_card())

        # Punkte vergleichen
        p_score = calculate_score(st.session_state.player)
        d_score = calculate_score(st.session_state.dealer)

        if d_score > 21 or p_score > d_score:
            st.session_state.message = "🏆 Gewonnen!"
            st.session_state.coins += st.session_state.bet * 2
        elif p_score == d_score:
            st.session_state.message = "🤝 Unentschieden"
            st.session_state.coins += st.session_state.bet
        else:
            st.session_state.message = "❌ Verloren"
        st.session_state.turn = "end"

# --- Spielende ---
if st.session_state.turn == "end":
    st.success(st.session_state.message)
    if st.button("🔁 Neue Runde"):
        st.session_state.bet = 0
        reset_game()
