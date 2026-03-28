import streamlit as st
from docx import Document
import io

st.set_page_config(page_title="Expert Jurisprudență", page_icon="⚖️")
st.title("⚖️ Asistent Jurisprudență - Simeria/Sântandrei")

# Meniu Lateral
st.sidebar.header("📝 Detalii Dosar")
nr_dosar = st.sidebar.text_input("Număr Dosar:", placeholder="ex: 5975/221/2018")
termen = st.sidebar.text_input("Termen Judecată:", placeholder="ex: 14.05.2026")
instanta = st.sidebar.text_input("Către:", value="Tribunalul Hunedoara")

st.subheader("Selectați situațiile din speță:")

baza_date = {
    "1": {"sit": "Titlu și Plan Parcelar validat (L.18/1991)", "leg": "Art. 27 L.18/1991", "iccj": "Decizia 24/2024 (RIL)", "arg": "Planul parcelar este baza legală supremă; expertiza trebuie să respecte geometria tarlalei validate."},
    "4": {"sit": "Repoziționare contrară Tarlalei (Suprapunere vecin)", "leg": "Decizia 66/2020 ICCJ", "iccj": "RIL 24/2024", "arg": "Expertul nu poate translata parcelele. O eroare la un vecin nu permite 'împingerea' hotarelor peste mine."},
    "8": {"sit": "Diminuarea suprafeței de către expert", "leg": "Art. 44 Constituție", "iccj": "Decizia 66/2020", "arg": "Expertul nu poate cenzura Titlul. Dacă terenul există real, diminuarea scriptică este un exces de putere."},
    "9": {"sit": "Obligarea expertului la respectarea actelor", "leg": "Art. 330 C.pc.", "iccj": "Practica ICCJ", "arg": "Expertul trebuie să se subordoneze actelor administrative validate (Titlu, Plan Parcelar)."},
    "10": {"sit": "Nerespectarea limitelor din Actul Notarial (Cumpărare subsecventă)", "leg": "Art. 1270 Cod Civil", "iccj": "Principiul Nemo plus iuris", "arg": "Vecinul a cumpărat o suprafață fixă din Titlu. Extinderea peste această limită încalcă propriul său act de achiziție și denotă rea-credință."}
}

selectii = [info for ch, info in baza_date.items() if st.checkbox(info['sit'], key=f"chk_{ch}")]

def generate_docx(date_selectate, d_nr, d_t, d_inst):
    doc = Document()
    header = doc.add_paragraph()
    header.alignment = 2
    if d_inst: header.add_run(f"CĂTRE: {d_inst}\n").bold = True
    if d_nr: header.add_run(f"DOSAR NR: {d_nr}\n")
    if d_t: header.add_run(f"TERMEN: {d_t}")

    doc.add_heading('\nMEMORIU ȘI OBIECȚIUNI LA EXPERTIZĂ', 0).alignment = 1

    for item in date_selectate:
        p = doc.add_paragraph()
        p.add_run(f"PUNCTUL: {item['sit'].upper()}").bold = True
        doc.add_paragraph(f"Temei: {item['leg']}. ICCJ: „{item['arg']}”").alignment = 3

    doc.add_heading('\nÎNTREBĂRI PENTRU EXPERT', level=1)
    intrebari = [
        "Să precizeze expertul dacă suprafața ocupată de vecin corespunde cu suprafața din Actul său Notarial de cumpărare.",
        "Dacă suprafața reală a tarlalei permite respectarea tuturor titlurilor fără diminuări arbitrare.",
        "Să explice de ce a ignorat Planul Parcelar validat în favoarea unei repoziționări nelegale."
    ]
    for q in intrebari: doc.add_paragraph(q, style='List Number')

    doc.add_paragraph("\nCu stimă,\n_________________").alignment = 2
    bio = io.BytesIO(); doc.save(bio); bio.seek(0)
    return bio

if st.button("🚀 GENEREAZĂ SINTEZA FINALA"):
    if selectii:
        st.download_button("📥 DESCARCĂ WORD", generate_docx(selectii, nr_dosar, termen, instanta), "Sinteza_Finala_Simeria.docx")
    else: st.warning("Bifează situațiile.")
