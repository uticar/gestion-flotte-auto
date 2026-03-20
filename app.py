import streamlit as st
import pandas as pd
from icalevents.icalevents import events
from datetime import datetime, timedelta

st.set_page_config(page_title="Ma Flotte Auto", layout="wide")

st.title("🚗 Gestionnaire de Flotte Turo & Getaround")

# --- CONFIGURATION DE VOS VOITURES ---
# Remplacez les liens entre guillemets par vos propres liens iCal plus tard
FLOTTE = {
    "Véhicule 1": {
        "getaround": "LIEN_ICAL_GETAROUND_ICI",
        "turo": "LIEN_ICAL_TURO_ICI"
    },
    "Véhicule 2": {
        "getaround": "LIEN_ICAL_GETAROUND_ICI",
        "turo": "LIEN_ICAL_TURO_ICI"
    }
}

def charger_reservations(nom, liens):
    donnees = []
    for plateforme, url in liens.items():
        if "http" in url:
            try:
                start = datetime.now() - timedelta(days=2)
                end = datetime.now() + timedelta(days=90)
                items = events(url, start=start, end=end)
                for ev in items:
                    donnees.append({
                        "Voiture": nom,
                        "Plateforme": plateforme.capitalize(),
                        "Début": ev.start,
                        "Fin": ev.end,
                    })
            except:
                pass
    return donnees

all_rentals = []
for nom, liens in FLOTTE.items():
    all_rentals.extend(charger_reservations(nom, liens))

if all_rentals:
    df = pd.DataFrame(all_rentals)
    
    # --- DÉTECTION DE DOUBLONS (CONFLITS) ---
    st.subheader("⚠️ Alertes de conflits")
    conflits = []
    df = df.sort_values("Début")
    for i in range(len(df)-1):
        for j in range(i+1, len(df)):
            if df.iloc[i]['Voiture'] == df.iloc[j]['Voiture']:
                # Si les dates se chevauchent
                if df.iloc[i]['Fin'] > df.iloc[j]['Début']:
                    conflits.append(f"ALERTE : Double réservation sur {df.iloc[i]['Voiture']} ({df.iloc[i]['Plateforme']} & {df.iloc[j]['Plateforme']})")
    
    if conflits:
        for c in conflits:
            st.error(c)
    else:
        st.success("Aucun conflit détecté sur les 90 prochains jours.")

    # --- AFFICHAGE DU TABLEAU ---
    st.subheader("📅 Toutes les réservations")
    df['Début'] = df['Début'].dt.strftime('%d/%m/%Y %H:%M')
    df['Fin'] = df['Fin'].dt.strftime('%d/%m/%Y %H:%M')
    st.table(df)
else:
    st.info("Ajoutez vos liens iCal dans le code pour voir vos réservations.")
