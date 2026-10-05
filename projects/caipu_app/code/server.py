"""看图识菜谱 — a page, a server, a real model, and a database.

    python3 code/server.py        then open http://localhost:8000

Flow of one photo:
    1. the page posts the photo to /api/recipes;
    2. the server asks DeepSeek's vision model what ingredients it sees;
    3. the server looks those ingredients up in the local recipe database
       (artifacts/caipu.db, built from data/recipes.json);
    4. the server asks DeepSeek to compose 3 recipes, grounding them in the
       database rows it found;
    5. the page shows the ingredients, the recipes, and where each came from.

Standard library only. The DeepSeek API key is read from the environment
(DEEPSEEK_API_KEY) or from a gitignored .env at the project root.
"""
import base64
import json
import os
import re
import sqlite3
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
DB = PROJECT / "artifacts" / "caipu.db"
STATIC = HERE / "static"
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-flash"
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", 8000))
MAX_IMAGE = 20 * 1024 * 1024
IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}


def load_env():
    env = PROJECT / ".env"
    if not env.is_file():
        return
    for line in env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def api_key():
    return os.environ.get("DEEPSEEK_API_KEY", "").strip()


load_env()


def call_deepseek(messages, temperature=None):
    if not api_key():
        raise RuntimeError("服务器缺少 DEEPSEEK_API_KEY，请设置环境变量或写入项目根目录的 .env")
    payload = {"model": MODEL, "messages": messages, "thinking": {"type": "disabled"}}
    if temperature is not None:
        payload["temperature"] = temperature
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key()}"},
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")
        try:
            detail = json.loads(detail).get("error", {}).get("message", detail)
        except ValueError:
            pass
        raise RuntimeError(f"DeepSeek API 错误 {error.code}: {detail[:200]}")
    return data["choices"][0]["message"]["content"]


def parse_json(text):
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    starts = [i for i in (text.find("{"), text.find("[")) if i >= 0]
    if not starts:
        raise ValueError("模型没有返回 JSON")
    start = min(starts)
    end = max(text.rfind("}"), text.rfind("]"))
    return json.loads(text[start : end + 1])


IDENTIFY_PROMPT = (
    "你是厨房助手。看这张照片，只列出画面里真实可见的食材，用常见中文名，"
    "不要猜测照片里没有的食物。只输出一个 JSON："
    '{"ingredients": ["番茄", "鸡蛋"]}。不要输出任何其他文字。'
    "如果分辨不出任何食材，返回 {\"ingredients\": []}。"
)


def identify(image, mime):
    data_url = f"data:{mime};base64,{base64.b64encode(image).decode()}"
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": data_url}},
                {"type": "text", "text": IDENTIFY_PROMPT},
            ],
        }
    ]
    result = parse_json(call_deepseek(messages))
    items = result.get("ingredients", []) if isinstance(result, dict) else result
    names = []
    for item in items:
        name = item.get("name") if isinstance(item, dict) else item
        name = str(name).strip()
        if name and name not in names:
            names.append(name)
    return names


def canonical_ids(con, names):
    found = {}
    for name in names:
        name = str(name).strip()
        if not name:
            continue
        row = con.execute(
            "SELECT ingredient_id, name_zh FROM ingredients WHERE name_zh = ?", (name,)
        ).fetchone()
        if row:
            found[row["ingredient_id"]] = row["name_zh"]
            continue
        for ing in con.execute("SELECT ingredient_id, name_zh, aliases FROM ingredients"):
            if name in [a for a in ing["aliases"].split(",") if a]:
                found[ing["ingredient_id"]] = ing["name_zh"]
                break
    return found


def recipe_dict(con, row):
    ingredients = con.execute(
        """SELECT i.name_zh, ri.amount FROM recipe_ingredients ri
           JOIN ingredients i ON i.ingredient_id = ri.ingredient_id
           WHERE ri.recipe_id = ? ORDER BY ri.essential DESC, i.name_zh""",
        (row["recipe_id"],),
    ).fetchall()
    steps = [
        s["text"]
        for s in con.execute(
            "SELECT text FROM recipe_steps WHERE recipe_id = ? ORDER BY step_no", (row["recipe_id"],)
        )
    ]
    return {
        "name": row["name_zh"],
        "cuisine": row["cuisine"],
        "difficulty": row["difficulty"],
        "minutes": row["minutes"],
        "summary": row["summary"],
        "source": "库中菜谱",
        "ingredients": [f"{i['name_zh']} {i['amount']}".strip() for i in ingredients],
        "steps": steps,
    }


