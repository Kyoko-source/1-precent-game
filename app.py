import streamlit as st
import random
from datetime import datetime

# --- Einstellungen ---
ROWS, COLUMNS = 3, 3

LEVEL_SYMBOLS = {
    1: [
        ("🚑", 50, 100),  # Symbol, Gewinn bei 2 gleichen, Gewinn bei 3 gleichen (Faktor vom Einsatz)
        ("⛑️", 20, 50),
        ("💉", 10, 30),
        ("🩺", 5, 15),
        ("🚨", 2, 8),
    ],
    2: [
        ("🚑", 70, 140),
        ("⛑️", 30, 80),
        ("💉", 15, 40),
        ("🩺", 7, 20),
        ("🚨", 3, 10),
        ("🚒", 5, 25),  # neu
    ],
    3: [
        ("🚑", 100, 200),
        ("⛑️", 50, 100),
        ("💉", 30, 70),
        ("🩺", 15, 40),
        ("🚨", 8, 20),
        ("🚒", 10, 50),
        ("🏥", 5, 25),  # neu
    ],
}

# Gewinnlinien (indizes: (row, col))
WIN_LINES = [
    # Horizontal
    [(0,0), (0,1), (0,2)],
    [(1,0), (1,1), (1,2)],
    [(2,0), (2,1), (2,2)],
    # Vertikal
    [(0,0), (1,0), (2,0)],
    [(0,1), (1,1), (2,1)],
    [(0,2), (1,2), (2,2)],
    # Diagonal
    [(0,0), (1,1), (2,2)],
    [(0,2), (1,1), (2,0)],
]

# --- Hilfsfunktionen ---

def weighted_choice(symbols):
    # Erstelle eine Liste mit Symbolen, die je nach Level öfter vorkommen (für unterschiedliche Wahrscheinlichkeiten)
    # Hier einfach gleiche Wahrscheinlichkeiten
    choices = []
    for sym, val2, val3 in symbols:
        # Symbol häufiger je nach Level
        weight = 10  # Standardgewicht
        choices.extend([sym]*weight)
    return random.choice(choices)

def calculate_win(grid, bet, symbols):
    # Gewinn prüfen für alle Gewinnlinien
    symbol_values = {sym: (val2, val3) for sym, val2, val3 in symbols}
    total_win = 0
    win_lines = []
    bonus_active = False

    for idx, line in enumerate(WIN_LINES, 1):
        line_symbols = [grid[r][c] for r,c in line]
        counts = {}
        for s in line_symbols:
            counts[s] = counts.get(s, 0) + 1
        # 3 gleiche?
        for sym, count in counts.items():
            if count == 3:
                win = bet * symbol_values[sym][1]
                total_win += win
                win_lines.append((f"Linie {idx}", "3 gleiche", f"{win} Coins mit {sym}"))
                if sym == "🚑":
                    bonus_active = True
                break
            elif count == 2:
                win = bet * symbol_values[sym][0]
                total_win += win
                win_lines.append((f"Linie {idx}", "2 gleiche", f"{win} Coins mit {sym}"))
                break
    return total_win, bonus_active, win_lines

# --- Session-State Initialisierung ---

defaults = {
    "coins": 1000,
    "last_claim": datetime(2000,1,1).date(),
    "level": 1,
    "grid": [["❓"]*COLUMNS for _ in range(ROWS)],
    "bet": 0,
    "message": "",
    "bonus_active": False,
    "bonus_spins": 0,
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- Täglicher Bonus ---
today = datetime.today().date()
if st.session_state.last_claim != today:
    st.session_state.coins += 500
    st.session_state.last_claim = today
    st.success("🎁 Täglicher Bonus: +500 Coins!")

# --- UI ---
st.title("🚑 Rettungsdienst Slotmaschine")
st.write(f"💰 Dein Guthaben: **{st.session_state.coins} Coins**")
st.write(f"🎚 Level: {st.session_state.level}")

# Einsatz auswählen
if not st.session_state.bonus_active:
    bet = st.number_input("💸 Einsatz wählen", min_value=10, max_value=st.session_state.coins, step=10, value=10)
else:
    bet = st.session_state.bet
    st.info(f"🔄 Bonusrunde! Einsatz automatisch: {bet} Coins")

spin_button = st.button("🎰 Walzen drehen")

# Walzen anzeigen
st.markdown("### 🎰 Walzen:")
for row in st.session_state.grid:
    st.write(" | ".join(row))

# Aktion beim Drehen
if spin_button or st.session_state.bonus_active:
    if not st.session_state.bonus_active:
        if bet > st.session_state.coins:
            st.warning("Nicht genug Coins!")
        else:
            st.session_state.coins -= bet
            st.session_state.bet = bet

    # Spin ausführen
    symbols = LEVEL_SYMBOLS[st.session_state.level]
    new_grid = [[random.choice([sym for sym,_,_ in symbols]) for _ in range(COLUMNS)] for _ in range(ROWS)]
    st.session_state.grid = new_grid

    # Gewinn prüfen
    win, bonus, win_lines = calculate_win(new_grid, st.session_state.bet, symbols)

    if win > 0:
        if bonus:
            st.session_state.message = f"🎉 Bonus ausgelöst! Du hast {len(win_lines)} Gewinnlinien mit 🚑 erzielt."
            st.session_state.bonus_active = True
            st.session_state.bonus_spins = 3
            st.session_state.coins += win
        else:
            st.session_state.message = f"🎉 Du hast {win} Coins gewonnen auf Linien: {', '.join([f'{line[0]} {line[1]} ({line[2]})' for line in win_lines])}!"
            st.session_state.coins += win
    else:
        st.session_state.message = "Leider kein Gewinn."

    if st.session_state.bonus_active:
        st.session_state.bonus_spins -= 1
        if st.session_state.bonus_spins <= 0:
            st.session_state.bonus_active = False
            st.success("🛑 Bonusrunde beendet!")

    # Levelaufstieg
    if st.session_state.coins >= st.session_state.level * 5000:
        st.session_state.level = min(3, st.session_state.level + 1)
        st.balloons()
        st.success(f"🎉 Du bist auf Level {st.session_state.level} aufgestiegen!")

    st.success(st.session_state.message)

# Auszahlungstabelle
st.markdown("## Auszahlungstabelle")

table_html = """
<style>
table, th, td {border:1px solid black; border-collapse: collapse; padding:6px; text-align:center;}
th {background-color:#4CAF50; color:white;}
</style>
<table>
<thead><tr><th>Symbol</th><th>Gewinn bei 2 gleichen</th><th>Gewinn bei 3 gleichen</th></tr></thead>
<tbody>
"""
for sym, val2, val3 in LEVEL_SYMBOLS[st.session_state.level]:
    table_html += f"<tr><td style='font-size:1.8em;'>{sym}</td><td>{val2}× Einsatz</td><td>{val3}× Einsatz</td></tr>"
table_html += "</tbody></table>"

st.markdown(table_html, unsafe_allow_html=True)
