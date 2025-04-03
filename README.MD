# Trivia Generator - Generador de Preguntas con IA

## Descripción
Trivia AI es una aplicación desarrollada en **Python** que permite generar preguntas a partir de un texto utilizando inteligencia artificial. Además, los usuarios pueden corregir y modificar las preguntas en lenguaje natural. Es una herramienta ideal para juegos de trivia o para estudiar de manera interactiva.

## Tecnologías Utilizadas
- [Python](https://www.python.org/)
- [Flet](https://flet.dev/) - Framework para interfaces de usuario
- [OpenAI](https://openai.com/) - Libreria usada para el manejo del LLM
- [python-dotenv](https://pypi.org/project/python-dotenv/) - Manejo de variables de entorno

## Estructura del Proyecto
El proyecto está organizado de la siguiente manera:

```
Trivia_Generator/
│-- App.py          # Archivo principal de la aplicación (usa Flet)
│-- .env            # Archivo de variables de entorno (contiene API_KEY)
│-- requirements.txt # Dependencias necesarias
│
└── utils/          # Carpeta con archivos de utilidades
    ├── Gen_Questions.py   # Genera preguntas usando IA (modelo Google Gemini 2.5 Pro Exp)
    ├── Gen_Dictionary.py  # Convierte la salida de la IA en una lista de preguntas
    ├── Json_Utility.py    # Maneja subida y descarga de archivos JSON (historial de preguntas)
```

## Instalación
1. Clona el repositorio:
   ```sh
   git clone https://github.com/SymondSalazar/Trivia_Generator.git
   cd Trivia_Generator
   ```
2. Crea un entorno virtual (opcional pero recomendado):
   ```sh
   python -m venv venv
   source venv/bin/activate  # En Linux/macOS
   venv\Scripts\activate  # En Windows
   ```
3. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```
4. Crea el archivo `.env` y agrega tu API key de **OpenRouter**:
   ```sh
   echo "API_KEY=tu_clave_aqui" > .env
   ```

## Uso
Para ejecutar la aplicación:
```sh
python App.py
```
La interfaz se abrirá y podrás comenzar a generar preguntas a partir de textos.

## Funcionalidades Principales
✅ **Generación de preguntas con IA** a partir de cualquier texto.
✅ **Corrección y edición de preguntas** con lenguaje natural.
✅ **Guardado y carga de preguntas en JSON** para reutilizarlas.
✅ **Interfaz de usuario interactiva** gracias a Flet.

---

📌 **Autor:** SymondSalazar
📌 **Repositorio:** [GitHub](https://github.com/SymondSalazar/Trivia_Generator)

