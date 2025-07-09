import streamlit as st
import random
import time
from datetime import datetime

# --- Symbol-Definitionen ---
SYMBOLS_BASE = [
    ("🚑", 3, 5, 50),    # Notarzt (Bonus-Symbol)
    ("🚒", 5, 3, 30),    # Feuerwehrwagen
    ("🚓", 7, 2, 20),    # Polizei
    ("🩺", 10, 1, 10),   # Stethoskop
    ("⛑️", 15, 1, 8),    # Helm
    ("🩹", 20, 1, 5),    # Pflaster
    ("💉", 25, 1, 3),    # Spritze
    ("🩸", 30, 1, 2),    # Blutstropfen
    ("🏥", 40, 2, 15),   # Krankenhaus
]

LEVEL_SYMBOLS = {
    1: SYMBOLS_BASE,
    2: [  # Level 2: höhere Chance für wertvolle Symbole
        ("🚑", 5, 5, 50),
        ("🚒", 7, 3, 30),
        ("🚓", 10, 2, 20),
        ("🩺", 12, 1, 10),
        ("⛑️", 15, 1, 8),
        ("🩹", 20, 1, 5),
        ("💉", 25, 1, 3),
        ("🩸", 30, 1, 2),
        ("🏥", 40, 2, 15),
    ],
    3: [  # Level 3: noch bessere Chancen
        ("🚑", 8, 5, 50),
        ("🚒", 10, 3, 30),
        ("🚓", 15, 2, 20),
        ("🩺", 15, 1, 10),
        ("⛑️", 18, 1, 8),
        ("🩹", 20, 1, 5),
        ("💉", 25, 1, 3),
        ("🩸", 35, 1, 2),
        ("🏥", 40, 2, 15),
    ],
}

ROWS = 3
COLUMNS = 3

def weighted_choice(symbols):
    choices, weights = zip(*[(s[0], s[1]) for s in symbols])
    return random.choices(choices, weights=weights, k=1)[0]

def get_symbol_info(symbol, symbols_list):
    for s in symbols_list:
        if s[0] == symbol:
            return s
    return None

def calculate_win(grid, bet, symbols_list):
    """
    Gewinne werden hier für 3 Reihen + 3 Spalten + 2 Diagonalen geprüft:
    - Gewinn bei 3 gleichen Symbolen in einer Reihe, Spalte oder Diagonale
    - Bonus wird bei 🚑 ausgelöst
    """
    total_win = 0
    bonus_triggered = False
    win_lines = []

    # Check rows
    for r in range(ROWS):
        line = [grid[r][c] for c in range(COLUMNS)]
        if len(set(line)) == 1:
            symbol = line[0]
            info = get_symbol_info(symbol, symbols_list)
            if info:
                total_win += bet * info[3]
                win_lines.append(('Reihe', r+1, symbol))
                if symbol == "🚑":
                    bonus_triggered = True

    # Check columns
    for c in range(COLUMNS):
        line = [grid[r][c] for r in range(ROWS)]
        if len(set(line)) == 1:
            symbol = line[0]
            info = get_symbol_info(symbol, symbols_list)
            if info:
                total_win += bet * info[3]
                win_lines.append(('Spalte', c+1, symbol))
                if symbol == "🚑":
                    bonus_triggered = True

    # Check diagonals
    diag1 = [grid[i][i] for i in range(ROWS)]
    if len(set(diag1)) == 1:
        symbol = diag1[0]
        info = get_symbol_info(symbol, symbols_list)
        if info:
            total_win += bet * info[3]
            win_lines.append(('Diagonal', 1, symbol))
            if symbol == "🚑":
                bonus_triggered = True

    diag2 = [grid[i][COLUMNS - 1 - i] for i in range(ROWS)]
    if len(set(diag2)) == 1:
        symbol = diag2[0]
        info = get_symbol_info(symbol, symbols_list)
        if info:
            total_win += bet * info[3]
            win_lines.append(('Diagonal', 2, symbol))
            if symbol == "🚑":
                bonus_triggered = True

    return total_win, bonus_triggered, win_lines

# --- Session State Init ---
if "coins" not in st.session_state:
    st.session_state.coins = 1000
if "last_claim" not in st.session_state:
    st.session_state.last_claim = datetime(2000,1,1).date()
if "level" not in st.session_state:
    st.session_state.level = 1
if "bonus_active" not in st.session_state:
    st.session_state.bonus_active = False
if "bonus_spins" not in st.session_state:
    st.session_state.bonus_spins = 0
if "message" not in st.session_state:
    st.session_state.message = ""
if "bet" not in st.session_state:
    st.session_state.bet = 0
if "grid" not in st.session_state:
    st.session_state.grid = [["❓"]*COLUMNS for _ in range(ROWS)]

# --- Täglicher Bonus ---
today = datetime.today().date()
if st.session_state.last_claim != today:
    st.session_state.coins += 500
    st.session_state.last_claim = today
    st.success("🎁 Täglicher Bonus: +500 Coins!")

# --- UI ---
st.title("🚑 Rettungsdienst Slotmaschine 3x3")

st.markdown(f"### Level: {st.session_state.level} | 💰 Coins: {st.session_state.coins}")

if not st.session_state.bonus_active:
    bet = st.number_input("💸 Einsatz wählen", min_value=10, max_value=st.session_state.coins, step=10)
else:
    bet = st.session_state.bet

spin_button = st.button("🎰 Drehen")

if spin_button or st.session_state.bonus_active:
    if not st.session_state.bonus_active:
        if bet > st.session_state.coins:
            st.warning("Nicht genug Coins!")
        else:
            st.session_state.coins -= bet
            st.session_state.bet = bet

    # Spin Animation (rudimentär)
    for _ in range(10):
        temp_grid = [[weighted_choice(LEVEL_SYMBOLS[st.session_state.level]) for _ in range(COLUMNS)] for _ in range(ROWS)]
        st.session_state.grid = temp_grid
        for row in st.session_state.grid:
            st.write(" | ".join(row))
        time.sleep(0.05)
        st.experimental_rerun()

    # Endgültiges Ergebnis
    final_grid = [[weighted_choice(LEVEL_SYMBOLS[st.session_state.level]) for _ in range(COLUMNS)] for _ in range(ROWS)]
    st.session_state.grid = final_grid

    for row in final_grid:
        st.write(" | ".join(row))

    # Gewinn prüfen
    win, bonus, win_lines = calculate_win(final_grid, st.session_state.bet, LEVEL_SYMBOLS[st.session_state.level])

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

    if st.session_state.coins >= st.session_state.level * 5000:
        st.session_state.level = min(3, st.session_state.level + 1)
        st.balloons()
        st.success(f"🎉 Du bist auf Level {st.session_state.level} aufgestiegen!")

    st.success(st.session_state.message)
    st.experimental_rerun()

# Zeige aktuelle Walzen
st.markdown("### 🎰 Aktuelles Walzen-Grid:")
for row in st.session_state.grid:
    st.write(" | ".join(row))

# Auszahlungstabelle
st.markdown("## Auszahlungstabelle")
table_html = """
<table>
<thead><tr><th>Symbol</th><th>Gewinn bei 2 gleichen</th><th>Gewinn bei 3 gleichen</th></tr></thead>
<tbody>
"""
for sym, _, val2, val3 in LEVEL_SYMBOLS[st.session_state.level]:
    table_html += f"<tr><td style='font-size:1.8em;'>{sym}</td><td>{val2}× Einsatz</td><td>{val3}× Einsatz</td></tr>"
table_html += "</tbody></table>"

st.markdown(table_html, unsafe_allow_html=True)
