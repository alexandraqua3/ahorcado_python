#!/usr/bin/env python3
"""
Ahorcado - Juego educativo para grado undécimo
Usa solo librerías estándar: tkinter y random
Archivo único: ahorcado.py

Funciones principales (arquitectura modular requerida):
- configurar_partida()
- dibujar_monigote(errores)
- verificar_letra(letra)
- mostrar_resultado(victoria)
- reiniciar_juego()

Variables descriptivas en español.
"""

import random
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont

# ---------------------------
# Diccionario de palabras
# Cada categoría contiene una lista de tuplas: (PALABRA, PISTA)
# Las palabras en mayúsculas para facilitar comparaciones.
# ---------------------------
PALABRAS = {
    "Animales": [
        ("PERRO", "Sustantivo"),
        ("ELEFANTE", "Sustantivo"),
        ("GATO", "Sustantivo"),
        ("JIRAFA", "Sustantivo"),
        ("TIBURON", "Sustantivo"),
    ],
    "Profesiones": [
        ("MEDICO", "Sustantivo"),
        ("INGENIERO", "Sustantivo"),
        ("MAESTRO", "Sustantivo"),
        ("ARQUITECTO", "Sustantivo"),
        ("ENFERMERA", "Sustantivo"),
    ],
    "Frutas": [
        ("MANZANA", "Sustantivo"),
        ("BANANO", "Sustantivo"),
        ("NARANJA", "Sustantivo"),
        ("FRESA", "Sustantivo"),
        ("MANGO", "Sustantivo"),
    ],
}

# ---------------------------
# Estado de la partida (globales controladas por funciones)
# ---------------------------
palabra_secreta = ""
pista_actual = ""
palabra_mostrar = []  # lista de caracteres o '_' para mostrar
intentos_maximos = 6
intentos_restantes = 0
errores = 0
letras_botones = {}  # mapa letra -> botón para deshabilitar
palabras_ganadas = 0
palabras_perdidas = 0
partida_activa = False

# ---------------------------
# Inicialización de la GUI
# ---------------------------
root = tk.Tk()
root.title("El Ahorcado - Aprende y defiende tu proyecto")
root.resizable(False, False)

# Fuentes legibles para estudiantes
fuente_palabra = ("Helvetica", 28, "bold")
fuente_info = ("Helvetica", 12)
fuente_botones = ("Helvetica", 10)

# Variables de control para OptionMenus
categoria_var = tk.StringVar(value=list(PALABRAS.keys())[0])
dificultad_var = tk.StringVar(value="Normal")

# Marco superior con controles
frame_top = tk.Frame(root, pady=8)
frame_top.pack(fill=tk.X)

# Controles: Categoría y Dificultad
tk.Label(frame_top, text="Categoría:", font=fuente_info).pack(side=tk.LEFT, padx=(6,2))
categoria_om = tk.OptionMenu(frame_top, categoria_var, *PALABRAS.keys())
categoria_om.config(font=fuente_info)
categoria_om.pack(side=tk.LEFT)

# Dificultad: Fácil -> 8 intentos, Normal -> 6 intentos
tk.Label(frame_top, text="   Dificultad:", font=fuente_info).pack(side=tk.LEFT, padx=(12,2))
dificultad_om = tk.OptionMenu(frame_top, dificultad_var, "Fácil", "Normal", "Difícil")
dificultad_om.config(font=fuente_info)
dificultad_om.pack(side=tk.LEFT)

# Marcadores: Ganadas, Perdidas, Pista
label_ganadas = tk.Label(frame_top, text="Ganadas: 0", font=fuente_info)
label_ganadas.pack(side=tk.RIGHT, padx=8)
label_perdidas = tk.Label(frame_top, text="Perdidas: 0", font=fuente_info)
label_perdidas.pack(side=tk.RIGHT)

label_pista = tk.Label(root, text="Pista: ", font=fuente_info, anchor="w")
label_pista.pack(fill=tk.X, padx=8)

# Panel principal dividido: Canvas izquierdo y controles derecho
frame_main = tk.Frame(root, padx=8, pady=8)
frame_main.pack()

# Canvas para dibujar la horca (panel izquierdo)
canvas_width = 320
canvas_height = 320
canvas = tk.Canvas(frame_main, width=canvas_width, height=canvas_height, bg="#f7f7f7", highlightthickness=1, highlightbackground="#cccccc")
canvas.grid(row=0, column=0, rowspan=2, padx=(0,12))

