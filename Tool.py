import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Meerwaardebelasting tool België")

with st.container(border=True):
    st.markdown("## 👥 Stap 1 - Profiel van de belastingplichtige")

st.info("velden met een * zijn verplicht.")
belastingplichtige = st.selectbox(
    "Bent u een natuurlijke persoon, VZW / private stichting, niet-inwoner of vennootschap?",
    [
        "Natuurlijke persoon (PB)",
        "VZW / private stichting (RPB)",
        "Niet-inwoner",
        "Vennootschap (VenB)"
        ]
 )

# Extra vraag bij natuurlijke persoon (PB)
Burgerlijke_staat = None
huwelijksstelsel = None
if belastingplichtige == "Natuurlijke persoon (PB)":

    Burgerlijke_staat = st.selectbox(
        "Burgerlijke staat",
        ["Alleenstaande",
         "Gehuwd",
         "Wettelijk samenwonend"]
     )
    # Extra vraag bij Gehuwd
    
    if Burgerlijke_staat == "Gehuwd":
        huwelijksstelsel = st.selectbox(
            "Huwelijksstelsel",
            [
                "Wettelijk stelsel",
                "Scheiding van goederen",
                "Gemeenschap van goederen"]
            )
if belastingplichtige == "Niet-inwoner":
    st.info("Er is geen Belgische meerwaardebelasting van toepassing.")
# Extra vraag bij Vennootschap (VenB)
vastgoedvennootschap = None
DBI_aftrek = None
if belastingplichtige == "Vennootschap (VenB)":

    vastgoedvennootschap = st.radio(
        "Is dit een vastgoedvennootschap?",
        ["Ja", "Nee"],
     )
    
    # Enkel tonen indien GEEN vastgoedvennootschap
    if vastgoedvennootschap == "Nee":

        DBI_aftrek = st.radio(
        "Komt u in aanmerking voor een DBI-aftrek?",
        ["Ja", "Nee"],
     )
# Extra vraag bij VZW / private stichting (RPB)
if belastingplichtige == "VZW / private stichting (RPB)":
    erkende_vzw = st.radio(
        "Gaat het over een fiscaal erkende vereniging die aftrekbare giften ontvangt?",
        ["Ja", "Nee"],
        key = "vereniging"
     )
if st.button ("Volgende ➡️"):
    st.session_state["belastingplichtige"] = belastingplichtige
    st.session_state["vastgoedvennootschap"] = vastgoedvennootschap
    st.session_state["DBI_aftrek"] = DBI_aftrek
    st.session_state["huwelijksstelsel"] = huwelijksstelsel
    st.session_state["Burgerlijke_staat"] = Burgerlijke_staat
    if belastingplichtige == "Niet-inwoner":
        st.switch_page("pages/pagina_4.py")
    if belastingplichtige is None:
        st.error("Gelieve alle verplichte velden in te vullen.")
    
    else:
        st.switch_page("pages/pagina_2.py")
st.caption(
    "Deze tool is louter informatief en vervangt geen fiscaal advies."
    " Raadpleeg steeds een expert voor uw persoonlijke situatie.")