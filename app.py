import streamlit as st

st.set_page_config(page_title="🚑 Krankenhaus Klicker", layout="centered")
st.title("🚑 Krankenhaus Klicker")

# --- Initialisierung ---
if "points" not in st.session_state:
    st.session_state.points = 0
if "click_value" not in st.session_state:
    st.session_state.click_value = 1
if "upgrades" not in st.session_state:
    # Upgrade-Daten: Name, Kosten, Klickwert-Boost, Anzahl gekauft
    st.session_state.upgrades = {
        "Pflegekräfte 👩‍⚕️": {"cost": 20, "value": 1, "owned": 0},
        "Ärzte 👨‍⚕️": {"cost": 100, "value": 5, "owned": 0},
        "Forschung 🧪": {"cost": 500, "value": 10, "owned": 0},
        "Medizinroboter 🤖": {"cost": 2000, "value": 50, "owned": 0},
    }

# --- Funktion: Klickwert neu berechnen ---
def calc_click_value():
    base = 1
    bonus = 0
    for upg in st.session_state.upgrades.values():
        bonus += upg["value"] * upg["owned"]
    return base + bonus

# --- Update Klickwert ---
st.session_state.click_value = calc_click_value()

# --- Kosmetische Krankenwagen-Auswahl ---
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

for name, data in st.session_state.upgrades.items():
    col1, col2, col3, col4 = st.columns([3,2,2,2])
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
                # Kosten steigen bei jedem Kauf um 20%
                data["cost"] = int(data["cost"] * 1.2)
                # Klickwert wird automatisch neu berechnet beim nächsten Klick
                st.success(f"{name} gekauft!")
            else:
                st.warning(f"Nicht genug Patienten für {name}!")

# --- Reset ---
st.markdown("---")
if st.button("🔁 Spiel zurücksetzen"):
    st.session_state.points = 0
    for data in st.session_state.upgrades.values():
        data["cost"] = {
            "Pflegekräfte 👩‍⚕️": 20,
            "Ärzte 👨‍⚕️": 100,
            "Forschung 🧪": 500,
            "Medizinroboter 🤖": 2000,
        }[list(st.session_state.upgrades.keys())[list(st.session_state.upgrades.values()).index(data)]]
        data["owned"] = 0
    st.success("Spiel wurde zurückgesetzt! Bitte Seite neu laden.")
