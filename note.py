import datetime
from csv import DictReader, DictWriter
from os.path import exists

"""
Заметка должна
содержать идентификатор, заголовок, тело заметки и дату/время создания или
последнего изменения заметки. Сохранение заметок необходимо сделать в
формате json или csv формат (разделение полей рекомендуется делать через
точку с запятой).
"""

# Класс с функционалом работы с заметками
class Notes:
    def __init__(self):
        self.id_count = 0
        self.notes = []
    # Метод создания/даваления новой заметки
    def add(self, head, body):
        # self.notes.append(note)
        self.notes.append({'Номер': self.id_count, 'Заголовок': head, 'Текст': body, 'Изменено': False,
                           'Дата создания': datetime.datetime.now(), 'Дата сохранения': datetime.datetime.now()})
        self.id_count += 1
    # Метод удаления заметки из общего списка по ноиеру/идентификатору
    def delete(self, id_rec):
        self.notes.pop(id_rec)
        self.id_count = 0
        for note in self.notes:
            note['Номер'] = self.id_count
            self.id_count += 1
    # Метод читающий заметки из файла заметок
    def read_from_file(self, file_name):
        print('Чтение содержимого файла заметок:')
        with open(file_name, 'r', encoding='utf-8') as data:
            f_reader = DictReader(data, delimiter=';')
            self.id_count = 0
            self.notes.clear()
            for elem in list(f_reader):
                self.notes.append({'Номер': self.id_count, 'Заголовок': elem['Заголовок'], 'Текст': elem['Текст'],
                                   'Изменено': elem['Изменено'], 'Дата создания': elem['Дата создания'],
                                   'Дата сохранения': elem['Дата сохранения']})
                self.id_count += 1
    # Метод сохраняющий список заметок в файл заметок
    def save_to_file(self, file_name):
        print('Сохранение файла зазаметок.')
        with open(file_name, 'w', encoding='utf-8', newline='') as data:
            f_writer = DictWriter(data, delimiter=';',
                                  fieldnames=['Номер', 'Заголовок', 'Текст', 'Изменено', 'Дата создания',
                                              'Дата сохранения'])
            f_writer.writeheader()
            f_writer.writerows(self.notes)
    # Метод редактирования/изменения существующей заметки по номеру/идентификатору заметки
    def edit(self, id_rec, head, body):
        for item in self.notes:
            if item['Номер'] == id_rec:
                item['Заголовок'] = head
                item['Текст'] = body
                item['Изменено'] = True
                item['Дата сохранения'] = datetime.datetime.now()


# Функция отображающий подсказку по списку используемых команд в приложении
def print_help():
    print(
        'Команды управления:\n'
        '\th - Список комманд (по умолчанию).\n'
        '\tr - Чтение файла с заметками.\n'
        '\ts - Сохранение заметок в файл.\n'
        '\ta - Новая заметка.\n'
        '\te - Редактирование заметки.\n'
        '\td - Удаление заметки.\n'
        '\tl - Отображение заметок списком.\n'
        '\tv - Отображение заметки по номеру.\n'
        '\tf - Поиск заметки по части текста из содержимого (по заголовку, по тексту, по дате и т.д.).\n'
        '\tq - Выход из программы (завершение работы)')

# Функция старта основной программы
def main():
    # Имя файла заметок
    file = "notes.txt"
    # Слздание объекта класса для работы с заметками
    my_notes = Notes()
    if exists(file):
        my_notes.read_from_file(file)
    print_help()
    # Циклический интерфейс ожидания ввода команды в консоли терминала
    while True:
        command = input("Введите команду: ")
        if command == 'q':
            print("Завершение работы программы.")
            break
        elif command == 's':
            my_notes.save_to_file(file)
            print('Заметки сохранены.')
        elif command == 'r':
            if not exists(file):
                print("Файл не существует. Создайте файл с заметками.")
                continue
            my_notes.read_from_file(file)
        elif command == 'f':
            if my_notes.id_count == 0:
                print("ПРЕДУПРЕЖДЕНИЕ: Список заметок пуст.")
                continue
            find = input("Введите часть текста искомой заметки: ")
            for note in my_notes.notes:
                for val in note.values():
                    if find in str(val):
                        print(note['Номер'], ';', note['Заголовок'], ';', note['Текст'], ';', note['Изменено'], ';',
                              note['Дата создания'], ';', note['Дата сохранения'])
                        break
        elif command == 'v':
            if my_notes.id_count == 0:
                print("ПРЕДУПРЕЖДЕНИЕ: Список заметок пуст.")
                continue
            id_rec = int(input("Введите номер редактируемой заметки: "))
            if my_notes.id_count < id_rec:
                print("ОШИБКА: Номер замети указан некорректный!")
                continue
            for elem in my_notes.notes:
                if elem['Номер'] == id_rec:
                    print(elem['Номер'], ';', elem['Заголовок'], ';', elem['Текст'], ';', elem['Изменено'], ';',
                          elem['Дата создания'], ';', elem['Дата сохранения'])
        elif command == 'l':
            if my_notes.id_count == 0:
                print("ПРЕДУПРЕЖДЕНИЕ: Список заметок пуст.")
                continue
            print("Список заметок:")
            for elem in my_notes.notes:
                print(elem['Номер'], ';', elem['Заголовок'], ';', elem['Текст'], ';', elem['Изменено'], ';',
                      elem['Дата создания'], ';', elem['Дата сохранения'])
        elif command == 'a':
            head = input("Введите заголовок заметки: ")
            body = input("Введите текст заметки: ")
            my_notes.add(head, body)
            my_notes.save_to_file(file)
        elif command == 'e':
            id_rec = int(input("Введите номер редактируемой заметки: "))
            if id_rec > my_notes.id_count or my_notes.id_count == 0:
                print('ОШИБКА: Изменение заметки невозможно! Не верно указан номер записи или записи отсутствуют.')
                continue
            head = input("Введите новый заголовок редактируемой заметки: ")
            body = input("Введите новый текст редактируемой заметки: ")
            my_notes.edit(id_rec, head, body)
            my_notes.save_to_file(file)
        elif command == 'd':
            id_rec = int(input("Введите номер редактируемой заметки: "))
            if id_rec > my_notes.id_count or my_notes.id_count == 0:
                print('ОШИБКА: Удаление заметки невозможно! Не верно указан номер записи или записи отсутствуют.')
                continue
            my_notes.delete(id_rec)
            my_notes.save_to_file(file)
        elif command == 'h':
            print_help()
        else:
            print_help()

# Запуск функции начала основной программы
main()
