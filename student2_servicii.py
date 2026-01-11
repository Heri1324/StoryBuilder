import re
import unicodedata

import speech_recognition as sr
import pyttsx3


class Student2Services:

    def __init__(self, language="ro-RO"):
        self.language = language
        self.rec = sr.Recognizer()
        self.engine = pyttsx3.init()

        self.rec.dynamic_energy_threshold = True

        
        self.stopwords = {
            "a", "am", "ai", "au", "fost", "odata", "este", "era", "sunt",
            "in", "din", "pe", "la", "cu", "si", "sau", "dar", "ca", "care", "ce",
            "un", "o", "unei", "unui", "de", "mai", "foarte", "tot"
        }

    #STT 
    def listen_sentence(self, timeout=5, phrase_time_limit=7):

        try:
            with sr.Microphone() as source:
                self.rec.adjust_for_ambient_noise(source, duration=0.5)
                print("Vorbește acum...")
                audio = self.rec.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

            text = self.rec.recognize_google(audio, language=self.language)
            return text

        except sr.WaitTimeoutError:
            print("Timeout: nu ai început să vorbești.")
            return None
        except sr.UnknownValueError:
            print("Nu am înțeles ce ai spus.")
            return None
        except sr.RequestError:
            print("Eroare rețea (Google STT).")
            return None
        except Exception as e:
            print("Eroare STT:", e)
            return None

    # TTS 
    def speak(self, text):
        if not text:
            return
        self.engine.say(text)
        self.engine.runAndWait()

    #Keywords / Query
    def make_query(self, sentence):
        
        if not sentence:
            return ""

        
        s = self._normalize(sentence)

        
        s = s.replace("a fost odata", " ").strip()

        words = s.split()

        
        for i in range(len(words) - 2):
            if words[i] in ("un", "o"):
                w1, w2 = words[i + 1], words[i + 2]
                if w1 not in self.stopwords and w2 not in self.stopwords:
                    return f"{w1} {w2}"

        
        core = [w for w in words if w not in self.stopwords and len(w) > 2]
        return " ".join(core[:3])

    
    def _normalize(self, text):
       
        t = text.lower()

        
        t = unicodedata.normalize("NFD", t)
        t = "".join(ch for ch in t if unicodedata.category(ch) != "Mn")

       
        t = re.sub(r"[^a-z0-9\s-]", " ", t)
        t = re.sub(r"\s+", " ", t).strip()

        return t
