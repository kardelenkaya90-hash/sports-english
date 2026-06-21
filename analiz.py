
import re
import os
import pandas as pd
from collections import defaultdict

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


THIS_FILE        = os.path.abspath(__file__)
PROJE_KOKU       = os.path.dirname(os.path.dirname(THIS_FILE))

KODLANMIS_KLASOR = os.path.join(PROJE_KOKU, "coded")
CIKTI_KLASOR     = os.path.join(PROJE_KOKU, "output")

os.makedirs(CIKTI_KLASOR, exist_ok=True)

KATILIMCILAR = {
    "coach_coded.txt"   : "Coach",
    "teacher_coded.txt" : "Teacher",
    "athlete_coded.txt" : "Athlete"
}


def transkript_oku(dosya_yolu):
    with open(dosya_yolu, "r", encoding="utf-8") as dosya:
        return dosya.read()

def rapor_yaz(dosya_yolu, icerik):
    with open(dosya_yolu, "w", encoding="utf-8") as dosya:
        dosya.write(icerik)



def kodlari_cikar(metin):
    sablon = r'\[(\w+)\](.*?)\[/\1\]'
    eslesmeler = re.findall(sablon, metin, re.DOTALL)

    return [(kod.strip(), alinti.strip()) for kod, alinti in eslesmeler]


def tum_verileri_yukle():
    tum_veriler = {}

    for dosya_adi, katilimci_adi in KATILIMCILAR.items():
        dosya_yolu = os.path.join(KODLANMIS_KLASOR, dosya_adi)

        try:
            metin  = transkript_oku(dosya_yolu)
            kodlar = kodlari_cikar(metin)
            tum_veriler[katilimci_adi] = kodlar
            print(f"  Yuklendi: {dosya_adi}  -->  {len(kodlar)} alinti")

        except FileNotFoundError:
            print(f"  Bulunamadi: {dosya_adi}  (henuz kodlanmadi)")

        except Exception as hata:
            print(f"  Hata: {dosya_adi}  -->  {hata}")

    return tum_veriler


def frekans_tablosu_olustur(tum_veriler):
  
    satirlar = [
        {"Katilimci": katilimci, "Kod": kod, "Alinti": alinti}
        for katilimci, segmentler in tum_veriler.items()
        for kod, alinti in segmentler
    ]

    df = pd.DataFrame(satirlar)

    if df.empty:
        print("  Henuz kodlanmis veri yok.")
        return df, pd.DataFrame()

    frekans = df.groupby(["Kod", "Katilimci"]).size().unstack(fill_value=0)
    frekans["TOPLAM"] = frekans.sum(axis=1)
    frekans = frekans.sort_values("TOPLAM", ascending=False)

    return df, frekans


def codebook_metni_olustur(tum_veriler, *kodlar_filtre):
    codebook = defaultdict(lambda: defaultdict(list))

    for katilimci, segmentler in tum_veriler.items():
        for kod, alinti in segmentler:
            if not kodlar_filtre or kod in kodlar_filtre:
                codebook[kod][katilimci].append(alinti)

    satirlar = ["TAM CODEBOOK\n", "=" * 60]

    for kod in sorted(codebook.keys()):
        satirlar.append(f"\nKOD: [{kod}]")
        satirlar.append("-" * 40)
        for katilimci, alintılar in codebook[kod].items():
            satirlar.append(f"\n  [{katilimci}] -- {len(alintılar)} alinti:")
            for i, a in enumerate(alintılar, 1):
                satirlar.append(f"    {i}. {a}")

    return "\n".join(satirlar)


def katilimci_ozeti_olustur(tum_veriler):
    toplam_say = lambda segmentler: len(segmentler)  
    satirlar = []

    for katilimci, segmentler in zip(tum_veriler.keys(), tum_veriler.values()):
        satirlar.append(f"\n{'='*60}")
        satirlar.append(f"KATILIMCI: {katilimci}  ({toplam_say(segmentler)} alinti)")
        satirlar.append("=" * 60)

        koda_gore = defaultdict(list)
        for kod, alinti in segmentler:
            koda_gore[kod].append(alinti)

        for kod in sorted(koda_gore.keys()):
            satirlar.append(f"\n  [{kod}] -- {len(koda_gore[kod])} alinti:")
            for a in koda_gore[kod]:
                satirlar.append(f"    --> {a}")

    return "\n".join(satirlar)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  SPORTS ENGLISH -- TEMATIK ANALIZ")
    print("="*60 + "\n")

    tum_veriler = tum_verileri_yukle()

    if not tum_veriler:
        print("\nKodlanmis dosya bulunamadi. kodlanmis/ klasorunu kontrol edin.")
    else:
        df, frekans = frekans_tablosu_olustur(tum_veriler)

        if not frekans.empty:
            excel_yolu = os.path.join(CIKTI_KLASOR, "frekans_tablosu.xlsx")
            frekans.to_excel(excel_yolu)
            print(f"\n  Frekans tablosu --> cikti/frekans_tablosu.xlsx")
            print("\n  FREKANS TABLOSU:\n")
            print(frekans.to_string())

        codebook = codebook_metni_olustur(tum_veriler)
        rapor_yaz(os.path.join(CIKTI_KLASOR, "codebook_full.txt"), codebook)
        print(f"\n  Codebook --> cikti/codebook_full.txt")

        ozet = katilimci_ozeti_olustur(tum_veriler)
        rapor_yaz(os.path.join(CIKTI_KLASOR, "katilimci_ozeti.txt"), ozet)
        print(f"  Katilimci ozeti --> cikti/katilimci_ozeti.txt")

        print("\n  Analiz tamamlandi!\n")

        
