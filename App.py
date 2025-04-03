import flet as ft
from Utils.Gen_Questions import generate_Questions,get_chat_history
from  Utils.Gen_Dictionary import gen_Dictionary
from Utils.Json_Utility import upload_file,save_file


def main(page):

    #####Variables usadas
    questions = []


    #######Funciones de la pagina
    #Funcion para generar las preguntas
    def add_clicked(e):
        nonlocal questions

        print("Generando preguntas, por favor no hacer nada")
        #Genera el texto que despues sera procesado
        text = generate_Questions(text_input.value)
        if text:
        #Actualiza el input del usuario
            text_input.value = ""
            text_input.hint_text = "Tambien puedes pedir que se mejore una pregunta."
            text_input.focus()
            text_input.update()

        #Procesa y genera todas las preguntas
            questions = gen_Dictionary(text)        
            show_Questions()
        else:
            print("Intente de nuevo")
        page.update()

    #Funcion para controlar los archivos
    def file_manager(e: ft.FilePickerResultEvent):
        nonlocal questions

        #Entrara si se selecciono una carpeta(solo ocurre cuando se guarda un archivo)
        if e.path:
            file_path = e.path
            save_file(file_path)

        #Entrara si se seleccion algun archivo
        elif e.files:
            file_path = e.files[0].path
            upload_file(file_path)
            questions = gen_Dictionary(get_chat_history()[-1]['content'])
            show_Questions()
        
        #En caso de no entrar en ningun caso.
        else:
            print("Accion no valida")
    
    #Funcion encargada de ocultar y mostrar la barra de generacion
    def on_keyboard(e: ft.KeyboardEvent): 
        if e.ctrl and e.key.lower() == "r":
            hidden = gen_bar.opacity == 1 #Detectar si esta oculto

            #Alternar opacidad y deshabilitar interaccion
            for elem in [gen_bar,info_text,button_bar]:
                elem.opacity = 0 if hidden else 1
                elem.disabled = hidden

            page.update()

    #Funcion para intentar de nuevo
    def try_again(e):
        show_Questions()

    #Funcion para mostrar las preguntas
    def show_Questions():
        nonlocal questions
        answer_cotainer.controls.clear()
        send_button.visible = True
        #Limpia el elemento contenedor de las preguntas
        question_column.controls.clear()
        
        #Recorre la lista de preguntas, creando para cada una un texto(la pregunta) y un dropdown(las posibles respuestas)
        for elem in questions:
            question_container = ft.Column(
            controls=[
                ft.Text(value=elem["key"]),  # Pregunta
                ft.Dropdown(                  # Opciones
                    key=elem["key"],
                    options=[ft.dropdown.Option(op) for op in elem["options"]],
                )
            ],
            spacing=10
        )
            #Se añade la pregunta al elemento de la columna y se actualiza la pagina
            question_column.controls.append(question_container)
        
        question_column.controls.append(send_button)
        page.update()

    #Funcion para verificar respuestas
    def check_answers(e):

        right_questions = 0
        nonlocal questions
        dropdown_list = []
        try:
            answer_cotainer.controls.clear()
            send_button.visible = False
            for elem in question_column.controls:
                if isinstance(elem,ft.Column):
                    for sub_control in elem.controls:
                        if isinstance(sub_control,ft.Dropdown):
                            dropdown_list.append(sub_control)

            for i, elem in enumerate(dropdown_list):
                if elem.value[0] == questions[i]["answer"]:
                    elem.color = ft.Colors.GREEN
                    right_questions += 1
                else:
                    elem.color = ft.Colors.RED
            
            answer_cotainer.controls.append(ft.Text(value=f"{right_questions}/{len(dropdown_list)}",color=ft.Colors.GREEN,size=20))
            answer_cotainer.controls.append(ft.ElevatedButton(
                "Volver a intentar",
                icon=ft.Icons.PLAY_ARROW,
                on_click=try_again
            ))
        except Exception as e:
            answer_cotainer.controls.append(ft.Text(value="No has conestado todas las preguntas",color=ft.Colors.RED,size=20))
            send_button.visible = True
        page.update()

    ###########Elementos de la pagina
    #Input principal
    text_input = ft.TextField(
            hint_text="Genera 5 preguntas del siguiente parrafo: .....",
            multiline=True,
            min_lines=1,
            max_lines=1000,
            expand=True)
    
    #Elemento contenedor de toda la app
    main_column = ft.Column(
        scroll=True,  # Scroll habilitado
        expand=True,  # Ocupa todo el espacio disponible
        spacing=20 ,
        alignment= ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    
    #Elemento contenedor de las preguntas
    question_column = ft.Column()

    #Elementos relacionados a la barra de generacion.
    gen_bar = ft.Row([text_input, ft.ElevatedButton("Generar", on_click=add_clicked)])
    info_text = ft.Text(value="Presiona Ctrl + R para ocultar o mostrar.")

    #Elemento contenedor de las respuestas
    answer_cotainer = ft.Column(alignment= ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    #Elemento  encargada de seleccionar archivos
    pick_files_dialog = ft.FilePicker(on_result=file_manager)

    #Se añade el elemento al overlay de la pagina
    page.overlay.append(pick_files_dialog)

    #Boton encargado de subir el json.
    upload_button = ft.Row( [
                ft.ElevatedButton(
                    "Subir",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False,
                        file_type=ft.FilePickerFileType.CUSTOM,
                        allowed_extensions=["json"]
                    ),
                )
            ])
    
    #Boton para descargar un archivo json con las preguntas generadas
    download_button = ft.Row( [
                ft.ElevatedButton(
                    "Guardar",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=lambda _: pick_files_dialog.save_file(
                        file_name="chat_history.json",
                        file_type=ft.FilePickerFileType.CUSTOM,
                        allowed_extensions=["json"]
                    ),
                )
            ])
    
    #Elemento contendero de los botones
    button_bar = ft.Row([
        upload_button,
        download_button
    ],
    alignment=ft.MainAxisAlignment.CENTER
    )

    #Boton para enviar informacion
    send_button = ft.ElevatedButton(
        "Enviar",
        icon=ft.Icons.SEND,
        on_click=check_answers
    )

    #Titulo
    title_text = ft.Text(value="Trivia",size=50,color=ft.Colors.GREEN)

    #Se añade al elemento contenedor principal todos los elementos
    main_column.controls.append(title_text)
    main_column.controls.append(gen_bar)
    main_column.controls.append(info_text)
    main_column.controls.append(button_bar)
    main_column.controls.append(question_column)
    main_column.controls.append(answer_cotainer)

    #Se añade a la pag el elemento contenedor principal
    page.add(main_column)

    #Se añade el evento del keyboard a la pag.
    page.on_keyboard_event = on_keyboard


ft.app(main)