import os

# Просто читаем переменные окружения (если заданы)
cell_1 = os.getenv("CELL_1", "A1")
cell_2 = os.getenv("CELL_2", "H8")
figure = os.getenv("FIGURE", "ферзь")

print("🚀 Приложение успешно запущено внутри Docker контейнера!")
print(f"Параметры окружения:")
print(f"  CELL_1 = {cell_1}")
print(f"  CELL_2 = {cell_2}")
print(f"  FIGURE = {figure}")

# Логика — просто пример вычисления
result = f"Комбинация: {figure} из {cell_1} в {cell_2}"
print(result)

print("✅ Всё выполнено успешно!")
