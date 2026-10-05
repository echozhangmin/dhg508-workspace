# 看图识菜谱 · caipu_app

Week 5 的「自己的 app」。拍一张食材照片，DeepSeek 视觉模型识别食材，
再对照本地**家常菜谱库**给出 5 个家常菜谱，每个都带详细步骤。

## 流程

```
浏览器网页  --照片-->  server.py
                         ├─ 1. DeepSeek 视觉模型：识别食材（JSON）
                         ├─ 2. 查本地 SQLite 菜谱库（artifacts/caipu.db）
                         ├─ 3. DeepSeek：依据「食材 + 库中候选菜谱」生成 5 个菜谱（每个 5–8 步详细步骤）
                         └─ 4. 返回网页：食材、菜谱、每条来自「库中菜谱」还是「模型补充」
```

demo 里的 `ask_model()` 是 fixture（固定答案）；这里换成了**真实的 DeepSeek 调用**，
并多了 demo 没有的一层：本地菜谱库。识别结果会先拿去查库，再交给模型组织菜谱。

## 目录

| 文件 | 作用 |
|---|---|
| `code/static/index.html` | 网页：拍照/拖拽上传，展示食材与菜谱（纯 HTML + JS） |
| `code/server.py` | 服务器：标准库 `http.server`，`POST /api/recipes` 走完上面 4 步 |
| `code/build_db.py` | 合并 `data/recipes*.json` 并重建 `artifacts/caipu.db`（查重、校验外键后写入） |
| `data/recipes.json` | 菜谱种子数据（30 道）+ 食材别名表 |
| `data/recipes_extra1.json` | 追加菜谱：荤菜、水产（35 道） |
| `data/recipes_extra2.json` | 追加菜谱：素菜、汤羹、面食（35 道） |
| `artifacts/caipu.db` | 生成的数据库（共 100 道菜谱），不进 Git，可重建 |

## 运行

```sh
python3 code/build_db.py                 # 建库（改过 data 就重跑）
cp .env.example .env                     # 填 DEEPSEEK_API_KEY，或直接 export
python3 code/server.py                   # 打开 http://localhost:8000
```

只依赖 Python 标准库，不用装任何包。要在手机上拍照，让服务器监听局域网：

```sh
HOST=0.0.0.0 PORT=8010 python3 code/server.py   # 手机访问 http://<电脑局域网IP>:8010
```

## 用到的 DeepSeek 文档

- 图像理解（vision，图片以 base64 data URL 传入 user 消息）：
  https://api-docs.deepseek.com/zh-cn/guides/vision
- 思考模式（本 app 关闭思考，出结果更快）：
  https://api-docs.deepseek.com/zh-cn/guides/thinking_mode
