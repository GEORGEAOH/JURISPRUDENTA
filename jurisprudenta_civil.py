import streamlit as st
from docx import Document
import io

# Configurare pagină
st.set_page_config(page_title="Expert Jurisprudență", page_icon="⚖️")

st.title("⚖️ Asistent Jurisprudență ICCJ")
st.sidebar.header("📝 Detalii Document")

# Câmpuri antet
nr_dosar = st.sidebar.text_input("Număr Dosar:", placeholder="ex: 1234/1/2024")
termen = st.sidebar.text_input("Termen Judecată:", placeholder="ex: 15.05.2024")
instanta = st.sidebar.text_input("Către (Instanța/Organul):", placeholder="ex: Tribunalul Hunedoara")

st.subheader("Bifează situațiile specifice speței tale:")

# Baza de date completă (v1.3)
baza_date = {
    "1": {"sit": "Titlu de Proprietate și Plan Parcelar validat (L18/1991)", "leg": "Art. 27 L.18/1991", "iccj": "Decizia 24/2024 (RIL)", "arg": "Planul parcelar este suprem; expertiza trebuie să i se subordoneze conform Deciziei 66/2020 a ICCJ."},
    "2": {"sit": "Revendicare irevocabilă vs. Grănițuire ulterioară contrară", "leg": "Art. 431 C.pc.", "iccj": "Decizia 12/2015 (RIL)", "arg": "Revendicarea are autoritate de lucru judecat; grănițuirea nu o poate infirma."},
    "4": {"sit": "Repoziționare contrară Planului Parcelar (Principiul Imuabilității)", "leg": "Art. 27 L.18/1991; Art. 914 Cod Civil", "iccj": "Decizia 66/2020 și Decizia 24/2024", "arg": "Expertul nu poate transla parcelele contrar tarlalei validate. O repoziționare care 'împinge' limitele pe latura opusă este nulă, planul parcelar fiind act administrativ obligatoriu."},
    "7": {"sit": "Construcție ridicată ÎN TIMPUL procesului (Rea-credință)", "leg": "Art. 582 Cod Civil", "iccj": "Decizia 355/2025", "arg": "Edificarea pe teren litigios (res litigiosa) confirmă reaua-credință. Sancțiunea: Demolarea."},
    "8": {"sit": "Diminuarea suprafeței de către expert (deși terenul există)", "leg": "Art. 44 Constituție; Art. 27 L.18/1991", "iccj": "Decizia 66/2020 (RIL)", "arg": "Expertul nu poate cenzura Titlul de Proprietate. Dacă măsurătoarea reală confirmă suprafața, diminuarea scriptică este un exces de putere; expertiza trebuie să respecte întinderea dreptului înscris în Titlu."},
    "9": {"sit": "Obligarea expertului la respectarea procedurii L.18/1991", "leg": "Art. 330 C.pc.; Art. 27 L.18/1991", "iccj": "Decizia 66/2020 (RIL)", "arg": "Expertul are obligația legală de a subordona constatările tehnice configurației juridice stabilite prin Planul Parcelar și Titlul de Proprietate validate în procedura specială a Legii 18/1991. Orice deviere constituie o depășire a atribuțiilor tehnice."}
}

selectii = []
for cheie, info in baza_date.items():
    if st.checkbox(info['sit'], key=f"chk_{cheie}"):
        selectii.append(info)

def generate_docx(date_selectate, d_nr, d_t, d_inst):
    doc = Document()
    header = doc.add_paragraph()
    header.alignment = 2
    if d_inst: header.add_run(f"CĂTRE: {d_inst}\n").bold = True
    if d_nr: header.add_run(f"DOSAR NR: {d_nr}\n")
    if d_t: header.add_run(f"TERMEN: {d_t}")

    doc.add_heading('\nMEMORIU ȘI OBIECȚIUNI LA EXPERTIZA TEHNICĂ', 0).alignment = 1

    doc.add_paragraph("\nÎn susținerea poziției procesuale, solicităm instanței să pună în vedere expertului obligația de a respecta actele de proprietate validate, invocând următoarele argumente:\n")

    for item in date_selectate:
        p = doc.add_paragraph()
        p.add_run(f"PUNCTUL: {item['sit'].upper()}").bold = True
        
        text_juridic = (
            f"\nTemeiul legal: {item['leg']}. În conformitate cu jurisprudența obligatorie a ICCJ ({item['iccj']}), "
            f"statuăm faptul că: „{item['arg']}”"
        )
        arg_p = doc.add_paragraph(text_juridic)
        arg_p.alignment = 3 

    doc.add_paragraph("\nCONCLUZIE: Solicităm refacerea raportului de expertiză/răspunsul la obiecțiuni prin raportare strictă la Planul Parcelar și Titlul de Proprietate, sub sancțiunea nulității.")
    doc.add_paragraph("\nCu stimă,\n_________________").alignment = 2
    
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio

if st.button("🚀 GENEREAZĂ SINTEZA ȘI OBIECȚIUNILE"):
    if not selectii:
        st.warning("⚠️ Bifează cel puțin o variantă.")
    else:
        file_word = generate_docx(selectii, nr_dosar, termen, instanta)
        st.download_button(
            label="📥 DESCARCĂ DOCUMENTUL WORD (.DOCX)",
            data=file_word,
            file_name=f"Obiectiuni_Dosar_{nr_dosar.replace('/', '_')}.docx" if nr_dosar else "Obiectiuni_Instanta.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
        full_text = ""
        for item in selectii:
            full_text += f"OBIECTIUNE: {item['sit']}\nArgumentare: {item['arg']}\n\n"
        st.text_area("Previzualizare (Copy-Paste rapid):", full_text, height=250)

st.sidebar.info("v1.3 - Include argumente pentru forțarea expertului să respecte Planul Parcelar și Titlul de Proprietate.")
