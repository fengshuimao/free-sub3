import requests
import base64
import re
from datetime import datetime

# 多个免费源
SOURCES = [
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    "https://raw.githubusercontent.com/aiboboxx/clashfree/main/v2"
]

def fetch_nodes():
    nodes = []
    for url in SOURCES:
        try:
            print(f"[INFO] Fetching {url}")
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                content = resp.text.strip()
                # 判断是否 base64 编码
                if re.match(r'^[A-Za-z0-9+/=]+={0,2}$', content.replace("\n", "")):
                    try:
                        decoded = base64.b64decode(content).decode("utf-8", errors="ignore")
                        nodes.extend(decoded.strip().split("\n"))
                    except:
                        pass
                else:
                    nodes.extend(content.split("\n"))
        except Exception as e:
            print(f"[ERROR] {url}: {e}")
    # 保留 vmess / vless / trojan
    clean_nodes = list(set(
        n.strip() for n in nodes if n.strip().startswith(("vmess://", "vless://", "trojan://"))
    ))
    return clean_nodes

def save_sub(nodes, filename="sub.txt"):
    content = "\n".join(nodes)
    encoded = base64.b64encode(content.encode()).decode()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(encoded)
    print(f"[INFO] Saved {len(nodes)} nodes to {filename}")

if __name__ == "__main__":
    print(f"[INFO] Updating at {datetime.now()}")
    nodes = fetch_nodes()
    save_sub(nodes)
