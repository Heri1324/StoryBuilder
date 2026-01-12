import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from io import BytesIO

from PIL import Image, ImageTk
import pyaudio

from student2_servicii import Student2Services
from student3_services import Student3Services


class StoryBuilderApp:
    """
    STORYBUILDER - Student 1 (GUI + Management) + integrare Student 2 + 3

    Mod înregistrare:
      - Apăs 1x: START recording
      - Apăs 2x: STOP recording -> STT -> keywords -> image search -> afișare -> TTS
    """

    # Audio config (ok pentru STT)
    RATE = 16000
    CHANNELS = 1
    FORMAT = pyaudio.paInt16
    CHUNK = 1024  # samples per buffer

    THUMB_SIZE = 96  # thumbnails square

    def __init__(self):
        # --- Services ---
        self.svc2 = Student2Services(language="ro-RO")
        api_key = os.getenv("UNSPLASH_KEY")
        self.svc3 = Student3Services(api_choice="unsplash", api_key=api_key)

        # --- State ---
        self.story = []  # list[str]
        self.current_photo = None  # main image reference
        self.thumb_photos = []  # keep thumbnail PhotoImage refs
        self.last_images = []

        # Recording state
        self.is_recording = False
        self._record_stop_event = threading.Event()
        self._record_frames = []
        self._record_thread = None

        # PyAudio instance
        self._pa = pyaudio.PyAudio()

        # --- GUI ---
        self.root = tk.Tk()
        self.root.title("StoryBuilder - Prezentare (Start/Stop Recording + Gallery)")
        self.root.geometry("1200x760")

        self._build_ui()
        self._ensure_placeholder_exists()
        self._show_image(self.placeholder_path)
        self._set_status("Ready")

        # Clean up audio on close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ---------------- UI ----------------
    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)

        left = ttk.Frame(main)
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        right = ttk.Frame(main)
        right.pack(side="right", fill="both", expand=True)

        # ===== Main image =====
        self.image_label = ttk.Label(left, text="(Imaginea va apărea aici)", anchor="center")
        self.image_label.pack(fill="both", expand=True)

        self.multi_info = ttk.Label(left, text="", anchor="w")
        self.multi_info.pack(fill="x", pady=(6, 0))

        # ===== Gallery strip (thumbnails) =====
        ttk.Label(left, text="Istoric imagini:").pack(anchor="w", pady=(10, 4))

        strip_container = ttk.Frame(left)
        strip_container.pack(fill="x")

        self.strip_canvas = tk.Canvas(strip_container, height=self.THUMB_SIZE + 18, highlightthickness=0)
        self.strip_canvas.pack(side="top", fill="x", expand=True)

        self.strip_scroll = ttk.Scrollbar(strip_container, orient="horizontal", command=self.strip_canvas.xview)
        self.strip_scroll.pack(side="bottom", fill="x")

        self.strip_canvas.configure(xscrollcommand=self.strip_scroll.set)

        self.strip_inner = ttk.Frame(self.strip_canvas)
        self.strip_window_id = self.strip_canvas.create_window((0, 0), window=self.strip_inner, anchor="nw")

        # update scroll region when inner changes
        self.strip_inner.bind("<Configure>", lambda e: self.strip_canvas.configure(scrollregion=self.strip_canvas.bbox("all")))
        self.strip_canvas.bind("<Configure>", self._on_strip_canvas_resize)

        # ===== Buttons =====
        btns = ttk.Frame(left)
        btns.pack(fill="x", pady=10)

        self.btn_record = ttk.Button(btns, text="🎤 Start înregistrare", command=self.on_toggle_record)
        self.btn_record.pack(side="left")

        self.btn_read = ttk.Button(btns, text="Citește povestea (TTS)", command=self.on_read_story)
        self.btn_read.pack(side="left", padx=8)

        self.btn_reset = ttk.Button(btns, text="Reset poveste", command=self.on_reset)
        self.btn_reset.pack(side="left")

        self.status = ttk.Label(left, text="Ready", anchor="w")
        self.status.pack(fill="x")

        # ===== Story text =====
        ttk.Label(right, text="Povestea:").pack(anchor="w")
        story_frame = ttk.Frame(right)
        story_frame.pack(fill="both", expand=True)

        self.story_text = tk.Text(story_frame, wrap="word")
        self.story_text.pack(side="left", fill="both", expand=True)

        scroll = ttk.Scrollbar(story_frame, command=self.story_text.yview)
        scroll.pack(side="right", fill="y")
        self.story_text.configure(yscrollcommand=scroll.set)

    def _on_strip_canvas_resize(self, event):
        # Keep inner window height aligned; width auto based on content
        self.strip_canvas.itemconfig(self.strip_window_id, height=event.height)

    def _set_status(self, msg: str):
        self.status.config(text=msg)

    def _set_status_safe(self, msg: str):
        self.root.after(0, lambda: self._set_status(msg))

    # ---------------- Story ----------------
    def _append_story(self, sentence: str):
        self.story.append(sentence)
        self.story_text.delete("1.0", "end")
        self.story_text.insert("end", "\n".join(self.story))

    def on_reset(self):
        # If recording, stop it first
        if self.is_recording:
            self._stop_recording()

        self.story = []
        self.last_images = []
        self.story_text.delete("1.0", "end")
        self.multi_info.config(text="")
        self._clear_gallery()
        self._show_image(self.placeholder_path)
        self._set_status("Reset done")

    # ---------------- Recording toggle ----------------
    def on_toggle_record(self):
        if not self.is_recording:
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self):
        self.is_recording = True
        self.btn_record.config(text="⏹ Stop & procesează")
        self.btn_reset.config(state="disabled")  # avoid state weirdness while recording

        self._record_frames = []
        self._record_stop_event.clear()

        self._set_status("🎤 Înregistrare... apasă din nou ca să oprești")

        self._record_thread = threading.Thread(target=self._record_loop, daemon=True)
        self._record_thread.start()

    def _stop_recording(self):
        self.is_recording = False
        self.btn_record.config(state="disabled")  # disable until processing done
        self.btn_reset.config(state="normal")
        self._set_status("Procesez audio...")

        self._record_stop_event.set()

        # processing in another thread so UI stays responsive
        threading.Thread(target=self._process_recorded_audio, daemon=True).start()

    def _record_loop(self):
        stream = None
        try:
            stream = self._pa.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RATE,
                input=True,
                frames_per_buffer=self.CHUNK
            )

            while not self._record_stop_event.is_set():
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                self._record_frames.append(data)

        except Exception as e:
            self._finish_safe(f"Eroare microfon/record: {e}")
        finally:
            try:
                if stream is not None:
                    stream.stop_stream()
                    stream.close()
            except Exception:
                pass

    def _process_recorded_audio(self):
        try:
            if not self._record_frames:
                self._finish_safe("Nu s-a înregistrat nimic. Încearcă din nou.")
                return

            raw = b"".join(self._record_frames)

            # Convert to SpeechRecognition AudioData
            import speech_recognition as sr
            sample_width = self._pa.get_sample_size(self.FORMAT)
            audio = sr.AudioData(raw, self.RATE, sample_width)

            # STT
            self._set_status_safe("Transcriu (STT)...")
            text = self.svc2.rec.recognize_google(audio, language="ro-RO")

            if not text:
                self._finish_safe("Nu am obținut text. Încearcă din nou.")
                return

            if "stop" in text.lower():
                self._finish_safe("Ai spus STOP. (Folosește Reset dacă vrei să reiei.)")
                return

            # Keywords
            self._set_status_safe("Extrag keywords...")
            keywords = self.svc2.make_query(text)

            # Image search
            self._set_status_safe(f"Caut imagini pentru: {keywords!r} ...")
            image_result = self.svc3.get_image_for_query(keywords)

            if not image_result:
                image_result = self.svc3.get_placeholder_image()

            # Update UI
            self.root.after(0, lambda: self._apply_result(text, keywords, image_result))

            # TTS
            self._set_status_safe("Citesc propoziția (TTS)...")
            self.svc2.speak(text)

            self._set_status_safe("Ready")

        except Exception as e:
            self._finish_safe(f"Eroare procesare: {e}")
        finally:
            self.root.after(0, self._enable_record_button_ready)

    def _enable_record_button_ready(self):
        self.btn_record.config(state="normal", text="🎤 Start înregistrare")

    # ---------------- Apply result ----------------
    def _apply_result(self, text: str, keywords: str, image_result):
        # Story
        self._append_story(text)

        # Images
        paths = []
        if isinstance(image_result, list):
            paths = [p for p in image_result if p]
            self.multi_info.config(text=f"Multiple images: {len(paths)} | Keywords: {keywords}")
        else:
            paths = [image_result] if image_result else []
            self.multi_info.config(text=f"Keywords: {keywords}")

        # Choose main image
        main_path = None
        for p in paths:
            if p and os.path.exists(p):
                main_path = p
                break
        if not main_path:
            main_path = self.placeholder_path

        self._show_image(main_path)

        # Add to gallery strip (add ALL returned images; nice for demo)
        for p in paths:
            if p and os.path.exists(p):
                self._add_thumbnail(p)

    def _finish_safe(self, msg: str):
        def _finish():
            self._set_status(msg)
            self.btn_record.config(state="normal", text="🎤 Start înregistrare")
            self.btn_reset.config(state="normal")
            messagebox.showinfo("StoryBuilder", msg)
        self.root.after(0, _finish)

    # ---------------- TTS full story ----------------
    def on_read_story(self):
        if not self.story:
            messagebox.showinfo("StoryBuilder", "Povestea este goală.")
            return

        story_text = " ".join(self.story)
        threading.Thread(target=lambda: self.svc2.speak(story_text), daemon=True).start()

    # ---------------- Images (main) ----------------
    def _ensure_placeholder_exists(self):
        os.makedirs("images", exist_ok=True)
        self.placeholder_path = os.path.join("images", "placeholder.jpg")
        if not os.path.exists(self.placeholder_path):
            try:
                img = Image.new("RGB", (640, 480), color=(200, 200, 200))
                img.save(self.placeholder_path)
            except Exception:
                pass

    def _show_image(self, path: str):
        try:
            img = Image.open(path)
            img.thumbnail((780, 520))
            photo = ImageTk.PhotoImage(img)
            self.current_photo = photo
            self.image_label.config(image=photo, text="")
        except Exception as e:
            self.image_label.config(text=f"(Eroare imagine: {e})", image="")
            self.current_photo = None

    # ---------------- Gallery strip (thumbnails) ----------------
    def _clear_gallery(self):
        for child in self.strip_inner.winfo_children():
            child.destroy()
        self.thumb_photos.clear()
        self.strip_canvas.configure(scrollregion=(0, 0, 0, 0))

    def _add_thumbnail(self, img_path: str):
        try:
            img = Image.open(img_path).convert("RGB")

            # center-crop to square then resize
            w, h = img.size
            side = min(w, h)
            left = (w - side) // 2
            top = (h - side) // 2
            img = img.crop((left, top, left + side, top + side))
            img = img.resize((self.THUMB_SIZE, self.THUMB_SIZE))

            photo = ImageTk.PhotoImage(img)
            self.thumb_photos.append(photo)  # keep ref

            # frame as "tile" with padding + border
            tile = ttk.Frame(self.strip_inner, padding=4, relief="ridge")
            tile.pack(side="left", padx=6, pady=6)

            lbl = ttk.Label(tile, image=photo)
            lbl.pack()

            # optional: click thumbnail to show as main image
            lbl.bind("<Button-1>", lambda e, p=img_path: self._show_image(p))

        except Exception:
            # ignore thumbnail errors
            pass

    # ---------------- Close ----------------
    def _on_close(self):
        try:
            if self.is_recording:
                self._record_stop_event.set()
        except Exception:
            pass

        try:
            self._pa.terminate()
        except Exception:
            pass

        self.root.destroy()

    # ---------------- Run ----------------
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = StoryBuilderApp()
    app.run()
