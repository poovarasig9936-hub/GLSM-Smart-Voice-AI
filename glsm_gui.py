from assistant_core import process_command
from voice_input import listen
from voice_output import speak

import tkinter as tk
import threading
from PIL import Image, ImageTk

def speak_thread(text):
    threading.Thread(
        target=speak,
        args=(text,),
        daemon=True
    ).start()

root = tk.Tk()
root.title("GLSM Coding AI")
root.geometry("820x940")  # Window width increased to accommodate side panels
root.configure(bg="#0b0b0b")

# =========================
# MAIN LAYOUT WITH SIDE PANELS
# =========================
main_container = tk.Frame(root, bg="#0b0b0b")
main_container.pack(fill="both", expand=True, padx=10, pady=10)

# Left Side Decorative Panel (Tech Lines / Binary vibe)
left_panel = tk.Frame(main_container, bg="#110500", width=60)
left_panel.pack(side=tk.LEFT, fill="y", padx=(0, 8))
left_panel.pack_propagate(False)

left_label = tk.Label(
    left_panel, 
    text="G\nL\nS\nM\n\nC\nO\nD\nE\n\nA\nI", 
    font=("Consolas", 11, "bold"), 
    fg="#ff4500", 
    bg="#110500"
)
left_label.pack(expand=True)

# Center Glow Card Frame (Original design)
center_wrapper = tk.Frame(main_container, bg="#0b0b0b")
center_wrapper.pack(side=tk.LEFT, fill="both", expand=True)

glow_frame3 = tk.Frame(center_wrapper, bg="#331100")
glow_frame3.pack(fill="both", expand=True)

glow_frame2 = tk.Frame(glow_frame3, bg="#992600")
glow_frame2.pack(fill="both", expand=True, padx=3, pady=3)

glow_frame1 = tk.Frame(glow_frame2, bg="#ff4500")
glow_frame1.pack(fill="both", expand=True, padx=3, pady=3)

card_frame = tk.Frame(glow_frame1, bg="#141414")
card_frame.pack(fill="both", expand=True, padx=3, pady=3)

# Right Side Decorative Panel (Tech Lines / Status vibe)
right_panel = tk.Frame(main_container, bg="#110500", width=60)
right_panel.pack(side=tk.LEFT, fill="y", padx=(8, 0))
right_panel.pack_propagate(False)

right_label = tk.Label(
    right_panel, 
    text="▲\nN\nE\nO\nN\n\nV\n1\n.\n0\n▼", 
    font=("Consolas", 10, "bold"), 
    fg="#ff4500", 
    bg="#110500"
)
right_label.pack(expand=True)

# =========================
# INNER CONTENT
# =========================
title_label = tk.Label(
    card_frame,
    text="GLSM Coding AI",
    font=("Arial", 22, "bold"),
    fg="white",
    bg="#141414"
)
title_label.pack(pady=(15, 5))

img_outer_frame = tk.Frame(card_frame, bg="#ff3300", padx=3, pady=3)
img_outer_frame.pack(pady=10)

image_path = "naruto.png"
img_label = None
bounce_y = 0
bounce_direction = 1

try:
    original_img = Image.open(image_path)
    original_img = original_img.resize((140, 170), Image.Resampling.LANCZOS)
    naruto_img = ImageTk.PhotoImage(original_img)
    
    img_label = tk.Label(img_outer_frame, image=naruto_img, bg="#141414")
    img_label.image = naruto_img
    img_label.pack()
except Exception as e:
    print("Image load aagala: ", e)

def animate_image():
    global bounce_y, bounce_direction
    bounce_y += bounce_direction * 1
    if abs(bounce_y) >= 4:
        bounce_direction *= -1
    img_outer_frame.pack_configure(pady=(10 + int(bounce_y), 10 - int(bounce_y)))
    root.after(90, animate_image)

root.after(90, animate_image)

ai_text = tk.Label(
    card_frame,
    text="AI: Here is the Factorial program loaded from your project files.",
    font=("Arial", 11, "bold"),
    fg="#ffcc00",
    bg="#141414",
    wraplength=520,
    justify="center"
)
ai_text.pack(pady=8)

input_frame = tk.Frame(card_frame, bg="#141414")
input_frame.pack(pady=5)

input_box = tk.Entry(
    input_frame,
    width=30,
    font=("Arial", 13),
    bg="#222222",
    fg="white",
    insertbackground="white",
    relief="flat"
)
input_box.pack(side=tk.LEFT, padx=5, ipady=7)
input_box.insert(0, "Type command...")

def on_click(event):
    if input_box.get() == "Type command...":
        input_box.delete(0, tk.END)
        input_box.config(fg="white")

input_box.bind("<FocusIn>", on_click)

def send_message():
    user_text = input_box.get().strip()
    if user_text == "" or user_text == "Type command...":
        return

    try:
        result = process_command(user_text)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, str(result))
        speak_thread("The program output is " + str(result))
    except Exception as error:
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "Error:\n" + str(error))
        speak_thread("There is an error")

    input_box.delete(0, tk.END)

send_button = tk.Button(
    input_frame,
    text="Send",
    width=8,
    font=("Arial", 11, "bold"),
    bg="#28a745",
    fg="white",
    relief="flat",
    command=send_message
)
send_button.pack(side=tk.LEFT, padx=5)

def run_voice_process():
    ai_text.config(text="AI: Listening...")
    root.update()
    try:
        voice_text = listen()
        if voice_text:
            ai_text.config(text=f"AI: You said '{voice_text}'")
            input_box.delete(0, tk.END)
            input_box.insert(0, voice_text)
            root.update()
            send_message()
        else:
            speak_thread("Voice not understood")
            ai_text.config(text="AI: Voice not understood.")
    except Exception as error:
        ai_text.config(text="AI: Voice Error occurred.")

def voice_command():
    threading.Thread(target=run_voice_process, daemon=True).start()

voice_button = tk.Button(
    card_frame,
    text="🎙️ Tap to Speak",
    width=38,
    font=("Arial", 13, "bold"),
    bg="#ff4500",
    fg="white",
    relief="flat",
    command=voice_command
)
voice_button.pack(pady=8, ipady=8)

output_box = tk.Text(
    card_frame,
    height=12,
    width=65,
    font=("Consolas", 10),
    bg="#0d0d0d",
    fg="#00ff66",
    relief="solid",
    bd=1
)
output_box.pack(pady=(5, 20))
output_box.insert(tk.END, "# factorial.py is currently empty. Add your code here!")

root.bind("<Return>", lambda event: send_message())

root.mainloop()