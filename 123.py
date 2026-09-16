# %% Исходные данные
employees_data = [
    {'name': 'Анна Смирнова', 'department': 'Продажи', 'sales': 1500000, 'deals_count': 45, 'satisfaction': 4.8},
    {'name': 'Игорь Петров', 'department': 'Продажи', 'sales': 2300000, 'deals_count': 62, 'satisfaction': 4.5},
    {'name': 'Елена Козлова', 'department': 'Маркетинг', 'sales': 800000, 'deals_count': 15, 'satisfaction': 4.9},
    {'name': 'Дмитрий Иванов', 'department': 'Продажи', 'sales': 950000, 'deals_count': 28, 'satisfaction': 4.2},
    {'name': 'Мария Сидорова', 'department': 'Маркетинг', 'sales': 1200000, 'deals_count': 22, 'satisfaction': 4.7},
    {'name': 'Алексей Морозов', 'department': 'Продажи', 'sales': 3100000, 'deals_count': 78, 'satisfaction': 4.6},
    {'name': 'Ольга Волкова', 'department': 'Поддержка', 'sales': 0, 'deals_count': 0, 'satisfaction': 4.9},
    {'name': 'Сергей Кузнецов', 'department': 'Продажи', 'sales': 1800000, 'deals_count': 51, 'satisfaction': 4.4},
    {'name': 'Наталья Белова', 'department': 'Маркетинг', 'sales': 950000, 'deals_count': 18, 'satisfaction': 4.3},
    {'name': 'Павел Новиков', 'department': 'Поддержка', 'sales': 0, 'deals_count': 0, 'satisfaction': 4.8}
]


# ---------- Вспомогательные функции: расчёты ----------

def calculate_total_sales(data):
    """Общая сумма продаж по всем сотрудникам."""
    return sum(employee['sales'] for employee in data)


def calculate_total_deals(data):
    """Общее количество закрытых сделок."""
    return sum(employee['deals_count'] for employee in data)


def calculate_average_deal_size(total_sales, total_deals):
    """Средняя сумма сделки по компании (защита от деления на 0)."""
    if total_deals == 0:
        return 0
    return total_sales / total_deals


def calculate_sales_by_department(data):
    """Сумма продаж по каждому отделу в виде словаря {отдел: сумма}."""
    sales_by_department = {}
    for employee in data:
        department = employee['department']
        sales_by_department[department] = sales_by_department.get(department, 0) + employee['sales']
    return sales_by_department


# ---------- Вспомогательные функции: отбор/фильтрация ----------

def get_top_sales_employees(data, top_n=3):
    """Топ-N сотрудников по сумме продаж.
    Возвращает список словарей [{'name': ..., 'sales': ...}]
    """
    sorted_employees = sorted(data, key=lambda employee: employee['sales'], reverse=True)
    top_employees = sorted_employees[:top_n]
    return [{'name': employee['name'], 'sales': employee['sales']} for employee in top_employees]


def get_training_candidates(data, satisfaction_threshold=4.5):
    """Сотрудники с 0 сделок ИЛИ удовлетворённостью ниже порога."""
    return [
        employee for employee in data
        if employee['deals_count'] == 0 or employee['satisfaction'] < satisfaction_threshold
    ]


def calculate_average_sales(data):
    """Средний объём продаж по всей компании (переиспользуем calculate_total_sales)."""
    if not data:
        return 0
    total_sales = calculate_total_sales(data)
    return total_sales / len(data)


def get_above_average_performers(employees):
    """Сотрудники, чьи продажи выше среднего по компании."""
    average_sales = calculate_average_sales(employees)
    return [employee for employee in employees if employee['sales'] > average_sales]


