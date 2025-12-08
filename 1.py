import matplotlib.pyplot as plt
import numpy as np

# Данные из условия
I_mag = 0.029012  # А, ток в цепи
# Действующие напряжения на элементах
U_R1 = 2.9099
U_R2 = 2.9099
U_L1 = 1.1849
U_L2 = 1.1849
U_C = 9.2348

# Суммарные напряжения
U_R = U_R1 + U_R2  # сумма напряжений на резисторах
U_L = U_L1 + U_L2  # сумма напряжений на катушках

# Представим векторы в комплексной форме (ток принят за опорный, фаза 0)
I = I_mag + 0j  # ток
V_R = U_R + 0j  # напряжение на резисторах совпадает по фазе с током
V_L = 0 + U_L * 1j  # напряжение на катушках опережает ток на 90°
V_C = 0 - U_C * 1j  # напряжение на конденсаторе отстаёт от тока на 90°

# Общее напряжение
V_total = V_R + V_L + V_C

# Для наглядности создадим список векторов для построения ВДТН
vectors_v = [
    (V_R, 'V_R (R1+R2)', 'green'),
    (V_L, 'V_L (L1+L2)', 'blue'),
    (V_C, 'V_C', 'red'),
    (V_total, 'E (общее)', 'black')
]

# Построение ВДТН (векторная диаграмма напряжений)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Диаграмма напряжений
ax1.set_title('Векторная диаграмма напряжений (ВДТН)')
ax1.axhline(y=0, color='k', linestyle='--', alpha=0.3)
ax1.axvline(x=0, color='k', linestyle='--', alpha=0.3)
ax1.set_xlabel('Re, В')
ax1.set_ylabel('Im, В')
ax1.grid(True)

# Начало координат
origin = 0 + 0j

# Рисуем каждый вектор
for vec, label, color in vectors_v:
    ax1.arrow(np.real(origin), np.imag(origin), np.real(vec), np.imag(vec),
              head_width=0.2, head_length=0.2, fc=color, ec=color, label=label)
    # Подпись конца вектора
    ax1.text(np.real(vec)*1.05, np.imag(vec)*1.05, label, fontsize=9)

ax1.legend(loc='upper left')
ax1.set_xlim([-10, 10])
ax1.set_ylim([-10, 10])
ax1.set_aspect('equal')

# Построение ВДТ (векторная диаграмма тока)
ax2.set_title('Векторная диаграмма тока (ВДТ)')
ax2.axhline(y=0, color='k', linestyle='--', alpha=0.3)
ax2.axvline(x=0, color='k', linestyle='--', alpha=0.3)
ax2.set_xlabel('Re, А')
ax2.set_ylabel('Im, А')
ax2.grid(True)

# Вектор тока (принят за опорный)
ax2.arrow(0, 0, np.real(I), np.imag(I), head_width=0.002, head_length=0.002,
          fc='purple', ec='purple', label='I (ток)')
ax2.text(np.real(I)*1.05, np.imag(I)*1.05, 'I', fontsize=12, color='purple')
ax2.legend(loc='upper left')
ax2.set_xlim([-0.04, 0.04])
ax2.set_ylim([-0.04, 0.04])
ax2.set_aspect('equal')

plt.tight_layout()
plt.show()

# Вывод комплексных значений для проверки
print("Комплексные значения:")
print(f"Ток I = {I:.6f} A")
print(f"Напряжение V_R = {V_R:.4f} В")
print(f"Напряжение V_L = {V_L:.4f} В")
print(f"Напряжение V_C = {V_C:.4f} В")
print(f"Общее напряжение E = {V_total:.4f} В")
print(f"Модуль E = {np.abs(V_total):.4f} В")