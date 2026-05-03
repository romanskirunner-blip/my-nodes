import os
import random
import base64
import re

# Источники, которые мы будем скачивать системно
urls = [
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/vless/base64",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity",
    "https://raw.githubusercontent.com/NiREAs/v2ray-collector/main/sub/vless",
    "https://raw.githubusercontent.com/LalatinaHub/Mineral/master/vless.txt",
    "https://raw.githubusercontent.com/BardiaFA/Free-V2ray-Config/main/Splitted-By-Protocol/VLESS.txt"
]

all_vless = []

print("Запуск системного сбора через CURL...")

for url in urls:
    try:
        # Используем системный curl, чтобы GitHub не понял, что это Python-скрипт
        print(f"Качаю: {url.split('/')[-1]}")
        content = os.popen(f'curl -L -s --max-time 15 "{url}"').read().strip()
        
        if not content:
            continue

        # Если данные в Base64 (нет явного vless://), пробуем декодировать
        if "vless://" not in content[:100]:
            try:
                # Добавляем запасные == для корректного декода
                content = base64.b64decode(content + "===").decode('utf-8', errors='ignore')
            except:
                pass
        
        # Вытаскиваем все VLESS ссылки
        found = re.findall(r'vless://[^\s]+', content)
        
        # Фильтруем Farah и OneClick (набиваем лицо рекламе)
        clean = [link for link in found if not any(bad in link.lower() for bad in ["farah", "oneclick", "vpnkeys"])]
        
        all_vless.extend(clean)
        print(f"Успех! Найдено: {len(clean)}")
    except Exception as e:
        print(f"Ошибка на источнике: {e}")

# Чистим дубликаты
unique_nodes = list(set(all_vless))
random.shuffle(unique_nodes)
final_nodes = unique_nodes[:300]

# Записываем результат
with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_nodes))

print(f"\n--- ИТОГ: В файле {len(final_nodes)} серверов ---")
