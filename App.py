import flet as ft
from Utils.Gen_Questions import generate_Questions, get_chat_history
from Utils.Gen_Dictionary import gen_Dictionary
from Utils.Json_Utility import upload_file, save_file


def main(page):
    # Paleta y tipografía base
    PRIMARY_TEXT = ft.Colors.BLACK
    SECONDARY_TEXT = ft.Colors.BLACK
    BACKGROUND = ft.Colors.WHITE
    ICON_COLOR = ft.Colors.BLACK
    CORRECT_COLOR = ft.Colors.GREEN_800  # Verde suave para respuestas correctas
    INCORRECT_COLOR = ft.Colors.RED_400  # Rojo suave para respuestas incorrectas

    # Configuración de página / tema
    page.title = "Estudia Con IA"
    page.bgcolor = BACKGROUND
    page.theme_mode = ft.ThemeMode.LIGHT
    # Intentar usar Montserrat instalada en el sistema
    page.theme = ft.Theme(font_family="Montserrat")

    #####Variables usadas
    questions = []

    #######Funciones de la pagina
    # Funcion para generar las preguntas
    def add_clicked(e):
        nonlocal questions

        print("Generando preguntas, por favor no hacer nada")
        # Genera el texto que despues sera procesado
        text = generate_Questions(text_input.value)
        if text:
            # Actualiza el input del usuario
            text_input.value = ""
            text_input.hint_text = "Tambien puedes pedir que se mejore una pregunta."
            text_input.focus()
            text_input.update()

            # Procesa y genera todas las preguntas
            questions = gen_Dictionary(text)
            show_Questions()
        else:
            print("Intente de nuevo")
        page.update()

    # Funcion para controlar los archivos
    def file_manager(e: ft.FilePickerResultEvent):
        nonlocal questions

        # Entrara si se selecciono una carpeta(solo ocurre cuando se guarda un archivo)
        if e.path:
            file_path = e.path
            save_file(file_path)

        # Entrara si se seleccion algun archivo
        elif e.files:
            file_path = e.files[0].path
            upload_file(file_path)
            questions = gen_Dictionary(get_chat_history()[-1]["content"])
            show_Questions()

        # En caso de no entrar en ningun caso.
        else:
            print("Accion no valida")

    # Funcion encargada de ocultar y mostrar la barra de generacion
    def on_keyboard(e: ft.KeyboardEvent):
        if e.ctrl and e.key.lower() == "r":
            hidden = gen_bar.opacity == 1  # Detectar si esta oculto

            # Alternar opacidad y deshabilitar interaccion
            for elem in [gen_bar, info_text, button_bar]:
                elem.opacity = 0 if hidden else 1
                elem.disabled = hidden

            page.update()

    # Funcion para intentar de nuevo
    def try_again(e):
        show_Questions()

    # Funcion para mostrar las preguntas
    def show_Questions():
        nonlocal questions
        answer_cotainer.controls.clear()
        send_button.visible = True
        # Limpia el elemento contenedor de las preguntas
        question_column.controls.clear()

        # Recorre la lista de preguntas, creando para cada una un texto(la pregunta) y un dropdown(las posibles respuestas)
        for elem in questions:
            question_container = ft.Column(
                controls=[
                    ft.Text(
                        value=elem["key"],
                        color=PRIMARY_TEXT,
                        style=ft.TextStyle(
                            font_family="Montserrat",
                            weight=ft.FontWeight.W_600,
                            size=18,
                        ),
                    ),  # Pregunta
                    ft.Container(
                        content=ft.Dropdown(  # Opciones
                            key=elem["key"],
                            options=[ft.dropdown.Option(op) for op in elem["options"]],
                            color=PRIMARY_TEXT,
                        ),
                        padding=ft.padding.symmetric(vertical=4),
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            )
            # Se añade la pregunta al elemento de la columna y se actualiza la pagina
            question_column.controls.append(question_container)

        # botón enviar centrado
        question_column.controls.append(
            ft.Row([send_button], alignment=ft.MainAxisAlignment.CENTER)
        )
        page.update()

    # Funcion para verificar respuestas
    def check_answers(e):
        nonlocal questions
        right_questions = 0
        dropdown_list = []
        try:
            answer_cotainer.controls.clear()
            send_button.visible = False

            # Buscar los dropdowns
            for elem in question_column.controls:
                if isinstance(elem, ft.Column):
                    for sub_control in elem.controls:
                        if isinstance(sub_control, ft.Container):
                            if isinstance(sub_control.content, ft.Dropdown):
                                dropdown_list.append(sub_control.content)

            for i, dd in enumerate(dropdown_list):
                if dd.value:
                    # Extraer la letra de la opción seleccionada (A, B, C, D)
                    selected_letter = dd.value[0] if dd.value else ""
                    correct_letter = questions[i]["answer"]

                    if selected_letter == correct_letter:
                        # Respuesta correcta - cambiar color del dropdown
                        dd.bgcolor = ft.Colors.GREEN_100
                        dd.color = ft.Colors.GREEN_800
                        right_questions += 1
                    else:
                        # Respuesta incorrecta - cambiar color del dropdown
                        dd.bgcolor = ft.Colors.RED_100
                        dd.color = ft.Colors.RED_800
                else:
                    # Sin respuesta - también incorrecto
                    dd.bgcolor = ft.Colors.RED_100
                    dd.color = ft.Colors.RED_800

            page.update()

            answer_cotainer.controls.append(
                ft.Text(
                    value=f"{right_questions}/{len(dropdown_list)}",
                    color=PRIMARY_TEXT,
                    size=22,
                    style=ft.TextStyle(
                        font_family="Montserrat",
                        weight=ft.FontWeight.W_700,
                    ),
                )
            )
            answer_cotainer.controls.append(
                ft.ElevatedButton(
                    "Volver a intentar",
                    icon=ft.Icons.PLAY_ARROW,
                    icon_color=ICON_COLOR,
                    on_click=try_again,
                    style=ft.ButtonStyle(
                        color=PRIMARY_TEXT,
                        bgcolor=BACKGROUND,
                        padding=ft.padding.symmetric(vertical=14, horizontal=22),
                        side=ft.BorderSide(1, PRIMARY_TEXT),
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                )
            )
        except Exception:
            answer_cotainer.controls.append(
                ft.Text(
                    value="No has conestado todas las preguntas",
                    color=PRIMARY_TEXT,
                    size=20,
                    style=ft.TextStyle(
                        font_family="Montserrat",
                        weight=ft.FontWeight.W_600,
                    ),
                )
            )
            send_button.visible = True
        page.update()

    ###########Elementos de la pagina
    # Input principal
    text_input = ft.TextField(
        hint_text="Genera 5 preguntas del siguiente párrafo: .....",
        multiline=True,
        min_lines=4,
        max_lines=1000,
        expand=True,
        border=ft.InputBorder.OUTLINE,
        border_radius=8,
        border_color=PRIMARY_TEXT,
        bgcolor=BACKGROUND,
        cursor_color=PRIMARY_TEXT,
        text_style=ft.TextStyle(
            font_family="Montserrat",
            size=16,
            weight=ft.FontWeight.W_500,
            color=PRIMARY_TEXT,
        ),
        hint_style=ft.TextStyle(color=PRIMARY_TEXT),
        content_padding=ft.padding.all(16),
    )

    # Elemento contenedor de toda la app
    main_column = ft.Column(
        scroll=True,  # Scroll habilitado
        expand=True,  # Ocupa todo el espacio disponible
        spacing=30,
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Elemento contenedor de las preguntas
    question_column = ft.Column(
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
    )

    # Elementos relacionados a la barra de generacion.
    # Barra de generación: input arriba, botón centrado debajo
    generate_button = ft.ElevatedButton(
        "Generar",
        icon=ft.Icons.PLAY_ARROW,
        icon_color=ICON_COLOR,
        on_click=add_clicked,
        style=ft.ButtonStyle(
            color=PRIMARY_TEXT,
            bgcolor=BACKGROUND,
            padding=ft.padding.symmetric(vertical=14, horizontal=22),
            side=ft.BorderSide(1, PRIMARY_TEXT),
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )

    gen_bar = ft.Column(
        controls=[
            text_input,
            ft.Row([generate_button], alignment=ft.MainAxisAlignment.CENTER),
        ],
        spacing=10,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    info_text = ft.Text(
        value="Presiona Ctrl + R para ocultar o mostrar.",
        color=SECONDARY_TEXT,
        style=ft.TextStyle(font_family="Montserrat", weight=ft.FontWeight.W_500),
    )

    # Elemento contenedor de las respuestas
    answer_cotainer = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Elemento  encargada de seleccionar archivos
    pick_files_dialog = ft.FilePicker(on_result=file_manager)

    # Se añade el elemento al overlay de la pagina
    page.overlay.append(pick_files_dialog)

    # Boton encargado de subir el json.
    upload_button = ft.Row(
        [
            ft.ElevatedButton(
                "Subir",
                icon=ft.Icons.UPLOAD_FILE,
                icon_color=ICON_COLOR,
                on_click=lambda _: pick_files_dialog.pick_files(
                    allow_multiple=False,
                    file_type=ft.FilePickerFileType.CUSTOM,
                    allowed_extensions=["json"],
                ),
                style=ft.ButtonStyle(
                    color=PRIMARY_TEXT,
                    bgcolor=BACKGROUND,
                    padding=ft.padding.symmetric(vertical=14, horizontal=22),
                    side=ft.BorderSide(1, PRIMARY_TEXT),
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            )
        ]
    )

    # Boton para descargar un archivo json con las preguntas generadas
    download_button = ft.Row(
        [
            ft.ElevatedButton(
                "Guardar",
                icon=ft.Icons.DOWNLOAD,
                icon_color=ICON_COLOR,
                on_click=lambda _: pick_files_dialog.save_file(
                    file_name="chat_history.json",
                    file_type=ft.FilePickerFileType.CUSTOM,
                    allowed_extensions=["json"],
                ),
                style=ft.ButtonStyle(
                    color=PRIMARY_TEXT,
                    bgcolor=BACKGROUND,
                    padding=ft.padding.symmetric(vertical=14, horizontal=22),
                    side=ft.BorderSide(1, PRIMARY_TEXT),
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            )
        ]
    )

    # Elemento contendero de los botones
    button_bar = ft.Row(
        [upload_button, download_button], alignment=ft.MainAxisAlignment.CENTER
    )

    # Boton para enviar informacion
    send_button = ft.ElevatedButton(
        "Enviar",
        icon=ft.Icons.SEND,
        icon_color=ICON_COLOR,
        on_click=check_answers,
        style=ft.ButtonStyle(
            color=PRIMARY_TEXT,
            bgcolor=BACKGROUND,
            padding=ft.padding.symmetric(vertical=14, horizontal=22),
            side=ft.BorderSide(1, PRIMARY_TEXT),
            shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )

    # Titulo
    title_text = ft.Text(
        value="Estudia Con Ia",
        size=64,
        color=PRIMARY_TEXT,
        style=ft.TextStyle(
            font_family="Montserrat",
            weight=ft.FontWeight.W_900,  # Montserrat Black
        ),
        text_align=ft.TextAlign.CENTER,
    )

    # Se añade al elemento contenedor principal todos los elementos
    main_column.controls.append(ft.Container(height=30))  # Espacio superior
    main_column.controls.append(title_text)
    main_column.controls.append(
        ft.Container(content=gen_bar, padding=ft.padding.symmetric(horizontal=40))
    )
    main_column.controls.append(
        ft.Container(content=info_text, padding=ft.padding.symmetric(horizontal=40))
    )
    main_column.controls.append(button_bar)
    main_column.controls.append(
        ft.Container(
            content=question_column, padding=ft.padding.symmetric(horizontal=40)
        )
    )
    main_column.controls.append(answer_cotainer)

    # Se añade a la pag el elemento contenedor principal
    page.add(main_column)

    # Se añade el evento del keyboard a la pag.
    page.on_keyboard_event = on_keyboard


ft.app(main)
