#Genera una lista con diccionarios de las preguntas con sus literales y respuestas
def gen_Dictionary(text):
    #Se sepera todas las preguntas y literales
    items = [elem.split("\n") for elem in text.split("\n--------")]
    questions = []
    
    #Se recorre la lista con todas las preguntas
    for elem in items: 
        key = ""
        options = []
        answer = ""
        
        #Se recorre las sublistas con los elementos de cada pregunta
        for e in elem:
            #Gurda la respuesta correcta
            if "Respuesta correcta:" in e:
                answer =  e[-1]
            #En caso de ser vacio sigue a la siguiente iteracion
            elif e == "":
                continue
            #Se guarda la pregunta            
            elif e[0].isdigit():
                key = e
            #Se guarda las opciones
            else:
                options.append(e)          
        #Si tiene pregunta se guarda en la lista question todas las preguntas con sus respectivas partes
        if key:
            questions.append({
            "key": key,
            "options": options,
            "answer": answer
        })   
    return questions

