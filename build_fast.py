# -*- coding: utf-8 -*-
"""Быстрая сборка: картинки отдельными webp-файлами рядом с index.html."""
import re, os, shutil, base64
from PIL import Image

BASE = '/Users/mustari/Desktop/Boost 11/Непал'
OUT = os.path.join(BASE, 'site-punhil')
IMG = os.path.join(OUT, 'img')
os.makedirs(IMG, exist_ok=True)

src = open(os.path.join(BASE, 'nepal-lending-punhil.html'), encoding='utf-8').read()

# вытаскиваем имена и base64, сохраняем как webp
saved = {}
def repl(mo):
    name, data = mo.group(1), mo.group(2)
    if name not in saved:
        raw = base64.b64decode(data)
        tmp = os.path.join(IMG, name + '.jpg')
        open(tmp,'wb').write(raw)
        im = Image.open(tmp).convert('RGB')
        im.save(os.path.join(IMG, name + '.webp'), 'WEBP', quality=80, method=5)
        os.remove(tmp)
        saved[name] = os.path.getsize(os.path.join(IMG, name + '.webp'))
    return '.im-%s { background-image: url("img/%s.webp"); }' % (name, name)

out = re.sub(r'\.im-([a-z0-9-]+)\s*\{\s*background-image:\s*url\("data:image/jpeg;base64,([^"]+)"\);\s*\}', repl, src)

# предзагрузка обложки
out = out.replace('<title>', '<link rel="preload" as="image" href="img/hero-drug.webp">\n<title>', 1)

meta = '''<meta name="description" content="Непал для своих — 11 дней, 14–24 ноября 2026: тибетский квартал Катманду, Патан, озеро Фева и четырёхдневный трек Гхорепани — Пунхилл — Гандрук. Группа до 6 человек.">
<meta property="og:type" content="website">
<meta property="og:title" content="Непал для своих — 11 дней, ноябрь 2026">
<meta property="og:description" content="Затеряемся в переулках старого города, встретим рассвет в Гималаях и, возможно, узнаем себя чуть лучше. 14–24 ноября 2026, максимум 6 человек.">
<meta property="og:image" content="preview.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🏔️</text></svg>">
'''
out = out.replace('<title>', meta + '<title>', 1)

open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(out)
total = sum(saved.values())
print('index.html:', round(os.path.getsize(os.path.join(OUT,'index.html'))/1024, 1), 'КБ')
print('картинок:', len(saved), '| суммарно:', round(total/1024/1024, 2), 'МБ')
