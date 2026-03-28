import streamlit as st
from docx import Document
from docx.shared import Pt
import io

# Configurare pagină
st.set_page_config(page_title="Expert Jurisprudență", page_icon="⚖️")

st.title("⚖️ Asistent Jurisprudență ICCJ")
st.sidebar.header("📝 Detalii Document")

# Câmpuri noi pentru antet în Sidebar
nr_dosar = st.sidebar.text_input("Număr Dosar:", placeholder="ex: 1234/1/2024")
termen = st.sidebar.text_input("Termen Judecată:", placeholder="ex: 15.05.2024")
instanta = st.sidebar.text_input("Către (Instanța/Organul):", placeholder="ex: Judecătoria Sector 1")

st.subheader("Bifează situațiile specifice speței tale:")

baza_date = {
    "1": {"sit": "Titlu de Proprietate și Plan Parcelar validat (L18/1991)", "leg": "Art. 27 L.18/1991", "iccj": "Decizia 24/2024 (RIL)", "arg": "Planul parcelar este suprem; expertiza trebuie să i se subordoneze."},
    "2": {"sit": "Revendicare irevocabilă vs. Grănițuire ulterioară contrară", "leg": "Art. 431 C.pc.", "iccj": "Decizia 12/2015 (RIL)", "arg": "Revendicarea are autoritate de lucru judecat; grănițuirea nu o poate infirma."},
    "4": {"sit": "Repoziționare prin expertiză contrară Planului Parcelar", "leg": "Art. 1250 Cod Civil", "iccj": "Decizia 24/2024 (RIL)", "arg": "Expertul nu poate transla parcele creând suprapuneri noi, ignorând tarlaua."},
    "5": {"sit": "Notare 'Suprapunere Reală' în Cartea Funciară", "leg": "Art. 902 Cod Civil", "iccj": "Decizia 396/2025", "arg": "Notarea în CF înlătură buna-credință. Publicitatea imobiliară este opozabilă."},
    "6": {"sit": "Notificare prin Avocat/Executor recepționată", "leg": "Art. 1522 Cod Civil", "iccj": "Practica ICCJ", "arg": "Somația directă constituie proba absolută a relei-credințe a constructorului."},
    "7": {"sit": "Construcție ridicată ÎN TIMPUL procesului", "leg": "Art. 582 Cod Civil", "iccj": "Decizia 355/2025", "arg": "Edificarea pe teren litigios (res litigiosa) confirmă reaua-credință. Soluție: Demolare."}
}

selectii = []
for cheie, info in baza_date.items():
    if st.checkbox(info['sit'], key=f"chk_{cheie}"):
        selectii.append(info)

def generate_docx(date_selectate, d_nr, d_t, d_inst):
    doc = Document()
    # Antet Dreapta
    header = doc.add_paragraph()
    header.alignment = 2
    if d_inst: header.add_run(f"CĂTRE: {d_inst}\n").bold = True
    if d_nr: header.add_run(f"DOSAR NR: {d_nr}\n")
    if d_t: header.add_run(f"TERMEN: {d_t}")

    doc.add_heading('\nNOTĂ DE ȘEDINȚĂ / CONCLUZII', 0).alignment = 1

    for item in date_selectate:
        p = doc.add_paragraph()
        p.add_run(f"\nREFERITOR LA: {item['sit'].upper()}").bold = True
        
        text_juridic = (
            f"\nSub aspectul dreptului material, temeiul legal incident este {item['leg']}. "
            f"În interpretarea și aplicarea unitară a legii, Înalta Curte de Casație și Justiție a statuat prin {item['iccj']} "
            f"cu caracter obligatoriu următoarele: \n"
            f"„{item['arg']}”"
        )
        arg_p = doc.add_paragraph(text_juridic)
        arg_p.alignment = 3 

    doc.add_paragraph("\nCu stimă,\n_________________").alignment = 2
    
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio

if st.button("🚀 GENEREAZĂ SINTEZA OFICIALĂ"):
    if not selectii:
        st.warning("⚠️ Bifează cel puțin o variantă.")
    else:
        file_word = generate_docx(selectii, nr_dosar, termen, instanta)
        st.download_button(
            label="📥 DESCARCĂ DOCUMENTUL WORD (.DOCX)",
            data=file_word,
            file_name=f"Note_Dosar_{nr_dosar.replace('/', '_')}.docx" if nr_dosar else "Note_Instanta.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        # Previzualizare rapidă pentru Copy-Paste direct de pe site
        full_text = ""
        for item in selectii:
            full_text += f"{item['sit']}\n{item['leg']} | {item['iccj']}\n{item['arg']}\n\n"
        st.text_area("Previzualizare text (pentru Copy-Paste rapid):", full_text, height=200)

st.sidebar.markdown("---")
st.sidebar.caption("v1.2 - Suport Antet Instanță")
