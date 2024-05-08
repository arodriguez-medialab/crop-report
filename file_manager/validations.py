import os
from datetime import datetime
from dateutil.parser import parse


def validDate(strDate):
    try:
        datetime.strptime(strDate, '%d/%m/%Y')
        parse(strDate)
        return strDate
    except ValueError:
        raise ValueError("Formato de dato incorrecto, este debe ser dd/mm/yyyy")


def validInt(strInt):
    try:
        int(strInt)
        return strInt
    except ValueError:
        raise ValueError("Formato de dato incorrecto, este debe ser un número")


def validStrTest(strTest):
    try:
        if strTest != '':
            if strTest.lower().strip() != 't':
                raise ValueError("Este campo solo acepta la palabra T o vacio")
        return strTest
    except ValueError:
        raise ValueError("Error campo ensayo")


def countFiles(dir):
    return len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))])


def cleanAcronimo(text):
    list = text.split()
    length = len(list)
    acrom_final = ''
    for i in range(length):
        text = list[i][0]
        if text == '0':
            text_tmp = list[i].replace('0', '')
            acrom_final += text_tmp
        else:
            acrom_final += list[i]
    return acrom_final.lower()