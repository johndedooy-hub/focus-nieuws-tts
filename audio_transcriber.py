import os
import whisper

# =====================================================================
# CONFIGURATIE: Pas hier je vaste begin- en eindwaarden aan
# =====================================================================
VASTE_BEGIN_TEKST = "--- START VAN TRANSCRIPT ---\n\n"
VASTE_EIND_TEKST = "\n\n--- EINDE VAN TRANSCRIPT ---"
# =====================================================================

def verwerk_bestaande_audio():
    # Zoek naar alle mp3-bestanden in de huidige map
    huidige_map = os.getcwd()
    mp3_bestanden = [f for f in os.listdir(huidige_map) if f.lower().endswith('.mp3')]
    
    if not mp3_bestanden:
        print("Geen MP3-bestanden gevonden in deze map.")
        return

    # Whisper model laden (gebruikt 'base' voor goede balans tussen snelheid en NL nauwkeurigheid)
    print("Whisper model wordt geladen (dit kan de eerste keer even duren)...")
    model = whisper.load_model("base") 
    
    for mp3_bestand in mp3_bestanden:
        audio_pad = os.path.join(huidige_map, mp3_bestand)
        print(f"\nBezig met converteren van: {mp3_bestand}...")
        
        try:
            # Transcriptie uitvoeren
            resultaat = model.transcribe(audio_pad, fp16=False)
            getypte_tekst = resultaat["text"].strip()
            
            # Het .txt bestand samenstellen
            volledige_inhoud = f"{VASTE_BEGIN_TEKST}{getypte_tekst}{VASTE_EIND_TEKST}"
            
            # Sla het .txt bestand op met dezelfde naam
            txt_pad = os.path.splitext(audio_pad)[0] + ".txt"
            with open(txt_pad, "w", encoding="utf-8") as f:
                f.write(volledige_inhoud)
                
            print(f"Succes! Tekstbestand opgeslagen: {os.path.basename(txt_pad)}")
            
            # Vraag in de console (terminal) om het bestand te verwijderen
            keuze = input(f"Wil je het originele bestand '{mp3_bestand}' verwijderen? (ja/nee): ").strip().lower()
            if keuze in ['ja', 'j', 'y', 'yes']:
                os.remove(audio_pad)
                print(f"'{mp3_bestand}' is succesvol verwijderd.")
            else:
                print(f"'{mp3_bestand}' is bewaard.")
                
        except Exception as e:
            print(f"Fout bij het verwerken van {mp3_bestand}: {e}")

if __name__ == "__main__":
    verwerk_bestaande_audio()
