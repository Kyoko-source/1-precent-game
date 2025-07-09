import streamlit as st
import random
from datetime import datetime

CARD_VALUES = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":10,"Q":10,"K":10,"A":11}
FULL_DECK = list(CARD_VALUES.keys())*4

def calculate_score(hand):
    score = sum(CARD_VALUES[c] for c in hand)
    aces = hand.count("A")
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

def draw_card():
    if not st.session_state.deck:
        st.session_state.deck = FULL_DECK.copy()
        random.shuffle(st.session_state.deck)
    return st.session_state.deck.pop()

def start_game(bet):
    st.session_state.bet = bet
    st.session_state.coins -= bet
    st.session_state.player_hand = [draw_card(), draw_card()]
    st.session_state.dealer_hand = [draw_card(), draw_card()]
    st.session_state.turn = "player"
    st.session_state.message = ""
    st.session_state.game_active = True

def dealer_plays():
    while calculate_score(st.session_state.dealer_hand) < 17:
        st.session_state.dealer_hand.append(draw_card())

def end_game():
    if st.session_state.turn != "dealer":
        dealer_plays()

    p = calculate_score(st.session_state.player_hand)
    d = calculate_score(st.session_state.dealer_hand)

    if p > 21:
        st.session_state.message = "💥 Überkauft! Verloren."
    elif d > 21 or p > d:
        st.session_state.message = "🏆 Gewonnen!"
        st.session_state.coins += st.session_state.bet*2
    elif p == d:
        st.session_state.message = "🤝 Unentschieden!"
        st.session_state.coins += st.session_state.bet
    else:
        st.session_state.message = "❌ Verloren!"

    st.session_state.turn = "end"
    st.session_state.game_active = False

defaults = {
    "coins": 1000,
    "last_claim": datetime(2000,1,1).date(),
    "deck": FULL_DECK.copy(),
    "player_hand": [],
    "dealer_hand": [],
    "turn": "start",
    "bet": 0,
    "message": "",
    "game_active": False,
}

for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

today = datetime.today().date()
if st.session_state.last_claim != today:
    st.session_state.coins += 1000
    st.session_state.last_claim = today
    st.success("🎁 Täglicher Bonus: +1000 Coins")

st.title("🃏 Blackjack mit Coins")
st.caption("Spiele Blackjack gegen die Bank – rein virtuell.")
st.write(f"💰 Coins: **{st.session_state.coins}**")

if not st.session_state.game_active and st.session_state.turn != "end":
    bet = st.number_input("💸 Einsatz wählen", min_value=10, max_value=st.session_state.coins, step=10)
    if st.button("🎮 Spielen"):
        start_game(bet)
        st.experimental_rerun()

if st.session_state.game_active or st.session_state.turn == "end":
    st.subheader("🧍 Deine Karten:")
    st.write(" | ".join(st.session_state.player_hand))
    st.write(f"🧮 Punkte: **{calculate_score(st.session_state.player_hand)}**")

    st.subheader("🏦 Bank:")
    if st.session_state.turn in ["dealer","end"]:
        st.write(" | ".join(st.session_state.dealer_hand))
        st.write(f"🧮 Punkte: **{calculate_score(st.session_state.dealer_hand)}**")
    else:
        st.write(f"{st.session_state.dealer_hand[0]} | ❓")

if st.session_state.turn == "player":
    c1,c2 = st.columns(2)
    if c1.button("🃕 Karte ziehen"):
        st.session_state.player_hand.append(draw_card())
        if calculate_score(st.session_state.player_hand) > 21:
            end_game()
        st.experimental_rerun()
    if c2.button("✋ Halten"):
        st.session_state.turn = "dealer"
        end_game()
        st.experimental_rerun()

if st.session_state.turn == "end":
    st.subheader("📢 Ergebnis:")
    st.success(st.session_state.message)
    if st.button("🔁 Neue Runde"):
        st.session_state.bet = 0
        st.session_state.player_hand = []
        st.session_state.dealer_hand = []
        st.session_state.turn = "start"
        st.session_state.message = ""
        st.session_state.game_active = False
        st.experimental_rerun()
