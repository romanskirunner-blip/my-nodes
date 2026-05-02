import urllib.request
import random
import base64
import re
import time

# Источники, которые мы обсуждали
urls = [
    "https://raw.githubusercontent.com/ebrasha/v2ray-free/main/v2ray.txt",
    "https://raw.githubusercontent.com/vfarid/v2ray-share/main/all.txt",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/vless/base64"
]

def update_configs():
    all_nodes = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    print("Сбор нод...")
    
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('utf-8')
                
                # Если base64 — декодируем, если нет — берем как есть
                if "://" not in content:
                    try:
                        content = base64.b64decode(content).decode('utf-8')
                    except:
                        pass
                
                # Ищем все ссылки (vless, vmess, ss и т.д.)
                nodes = re.findall(r'(vless|vmess|ss|trojan)://[^\s]+', content)
                all_nodes.extend(nodes)
        except Exception as e:
            print(f"Ошибка при загрузке {url}: {e}")

    # Убираем дубликаты
    all_nodes = list(set(all_nodes))
    
    # Перемешиваем и берем ровно 300
    random.shuffle(all_nodes)
    final_list = all_nodes[:300]
    
    # Сохраняем в файл
    with open("results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_list))
    
    print(f"Готово! Сохранено {len(final_list)} конфигов в results.txt")

# Если планируешь запускать на сервере/телефоне вручную:
if __name__ == "__main__":
    while True:
        update_configs()
        print("Ожидание 1 час...")
        time.sleep(3600) # 3600 секунд = 1 час
