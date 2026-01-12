# 📖 About – StoryBuilder Project

StoryBuilder este o aplicație interactivă pentru copii care permite construirea unei povești folosind **voce, imagini și redare audio**.  
Utilizatorul spune o propoziție, aplicația o transcrie (Speech-to-Text), caută o imagine relevantă online, o afișează și apoi citește propoziția cu o voce sintetică (Text-to-Speech).

Aplicația permite adăugarea succesivă de propoziții, rezultând o **poveste vizuală și audio**, cu istoric de imagini și text.

Proiectul este structurat modular:
- Student 1 – GUI și managementul aplicației  
- Student 2 – STT, TTS și Keywords  
- Student 3 – Image Search și procesare vizuală  


# 🧩 Student 1 – GUI și Managementul Poveștii

## Ce am eu în proiect

Eu am fișierul: `student1_services.py`.

În el există clasa `StoryBuilderApp`, care reprezintă **aplicația principală** și face legătura între toate componentele proiectului.

Modulul Student 1 este responsabil de:
1. Interfața grafică (Tkinter GUI)
2. Managementul poveștii
3. Controlul captării audio (Start / Stop)
4. Integrarea completă Student 2 + Student 3


## Ce face Student 1

- Creează interfața grafică:
  - zonă mare pentru afișarea imaginii curente  
  - zonă text unde se construiește povestea  
  - bandă cu imagini anterioare (gallery strip / thumbnails)  
  - butoane de control (Start/Stop înregistrare, Citește povestea, Reset)

- Gestionează povestea:
  - salvează propozițiile spuse de utilizator  
  - le afișează în timp real  
  - permite citirea întregii povești folosind TTS  

- Controlează captarea vocii:
  - un click → începe înregistrarea  
  - al doilea click → oprește înregistrarea și procesează propoziția  

- Coordonează întreg fluxul aplicației:
  - STT → keywords → image search → afișare → TTS  


## Cum se rulează partea Student 1

py student1_services.py


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

