import urllib.request, base64, os

def main():
    # Новые источники, где 90% конфигов — это качественный VLESS
    urls = [
        "https://raw.githubusercontent.com/mansorid/free-v2ray-config/main/sub.txt",
        "https://raw.githubusercontent.com/Paimon-v2ray/Paimon-VLESS-Reality/main/v2ray.txt",
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless",
        "https://raw.githubusercontent.com/SreN-9/Free-V2ray-Config/main/Splited/vless.txt"
    ]
    
    nodes = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for u in urls:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=12) as r:
                d = r.read().decode('utf-8')
                # Если подписка зашифрована, декодируем
                if "://" not in d:
                    try: d = base64.b64decode(d).decode('utf-8')
                    except: pass
                
                for line in d.splitlines():
                    line = line.strip()
                    # СТРОГИЙ ФИЛЬТР: только VLESS
                    if line.startswith('vless://'):
                        nodes.append(line)
        except: continue
    
    if nodes:
        # Убираем дубликаты
        nodes = list(dict.fromkeys(nodes))
        
        # Сортировка по Европе (Германия, Нидерланды, Польша)
        eu_nodes = []
        other_nodes = []
        
        # Ключевые слова для поиска Европы в названиях
        eu_keywords = ['germany', 'de', 'netherlands', 'nl', 'poland', 'pl', 'frankfurt', 'amsterdam', 'warsaw']
        
        for n in nodes:
            n_lower = n.lower()
            if any(key in n_lower for key in eu_keywords):
                eu_nodes.append(n)
            else:
                other_nodes.append(n)
        
        # Сначала Европа, потом всё остальное, лимит 150
        final_list = (eu_nodes + other_nodes)[:150]
        
        res = base64.b64encode("\n".join(final_list).encode()).decode()
        os.makedirs("configs", exist_ok=True)
        with open("configs/list.txt", "w") as f: f.write(res)

if __name__ == "__main__": main()
