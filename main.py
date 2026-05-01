import urllib.request
import base64
import os

# Список проверенных источников с качественными конфигами (GitHub Raw ссылки)
SOURCES = [
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/E01.txt",
    "https://raw.githubusercontent.com/yebekhe/TVip/main/Sub/Sub.txt",
    "https://raw.githubusercontent.com/Lidatong/v2ray_pool/main/all.txt"
]

def fetch_configs():
    unique_configs = set()
    
    for url in SOURCES:
        try:
            with urllib.request.urlopen(url) as response:
                content = response.read().decode('utf-8')
                # Разбиваем на строки и убираем пустые
                for line in content.splitlines():
                    if line.strip().startswith(('vless://', 'ss://', 'trojan://')):
                        # Отбираем только современные протоколы
                        unique_configs.add(line.strip())
        except Exception as e:
            print(f"Ошибка при загрузке {url}: {e}")
            
    return list(unique_configs)

def main():
    configs = fetch_configs()
    # Берем топ-150 самых свежих (или первых из списка)
    top_configs = configs[:150]
    
    # Объединяем в одну строку
    final_text = "\n".join(top_configs)
    
    # Кодируем в Base64
    base64_configs = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')
    
    # Путь к твоему файлу (согласно твоей структуре)
    file_path = "configs/list.txt"
    
    # Проверяем, существует ли папка, если нет — создаем
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w") as f:
        f.write(base64_configs)
    
    print(f"Обновлено! Собрано {len(top_configs)} конфигов.")

if __name__ == "__main__":
    main()
