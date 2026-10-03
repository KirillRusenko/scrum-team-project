import math


def f(prompt):
    """Ввод вещественного числа."""
    while True:
        try:
            return float(input(f"{prompt}: ").strip().replace(",", "."))
        except ValueError:
            print("Введите число.")

def i(prompt):
    """Ввод целого числа."""
    while True:
        try:
            return int(input(f"{prompt}: ").strip())
        except ValueError:
            print("Введите целое число.")

def lst(prompt):
    """Ввод списка чисел через пробел/запятую."""
    while True:
        s = input(f"{prompt}: ").strip().replace(",", " ")
        try:
            return [float(x) for x in s.split()]
        except ValueError:
            print("Пример: 5 7 9 11")


print("\n=== ЗАДАНИЕ 1. Потенциальное число ошибок ===")
n_track = i("Количество отслеживаемых параметров")
n_calc  = i("Количество рассчитываемых параметров на цель")
lam     = f("Уровень языка программирования λ")

eta = n_track + n_calc
V_star = (eta + 2) * math.log2(eta + 2)
B1 = V_star**2 / (3000 * lam)

print(f"\nη = {n_track} + {n_calc} = {eta}")
print(f"V* = ({eta}+2)·log2({eta}+2) = {V_star:.4f} бит")
print(f"B  = V*²/(3000·λ) = {B1:.4f}")


print("\n=== ЗАДАНИЕ 2. Структурные параметры ПО ===")
k = eta / 8
K = 2 if k < 8 else round(k)
N = 220 * K + 2 * math.log2(K)
V = 2 * 220 * math.log2(440)
P = 3 * N / 8
m  = i("Количество программистов m")
Vp = i("Производительность V (команд/день)")
Tk = P / (8 * m * Vp)
B2 = V / 3000
Tk_h = Tk * 8

print(f"\nk = η/8 = {eta}/8 = {k:.4f} → K = {K}")
print(f"N = 220·{K} + 2·log2({K}) = {N:.4f} слов")
print(f"V = 2·220·log2(440) = {V:.4f} бит")
print(f"P = 3·{N:.2f}/8 = {P:.4f} ≈ {round(P)} команд")
print(f"Tk = {P:.2f}/(8·{m}·{Vp}) = {Tk:.4f} дней ({Tk_h:.4f} ч)")
print(f"B  = V/3000 = {B2:.4f}")
if B2 > 1:
    print(f"tн = Tk/(2·ln B) = {Tk_h / (2 * math.log(B2)):.4f} ч")
elif abs(B2 - 1) < 1e-9:
    print("tн → ∞ (B ≈ 1)")
else:
    print("tн → ∞ (B < 1, ошибок практически нет)")


print("\n=== ЗАДАНИЕ 3. Рейтинг программиста ===")
R0    = f("Начальный рейтинг R0")
lam   = f("Уровень языка λ")
vols  = lst("Объёмы программ Vj (Кбайт), через пробел")
errs  = lst("Количество ошибок Bk, через пробел")
V_new = f("Объём новой программы (Кбайт)")

n = min(len(vols), len(errs))
vols, errs = vols[:n], errs[:n]
print(f"\nПрограмм: n = {n}, с ошибками: m = {sum(1 for b in errs if b > 0)}")

for name, Kf in [
    ("K = 1/(λ·k + R)",   lambda k, R: 1 / (lam * k + R)),
    ("K = 1/(λ·k·R)",     lambda k, R: 1 / (lam * k * R)),
    ("K = 1/(λ·k) + 1/R", lambda k, R: 1 / (lam * k) + 1 / R),
]:
    R = R0
    print(f"\n--- {name} ---")
    print(f"  R0 = {R:.4f}")
    for k in range(1, n + 1):
        Kk = Kf(k, R)
        delta = vols[k-1] - errs[k-1]
        R = R + Kk * delta
        print(f"  k={k}: K={Kk:.6f}, V−B={delta:+.1f}, R = {R:.4f}")
    print(f"  Итоговый рейтинг: R = {R:.4f}")

B_new = V_new / (lam * 3000)
print(f"\nB новой программы = {V_new}/(λ·3000) = {B_new:.6f}")
