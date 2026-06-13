import csv
from datetime import datetime
from modules.queue import Queue
from modules.bst import BinarySearchTree


def load_data(filename):
    """
    Загружает даты и температуры из CSV-файла.

    Параметры:
        filename - CSV-файл

    Возвращает:
        dates — список дат
        temperatures — список температур в виде чисел с плавающей точкой
    """
    dates = []
    temperatures = []

    with open(filename, 'r', encoding='utf-8') as file:
        first_line = file.readline()
        file.seek(0)
        delimiter = ';' if ';' in first_line else ','  # определяем разделитель

        reader = csv.reader(file, delimiter=delimiter)
        next(reader)  # пропускаем заголовок

        for row in reader:
            if len(row) < 2:
                continue
            if not row[0] or not row[1]:
                continue

            dates.append(row[0].strip())
            try:
                temp = float(row[1].replace(',', '.'))  # делаем температуру числом
                temperatures.append(round(temp, 2))  # округляем значение температуры до двух знаков после запятой
            except ValueError:
                continue

    return dates, temperatures


def compute_prefix_sums(temperatures):
    """
    Строит массив префиксных сумм для температур

    Параметры:
        temperatures - список температур по дням

    Возвращает:
        массив префиксных сумм
    """
    prefix_sums = [0] * (len(temperatures) + 1)
    for i in range(len(temperatures)):
        prefix_sums[i + 1] = prefix_sums[i] + temperatures[i]
    return prefix_sums


def get_sum_between_days(prefix_sums, start_idx, end_idx):
    """
    Считает сумму температур на отрезке с помощью префиксной суммы

    Параметры:
        prefix_sums - массив префиксных сумм
        start_idx - индекс первого дня в отрезке, в нашем случае всегда первый день месяца
        end_idx - индекс последнего дня в отрезке, в нашем случае всегда последний день месяца

    Возвращает:
        сумму температур с первого по последний дни
    """
    return prefix_sums[end_idx + 1] - prefix_sums[start_idx]


def parse_date(date_str):
    """
    Преобразует строку с датой в объект date

    Параметры:
        date_str - строка с датой
            Поддерживаемые форматы: ДД.ММ.ГГГГ, ГГГГ-ММ-ДД, ДД/ММ/ГГГГ

    Возвращает:
        объект даты, если распознать формат удалось, если нет - None
    """
    date_str = (date_str or "").strip()
    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            pass
    return None


def find_date_index(dates, date_str):
    """
    Ищет индекс даты в списке дат

    Возвращает:
        индекс найденной даты в списке dates, если дата не найдена или не распознана - -1
    """
    target = parse_date(date_str)
    if target is None:
        return -1
    for i, d in enumerate(dates):
        if parse_date(d) == target:
            return i
    return -1


def average_temperature_by_month(dates, temperatures, prefix_sums):
    """Средняя температура по каждому месяцу (месяц берётся из даты в CSV)."""
    month_names = [
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ]

    month_avg = []
    current_key = None  #(год, месяц)
    start_idx = None
    count_in_month = 0

    for i, d in enumerate(dates):
        dt = parse_date(d)
        if dt is None:
            continue

        key = (dt.year, dt.month)
        if current_key is None:
            current_key = key
            start_idx = i
            count_in_month = 1
            continue

        if key == current_key:
            count_in_month += 1
            continue

        # закрываем предыдущий месяц
        end_idx = i - 1
        month_sum = get_sum_between_days(prefix_sums, start_idx, end_idx)
        y, m = current_key
        month_avg.append((f"{month_names[m - 1]} {y}", month_sum / count_in_month))

        current_key = key
        start_idx = i
        count_in_month = 1

    # последний месяц в файле
    if current_key is not None and start_idx is not None and count_in_month > 0:
        end_idx = len(temperatures) - 1
        month_sum = get_sum_between_days(prefix_sums, start_idx, end_idx)
        y, m = current_key
        month_avg.append((f"{month_names[m - 1]} {y}", month_sum / count_in_month))

    return month_avg