# Panel derecho: palabra y teclas
frame_right = tk.Frame(frame_main)
frame_right.grid(row=0, column=1, sticky="n")

label_palabra = tk.Label(frame_right, text="_ _ _ _ _", font=fuente_palabra)
label_palabra.pack(pady=(10,12))

# Grid de botones de la A a la Z
frame_teclado = tk.Frame(frame_right)
frame_teclado.pack()

# Botón reiniciar
btn_nueva = tk.Button(root, text="Nueva ronda", font=fuente_info, command=lambda: reiniciar_juego())
btn_nueva.pack(pady=(8,10))

# ---------------------------
# Funciones requeridas
# ---------------------------

def configurar_partida():
    """Configura una nueva partida según categoría y dificultad seleccionadas.

    Lee `categoria_var` y `dificultad_var`, escoge una palabra aleatoria,
    inicializa `palabra_mostrar`, `intentos_restantes`, `errores` y actualiza la GUI.
    """
    global palabra_secreta, pista_actual, palabra_mostrar, intentos_maximos, intentos_restantes, errores

    # Selección de palabra aleatoria de la categoría
    categoria = categoria_var.get()
    lista = PALABRAS.get(categoria, [])
    palabra_secreta, pista_actual = random.choice(lista)

    # Dificultad -> intentos máximos
    # Ajuste de intentos según la dificultad seleccionada
    if dificultad_var.get() == "Fácil":
        intentos_maximos = 8
    elif dificultad_var.get() == "Normal":
        intentos_maximos = 6
    else:  # "Difícil"
        intentos_maximos = 4

    # Reinicio de estado de la partida
    intentos_restantes = intentos_maximos
    errores = 0

    # Crear la representación visible con '_' para letras no adivinadas
    palabra_mostrar = ["_" if c.isalpha() else c for c in palabra_secreta]

    # Actualizar la GUI
    # Mostrar pista según dificultad: en Fácil mostramos tipo gramatical,
    # en Normal/Difícil mostramos solo la categoría general.
    if dificultad_var.get() == "Fácil":
        label_pista.config(text=f"Pista: {pista_actual}     Intentos: {intentos_restantes}")
    else:
        label_pista.config(text=f"Categoría: {categoria}     Intentos: {intentos_restantes}")
    actualizar_etiqueta_palabra()
    canvas.delete("all")
    dibujar_monigote(errores)

    # Habilitar botones de letras
    for letra, boton in letras_botones.items():
        boton.config(state=tk.NORMAL)
    # Bloqueamos las opciones para evitar cambiar categoría/dificultad durante la ronda
    categoria_om.config(state=tk.DISABLED)
    dificultad_om.config(state=tk.DISABLED)
    # Indicador de partida activa
    global partida_activa
    partida_activa = True


def dibujar_monigote(errores_local):
    """Dibuja la horca/monigote según el número de errores.

    Usamos `create_line` y `create_oval`. Cada `if` añade una parte nueva.
    Este diseño permite explicar `if/else` y la secuencia de pasos.
    """
    # Limpiamos y dibujamos la estructura base (poste)
    canvas.delete("all")
    # Base
    canvas.create_line(40, 300, 200, 300, width=4, fill="#654321")
    # Poste vertical
    canvas.create_line(80, 300, 80, 40, width=4, fill="#654321")
    # Viga superior
    canvas.create_line(80, 40, 200, 40, width=4, fill="#654321")
    # Cuerda
    canvas.create_line(200, 40, 200, 80, width=2, fill="#333333")

    # Partes del monigote según errores: cabeza, torso, brazos, piernas, detalles
    # Explicación para estudiantes: los condicionales `if errores_local >= N` añaden partes
    if errores_local >= 1:
        # Cabeza
        canvas.create_oval(180, 80, 220, 120, width=2, fill="#ffe6cc")
    if errores_local >= 2:
        # Torso
        canvas.create_line(200, 120, 200, 200, width=3)
    if errores_local >= 3:
        # Brazo izquierdo
        canvas.create_line(200, 140, 170, 170, width=3)
    if errores_local >= 4:
        # Brazo derecho
        canvas.create_line(200, 140, 230, 170, width=3)
    if errores_local >= 5:
        # Pierna izquierda
        canvas.create_line(200, 200, 175, 250, width=3)
    if errores_local >= 6:
        # Pierna derecha
        canvas.create_line(200, 200, 225, 250, width=3)
    if errores_local >= 7:
        # Ojo izquierdo (detalle)
        canvas.create_oval(190, 92, 195, 97, fill="#000000")
    if errores_local >= 8:
        # Ojo derecho (detalle)
        canvas.create_oval(205, 92, 210, 97, fill="#000000")


