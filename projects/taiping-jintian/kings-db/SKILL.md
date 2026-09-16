---
name: tianwang-lookup
description: 输入太平天国一位天王/诸王的名字（洪秀全、杨秀清、萧朝贵、冯云山、韦昌辉、石达开），从 taiping-kings.db 查出称号、生卒、功绩、画像与出处。Use when the user asks about a Taiping Heavenly Kingdom king by name.
---

# 天国掌故 Tianwang-Lookup

## 这个文件所在目录里有什么

- `taiping-kings.db` —— SQLite，表 `kings`，6 行：天王洪秀全、东王杨秀清、西王萧朝贵、
  南王冯云山、北王韦昌辉、翼王石达开。
  列：`id, title, name, honorific, full_title, birth, death, death_place,
  achievement, source, portrait_url, portrait_note, note`。

（`kings-db/` 副本里另有 `records.json` 与 `build_db.py`，用 `python3 build_db.py` 重建库。）

## 怎么查

用 Python 标准库 `sqlite3` 读库，自己写小脚本（机器上没有 python3 就先装）。
不要装任何查询工具，不要凭记忆回答。

## 规矩

1. 输入是一个名字（如「石达开」「杨秀清」「洪秀全」），用 `name` 匹配查出该行。
   匹配不到就模糊搜一次，仍没有就走第 5 条。
2. 按固定格式作答：
   - **王号 · 姓名**（如「翼王 · 石达开」）
   - 封号全称（含「五千岁」这类称号）
   - 生年 / 卒年（含卒地）
   - 主要功绩
   - 画像：`portrait_url` + `portrait_note`
   - 出处：`source`
   - 备注：`note`
3. 每条事实带该行的 `[id]`。
4. 生卒有存疑处（萧朝贵 1820/1826、冯云山 1815/1822、韦昌辉 1823/1826）照实转述，
   原文怎么写就怎么答，不替史料选一个。
5. 画像一律照抄 `portrait_note`，标注「现代塑像 / 非当时真容」；不许把画像说成真容。
6. 库里没有的名字（如「李秀成」「洪仁玕」「秦日纲」）就说「库里没有这个人」，
   不用常识补；若一定要补，必须声明「这不是库里的内容」。
7. 用用户提问的语言回答（中文问中文答）。
