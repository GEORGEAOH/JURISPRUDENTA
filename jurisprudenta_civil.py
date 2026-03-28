import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Pt
import io

# 1. Configurare Pagină
st.set_page_config(page_title="Expert Jurisprudență GeorgeAOH", page_icon="⚖️", layout="wide")

# Stil vizual pentru bife
st.markdown("""<style>.stCheckbox { background-color: #f0f2f6; padding: 10px; border-radius: 10px; border: 2px solid #1976d2; }</style>""", unsafe_allow_html=True)

# 2. Funcție Resetare Completă
def reset_form():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# 3. Baza de Date Completă (Toate cele 8 puncte VERIFICATE MANUAL)
data_points = [
    {
        "id": "RECT-907", 
        "sit": "1. RECTIFICAREA ÎNTABULĂRII (ART. 907 C. CIV.) ÎN BAZA S. 832/2000", 
        "leg": "Art. 907-908 C. Civ. / Art. 430 C.pc.", 
        "iccj": "S. 832/2000 IREVOCABILĂ", 
        "arg": "Cererea de rectificare este accesorie dreptului de proprietate stabilit prin S. 832/2000. Expertul trebuie să elimine suprapunerea peste cei 932 mp.", 
        "q": "Să precizeze expertul cum justifică menținerea unei suprapuneri în fața unei sentințe de revendicare irevocabile?"
    },
    {
        "id": "GRAN-REV", 
        "sit": "2. PRIORITATEA REVENDICĂRII FAȚĂ DE GRĂNIȚUIRE (COMBATERE)", 
        "leg": "Art. 560-563 C. Civ. / Decizia ÎCCJ nr. 433/2006", 
        "iccj": "Jurisprudență Constantă (Decizia ÎCCJ nr. 433/2006)", 
        "arg": "Conform jurisprudenței constante (ex. Decizia 433/2006), o acțiune în grănițuire ulterioară NU are caracter constitutiv de drepturi și nu poate invalida o hotărâre în revendicare (S. 832/2000).", 
        "q": "Cum poate expertul să valideze o grănițuire care încalcă o sentință de revendicare irevocabilă?"
    },
    {
        "id": "OBJ-1", 
        "sit": "3. NERESPECTAREA MANDATULUI (OBIECTIVUL NR. 1)", 
        "leg": "Art. 330 C.pc. / Art. 187 C.pc.", 
        "iccj": "Decizia 1/2020 ICCJ", 
        "arg": "Expertul a ignorat dispoziția de a face repoziționarea conform Planului Parcelar validat. Refuzul constituie o sfidare a mandatului judiciar.", 
        "q": "De ce expertul nu a prezentat varianta tehnică ce transpune riguros Planul Parcelar pe teren?"
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
        "leg": "Art. 44 Constituție / Decizia 66/2020 ICCJ", 
        "iccj": "Decizia 66/2020 ICCJ", 
        "arg": "Expertul nu poate diminua suprafața din Titlu pentru a compensa erori tehnice. Titlul validat administrativ este intangibil.", 
        "q": "De ce s-a procedat la diminuarea suprafeței mele din Titlu, deși terenul există real în tarlă?"
    },
    {
        "id": "TRANS-1", 
        "sit": "6. TRANSLATAREA PARCELEI ȘI EFECTUL DE DOMINO", 
        "leg": "Art. 1200 Cod Civil / RIL 24/2024", 
        "iccj": "Jurisprudență RIL", 
        "arg": "Repoziționarea prin translatare ignoră Planul Parcelar și creează suprapuneri peste terți deja întabulați.", 
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
        "arg": "Conform ÎCCJ, Planul Parcelar fundamentează legalitatea amplasamentului. Expertul este OBLIGAT să respecte geometria tarlalei validate.", 
        "q": "Având în vedere Decizia 66/2020 a ÎCCJ, de ce expertul a ales să ignore configurația tarlalei stabilită prin Planul Parcelar?"
    }
]

# 4. Bara Laterală
with st.sidebar:
    st.header("📝 Detalii Memoriu")
    nr_dosar = st.text_input("Dosar nr:", value="5975/221/2018", key="dosar_input")
    instanta = st.text_input("Către:", value="Tribunalul Hunedoara", key="inst_input")
    st.divider()
    btn_generate = st.button("🚀 GENEREAZĂ WORD", use_container_width=True)
    st.button("🔄 RESETEAZĂ TOT", on_click=reset_form, use_container_width=True)

# 5. Corp Principal
st.title("⚖️ Expert Jurisprudență GeorgeAOH")
search_q = st.text_input("🔍 Filtrează spețe:", "")

selected_list = []

for item in data_points:
    # Filtrare simplă
    show_item = False
    if search_q == "":
        show_item = True
    elif search_q.lower() in item['sit'].lower() or search_q.lower() in item['leg'].lower():
        show_item = True
        
    if show_item:
        with st.container():
            col_check, col_info = st.columns([0.1, 0.9])
            with col_check:
                is_selected = st.checkbox("SEL", key=f"sel_{item['id']}")
            with col_info:
                st.markdown(f"### {item['sit']}")
                st.write(f"📖 **Temei:** {item['leg']} | 🏛️ **ICCJ:** {item['iccj']}")
                st.info(f"💡 **Argument:** {item['arg']}")
                if is_selected:
                    obs_val = st.text_area("✍️ Note specifice:", key=f"obs_{item['id']}", placeholder="Detalii speță...")
                    # Salvăm selecția într-un mod sigur
                    selected_list.append({
                        "sit": item['sit'],
                        "leg": item['leg'],
                        "iccj": item['iccj'],
                        "arg": item['arg'],
                        "q": item['q'],
                        "note": obs_val
                    })
            st.divider()

# 6. Funcție Word
if btn_generate:
    if selected_list:
        doc = Document()
        p = doc.add_paragraph()
        run = p.add_run(f"CĂTRE: {instanta}\nDOSAR NR: {nr_dosar}")
        run.bold, run.font.size = True, Pt(12)
        p.alignment = 2
        doc.add_heading('OBIECTIUNI LA RAPORTUL DE EXPERTIZĂ', 0).alignment = 1

        for s in selected_list:
            h = doc.add_paragraph()
            r_h = h.add_run(s['sit'].upper())
            r_h.bold, r_h.underline, r_h.font.size = True, True, Pt(14)
            doc.add_paragraph(f"Temei Legal: {s['leg']} | {s['iccj']}").italic = True
            
            arg_p = doc.add_paragraph()
            arg_p.add_run("ARGUMENT JURIDIC: ").bold = True
            arg_p.add_run(s['arg'])

            if s['note']:
                obs_p = doc.add_paragraph()
                obs_p.add_run(f"SITUAȚIA DE FAPT: {s['note']}").bold = True

            q_p = doc.add_paragraph(style='List Number')
            r_q = q_p.add_run(s['q'])
            r_q.bold, r_q.underline = True, True

        doc.add_paragraph("\n")
        sanc = doc.add_paragraph()
        run_s = sanc.add_run("SOLICITARE FINALĂ: În temeiul Art. 187 C.pc., solicităm AMENDAREA EXPERTULUI pentru nerespectarea mandatului (Obiectivul nr. 1) și a Autorității de Lucru Judecat (S. 832/2000).")
        run_s.bold, run_s.underline = True, True

        bio = io.BytesIO(); doc.save(bio); bio.seek(0)
        st.sidebar.download_button("📥 DESCARCĂ DOCUMENTUL", bio, f"Obiectiuni_{nr_dosar.replace('/','_')}.docx", use_container_width=True)
    else:
        st.sidebar.error("⚠️ Bifează punctele!")
