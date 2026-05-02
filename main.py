import urllib.request, base64, os

def main():
    # Проверенные источники с VLESS/Reality
    urls = [
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless",
        "https://raw.githubusercontent.com/Paimon-v2ray/Paimon-VLESS-Reality/main/v2ray.txt",
        "https://raw.githubusercontent.com/RealSreN/Free-V2ray-Config/main/Splited/vless.txt"
    ]
    
    # Метка для проверки обновления
    nodes = ["vless://update-check@1.1.1.1:443?encryption=none&security=reality#UPDATED_NOW"]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for u in urls:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r:
                data = r.read().decode('utf-8')
                if "://" not in data:
                    try: data = base64.b64decode(data).decode('utf-8')
                    except: pass
                
                for line in data.splitlines():
                    line = line.strip()
                    # Жесткий фильтр: ТОЛЬКО vless и никакой грязи
                    if line.startswith('vless://') and 'trojan' not in line.lower() and 'vmess' not in line.lower():
                        nodes.append(line)
        except:
            continue
    
    if len(nodes) > 1:
        # Убираем дубликаты и берем первые 100
        unique_nodes = list(dict.fromkeys(nodes))
        result_str = "\n".join(unique_nodes[:100])
        
        # Кодируем в Base64
        encoded = base64.b64encode(result_str.encode()).decode()
        
        # Принудительная запись
        os.makedirs("configs", exist_ok=True)
        with open("configs/list.txt", "w", encoding="utf-8") as f:
            f.write(encoded)
        print(f"Success! Collected {len(unique_nodes)} nodes.")

if __name__ == "__main__":
    main()
