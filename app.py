import streamlit as st

st.set_page_config(page_title="🚑 Krankenhaus Klicker", layout="centered")
st.title("🚑 Krankenhaus Klicker")

# --- Initialisierung ---
if "points" not in st.session_state:
    st.session_state.points = 0
if "click_value" not in st.session_state:
    st.session_state.click_value = 1
if "upgrades" not in st.session_state:
    # 100 verschiedene Upgrades erzeugen
    st.session_state.upgrades = {}
    base_cost = 20
    base_value = 1
    for i in range(1, 101):
        name = f"Medizinisches Upgrade #{i}"
        cost = int(base_cost * (1.15 ** (i - 1)))  # Kosten steigen exponentiell
        value = base_value * i  # Klickwert steigt linear mit i
        st.session_state.upgrades[name] = {"cost": cost, "value": value, "owned": 0}

# --- Funktion: Klickwert neu berechnen ---
def calc_click_value():
    base = 1
    bonus = 0
    for upg in st.session_state.upgrades.values():
        bonus += upg["value"] * upg["owned"]
    return base + bonus

# --- Update Klickwert ---
st.session_state.click_value = calc_click_value()

# --- Krankenwagen-Emoji (bleibt gleich) ---
def get_ambulance_emoji(click_value):
    if click_value < 5:
        return "🚑"
    elif click_value < 20:
        return "🚒"
    elif click_value < 50:
        return "🚐"
    elif click_value < 100:
        return "🚓"
    else:
        return "🚁"

ambulance_emoji = get_ambulance_emoji(st.session_state.click_value)

# --- Klick-Button ---
if st.button(f"{ambulance_emoji} Patienten retten (+{st.session_state.click_value})"):
    st.session_state.points += st.session_state.click_value

# --- Anzeige Punkte & Klickwert ---
st.metric("👥 Gerettete Patienten", int(st.session_state.points))
st.metric("🖱️ Patienten pro Klick", int(st.session_state.click_value))

# --- Upgrade-Bereich ---
st.subheader("⬆️ Medizinische Upgrades kaufen")

# Damit es nicht ewig scrollt, zeigen wir 20 Upgrades pro Seite (Pagination)
if "page" not in st.session_state:
    st.session_state.page = 0
UPGRADES_PER_PAGE = 20

upgrades_list = list(st.session_state.upgrades.items())
start_idx = st.session_state.page * UPGRADES_PER_PAGE
end_idx = start_idx + UPGRADES_PER_PAGE
page_upgrades = upgrades_list[start_idx:end_idx]

for name, data in page_upgrades:
    col1, col2, col3, col4 = st.columns([4,2,2,2])
    with col1:
        st.write(f"**{name}**")
        st.write(f"Gekauft: {data['owned']}")
    with col2:
        st.write(f"Kosten: {int(data['cost'])} Patienten")
    with col3:
        st.write(f"+{data['value']} Klickwert")
    with col4:
        if st.button(f"Kaufen", key=name):
            if st.session_state.points >= data["cost"]:
                st.session_state.points -= data["cost"]
                data["owned"] += 1
                # Kosten steigen um 15% bei jedem Kauf
                data["cost"] = int(data["cost"] * 1.15)
                st.success(f"{name} gekauft! Anzahl: {data['owned']}")
            else:
                st.warning(f"Nicht genug Patienten für {name}!")

# --- Pagination Buttons ---
col_prev, col_page, col_next = st.columns([1,2,1])
with col_prev:
    if st.button("⬅️ Vorherige Seite") and st.session_state.page > 0:
        st.session_state.page -= 1
with col_page:
    st.write(f"Seite {st.session_state.page + 1} / {(len(st.upgrades) - 1) // UPGRADES_PER_PAGE + 1}")
with col_next:
    if st.button("➡️ Nächste Seite") and end_idx < len(upgrades_list):
        st.session_state.page += 1

# --- Reset ---
st.markdown("---")
if st.button("🔁 Spiel zurücksetzen"):
    st.session_state.points = 0
    for upg in st.session_state.upgrades.values():
        upg["cost"] = int(20 * (1.15 ** (list(st.session_state.upgrades.values()).index(upg))))
        upg["owned"] = 0
    st.success("Spiel wurde zurückgesetzt! Bitte Seite neu laden.")
