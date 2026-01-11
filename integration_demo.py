
from student2_servicii import Student2Services
from student3_services import Student3Services


def demo_flow_interactive():
    print("=" * 70)
    print(" " * 15 + "STORYBUILDER - INTEGRARE STUDENT 2 + 3")
    print("=" * 70)
    print("\nConstruim o poveste vizuala impreuna!")
    print("   Vorbeste o propozitie si voi gasi o imagine potrivita.\n")
    
    student2 = Student2Services(language="ro-RO")
    student3 = Student3Services(api_choice="unsplash")
    
    story = []
    sentence_count = 0
    
    print("Spune STOP pentru a termina povestea\n")
    print("-" * 70)
    
    while True:
        sentence_count += 1
        print(f"\nPROPOZITIA {sentence_count}")
        print("=" * 70)
        
        print("Ascult... (vorbeste acum)")
        text = student2.listen_sentence(timeout=5, phrase_time_limit=10)
        
        if not text:
            print("Nu am auzit nimic. Incearca din nou.")
            sentence_count -= 1
            continue
        
        print(f"Am auzit: \"{text}\"")
        
        if "stop" in text.lower():
            print("\nAi spus STOP. Inchei povestea...")
            break
        
        print("\nExtrag cuvintele cheie...")
        keywords = student2.make_query(text)
        print(f"Keywords: \"{keywords}\"")
        
        print(f"\nCaut imagine pentru \"{keywords}\"...")
        image_path = student3.get_image_for_query(keywords)
        
        if image_path:
            print(f"Imagine gasita si descarcata: {image_path}")
        else:
            print("Nu am gasit imagine, folosesc placeholder...")
            image_path = student3.get_placeholder_image()
        
        print("\nCitesc propozitia inapoi...")
        student2.speak(text)
        
        story.append({
            "text": text,
            "keywords": keywords,
            "image": image_path
        })
        
        print("\n" + "-" * 70)
        print(f"Propozitia {sentence_count} adaugata la poveste!")
        print("-" * 70)
    
    print("\n\n" + "=" * 70)
    print(" " * 25 + "POVESTEA TA")
    print("=" * 70)
    
    for i, entry in enumerate(story, 1):
        print(f"\n{i}. {entry['text']}")
        print(f"   Keywords: {entry['keywords']}")
        print(f"   Imagine: {entry['image']}")
    
    print("\n" + "=" * 70)
    print(f"Poveste completa cu {len(story)} propozitii!")
    print("=" * 70)
    print(f"\nToate imaginile sunt in folderul 'images/'")
    print("Student 1 va afisa aceste imagini in GUI")


def demo_flow_simulated():
    print("\n" + "=" * 70)
    print(" " * 20 + "DEMO SIMULAT (FARA MICROFON)")
    print("=" * 70)
    
    sentences = [
        "A fost odata un dragon rosu",
        "Dragon locuia intr-un castel mare",
        "In castel era o printesa frumoasa",
        "Printesa avea un cal alb"
    ]
    
    student2 = Student2Services(language="ro-RO")
    student3 = Student3Services(api_choice="unsplash")
    
    story = []
    
    for i, text in enumerate(sentences, 1):
        print(f"\nPROPOZITIA {i}: \"{text}\"")
        print("-" * 70)
        
        keywords = student2.make_query(text)
        print(f"Keywords: \"{keywords}\"")
        
        print(f"Caut imagini pentru propozitia completa...")
        image_result = student3.get_image_for_query(text)
        
        if isinstance(image_result, list):
            print(f"Imagini: {len(image_result)} imagini gasite")
            for img in image_result:
                print(f"  - {img}")
            image_path = image_result
        elif image_result:
            print(f"Imagine: {image_result}")
            image_path = image_result
        else:
            print(f"Placeholder: {student3.get_placeholder_image()}")
            image_path = "placeholder.jpg"
        
        print(f"[TTS ar citi: \"{text}\"]")
        
        story.append({
            "text": text,
            "keywords": keywords,
            "image": image_path
        })
    
    print("\n\n" + "=" * 70)
    print("POVESTE COMPLETA:")
    print("=" * 70)
    for i, entry in enumerate(story, 1):
        print(f"\n{i}. {entry['text']}")
        print(f"   → {entry['image']}")


def main():
    print("\n" + "" * 35)
    print(" " * 20 + "INTEGRARE STUDENT 2 + STUDENT 3")
    print("" * 35)
    print("\nAlege modul de rulare:")
    print("  1. Interactiv (cu microfon - STT real)")
    print("  2. Simulat (fara microfon - pentru testare)")
    print("  3. Ambele\n")
    
    choice = input("Optiunea ta (1/2/3): ").strip()
    
    try:
        if choice == "1":
            demo_flow_interactive()
        elif choice == "2":
            demo_flow_simulated()
        elif choice == "3":
            demo_flow_simulated()
            input("\n\nApasa ENTER pentru demo interactiv...")
            demo_flow_interactive()
        else:
            print("Optiune invalida!")
            return
        
        print("\n\n" + "=" * 70)
        print("INTEGRARE REUSITA!")
        print("=" * 70)
        print("\nNEXT STEPS pentru Student 1 (GUI):")
        print("   1. Importa Student2Services si Student3Services")
        print("   2. Creaza interfata Tkinter")
        print("   3. Afiseaza imaginile din story[] in GUI")
        print("   4. Adauga buton 'Spune Urmatoarea Propozitie'")
        print("\nExemplu cod pentru Student 1 in STUDENT3_README.md")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Întrerupt de utilizator.")
    except Exception as e:
        print(f"\n\n❌ Eroare: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
