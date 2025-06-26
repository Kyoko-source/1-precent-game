import streamlit as st

st.set_page_config(page_title="🚑 Krankenhaus Klicker", layout="centered")
st.title("🚑 Krankenhaus Klicker")

# Initialisierung
if "points" not in st.session_state:
    st.session_state.points = 0
if "click_value" not in st.session_state:
    st.session_state.click_value = 1
if "upgrade_cost" not in st.session_state:
    st.session_state.upgrade_cost = 20
if "click_upgrades" not in st.session_state:
    st.session_state.click_upgrades = 0

# Klick-Button
if st.button(f"🚑 Patienten retten (+{st.session_state.click_value})"):
    st.session_state.points += st.session_state.click_value

# Anzeige
st.metric("👥 Gerettete Patienten", st.session_state.points)
st.metric("🖱️ Patienten pro Klick", st.session_state.click_value)

# Upgrade-Bereich
st.subheader("⬆️ Klickkraft verbessern")
st.write(f"Aktuelle Stufe: {st.session_state.click_upgrades}")
st.write(f"Kosten: {st.session_state.upgrade_cost} Patienten")

if st.button("📈 Upgrade kaufen"):
    if st.session_state.points >= st.session_state.upgrade_cost:
        st.session_state.points -= st.session_state.upgrade_cost
        st.session_state.click_value += 1
        st.session_state.click_upgrades += 1
        st.session_state.upgrade_cost = int(st.session_state.upgrade_cost * 1.5)
    else:
        st.warning("Nicht genug Patienten für Upgrade!")

# Reset
st.markdown("---")
if st.button("🔁 Spiel zurücksetzen"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()
