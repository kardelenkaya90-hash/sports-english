import os
import re
from collections import Counter
import pandas as pd


stop_words = set([
    'bir', 'bu', 'da', 'de', 've', 'ile', 'mi', 'mu', 'mı', 'mü',
    'ne', 'ki', 'ama', 'ya', 'için', 'gibi', 'daha', 'çok', 'en',
    'ben', 'sen', 'biz', 'siz', 'onlar', 'o', 'var', 'yok', 'olan',
    'olarak', 'olan', 'olan', 'bunu', 'bunu', 'şey', 'yani', 'işte',
    'falan', 'gibi', 'hani', 'mesela', 'çünkü', 'ama', 'zaten',
    'sadece', 'bile', 'kadar', 'sonra', 'önce', 'çok', 'diye',
    'oldu', 'olur', 'olan', 'olduğu', 'olduğunu', 'olması',
    'olan', 'benim', 'senin', 'onun', 'bizim', 'sizin', 'onların',
    'bana', 'sana', 'ona', 'bize', 'size', 'onlara', 'bende',
    'sende', 'onda', 'bizde', 'sizde', 'onlarda', 'bunun', 'şunu',
    'şu', 'şimdi', 'artık', 'nasıl', 'neden', 'niye', 'hangi',
    'her', 'hiç', 'hiçbir', 'hem', 'veya', 'yahut', 'oysa',
    'orada', 'burada', 'şurada', 'oraya', 'buraya', 'şuraya',
    'oradan', 'buradan', 'şuradan', 'zaman', 'şeyi', 'şeyde',
    'şeyden', 'şeyler', 'şeyleri', 'şeylerde', 'şeylerden',
    'tabi', 'tabii', 'yine', 'gene', 'hep', 'bazen', 'aslında'
])


def temizle(metin):
    metin = metin.lower()
    metin = re.sub(r'[^\w\s]', '', metin)
    kelimeler = metin.split()
    return [k for k in kelimeler if k not in stop_words and len(k) > 2]


klasor = '../transkriptler'
gruplar = {}

for dosya in ['sporcu.txt', 'antrenor.txt', 'ogretmen.txt']:
    with open(os.path.join(klasor, dosya), encoding='utf-8') as f:
        metin = f.read()
    gruplar[dosya.replace('.txt', '')] = temizle(metin)


for grup, kelimeler in gruplar.items():
    print(f"\n--- {grup.upper()} --- En sık 20 kelime:")
    for kelime, sayi in Counter(kelimeler).most_common(20):
        print(f"  {kelime}: {sayi}")
