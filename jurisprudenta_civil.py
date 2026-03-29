import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Pt
import io
import datetime

# 1. Configurare Pagină
st.set_page_config(page_title="Expert Jurisprudență GeorgeAOH", layout="wide")

# 2. Baza de date pentru funcția de Căutare AI (Sidebar)
biblioteca_ai = {
    "plan parcelar": "Decizia 27/2022 ÎCCJ: Planul Parcelar este act de autoritate. Expertul NU îl poate modifica sau diminua suprafețele din Titlu.",
    "revendicare": "Decizia RIL 53/2007: Revendicarea (S. 832/2000) are prioritate față de Grănițuirea (S. 1500/2001). Grănițuirea nu creează proprietate.",
    "dn7": "Limita DN7 este punct FIX de hotar. Excedentul de 49 mp măsurat în teren trebuie să asigure integritatea tuturor Titlurilor din zonă.",
    "49 mp": "Excedentul de 49 mp demonstrează că nu există 'lipsă de teren'. Diminuarea suprafețelor este deci un abuz tehnic.",
    "translatare": "Translatarea peste vecini (Top 2) încalcă stabilitatea tarlalei și a generat intervenția terților în apel.",
    "amenda": "Art. 187 C.pc.: Permite amendarea expertului pentru nerespectarea mandatului (Obiectiv nr. 1)."
}

# 3. Cele 8 Bife Juridice (Actualizate)
data_points = [
    {"id": "RIL-53", "sit": "1. PRIORITATEA REVENDICĂRII (RIL 53/2007)", "leg": "Decizia RIL 53/2007 / S. 832/2000", "arg": "Grănițuirea pârâtului nu poate înfrânge Revendicarea mea irevocabilă.", "q": "Cum justificați prioritizarea grănițuirii în fața revendicării?"},
    {"id": "DEC-27", "sit": "2. INTANGIBILITATEA PLANULUI PARCELAR", "leg": "Decizia 27/2022 ÎCCJ / Art. 27 L. 18", "arg": "Expertul nu poate diminua suprafețele din Titluri pe cale incidentală.", "q": "În ce bază legală ați diminuat suprafețele din Titluri?"},
    {"id": "DN7-49", "sit": "3. LIMITA DN7 ȘI EXCEDENTUL DE 49 MP", "leg": "Realitatea Terenului / Proba Tehnică", "arg": "Există excedent de teren în zonă, deci diminuarea este nejustificată.", "q": "Unde se regăsește faptic excedentul de 49 mp măsurat de dvs.?"},
    {"id": "TRANS", "sit": "4. TRANSLATARE NELEGALĂ PESTE TOP 2", "leg": "Intervenția Vecinilor / Art. 1200 C.civ.", "arg": "Mutarea parcelelor peste vecini încalcă stabilitatea tarlalei.", "q": "De ce ați creat o nouă suprapunere peste intervenienți?"},
    {"id": "DIM-4", "sit": "5. DIMINUAREA TOP 4 (932 MP SUPRAPUNERE)", "leg": "Art. 44 Constituție / S. 832/2000", "arg": "Top 4 are 2131 mp și conține revendicarea; diminuarea este nelegală.", "q": "De ce diminuați Top 4 dacă în teren există excedent?"},
    {"id": "MARIRE-19", "sit": "6. MĂRIREA VECINULUI CU 19%", "leg": "Frauda la Lege / Art. 27 L. 18", "arg": "Expertul 'legalizează' ocuparea nelegală a pârâtului.", "q": "Care e baza legală pentru plusul de 19% al pârâtului?"},
    {"id": "CALCUL", "sit": "7. CRITICA METODEI DE CALCUL (L x h)", "leg": "Tabelul de Calcul L. 18 / Geometrie", "arg": "Expertul ignoră perpendicularitatea (înălțimea) din fișa de calcul.", "q": "De ce ignorați metoda de calcul care a fundamentat Titlurile?"},
    {"id": "AMENDA", "sit": "8. SOLICITARE AMENDĂ (ART. 187 C.PC.)", "leg": "Art. 187 C.pc. / Nerespectare Mandat", "arg": "Expertul refuză sistematic Obiectivul nr. 1 stabilit de instanță.", "q": "Solicităm amendarea expertului pentru sfidarea mandatului."}
]

# 4. Bara Laterală
with st.sidebar:
    st.header("📝 Detalii Dosar")
    nr_dosar = st.text_input("Dosar nr:", value="5975/221/2018")
    termen_jud = st.date_input("📅 Termen:", value=datetime.date(2026, 4, 14))
    
    st.divider()
    st.subheader("🔎 CĂUTARE JURISPRUDENȚĂ AI")
    query_ai = st.text_input("Caută (ex: dn7, 49 mp, plan):").lower()
    if query_ai:
        found = False
        for k, v in biblioteca_ai.items():
            if k in query_ai:
                st.success(f"**Rezultat:** {v}")
                found = True
        if not found: st.warning("Nu am găsit. Încearcă 'dn7' sau 'plan'.")

    st.divider()
    btn_word = st.button("🚀 GENEREAZĂ WORD")

# 5. Corp Principal
st.title("⚖️ Expert Jurisprudență GeorgeAOH")

# Tabel Editabil
st.subheader("📊 Situația celor 6 Parcele")
df_init = pd.DataFrame({
    "Nr. Parcela": ["Top 1", "Top 2", "Top 3", "Top 4 (2131mp)", "Top 5", "Top 6/1"],
    "Titlu (mp)": [0.0, 0.0, 0.0, 2131.0, 0.0, 0.0],
    "Expert (mp)": [0.0, 0.0, 0.0, 2082.0, 0.0, 0.0]
})
edited_df = st.data_editor(df_init, use_container_width=True)

st.divider()
st.subheader("🔍 Selectează Argumentele (Bife):")
selected_points = []
for item in data_points:
    if st.checkbox(item['sit'], key=item['id']):
        selected_points.append(item)

# 6. Generare Word (Corectată)
if btn_word:
    if not selected_points:
        st.error("⚠️ Selectează cel puțin o bifă!")
    else:
        doc = Document()
        # Antet
        antet = doc.add_paragraph()
        antet.add_run(f"DOSAR NR: {nr_dosar}\nTERMEN: {termen_jud.strftime('%d.%m.%Y')}").bold = True
        antet.alignment = 2

        doc.add_heading('OBIECTIUNI LA RĂSPUNSUL LA OBIECTIUNI NR. 6', 0).alignment = 1

        # Tabel
        doc.add_heading('SITUAȚIA COMPARATIVĂ A SUPRAFEȚELOR', level=1)
        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        h_cells = table.rows[0].cells
        h_cells[0].text, h_cells[1].text, h_cells[2].text = 'Nr. Parcela', 'Titlu (mp)', 'Expert (mp)'

        for _, row in edited_df.iterrows():
            r_cells = table.add_row().cells
            r_cells[0].text, r_cells[1].text, r_cells[2].text = str(row[0]), str(row[1]), str(row[2])

        # Argumente
        for s in selected_points:
            doc.add_heading(s['sit'], level=2)
            doc.add_paragraph(f"Temei: {s['leg']}").italic = True
            doc.add_paragraph(f"Argument: {s['arg']}")
            p_q = doc.add_paragraph()
            p_q.add_run(f"SOLICITARE/ÎNTREBARE: {s['q']}").bold = True

        bio = io.BytesIO(); doc.save(bio); bio.seek(0)
        st.sidebar.download_button("📥 DESCARCĂ DOCUMENTUL", bio, "Obiectiuni_Final.docx", use_container_width=True)
        st.success("✅ Document pregătit în sidebar!")
