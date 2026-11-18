"""Erzeugt index.html (Web-App) aus source/journal.html (Claude-Artefakt-Version).
Aufruf im Projektordner:  python3 tools/build_webapp.py"""
import re, sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, 'source', 'journal.html')).read()
h = src

def rep(a, b, count=1, first=False):
    global h
    n = h.count(a)
    assert n == count, f'{n}x gefunden: {a[:70]!r}'
    h = h.replace(a, b, 1 if first else -1)

rep('<meta name="viewport" content="width=device-width, initial-scale=1">',
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="theme-color" content="#5b6b45">\n'
    '<meta name="apple-mobile-web-app-capable" content="yes">\n'
    '<meta name="mobile-web-app-capable" content="yes">\n'
    '<meta name="apple-mobile-web-app-status-bar-style" content="default">\n'
    '<meta name="apple-mobile-web-app-title" content="Journal">\n'
    '<link rel="manifest" href="manifest.webmanifest">\n'
    '<link rel="icon" href="icon-192.png">\n'
    '<link rel="apple-touch-icon" href="apple-touch-icon.png">', count=2, first=True)
rep('#app{max-width:640px;margin:0 auto;padding:12px 12px 110px}',
    '#app{max-width:640px;margin:0 auto;padding:calc(12px + env(safe-area-inset-top)) calc(12px + env(safe-area-inset-right)) 110px calc(12px + env(safe-area-inset-left))}')
rep('var IS_PWA=false;', 'var IS_PWA=true;')
# Keine persönlichen Daten in der öffentlichen App: Startzustand leer, Umzug per Sicherung
h = re.sub(r'(<script type="application/json" id="state">).*?(</script>)', r'\1{"v":1,"sessions":[]}\2', h, count=1, flags=re.S)
# Training lokal laden/speichern
rep("var ART=null,artState='pending';",
    "var _ls=LS.get('tj_train');if(_ls&&_ls.sessions)S=_ls;\nvar ART=null,artState='pending';")
h = re.sub(r"function persist\(msg\)\{.*?\n\}\n",
    "function persist(msg){var ok=true;try{localStorage.setItem('tj_train',JSON.stringify(S))}catch(e){ok=false}toast(ok?msg:'Speichern fehlgeschlagen – Gerätespeicher voll?');return Promise.resolve(ok)}\n",
    h, count=1, flags=re.S)
h = re.sub(r"function connect\(\)\{.*?\n\}\nfunction goLocal",
    "function connect(){artState='ok';nutLocal();try{if(navigator.storage&&navigator.storage.persist)navigator.storage.persist()}catch(e){}"
    "if('serviceWorker' in navigator&&location.protocol!=='file:'){navigator.serviceWorker.register('sw.js').catch(function(){})}render()}\nfunction goLocal",
    h, count=1, flags=re.S)
rep("✓ Einträge werden in diesem Journal gespeichert – auf jedem Gerät verfügbar.",
    "✓ Gespeichert auf diesem Gerät · funktioniert auch offline")
rep(" else if(NUT.mode==='local')h+='<div class=\"status warn\">Dauerhaftes Speichern ist in dieser Ansicht nicht möglich – Einträge bleiben nur in diesem Browser. Öffne das Journal über claude.ai.</div>';\n", "\n")
rep("Keine Werte zur Hand? Schreib mir im Chat, was du gegessen hast – ich recherchiere die Nährwerte und trage sie ein.",
    "Keine Werte zur Hand? Auf der Verpackung oder per Websuche (z. B. „Pizza Margherita kcal“) findest du gute Richtwerte – dann „Werte sind geschätzt“ anhaken.")
assert 'claude.use' not in h.split('function connect')[1].split('function goLocal')[0]
# App-Name
rep('<title>Trainingsjournal</title>', '<title>Health Journal</title>', count=2, first=True)
rep('<meta name="apple-mobile-web-app-title" content="Journal">', '<meta name="apple-mobile-web-app-title" content="Health Journal">')
h = h.replace("name='trainingsjournal-'+today()+'.json'", "name='health-journal-'+today()+'.json'")
open(os.path.join(ROOT, 'index.html'), 'w').write(h)
print('ok', len(h))
