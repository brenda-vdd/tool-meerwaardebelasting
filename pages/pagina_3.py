import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.title("📊 Meerwaardebelasting tool België")
with st.container(border=True):
    st.markdown("## 💶 Stap 3 - Bedragen")

aankoop_voor = st.session_state.get("aankoop_voor")
vastgoedvennootschap = st.session_state.get("vastgoedvennootschap")
belastingplichtige = st.session_state.get("belastingplichtige")
participatie = st.session_state.get("participatie")
DBI_aftrek = st.session_state.get("DBI_aftrek")
huwelijksstelsel = st.session_state.get("huwelijksstelsel")
Burgerlijke_staat = st.session_state.get("Burgerlijke_staat")
aankoopwaarde = None
aankoopwaarde_2025 = None
eindwaarde_2025 = None
if aankoop_voor == "Ja":
    aankoopwaarde_2025 = st.number_input(
        "Wat is de oorspronkelijke aankoopwaarde?",
        min_value=0.00,
        step=100.00,
     )
    eindwaarde_2025 = st.number_input(
        "Wat is de waarde op 31/12/2025?",
        min_value = 0.00,
        step= 100.00
     )
    aankoopwaarde_berekening = max(aankoopwaarde_2025, eindwaarde_2025)
else:
     aankoopwaarde = st.number_input(
        "Wat is de aankoopwaarde?",
        min_value = 0.00,
        step = 100.00
     )
     aankoopwaarde_berekening = aankoopwaarde
Verkoop = st.number_input(
    "Wat is de verkoopwaarde?",
    min_value=0.00,
    step=100.00
)
minderwaarde = None
minderwaarden_bedrag = 0.0
voorlopige_meerwaarde = Verkoop - aankoopwaarde_berekening

toon_minderwaarde_vraag = not (
    belastingplichtige == "Vennootschap (VenB)"
)

if voorlopige_meerwaarde > 0 and toon_minderwaarde_vraag:

    minderwaarde = st.radio(
        "Hebt u minderwaarden?",
        ["Ja", "Nee"]
    )
    minderwaarden_bedrag = 0.0
    with st.expander("ℹ️ Info over de minderwaarde"):
        st.write("Minderwaarden kunnen enkel verrekend worden als de minderwaarden in hetzelfde aanslagjaar zijn en binnen dezelfde categorie van financiële activa.")

    if minderwaarde == "Ja":
        minderwaarden_bedrag = st.number_input(
            "Wat is de minderwaarde?",
            min_value=0.00,
            step = 100.00
        )
meerwaarde = Verkoop - aankoopwaarde_berekening - minderwaarden_bedrag
if meerwaarde >= 0:
    titel = "Te belasten meerwaarde"
    bedrag = meerwaarde
else:
    titel = "Minderwaarde"
    bedrag = abs(meerwaarde)
if belastingplichtige == "Vennootschap (VenB)":
    tekst_minderwaarde = "Aangezien er sprake is van een minderwaarde, is er geen belasting verschuldigd."
