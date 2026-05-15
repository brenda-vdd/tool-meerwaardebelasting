import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.title("📊 Meerwaardebelasting tool België")

meerwaarde = st.session_state.get("meerwaarde")
beschikbare_vrijstelling = st.session_state.get("beschikbare_vrijstelling")
participatie = st.session_state.get("participatie")
vrijstelling_gebruiken = st.session_state.get("vrijstelling_gebruiken")
belastingplichtige = st.session_state.get("belastingplichtige")
vastgoedvennootschap = st.session_state.get("vastgoedvennootschap")
DBI_aftrek = st.session_state.get("DBI_aftrek")
huwelijksstelsel = st.session_state.get("huwelijksstelsel")
Burgerlijke_staat = st.session_state.get("Burgerlijke_staat")
soort_activa = st.session_state.get("soort_activa")
aankoop_voor = st.session_state.get("aankoop_voor")
aankoopdatum = st.session_state.get("aankoopdatum")
verkoopdatum = st.session_state.get("verkoopdatum")
aankoopwaarde = st.session_state.get("aankoopwaarde")
minderwaarde = st.session_state.get("minderwaarde")
eindwaarde_2025 = st.session_state.get("eindwaarde_2025")
aankoopwaarde_2025 = st.session_state.get("aankoopwaarde_2025")
minderwaarden_bedrag = st.session_state.get("minderwaarden_bedrag")
verkoop = st.session_state.get("verkoop")

if belastingplichtige == "Niet-inwoner":
    st.markdown(
        """
<div style="
background-color:#eef8fd;
padding:20px;
border-left:6px solid #14a0e3;
border-radius:12px;
">

<h4 style="
margin-top:0;
color:#0b2e4f;
">
Niet-inwoner
</h4>
<h2 style="
color:#0b2e4f;
font-size:17px;
margin-bottom:0;
">
De Belgische meerwaardebelasting is niet van toepassing.
</h2>

</div>

""",
    unsafe_allow_html=True
)
    belasting = 0
    st.write("")
    if st.button("🔁 Nieuwe berekening", key="nieuwe_berekening_niet-inwoner"):
        st.session_state.clear()
        st.switch_page("Tool.py")
    
    st.stop()
tarief_tekst = ""

def bereken_ab_belasting(meerwaarde, gebruikte_vrijstelling):
    resterend = max(0,meerwaarde - gebruikte_vrijstelling)
    belasting = 0

    eerste_schijf_grens = max(0, 2_500_000 - gebruikte_vrijstelling)

    schijf_1 = min(resterend, eerste_schijf_grens)
    belasting += schijf_1 * 0.0125
    resterend -= schijf_1

    if resterend > 0:
        schijf_2 = min(resterend, 2_500_000)
        belasting +=schijf_2 * 0.025
        resterend -= schijf_2
    if resterend > 0:
        schijf_3 = min(resterend, 5_000_000)
        belasting += schijf_3 * 0.05
        resterend -= schijf_3
    if resterend > 0:
        belasting += resterend * 0.10
    return belasting

# Gebruiker gebruikt de vrijstelling niet
if vrijstelling_gebruiken == "Ja":
    gebruikte_vrijstelling = beschikbare_vrijstelling
    belastbare_basis = max(0,meerwaarde - beschikbare_vrijstelling)
else:
    gebruikte_vrijstelling = 0 
    belastbare_basis = meerwaarde

# vennootschap
if belastingplichtige == "Vennootschap (VenB)":

    # DBI-aftrek --> vrijgesteld
    if DBI_aftrek == "Ja":
        belasting = 0
        tarief_tekst = "Vrijgesteld"

    elif vastgoedvennootschap == "Nee" and DBI_aftrek == "Nee":
        belasting = belastbare_basis *0.25
        tarief_tekst = "25.00%"

    # Vastgoedvennootschap --> meerwaardebelasting
    elif vastgoedvennootschap == "Ja":

        if participatie == "Interne meerwaarde":
            belasting = belastbare_basis * 0.33
            tarief_tekst = "33,00%"

    elif participatie == "Aanmerkelijk belang-meerwaarde (≥ 20%)":
        belasting = bereken_ab_belasting(meerwaarde,gebruikte_vrijstelling)
        tarief_tekst = "Progressief tarief"
    else: 
        belasting = belastbare_basis * 0.10
        tarief_tekst = "10,00%"
