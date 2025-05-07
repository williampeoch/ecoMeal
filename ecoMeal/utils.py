def convert_column_name_to_index(column_name):

    column_name = column_name.upper()
    column_index = 0
    column_name_len = len(column_name)

    for index, col_char in enumerate(column_name):
        pow_index = column_name_len - 1 - index
        char_value = ord(col_char)-64 # la valeur ASCII de A = 65, or on veut A = 1 (format excel)
        real_char_value = char_value*pow(26, pow_index)
        column_index += real_char_value

    return column_index - 1 # excel est indexé à 1, column_index est indexé à 0

def get_input(displayed_text, format):
    user_input = input(displayed_text)

    if re.search("^" + format + "$", user_input) != None:
        # le format est bon
        return user_input
    else:
        # le format n'est pas bon
        print("La valeur saisie est invalide.")
        return get_input(displayed_text, format)
