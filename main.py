import urllib.request
import random
import base64

# Список источников с четкими названиями стран и протоколами
urls = [
    "https://raw.githubusercontent.com/m-reza-m/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/AzadNet/V2ray-Configs/main/Vless_Configs.txt",
    "https://raw.githubusercontent.com/Leon-K-One/VPN/main/VLESS.txt",
    "https://raw.githubusercontent.com/SadeghHoseini/v2ray-config/main/VLESS.txt",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/vless/base64"
]

all_nodes = []

print("Начинаю сбор серверов с названиями стран...")

for url in urls:
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8').strip()
            
            # Если данные зашифрованы в base64 (часто бывает в подписках), расшифровываем
            if not content.startswith('vless://'):
                try:
                    content = base64.b64decode(content).decode('utf-8')
                except:
                    pass
            
            nodes = [n.strip() for n in content.split('\n') if n.strip()]
            all_nodes.extend(nodes)
            print(f"Загружено из {url}: {len(nodes)} шт.")
    except Exception as e:
        print(f"Пропустил источник {url} из-за ошибки")

# Очистка: только уникальные VLESS конфиги
vless_nodes = list(set([n for n in all_nodes if n.startswith('vless://')]))

# Перемешиваем, чтобы список обновлялся
random.shuffle(vless_nodes)

# Берем ровно 300 штук
final_nodes = vless_nodes[:300]

# Записываем в файл
with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_nodes))

print(f"---")
print(f"Успех! Собрано серверов: {len(final_nodes)}")
print(f"Теперь в NekoBox будут видны страны и флаги.")