def calculate_bonuses(employees, total_bonus_fund):
    """Распределяет премиальный фонд пропорционально вкладу в продажи.

    Формула: (личные продажи / общие продажи компании) * общий фонд.
    Если satisfaction < 4.0 — бонус сотрудника уменьшается в 2 раза,
    а "сэкономленная" часть НЕ перераспределяется другим (сгорает).
    Возвращает новый список словарей с добавленным ключом 'bonus'.
    """
    total_sales = calculate_total_sales(employees)

    employees_with_bonus = []
    for employee in employees:
        if total_sales == 0:
            # Защита от деления на 0, если у всех продажи нулевые
            bonus = 0
        else:
            share_of_sales = employee['sales'] / total_sales
            bonus = share_of_sales * total_bonus_fund

            # Штраф за низкую удовлетворённость: бонус уменьшается вдвое,
            # остаток при этом сгорает (не идёт другим сотрудникам)
            if employee['satisfaction'] < 4.0:
                bonus = bonus / 2

        # Создаём новый словарь (копию), чтобы не мутировать исходные данные
        employee_with_bonus = employee.copy()
        employee_with_bonus['bonus'] = round(bonus, 2)
        employees_with_bonus.append(employee_with_bonus)

    return employees_with_bonus


# ---------- Вспомогательные функции: форматированный вывод ----------

def print_general_metrics(total_sales, total_deals, average_deal_size):
    print("=" * 50)
    print("1. ОБЩИЕ ПОКАЗАТЕЛИ")
    print("=" * 50)
    print(f"Общая сумма продаж:      {total_sales:,.0f} руб.".replace(",", " "))
    print(f"Общее количество сделок: {total_deals}")
    print(f"Средняя сумма сделки:    {average_deal_size:,.0f} руб.".replace(",", " "))
    print()


def print_department_analytics(sales_by_department):
    print("=" * 50)
    print("2. АНАЛИТИКА ПО ОТДЕЛАМ")
    print("=" * 50)
    for department, sales in sorted(sales_by_department.items(), key=lambda item: item[1], reverse=True):
        print(f"{department:<15} {sales:,.0f} руб.".replace(",", " "))
    print()


def print_bonus_candidates(top_employees):
    print("=" * 50)
    print("3. КАНДИДАТЫ НА ПРЕМИЮ (топ-3 по продажам)")
    print("=" * 50)
    for i, employee in enumerate(top_employees, start=1):
        print(f"{i}. {employee['name']:<20} {employee['sales']:,.0f} руб.".replace(",", " "))
    print()


def print_training_candidates(training_candidates):
    print("=" * 50)
    print("4. КАНДИДАТЫ НА ОБУЧЕНИЕ")
    print("=" * 50)
    if not training_candidates:
        print("Нет сотрудников, требующих обучения.")
    else:
        for employee in training_candidates:
            print(f"- {employee['name']:<20} сделок: {employee['deals_count']:<4} "
                  f"удовлетворённость: {employee['satisfaction']}")
    print()


# ---------- Главная функция ----------

def generate_report(data):
    """Главная функция: только вызывает расчёты и печатает отчёт."""
    total_sales = calculate_total_sales(data)
    total_deals = calculate_total_deals(data)
    average_deal_size = calculate_average_deal_size(total_sales, total_deals)
    sales_by_department = calculate_sales_by_department(data)
    top_employees = get_top_sales_employees(data, top_n=3)
    training_candidates = get_training_candidates(data)

    print_general_metrics(total_sales, total_deals, average_deal_size)
    print_department_analytics(sales_by_department)
    print_bonus_candidates(top_employees)
    print_training_candidates(training_candidates)


if __name__ == "__main__":
    generate_report(employees_data)

    print("=" * 50)
    print("ЗАДАНИЕ 2: СОТРУДНИКИ ВЫШЕ СРЕДНЕГО ПО ПРОДАЖАМ")
    print("=" * 50)
    average_sales = calculate_average_sales(employees_data)
    print(f"Средние продажи по компании: {average_sales:,.0f} руб.".replace(",", " "))
    above_average = get_above_average_performers(employees_data)
    for employee in above_average:
        print(f"- {employee['name']:<20} {employee['sales']:,.0f} руб.".replace(",", " "))

    print()
    print("=" * 50)
    print("ЗАДАНИЕ 3: РАСПРЕДЕЛЕНИЕ ПРЕМИАЛЬНОГО ФОНДА (500 000 руб.)")
    print("=" * 50)
    employees_with_bonuses = calculate_bonuses(employees_data, total_bonus_fund=500000)
    for employee in employees_with_bonuses:
        flag = " (штраф за satisfaction < 4.0)" if employee['satisfaction'] < 4.0 else ""
        print(f"- {employee['name']:<20} бонус: {employee['bonus']:,.2f} руб.{flag}".replace(",", " "))
# %%
