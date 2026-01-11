# Student 1 – Student 1 (GUI și Managementul Poveștii)|



# Student 2 – STT + TTS + Keywords (cum folosiți codul meu)

## Ce am eu în proiect
Eu am fișierul: `student2_servicii.py`.

În el există clasa `Student2Services` care face 3 lucruri:
1. **STT**: ascultă de la microfon și îți dă text  
2. **TTS**: citește un text cu voce  
3. **Keywords/Query**: din text scoate un query simplu pentru căutare (ex: `dragon rosu`)

## Cum se folosește:

```python
from student2_servicii import Student2Services

svc = Student2Services(language="ro-RO")

# 1. Asculta propozitie
text = svc.listen_sentence()

# 2. Extrage keywords
query = svc.make_query(text)

# 3. Citeste cu voce
svc.speak(text)
```

---

# Student 3 – Image Search (cum folosiți codul meu)

## Ce am eu în proiect
Eu am fișierul: `student3_services.py`.

În el există clasa `Student3Services` care face:
1. **Image Search**: caută imagini pe API-uri (Unsplash, Pexels, Pixabay)
2. **Download**: descarcă imaginea găsită
3. **Smart Translation**: traduce română → engleză pentru căutare precisă
4. **Multiple Concepts**: detectează și descarcă mai multe imagini pentru concepte multiple

## Funcționalități avansate:
- **Traducere automată**: `dragon rosu` → `red dragon`, `castel mare` → `big castle`
- **Filtrare verbe**: elimină verbe și prepoziții (`locuia`, `intr-un`, etc.)
- **Concepte multiple**: `dragon locuia intr-un castel mare` → 2 imagini (dragon + big castle)
- **Ordine corectă**: română (substantiv + adjectiv) → engleză (adjectiv + substantiv)

## Cum se folosește:

```python
from student3_services import Student3Services

svc = Student3Services(api_choice="unsplash", api_key="YOUR_KEY")

# Simple: o singura imagine
image_path = svc.get_image_for_query("dragon rosu")
# Rezultat: images/red_dragon.jpg

# Multiple: concepte multiple
images = svc.get_image_for_query("dragon locuia intr-un castel mare")
# Rezultat: ['images/dragon.jpg', 'images/big_castle.jpg']
```

## Integrare cu Student 2:

```python
from student2_servicii import Student2Services
from student3_services import Student3Services

svc2 = Student2Services(language="ro-RO")
svc3 = Student3Services(api_choice="unsplash", api_key="YOUR_KEY")

# Student 2: STT + Keywords
text = svc2.listen_sentence()  # "Dragon locuia intr-un castel mare"
keywords = svc2.make_query(text)  # "dragon locuia intr-un"

# Student 3: Cauta imagini (auto-traduce si detecteaza concepte)
result = svc3.get_image_for_query(keywords)
# Rezultat: 'images/dragon.jpg' SAU ['images/dragon.jpg', 'images/big_castle.jpg']

# Student 2: TTS
svc2.speak(text)

# Student 1 va afisa imaginile in GUI
```

## Exemple de traducere automată:
- `dragon rosu` → `red dragon` ✓
- `castel mare` → `big castle` ✓ (nu `sea`!)
- `lup negru` → `black wolf` ✓
- `padure verde` → `green forest` ✓
- `casa veche` → `old house` ✓

## API-uri suportate:
- **Unsplash**: FREE API key de la https://unsplash.com/developers
- **Pexels**: FREE API key de la https://www.pexels.com/api/
- **Pixabay**: FREE API key de la https://pixabay.com/api/docs/

### Cum obtin API key:
```python
# Cu API key (recomandat)
svc = Student3Services(api_choice="unsplash", api_key="YOUR_API_KEY")
```

## Demo:
```bash
python demo_student3.py          # Demo Student 3
python integration_demo.py       # Demo integrare Student 2 + 3
```

