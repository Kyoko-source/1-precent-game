
import streamlit as st
import random

st.set_page_config(page_title="Das 1% Spiel", page_icon="🎯", layout="centered")

st.title("🎯 Das 1% Spiel")

# Session State initialisieren
if "counter" not in st.session_state:
    st.session_state.counter = 0
if "chance" not in st.session_state:
    st.session_state.chance = 1

st.markdown("**Regeln:** Mit jedem Klick steigt die Chance um 1%, dass dein Zähler auf 0 zurückgesetzt wird. Schaffst du es, den höchsten Counter zu erreichen?")

# Klick-Button
if st.button("Klick mich!"):
    reset = random.randint(1, 100) <= st.session_state.chance
    if reset:
        st.warning(f"Zurückgesetzt bei {st.session_state.counter} Klicks! 😢")
        st.session_state.counter = 0
        st.session_state.chance = 1
    else:
        st.session_state.counter += 1
        st.session_state.chance += 1

# Anzeigen des aktuellen Zählers
st.metric(label="Aktueller Counter", value=st.session_state.counter)
st.metric(label="Zurücksetz-Chance", value=f"{st.session_state.chance}%")

# Reset-Button für manuelles Zurücksetzen
if st.button("Zurücksetzen"):
    st.session_state.counter = 0
    st.session_state.chance = 1
    st.success("Spiel wurde zurückgesetzt.")
