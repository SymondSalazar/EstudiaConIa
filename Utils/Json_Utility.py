from Utils.Gen_Questions import get_chat_history,set_chat_history
import json
import os 

#Obtener el historial del chat
chat_history = get_chat_history()

#Funcion para subir el archivo
def upload_file(path):
    global chat_history

    #Se actualiza el chat_history y se lo coloca en el script Gen_Questions
    with open (path,'r') as f:
        data = json.load(f)
        chat_history+= data
        set_chat_history(chat_history)
        print("Archivo subido con exito")

#Funcion para guardar el archivo
def save_file(path):
    global chat_history

    #Se abre el archivo con el nombre en modo de escritura
    with open(path,'w') as f:
        json.dump(chat_history[1:],f)
        print("Archivo guardado con exito")

        #Se abre el directorio donde se guardo el archivo. 
        os.startfile(os.path.dirname(path))
