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

WINDOW_SIZE = 7


def print_week_table(dates, original, smoothed, start_idx, title):
    """Таблица для 7 дней: дата, исходная и (при необходимости) сглаженная температура."""
    print(f"\n    {title}")
    print(f"    с {dates[start_idx]} по {dates[start_idx + WINDOW_SIZE - 1]}:")
    if smoothed is None:
        print("     №    Дата         Исходная")
    else:
        print("     №   Дата          Исходная    Сглаженная")
    for i in range(WINDOW_SIZE):
        idx = start_idx + i
        if smoothed is None:
            print(f"    {i + 1:2}   {dates[idx]:10}   {original[idx]:8.2f}")
        else:
            print(f"    {i + 1:2}   {dates[idx]:10}   {original[idx]:8.2f}   {smoothed[i]:8.2f}")


def main():
    print("Анализ температурных данных")

    print("\n1. Загрузка данных...")
    dates, temperatures = load_data("data/temperatures.csv")
    if len(dates) == 0:
        print("    Ошибка: нет данных для анализа")
        return
    print(f"    Загружено {len(dates)} дней")

    print("\n2. Префиксные суммы...")
    prefix_sums = compute_prefix_sums(temperatures)
    print("    Готово")

    print("\n3. Средняя температура по месяцам (префиксные суммы):")
    month_avg = average_temperature_by_month(dates, temperatures, prefix_sums)
    for month, avg in month_avg:
        print(f"    {month}: {avg:.2f}'C")

    print("\n4. Самый холодный и самый тёплый день (линейный поиск):")
    result = find_min_max_temp(temperatures, dates)
    if result[0] is not None:
        (min_day, min_temp), (max_day, max_temp) = result
        print(f"    Самый холодный: {min_day} ({min_temp:.1f}'C)")
        print(f"    Самый тёплый:   {max_day} ({max_temp:.1f}'C)")
    else:
        print("    Нет данных")

    print("\n5. Месяцы, отсортированные по средней температуре (сортировка вставками):")
    for month, avg in sort_months_by_temp(month_avg):
        print(f"    {month}: {avg:.2f}'C")

    print("\n6. Бинарное дерево поиска (температура -> список дат):")
    tree = build_temperature_tree(dates, temperatures)
    print("    Дерево построено")

    while True:
        try:
            threshold = float(input("\n    Порог температуры (например, 20): "))
            break
        except ValueError:
            print("    Ошибка: введите число")

    above = tree.find_above_threshold(threshold)
    print(f"\n    Дни с температурой выше {threshold}'C (рекурсивный обход дерева):")
    if above:
        for temp, date in sort_pairs_by_temp(above):
            print(f"    {date}: {temp:.2f}'C")
    else:
        print("    Таких дней нет")

    print("\n7. Сглаживание (скользящее среднее, окно 7 дней, очередь)")
    print("    Введите первую дату из семи подряд (формат ДД.ММ.ГГГГ, например 25.02.2025)")

    start_idx = None
    smoothed_week = None
    original_before = None

    while True:
        start_date = input("    Начальная дата: ").strip()
        result, error = smooth_week_from_date(dates, temperatures, start_date, WINDOW_SIZE)
        if error:
            print(f"    {error}")
            continue
        start_idx, smoothed_week = result
        break

    undo_stack = Stack()
    undo_stack.push(temperatures.copy())
    original_before = undo_stack.peek()

    for j in range(WINDOW_SIZE):
        temperatures[start_idx + j] = smoothed_week[j]

    print_week_table(dates, original_before, smoothed_week, start_idx, "Результат сглаживания")

    print("\n8. Отмена последнего преобразования (стек)")
    choice = input("\n    Отменить сглаживание? (да/нет): ").strip().lower()

    if choice == 'да':
        if not undo_stack.is_empty():
            temperatures = undo_stack.pop()
            print("    Сглаживание отменено. Восстановлены исходные значения для этих 7 дней:")
            print_week_table(dates, temperatures, None, start_idx, "После отмены")
        else:
            print("    Стек пуст — нечего отменять")
    else:
        print("    Программа завершена")


if __name__ == "__main__":
    main()
