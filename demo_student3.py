from student3_services import Student3Services, get_image_from_keywords

def demo_simple():
    print("=" * 60)
    print("DEMO SIMPLU - Functie Helper")
    print("=" * 60)
    
    print("\n1 Caut imagine pentru 'dragon rosu'...")
    image_path = get_image_from_keywords("dragon rosu")
    if image_path:
        print(f"Succes! Imagine la: {image_path}")
    else:
        print("Nu s-a putut descarca imaginea")
    
    print("\n2 Caut imagine pentru 'castel magic'...")
    image_path = get_image_from_keywords("castel magic")
    if image_path:
        print(f"Succes! Imagine la: {image_path}")
    else:
        print("Nu s-a putut descarca imaginea")


def demo_advanced():
    print("\n" + "=" * 60)
    print("DEMO AVANSAT - Clasa Student3Services")
    print("=" * 60)
    
    svc = Student3Services(api_choice="unsplash")
    
    print("\nCaut imagine pentru 'printesa'...")
    image_info = svc.search_image("printesa")
    
    if image_info:
        print(f"Am gasit imagine!")
        print(f"   URL: {image_info['url'][:60]}...")
        print(f"   Autor: {image_info['author']}")
        print(f"   Sursa: {image_info['source']}")
        
        print("\nDescarc imaginea...")
        filepath = svc.download_image(image_info)
        if filepath:
            print(f"Imagine salvata la: {filepath}")
    else:
        print("Nu am gasit imagine")
    
    print("\nTest all-in-one pentru 'vrajitor'...")
    filepath = svc.get_image_for_query("vrajitor")
    if filepath:
        print(f"✅ Succes! {filepath}")


def demo_integration_with_student2():
    print("\n" + "=" * 60)
    print("DEMO INTEGRARE CU STUDENT 2")
    print("=" * 60)
    
    simulated_keywords = [
        "dragon rosu",
        "print curajos",
        "padure intunecata",
        "zana frumoasa"
    ]
    
    svc = Student3Services(api_choice="unsplash")
    
    print("\nConstruim o poveste vizuala...\n")
    
    for i, keywords in enumerate(simulated_keywords, 1):
        print(f"\n--- Propozitia {i}: '{keywords}' ---")
        filepath = svc.get_image_for_query(keywords)
        
        if filepath:
            print(f"Imagine adaugata la poveste: {filepath}")
        else:
            print(f"Folosim placeholder pentru '{keywords}'")
            filepath = svc.get_placeholder_image()
        
        print(f"   (Student 1 ar afisa acum imaginea in GUI)")


def demo_error_handling():
    print("\n" + "=" * 60)
    print("DEMO GESTIONARE ERORI")
    print("=" * 60)
    
    svc = Student3Services(api_choice="unsplash")
    
    print("\n1 Test cu query gol...")
    result = svc.search_image("")
    print(f"   Rezultat: {result}")
    
    print("\n2 Test cu query obscur...")
    result = svc.search_image("xyzqwerty12345abcdef")
    if not result:
        print("   Corect - nu exista rezultate, dar nu a crapac!")
    
    print("\n3 Creez imagine placeholder...")
    placeholder = svc.get_placeholder_image()
    if placeholder:
        print(f"   Placeholder creat: {placeholder}")


def main():
    print("\n" + "" * 30)
    print(" " * 20 + "DEMO STUDENT 3 - IMAGE SEARCH")
    print("" * 30)
    
    try:
        demo_simple()
        
        demo_advanced()
        
        demo_integration_with_student2()
        
        demo_error_handling()
        
        print("\n" + "=" * 60)
        print("TOATE DEMO-URILE AU FOST COMPLETATE!")
        print("=" * 60)
        print("\nVerifica folderul 'images/' pentru imaginile descarcate.")
        print("Pentru API key-uri (Pexels, Pixabay), modifica initializarea:")
        print("   svc = Student3Services(api_choice='pexels', api_key='YOUR_KEY')")
        
    except KeyboardInterrupt:
        print("\n\nDemo intrerupt de utilizator.")
    except Exception as e:
        print(f"\n\nEroare neasteptata: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
