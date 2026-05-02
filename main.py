import urllib.request
import random

# Список надежных источников с VLESS конфигами
urls = [
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/sevcator/5ubscrpt10n/main/protocols/vl.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/all_configs.txt"
]

all_nodes = []

print("Начинаю сбор серверов...")

for url in urls:
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            # Разбиваем на строки и убираем пустые
            nodes = [n.strip() for n in data.strip().split('\n') if n.strip()]
            all_nodes.extend(nodes)
            print(f"Загружено из {url}: {len(nodes)} шт.")
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")

# Убираем дубликаты, чтобы не было одинаковых серверов
unique_nodes = list(set(all_nodes))

# Перемешиваем список
random.shuffle(unique_nodes)

# Берем ровно 300 штук (или меньше, если всего добыто меньше 300)
final_nodes = unique_nodes[:300]

# Записываем в файл для подписки
with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_nodes))

print(f"---")
print(f"Итог: выбрано {len(final_nodes)} лучших серверов из {len(unique_nodes)} найденных.")
print(f"Файл ultra_sub.txt обновлен.")
