import streamlit as st
import time
import random

st.set_page_config(page_title="🚑 Krankenhaus Klicker", layout="centered")
st.title("🚑 Krankenhaus Klicker")

MAX_LEVEL = 100

# --- Initialisierung ---
if "points" not in st.session_state:
    st.session_state.points = 0
if "click_value" not in st.session_state:
    st.session_state.click_value = 1
if "upgrades" not in st.session_state:
    st.session_state.upgrades = {
        "Pflegekräfte 👩‍⚕️": {"cost": 20, "value": 1, "owned": 0},
        "Ärzte 👨‍⚕️": {"cost": 100, "value": 5, "owned": 0},
        "Forschung 🧪": {"cost": 500, "value": 10, "owned": 0},
        "Medizinroboter 🤖": {"cost": 2000, "value": 50, "owned": 0},
    }
if "prestige" not in st.session_state:
    st.session_state.prestige = 0
if "boost_active" not in st.session_state:
    st.session_state.boost_active = False
if "boost_end" not in st.session_state:
    st.session_state.boost_end = 0
if "boost_cooldown" not in st.session_state:
    st.session_state.boost_cooldown = 0
if "achievements" not in st.session_state:
    st.session_state.achievements = {
        "100 Patienten gerettet": False,
        "10 Upgrades gekauft": False,
        "Erster Prestige": False,
    }
if "event_active" not in st.session_state:
    st.session_state.event_active = False
if "event_end" not in st.session_state:
    st.session_state.event_end = 0
if "event_points" not in st.session_state:
    st.session_state.event_points = 0

# --- Funktionen ---

def calc_click_value():
    base = 1 + st.session_state.prestige * 0.1  # 10% Bonus pro Prestige-Level
    bonus = 0
    for upg in st.session_state.upgrades.values():
        bonus += upg["value"] * upg["owned"]
    val = base + bonus
    if st.session_state.boost_active:
        val *= 2
    if st.session_state.event_active:
        val *= 2  # Event verdoppelt Klickwert ebenfalls
    return val

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

def check_achievements():
    # Achievement 1: 100 Patienten
    if st.session_state.points >= 100 and not st.session_state.achievements["100 Patienten gerettet"]:
        st.session_state.achievements["100 Patienten gerettet"] = True
        st.success("Achievement erreicht: 100 Patienten gerettet!")
    # Achievement 2: 10 Upgrades gekauft
    total_upgrades = sum(upg["owned"] for upg in st.session_state.upgrades.values())
    if total_upgrades >= 10 and not st.session_state.achievements["10 Upgrades gekauft"]:
        st.session_state.achievements["10 Upgrades gekauft"] = True
        st.success("Achievement erreicht: 10 Upgrades gekauft!")
    # Achievement 3: Erster Prestige
    if st.session_state.prestige >= 1 and not st.session_state.achievements["Erster Prestige"]:
        st.session_state.achievements["Erster Prestige"] = True
        st.success("Achievement erreicht: Erster Prestige Level!")

def maybe_start_event():
    # Event startet zufällig mit 1% Chance pro Klick, wenn kein Event aktiv ist
    if not st.session_state.event_active and random.random() < 0.01:
        st.session_state.event_active = True
        st.session_state.event_end = time.time() + 20  # Event dauert 20 Sekunden
        st.session_state.event_points = 0
        st.info("🚨 Notfall-Ereignis gestartet! Klicke schnell, um Bonuspunkte zu sammeln!")

def end_event():
    st.session_state.event_active = False
    bonus = st.session_state.event_points * 10  # Jeder Klick 10 Bonuspunkte
    st.session_state.points += bonus
    st.success(f"Notfall-Ereignis beendet! Du hast {st.session_state.event_points} mal geklickt und {bonus} Bonuspunkte erhalten!")

# --- Update Klickwert ---
st.session_state.click_value = calc_click_value()

# --- Boost Timer Check ---
now = time.time()
if st.session_state.boost_active and now > st.session_state.boost_end:
    st.session_state.boost_active = False
    st.success("🚨 Notfall-Boost vorbei!")

# --- Boost Cooldown ---
if now > st.session_state.boost_cooldown:
    boost_ready = True
else:
    boost_ready = False
    cd = int(st.session_state.boost_cooldown - now)

# --- Event Timer Check ---
if st.session_state.event_active and now > st.session_state.event_end:
    end_event()

