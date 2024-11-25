def tipo_input_string(tipo_input):

    tipo_input = int(tipo_input)

    if tipo_input == 6:
        tipo_input = "Elearnings"
        return tipo_input
    elif tipo_input == 7:
        tipo_input = "Materiais"
        return tipo_input
    elif tipo_input == 8 :
        tipo_input = "LinkUteis"
        return tipo_input
    elif tipo_input == 9:
        tipo_input = "Vídeos"
        return tipo_input
    elif tipo_input == 10:
        tipo_input = "Audios"
        return tipo_input
    else:
        print("Tipo invalido")

