import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Pt
import io

# Configurare GeorgeAOH
st.set_page_config(page_title="Expert Jurisprudență Proprietate", page_icon="⚖️", layout="wide")

# Stil vizual pentru bife vizibile
st.markdown("""<style>.stCheckbox { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border: 2px solid #1976d2; }</style>""", unsafe_allow_html=True)

# --- BAZA DE DATE (8 SITUAȚII) ---
data_list = [
    {
        "id": "RECT-907", 
        "sit": "1. RECTIFICAREA ÎNTABULĂRII (ART. 907 C. CIV.) ÎN BAZA S. 832/2000", 
        "leg": "Art. 907-908 C. Civ. / Art. 430 C.pc.", 
        "iccj": "S. 832/2000 IREVOCABILĂ", 
        "arg": "Cererea de rectificare este accesorie dreptului de proprietate stabilit irevocabil prin S. 832/2000. Expertul trebuie să propună varianta care elimină suprapunerea, conform hotărârii.",
        "q": "Să precizeze expertul cum justifică menținerea unei suprapuneri în fața unei sentințe de revendicare irevocabile?"
    },
    {
        "id": "GRAN-REV", 
        "sit": "2. DIFERENȚA DINTRE REVENDICARE ȘI GRĂNIȚUIRE (COMBATERE AVOCAT)", 
        "leg": "Art. 560-563 C. Civ.", 
        "iccj": "Jurisprudență Constantă ÎCCJ / CCR", 
        "arg": "Revendicarea (S. 832/2000) tranșează fondul dreptului, în timp ce grănițuirea doar delimitează hotarul. O grănițuire ulterioară NU poate anula o sentință de revendicare irevocabilă.",
        "q": "Având în vedere că revendicarea are prioritate asupra grănițuirii, cum poate expertul să ignore titlul de proprietate confirmat judiciar?"
    },
    {
        "id": "OBJ-1", 
        "sit": "3. NERESPECTAREA MANDATULUI INSTANȚEI (OBIECTIVUL NR. 1)", 
        "leg": "Art. 330 C.pc. / Art. 187 C.pc.", 
        "iccj": "Decizia 1/2020 ICCJ", 
        "arg": "Expertul a ignorat dispoziția de a face repoziționarea conform Planului Parcelar validat. Refuzul răspunsului tehnic constituie o sfidare a mandatului judiciar.",
        "q": "De ce expertul nu a prezentat varianta tehnică ce transpune riguros Planul Parcelar pe teren, conform obiectivului fixat?"
    },
    {
        "id": "MAR-19", 
        "sit": "4. MĂRIREA NELEGALĂ A SUPRAFEȚEI VECINULUI CU 19%", 
        "leg": "Legea 18/1991 / Art. 583 Cod Civil", 
        "iccj": "Principiul intangibilității Titlului L.18", 
        "arg": "Vecinul deține un excedent de 19% fără titlu modificat legal. Expertul nu poate 'legaliza' o ocupare de fapt în detrimentul unui titlu validat.",
        "q": "Să indice expertul temeiul legal prin care a validat o suprafață cu 19% mai mare pentru vecin?"
    },
    {
        "id": "DIM-1", 
        "sit": "5. DIMINUAREA NELEGALĂ A SUPRAFEȚEI DIN TITLU", 
        "leg": "Art. 44 Constituție", 
        "iccj": "Decizia 66/2020 ICCJ", 
        "arg": "Expertul nu poate diminua suprafața din Titlu pentru a compensa erori tehnice. Titlul validat administrativ este intangibil.",
        "q": "De ce s-a procedat la diminuarea suprafeței mele din Titlu, deși terenul există real în tarlă?"
    },
    {
        "id": "TRANS-1", 
        "sit": "6. TRANSLATAREA PARCELEI ȘI EFECTUL DE DOMINO", 
        "leg": "Art. 1200 Cod Civil / RIL 24/2024", 
        "arg": "Repoziționarea prin translatare ignoră Planul Parcelar și creează suprapuneri peste terți deja întabulați, încălcând certitudinea circuitului civil.",
        "q": "Cum justifică expertul varianta care 'împinge' parcela mea peste vecini deja întabulați?"
    },
    {
        "id": "PROC-1", 
        "sit": "7. NERESPECTAREA COTELOR DIN FIȘA DE CALCUL L.18", 
        "leg": "HG 890/2005 / Art. 27 L.18/1991", 
        "iccj": "Securitatea Raporturilor Juridice", 
        "arg": "Dimensiunile laturilor din Fișa de Calcul sunt obligatorii. Expertul nu poate modifica aceste cote validate administrativ.",
        "q": "De ce expertul a ignorat dimensiunile laturilor din Fișa de Calcul care a fundamentat Titlul?"
    },
    {
        "id": "PARCELAR-ICCJ", 
        "sit": "8. OBLIGATIVITATEA RESPECTĂRII PLANULUI PARCELAR VALIDAT", 
        "leg": "Legea 18/1991 / HG 890/2005", 
        "iccj": "DECIZIA 66/2020 ÎCCJ", 
        "arg": "Conform ÎCCJ, Planul Parcelar fundamentează legalitatea amplasamentului. Expertul este OBLIGAT să respecte geometria tarlalei validate administrativ.",
        "q": "Având în vedere Decizia 66/2020 a ÎCCJ, să precizeze expertul de ce a ales să ignore configurația tarlalei stabilită prin Planul Parcelar?"
    }
]

