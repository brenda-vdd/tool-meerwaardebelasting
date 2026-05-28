import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

belastingplichtige = st.session_state.get("belastingplichtige")
DBI_aftrek = st.session_state.get("DBI_aftrek")

st.title("📊 Meerwaardebelasting tool België")

with st.container(border=True):
    st.markdown("## 📂 Stap 2 - Type financieel activa")

soort_activa = st.selectbox(
    "Welke soort financiële activa wordt verkocht?",
    ["Categorie 1: financiële instrumenten",
     "Categorie 2: tak 21-, tak 23- en tak 26",
     "Categorie 3: crypto activa",
     "Categorie 4: valuta"]
    )
with st.expander("ℹ️ Info bij soort FVA"):
    st.markdown(
        """
**Categorie 1:** 
Zowel beursgenoteerde als niet-beursgenoteerde aandelen, obligaties, ETF's, derivatencontracten (zoals opties, futures, swaps,...), emissierechten en vergelijkbare producten.

**Categorie 2:** 
Spaar- en beleggingsverzekeringen, waaronder tak 21-, tak 23- en tak 26

**Categorie 3:** 
Dit zijn digitale weergaven van waarde of rechten."

**Categorie 4:** 
Beleggingsgoud, munten, biljetten, digitaal geld,...
"""
    )
buitenlandse_brokers = None
toon_buitenlandse_brokers = not(
    belastingplichtige == "Vennootschap (VenB)"
    and DBI_aftrek == "Nee")
if toon_buitenlandse_brokers:
    # Extra vraag tonen na keuze
    if soort_activa:
        buitenlandse_brokers = st.radio(
            "Zijn de financiële activa bij buitenlandse brokers, banken of verzekeraars afgesloten?",
            ["Ja", "Nee"]
        )
    with st.expander("ℹ️ Info bij buitenlandse brokers, banken of verzekeraars"):
        st.write("Buitenlandse brokers, banken of verzekeraars zullen de belasting nooit inhouden. U gaat dit zelf moeten aangeven.")

with st.container(border=True):
    st.markdown("## 📅 Stap 2.1 - Aankoop en verkoop")
toon_aankoop_voor = not(
    belastingplichtige == "Vennootschap (VenB)"
    and DBI_aftrek == "Nee"
)

if toon_aankoop_voor:
    aankoop_voor = st.radio(
        "Aangekocht voor 31 december 2025?",
        ["Ja", "Nee"]
    )
    with st.expander("ℹ️ Info over de historische aankoopwaarde"):
        st.write("Voor financiële activa aangekocht voor 31 december 2025 wordt de waarde op 31 december 2025 gebruikt. Indien u de oorspronkelijke aankoopprijs kunt aantonen, dan mag u de hoogste van beide gebruiken. Zonder bewijs gebruikt de fiscus de waarde op 31 december 2025.")
else:
    aankoop_voor = "Nee"
aankoopdatum = st.date_input(
    "Wat is de aankoopdatum van uw financiële activa?",
    value=None,
    format="DD/MM/YYYY"
 )
controle_2025 = not(
    belastingplichtige == "Vennootschap (VenB)"
)
if controle_2025 and aankoopdatum:
    grensdatum = date(2025,12,31)
    if aankoop_voor == "Ja" and aankoopdatum > grensdatum:
        st.error(
            "De aankoopdatum ligt na 31/12/2025. "
            "Gelieve een correcte datum in te vullen."
        )
    if aankoop_voor == "Nee" and aankoopdatum <= grensdatum:
        st.error(
            "De aankoopdatum ligt voor of op 31/12/2025. "
            "Gelieve de juiste optie te selecteren."
        )
verkoopdatum = st.date_input(
    "Wat is de verkoopdatum van uw financîële activa?",
    value=date.today(),
    format="DD/MM/YYYY"
)

toon_participatie = not(
    belastingplichtige == "Vennootschap (VenB)"
    and DBI_aftrek =="Nee"
)
if toon_participatie:
    with st.container(border=True):
        st.markdown("## 💶 Stap 2.3 - Soort meerwaarde")
    participatie = st.selectbox(
        "Soort participatie",
        ["Aanmerkelijk belang-meerwaarde (≥ 20%)",
        "Interne meerwaarde",
        "Gewone meerwaarde"]
 )
else:
    participatie = "Gewone meerwaarde"
if st.button ("⬅️ Vorige"):
    st.switch_page("Tool.py")

if st.button ("Volgende ➡️"):
    st.session_state["soort_activa"] = soort_activa
    st.session_state["buitenlandse_brokers"] = buitenlandse_brokers
    st.session_state["aankoop_voor"] = aankoop_voor
    st.session_state["aankoopdatum"] = aankoopdatum
    st.session_state["verkoopdatum"] = verkoopdatum
    st.session_state["participatie"] = participatie
    st.switch_page("pages/pagina_3.py")
st.caption(
    "Deze tool is louter informatief en vervangt geen fiscaal advies."
    " Raadpleeg steeds een expert voor uw persoonlijke situatie.")