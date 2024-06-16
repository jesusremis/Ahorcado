import tkinter as tk
from PIL import Image, ImageTk
import random
from unidecode import unidecode

# Función para cargar y filtrar palabras del diccionario
def cargar_palabras():
    with open("palabras.txt", "r", encoding="utf-8") as f:
        palabras = [line.strip().upper() for line in f if len(line.strip()) >= 6]
    return palabras

# Lista de palabras para el juego y conjunto para registrar las palabras ya seleccionadas
all_words = cargar_palabras()
selected_words = set()

def obtener_palabra():
    palabra = random.choice(all_words)
    while palabra in selected_words:
        palabra = random.choice(all_words)
    selected_words.add(palabra)
    return palabra

def iniciar_juego():
    global selected_word, guessed_word, attempts, play_again_button
    selected_word = obtener_palabra()
    guessed_word = ["_" for _ in selected_word]
    attempts = 6
    play_again_button.pack_forget()
    entry.config(state='normal', width=2)
    guess_button.config(state='normal')
    guess_word_button.config(state='normal')
    update_display()

def update_display():
    display_word.set(" ".join(guessed_word))
    display_attempts.set(f"Intentos restantes: {attempts}")
    display_message.set("")

def guess_letter():
    global attempts
    letter = entry.get().strip().upper()  # Convertir a mayúsculas
    entry.delete(0, tk.END)
    
    if len(letter) == 1:  # Adivinando una letra
        if unidecode(letter) in unidecode(selected_word):  # Convertir a ASCII para manejar tildes
            for i, char in enumerate(selected_word):
                if unidecode(char) == unidecode(letter):
                    guessed_word[i] = char
        else:
            attempts -= 1
    else:  # Adivinando la palabra completa
        if unidecode(letter) == unidecode(selected_word):
            for i, char in enumerate(selected_word):
                guessed_word[i] = char
        else:
            attempts -= 1
            entry.config(width=2)  # Volver a la opción de adivinar solo letra

    update_display()
    
    if "_" not in guessed_word:
        display_message.set("¡Felicidades!\nHas adivinado la palabra:\n" + selected_word)
        end_game()
    elif attempts == 0:
        display_message.set(f"Has perdido.\nLa palabra era:\n{selected_word}")
        end_game()

def enable_word_guess():
    entry.config(width=20)

def end_game():
    entry.config(state='disabled')
    guess_button.config(state='disabled')
    guess_word_button.config(state='disabled')
    play_again_button.pack(pady=10)

root = tk.Tk()
root.title("Juego del Ahorcado")
root.geometry("600x400")  # Tamaño de la ventana

# Cambiar el icono de la ventana
root.iconbitmap("icono.ico")

# Marco principal
frame = tk.Frame(root)
frame.pack(expand=True, fill=tk.BOTH)

# Submarcos para la imagen y la información del juego
left_frame = tk.Frame(frame)
left_frame.pack(side=tk.LEFT, padx=20, pady=20)

right_frame = tk.Frame(frame)
right_frame.pack(side=tk.RIGHT, padx=20, pady=20)

# Cargar imagen
image = Image.open("imagen.jpg")  # Reemplaza "imagen.jpg" con la ruta de tu imagen
photo = ImageTk.PhotoImage(image)
img_label = tk.Label(left_frame, image=photo)
img_label.pack()

display_word = tk.StringVar()
display_attempts = tk.StringVar()
display_message = tk.StringVar()

tk.Label(right_frame, textvariable=display_word, font=("Helvetica", 20)).pack(pady=10)
tk.Label(right_frame, textvariable=display_attempts, font=("Helvetica", 14)).pack(pady=5)
tk.Label(right_frame, textvariable=display_message, font=("Helvetica", 14), fg="red").pack(pady=10)

entry = tk.Entry(right_frame, font=("Helvetica", 14), width=2)  # Campo de texto para una sola letra
entry.pack(pady=10)
entry.bind("<Return>", lambda event: guess_letter())

guess_button = tk.Button(right_frame, text="Adivinar letra", command=guess_letter, font=("Helvetica", 14))
guess_button.pack(pady=10)

guess_word_button = tk.Button(right_frame, text="Adivinar palabra completa", command=enable_word_guess, font=("Helvetica", 14))
guess_word_button.pack(pady=10)

play_again_button = tk.Button(left_frame, text="Jugar de Nuevo", command=iniciar_juego, font=("Helvetica", 14))

iniciar_juego()  # Iniciar el primer juego

root.mainloop()