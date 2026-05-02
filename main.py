import urllib.request
import random
import base64
import ssl

# Отключаем проверку сертификатов, чтобы GitHub не ругался на источники
context = ssl._create_unverified_context()

# Свежие источники, которые работают прямо сейчас
urls = [
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/all_configs.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/vless.txt",
    "https://raw.githubusercontent.com/NiREAs/v2ray-collector/main/sub/vless",
    "https://raw.githubusercontent.com/LalatinaHub/Mineral/master/vless.txt"
]

all_nodes = []
# Маскируемся под реальный браузер
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

print("Запуск экстренного сбора прокси...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=context) as response:
            raw_content = response.read().decode('utf-8').strip()
            
            # Проверка на Base64
            if "vless://" not in raw_content[:100]:
                try:
                    content = base64.b64decode(raw_content).decode('utf-8')
                except:
                    content = raw_content
            else:
                content = raw_content
            
            nodes = [n.strip() for n in content.split('\n') if n.startswith('vless://')]
            all_nodes.extend(nodes)
            print(f"Успешно: {url} (Найдено: {len(nodes)})")
    except Exception as e:
        print(f"Ошибка на {url}: {e}")

# Убираем дубликаты и берем 300 штук
vless_nodes = list(set(all_nodes))
random.shuffle(vless_nodes)
final_nodes = vless_nodes[:300]

# Записываем в файл
with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_nodes))

print(f"---")
print(f"Готово! В файле ultra_sub.txt теперь {len(final_nodes)} прокси.")
