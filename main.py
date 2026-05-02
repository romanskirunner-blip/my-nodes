import urllib.request, base64, os

def main():
    # Оставил только самые "жирные" источники с VLESS
    urls = [
        "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
        "https://raw.githubusercontent.com/barry-far/V2Ray-Configs/main/All_Configs_Sub.txt",
        "https://raw.githubusercontent.com/yebekhe/TVip/main/Sub/Sub.txt"
    ]
    
    nodes = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for u in urls:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as r:
                d = r.read().decode('utf-8')
                if "://" not in d:
                    try: d = base64.b64decode(d).decode('utf-8')
                    except: pass
                
                for line in d.splitlines():
                    line = line.strip()
                    # ФИЛЬТР: Убираем ss:// (Shadowsocks), оставляем только VLESS и Trojan
                    if line.startswith(('vless://', 'trojan://')):
                        nodes.append(line)
        except: continue
    
    if nodes:
        # 1. Убираем дубликаты
        nodes = list(dict.fromkeys(nodes))
        
        # 2. Сортировка: вытаскиваем Германию, Нидерланды и Польшу в начало списка
        fast_nodes = []
        other_nodes = []
        for n in nodes:
            n_lower = n.lower()
            if any(country in n_lower for country in ['germany', 'de', 'netherlands', 'nl', 'poland', 'pl']):
                fast_nodes.append(n)
            else:
                other_nodes.append(n)
        
        # Собираем финальный список: сначала быстрые страны, потом остальные до 150 штук
        final_list = (fast_nodes + other_nodes)[:150]
        
        res = base64.b64encode("\n".join(final_list).encode()).decode()
        os.makedirs("configs", exist_ok=True)
        with open("configs/list.txt", "w") as f: f.write(res)

if __name__ == "__main__": main()
