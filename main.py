import urllib.request
import base64
import os

SOURCES = [
    "https://raw.githubusercontent.com/barry-far/V2Ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/yebekhe/TVip/main/Sub/Sub.txt"
]

def fetch_configs():
    unique_configs = set()
    headers = {'User-Agent': 'Mozilla/5.0'}
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read().decode('utf-8')
                try:
                    if not content.startswith(('vless://', 'ss://', 'trojan://')):
                        content = base64.b64decode(content).decode('utf-8')
                except:
                    pass
                for line in content.splitlines():
                    if line.strip().startswith(('vless://', 'ss://', 'trojan://')):
                        unique_configs.add(line.strip())
        except:
            continue
    return list(unique_configs)

def main():
    configs = fetch_configs()
    if not configs:
        return
    top_configs = configs[:150]
    final_text = "\n".join(top_configs)
    base64_configs = base64.b64encode(final_text.encode('utf-8')).decode('utf-8')
    file_path = "configs/list.txt"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(base64_configs)

if __name__ == "__main__":
    main()
