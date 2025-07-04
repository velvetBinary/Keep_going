import os
import datetime
import customtkinter as ctk
import threading
from fpdf import FPDF
import pygame
import time

# --- CONFIG ---

# Music file (optional)
MUSIC_FILE = "soft_piano.mp3"

# File to store responses
storage_file = "responses.txt"

# --- INIT ---

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
pygame.init()

# --- GUI SETUP ---

app = ctk.CTk()
app.title("🕯️ The Sacrifice Mirror")
app.geometry("800x700")

title = ctk.CTkLabel(app, text="Tell Me What You Let Go", font=("Georgia", 26, "bold"))
title.pack(pady=20)

entry1 = ctk.CTkEntry(app, placeholder_text="What did you sacrifice?", width=600)
entry1.pack(pady=10)

entry2 = ctk.CTkEntry(app, placeholder_text="Why did you have to make it?", width=600)
entry2.pack(pady=10)

entry3 = ctk.CTkEntry(app, placeholder_text="How hard was it emotionally?", width=600)
entry3.pack(pady=10)

result_label = ctk.CTkLabel(app, text="", font=("Courier New", 15), wraplength=700, justify="left")
result_label.pack(pady=30)

# --- FUNCTIONS ---

def store_data(sacrifice, reason, difficulty):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(storage_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}]\nSacrifice: {sacrifice}\nReason: {reason}\nDifficulty: {difficulty}\n\n")


def generate_poem(sacrifice, reason, difficulty):
    poem = f"""
🕯️ A Poem Just For You

You gave up your light —  
"{sacrifice}" — a dream sewn tight.  
For love, for loss, for sleepless nights,  
You chose the shadows, hid your might.  

You told me:  
> "{reason}"  
In those words — a universe  
Of grief and grit, wound and verse.  

You said it was:  
> "{difficulty}"  
That line alone could break the sky,  
But still you rose and did not cry  
For pity. No — just cried to feel,  
Then stitched yourself with time to heal.  

You, who gave when no one knew,  
Walk with pain, but walk through too.  
Not all warriors hold a sword —  
Some just keep walking forward.
    """
    return poem.strip()


def typewriter_effect(text, label):
    label.configure(text="")
    displayed = ""
    for char in text:
        displayed += char
        label.configure(text=displayed)
        app.update()
        time.sleep(0.01)


def on_submit():
    sacrifice = entry1.get().strip()
    reason = entry2.get().strip()
    difficulty = entry3.get().strip()

    if not (sacrifice and reason and difficulty):
        result_label.configure(text="Please fill in all fields.", text_color="red")
        return

    store_data(sacrifice, reason, difficulty)
    poem = generate_poem(sacrifice, reason, difficulty)

    # Save poem globally for reuse/export
    global current_poem
    current_poem = poem

    threading.Thread(target=lambda: typewriter_effect(poem, result_label)).start()


def regenerate_poem():
    if current_poem:
        threading.Thread(target=lambda: typewriter_effect(current_poem, result_label)).start()


def export_to_pdf():
    if not current_poem:
        return
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in current_poem.split("\n"):
        pdf.multi_cell(0, 10, txt=line)

    pdf.output("your_poem.pdf")


def toggle_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        music_button.configure(text="Play Music")
    else:
        try:
            pygame.mixer.music.load(MUSIC_FILE)
            pygame.mixer.music.play(-1)
            music_button.configure(text="Pause Music")
        except:
            result_label.configure(text="Could not load music file.", text_color="red")

# --- BUTTONS ---

button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

submit_btn = ctk.CTkButton(button_frame, text="Submit & Get Poem", command=on_submit)
submit_btn.grid(row=0, column=0, padx=10)

regen_btn = ctk.CTkButton(button_frame, text="Generate Again", command=regenerate_poem)
regen_btn.grid(row=0, column=1, padx=10)

export_btn = ctk.CTkButton(button_frame, text="Export to PDF", command=export_to_pdf)
export_btn.grid(row=0, column=2, padx=10)

music_button = ctk.CTkButton(app, text="Play Music", command=toggle_music)
music_button.pack(pady=5)

# --- STATE ---
current_poem = ""

app.mainloop()