else:

    # Andere belastingplichtige
    if participatie == "Interne meerwaarde":
        belasting = belastbare_basis *0.33
        tarief_tekst = "33,00%"

    elif participatie == "Aanmerkelijk belang-meerwaarde (≥ 20%)":
        belasting = bereken_ab_belasting(meerwaarde,gebruikte_vrijstelling)
        tarief_tekst = "Progressief tarief"

    else:
        belasting = belastbare_basis * 0.10
        tarief_tekst = "10,00%"

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
         
<h2> Verschuldigde meerwaardebelasting: </h2>
<h1>
€ {belasting:,.0f}
</h1>
   
</div>
""".replace(",","."),
unsafe_allow_html=True
)
st.write("")

col1, col2 = st.columns (2)

with col1:
    st.markdown(
        f"""
<div style="
padding:10px;
text-align:center;
display:flex;
flex-direction:column;
justify-content:flex-start;
height:140px;
border:2px solid #080808;
border-radius:12px;
background-color:white;
">

<h4>Meerwaarde</h4>

<h2>
€ {meerwaarde:,.0f}
</h2>

</div>
""".replace(",", "."),
     unsafe_allow_html = True
  )
with col2:
    st.markdown(
        f"""
<div style="
padding:10px;
text-align:center;
display:flex;
flex-direction:column;
justify-content:flex-start;
height:140px;
border:2px solid #080808;
border-radius:12px;
background-color:white;
">

<h4 style="color:#98c21d">
Vrijstelling</h4>

<h2 style = "color:#98c21d;">
€ {gebruikte_vrijstelling:,.0f}
</h2>

</div>
""".replace(",", "."),
        unsafe_allow_html = True
   )
st.write("")
col1, col2 = st.columns (2)
with col1:
    st.markdown(
        f"""
<div style="
padding:10px;
text-align:center;
display:flex;
flex-direction:column;
justify-content:flex-start;
height:140px;
border:2px solid #080808;
border-radius:12px;
background-color:white;
">

<h4 style="color:#e30814
"> 
Belastbaar bedrag </h4>

<h2 style="color:#e30814;">
€ {belastbare_basis:,.0f}
</h2>

</div>
""".replace(",", "."),
        unsafe_allow_html = True
   )
with col2:
    st.markdown(
        f"""
<div style="
padding:10px;
text-align:center;
display:flex;
flex-direction:column;
justify-content:flex-start;
height:140px;
border:2px solid #080808;
border-radius:12px;
background-color:white;
">

<h4 style="
margin-top:0;
">
Tarief 
</h4>

<h2 style="
line-height: 1.4;
word-wrap:break-word;
margin:0;
">
{tarief_tekst}
</h2>

</div>
""".replace(",","."),
        unsafe_allow_html = True
    )

st.subheader("💡 Advies & actiepunten")
    
st.markdown(
    """
<div style="
background-color:#eef8fd;
padding:20px;
border-left:8px solid #14a0e3;
border-radius:12px;
">

<h4 style="
margin-top:0;
color:#0b2e4f;
">
Keuze opt-in / opt-out:
</h4>

<p style="
color:#0b2e4f;
font-size:17px;
margin-bottom:0;
">

**Opt-in:**
- De bank of verzekeringsmaatschappij houdt de belasting in zodat u dit niet zelf moet aangeven. 

**Opt-out:**
- U laat weten aan u bank of verzekeringsmaatschappij dat u de belasting zelf gaat aangeven.

