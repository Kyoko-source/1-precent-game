import streamlit as st
import time

st.set_page_config(page_title="🚑 Krankenhaus Klicker", layout="centered")
st.title("🚑 Krankenhaus Klicker")

# Session State initialisieren
if "points" not in st.session_state:
    st.session_state.points = 0.0
if "cps" not in st.session_state:
    st.session_state.cps = 0.0
if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()
if "helpers" not in st.session_state:
    st.session_state.helpers = {
        "👩‍⚕️ Pflegekraft": {"count": 0, "cps": 0.2, "cost": 10},
        "💉 Impfteam": {"count": 0, "cps": 1.0, "cost": 50},
        "🚁 Notfallhelikopter": {"count": 0, "cps": 5.0, "cost": 200},
        "🧪 Laborteam": {"count": 0, "cps": 10.0, "cost": 500},
        "🤖 Medizinroboter": {"count": 0, "cps": 20.0, "cost": 1000},
    }

# Zeit seit letztem Update berechnen
now = time.time()
elapsed = now - st.session_state.last_update
st.session_state.points += elapsed * st.session_state.cps
st.session_state.last_update = now

# Button zum "Klicken"
if st.button("🚑 Krankenwagen losschicken"):
    st.session_state.points += 1

# Anzeigen aktueller Status
st.metric(label="👥 Gerettete Patienten", value=int(st.session_state.points))
st.metric(label="⏱️ Patienten/Sekunde", value=round(st.session_state.cps, 2))

st.subheader("🩺 Medizinische Unterstützung kaufen")

# Helfer kaufen
for name, data in st.session_state.helpers.items():
    col1, col2, col3 = st.columns([4, 2, 2])
    with col1:
        st.write(f"{name} (x{data['count']}) – {data['cost']} Patienten")
    with col2:
        if st.button(f"Kaufen {name}", key=name):
            if st.session_state.points >= data["cost"]:
                st.session_state.points -= data["cost"]
                data["count"] += 1
                st.session_state.cps += data["cps"]
                data["cost"] = int(data["cost"] * 1.15)  # Preis steigt leicht

# Spiel zurücksetzen
st.markdown("---")
if st.button("🔁 Spiel zurücksetzen"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()

