# ✈ 禁航分析 V2 · 网页版

NOTAM × CFP × 起飞窗口 · 签派放行工具。

## 功能

- 一次粘贴多条 NOTAM（自动按编号切块，每块用各自 B/C 时间计算）
- 一次粘贴多个 CFP（按 PLAN 自动切分）
- 自动时区识别（A 系列 UTC+8，C/D 系列北京时间）
- 命中 ≥ 2 个航路点判定受影响
- 输出每段窗口、合并窗口、甘特图、可复制的【禁航通告评估】文本
- 算法严格按 Excel 原型口径（不可改）

## 本地运行

```bash
streamlit run app.py
```

## 一键部署（Streamlit Cloud · 免费 · 国内可访问）

1. 把本目录 push 到 GitHub
2. 打开 https://share.streamlit.io/  → 用 GitHub 账号登录
3. New app → 选本仓库 → Main file path 填 `app.py` → Deploy
4. 拿到 `https://xxx.streamlit.app` 的链接，发给同事即可

## 同步流程

修改 `禁航分析V2.html` → `git push` → Streamlit Cloud 自动重建（~1 分钟）。本机不用一直开。

## 作者

王迪
