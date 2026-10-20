"""Generuje hero i galerię w src/index.html z listy zdjęć (sizes.json)."""
import json, re

R = json.load(open('/home/deck/.hermes/cache/scratch/sizes.json'))
CREDIT = 'fot. Jakub Bartnicki ©&nbsp;2026'
ALT = {
    'L1150313': 'Paweł Polanowski, portret castingowy, biała koszula, ręce skrzyżowane, ciemne tło',
    '29': 'Portret castingowy, biała koszula, ręce skrzyżowane',
    '23': 'Czarno-biały portret, biała koszula, dłoń przy brodzie',
    '09': 'Portret w koszuli w paski, ciepłe światło',
    '06': 'Czarno-biały portret w marynarce przy ceglanej ścianie',
    '15': 'Portret nad morzem, ciemne okulary, czarny t-shirt',
    '20': 'Siedząc na progu kampera, biała koszula',
    '21': 'Czarno-biała postać w białej koszuli w betonowym wnętrzu',
    '22': 'Czarno-białe ujęcie, pochylona głowa, dłoń przy twarzy',
    '28': 'Plan amerykański na ciemnym tle, biała koszula',
    '05': 'Czarno-białe ujęcie, siedząc na skarpie',
    '11': 'Za szybą kawiarni, przy stoliku',
    '13': 'Czarno-biały plan ogólny pod wiaduktem, pas światła',
    '10': 'W kawiarni, marynarka, kadr przez szybę',
    '24': 'Czarno-biały plan ogólny w podziemnym korytarzu',
    '27': 'Postać w snopie światła na ciemnej scenie',
    '19': 'Przy kamperze, plan ogólny',
}


def picture(n, w, h, sizes, hero=False):
    def srcset(ext):
        return f'img/p{n}-480.{ext} 480w, img/p{n}-960.{ext} 960w'
    load = 'fetchpriority="high"' if hero else 'loading="lazy"'
    return (f'<picture><source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">'
            f'<img src="img/p{n}-480.jpg" width="{w}" height="{h}" {load} alt="{ALT.get(n, 'Paweł Polanowski, sesja zdjęciowa 2026')}"></picture>')


hero = R[0]
w, h = hero['480']
hero_html = (f'<figure>\n      {picture(hero["n"], w, h, "(min-width:46rem) 28rem, 100vw", True)}\n'
             f'      <figcaption>{CREDIT}</figcaption>\n    </figure>')

items = []
for r in R[1:]:
    w, h = r['480']
    wide = w > h
    cls = ' class="wide"' if wide else ''
    sizes = '(min-width:46rem) 30rem, 100vw' if wide else '(min-width:46rem) 15rem, 50vw'
    items.append(f'        <li{cls}><figure>{picture(r["n"], w, h, sizes)}'
                 f'<figcaption>{CREDIT}</figcaption></figure></li>')
# REVERSE_WIDE: poziome w odwrotnej kolejności (najlepsze najpierw)
wi=[i for i,x in enumerate(items) if 'class="wide"' in x]
wv=[items[i] for i in wi][::-1]
for i,x in zip(wi,wv): items[i]=x
gallery = '<ul class="gallery">\n' + '\n'.join(items) + '\n      </ul>'

s = open('src/index.html').read()
s = re.sub(r'<figure>\s*<picture>.*?</figure>', hero_html, s, count=1, flags=re.S)
s = re.sub(r'<ul class="gallery">.*?</ul>', gallery, s, count=1, flags=re.S)
s = re.sub(r'<p class="cap">Sesja wrzesień 2026\..*?</p>',
           '<p class="cap">Wszystkie zdjęcia: Jakub Bartnicki, 2026. Kopiowanie i publikacja tylko za zgodą autora.</p>', s)
s = s.replace('img/portret-480.jpg', 'img/p30-480.jpg')
open('src/index.html', 'w').write(s)
print(len(items), 'zdjęć w galerii')
