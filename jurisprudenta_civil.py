import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Pt
import io

# Configurare aplicație GeorgeAOH
st.set_page_config(page_title="Expert Jurisprudență Proprietate", page_icon="⚖️", layout="wide")

# Verificarea Datelor de Bază (Nucleul Speței)
if 'data' not in st.session_state:
    st.session_state.data = [
        {
            "id": "REV-832", 
            "sit": "1. AUTORITATEA DE LUCRU JUDECAT - SENTINȚA NR. 832/2000", 
            "leg": "Art. 430 C.pc. / Art. 287 Cod Penal", 
            "iccj": "Jurisprudență CEDO (Dreptul la executare)", 
            "arg": "Sentința 832/2000 (irevocabilă) a stabilit obligația lăsării în deplină proprietate și posesie a suprafeței de 932 mp. Aceasta are la bază Planul Parcelar, Titlul L.18 și Procesul Verbal de Punere în Posesie. Expertul NU poate propune variante care anulează folosința stabilită prin judecată.",
            "q": "Să precizeze expertul de ce ignoră suprafața de 932 mp soluționată irevocabil, propunând o variantă care încalcă autoritatea de lucru judecat a Sentinței 832/2000?"
        },
        {
            "id": "OBJ-1", 
            "sit": "2. NERESPECTAREA MANDATULUI INSTANȚEI (OBIECTIVUL NR. 1)", 
            "leg": "Art. 330 C.pc. / Art. 187 C.pc.", 
            "iccj": "Decizia 66/2020 ICCJ (Plan Parcelar Obligatoriu)", 
            "arg": "Expertul a ignorat dispoziția expresă de a prezenta repoziționarea conform Planului Parcelar validat (Obiectivul nr. 1). Refuzul răspunsului tehnic la acest obiectiv constituie o sfidare a mandatului judiciar.",
            "q": "De ce expertul nu a prezentat varianta tehnică ce transpune riguros Planul Parcelar pe teren, așa cum s-a dispus prin Obiectivul nr. 1?"
        },
        {
            "id": "MAR-19", 
            "sit": "3. MĂRIREA NELEGALĂ A SUPRAFEȚEI VECINULUI CU 19%", 
            "leg": "Legea 18/1991 / Art. 583 Cod Civil", 
            "iccj": "Principiul intangibilității Titlului L.18", 
            "arg": "Vecinul și-a mărit suprafața cu 19% față de actul de cumpărare și Titlul L.18, fără nicio procedură legală de rectificare. Expertul nu are autoritatea să 'legalizeze' o ocupare de fapt în detrimentul unui titlu validat.",
            "q": "Să indice expertul temeiul legal prin care a validat o suprafață cu 19% mai mare pentru vecin, în condițiile în care acesta nu deține un Titlu modificat conform Legii 18/1991?"
        }
    ]

st.title("⚖️ Expert Jurisprudență - Sinteză Finală (GeorgeAOH)")
st.info("Format optimizat: Font 12pt, Titluri 14pt, BOLD și SUBLINIAT.")

# Interfața de selecție
search_query = st.text_input("🔍 Filtrează spețe:", "")
df = pd.DataFrame(st.session_state.data)
filtered_df = df[df.apply(lambda row: search_query.lower() in row.astype(str).str.lower().values, axis=1)] if search_query else df

selectii = []
for index, row in filtered_df.iterrows():
    with st.container():
        col_bifa, col_text = st.columns([0.1, 0.9])
        with col_bifa:
            ales = st.checkbox("SELECT", key=f"ch_{row['id']}")
        with col_text:
            st.markdown(f"### {row['sit']}")
            st.write(f"📖 **Temei:** {row['leg']} | 🏛️ **ICCJ:** {row['iccj']}")
            if ales:
                obs = st.text_area(f"✍️ Note specifice:", placeholder="Detalii speță...", key=f"obs_{row['id']}")
                selectii.append({**row.to_dict(), "obs": obs})
        st.divider()

# Generare Document
with st.sidebar:
    st.header("📝 Detalii Dosar")
    nr_dosar = st.text_input("Dosar nr:", "5975/221/2018")
    instanta = st.text_input("Către:", "Tribunalul Hunedoara")
    
    if st.button("🚀 GENEREAZĂ OBIECȚIUNILE FINALE"):
        if selectii:
            doc = Document()
            # Antet
            p_antet = doc.add_paragraph()
            run_antet = p_antet.add_run(f"CĂTRE: {instanta}\nDOSAR NR: {nr_dosar}")
            run_antet.bold = True
            run_antet.font.size = Pt(12)
            p_antet.alignment = 2

            title = doc.add_heading('OBIECTIUNI LA RAPORTUL DE EXPERTIZĂ', 0)
            title.alignment = 1

            for s in selectii:
                # Titlu Secțiune: 14pt, BOLD + SUBLINIAT
                h = doc.add_paragraph()
                run_h = h.add_run(s['sit'].upper())
                run_h.bold = True
                run_h.underline = True
                run_h.font.size = Pt(14)

                p_leg = doc.add_paragraph()
                run_leg = p_leg.add_run(f"Temei Legal: {s['leg']} | {s['iccj']}")
                run_leg.italic = True
                run_leg.font.size = Pt(12)
                
                arg_p = doc.add_paragraph()
                run_arg_title = arg_p.add_run("ARGUMENT JURIDIC: ")
                run_arg_title.bold = True
                run_arg_title.font.size = Pt(12)
                run_arg_text = arg_p.add_run(s['arg'])
                run_arg_text.font.size = Pt(12)

                if s['obs']:
                    obs_p = doc.add_paragraph()
                    run_obs = obs_p.add_run(f"SITUAȚIA DE FAPT: {s['obs']}")
                    run_obs.bold = True
                    run_obs.font.size = Pt(12)

                # Întrebarea: BOLD + SUBLINIAT
                q_p = doc.add_paragraph(style='List Number')
                run_q = q_p.add_run(s['q'])
                run_q.bold = True
                run_q.underline = True
                run_q.font.size = Pt(12)

            # Solicitarea finală
            doc.add_paragraph("\n")
            sanc = doc.add_paragraph()
            run_s = sanc.add_run("SOLICITARE FINALĂ: În temeiul Art. 187 C.pc., solicităm AMENDAREA EXPERTULUI pentru nerespectarea obiectivelor dispuse și a Autorității de Lucru Judecat.")
            run_s.bold = True
            run_s.underline = True
            run_s.font.size = Pt(12)

            bio = io.BytesIO(); doc.save(bio); bio.seek(0)
            st.download_button("📥 DESCARCĂ PENTRU E-MAIL", bio, f"Obiectiuni_Finale_{nr_dosar.replace('/','_')}.docx")
        else:
            st.error("Bifează punctele de susținut!")
    
    if st.button("🔄 RESET"):
        st.rerun()
