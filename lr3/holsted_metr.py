import math


def log2(x: float) -> float:
    return math.log(x) / math.log(2)


def ask_int(prompt: str) -> int:
    """Запрос целого числа с валидацией."""
    while True:
        s = input(f"{prompt}: ").strip().replace(",", ".")
        if not s:
            print("   Значение не может быть пустым. Повторите ввод.")
            continue
        try:
            return int(s)
        except ValueError:
            print(f" '{s}' не является целым числом. Повторите ввод.")


def ask_double(prompt: str) -> float:
    """Запрос вещественного числа с валидацией."""
    while True:
        s = input(f"{prompt}: ").strip().replace(",", ".")
        if not s:
            print("  Значение не может быть пустым. Повторите ввод.")
            continue
        try:
            return float(s)
        except ValueError:
            print(f"   '{s}' не является числом. Повторите ввод.")


def ask_positive_int(prompt: str) -> int:
    """Запрос положительного целого числа."""
    while True:
        v = ask_int(prompt)
        if v > 0:
            return v
        print("  Значение должно быть положительным. Повторите ввод.")


def ask_positive_double(prompt: str) -> float:
    """Запрос положительного вещественного числа."""
    while True:
        v = ask_double(prompt)
        if v > 0:
            return v
        print("  Значение должно быть положительным. Повторите ввод.")


#Общие расчёты метрик Холстеда
def compute_halstead(n1: int, n2: int, N1: int, N2: int, lam: float) -> dict:
    """
    n1, n2 — количество уникальных операторов/операндов;
    N1, N2 — общее число операторов/операндов;
    lam    — уровень языка программирования (λ).
    """
    n = n1 + n2
    N = N1 + N2
    V = N * log2(n) if n > 1 else 0
    V_star = (n2 + 2) * log2(n2 + 2) if n2 + 2 > 0 else 0
    B = V_star * V_star / (3000 * lam) if lam > 0 else 0
    L = V_star / V if V > 0 else 0
    L_hat = 2 * n2 / (n1 * N2) if n1 * N2 > 0 else 0
    E = V / L if L > 0 else 0
    T = E / 18 if E > 0 else 0
    return {
        "n1": n1, "n2": n2, "N1": N1, "N2": N2,
        "n": n, "N": N, "V": V, "V_star": V_star,
        "B": B, "L": L, "L_hat": L_hat, "E": E, "T": T,
    }


# Задание 1

def task1():
    print("\n--- Задание 1. Потенциальное число ошибок ПО БКС ---")
    targets = ask_positive_int("Число одновременно сопровождаемых целей")
    measures = ask_positive_int("Количество измерений каждого отслеживаемого параметра")
    tracked = ask_positive_int("Количество отслеживаемых параметров")
    calculated = ask_positive_int("Количество рассчитываемых параметров по каждой цели")
    lam = ask_positive_double("Уровень языка программирования λ")

    input_params = targets * tracked * measures
    output_params = targets * calculated
    n2 = input_params + output_params

    v_star = (n2 + 2) * log2(n2 + 2)
    b = v_star * v_star / (3000 * lam)

    print("\nРезультаты задания 1:")
    print(f"  Входные параметры:  {targets} × {tracked} × {measures} = {input_params}")
    print(f"  Выходные параметры: {targets} × {calculated} = {output_params}")
    print(f"  n2* = {n2}")
    print(f"  Потенциальный объём V* = {v_star:.2f} бит")
    print(f"  Потенциальное число ошибок B = {b:.4f}")


# Задание 2

def task2():
    print("\n--- Задание 2. Структурные параметры, объём, время, надёжность ---")
    targets = ask_positive_int("Число одновременно сопровождаемых целей")
    measures = ask_positive_int("Количество измерений каждого отслеживаемого параметра")
    tracked = ask_positive_int("Количество отслеживаемых параметров")
    calculated = ask_positive_int("Количество рассчитываемых параметров по каждой цели")
    m = ask_positive_int("Количество программистов в бригаде m")
    nu = ask_positive_int("Производительность ν (отлаженных команд в день)")
    work_day = ask_positive_int("Длительность рабочего дня, часов")

    n2 = targets * tracked * measures + targets * calculated

    k = n2 / 8
    levels = 1
    if k > 8:
        levels = log2(n2) / 3 + 1
        K = n2 / 8 + n2 / 64
    else:
        K = k

    N = 220 * K + K * log2(K) if K > 0 else 0
    V = K * 220 * log2(48) if K > 0 else 0
    P = 3 * N / 8
    Tk_days = 3 * N / (8.0 * m * nu) if m * nu > 0 else 0
    B = V / 3000 if V > 0 else 0
    tN = Tk_days * work_day / (2 * math.log(B)) if B > 1 else 0

    print("\nРезультаты задания 2:")
    print(f"  n2* = {n2:.0f}")
    print(f"  Число модулей k = n2*/8 = {k:.2f}")
    if k > 8:
        print(f"  k >> 8, уровней i = {levels:.2f} (округл. {round(levels)})")
        print(f"  Число модулей с учётом иерархии K = {K:.2f}")
    print(f"  Длина программы N = {N:.2f}")
    print(f"  Объём ПО V = {V:.2f} бит")
    print(f"  Команд ассемблера P = {P:.2f}")
    print(f"  Календарное время Tk = {Tk_days:.2f} дней ({Tk_days * work_day:.2f} часов)")
    print(f"  Потенциальное число ошибок B = {B:.2f}")
    print(f"  Начальная надёжность tн = {tN:.2f} часов")