def verificar_letra(letra):
    """Procesa la letra elegida, actualiza estado y GUI.

    - Si la letra está en `palabra_secreta`, revela las posiciones.
    - Si no, incrementa `errores` y reduce `intentos_restantes`.
    - Deshabilita el botón correspondiente para evitar reintentos.
    """
    global intentos_restantes, errores, palabras_ganadas, palabras_perdidas

    letra = letra.upper()

    # Deshabilitar el botón (si existe)
    boton = letras_botones.get(letra)
    if boton:
        boton.config(state=tk.DISABLED)

    # Si la letra ya fue procesada, no hacemos nada
    # (Por ejemplo, desde el teclado se podría repetir)
    if letra not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return

    # Comprobar si la letra está en la palabra secreta
    if letra in palabra_secreta:
        # Reemplazar '_' por la letra en todas las posiciones correctas
        for i, ch in enumerate(palabra_secreta):
            if ch == letra:
                palabra_mostrar[i] = letra
        actualizar_etiqueta_palabra()

        # Verificar victoria: si no quedan '_' -> victoria
        if "_" not in palabra_mostrar:
            palabras_ganadas += 1
            mostrar_resultado(True)
    else:
        # Letra incorrecta -> aumentan errores
        errores += 1
        intentos_restantes -= 1
        dibujar_monigote(errores)

        # Mostrar intentos restantes en la pista (como ejemplo de actualización)
        label_pista.config(text=f"Pista: {pista_actual}     Intentos restantes: {intentos_restantes}")

        # Si se agotaron los intentos, el jugador pierde
        if intentos_restantes <= 0:
            palabras_perdidas += 1
            mostrar_resultado(False)


def mostrar_resultado(victoria):
    """Gestiona el final de la ronda: muestra mensaje, actualiza marcadores y bloquea el teclado.

    `victoria` es True si el jugador adivinó la palabra.
    """
    # Bloquear todos los botones del teclado
    for boton in letras_botones.values():
        boton.config(state=tk.DISABLED)

    if victoria:
        messagebox.showinfo("¡Victoria!", f"¡Felicidades! Adivinaste: {palabra_secreta}")
    else:
        messagebox.showinfo("Derrota", f"Se han agotado los intentos. La palabra era: {palabra_secreta}")

    # Actualizar contadores visibles
    label_ganadas.config(text=f"Ganadas: {palabras_ganadas}")
    label_perdidas.config(text=f"Perdidas: {palabras_perdidas}")
    # Permitir cambiar categoría/dificultad antes de la siguiente ronda
    categoria_om.config(state=tk.NORMAL)
    dificultad_om.config(state=tk.NORMAL)
    # Marcamos la partida como inactiva para la lógica del juego
    global partida_activa
    partida_activa = False


def reiniciar_juego():
    """Prepara la interfaz para una nueva ronda pero mantiene la puntuación general.

    Limpia el `canvas`, rehabilita los botones y llama a `configurar_partida()`.
    """
    # Habilitar botones de letras
    for letra, boton in letras_botones.items():
        boton.config(state=tk.NORMAL)

    configurar_partida()


# ---------------------------
# Utilidades de GUI
# ---------------------------

def actualizar_etiqueta_palabra():
    """Actualiza `label_palabra` con espacios entre letras para mejor lectura."""
    texto = " ".join(palabra_mostrar)
    label_palabra.config(text=texto)


# Crear botones de la A a la Z en una cuadrícula
letras = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
cols = 9
for idx, letra in enumerate(letras):
    r = idx // cols
    c = idx % cols
    btn = tk.Button(frame_teclado, text=letra, width=3, height=2, font=fuente_botones,
                    command=lambda l=letra: verificar_letra(l))
    btn.grid(row=r, column=c, padx=2, pady=2)
    letras_botones[letra] = btn


# Manejar eventos de teclado físico
def on_tecla(event):
    """Convierte la tecla presionada a letra y la procesa con `verificar_letra`.

    Aquí se ve un ejemplo de manejo de eventos: `root.bind("<Key>", on_tecla)`.
    """
    char = event.char.upper()
    if char and char in letras_botones:
        # Llamamos a la misma función que usa el botón para mantener lógica unificada
        verificar_letra(char)


root.bind("<Key>", on_tecla)

# Inicializar y arrancar la primera partida
configurar_partida()

# Iniciar el bucle principal de Tkinter
if __name__ == "__main__":
    root.mainloop()