def db_candidates(con, names):
    ids = canonical_ids(con, names)
    if not ids:
        return [], []
    marks = ",".join("?" * len(ids))
    rows = con.execute(
        f"""SELECT r.recipe_id, r.name_zh, r.cuisine, r.difficulty, r.minutes, r.summary,
                   SUM(ri.essential) AS ess, COUNT(*) AS hits
            FROM recipes r JOIN recipe_ingredients ri ON ri.recipe_id = r.recipe_id
            WHERE ri.ingredient_id IN ({marks})
            GROUP BY r.recipe_id
            ORDER BY ess DESC, hits DESC, r.minutes ASC LIMIT 10""",
        tuple(ids),
    ).fetchall()
    return [recipe_dict(con, row) for row in rows], list(ids.values())


COMPOSE_PROMPT = """你是家常菜厨师。用户手头确认能用的食材是：{ingredients}。

本地菜谱库里找到这些候选菜谱（JSON，可能为空）：
{candidates}

请给出 5 个家常菜谱：优先采用上面的候选菜谱，用用户现有的食材；若候选不够或食材不搭，可用常识补充，补充的 source 写"模型补充"。
每个菜谱的 steps 必须详细：5–8 步，每步写清材料用量、火候（大/中/小火）、时间、下锅顺序和调味时机，让人照着就能做。
只输出一个 JSON：
{{"recipes": [{{"name": "菜名", "summary": "一句话介绍", "difficulty": "简单|中等|稍难", "minutes": 25, "source": "库中菜谱|模型补充", "ingredients": ["番茄 2个", "鸡蛋 3个"], "steps": ["第一步，写清用量/火候/时间", "第二步"]}}]}}
必须正好 5 个菜谱，不要输出任何其他文字。"""


def compose(ingredients, candidates):
    compact = [
        {"name": c["name"], "ingredients": c["ingredients"], "steps": c["steps"]}
        for c in candidates
    ]
    prompt = COMPOSE_PROMPT.format(
        ingredients="、".join(ingredients) or "（未识别到）",
        candidates=json.dumps(compact, ensure_ascii=False),
    )
    result = parse_json(call_deepseek([{"role": "user", "content": prompt}], temperature=0.7))
    recipes = result.get("recipes", []) if isinstance(result, dict) else []
    return recipes[:5]


class Handler(BaseHTTPRequestHandler):
    def send(self, status, body, kind):
        self.send_response(status)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, status, obj):
        self.send(200 if status == 200 else status, json.dumps(obj, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self.send(200, (STATIC / "index.html").read_bytes(), "text/html; charset=utf-8")
        if self.path == "/api/health":
            count = 0
            if DB.is_file():
                con = sqlite3.connect(DB)
                count = con.execute("SELECT COUNT(*) FROM recipes").fetchone()[0]
                con.close()
            return self.send_json(200, {"model": MODEL, "recipes": count, "key": bool(api_key())})
        self.send(404, b"not found", "text/plain; charset=utf-8")

    def do_POST(self):
        if self.path != "/api/recipes":
            return self.send_json(404, {"error": "not found"})
        length = int(self.headers.get("Content-Length", 0))
        if length <= 0:
            return self.send_json(400, {"error": "没有收到图片"})
        if length > MAX_IMAGE:
            return self.send_json(413, {"error": "图片太大（超过 20MB），请换一张小一点的"})
        image = self.rfile.read(length)
        mime = (self.headers.get("Content-Type") or "image/jpeg").split(";")[0].strip()
        if mime not in IMAGE_TYPES:
            mime = "image/jpeg"
        if not api_key():
            return self.send_json(400, {"error": "服务器没有 DEEPSEEK_API_KEY，请设置后重启"})
        try:
            ingredients = identify(image, mime)
            if not ingredients:
                return self.send_json(200, {"model": MODEL, "ingredients": [], "matched": [],
                                            "db_matches": [], "recipes": [],
                                            "note": "没有识别到食材"})
            con = sqlite3.connect(DB)
            con.row_factory = sqlite3.Row
            candidates, matched = db_candidates(con, ingredients)
            con.close()
            recipes = compose(ingredients, candidates)
        except Exception as error:
            return self.send_json(500, {"error": str(error)})
        self.send_json(
            200,
            {
                "model": MODEL,
                "ingredients": ingredients,
                "matched": matched,
                "db_matches": [c["name"] for c in candidates],
                "recipes": recipes,
            },
        )

    def log_message(self, fmt, *args):
        print("  " + fmt % args)


if __name__ == "__main__":
    if not DB.is_file():
        raise SystemExit("找不到 artifacts/caipu.db，先运行: python3 code/build_db.py")
    shown = "localhost" if HOST in ("127.0.0.1", "0.0.0.0") else HOST
    print(f"看图识菜谱  ->  http://{shown}:{PORT}   (Ctrl+C 停止)")
    print(f"模型: {MODEL}   数据库: {DB.name}   key: {'已设置' if api_key() else '未设置'}")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
