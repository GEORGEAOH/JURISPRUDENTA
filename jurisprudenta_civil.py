
class MotorJurisprudenta:
    def __init__(self):
        # Baza de date cu argumente, articole de lege și decizii ICCJ obligatorii
        self.baza_date = {
            "1": {
                "situatie": "Titlu de Proprietate (TP) și Plan Parcelar validat (L18/1991)",
                "lege": "Art. 27 Legea 18/1991; Art. 11 Legea 7/1996",
                "iccj": "Decizia nr. 24/2024 (RIL) - Supremația tarlalei.",
                "argument": "Planul parcelar validat este actul administrativ de autoritate care individualizează tarlaua. Orice măsurătoare privată contrară este nulă."
            },
            "2": {
                "situatie": "Revendicare irevocabilă vs. Grănițuire ulterioară contrară",
                "lege": "Art. 431 alin. (1) C.proc.civ. (Autoritatea de lucru judecat)",
                "iccj": "Decizia nr. 12/2015 (RIL); Decizia nr. 339/2024",
                "argument": "Prima hotărâre de revendicare prevalează. Grănițuirea nu poate modifica proprietatea stabilită anterior prin sentință petitorie."
            },
            "3": {
                "situatie": "Mărire de suprafață prin Grănițuire (fără titlu)",
                "lege": "Art. 560 Cod Civil; Art. 563 Cod Civil",
                "iccj": "Practica constantă ICCJ - Grănițuirea nu este mod de dobândire.",
                "argument": "Grănițuirea servește doar la marcarea hotarului. Invocarea ei pentru a mări suprafața în detrimentul vecinului revendicat este ilegală."
            },
            "4": {
                "situatie": "Repoziționare prin expertiză contrară Planului Parcelar",
                "lege": "Art. 1250 Cod Civil (Cauza ilicită); Normele tehnice ANCPI",
                "iccj": "Decizia nr. 24/2024 (RIL) - Subordonarea expertizei față de tarlă.",
                "argument": "Expertul nu poate transla o parcelă creând suprapuneri noi pe latura opusă, ignorând configurația tarlalei validate administrativ."
            },
            "5": {
                "situatie": "Notare 'Suprapunere Reală' în Cartea Funciară (CF)",
                "lege": "Art. 902 alin. (2) pct. 19 Cod Civil (Opozabilitate)",
                "iccj": "Decizia nr. 396/2025 - Efectul de informare publică.",
                "argument": "Notarea în CF înlătură buna-credință. Orice persoană care consultă CF are cunoștință de caracterul litigios al terenului."
            },
            "6": {
                "situatie": "Notificare prin Avocat/Executor recepționată de vecin",
                "lege": "Art. 1522 Cod Civil (Punerea în întârziere)",
                "iccj": "Principiul protecției proprietății (Art. 1 Protocol 1 CEDO)",
                "argument": "Somația directă prin reprezentant legal constituie proba absolută a relei-credințe a constructorului care continuă lucrările."
            },
            "7": {
                "situatie": "Construcție ridicată ÎN TIMPUL procesului de Rectificare/Anulare",
                "lege": "Art. 582 alin. (1) lit. b) Cod Civil (Accesiunea artificială)",
                "iccj": "Decizia nr. 355/2025; Decizia nr. 1480/2025",
                "argument": "Edificarea pe 'res litigiosa' implică asumarea riscului demolării. Constructorul nu poate invoca buna-credință pe durata litigiului."
            },
            "8": {
                "situatie": "Autorizație de Construire emisă nelegal pe zonă suprapusă",
                "lege": "Legea 50/1991; Art. 1 din Legea 554/2004",
                "iccj": "Practica secției de Contencios Administrativ ICCJ",
                "argument": "Autorizația nu poate înfrânge o hotărâre de revendicare. Notarea suprapunerii în CF face ca actul administrativ să fie viciat la emitere."
            }
        }

    def afiseaza_meniu(self):
        print("\n" + "="*60)
        print(" APLICAȚIE JURISPRUDENȚĂ: BIFEAZĂ VARIANTELE SPEȚEI TALE")
        print("="*60)
        for cheie, info in self.baza_date.items():
            print(f"[{cheie}] - {info['situatie']}")
        print("[0] - GENEREAZĂ SINTEZA PENTRU INSTANȚĂ")
        print("="*60)

    def ruleaza(self):
        selectii = []
        while True:
            self.afiseaza_meniu()
            optiune = input("Alege bifa (sau 0 pentru rezultat): ").strip()
            
            if optiune == "0":
                break
            elif optiune in self.baza_date:
                if optiune not in selectii:
                    selectii.append(optiune)
                    print(f"✅ Adăugat: {self.baza_date[optiune]['situatie']}")
                else:
                    print("⚠️ Deja selectat!")
            else:
                print("❌ Opțiune invalidă!")

        self.genereaza_output(selectii)

    def genereaza_output(self, selectii):
        if not selectii:
            print("\nNu ai selectat nicio variantă!")
            return

        print("\n\n" + "#"*70)
        print(" SINTEZĂ JURISPRUDENȚĂ PENTRU NOTE SCRISE / INSTANȚĂ")
        print("#"*70)

        for s in selectii:
            item = self.baza_date[s]
            print(f"\n📍 SITUAȚIE: {item['situatie']}")
            print(f"📜 TEMEI LEGAL: {item['lege']}")
            print(f"🏛️ JURISPRUDENȚĂ ÎCCJ: {item['iccj']}")
            print(f"✍️ CITAT ARGUMENTARE: \"{item['argument']}\"")
            print("-" * 70)
        
        print("\nNOTĂ: Această sinteză se bazează pe deciziile obligatorii ale ICCJ.")

# Pornire aplicație
if __name__ == "__main__":
    app = MotorJurisprudenta()
    app.ruleaza()