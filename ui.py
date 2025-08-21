import customtkinter as ctk
import main

# ---------------- ctk --------------------
WIDTH = 800
HEIGHT = 600

# ------------------ CUSTOMTKINTER ------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry(f"{WIDTH}x{HEIGHT}")
app.title("Repetitioner")

# ------------------ WIDGETS ------------------
label_timer = ctk.CTkLabel(app, text="Готов?")
button_start = ctk.CTkButton(app, text="Начать")
txt_words = ctk.CTkTextbox(app, height=120)
entry = ctk.CTkEntry(app, placeholder_text="Введите слова через пробел")
button_check = ctk.CTkButton(app, text="Проверить")
label_result = ctk.CTkLabel(app, text="")

# ------------------ STATE ------------------
session_words = ""
timer_job = None
time_left = 60
SESSION_TIME = 60


def start_session():
    global session_words, timer_job, time_left
    label_result.configure(text="")
    entry.delete(0, "end")
    entry.pack_forget()
    button_start.pack_forget()
    txt_words.configure(state="normal")
    txt_words.delete("1.0", "end")

    nowadays = main.return_all_words()
    todays = main.nowaday_words(nowadays)

    if not todays.strip():
        txt_words.insert("1.0", "(слов нет)")
        txt_words.configure(state="disabled")
        return

    session_words = todays.split()
    txt_words.insert("1.0", "\n".join(session_words))
    txt_words.configure(state="disabled")

# ---------------- UI ----------------
def ui():
    global label_timer, button_start, txt_words, entry, button_check, label_result

    frame = ctk.CTkFrame(app, corner_radius=10)
    frame.pack(padx=20, pady=20, fill="both", expand=True)

    label_timer = ctk.CTkLabel(frame, text="Готов?")
    label_timer.pack(pady=8)

    button_start = ctk.CTkButton(frame, text="Начать", command=start_session)
    button_start.pack(pady=6)

    txt_words = ctk.CTkTextbox(frame, height=120)
    txt_words.pack(fill="x", padx=8, pady=6)

    entry = ctk.CTkEntry(frame, placeholder_text="Введите слова через пробел")
    button_check = ctk.CTkButton(frame, text="Проверить")

    label_result = ctk.CTkLabel(frame, text="")
    label_result.pack(pady=6)


if __name__ == "__main__":
    ui()
    app.mainloop()
