
import streamlit as st

st.set_page_config(page_title="🚑 Krankenhaus Klicker", layout="centered")
st.title("🚑 Krankenhaus Klicker")

if "points" not in st.session_state:
    st.session_state.points = 0
if "click_value" not in st.session_state:
    st.session_state.click_value = 1
if "upgrade_cost" not in st.session_state:
    st.session_state.upgrade_cost = 20
if "click_upgrades" not in st.session_state:
    st.session_state.click_upgrades = 0

if st.button(f"🚑 Patienten retten (+{st.session_state.click_value})"):
    st.session_state.points += st.session_state.click_value

st.metric("👥 Gerettete Patienten", int(st.session_state.points))
st.metric("🖱️ Patienten pro Klick", int(st.session_state.click_value))

st.subheader("⬆️ Klickkraft verbessern")
st.write(f"**Aktuelle Stufe:** {st.session_state.click_upgrades}")
st.write(f"**Kosten:** {int(st.session_state.upgrade_cost)} Patienten")

if st.button("📈 Upgrade kaufen"):
    if st.session_state.points >= int(st.session_state.upgrade_cost):
        st.session_state.points -= int(st.session_state.upgrade_cost)
        st.session_state.click_value += 1
        st.session_state.click_upgrades += 1
        st.session_state.upgrade_cost = int(st.session_state.upgrade_cost * 1.5)
    else:
        st.warning("❌ Nicht genug Patienten für ein Upgrade!")

st.markdown("---")

if st.button("🔁 Spiel zurücksetzen"):
    st.session_state.points = 0
    st.session_state.click_value = 1
    st.session_state.upgrade_cost = 20
    st.session_state.click_upgrades = 0
    st.success("Spiel wurde zurückgesetzt! Bitte aktualisiere die Seite manuell.")