# Задание 3

def c_coef(lam: float, R: float, variant: int) -> float:
    """Коэффициент c(λ, R)."""
    if variant == 1:
        return 1.0 / (lam + R)
    elif variant == 2:
        return 1.0 / (lam * R)
    else:
        return 1.0 / lam + 1.0 / R


def task3():
    print("\n--- Задание 3. Рейтинг программиста и ожидаемое число ошибок ---")
    R0 = ask_positive_double("Начальный рейтинг R0")
    lam = ask_positive_double("Уровень языка λ")
    n = ask_positive_int("Количество написанных программ за период")

    V, B = [], []
    print("Введите объём (Кбайт) и число ошибок каждой программы:")
    for j in range(n):
        v = ask_positive_double(f"  Программа {j + 1}: объём V (Кбайт)")
        b = ask_double(f"  Программа {j + 1}: ошибки B")  # ошибок может быть 0
        V.append(v)
        B.append(b)

    V_next = ask_positive_double("Объём следующей программы (Кбайт)")
    sum_v = sum(V)

    names = ["c = 1/(λ+R)", "c = 1/(λ·R)", "c = 1/λ + 1/R"]
    print("\nРезультаты задания 3 (три варианта коэффициента):")
    for variant in range(1, 4):
        c0 = c_coef(lam, R0, variant)
        penalty = sum(b / c0 for b in B if b > 0)
        R1 = R0 * (1 + 1e-3 * (sum_v - penalty))
        B_next = c_coef(lam, R1, variant) * V_next

        print(f"\n  Вариант {variant}: {names[variant - 1]}")
        print(f"    c(λ, R0) = {c0:.6f}, штраф Σ Bk/c = {penalty:.4f}")
        print(f"    Текущий рейтинг R1 = {R1:.2f}")
        print(f"    Ожидаемое число ошибок в программе {V_next:.0f} Кбайт: B = {B_next:.5f}")


# ---------- Задание 4 (универсальный расчёт Холстеда) ----------
'''
def task4():
    print("\n--- Задание 4. Универсальный расчёт метрик Холстеда ---")
    n1 = ask_positive_int("Уникальные операторы n1")
    n2 = ask_positive_int("Уникальные операнды n2")
    N1 = ask_positive_int("Всего операторов N1")
    N2 = ask_positive_int("Всего операндов N2")
    lam = ask_positive_double("Уровень языка λ")

    r = compute_halstead(n1, n2, N1, N2, lam)

    print("\nРезультаты расчёта метрик Холстеда:")
    print(f"  Словарь программы n = n1 + n2 = {r['n']}")
    print(f"  Длина программы N = N1 + N2 = {r['N']}")
    print(f"  Объём программы V = N·log2(n) = {r['V']:.2f} бит")
    print(f"  Потенциальный объём V* = (n2+2)·log2(n2+2) = {r['V_star']:.2f} бит")
    print(f"  Потенциальное число ошибок B = V*²/(3000·λ) = {r['B']:.4f}")
    print(f"  Уровень программы L = V*/V = {r['L']:.4f}")
    print(f"  Оценка уровня L^ = 2·n2/(n1·N2) = {r['L_hat']:.4f}")
    print(f"  Сложность E = V/L = {r['E']:.2f}")
    print(f"  Время программирования T = E/18 = {r['T']:.2f} сек ({r['T'] / 3600:.2f} ч)")

'''
# ---------- Главное меню ----------

def main():
    while True:
        print()
        print("Лабораторная работа №3. Метрики Холстеда")
        print("1 - Задание 1: потенциальное число ошибок ПО БКС")
        print("2 - Задание 2: структура, объём, время, надёжность ПО")
        print("3 - Задание 3: рейтинг программиста")
        print("0 - Выход")
        choice = input("Выбор: ").strip()

        if choice == "1":
            task1()
        elif choice == "2":
            task2()
        elif choice == "3":
            task3()
        elif choice == "0":
            print("Выход.")
            return
        else:
            print("Нет такого пункта меню.")


if __name__ == "__main__":
    main()
