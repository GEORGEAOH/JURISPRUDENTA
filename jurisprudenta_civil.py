import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Pt
import io
import datetime

# 1. Configurare Pagină
st.set_page_config(page_title="Expert Jurisprudență GeorgeAOH", layout="wide")

# 2. Argumente "De Fier" pentru Termenul din 14.04.2026
argumente_fundamentale = [
    {
        "id": "DN7_FIX",
        "sit": "1. FIXAREA LIMITEI LA DN7 (PARCELA 1)",
        "leg": "Art. 27 Legea 18/1991 / Plan Parcelar Validat",
        "arg": "Parcela nr. 1 se învecinează cu DN7, fiind un punct fix de hotar. Plusul de 49 mp măsurat de expert în zona primelor 6 parcele demonstrează că există suficient teren pentru respectarea tuturor Titlurilor.",
        "q": "Dacă ați măsurat un excedent de 49 mp în teren față de acte, de ce propuneți diminuarea suprafețelor (Top 1, 5, 6/1) și translatarea Top 3 și 4, în loc să respectați dimensiunile din Fișa de Calcul a Comisiei?"
    },
    {
        "id": "RIL_53",
        "sit": "2. PRIORITATEA REVENDICĂRII (RIL 53/2007)",
        "leg": "Decizia RIL 53/2007 ÎCCJ / S. 832/2000",
        "arg": "Grănițuirea vecinului (S. 1500/2001) nu poate înfrânge Revendicarea (S. 832/2000). Mărirea suprafeței pârâtului cu 19% este nelegală.",
        "q": "Cum justificați validarea unei grănițuiri care și-a mărit suprafața cu 19% prin încălcarea autorității de lucru judecat a sentinței de revendicare?"
    },
    {
        "id": "TRANSLATARE_TOP2",
        "sit": "3. TRANSLATARE NELEGALĂ PESTE TOP 2",
        "leg": "Art. 1200 C. Civ. / Intervenția vecinilor în Apel",
        "arg": "Translatarea parcelelor mele (Top 3, 4) peste parcela Top 2 a provocat intervenția vecinilor în apel. Această manevră tehnică încalcă stabilitatea întregii tarlale.",
        "q": "De ce ați creat o nouă suprapunere peste intervenienți (Top 2), ignorând geometria Tarlalei 1 stabilită prin Planul Parcelar?"
    }
]

# 3. Sidebar (Bara Laterală)
with st.sidebar:
    st.header("📝 Detalii Dosar")
    nr_dosar = st.text_input("Dosar nr:", value="5975/221/2018")
    instanta = st.text_input("Către:", value="Tribunalul Hunedoara")
    termen_jud = st.date_input("📅 Termen:", value=datetime.date(2026, 4, 14))
    
    st.divider()
    st.subheader("🔎 Căutare AI Jurisprudență")
    ai_q = st.text_input("Întreabă AI (ex: 'plan parcelar'):")
    if "plan" in ai_q.lower():
        st.success("Argument: Decizia 27/2022 ÎCCJ obligă expertul să respecte geometria tarlalei validate.")

    st.divider()
    btn_gen = st.button("🚀 GENEREAZĂ OBIECȚIUNI WORD", use_container_width=True)

# 4. Corp Principal
st.title("⚖️ Expert Jurisprudență GeorgeAOH")
st.subheader(f"Obiecțiuni Răspuns nr. 6 | Simeria Sântandrei | Termen: {termen_jud.strftime('%d.%m.%Y')}")

# Tabel Comparativ Editabil
st.markdown("### 📊 Analiză Suprafață: Titlu vs. Propunere Expert")
df_init = pd.DataFrame({
    "Nr. Parcela": ["Top 1 (Lângă DN7)", "Top 2 (Intervenient)", "Top 3 (Reclamant)", "Top 4 (932mp suprap.)", "Top 5", "Top 6/1"],
    "Suprafata Titlu (mp)": [0.0, 0.0, 0.0, 2131.0, 0.0, 0.0],
    "Suprafata Expert (mp)": [0.0, 0.0, 0.0, 2142.0, 0.0, 0.0],
    "Observații": ["DN7 - Punct Fix", "Translatare Nelegală", "Diminuată", "Mărită artificial (+11mp)", "Diminuată", "Diminuată"]
})
edited_df = st.data_editor(df_init, use_container_width=True)

st.divider()
st.subheader("🔍 Selectează argumentele pentru Nota de Ședință:")

selected_points = []
for item in argumente_fundamentale:
    if st.checkbox(item['sit'], key=item['id']):
        selected_points.append(item)

# 5. Generare Document Word
if btn_gen:
    if not selected_points:
        st.error("⚠️ Selectează cel puțin un argument!")
    else:
        doc = Document()
        p = doc.add_paragraph()
        p.add_run(f"CĂTRE: {instanta}\nDOSAR NR: {nr_dosar}\nTERMEN: {termen_jud.strftime('%d.%m.%Y')}").bold = True
        p.alignment = 2
        doc.add_heading('OBIECTIUNI LA RĂSPUNSUL LA OBIECTIUNI NR. 6', 0).alignment = 1

        # Secțiunea Specială: DN7 și excedentul de 49mp
        doc.add_heading('1. ANALIZA TEHNICĂ: LIMITA DN7 ȘI EXCEDENTUL DE 49 MP', level=1)
        doc.add_paragraph(
            "Expertul omite un fapt esențial: parcela nr. 1 se învecinează cu drumul național DN7, constituind un punct fix de hotar. "
            "Prin propriile măsurători, expertul a identificat un EXCEDENT de 49 mp în zona primelor 6 parcele. "
            "În aceste condiții, diminuarea suprafețelor din Titlu și translatarea parcelelor peste Top 2 (care a generat intervenția vecinilor în apel) "
            "reprezintă o eroare metodologică voită, menită să favorizeze pârâtul în detrimentul realității juridice a Planului Parcelar."
        )

        # Argumentele selectate
        for s in selected_points:
            doc.add_heading(s['sit'], level=2)
            doc.add_paragraph(f"Temei: {s['leg']}").italic = True
            doc.add_paragraph(f"Argument juridic: {s['arg']}")
            doc.add_paragraph(f"ÎNTREBARE PENTRU EXPERT: {s['q']}").bold = True

        # Tabelul în Word
        doc.add_heading('SITUAȚIA COMPARATIVĂ A SUPRAFEȚELOR', level=1)
        table = doc.add_table(rows=1, cols=3)
        table.rows.cells[0].text = 'Nr. Parcela'
        table.rows.cells[1].text = 'Suprafață Titlu (mp)'
        table.rows.cells[2].text = 'Suprafață Expert (mp)'
        for _, row in edited_df.iterrows():
            row_cells = table.add_row().cells
            row_cells.text, row_cells.text, row_cells.text = str(row[0]), str(row[1]), str(row[2])

        doc.add_paragraph("\nSOLICITĂM: Respingerea raportului, refacerea acestuia fără translatări și amendarea expertului (Art. 187 C.pc.).")

        bio = io.BytesIO(); doc.save(bio); bio.seek(0)
        st.sidebar.download_button("📥 DESCARCĂ MEMORIUL", bio, f"Obiectiuni_GeorgeAOH_Final.docx")
        st.success("✅ Documentul a fost generat cu argumentul DN7 și excedentul de 49mp!")
