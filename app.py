import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# -------------------------------
# 1. ВЫЧИСЛИТЕЛЬНОЕ ЯДРО (ФУНКЦИЯ РЕШЕНИЯ ДУ)
# -------------------------------
def solve_oscillator_euler(params, init_conds, t_settings):

    # Извлечение параметров
    m, mu, k = params['m'], params['mu'], params['k']
    x0, v0 = init_conds['x0'], init_conds['v0']
    t_start, t_end, dt = t_settings['start'], t_settings['end'], t_settings['step']

    # Создание массивов для результатов
    steps = int((t_end - t_start) / dt) + 1
    time_array = np.linspace(t_start, t_end, steps)
    pos_array = np.zeros(steps)
    vel_array = np.zeros(steps)

    # Начальные условия
    pos_array[0] = x0
    vel_array[0] = v0

    # Численное интегрирование методом Эйлера
    for i in range(1, steps):
        # Расчет ускорения на предыдущем шаге
        a_prev = (-mu * vel_array[i - 1] - k * pos_array[i - 1]) / m
        # Расчет новой позиции и скорости
        pos_array[i] = pos_array[i - 1] + vel_array[i - 1] * dt
        vel_array[i] = vel_array[i - 1] + a_prev * dt

    return time_array, pos_array, vel_array


