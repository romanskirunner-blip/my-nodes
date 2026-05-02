import urllib.request, base64, os

def main():
    urls = [
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless",
        "https://raw.githubusercontent.com/Paimon-v2ray/Paimon-VLESS-Reality/main/v2ray.txt",
        "https://raw.githubusercontent.com/RealSreN/Free-V2ray-Config/main/Splited/vless.txt"
    ]
    # Тестовая метка, чтобы мы поняли, что файл новый
    nodes = ["vless://test@1.1.1.1:443?encryption=none&security=reality#!!!_NEW_VLESS_VERSION_!!!"]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    for u in urls:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r:
                d = r.read().decode('utf-8')
                if "://" not in d:
                    try: d = base64.b64decode(d).decode('utf-8')
                    except: pass
                for line in d.splitlines():
                    line = line.strip()
                    if line.startswith('vless://') and 'trojan' not in line.lower():
                        nodes.append(line)
        except: continue
    
    if len(nodes) > 1:
        nodes = list(dict.fromkeys(nodes))
        res = base64.b64encode("\n".join(nodes[:100]).encode()).decode()
        os.makedirs("configs", exist_ok=True)
        with open("configs/list.txt", "w") as f: f.write(res)

if __name__ == "__main__": main()
