from modules.analysis import (
    load_data,
    compute_prefix_sums,
    average_temperature_by_month,
    find_min_max_temp,
    sort_months_by_temp,
    build_temperature_tree,
    sort_pairs_by_temp,
    smooth_week_from_date,
)
from modules.stack import Stack

WINDOW_SIZE = 7  # задаем размер скользящего окна

def print_week_table(dates, original, smoothed, start_idx, title):
    """
    Создает таблицу с 7-ю днями, со сглаживанием: дата, исходная и сглаженная температура

     Параметры:
        dates - список дат в формате ДД.ММ.ГГГГ
        original - изначальные температуры
        smoothed - сглаженные температуры
        start_idx - индекс первого дня в окне длиной 7 дней
    """
    print(f"\n    {title}")
    print(f"    с {dates[start_idx]} по {dates[start_idx + WINDOW_SIZE - 1]}:")
    if smoothed is None:
        print("     №    Дата         Исходная")
    else:
        print("     №    Дата         Исходная    Сглаженная")
    for i in range(WINDOW_SIZE):
        idx = start_idx + i  # считаем индекс дня в общем списке
        if smoothed is None:
            print(f"    {i + 1:2}   {dates[idx]:10}   {original[idx]:8.2f}")
        else:
            print(f"    {i + 1:2}   {dates[idx]:10}   {original[idx]:8.2f}   {smoothed[i]:8.2f}")


def do_search_above_threshold(tree):
    """
    Поиск дней с температурой выше порога

    Параметры:
        tree - бинарное дерево поиска
    """
    while True:
        try:
            threshold = float(input("\n    Порог температуры (например, 20): "))  # пользователь задает порог
            break
        except ValueError:
            print("    Ошибка: введите число")

    above = tree.find_above_threshold(threshold)  # делаем поиск значений выше порога в дереве
    print(f"\n    Дни с температурой выше {threshold}:")
    if above:
        for temp, date in sort_pairs_by_temp(above):  # сортируем пары по температуре (температура, дата)
            print(f"    {date}: {temp:.2f}'C")
    else:
        print("    Таких дней нет")


def do_smoothing(dates, temperatures, undo_stack):
    """
    Сглаживание 7 дней по выбранной дате, начиная с заданной даты

    Параметры:
        undo_stack - стек для хранения предыдущих состояний температур, нужен для отмены сглаживания

    Возвращает:
        индекс первого дня в сглаженном окне, если сглаживание не было выполнено, то None
    """
    print("\n7.   Сглаживание температур")
    print("    Введите первую дату из семи подряд (ДД.ММ.ГГГГ, например 25.02.2025)")

    while True:
        start_date = input("\n    Начальная дата: ").strip()  # вызываем функцию анализа, которая находит индекс даты и считает сглаженные значения
        result, error = smooth_week_from_date(dates, temperatures, start_date, WINDOW_SIZE)
        if error:
            print(f"    {error}")
            continue

        start_idx, smoothed_week = result  # принимаем индекс начала и список сглаженных значений
        undo_stack.push(temperatures.copy())  # делаем копию температур в стек, чтобы потом сделать отмену
        original_before = undo_stack.peek()

        for j in range(WINDOW_SIZE):
            temperatures[start_idx + j] = smoothed_week[j]  # перезаписываем значения

        print_week_table(dates, original_before, smoothed_week, start_idx, "Результат сглаживания")
        return start_idx


def do_undo(dates, temperatures, undo_stack, last_start_idx):
    """
    Отмена последнего сглаживания через стек

    Параметры:
        last_start_idx - индекс начала последнего сглаживания, нужен, чтобы вывести таблицу по тем же 7 дням

    Возвращает:
        обновлённый список температур после отмены и новое значение last_start_idx
    """
    if last_start_idx is None:  # проверяем было ли сделано сглаживание
        print("\n    Сначала выполните сглаживание (пункт 7)")
        return temperatures, last_start_idx

    if undo_stack.is_empty():  # проверяем пустой ли стек
        print("\n    Стек пуст, отмену сделать нельзя")
        return temperatures, last_start_idx

    temperatures = undo_stack.pop()  # восстанавливаем сохраненный список температур
    print("\n    Сглаживание отменено. Исходные значения для этих 7 дней:")
    print_week_table(dates, temperatures, None, last_start_idx, "После отмены")
    return temperatures, None


def print_interactive_menu():
    """
    Меню повторных действий для пунктов 6, 7, 8
    """
    print("    Дополнительные действия:")
    print("    6 — новый порог температуры (поиск в дереве)")
    print("    7 — новая дата для сглаживания 7 дней")
    print("    8 — отменить последнее сглаживание")
    print("    0 — выход из программы")

def main():
    print("Анализ температурных данных")

    print("\n1. Загрузка данных")
    dates, temperatures = load_data("data/temperatures.csv")  # загружаем данные
    if len(dates) == 0:
        print("    Ошибка: нет данных для анализа")
        return
    print(f"    Загружено {len(dates)} дней")

    print("\n2. Расчет префиксных сумм")
    prefix_sums = compute_prefix_sums(temperatures)
    print("    Готово")

    print("\n3. Средняя температура по месяцам:")
    month_avg = average_temperature_by_month(dates, temperatures, prefix_sums)
    for month, avg in month_avg:
        print(f"    {month}: {avg:.2f}'C")

    print("\n4. Самый холодный и самый тёплый день:")
    result = find_min_max_temp(temperatures, dates)
    if result[0] is not None:
        (min_day, min_temp), (max_day, max_temp) = result
        print(f"    Самый холодный: {min_day} ({min_temp:.1f}'C)")
        print(f"    Самый тёплый:   {max_day} ({max_temp:.1f}'C)")
    else:
        print("    Нет данных")

    print("\n5. Месяцы, отсортированные по средней температуре:")
    for month, avg in sort_months_by_temp(month_avg):
        print(f"    {month}: {avg:.2f}'C")

    print("\n6. Бинарное дерево поиска (температура -> список дат):")
    tree = build_temperature_tree(dates, temperatures)
    print("    Дерево построено")

    undo_stack = Stack()  # создаем стек для хранения температур
    last_start_idx = None

    # Первый проход по пунктам 6, 7, 8
    do_search_above_threshold(tree)
    last_start_idx = do_smoothing(dates, temperatures, undo_stack)

    print("\n8. Отмена последнего преобразования")
    choice = input("    Отменить сглаживание? (да/нет): ").strip().lower()
    if choice == 'да':
        temperatures, last_start_idx = do_undo(dates, temperatures, undo_stack, last_start_idx)

    while True:  # цикл, чтобы пользователь мог повторить действия (новый порог температуры, новая дата и отмена)
        print_interactive_menu()
        action = input("\n    Выберите пункт (6 / 7 / 8 / 0): ").strip()

        if action == '0':
            print("\n    Программа завершена")
            break
        if action == '6':
            do_search_above_threshold(tree)
        elif action == '7':
            last_start_idx = do_smoothing(dates, temperatures, undo_stack)
        elif action == '8':
            temperatures, last_start_idx = do_undo(dates, temperatures, undo_stack, last_start_idx)
        else:
            print("    Неверный выбор. Введите 6, 7, 8 или 0")


if __name__ == "__main__":
    main()