else:
    tekst_minderwaarde = "Aangezien er sprake is van een minderwaarde, is er geen meerwaardebelasting verschuldigd."
    with st.container (border=False):
        st.markdown(
f"""
<div style="
background-color:#fffbea;
padding:20px;
border-left:8px solid #f5df00;
border-radius:12px;
color:#7a5c00;
">
         
<h2> {titel} </h2>
<h1>
€ {meerwaarde:,.2f}
</h1>
   
</div>
""".replace(","," ")
   .replace(".",","),
unsafe_allow_html=True
)
st.write("")
if titel == "Minderwaarde":
    with st.container (border=False):  
        st.markdown(
f"""
<div style="
background-color:#fff1f2;
padding:20px;
border-left:8px solid #e30814;
border-radius:12px;
color:#7f1d1d;
">
         
<h2> Minderwaarde: </h2>
<p>{tekst_minderwaarde}<p>
</div>
""",
    unsafe_allow_html=True
)
toon_vrijstelling = meerwaarde > 0 and not(
    belastingplichtige == "Vennootschap (VenB)"
    and DBI_aftrek == "Nee"
) and participatie != "Interne meerwaarde"
if toon_vrijstelling:
    st.write("")
    with st.container(border=True):
        st.markdown("## 💶 Stap 3.1 - Vrijstelling")

    if toon_vrijstelling:
        # Reeds gebruikte vrijstelling
        hoeveel_vrijstelling = 0.00
        
        vrijstelling_gebruikt = st.radio(
            "Hebt u dit jaar al FVA verkocht en de vrijstelling (deels) gebruikt?",
            ["Ja", "Nee"]
        )
        if vrijstelling_gebruikt == "Ja":
            hoeveel_vrijstelling = st.number_input(
            "Hoeveel van de vrijstelling hebt u al gebruikt?",
                min_value = 0.00,
                step = 100.00
             )

    # Algemene vrijstelling bepalen
    if belastingplichtige == "Vennootschap (VenB)" and DBI_aftrek == "Ja":
        vrijstelling = 0
        vrijstelling_tekst = "Vrijgesteld"
    elif participatie == "Aanmerkelijk belang-meerwaarde (≥ 20%)":
        vrijstelling = 1_000_000
        vrijstelling_tekst = "€ 1 000 000"

    elif Burgerlijke_staat == "Alleenstaande":
        vrijstelling = 10_000
        vrijstelling_tekst = "€ 10 000"

    elif(Burgerlijke_staat == "Gehuwd"
        and huwelijksstelsel in [
            "Gemeenschap van goederen"]
    ):
        vrijstelling = 20_000
        vrijstelling_tekst = "€ 20 000"

    else:
        vrijstelling = 10_000
        vrijstelling_tekst = "€ 10 000"
    beschikbare_vrijstelling = max(0,vrijstelling - hoeveel_vrijstelling)

    col1, col2 = st.columns (2)

    with col1:
        st.markdown(
            f"""
<div style="
background-color:#f7fbe8;
padding:20px;
border-left:8px solid #98c21d;
border-radius:12px;
text-align:center;
color:#4d5f12;
">
<h4 style="margin-top:0;">
Totale vrijstelling dit jaar
</h4>

<h2 style="margin-bottom:0;">
€ {vrijstelling:,.0f}
</h2>

</div>
""".replace(",", " "),
        unsafe_allow_html=True
     )
    with col2:
        st.markdown(
            f"""
<div style="
background-color:#f7fbe8;
padding:20px;
border-left:8px solid #98c21d;
border-radius:12px;
text-align:center;
color:#4d5f12;
">

<h4 style="margin-top:0;">
Beschikbare vrijstelling
</h4>

<h2 style="margin-bottom:0;">
€ {beschikbare_vrijstelling:,.0f}
</h2>

</div>
""".replace(",", " "),
        unsafe_allow_html=True
     )
    st.write("")
    vrijstelling_gebruiken = st.radio(
        "Wenst u de vrijstelling te gebruiken?",
        ["Ja", "Nee"]
)
else:
    vrijstelling = 0
    beschikbare_vrijstelling = 0
    vrijstelling_gebruikt = "Nee"
    vrijstelling_gebruiken = "Nee"
    
    if meerwaarde > 0:
        st.markdown(
            """
<div style="
background-color:#fffbea;
padding:20px;
border-left:8px solid #f5df00;
border-radius:12px;
color:#7a5c00;
">

<h2 style="margin-bottom:0;">
Voor deze vennootschap is geen vrijstelling van toepassing.
</h2>
</div>
""",
    unsafe_allow_html=True
)
st.write("")

if st.button ("⬅️ Vorige"):
    st.switch_page("pages/pagina_2.py")
if st.button("Berekenen ➡️"):
    st.session_state["aankoopwaarde_2025"] = aankoopwaarde_2025
    st.session_state["eindwaarde_2025"] = eindwaarde_2025
    st.session_state["aankoopwaarde"] = aankoopwaarde
    st.session_state["Verkoop"] = Verkoop
    st.session_state["minderwaarde"] = minderwaarde
    st.session_state["minderwaarden_bedrag"] = minderwaarden_bedrag
    st.session_state["vrijstelling_gebruikt"] = vrijstelling_gebruikt
    st.session_state["vrijstelling_gebruiken"] = vrijstelling_gebruiken
    st.session_state["beschikbare_vrijstelling"] = beschikbare_vrijstelling
    st.session_state["meerwaarde"] = meerwaarde
    st.session_state["titel"] = titel
    st.session_state["aankoopwaarde_berekening"] = aankoopwaarde_berekening
    st.switch_page("pages/pagina_4.py")
st.caption(
    "Deze tool is louter informatief en vervangt geen fiscaal advies."
    " Raadpleeg steeds een expert voor uw persoonlijke situatie.")