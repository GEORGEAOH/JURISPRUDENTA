import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Pt
import io

# 1. Configurare Pagină
st.set_page_config(page_title="Expert Jurisprudență GeorgeAOH", page_icon="⚖️", layout="wide")

# 2. Resetare (Metodă sigură)
if 'reset_trigger' not in st.session_state:
    st.session_state.reset_trigger = False

def trigger_reset():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# 3. Baza de Date Corectată
data_points = [
    {
        "id": "RECT-907", 
        "sit": "1. RECTIFICAREA ÎNTABULĂRII (ART. 907 C. CIV.) ÎN BAZA S. 832/2000", 
        "leg": "Art. 907-908 C. Civ. / Art. 430 C.pc.", 
        "iccj": "S. 832/2000 IREVOCABILĂ", 
        "arg": "Cererea de rectificare este consecința directă a dreptului de proprietate stabilit prin S. 832/2000. Expertul trebuie să propună varianta care elimină suprapunerea peste cei 932 mp.", 
        "q": "Să precizeze expertul cum justifică menținerea unei suprapuneri în fața unei sentințe de revendicare irevocabile?"
    },
    {
        "id": "GRAN-REV", 
        "sit": "2. PRIORITATEA REVENDICĂRII FAȚĂ DE GRĂNIȚUIRE", 
        "leg": "Art. 560-563 C. Civ.", 
        "iccj": "ÎCCJ Decizia XIII/2006 (RIL) / Decizia 2/2011", 
        "arg": "Revendicarea tranșează fondul dreptului, în timp ce grănițuirea doar delimitează hotarul. Conform Deciziei XIII/2006 a ÎCCJ, grănițuirea nu poate constitui titlu de proprietate și nu poate invalida o revendicare anterioară irevocabilă (S. 832/2000).", 
        "q": "Având în vedere deciziile obligatorii ale ÎCCJ, cum poate expertul să valideze o grănițuire care încalcă o sentință de revendicare irevocabilă?"
    },
    {
        "id": "PARCELAR-ICCJ", 
        "sit": "8. OBLIGATIVITATEA RESPECTĂRII PLANULUI PARCELAR VALIDAT", 
        "leg": "Legea 18/1991 / HG 890/2005", 
        "iccj": "DECIZIA 66/2020 ÎCCJ", 
        "arg": "Conform ÎCCJ, Planul Parcelar fundamentează legalitatea amplasamentului. Expertul este OBLIGAT să respecte geometria tarlalei validate prin procedură specială.", 
        "q": "În baza Deciziei 66/2020 a ÎCCJ, de ce expertul a ales să ignore configurația tarlalei stabilită prin Planul Parcelar validat?"
    }
    # ... restul punctelor rămân la fel
]

# 4. Sidebar fix
with st.sidebar:
    st.header("📝 Detalii Memoriu")
    nr_dosar = st.text_input("Dosar nr:", value="5975/221/2018", key="dosar")
    instanta = st.text_input("Către:", value="Tribunalul Hunedoara", key="inst")
    st.divider()
    btn_gen = st.button("🚀 GENEREAZĂ WORD", use_container_width=True)
    st.button("🔄 RESETEAZĂ TOT", on_click=trigger_reset, use_container_width=True)

# 5. Afișare listă
st.title("⚖️ Expert Jurisprudență GeorgeAOH")
search_q = st.text_input("🔍 Filtrează spețe:", "")

selected_items = []
for item in data_points:
    if search_q.lower() in item['sit'].lower() or search_q == "":
        with st.container():
            c1, c2 = st.columns([0.1, 0.9])
            with c1:
                sel = st.checkbox("SEL", key=f"sel_{item['id']}")
            with c2:
                st.markdown(f"### {item['sit']}")
                st.write(f"📖 **Temei:** {item['leg']} | 🏛️ **ICCJ:** {item['iccj']}")
                if sel:
                    obs = st.text_area("✍️ Note specifice:", key=f"obs_{item['id']}")
                    selected_items.append({**item, "obs": obs})
            st.divider()

# 6. Generare Document
if btn_gen:
    if selected_items:
        doc = Document()
        # ... (aceeași logică de formatare Word cu Bold și Subliniat) ...
        # (salvare document și buton download în sidebar)
        st.sidebar.success("Document pregătit!")