# --- Klick-Button & Event ---
col1, col2 = st.columns([3,1])
with col1:
    if st.button(f"{get_ambulance_emoji(st.session_state.click_value)} Patienten retten (+{int(st.session_state.click_value)})"):
        st.session_state.points += st.session_state.click_value
        # Event: Zähle Klicks
        if st.session_state.event_active:
            st.session_state.event_points += 1
        else:
            maybe_start_event()
with col2:
    if boost_ready:
        if st.button("🚨 Notfall-Boost aktivieren (30s)"):
            st.session_state.boost_active = True
            st.session_state.boost_end = time.time() + 30
            st.session_state.boost_cooldown = time.time() + 120
            st.success("🚨 Notfall-Boost aktiviert! Klickwert x2 für 30 Sekunden.")
    else:
        st.write(f"Boost Cooldown: {cd}s")

# --- Anzeige Punkte & Klickwert & Prestige ---
st.metric("👥 Gerettete Patienten", int(st.session_state.points))
st.metric("🖱️ Patienten pro Klick", int(st.session_state.click_value))
st.metric("⭐ Prestige-Level", st.session_state.prestige)

# --- Upgrade-Bereich ---
st.subheader("⬆️ Medizinische Upgrades kaufen")

for name, data in st.session_state.upgrades.items():
    col1, col2, col3, col4 = st.columns([3,2,2,2])
    with col1:
        st.write(f"**{name}**")
        st.write(f"Gekauft: {data['owned']} / {MAX_LEVEL}")
    with col2:
        st.write(f"Kosten: {int(data['cost'])} Patienten")
    with col3:
        st.write(f"+{data['value']} Klickwert")
    with col4:
        if data["owned"] < MAX_LEVEL:
            if st.button(f"Kaufen", key=name):
                if st.session_state.points >= data["cost"]:
                    st.session_state.points -= data["cost"]
                    data["owned"] += 1
                    # Kosten steigen bei jedem Kauf um 20%
                    data["cost"] = int(data["cost"] * 1.2)
                    st.success(f"{name} gekauft! Stufe {data['owned']}/{MAX_LEVEL}")
                else:
                    st.warning(f"Nicht genug Patienten für {name}!")
        else:
            st.write("Max Stufe erreicht ✅")

# --- Prestige System ---
st.markdown("---")
st.subheader("⏫ Prestige System")
prestige_cost = 10000 * (st.session_state.prestige + 1)
st.write(f"Prestige aufsteigen kostet: {prestige_cost} Patienten")

if st.button("🚀 Aufsteigen (Prestige)"):
    if st.session_state.points >= prestige_cost:
        st.session_state.points = 0
        for key, upg in st.session_state.upgrades.items():
            # Reset Upgrades
            base_costs = {
                "Pflegekräfte 👩‍⚕️": 20,
                "Ärzte 👨‍⚕️": 100,
                "Forschung 🧪": 500,
                "Medizinroboter 🤖": 2000,
            }
            upg["cost"] = base_costs[key]
            upg["owned"] = 0
        st.session_state.prestige += 1
        st.success(f"Prestige erhöht auf Level {st.session_state.prestige}!\nDauerhafter +10% Klickwert Bonus!")
    else:
        st.warning("Nicht genug Patienten für Prestige!")

# --- Achievements Anzeige ---
st.markdown("---")
st.subheader("🏆 Achievements")
for ach, unlocked in st.session_state.achievements.items():
    status = "✅" if unlocked else "❌"
    st.write(f"{status} {ach}")

check_achievements()

# --- Spiel zurücksetzen ---
st.markdown("---")
if st.button("🔁 Spiel komplett zurücksetzen"):
    st.session_state.points = 0
    st.session_state.prestige = 0
    st.session_state.boost_active = False
    st.session_state.boost_end = 0
    st.session_state.boost_cooldown = 0
    st.session_state.event_active = False
    st.session_state.event_end = 0
    st.session_state.event_points = 0
    st.session_state.achievements = {key: False for key in st.session_state.achievements.keys()}
    for key, upg in st.session_state.upgrades.items():
        base_costs = {
            "Pflegekräfte 👩‍⚕️": 20,
            "Ärzte 👨‍⚕️": 100,
            "Forschung 🧪": 500,
            "Medizinroboter 🤖": 2000,
        }
        upg["cost"] = base_costs[key]
        upg["owned"] = 0
    st.success("Spiel wurde komplett zurückgesetzt! Bitte Seite neu laden.")