### 📬 Verkoop voof 1 juni 2026 - opt-in / opt-out keuze
Bij een verkoop voor 1 juni gaat de bank de belasting niet automatisch inhouden.Tenzij u kiest voor een opt-in. 
### 📬 Verkoop voor 31 augustus 2026 - opt-in / opt-out keuze
Bij een verkoop voor 31 augustus 2026 gaat de verzekeraar de belasting niet automatisch inhouden. Tenzij u kiest voor een opt-in.
</p>

</div>
""",
    unsafe_allow_html=True
)
st.write("")
    
st.markdown(
    """
<div style="
background-color:#eef8fd;
padding:20px;
border-left:8px solid #14a0e3;
border-radius:12px;
">

<h4 style="
margin-top:0;
color:#0b2e4f;
">
📈 Vrijstellingsopbouw
</h4>

<p style="
color:#0b2e4f;
font-size:17px;
margin-bottom:0;
">
Als u de vrijstelling niet helemaal benut, kan gedurende een periode van vijf jaar jaarlijks een bijkomende vrijstelling van € 1.000,00 worden opgebouwd.
Wordt de volledige jaarlijkse vrijstelling aangewend, dan kan er geen vrijstelling worden overgedragen naar volgend jaar. 
</p>

</div>
""",
    unsafe_allow_html=True
)
st.write("")

st.markdown(
    """
<div style="
background-color:#eef8fd;
padding:20px;
border-left:8px solid #14a0e3;
border-radius:12px;
">

<h4 style="
margin-top:0;
color:#0b2e4f;
">
Risicospreiding
</h4>

<p style="
color:#0b2e4f;
font-size:17px;
margin-bottom:0;
">
Het spreiden van beleggingen over verschillende financiële vaste activa kan bijdragen tot risicospreiding, maar heeft niet noodzakelijk een directe impact op de belastingdruk.
</p>

</div>
""",
    unsafe_allow_html=True
)
st.write("")

st.markdown(
    """
<div style="
background-color:#fffbea;
padding:20px;
border-left:8px solid #f5df00;
border-radius:12px;
color: #7a5c00
">

<h4 style="
margin-top:0;
">
📄 Bewijs aankoopwaarde
</h4>

<p style="
font-size:17px;
margin-bottom:0;
">
Bewaar al uw aankoopbewijzen zorgvuldig. Kunt u de historische aankoopwaarde niet bewijzen, dan hanteert de fiscus de waarde van 31 december 2025 als aankoopwaarde.
</p>

</div>
""",
    unsafe_allow_html=True
)
st.write("")

with st.container(border=True):
    st.markdown("## 📋 Samenvatting")
st.write(f"**Belastingplichtige:** {belastingplichtige}")

if Burgerlijke_staat:
    st.write(f"**Burgerlijke staat:** {Burgerlijke_staat}")

if huwelijksstelsel:
    st.write(f"**Huwelijksstelsel:** {huwelijksstelsel}")

st.write(f"**Soort Activa:** {soort_activa}")

if aankoop_voor:
    st.write(f"**Aankoopdatum voor 31/12/2025:** {aankoop_voor}")

st.write(f"**Aankoopdatum:** {aankoopdatum}")

st.write(f"**Verkoopdatum:** {verkoopdatum}")

st.write(f"**Participatie:** {participatie}")

if aankoopwaarde_2025:
    st.write(f"**Aankoopwaarde voor 31/12/2025:** {aankoopwaarde_2025}")
else:
    st.write(f"**Aankoopwaarde:** {aankoopwaarde}")

st.write(f"**Verkoopwaarde:** {verkoop}")

st.write(f"**Minderwaarde:** {minderwaarde}")
if minderwaarde == "Ja":
    st.write(f"**Hoeveel Minderwaarde:** {minderwaarden_bedrag}")


if st.button ("⬅️ Vorige"):

    st.switch_page("pages/pagina_3.py")

if st.button("🔁 Nieuwe berekening"):
    st.session_state.clear()
    st.switch_page("Tool.py")

st.caption(
    "Deze tool is louter informatief en vervangt geen fiscaal advies."
    " Raadpleeg steeds een expert voor uw persoonlijke situatie.")