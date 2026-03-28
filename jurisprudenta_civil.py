import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Pt
import io

st.set_page_config(page_title="Expert Jurisprudență Proprietate", page_icon="⚖️", layout="wide")

# BAZA DE DATE ACTUALIZATĂ (7 SITUAȚII)
if 'data' not in st.session_state:
    st.session_state.data = [
        {
            "id": "RECT-907", 
            "sit": "1. RECTIFICAREA ÎNTABULĂRII (ART. 907 C. CIV.) ÎN BAZA S. 832/2000", 
            "leg": "Art. 907-908 C. Civ. / Art. 430 C.pc.", 
            "iccj": "S. 832/2000 IREVOCABILĂ", 
            "arg": "Cererea de rectificare se bazează pe Sentința 832/2000 (Revendicare), bazată pe Planul Parcelar și PV de punere în posesie. Expertul nu poate menține suprapunerea fără a încălca autoritatea de lucru judecat.",
            "q": "Să precizeze expertul cum justifică menținerea unei suprapuneri nelegale în fața unei sentințe de revendicare irevocabile?"
        },
        {
            "id": "GRAN-REV", 
            "sit": "2. PRIORITATEA REVENDICĂRII FAȚĂ DE GRĂNIȚUIRE", 
            "leg": "Art. 560-561 C. Civ. vs. Art. 563 C. Civ.", 
            "iccj": "Jurisprudență Constantă ÎCCJ", 
            "arg": "Contrar susținerilor părții adverse, grănițuirea nu are întâietate față de revendicare. Grănițuirea doar delimitează hotarul, pe când revendicarea (S. 832/2000) a stabilit însuși dreptul de proprietate. O grănițuire ulterioară nu poate constitui titlu de achiziție pentru suprafața de 932 mp deja pierdută în revendicare.",
            "q": "Cum poate expertul să valideze o grănițuire care încalcă o sentință de revendicare irevocabilă, ignorând faptul că revendicarea tranșează însuși dreptul de proprietate?"
        },
        {
            "id": "OBJ-1", 
            "sit": "3. NERESPECTAREA MANDATULUI INSTANȚEI (OBIECTIVUL NR. 1)", 
            "leg": "Art. 330 C.pc.", 
            "iccj": "Decizia 66/2020 ICCJ", 
            "arg": "Expertul a ignorat dispoziția de a face repoziționarea conform Planului Parcelar validat. Refuzul răspunsului tehnic constituie o sfidare a mandatului judiciar.",
            "q": "De ce expertul nu a prezentat varianta tehnică ce transpune riguros Planul Parcelar pe teren, așa cum s-a dispus prin Obiectivul nr. 1?"
        },
        {
            "id": "MAR-19", 
            "sit": "4. MĂRIREA NELEGALĂ A SUPRAFEȚEI VECINULUI CU 19%", 
            "leg": "Legea 18/1991 / Art. 583 Cod Civil", 
            "iccj": "Principiul intangibilității Titlului L.18", 
            "arg": "Mărirea suprafeței vecinului cu 19% fără titlu legal este nulă. Expertul nu poate 'legaliza' prin raportul său o ocupare de fapt care încalcă actele de achiziție validate.",
            "q": "Să indice expertul temeiul legal prin care a validat o suprafață cu 19% mai mare pentru vecin, deși acesta nu deține un Titlu modificat?"
        },
        {
            "id": "DIM-1", 
            "sit": "5. DIMINUAREA NELEGALĂ A SUPRAFEȚEI DIN TITLU", 
            "leg": "Art. 44 Constituție", 
            "iccj": "Decizia 66/2020 ICCJ", 
            "arg": "Expertul nu poate diminua suprafața din Titlu pentru a compensa erori. Titlul de proprietate validat administrativ este intangibil.",
            "q": "De ce s-a procedat la diminuarea suprafeței mele din Titlu, deși terenul există real în tarlă?"
        },
        {
            "id": "TRANS-1", 
            "sit": "6. TRANSLATAREA PARCELEI ȘI EFECTUL DE DOMINO", 
            "leg": "Art. 1200 Cod Civil / RIL 24/2024", 
            "arg": "Repoziționarea prin translatare ignoră Planul Parcelar și creează suprapuneri peste terți deja întabulați, încălcând ordinea publică a cadastrului.",
            "q": "Cum justifică expertul varianta care 'împinge' parcela mea peste vecini deja întabulați?"
        },
        {
            "id": "PROC-1", 
            "sit": "7. NERESPECTAREA COTELOR DIN FIȘA DE CALCUL L.18", 
            "leg": "HG 890/2005 / Art. 27 L.18/1991", 
            "iccj": "Securitatea Raporturilor Juridice", 
            "arg": "Dimensiunile laturilor din documentele premergătoare sunt obligatorii. Expertul nu poate modifica cote validate administrativ.",
            "q": "De ce expertul a ignorat dimensiunile laturilor din Fișa de Calcul care a fundamentat Titlul și PV de Punere în Posesie?"
        }
    ]

# Restul codului Streamlit (Interfață și Word) rămâne identic cu cel anterior...
# (Codul de interfață urmează aici ca în mesajele precedente)
