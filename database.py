import json
from datetime import datetime
import os

DOSYA_ADI = "egzersiz_kayitlari.json"

def egzersiz_kaydet(kullanici_adi, bolge, egzersiz_listesi):
    kayit = {
        "kullanici": kullanici_adi,
        "bolge": bolge,
        "egzersizler": egzersiz_listesi,
        "tarih": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    if os.path.exists(DOSYA_ADI):
        with open(DOSYA_ADI, "r", encoding="utf-8") as f:
            veriler = json.load(f)
    else:
        veriler = []

    veriler.append(kayit)

    with open(DOSYA_ADI, "w", encoding="utf-8") as f:
        json.dump(veriler, f, ensure_ascii=False, indent=4)

def egzersiz_gecmisi_getir(kullanici_adi):
    if not os.path.exists(DOSYA_ADI):
        return []

    with open(DOSYA_ADI, "r", encoding="utf-8") as f:
        veriler = json.load(f)

    return [k for k in veriler if k["kullanici"] == kullanici_adi]