def find_min_max_temp(temperatures, dates):
    """
    функция find_min_max_temp находит самый холодный и самый тёплый день (линейный поиск)

    параметры:
    temperatures: список температур
    dates: список дат
        
    возвращает:
    кортеж из двух кортежей: ((min_day, min_temp), (max_day, max_temp))
    """
    if len(temperatures) == 0:
        return None, None

    min_temp = max_temp = temperatures[0]
    min_day = max_day = dates[0]

    for i in range(1, len(temperatures)):
        if temperatures[i] < min_temp:
            min_temp = temperatures[i]
            min_day = dates[i]
        if temperatures[i] > max_temp:
            max_temp = temperatures[i]
            max_day = dates[i]

    return (min_day, min_temp), (max_day, max_temp)


def sort_months_by_temp(month_avg):
    """
    функция sort_months_by_temp сортирует месяцы по средней температуре (сортировка вставками)

    параметры:
    month_avg: список кортежей (месяц, средняя температура)
    
    возвращает:
    отсортированный список кортежей
    """
    arr = month_avg[:]
    for i in range(1, len(arr)):
        key_item = arr[i]
        j = i - 1
        while j >= 0 and arr[j][1] > key_item[1]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item
    return arr


def sort_pairs_by_temp(pairs):
    """
    функция sort_pairs_by_temp сортирует пары (температура, дата) по температуре (сортировка вставками)

    параметры:
    pairs: список пар (температура, дата)
    
    возвращает:
    отсортированный список пар
    """
    arr = pairs[:]
    for i in range(1, len(arr)):
        key_item = arr[i]
        j = i - 1
        while j >= 0 and arr[j][0] > key_item[0]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item
    return arr


def build_temperature_tree(dates, temperatures):
    """
    функция build_temperature_tree строит бинарное дерево поиска по температурам

    параметры:
    dates: список дат
    temperatures: список температур
    
    возвращает:
    построенное дерево BST
    """
    tree = BinarySearchTree()
    for i in range(len(temperatures)):
        tree.insert(temperatures[i], dates[i])
    return tree


def smooth_with_queue(temperatures, window_size=7):
    """
    функция smooth_with_queue реализует скользящее среднее с окном window_size (у нас =7)
    очередь хранит последние 7 значений, пока в очереди меньше 7 значений, оставляем исходную температуру

    параметры:
    temperatures: список температур
    window_size: размер окна (у нас 7)
    
    возвращает:
    список сглаженных температур
    """
    smoothed = []
    q = Queue()

    for temp in temperatures:
        q.enqueue(temp)
        if q.size() > window_size:
            q.dequeue() #удаляем самый старый элемент, если окно переполнено

        if q.size() == window_size:
            values = q.get_all_values()
            smoothed.append(sum(values) / len(values)) #считаем среднее
        else:
            smoothed.append(temp) #для первых дней без полного окна

    return smoothed


def smooth_week_from_date(dates, temperatures, start_date_str, window_size=7):
    """
    функция smooth_week_from_date сглаживает 7 дней подряд, начиная с введённой даты (ДД.ММ.ГГГГ)
    
    параметры:
    dates: список дат
    temperatures: список температур
    start_date_str: начальная дата в формате ДД.ММ.ГГГГ
    window_size: размер окна (у нас 7)
    
    возвращает:
    кортеж (start_idx, список из 7 сглаженных) или (None, текст ошибки)
    """
    start_idx = find_date_index(dates, start_date_str)
    if start_idx < 0:
        return None, "Дата не найдена. Введите в формате ДД.ММ.ГГГГ (например, 25.02.2025)"

    if start_idx + window_size > len(temperatures):
        return None, f"От даты {start_date_str} не хватает {window_size} дней подряд в файле"

    segment = temperatures[start_idx:start_idx + window_size] #вырезаем 7 дней
    smoothed_segment = smooth_with_queue(segment, window_size) #сглаживаем
    return (start_idx, smoothed_segment), None
