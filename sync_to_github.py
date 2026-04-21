#!/usr/bin/env python3
"""
同步本目录到 GitHub: 593682963wd-wq/nofly-analysis-web

用法:
    python3 sync_to_github.py

环境前提:
    Mac 钥匙串里已存有 github.com 的 PAT (与 obstacle-web 同一个账号)。
    不需要 git push 能跑通 — 走 GitHub Contents API,
    国内网络 git push 22/443 偶尔抽风时也能稳定上传。
"""
import os, base64, json, subprocess, urllib.request, urllib.error, urllib.parse, sys

REPO   = "593682963wd-wq/nofly-analysis-web"
BRANCH = "main"
ROOT   = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS  = {".git", "__pycache__", ".venv", "venv", "node_modules"}
SKIP_FILES = {".DS_Store"}

def get_token() -> str:
    out = subprocess.run(
        ["git", "credential", "fill"],
        input="protocol=https\nhost=github.com\n\n",
        capture_output=True, text=True, check=True,
    ).stdout
    for line in out.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1]
    sys.exit("找不到 github.com 的 PAT (Mac 钥匙串)")

TOKEN = get_token()

def api(method: str, path: str, body=None):
    req = urllib.request.Request(
        f"https://api.github.com/{path}",
        method=method,
        headers={
            "Authorization": f"token {TOKEN}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "nofly-uploader",
        },
        data=json.dumps(body).encode() if body else None,
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")

def upload(rel_path: str, abs_path: str) -> bool:
    with open(abs_path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode()
    enc = urllib.parse.quote(rel_path)
    code, data = api("GET", f"repos/{REPO}/contents/{enc}?ref={BRANCH}")
    body = {
        "message": f"sync: {rel_path}",
        "content": content_b64,
        "branch": BRANCH,
    }
    if code == 200 and isinstance(data, dict) and "sha" in data:
        if data.get("content", "").replace("\n", "") == content_b64:
            print(f"  ==  {rel_path} (无变化)")
            return True
        body["sha"] = data["sha"]
    code, data = api("PUT", f"repos/{REPO}/contents/{enc}", body)
    print(f"  {code}  {rel_path}")
    if code >= 400:
        print(f"      ERR: {data}")
        return False
    return True

def main():
    ok = fail = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn in SKIP_FILES or fn.endswith(".pyc"):
                continue
            abs_p = os.path.join(dirpath, fn)
            rel_p = os.path.relpath(abs_p, ROOT)
            if upload(rel_p, abs_p):
                ok += 1
            else:
                fail += 1
    print(f"\n完成: 成功 {ok}, 失败 {fail}")
    print("→ Streamlit Cloud 会在 ~1 分钟内自动重新部署。")

if __name__ == "__main__":
    main()
