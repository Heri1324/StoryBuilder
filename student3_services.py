import requests
import os
from typing import Optional, Dict, Any
from io import BytesIO
from PIL import Image


class Student3Services:
    
    def __init__(self, api_choice="unsplash", api_key=None):
        self.api_choice = api_choice.lower()
        self.api_key = api_key
        
        self.apis = {
            "unsplash": {
                "url": "https://api.unsplash.com/search/photos",
                "headers": {"Authorization": f"Client-ID {api_key}"} if api_key else {},
            },
            "pexels": {
                "url": "https://api.pexels.com/v1/search",
                "headers": {"Authorization": api_key} if api_key else {},
            },
            "pixabay": {
                "url": "https://pixabay.com/api/",
                "headers": {},
            }
        }
        
        self.last_image_path = None
        self.last_query = None
        self.last_image_data = None
    
    def _improve_query(self, query: str) -> str:
        """Imbunatateste query-ul primit de la Student 2"""
        concepts = self._extract_multiple_concepts(query)
        
        if len(concepts) > 1:
            return concepts
        
        return concepts[0] if concepts else query
    
    def _extract_multiple_concepts(self, query: str):
        """Extrage concepte multiple din query (ex: dragon + castel mare)"""
        if not query:
            return [query]
        
        translations = {
            'dragon': 'dragon',
            'castel': 'castle',
            'mare': 'big',
            'mic': 'small',
            'rosu': 'red',
            'albastru': 'blue',
            'verde': 'green',
            'galben': 'yellow',
            'negru': 'black',
            'alb': 'white',
            'frumos': 'beautiful',
            'urat': 'ugly',
            'vechi': 'old',
            'nou': 'new',
            'padure': 'forest',
            'munte': 'mountain',
            'rau': 'river',
            'lac': 'lake',
            'oras': 'city',
            'sat': 'village',
            'casa': 'house',
            'copac': 'tree',
            'floare': 'flower',
            'soare': 'sun',
            'luna': 'moon',
            'stea': 'star',
            'cer': 'sky',
            'nori': 'clouds',
            'ploaie': 'rain',
            'zapada': 'snow',
            'lup': 'wolf',
            'urs': 'bear',
            'vulpe': 'fox',
            'iepure': 'rabbit',
            'pasare': 'bird',
            'peste': 'fish',
            'cal': 'horse',
            'pisica': 'cat',
            'caine': 'dog'
        }
        
        verbs_to_remove = ['locuia', 'era', 'avea', 'traieste', 'face', 'spune', 'merge', 'vine', 'pleaca']
        prepositions = ['intr-un', 'intr', 'pe', 'la', 'din', 'cu', 'fara']
        
        words = [w.lower() for w in query.split()]
        
        adjectives_ro = {'mare', 'mic', 'rosu', 'albastru', 'verde', 'galben', 'negru', 'alb', 'frumos', 'urat', 'vechi', 'nou'}
        
        nouns_found = []
        i = 0
        
        while i < len(words):
            word = words[i]
            
            if word in verbs_to_remove or word in prepositions:
                i += 1
                continue
            
            if word in translations and word not in adjectives_ro:
                noun = translations[word]
                
                if i + 1 < len(words) and words[i + 1] in adjectives_ro:
                    adjective = translations[words[i + 1]]
                    nouns_found.append(f"{adjective} {noun}")
                    i += 2
                else:
                    nouns_found.append(noun)
                    i += 1
            else:
                i += 1
        
        return nouns_found if nouns_found else [query]
    
    def search_image(self, query: str, max_results: int = 1) -> Optional[Dict[str, Any]]:
        improved_query = self._improve_query(query)
        
        if isinstance(improved_query, list):
            return None
        
        if not improved_query or improved_query.strip() == "":
            print("Query gol, nu pot cauta imagini.")
            return None
        
        if improved_query != query:
            print(f"Query imbunatatit: '{query}' -> '{improved_query}'")
        
        print(f"Caut imagini pentru: '{improved_query}' folosind {self.api_choice.upper()}")
        
        try:
            if self.api_choice == "unsplash":
                return self._search_unsplash(improved_query, max_results)
            elif self.api_choice == "pexels":
                return self._search_pexels(improved_query, max_results)
            elif self.api_choice == "pixabay":
                return self._search_pixabay(improved_query, max_results)
            else:
                print(f"API necunoscut: {self.api_choice}")
                return None
                
        except requests.RequestException as e:
            print(f"Eroare de retea: {e}")
            return None
        except Exception as e:
            print(f"Eroare la cautarea imaginii: {e}")
            return None
    
    def _search_unsplash(self, query: str, max_results: int) -> Optional[Dict[str, Any]]:
        url = self.apis["unsplash"]["url"]
        headers = self.apis["unsplash"]["headers"]
        
        params = {
            "query": query,
            "per_page": max_results,
            "orientation": "landscape"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 401:
            print("Unsplash necesita API Key! Obtine unul gratuit de la https://unsplash.com/developers")
            return None
        elif response.status_code != 200:
            print(f"Unsplash API Error: {response.status_code}")
            return None
        
        data = response.json()
        
        if not data.get("results") or len(data["results"]) == 0:
            print(f"Nu am gasit imagini pentru '{query}' pe Unsplash.")
            return None
        
        img = data["results"][0]
        
        return {
            "url": img["urls"]["regular"],
            "thumbnail": img["urls"]["thumb"],
            "author": img["user"]["name"],
            "description": img.get("description", query),
            "source": "Unsplash"
        }
    
    def _search_pexels(self, query: str, max_results: int) -> Optional[Dict[str, Any]]:
        if not self.api_key:
            print("Pexels necesita API Key!")
            return None
        
        url = self.apis["pexels"]["url"]
        headers = self.apis["pexels"]["headers"]
        
        params = {
            "query": query,
            "per_page": max_results,
            "orientation": "landscape"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Pexels API Error: {response.status_code}")
            return None
        
        data = response.json()
        
        if not data.get("photos") or len(data["photos"]) == 0:
            print(f"Nu am gasit imagini pentru '{query}' pe Pexels.")
            return None
        
        img = data["photos"][0]
        
        return {
            "url": img["src"]["large"],
            "thumbnail": img["src"]["small"],
            "author": img.get("photographer", "Unknown"),
            "description": query,
            "source": "Pexels"
        }
    
    def _search_pixabay(self, query: str, max_results: int) -> Optional[Dict[str, Any]]:
        if not self.api_key:
            print("Pixabay necesita API Key!")
            return None
        
        url = self.apis["pixabay"]["url"]
        
        params = {
            "key": self.api_key,
            "q": query,
            "image_type": "photo",
            "per_page": max_results,
            "safesearch": "true"
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"Pixabay API Error: {response.status_code}")
            return None
        
        data = response.json()
        
        if not data.get("hits") or len(data["hits"]) == 0:
            print(f"Nu am gasit imagini pentru '{query}' pe Pixabay.")
            return None
        
        img = data["hits"][0]
        
        return {
            "url": img["largeImageURL"],
            "thumbnail": img["previewURL"],
            "author": img.get("user", "Unknown"),
            "description": query,
            "source": "Pixabay"
        }
    
    def download_image(self, image_info: Dict[str, Any], save_dir: str = "images") -> Optional[str]:
        if not image_info or "url" not in image_info:
            print("Nu exista informatii despre imagine!")
            return None
        
        try:
            os.makedirs(save_dir, exist_ok=True)
            
            print(f"Descarc imaginea de la {image_info['source']}...")
            response = requests.get(image_info["url"], timeout=15)
            response.raise_for_status()
            
            img = Image.open(BytesIO(response.content))
            
            description = image_info.get("description") or image_info.get("query") or "image"
            query_safe = str(description)[:30]
            query_safe = "".join(c if c.isalnum() or c in " " else "_" for c in query_safe)
            filename = f"{query_safe}.jpg"
            filepath = os.path.join(save_dir, filename)
            
            img.convert("RGB").save(filepath, "JPEG", quality=85)
            
            self.last_image_path = filepath
            self.last_image_data = image_info
            
            print(f"Imagine salvata: {filepath}")
            print(f"   Autor: {image_info.get('author', 'Unknown')}")
            
            return filepath
            
        except requests.RequestException as e:
            print(f"Eroare la descarcarea imaginii: {e}")
            return None
        except Exception as e:
            print(f"Eroare la salvarea imaginii: {e}")
            return None
    
    def get_image_for_query(self, query: str, save_dir: str = "images"):
        improved = self._improve_query(query)
        
        if isinstance(improved, list) and len(improved) > 1:
            return self.get_images_for_multiple_concepts(improved, save_dir)
        
        single_query = improved[0] if isinstance(improved, list) else improved
        
        image_info = self.search_image(query)
        
        if not image_info:
            return None
        
        if "query" not in image_info:
            image_info["query"] = query
        
        return self.download_image(image_info, save_dir)
    
    def get_images_for_multiple_concepts(self, concepts, save_dir: str = "images"):
        """Descarca imagini pentru concepte multiple"""
        results = []
        
        print(f"\nGasit {len(concepts)} concepte: {', '.join(concepts)}")
        
        for i, concept in enumerate(concepts, 1):
            print(f"\n[{i}/{len(concepts)}] Procesez: '{concept}'")
            
            image_info = self.search_image(concept)
            
            if image_info:
                if "query" not in image_info:
                    image_info["query"] = concept
                
                filepath = self.download_image(image_info, save_dir)
                if filepath:
                    results.append(filepath)
        
        return results if results else None
    
    def get_last_image(self) -> Optional[str]:
        return self.last_image_path
    
    def get_placeholder_image(self, save_dir: str = "images") -> str:
        try:
            os.makedirs(save_dir, exist_ok=True)
            
            img = Image.new("RGB", (640, 480), color=(200, 200, 200))
            filepath = os.path.join(save_dir, "placeholder.jpg")
            img.save(filepath)
            
            return filepath
        except Exception as e:
            print(f"Eroare la crearea placeholder: {e}")
            return None


def get_image_from_keywords(keywords: str, api="unsplash", api_key=None) -> Optional[str]:
    svc = Student3Services(api_choice=api, api_key=api_key)
    return svc.get_image_for_query(keywords)
