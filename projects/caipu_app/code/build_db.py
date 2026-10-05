"""Build artifacts/caipu.db from data/recipes.json.

Usage:
    python3 code/build_db.py

Only-add data: edit data/recipes.json, rerun this script. Existing rows are
replaced, the database is never edited by hand.
"""
import json
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
DATA_DIR = PROJECT / "data"
DB = PROJECT / "artifacts" / "caipu.db"

CATEGORY = {
    "番茄": "蔬菜", "土豆": "蔬菜", "青椒": "蔬菜", "茄子": "蔬菜", "胡萝卜": "蔬菜",
    "西兰花": "蔬菜", "韭菜": "蔬菜", "白菜": "蔬菜", "冬瓜": "蔬菜", "洋葱": "蔬菜",
    "菠菜": "蔬菜", "油菜": "蔬菜", "黄瓜": "蔬菜", "包菜": "蔬菜", "青菜": "蔬菜",
    "蒜苔": "蔬菜", "四季豆": "蔬菜", "生菜": "蔬菜", "蒜苗": "蔬菜", "莲藕": "蔬菜",
    "玉米": "蔬菜", "白萝卜": "蔬菜", "山药": "蔬菜", "豆芽": "蔬菜", "花菜": "蔬菜",
    "娃娃菜": "蔬菜", "荷兰豆": "蔬菜", "芹菜": "蔬菜", "香菜": "蔬菜",
    "鸡蛋": "肉蛋", "猪肉": "肉蛋", "鸡肉": "肉蛋", "牛肉": "肉蛋", "排骨": "肉蛋",
    "猪肉末": "肉蛋", "鸭肉": "肉蛋", "鱼": "肉蛋", "带鱼": "肉蛋", "虾": "肉蛋",
    "蛤蜊": "肉蛋", "皮蛋": "肉蛋", "腊肉": "肉蛋",
    "豆腐": "豆制品", "豆腐皮": "豆制品", "香干": "豆制品",
    "香菇": "菌类", "木耳": "菌类", "杏鲍菇": "菌类",
    "蒜": "调味", "姜": "调味", "葱": "调味", "生抽": "调味", "老抽": "调味",
    "醋": "调味", "盐": "调味", "糖": "调味", "冰糖": "调味", "淀粉": "调味",
    "豆瓣酱": "调味", "花椒": "调味", "干辣椒": "调味", "蚝油": "调味",
    "香油": "调味", "番茄酱": "调味", "甜面酱": "调味", "泡椒": "调味",
    "剁椒": "调味", "辣椒油": "调味", "米酒": "调味", "白胡椒粉": "调味", "豆豉": "调味",
    "米饭": "主食", "粉条": "主食", "蒸肉米粉": "主食", "面粉": "主食", "面条": "主食",
    "花生": "其他", "温水": "其他", "紫菜": "其他", "可乐": "其他", "梅干菜": "其他",
    "酸菜": "其他", "海带": "其他", "枸杞": "其他", "啤酒": "其他", "酸豆角": "其他",
}

SCHEMA = """
CREATE TABLE ingredients (
    ingredient_id INTEGER PRIMARY KEY,
    name_zh       TEXT NOT NULL UNIQUE,
    aliases       TEXT NOT NULL DEFAULT '',
    category      TEXT NOT NULL DEFAULT '其他',
    note          TEXT NOT NULL DEFAULT ''
);
CREATE TABLE recipes (
    recipe_id  INTEGER PRIMARY KEY,
    name_zh    TEXT NOT NULL UNIQUE,
    cuisine    TEXT NOT NULL DEFAULT '家常',
    difficulty TEXT NOT NULL CHECK (difficulty IN ('简单', '中等', '稍难')),
    minutes    INTEGER NOT NULL CHECK (minutes > 0),
    summary    TEXT NOT NULL DEFAULT '',
    source     TEXT NOT NULL DEFAULT '家常菜谱库',
    note       TEXT NOT NULL DEFAULT ''
);
CREATE TABLE recipe_ingredients (
    recipe_id     INTEGER NOT NULL REFERENCES recipes(recipe_id),
    ingredient_id INTEGER NOT NULL REFERENCES ingredients(ingredient_id),
    amount        TEXT NOT NULL DEFAULT '',
    essential     INTEGER NOT NULL DEFAULT 0 CHECK (essential IN (0, 1)),
    PRIMARY KEY (recipe_id, ingredient_id)
);
CREATE TABLE recipe_steps (
    recipe_id INTEGER NOT NULL REFERENCES recipes(recipe_id),
    step_no   INTEGER NOT NULL,
    text      TEXT NOT NULL,
    PRIMARY KEY (recipe_id, step_no)
);
CREATE INDEX idx_ri_ingredient ON recipe_ingredients(ingredient_id);
"""


