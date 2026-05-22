import asyncio
import threading
import customtkinter as ctk
from tkinter import messagebox, filedialog
import edge_tts

class EdgeTTSApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("TTX")
        self.geometry("600x700")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Türkçe Ses Seçenekleri
        self.voices = {
            "Ahmet (Erkek)": "tr-TR-AhmetNeural",
            "Emel (Kadın)": "tr-TR-EmelNeural"
        }

        self.init_ui()

    def init_ui(self):
        # 1. Metin Girişi
        self.lbl_text = ctk.CTkLabel(self, text="Seslendirilecek Metin:", font=("Arial", 14, "bold"))
        self.lbl_text.pack(pady=(20, 5), padx=20, anchor="w")

        self.txt_input = ctk.CTkTextbox(self, height=150)
        self.txt_input.pack(fill="x", padx=20, pady=5)

        # 2. Ses Seçimi
        self.lbl_voice = ctk.CTkLabel(self, text="Ses Seçimi:", font=("Arial", 12, "bold"))
        self.lbl_voice.pack(pady=(15, 5), padx=20, anchor="w")
        
        self.cmb_voice = ctk.CTkComboBox(self, values=list(self.voices.keys()))
        self.cmb_voice.pack(fill="x", padx=20, pady=5)
        self.cmb_voice.set("Ahmet (Erkek)")

        # 3. Hız Ayarı (Rate)
        self.lbl_rate = ctk.CTkLabel(self, text="Hız (Rate): Normal (%0)", font=("Arial", 12, "bold"))
        self.lbl_rate.pack(pady=(15, 5), padx=20, anchor="w")
        
        self.sld_rate = ctk.CTkSlider(self, from_=-50, to=50, command=self.update_rate_label)
        self.sld_rate.pack(fill="x", padx=20, pady=5)
        self.sld_rate.set(0)

        # 4. Perde Ayarı (Pitch)
        self.lbl_pitch = ctk.CTkLabel(self, text="Perde (Pitch): Normal (0Hz)", font=("Arial", 12, "bold"))
        self.lbl_pitch.pack(pady=(15, 5), padx=20, anchor="w")
        
        self.sld_pitch = ctk.CTkSlider(self, from_=-50, to=50, command=self.update_pitch_label)
        self.sld_pitch.pack(fill="x", padx=20, pady=5)
        self.sld_pitch.set(0)

        # 5. Dönüştür ve Kaydet Butonu
        self.btn_save = ctk.CTkButton(self, text="Ses Dosyası Olarak Kaydet (MP3)", command=self.start_generation_thread, font=("Arial", 14, "bold"))
        self.btn_save.pack(fill="x", padx=20, pady=30)

    def update_rate_label(self, value):
        val = int(value)
        sign = "+" if val > 0 else ""
        self.lbl_rate.configure(text=f"Hız (Rate): {sign}{val}%")

    def update_pitch_label(self, value):
        val = int(value)
        sign = "+" if val > 0 else ""
        self.lbl_pitch.configure(text=f"Perde (Pitch): {sign}{val}Hz")

    async def save_audio_async(self, text, voice, rate_str, pitch_str, file_path):
        communicate = edge_tts.Communicate(text, voice, rate=rate_str, pitch=pitch_str)
        await communicate.save(file_path)

    def start_generation_thread(self):
        """Butona tıklandığında işlemi arayüzü kilitlememesi için ayrı bir Thread'de başlatır."""
        text = self.txt_input.get("1.0", "end-1c").strip()
        if not text:
            messagebox.showwarning("Uyarı", "Lütfen seslendirilecek bir metin girin.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".mp3",
            filetypes=[("MP3 Files", "*.mp3")],
            title="Ses Dosyasını Kaydet"
        )
        
        if not file_path:
            return

        selected_voice_key = self.cmb_voice.get()
        voice = self.voices[selected_voice_key]
        
        rate_val = int(self.sld_rate.get())
        rate_str = f"{'+' if rate_val >= 0 else ''}{rate_val}%"
        
        pitch_val = int(self.sld_pitch.get())
        pitch_str = f"{'+' if pitch_val >= 0 else ''}{pitch_val}Hz"

        # Butonu işlem bitene kadar devre dışı bırakalım
        self.btn_save.configure(state="disabled", text="İşleniyor...")

        # Yeni iş parçacığını (Thread) oluşturup başlatıyoruz
        threading.Thread(
            target=self.run_async_task, 
            args=(text, voice, rate_str, pitch_str, file_path), 
            daemon=True
        ).start()

    def run_async_task(self, text, voice, rate_str, pitch_str, file_path):
        """Thread içinde çalışan ve asenkron döngüyü güvenli bir şekilde başlatan metot."""
        try:
            # Yeni ve temiz bir olay döngüsü oluşturup çalıştırıyoruz
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.save_audio_async(text, voice, rate_str, pitch_str, file_path))
            loop.close()
            
            messagebox.showinfo("Başarılı", "Ses dosyası başarıyla oluşturuldu ve kaydedildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"Ses oluşturulurken bir hata oluştu:\n{e}")
        finally:
            # İşlem bittiğinde butonu tekrar aktif hale getiriyoruz
            self.btn_save.configure(state="normal", text="Ses Dosyası Olarak Kaydet (MP3)")

if __name__ == "__main__":
    app = EdgeTTSApp()
    app.mainloop()
