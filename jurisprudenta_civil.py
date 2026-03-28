import streamlit as st
import pandas as pd
from docx import Document
import io

# Configurare pagină
st.set_page_config(page_title="Expert Jurisprudență Proprietate", page_icon="⚖️", layout="wide")

# Stil vizual pentru claritate
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stCheckbox { background-color: #ffffff; padding: 10px; border-radius: 5px; border: 1px solid #ddd; }
    .law-tag { color: #d32f2f; font-weight: bold; }
    .iccj-tag { color: #1976d2; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- INIȚIALIZARE STAT PENTRU RESETARE ---
if 'refresh' not in st.session_state:
    st.session_state.refresh = 0

def reset_app():
    st.session_state.refresh += 1

# --- BAZA DE DATE CONCISĂ (JURISPRUDENȚĂ ȘI RIL) ---
# Structură: Situație -> Lege -> RIL/ICCJ -> Argument -> Întrebare Expert
data = [
    {
        "id": "1", 
        "sit": "Plan Parcelar și Titlu validate prin Procedură Specială (L.18/1991)", 
        "leg": "Art. 27 alin. 1 din Legea 18/1991", 
        "iccj": "RIL Decizia 24/2024", 
        "arg": "Actele emise în procedura specială a legilor fondului funciar, necontestate, sunt intangibile. Expertiza nu poate eluda geometria tarlalei validate administrativ.",
        "q": "Să precizeze expertul dacă dimensiunile laturilor măsurate corespund cu cele din Fișa de Calcul care a fundamentat Titlul de Proprietate?"
    },
    {
        "id": "2", 
        "sit": "Neîndeplinirea Obiectivului nr. 1 (Mandatul Instanței în Apel)", 
        "leg": "Art. 330 C.pc.", 
        "iccj": "Jurisprudență Constantă ICCJ", 
        "arg": "Expertul a ignorat dispoziția expresă de a face repoziționarea conform Planului Parcelar, propunând variante subiective care eludează mandatul judiciar.", 
        "q": "De ce expertul nu a prezentat o variantă care să respecte strict Planul Parcelar validat, așa cum s-a dispus prin Obiectivul nr. 1?"
    },
    {
        "id": "3", 
        "sit": "Repoziționare/Translare contrară Planului Parcelar (Efect Domino)", 
        "leg": "Art. 1200 pct. 4 Cod Civil", 
        "iccj": "RIL Decizia 24/2024", 
        "arg": "Expertul nu poate translata parcelele peste terți legal întabulați. Orice repoziționare care ignoră Planul Parcelar generează suprapuneri ilegale.", 
        "q": "Cum justifică expertul propunerea unor variante care încalcă drepturile de proprietate ale vecinilor intervenienți, ignorând configurația legală din Planul Parcelar?"
    },
    {
        "id": "4", 
        "sit": "Excedent de teren în tarlă (Suprafață Reală > Scriptic)", 
        "leg": "Art. 44 Constituție & Art. 582 Cod Civil", 
        "iccj": "Decizia 66/2020 ICCJ", 
        "arg": "Existența unui excedent în tarlă nu justifică diminuarea titlurilor validate. Expertul nu are dreptul să 'cenzureze' suprafața din Titlu pentru a anula plusul de teren găsit.", 
        "q": "Dacă suprafața tarlalei permite satisfacerea tuturor titlurilor conform dimensiunilor lor din actele premergătoare, de ce s-a procedat la diminuarea suprafeței mele?"
    },
    {
        "id": "5", 
        "sit": "Intangibilitatea Calculului Suprafețelor (Documente Premergătoare)", 
        "leg": "Art. 11, 12 din HG 890/2005", 
        "iccj": "Securitatea Raporturilor Juridice", 
        "arg": "Dimensiunile laturilor din Fișa de Calcul anexată Titlului sunt parte integrantă a acestuia. Expertiza trebuie să se subordoneze acestor cote validate administrativ.",
        "q": "De ce expertul a ignorat dimensiunile laturilor din documentația premergătoare care a stat la baza emiterii Titlului de Proprietate?"
    }
]

# --- INTERFAȚA ---
st.title("⚖️ Expert Jurisprudență Proprietate")
st.subheader("Generator Sintetic de Obiecțiuni (Plan Parcelar & RIL)")

# Sidebar
with st.sidebar:
    st.header("📝 Identificare")
    nr_dosar = st.text_input("Dosar nr:", "5975/221/2018", key=f"dosar_{st.session_state.refresh}")
    instanta = st.text_input("Către:", "Tribunalul Hunedoara", key=f"inst_{st.session_state.refresh}")
    st.divider()
    st.button("🔄 RESETEAZĂ TOT", on_click=reset_app, use_container_width=True)

# Căutare
search_query = st.text_input("🔍 Caută (ex: 'RIL', 'Laturi', 'Obiectiv', 'Excedent'):", "", key=f"search_{st.session_state.refresh}").lower()

# Filtrare date
df = pd.DataFrame(data)
filtered_df = df[df.apply(lambda row: search_query in row.astype(str).str.lower().values, axis=1)]

# Selecție și Note
selectii = []
st.write(f"Identificate **{len(filtered_df)}** situații relevante:")

for index, row in filtered_df.iterrows():
    with st.container():
        col1, col2 = st.columns([0.05, 0.95])
        with col1:
            is_selected = st.checkbox("", key=f"ch_{row['id']}_{st.session_state.refresh}")
        with col2:
            st.markdown(f"🚩 **SITUAȚIE:** {row['sit']}")
            st.markdown(f"📖 **LEGE:** <span class='law-tag'>{row['leg']}</span> | 🏛️ **ICCJ:** <span class='iccj-tag'>{row['iccj']}</span>", unsafe_allow_html=True)
            st.markdown(f"💡 **ARGUMENT CONCIS:** {row['arg']}")
            
            if is_selected:
                obs = st.text_area("✍️ DETALII SPEȚĂ (Observația ta):", 
                                   placeholder="Descrie aici cum a ignorat expertul Planul Parcelar sau intervenția vecinilor...",
                                   key=f"obs_{row['id']}_{st.session_state.refresh}")
                selectii.append({**row.to_dict(), "obs": obs})
        st.divider()

# --- GENERARE DOCUMENT WORD ---
def create_word(data_selected, d_nr, d_inst):
    doc = Document()
    header = doc.add_paragraph()
    header.add_run(f"CĂTRE: {d_inst}\nDOSAR NR: {d_nr}").bold = True
    header.alignment = 2

    doc.add_heading('OBIECTIUNI LA RAPORTUL DE EXPERTIZĂ', 0).alignment = 1

    for s in data_selected:
        doc.add_heading(s['sit'], level=1)
        p = doc.add_paragraph()
        p.add_run(f"Temei Legal: {s['leg']} | {s['iccj']}\n").italic = True
        p.add_run(f"Sinteză Argument: {s['arg']}")
        
        if s['obs']:
            p_obs = doc.add_paragraph()
            p_obs.add_run(f"Situație concretă: {s['obs']}").bold = True
            
        doc.add_paragraph(f"Întrebare Expert: {s['q']}", style='List Number')

    doc.add_paragraph("\nCu stimă,\n_________________").alignment = 2
    bio = io.BytesIO(); doc.save(bio); bio.seek(0)
    return bio

# Buton Generare Finală
if st.button("🚀 GENEREAZĂ SINTEZA FINALA (WORD)"):
    if selectii:
        word_file = create_word(selectii, nr_dosar, instanta)
        st.download_button("📥 DESCARCĂ ACUM", word_file, f"Obiectiuni_{nr_dosar.replace('/','_')}.docx")
        st.success(f"Document generat cu {len(selectii)} puncte de jurisprudență.")
    else:
        st.error("Bifează cel puțin o situație pentru a genera documentul!")
