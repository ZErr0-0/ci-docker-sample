import sys

def validate_utf8(file_name):
    error_found = False  # Флаг, сигнализирующий о наличии ошибки в файле
    error_position = 0  # Позиция в файле, где была обнаружена ошибка

    with open(file_name, 'rb') as opened_file:  # Открываем файл в двоичном режиме для чтения
        while True:
            current_byte = opened_file.read(1)  # Читаем один байт из файла
            if not current_byte:  # Если конец файла, выходим из цикла
                break
            error_position += 1  # Увеличиваем счетчик позиции в файле
            byte_value = ord(current_byte)  # Преобразуем байт в целое число
            if byte_value < 0x80:  # Если это ASCII-символ, пропускаем его
                continue
            elif 0xC0 <= byte_value < 0xE0:  # Если это первый байт двухбайтовой последовательности UTF-8
                next_byte = opened_file.read(1)  # Читаем следующий байт
                if not next_byte:  # Если конец файла, сигнализируем об ошибке
                    error_found = True
                    break
                error_position += 1  # Увеличиваем счетчик позиции в файле
                next_byte_value = ord(next_byte)  # Преобразуем байт в целое число
                if not (0x80 <= next_byte_value < 0xC0):  # Если второй байт не соответствует формату UTF-8, сигнализируем об ошибке
                    error_found = True
                    break
            elif 0xE0 <= byte_value < 0xF0:  # Если это первый байт трехбайтовой последовательности UTF-8
                next_byte = opened_file.read(1)  # Читаем следующий байт
                if not next_byte:  # Если конец файла, сигнализируем об ошибке
                    error_found = True
                    break
                error_position += 1  # Увеличиваем счетчик позиции в файле
                next_byte_value = ord(next_byte)  # Преобразуем байт в целое число
                if not (0x80 <= next_byte_value < 0xC0):  # Если второй байт не соответствует формату UTF-8, сигнализируем об ошибке
                    error_found = True
                    break
                next_byte = opened_file.read(1)  # Читаем следующий байт
                if not next_byte:  # Если конец файла, сигнализируем об ошибке
                    error_found = True
                    break
                error_position += 1  # Увеличиваем счетчик позиции в файле
                next_byte_value = ord(next_byte)  # Преобразуем байт в целое число
                if not (0x80 <= next_byte_value < 0xC0):  # Если третий байт не соответствует формату UTF-8, сигнализируем об ошибке
                    error_found = True
                    break
            elif 0xF0 <= byte_value < 0xF8:  # Если это первый байт четырехбайтовой последовательности UTF-8
                next_byte = opened_file.read(1)  # Читаем следующий байт
                if not next_byte:  # Если конец файла, сигнализируем об ошибке
                    error_found = True
                    break
                error_position += 1  # Увеличиваем счетчик позиции в файле
                next_byte_value = ord(next_byte)  # Преобразуем байт в целое число
                if not (0x80 <= next_byte_value < 0xC0):  # Если второй байт не соответствует формату UTF-8, сигнализируем об ошибке
                    error_found = True
                    break
                next_byte = opened_file.read(1)  # Читаем следующий байт
                if not next_byte:  # Если конец файла, сигнализируем об ошибке
                    error_found = True
                    break
                error_position += 1  # Увеличиваем счетчик позиции в файле
                next_byte_value = ord(next_byte)  # Преобразуем байт в целое число
                if not (0x80 <= next_byte_value < 0xC0):  # Если третий байт не соответствует формату UTF-8, сигнализируем об ошибке
                    error_found = True
                    break
                next_byte = opened_file.read(1)  # Читаем следующий байт
                if not next_byte:  # Если конец файла, сигнализируем об ошибке
                    error_found = True
                    break
                error_position += 1  # Увеличиваем счетчик позиции в файле
                next_byte_value = ord(next_byte)  # Преобразуем байт в целое число
                if not (0x80 <= next_byte_value < 0xC0):  # Если четвертый байт не соответствует формату UTF-8, сигнализируем об ошибке
                    error_found = True
                    break
            else:  # Если первый байт не соответствует формату UTF-8, сигнализируем об ошибке
                error_found = True
                break

    if error_found:  # Если была обнаружена ошибка, выводим сообщение об ошибке и завершаем работу программы
        print(f"Ошибка в позиции {error_position}: неверная последовательность UTF-8", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:  # Если не был передан аргумент командной строки, выводим инструкцию по использованию программы и завершаем работу
        print("Введите в командной строке директории, в которой расположены файл программы и анализируемый файл: \npython 4lab.py <filename>")
        sys.exit(1)
    input_file_name = sys.argv[1]  # Получаем имя входного файла из аргумента командной строки
    validate_utf8(input_file_name)  # Вызываем функцию валидации UTF-8
    print("Файл является допустимым представлением UTF-8")  # Выводим сообщение об успешном завершении работы программы
