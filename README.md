# ahorcado_python

Juego educativo del Ahorcado implementado en un único archivo `ahorcado.py` usando solo librerías estándar (`tkinter`, `random`). Diseñado para estudiantes de secundaria (grado 11): código modular, legible y con comentarios para defensa académica.

## Estructura del proyecto

- `ahorcado.py` : Código fuente único con la GUI y la lógica del juego.

## Funciones principales (explicación breve)

- `configurar_partida()`:
  - Inicializa la partida leyendo la `categoria_var` y `dificultad_var`.
  - Escoge aleatoriamente una palabra de `PALABRAS` y prepara `palabra_mostrar`.
  - Ajusta `intentos_maximos` según la dificultad (Fácil:8, Normal:6, Difícil:4).
  - Actualiza la interfaz (pista o categoría visible) y deshabilita opciones para evitar cambios durante la ronda.

- `dibujar_monigote(errores)`:
  - Dibuja la horca y las partes del monigote en el `Canvas` según `errores`.
  - Usa condicionales `if errores_local >= N` para añadir partes progresivamente.

- `verificar_letra(letra)`:
  - Procesa una letra (clic o teclado físico) y deshabilita su botón.
  - Si la letra está en `palabra_secreta`, actualiza `palabra_mostrar` mediante un `for`.
  - Si es incorrecta, incrementa `errores` y reduce `intentos_restantes`.
  - Llama a `mostrar_resultado()` cuando hay victoria o se agotan los intentos.

- `mostrar_resultado(victoria)`:
  - Informa al jugador con un diálogo (`messagebox`) y actualiza los contadores `palabras_ganadas` / `palabras_perdidas`.
  - Habilita las opciones de categoría/dificultad para la siguiente ronda.

- `reiniciar_juego()`:
  - Rehabilita botones y lanza `configurar_partida()` para iniciar una nueva ronda.

### Variables clave

- `PALABRAS` : Diccionario por categorías. Cada entrada es una lista de tuplas `(PALABRA, TIPO_GRAMATICAL)`.
- `palabra_secreta`, `pista_actual` : String con la palabra seleccionada y su pista (tipo gramatical).
- `palabra_mostrar` : Lista con letras o `_` que se muestra al usuario.
- `intentos_maximos`, `intentos_restantes`, `errores` : Control de fallos e intentos.
- `palabras_ganadas`, `palabras_perdidas` : Contadores de sesión.

## Interfaz

- Panel superior: selección de `Categoría` y `Dificultad`, y contadores (Ganadas/Perdidas).
- Panel izquierdo: `Canvas` con dibujo del ahorcado.
- Panel derecho: palabra oculta y teclado A-Z en una cuadrícula.
- Eventos: Se soporta tanto clic en botones como entrada desde teclado físico (evento `root.bind("<Key>")`).

## Requisitos

- Python 3.x (3.7+ recomendado)
- Solo librerías estándar; no usar `pip`.

## Ejecución

Abrir una terminal y ejecutar:

```bash
python "c:/Archivos/Escritorio/JUEGO PYTHON/ahorcado.py"
```

## Subir a GitHub (pasos sugeridos)

```bash
git init
git add .
git commit -m "feat: Juego del Ahorcado modular en Tkinter"
git remote add origin https://github.com/alexandraqua3/ahorcado_python.git
git push -u origin main
```

---

Si quieres, puedo:
- Añadir más categorías o palabras.
- Mejorar la paleta visual y accesibilidad (contraste, tamaños).
- Preparar una versión lista para presentar con puntos clave para la defensa oral.
