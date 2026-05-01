
    import urllib.request
import base64
import os

# Еще более мощные и стабильные источники
SOURCES = [
    "https://raw.githubusercontent.com/barry-far/V2Ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/yebekhe/TVip/main/Sub/Sub.txt"
]

def fetch_configs():
    unique_configs = set()
    headers = {'User-Agent': 'Mozilla/5.0'} # Добавили заголовок, чтобы сайты не блокировали бота
    
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8')
                
                # Если контент уже в base64 (часто бывает в подписках), декодируем его
                try:
                    if not content.startswith(('vless://', 'ss://', 'trojan://')):
                        content = base64.b64decode(content).decode('utf-8')
                except:
                    pass

                for line in content.splitlines():
                    if line.strip().startswith(('vless://', 'ss://', 'trojan://')):
                        unique_configs.add(line.strip())
        except Exception as e:
            print(f"Ошибка с {url}: {e}")
            
    return list(unique_configs)

def main():
    configs = fetch_configs()
    # Если нашли сервера — берем 150, если нет — пишем ошибку
    if not configs:
        print("Сервера не найдены!")
        return

    top_configs = configs[:150]
    final_text = "\n".join(top_configs)
    base64_configs = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')
    
    file_path = "configs/list.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w") as f:
        f.write(base64_configs)
    
    print(f"Успех! Собрано {len(top_configs)} конфигов.")

if __name__ == "__main__":
    main()

    # Путь к твоему файлу (согласно твоей структуре)
    file_path = "configs/list.txt"
    
    # Проверяем, существует ли папка, если нет — создаем
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with open(file_path, "w") as f:
        f.write(base64_configs)
    
    print(f"Обновлено! Собрано {len(top_configs)} конфигов.")

if __name__ == "__main__":
    main()