def canonical(name, aliases):
    for canon, alist in aliases.items():
        if name == canon or name in alist:
            return canon
    return name


def load():
    aliases = {}
    recipes = []
    for path in sorted(DATA_DIR.glob("recipes*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        for canon, alist in raw.get("ingredient_aliases", {}).items():
            merged = aliases.setdefault(canon, [])
            for alias in alist:
                if alias not in merged:
                    merged.append(alias)
        recipes.extend(raw["recipes"])

    names = [r["name"] for r in recipes]
    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes:
        raise SystemExit("菜谱重名: " + "、".join(dupes))

    ingredients = {}
    for r in recipes:
        for item in r["ingredients"]:
            canon = canonical(item["name"], aliases)
            ingredients.setdefault(canon, item["name"])

    rows = []
    for recipe in recipes:
        seen = set()
        ings = []
        for item in recipe["ingredients"]:
            canon = canonical(item["name"], aliases)
            if canon in seen:
                continue
            seen.add(canon)
            ings.append((canon, item["amount"], 1 if item.get("essential") else 0))
        rows.append(
            {
                "name": recipe["name"],
                "cuisine": recipe.get("cuisine", "家常"),
                "difficulty": recipe["difficulty"],
                "minutes": recipe["minutes"],
                "summary": recipe.get("summary", ""),
                "ingredients": ings,
                "steps": recipe["steps"],
            }
        )
    return ingredients, aliases, rows


def validate(rows):
    problems = []
    for r in rows:
        if not any(e for _, _, e in r["ingredients"]):
            problems.append(f"{r['name']}: 没有主料(essential)")
        if len(r["steps"]) < 2:
            problems.append(f"{r['name']}: 步骤少于 2 条")
        if any(not s.strip() for s in r["steps"]):
            problems.append(f"{r['name']}: 有空步骤")
        if r["difficulty"] not in ("简单", "中等", "稍难"):
            problems.append(f"{r['name']}: 难度非法 {r['difficulty']!r}")
    return problems


def build():
    ingredients, aliases, rows = load()
    problems = validate(rows)
    if problems:
        raise SystemExit("数据校验失败:\n  - " + "\n  - ".join(problems))

    DB.parent.mkdir(parents=True, exist_ok=True)
    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    con.executescript(SCHEMA)

    ing_id = {}
    for canon in sorted(ingredients):
        cur = con.execute(
            "INSERT INTO ingredients(name_zh, aliases, category) VALUES (?, ?, ?)",
            (canon, ",".join(aliases.get(canon, [])), CATEGORY.get(canon, "其他")),
        )
        ing_id[canon] = cur.lastrowid

    for r in rows:
        cur = con.execute(
            "INSERT INTO recipes(name_zh, cuisine, difficulty, minutes, summary) VALUES (?, ?, ?, ?, ?)",
            (r["name"], r["cuisine"], r["difficulty"], r["minutes"], r["summary"]),
        )
        rid = cur.lastrowid
        for canon, amount, essential in r["ingredients"]:
            con.execute(
                "INSERT INTO recipe_ingredients(recipe_id, ingredient_id, amount, essential) VALUES (?, ?, ?, ?)",
                (rid, ing_id[canon], amount, essential),
            )
        for i, text in enumerate(r["steps"], 1):
            con.execute(
                "INSERT INTO recipe_steps(recipe_id, step_no, text) VALUES (?, ?, ?)",
                (rid, i, text),
            )

    con.commit()
    fk = con.execute("PRAGMA foreign_key_check").fetchall()
    if fk:
        raise SystemExit(f"外键校验失败: {fk}")
    con.close()

    print(f"OK  recipes={len(rows)}  ingredients={len(ingredients)}  ->  {DB.relative_to(PROJECT)}")


if __name__ == "__main__":
    build()