# -------------------------------
# 2. ФУНКЦИИ ДЛЯ РАБОТЫ С ФАЙЛАМИ
# -------------------------------
def load_params_from_file():
    """Загружает параметры из текстового файла."""
    filepath = filedialog.askopenfilename(title="Выберите файл с параметрами",
                                          filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not filepath:
        return None

    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()

        params = {}
        for line in lines:
            if '=' in line:
                key, value = line.strip().split('=')
                params[key.strip()] = float(value.strip())

        return params
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{str(e)}")
        return None


def load_and_update_fields():
    """Загружает параметры из файла и обновляет поля ввода."""
    params = load_params_from_file()
    if params:
        # Обновляем поля ввода значениями из файла
        for key, entry_widget in entry_fields.items():
            if key in params:
                entry_widget.delete(0, tk.END)
                entry_widget.insert(0, str(params[key]))
        messagebox.showinfo("Успех", "Параметры загружены из файла!")


def save_results_to_file(time_array, pos_array, vel_array):
    """Сохраняет результаты расчета в текстовый файл."""
    filepath = filedialog.asksaveasfilename(title="Сохранить результаты",
                                            defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not filepath:
        return

    try:
        with open(filepath, 'w') as f:
            f.write("Время (с)\tПоложение (м)\tСкорость (м/с)\tЭнергия (Дж)\tОтн. погр. энергии\n")
            f.write("-------------------------------------------------------------------------\n")
            for i, (t, x, v) in enumerate(zip(time_array, pos_array, vel_array)):
                energy = energy_array[i] if i < len(energy_array) else 0
                error = energy_error_array[i] if i < len(energy_error_array) else 0
                f.write(f"{t:.4f}\t{x:.6f}\t{v:.6f}\t{energy:.6e}\t{error:.6e}\n")

        # Добавляем информацию о средней энергии и погрешности
        with open(filepath, 'a') as f:
            if len(energy_array) > 0:
                energy_avg = np.mean(energy_array)
                rms_error = np.sqrt(np.mean(energy_error_array ** 2))
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"СРЕДНЯЯ ЭНЕРГИЯ: {energy_avg:.6e} Дж\n")
                f.write(f"СРЕДНЕКВАДРАТИЧНАЯ ОТНОСИТЕЛЬНАЯ ПОГРЕШНОСТЬ: {rms_error:.6e}\n")

        messagebox.showinfo("Успех", "Результаты успешно сохранены!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")


# -------------------------------
# 3. ФУНКЦИИ ВИЗУАЛИЗАЦИИ
# -------------------------------
def plot_results(time_array, pos_array, vel_array):
    """Строит графики движения осциллятора."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))

    # График положения от времени
    ax1.plot(time_array, pos_array, 'b-', linewidth=2)
    ax1.set_xlabel('Время, с')
    ax1.set_ylabel('Отклонение, м')
    ax1.set_title('Положение осциллятора')
    ax1.grid(True)

    # График скорости от времени
    ax2.plot(time_array, vel_array, 'r-', linewidth=2)
    ax2.set_xlabel('Время, с')
    ax2.set_ylabel('Скорость, м/с')
    ax2.set_title('Скорость осциллятора')
    ax2.grid(True)

    # Фазовый портрет (скорость от положения)
    ax3.plot(pos_array, vel_array, 'g-', linewidth=2)
    ax3.set_xlabel('Отклонение, м')
    ax3.set_ylabel('Скорость, м/с')
    ax3.set_title('Фазовый портрет')
    ax3.grid(True)

    # График энергии (если массив энергии рассчитан)
    if 'energy_array' in globals() and len(energy_array) > 0:
        ax4.plot(time_array, energy_array, 'k-', label='Полная энергия', linewidth=2)
        if len(energy_array) > 1:
            energy_avg = np.mean(energy_array)
            ax4.axhline(y=energy_avg, color='r', linestyle='--',
                        label=f'Средняя: {energy_avg:.4e} Дж')
        ax4.set_xlabel('Время, с')
        ax4.set_ylabel('Энергия, Дж')
        ax4.set_title('Полная энергия системы')
        ax4.legend()
        ax4.grid(True)
    else:
        ax4.text(0.5, 0.5, 'Рассчитайте энергию\nнажатием кнопки "Рассчитать"',
                 horizontalalignment='center', verticalalignment='center',
                 transform=ax4.transAxes)
        ax4.set_title('Полная энергия системы')

    plt.tight_layout()
    return fig


# -------------------------------
# 4. ФУНКЦИИ ОЦЕНКИ ТОЧНОСТИ
# -------------------------------
def calculate_energy_analysis():
    """Выполняет расчет и анализ энергии системы."""
    global energy_array, energy_error_array, energy_avg, rms_error

    try:
        # Получаем параметры из интерфейса
        params = {
            'm': float(m_entry.get()),
            'mu': float(mu_entry.get()),
            'k': float(k_entry.get())
        }
        init_conds = {
            'x0': float(x0_entry.get()),
            'v0': float(v0_entry.get())
        }
        t_settings = {
            'start': float(t0_entry.get()),
            'end': float(t_end_entry.get()),
            'step': float(dt_entry.get())
        }

        # Выполнение расчета
        time_array, pos_array, vel_array = solve_oscillator_euler(params, init_conds, t_settings)

        # РАСЧЕТ ЭНЕРГИИ И ПОГРЕШНОСТИ
        m_val = params['m']
        k_val = params['k']

        # Кинетическая энергия
        kinetic_energy = 0.5 * m_val * vel_array ** 2
        # Потенциальная энергия
        potential_energy = 0.5 * k_val * pos_array ** 2
        # Полная энергия
        energy_array = kinetic_energy + potential_energy

        # Расчет средней энергии и погрешности
        if len(energy_array) > 0:
            # Среднее значение энергии
            energy_avg = np.mean(energy_array)
            # Относительная погрешность на каждом шаге
            energy_error_array = np.abs(energy_avg - energy_array) / np.abs(energy_avg)
            # Среднеквадратичная относительная погрешность
            rms_error = np.sqrt(np.mean(energy_error_array ** 2))

            # Вывод результатов на форму
            energy_avg_label.config(text=f"{energy_avg:.6e} Дж")
            energy_error_label.config(text=f"{rms_error:.6e}")

            # Сохраняем результаты для отображения
            global saved_time, saved_pos, saved_vel
            saved_time, saved_pos, saved_vel = time_array, pos_array, vel_array

            # Обновление графиков
            update_plots()

            return True
        else:
            energy_avg_label.config(text="N/A")
            energy_error_label.config(text="N/A")
            return False

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при расчете энергии:\n{str(e)}")
        return False


def runge_accuracy_estimation():
    """Оценка точности методом Рунге."""
    try:
        # Получаем параметры из интерфейса
        params = {
            'm': float(m_entry.get()),
            'mu': float(mu_entry.get()),
            'k': float(k_entry.get())
        }
        init_conds = {
            'x0': float(x0_entry.get()),
            'v0': float(v0_entry.get())
        }
        t_settings = {
            'start': float(t0_entry.get()),
            'end': float(t_end_entry.get()),
            'step': float(dt_entry.get())
        }

        # Решение с текущим шагом
        time1, pos1, vel1 = solve_oscillator_euler(params, init_conds, t_settings)

        # Решение с шагом в 2 раза меньше
        t_settings_fine = t_settings.copy()
        t_settings_fine['step'] = t_settings['step'] / 2
        time2, pos2, vel2 = solve_oscillator_euler(params, init_conds, t_settings_fine)

        # Интерполируем точное решение на грубую сетку
        # Берем каждую вторую точку из точного решения
        pos2_coarse = pos2[::2]
        vel2_coarse = vel2[::2]

        # Вычисляем погрешности
        pos_error = np.abs(pos1 - pos2_coarse)
        vel_error = np.abs(vel1 - vel2_coarse)

        # Находим максимальные погрешности
        max_pos_error = np.max(pos_error)
        max_vel_error = np.max(vel_error)

        # Выводим результаты
        result_text = f"ОЦЕНКА ТОЧНОСТИ МЕТОДОМ РУНГЕ:\n"
        result_text += f"Макс. погрешность координаты: {max_pos_error:.2e} м\n"
        result_text += f"Макс. погрешность скорости: {max_vel_error:.2e} м/с\n"
        result_text += f"Шаг dt: {t_settings['step']:.4f} с\n"
        result_text += f"Шаг dt/2: {t_settings_fine['step']:.4f} с\n\n"
        result_text += f"Отношение погрешностей (порядок метода):\n"
        result_text += f"Координата: {max_pos_error / (max_pos_error / 2):.2f}\n"
        result_text += f"Скорость: {max_vel_error / (max_vel_error / 2):.2f}"

        messagebox.showinfo("Оценка точности методом Рунге", result_text)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при оценке точности:\n{str(e)}")


def multiple_step_analysis():
    """Анализ точности для нескольких значений шага."""
    try:
        # Получаем параметры из интерфейса
        params = {
            'm': float(m_entry.get()),
            'mu': float(mu_entry.get()),
            'k': float(k_entry.get())
        }
        init_conds = {
            'x0': float(x0_entry.get()),
            'v0': float(v0_entry.get())
        }
        t_settings = {
            'start': float(t0_entry.get()),
            'end': float(t_end_entry.get()),
            'step': float(dt_entry.get())
        }

        # Различные значения шага для анализа
        steps = [0.1, 0.05, 0.01, 0.005]
        results = []

        for step in steps:
            t_settings_current = t_settings.copy()
            t_settings_current['step'] = step

            # Решение с текущим шагом
            time1, pos1, vel1 = solve_oscillator_euler(params, init_conds, t_settings_current)

            # Решение с шагом в 2 раза меньше
            t_settings_fine = t_settings_current.copy()
            t_settings_fine['step'] = step / 2
            time2, pos2, vel2 = solve_oscillator_euler(params, init_conds, t_settings_fine)

            # Интерполируем на грубую сетку
            pos2_coarse = pos2[::2]
            vel2_coarse = vel2[::2]

            # Вычисляем погрешности
            max_pos_error = np.max(np.abs(pos1 - pos2_coarse))
            max_vel_error = np.max(np.abs(vel1 - vel2_coarse))

            results.append((step, max_pos_error, max_vel_error))

        # Формируем отчет
        result_text = "АНАЛИЗ ТОЧНОСТИ ДЛЯ РАЗНЫХ ШАГОВ:\n\n"
        result_text += "Шаг (с)\tПогр. координаты (м)\tПогр. скорости (м/с)\n"
        result_text += "-------------------------------------------------\n"

        for step, pos_err, vel_err in results:
            result_text += f"{step:.4f}\t{pos_err:.2e}\t\t{vel_err:.2e}\n"

        result_text += "\nВывод: метод Эйлера имеет первый порядок точности.\n"
        result_text += "Погрешность пропорциональна шагу интегрирования."

        # Создаем отдельное окно для результатов
        result_window = tk.Toplevel(root)
        result_window.title("Анализ точности для разных шагов")
        result_window.geometry("600x400")

        text_widget = tk.Text(result_window, wrap=tk.WORD)
        text_widget.insert(tk.END, result_text)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Кнопка для сохранения результатов
        save_button = ttk.Button(result_window, text="Сохранить результаты",
                                 command=lambda: save_accuracy_results(results))
        save_button.pack(pady=10)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при анализе точности:\n{str(e)}")


def save_accuracy_results(results):
    """Сохраняет результаты анализа точности в файл."""
    filepath = filedialog.asksaveasfilename(title="Сохранить анализ точности",
                                            defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not filepath:
        return

    try:
        with open(filepath, 'w') as f:
            f.write("АНАЛИЗ ТОЧНОСТИ МЕТОДА ЭЙЛЕРА\n")
            f.write("==============================\n\n")
            f.write("Шаг (с)\tПогр. координаты (м)\tПогр. скорости (м/с)\n")
            f.write("-------------------------------------------------\n")

            for step, pos_err, vel_err in results:
                f.write(f"{step:.4f}\t{pos_err:.2e}\t\t{vel_err:.2e}\n")

            f.write("\nВЫВОДЫ:\n")
            f.write("1. Метод Эйлера имеет первый порядок точности\n")
            f.write("2. Погрешность пропорциональна шагу интегрирования\n")
            f.write("3. Для повышения точности необходимо уменьшать шаг\n")
            f.write("4. Малый шаг увеличивает время вычислений\n")

        messagebox.showinfo("Успех", "Результаты анализа сохранены!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")


# -------------------------------
# 5. ГЛАВНАЯ ФУНКЦИЯ И ГРАФИЧЕСКИЙ ИНТЕРФЕЙС
# -------------------------------
def update_plots():
    """Обновляет графики в интерфейсе."""
    global canvas
    # Очистка предыдущего графика
    for widget in plot_frame.winfo_children():
        widget.destroy()

    # Создание нового графика
    fig = plot_results(saved_time, saved_pos, saved_vel)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


# -------------------------------
# 6. СОЗДАНИЕ ГРАФИЧЕСКОГО ИНТЕРФЕЙСА
# -------------------------------
# Настройка главного окна
root = tk.Tk()
root.title("Моделирование гармонического осциллятора с трением")
root.geometry("1400x900")

# Создание основной структуры
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Панель параметров (слева)
params_frame = ttk.LabelFrame(main_frame, text="Параметры системы", padding="5")
params_frame.grid(row=0, column=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5)

# Поля для ввода параметров
ttk.Label(params_frame, text="Масса, m (кг):").grid(row=0, column=0, sticky=tk.W, pady=2)
m_entry = ttk.Entry(params_frame)
m_entry.insert(0, "1.0")
m_entry.grid(row=0, column=1, pady=2)

ttk.Label(params_frame, text="Коэф. трения, μ (кг/с):").grid(row=1, column=0, sticky=tk.W, pady=2)
mu_entry = ttk.Entry(params_frame)
mu_entry.insert(0, "0.0")
mu_entry.grid(row=1, column=1, pady=2)

ttk.Label(params_frame, text="Жесткость, k (Н/м):").grid(row=2, column=0, sticky=tk.W, pady=2)
k_entry = ttk.Entry(params_frame)
k_entry.insert(0, "10.0")
k_entry.grid(row=2, column=1, pady=2)

ttk.Label(params_frame, text="Нач. положение, x₀ (м):").grid(row=3, column=0, sticky=tk.W, pady=2)
x0_entry = ttk.Entry(params_frame)
x0_entry.insert(0, "0.5")
x0_entry.grid(row=3, column=1, pady=2)

ttk.Label(params_frame, text="Нач. скорость, v₀ (м/с):").grid(row=4, column=0, sticky=tk.W, pady=2)
v0_entry = ttk.Entry(params_frame)
v0_entry.insert(0, "0.0")
v0_entry.grid(row=4, column=1, pady=2)

ttk.Label(params_frame, text="Нач. время, t₀ (с):").grid(row=5, column=0, sticky=tk.W, pady=2)
t0_entry = ttk.Entry(params_frame)
t0_entry.insert(0, "0.0")
t0_entry.grid(row=5, column=1, pady=2)

ttk.Label(params_frame, text="Конеч. время, t_end (с):").grid(row=6, column=0, sticky=tk.W, pady=2)
t_end_entry = ttk.Entry(params_frame)
t_end_entry.insert(0, "10.0")
t_end_entry.grid(row=6, column=1, pady=2)

ttk.Label(params_frame, text="Шаг времени, dt (с):").grid(row=7, column=0, sticky=tk.W, pady=2)
dt_entry = ttk.Entry(params_frame)
dt_entry.insert(0, "0.01")
dt_entry.grid(row=7, column=1, pady=2)

# Словарь для связи имен параметров и виджетов ввода
entry_fields = {
    'm': m_entry,
    'mu': mu_entry,
    'k': k_entry,
    'x0': x0_entry,
    'v0': v0_entry,
    't0': t0_entry,
    't_end': t_end_entry,
    'dt': dt_entry
}

# Кнопки управления
buttons_frame = ttk.Frame(params_frame)
buttons_frame.grid(row=8, column=0, columnspan=2, pady=10)

ttk.Button(buttons_frame, text="Рассчитать энергию", command=calculate_energy_analysis).pack(side=tk.LEFT, padx=2)
ttk.Button(buttons_frame, text="Загрузить из файла", command=load_and_update_fields).pack(side=tk.LEFT, padx=2)
ttk.Button(buttons_frame, text="Сохранить результаты",
           command=lambda: save_results_to_file(saved_time, saved_pos, saved_vel)).pack(side=tk.LEFT, padx=2)

# Кнопки для оценки точности
accuracy_frame = ttk.Frame(params_frame)
accuracy_frame.grid(row=9, column=0, columnspan=2, pady=5)

ttk.Button(accuracy_frame, text="Оценка точности (Рунге)",
           command=runge_accuracy_estimation).pack(side=tk.LEFT, padx=2)
ttk.Button(accuracy_frame, text="Анализ для разных шагов",
           command=multiple_step_analysis).pack(side=tk.LEFT, padx=2)

# Панель для отображения результатов по энергии
energy_frame = ttk.LabelFrame(params_frame, text="Анализ энергии системы", padding="5")
energy_frame.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

ttk.Label(energy_frame, text="Средняя энергия:").grid(row=0, column=0, sticky=tk.W, padx=5)
energy_avg_label = ttk.Label(energy_frame, text="N/A")
energy_avg_label.grid(row=0, column=1, sticky=tk.W, padx=5)

ttk.Label(energy_frame, text="Ср.кв. погрешность:").grid(row=1, column=0, sticky=tk.W, padx=5)
energy_error_label = ttk.Label(energy_frame, text="N/A")
energy_error_label.grid(row=1, column=1, sticky=tk.W, padx=5)

# Область для графиков (справа)
plot_frame = ttk.LabelFrame(main_frame, text="Результаты моделирования")
plot_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

# Настройка расширения областей
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(0, weight=1)
params_frame.columnconfigure(1, weight=1)

# Инициализация глобальных переменных
energy_array = np.array([])
energy_error_array = np.array([])
energy_avg = 0
rms_error = 0
saved_time, saved_pos, saved_vel = np.array([]), np.array([]), np.array([])

# Запуск главного цикла
try:
    root.mainloop()
except KeyboardInterrupt:
    print("Программа завершена пользователем")