st.title("⚖️ Expert Jurisprudență - GeorgeAOH")

# Bara de căutare
search_query = st.text_input("🔍 Filtrează spețe:", "")

# Dicționar pentru a păstra observațiile și starea bifelor
if 'selections' not in st.session_state:
    st.session_state.selections = {}

# Afișare bife
for item in data_list:
    if search_query.lower() in item['sit'].lower() or search_query == "":
        with st.container():
            col_bifa, col_text = st.columns([0.1, 0.9])
            with col_bifa:
                # Bifa
                is_checked = st.checkbox("", key=f"check_{item['id']}", value=st.session_state.selections.get(item['id'], False))
                st.session_state.selections[item['id']] = is_checked
            with col_text:
                st.markdown(f"### {item['sit']}")
                st.write(f"📖 **Temei:** {item['leg']} | 🏛️ **ICCJ:** {item['iccj']}")
                if is_checked:
                    obs_key = f"obs_{item['id']}"
                    st.text_area("✍️ Note specifice:", key=obs_key, placeholder="Introduceți detaliile speței...")
            st.divider()

# Funcție Generare Word
def create_word(data_list, selections, session_state, d_nr, d_inst):
    doc = Document()
    p_antet = doc.add_paragraph()
    run_antet = p_antet.add_run(f"CĂTRE: {d_inst}\nDOSAR NR: {d_nr}")
    run_antet.bold, run_antet.font.size = True, Pt(12)
    p_antet.alignment = 2
    doc.add_heading('OBIECTIUNI LA RAPORTUL DE EXPERTIZĂ', 0).alignment = 1

    for s in data_list:
        if selections.get(s['id']):
            h = doc.add_paragraph()
            run_h = h.add_run(s['sit'].upper())
            run_h.bold, run_h.underline, run_h.font.size = True, True, Pt(14)
            doc.add_paragraph(f"Temei Legal: {s['leg']} | {s['iccj']}").italic = True
            
            arg_p = doc.add_paragraph()
            arg_p.add_run("ARGUMENT JURIDIC: ").bold = True
            arg_p.add_run(s['arg'])

            # Luăm observația din session_state
            obs_val = session_state.get(f"obs_{s['id']}", "")
            if obs_val:
                obs_p = doc.add_paragraph()
                obs_p.add_run(f"SITUAȚIA DE FAPT: {obs_val}").bold = True

            q_p = doc.add_paragraph(style='List Number')
            run_q = q_p.add_run(s['q'])
            run_q.bold, run_q.underline = True, True
            
    doc.add_paragraph("\n")
    sanc = doc.add_paragraph()
    run_s = sanc.add_run("SOLICITARE FINALĂ: În temeiul Art. 187 C.pc., solicităm AMENDAREA EXPERTULUI pentru nerespectarea mandatului (Obiectivul nr. 1) și a Autorității de Lucru Judecat (S. 832/2000).")
    run_s.bold, run_s.underline = True, True
    
    bio = io.BytesIO(); doc.save(bio); bio.seek(0)
    return bio

with st.sidebar:
    st.header("📝 Detalii Memoriu")
    nr_dosar = st.text_input("Dosar nr:", "5975/221/2018")
    instanta = st.text_input("Către:", "Tribunalul Hunedoara")
    if st.button("🚀 GENEREAZĂ WORD"):
        has_sel = any(st.session_state.selections.values())
        if has_sel:
            word_bio = create_word(data_list, st.session_state.selections, st.session_state, nr_dosar, instanta)
            st.download_button("📥 DESCARCĂ ACUM", word_bio, f"Obiectiuni_{nr_dosar.replace('/','_')}.docx")
        else:
            st.error("Bifează punctele!")
    if st.button("🔄 RESET"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()
