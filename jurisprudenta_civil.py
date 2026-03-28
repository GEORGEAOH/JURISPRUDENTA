import streamlit as st
from docx import Document
import io

# Configurare pagină
st.set_page_config(page_title="Expert Jurisprudență Civilă", page_icon="⚖️")

st.title("⚖️ Asistent Jurisprudență ICCJ")
st.markdown("---")
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

st.markdown("---")

# Funcție pentru crearea fișierului Word
def generate_docx(date_selectate):
    doc = Document()
    doc.add_heading('SINTEZĂ JURISPRUDENȚĂ ȘI ARGUMENTARE JURIDICĂ', 0)
    
    for item in date_selectate:
        doc.add_heading(item['sit'], level=1)
        doc.add_paragraph(f"Temei Legal: {item['leg']}", style='List Bullet')
        doc.add_paragraph(f"Jurisprudență ICCJ: {item['iccj']}", style='List Bullet')
        p = doc.add_paragraph()
        p.add_run(f"Argumentare: {item['arg']}").bold = True
        doc.add_paragraph("-" * 20)
    
    doc.add_paragraph("\nGenerat automat de Asistentul LegalTech.")
    
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio

# Buton Generare și Descărcare
if st.button("🚀 GENEREAZĂ SINTEZA PENTRU INSTANȚĂ"):
    if not selectii:
        st.warning("⚠️ Te rugăm să bifezi cel puțin o variantă de mai sus.")
    else:
        st.success("Sinteză generată! Poți vizualiza mai jos sau descărca fișierul Word.")
        
        # Generăm conținutul pentru Word
        file_word = generate_docx(selectii)
        
        st.download_button(
            label="📥 DESCARCĂ NOTELE ÎN FORMAT WORD (.DOCX)",
            data=file_word,
            file_name="Argumente_Instanta.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
        # Afișare pe ecran
        for item in selectii:
            with st.expander(f"📍 {item['sit']}", expanded=True):
                st.write(f"**⚖️ Temei Legal:** {item['leg']}")
                st.write(f"**🏛️ Jurisprudență ICCJ:** `{item['iccj']}`")
                st.info(f"**✍️ Argument:** {item['arg']}")

st.sidebar.info("Aplicație creată pentru suport juridic rapid. Include deciziile ICCJ 2024-2025.")
