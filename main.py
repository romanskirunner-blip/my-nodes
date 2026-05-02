import urllib.request
import random
import base64

# Источники, которые лучше всего обходят блокировки мессенджеров
urls = [
    "https://raw.githubusercontent.com/coldwater-10/clash_vless/main/vless.txt",
    "https://raw.githubusercontent.com/Nomad-Developer/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/proxies",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/vless.txt",
    "https://raw.githubusercontent.com/Surfboardv2ray/TG-Proxy-Config/main/V2ray/Vless.txt"
]

all_nodes = []
headers = {'User-Agent': 'v2rayNG/1.8.5'} # Маскируемся под приложение

print("Запуск сбора 'бронебойных' конфигов...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8').strip()
            
            # Если данные в Base64, расшифровываем
            if not content.startswith('vless://'):
                try:
                    content = base64.b64decode(content).decode('utf-8')
                except:
                    pass
            
            # Вытаскиваем только VLESS ссылки
            nodes = [n.strip() for n in content.split('\n') if n.startswith('vless://')]
            all_nodes.extend(nodes)
            print(f"ОК: {url} (Найдено: {len(nodes)})")
    except:
        print(f"Пропустил источник {url}")

# Убираем дубликаты
vless_nodes = list(set(all_nodes))

# Перемешиваем и берем 300 штук
random.shuffle(vless_nodes)
final_nodes = vless_nodes[:300]

# Кодируем в Base64 для стабильной работы NekoBox
subscription_data = "\n".join(final_nodes)
encoded_data = base64.b64encode(subscription_data.encode('utf-8')).decode('utf-8')

with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write(encoded_data)

print(f"---")
print(f"Успех! Собрано и зашифровано: {len(final_nodes)} серверов.")
