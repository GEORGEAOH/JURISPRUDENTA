import streamlit as st
import pandas as pd
from docx import Document
import io

# Configurare pagină
st.set_page_config(page_title="Expert Jurisprudență", page_icon="⚖️", layout="wide")

# Stil pentru bife vizibile
st.markdown("""
    <style>
    .stCheckbox { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border: 2px solid #1976d2; }
    .stTextArea { margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- DATELE TALE (SPEȚELE) ---
if 'data' not in st.session_state:
    st.session_state.data = [
        {"id": "1", "sit": "Plan Parcelar validat (L.18/1991) - Intangibilitatea coteslor", "leg": "Art. 27 L.18/1991", "iccj": "RIL Dec. 24/2024", "arg": "Planul parcelar este baza legală supremă; geometria tarlalei trebuie respectată obligatoriu.", "q": "Să precizeze expertul dacă a respectat laturile din Calculul Suprafețelor?"},
        {"id": "2", "sit": "Neîndeplinirea Obiectivului nr. 1 (Mandatul Instanței)", "leg": "Art. 330 C.pc.", "iccj": "Jurisprudență ICCJ", "arg": "Expertul a ignorat dispoziția de a face repoziționarea conform Planului Parcelar, propunând variante subiective.", "q": "De ce expertul nu a prezentat varianta conform Planului Parcelar cerută de instanță?"},
        {"id": "3", "sit": "Translatare/Suprapunere peste vecini (Efect Domino)", "leg": "Art. 1200 Cod Civil", "iccj": "RIL 24/2024", "arg": "Expertul nu poate muta parcelele peste vecini legal întabulați, ignorând ordinea publică a cadastrului.", "q": "Cum justifică expertul suprapunerea peste terți întabulați în loc să respecte Planul?"},
        {"id": "4", "sit": "Excedent de teren în tarlă (Real > Scriptic)", "leg": "Art. 44 Constituție", "iccj": "Decizia 66/2020", "arg": "Existența unui excedent nu justifică diminuarea titlurilor validate. Expertul nu are dreptul să 'taie' din acte.", "q": "Dacă tarlaua are plus de teren, de ce s-a procedat la diminuarea suprafeței mele?"}
    ]

st.title("⚖️ Expert Jurisprudență Proprietate")
st.subheader("Selectați spețele pentru generarea memoriului:")

# --- BARA DE CĂUTARE ---
search_query = st.text_input("🔍 Caută speță (lasă gol pentru a vedea toată lista):", "")

# --- FILTRARE ȘI AFIȘARE LISTĂ ---
df = pd.DataFrame(st.session_state.data)
# Dacă bara e goală, arată tot. Dacă are text, filtrează.
if search_query:
    filtered_df = df[df.apply(lambda row: search_query.lower() in row.astype(str).str.lower().values, axis=1)]
else:
    filtered_df = df

selectii = []

# AFIȘARE SPEȚE UNA SUB ALTA
for index, row in filtered_df.iterrows():
    with st.container():
        # Bifa este acum mare și vizibilă
        ales = st.checkbox(f"✅ INCLUDE: {row['sit']}", key=f"ch_{row['id']}")
        
        # Detalii speță
        st.write(f"📖 **Lege:** {row['leg']} | 🏛️ **ICCJ/RIL:** {row['iccj']}")
        st.write(f"💡 **Sinteză:** {row['arg']}")
        
        if ales:
            # Apare caseta de text doar dacă bifezi
            comentariu = st.text_area(f"✍️ Detalii pentru {row['sit']}:", placeholder="Scrie aici observația ta...", key=f"obs_{row['id']}")
            selectii.append({**row.to_dict(), "obs": comentariu})
        st.divider()

# --- SIDEBAR ȘI GENERARE ---
with st.sidebar:
    st.header("📝 Finalizare")
    nr_dosar = st.text_input("Dosar nr:", "5975/221/2018")
    
    if st.button("🚀 GENEREAZĂ WORD"):
        if selectii:
            doc = Document()
            doc.add_heading(f'Obiecțiuni Dosar {nr_dosar}', 0)
            for s in selectii:
                doc.add_heading(s['sit'], level=1)
                doc.add_paragraph(f"Temei: {s['leg']} | {s['iccj']}").italic = True
                doc.add_paragraph(f"Sinteză: {s['arg']}")
                if s['obs']: doc.add_paragraph(f"Obs: {s['obs']}").bold = True
                doc.add_paragraph(f"Întrebare: {s['q']}", style='List Number')
            
            bio = io.BytesIO(); doc.save(bio); bio.seek(0)
            st.download_button("📥 DESCARCĂ ACUM", bio, "Memoriu.docx")
        else:
            st.error("⚠️ Bifează cel puțin o opțiune din listă!")

    if st.button("🔄 RESETEAZĂ TOT"):
        st.rerun()
