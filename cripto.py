def cripto_valores(valor):
    new_string = ""
    chars_ant = []
    for v in valor:
        if v.isnumeric():
            v = int(v)
            new_string += str(chr(v))
            chars_ant.append(str(chr(v)))
            continue

        v = str(v)
        new_string += str(ord(v))
        chars_ant.append(str(ord(v)))

    return chars_ant


def decripto_valores(array_chars):
    palavra_original = ""
    for v in array_chars:
        if v.isnumeric():
            v = int(v)
            palavra_original += str(chr(v))
            continue

        v = str(v)
        palavra_original += str(ord(v))

    return palavra_original

# obtermos o código ascii ou unicode de um caractere na função ord()
# para obtermos o caractere correspondente a um código unicode devemos utilizar a função chr()


