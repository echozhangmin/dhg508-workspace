# Research Journal

- [Design Document](../design/design_doc.md)

## 2026-10-30

- 用 OpenAlex works API 为《北宋赶考记》检索北宋科举文献：12 组查询，6 组有效、4 组高度有效、4 组无效（详见 `research/references/search_log.md`）。
- 建立工作书目 `research/references/bibliography.md`：20 条正式候选（嘉祐二年人物／省试殿试制度／报名资格周期／总论与文学社会），另有 7 条备选；全部标「未读待核」。
- 关键命中：Rong 2019（《Diogenes》，正面写 1057 欧阳修-梅尧臣-苏轼）、王瑞来 1986 与龚延明 2005（殿试）、祝尚书 2005（试卷）、荒木敏一 1964（糊名）。
- 覆盖缺口：赴京行程/驿路、宋行卷——OpenAlex 弱，待本人在 Google Scholar 手查（检索式已列入 search_log.md）。
- 下一步：优先读 Rong 2019 → 王瑞来 1986 + 龚延明 2005 → 祝尚书 2005；读后要点与页码记入 `research/notes/`，再回填游戏设定核查结论。
- 打开核验：Rong 2019 为 Cairn 开放获取全文（Subscribe To Open）；祝尚书 2005 的 CNKI 英文页有效（下载需订阅）；王瑞来 1986、龚延明 2005、许结 2003 的维普旧深链已失效，改走题名检索（qikan.cqvip.com／百度学术）；荒木敏一 1964 经京都学艺大学 OPAC 核实（纪要·文科第 25 辑）；Hawes 2009 仅拦机器人，浏览器可开。书目「访问」栏已同步更新。

## 2026-10-31

- 完成 Week 8（历史模拟）作业 presentation：
  - `assignments/week-08/answer.md`——覆盖 Bring-to-class 清单（情境、why-not-a-film、
    人物 scripted 理由、证据分级表 18 行、工具/AI/人工分工、真实困难及例子、链接）。
  - `research/outputs/presentation.html`——单文件 HTML 幻灯片 12 页（方向键翻页，
    带 print 样式可导出 PDF）+ `presentation_script.md` 讲稿（约 5 分钟）。
  - `questions.md`——未解问题清单（驿程、门税出处、苏洵出处、嘉祐行卷形态、
    五甲表述、agentic 人物、平衡调参、开发提示词索引）。
- 证据分级依据：游戏词条表 54 条（两档出处）+ OpenAlex 书目 20 条（摘要级/题名级）。
- 确认 GitHub Pages 在线可玩（https://echozhangmin.github.io/songgame/）。

## 2026-11-02

- 游戏接入**分场景插图机制**（本地仓库 `~/Documents/deepseek-harness/default-workspace/song-exam`）：
  - `game.template.html`：舞台横幅背景第二层改 `var(--scene-art, 共用底图)`；
    `render()` 按当前场景 id 注入 `--scene-art` 内联变量；新增 `SCENE_ART = __SCENE_ART__`。
  - `build.py`：按文件名约定扫描 `assets/scene_<场景id>.jpg` 内嵌成 JS 表；
    顺手修复既有 bug——`__SCROLL_IMG__` 只替换第一个出现处，开始页画轴图是坏的。
  - 第二幕「长亭 · 饯别」已配图：`scene_changting.jpg`（原图 2848×1600 PNG 6.3MB
    → 1600×899 JPEG 488KB）。构建后单文件 2068 KB，占位符零残留。
  - 第三幕「官道 · 驿站」已配图：`scene_yizhan.jpg`（原图 2048×1152 PNG 3.7MB
    → 1600×900 JPEG 495KB）；用户口述"第四幕驿站"，实际驿站为第三幕（第 4–6 日），
    已按场景名配图并当面说明。单文件 2728 KB。
  - 第四幕「山路 · 风雨」已配图：`scene_shandao.jpg`（原图 PNG 4.2MB → 1600×900
    JPEG 555KB）。单文件 3469 KB（每张约 +650KB，若 11 个场景全配将达 ~9MB，
    届时考虑降质量或 1400px）。
  - 第五幕「汴河 · 舟中」已配图：`scene_bianhe.jpg`（原图 PNG 3.8MB → 1600×900
    JPEG 440KB），覆盖第 10–11 日与 13–14 日两段舟行；虹桥闸口（第 12 日）为
    独立场景另配。单文件 4055 KB。
  - 第五幕「虹桥 · 汴河闸口」已配图：`scene_hongqiao.jpg`（原图 PNG 6.2MB →
    1600×899 JPEG 488KB，用户指定 (7) 号图）。至此第五幕三个场景条目齐了。
    单文件 4706 KB；剩 jiaxu／chengmen／jiulou／shuku／gongyuan／fangbang 六位。
  - 第六幕「汴京 · 城门」已配图：`scene_chengmen.jpg`（原图 PNG 5.6MB → 1600×899
    JPEG 419KB）。单文件 5265 KB；剩 jiaxu／jiulou／shuku／gongyuan／fangbang 五位。
  - 第七幕「御街 · 酒楼」已配图：`scene_jiulou.jpg`（1600×899 JPEG 488KB）。
    **用户确认 (7) 号与虹桥闸口共用**（两幕同图）；同一图片在单文件里 base64
    内嵌了两份（hongqiao＋jiulou 各 488KB），若在意体积，将来可让 build 按
    内容哈希去重。单文件 5915 KB；剩 jiaxu／shuku／gongyuan／fangbang 四位。
  - **换图**：虹桥闸口 (7) → (4) 号（用户确认换闸口、酒楼不动）：`scene_hongqiao.jpg`
    重压为 1600×899 JPEG 537KB；两幕同图的重复内嵌随之消失。单文件 5981 KB。
    已配：长亭(11)／驿站(12)／山道(13)／舟中(14)／闸口(4)／城门(15)／酒楼(7)；
    剩 jiaxu／shuku／gongyuan／fangbang 四位。
  - 第八幕「国子监 · 书库」已配图：`scene_shuku.jpg`（原图 PNG 5.8MB → 1600×899
    JPEG 438KB，(16) 号）。单文件 6564 KB；剩 jiaxu／gongyuan／fangbang 三位。
  - 第九幕「贡院 · 号舍」已配图：`scene_gongyuan.jpg`（原图 PNG 5.9MB → 1600×899
    JPEG 465KB，(8) 号）。单文件 7185 KB；剩 jiaxu／fangbang 两位。
  - 第十幕「琼林苑 · 放榜」已配图：`scene_fangbang.jpg`（原图 PNG 3.6MB → 1600×900
    JPEG 397KB，(17) 号）。单文件 7714 KB；仅剩 jiaxu（家塾，第 1–2 日）一位。
- **发现既有回归（先于本次改动，git stash 隔离验证 HEAD 基线同样失败）**：
  sim.js 无头 180 局中 175 局在第 15 日「病卧逆旅」。诊断与修法记入
  `questions.md` 游戏待办第一条。presentation/README 引用的旧基线数字需加标注。
- 未提交：仓库有 post-commit 自动推送钩子，等用户验收后自行 commit。
- **修复 sim.js 无头测试回归（只动测试工具，游戏本体零改动）**：① `chooseAction`
  加 `lodge`（寻住处）优先级与"无回精力手段时停做耗精力事"护栏；② 行动表过滤
  `hideIf`（一次性动作不可重复）；③ 主循环经 `chooseEvent` 按 cost/gain 评分结算
  全部二选一事件（门税／桥头／山匪／书肆／山寺／醉客／贵人——此前 sim 一律跳过，
  事件开销形同虚设）；④ `__G` 导出 `chooseEvent`。修复后 balanced 180 局**零病倒**
  （原 175 死于第 15 日）：55% 档同进士 17／特奏名 12，70% 档二甲 26／一甲 15，
  85% 档一甲 31／状元 15；仅 5 局困于逆旅（第 24–28 日盘缠见底——事件开销现在
  真实扣费，期末盘缠收紧到个位数）。neglectYuan／neglectJing 验证模式照常
  180/180 触发。新基线已写入 game repo README §六，answer.md 数字已同步。

## 2026-11-04

- 应用户问"游戏符合北宋省考逻辑吗"，核验《宋史·选举志一》（卷155）原文
  （记于 `research/notes/songshi_xuanju_zhi_2026-11-04.md`）：
  - **合**：秋取解→冬集礼部→春考试的时间骨架；诗赋居首的三场制；糊名誊录下
    "一切考诸试篇"（打听偏好只得传闻暗合）；殿试三题（御试祖宗法）；殿试定
    等第；省试黜落。
  - **相抵**：①第二场"经义"是熙宁后之制，嘉祐二年应为**论**（待拍板一行改）；
    ②特奏名须"积举数与年岁"，首举青年落第不该得（待拍板文案改）。
  - **顺带**：公卷在封弥誊录后已罢（贾昌朝议），词条「行卷」备注待升级；
    考运加成补标 invented。questions.md 已更新。
- 三处制度校正已实施并推送（commit fb5e3de）：第二场"经义"→"论"；三处
  "主司好经义"传闻文案改"好古文、厌险怪"（合嘉祐二年欧阳修黜太学体事）；
  特奏名结局加史实自注＋词条注；词条「经义／策论／行卷／投行卷／特奏名」
  升级（策论升原文级，行卷补"公卷已罢"）。answer.md 与幻灯片证据表同步，
  questions.md 四项勾销。
- presentation 增页：S8「一次校证：从疑问到原文到修复」（三疑点/两利好/当日
  推送），S6 补临川=王安石同乡，S7 inferred 行补漕路路线与"三千里"量级；
  讲稿同步插入 S8 并重编号至 S13、加答辩备忘（为什么第二场是"论"）。
  幻灯片现为 13 页。
- **presentation 精简为 9 页**（用户要求更简短）：玩法表并入"为什么不是电影"的
  论证、检索并入工具页、其他困难并入结尾页；每页文字收紧，讲稿同步改写为
  9 段约 4 分钟；答辩备忘保留。
- presentation 增页 S5「为什么是这一年：1057 留下的纸」：四层理由各配一条证据
  （归田录锁院／Rong 2019 唱和与谢启／刑赏忠厚之至论＋误置第二待核／同榜名单／
  制度诸条原文级），沿用分级标注；幻灯片 10 页约 4.5 分钟；"误置第二"掌故与
  谢启篇目原文记入 questions.md 待核。
- presentation 增页 S2「实机画面」：用户桌面 13 张截屏经编号拼图挑选（Blender
  未开、模型无图像输入，改由用户看拼图拍板），只用 11-04 大图——3.6MB PNG
  压为 1600×1085 JPEG 307KB，存 `outputs/screenshot_game.jpg`，PPT 相对路径引用
  （保持 HTML 小体积）。幻灯片 11 页约 5 分钟，讲稿同步（S3 插入、后续重编号）。
- **写 `research/design/design_doc.md`（机制完整规格，依代码逐项核录）**：总参数、
  日循环、十二幕表（含插图）、26 项行动全规格、事件四类全表（随机/固定/弹窗/
  路况）、题诗十八题材与判分、12 NPC 表、考试公式与六档、四失败线、存档、
  机制×证据要点、已知问题。**核录中发现两处死代码**：虹桥 acts 的 `ask`
  无定义（"打听消息"从未在虹桥显示，README 却有承诺）；`enter`（入城安顿）
  定义无引用。已列 design_doc §十二待拍板。
- **两处死代码已修并推送（commit 389c932）**：虹桥 `ask`→`info`（打听消息
  恢复显示）；删 `enter` 行动与 sim 死分支。构建校验通过（"入城安顿"清零、
  虹桥 acts 含 info）；sim 回归 180 局零病倒、分布与基线同形。design_doc §十二
  两条勾销。
- **题诗判定收紧为三重标准（用户拍板，已实施并验证）**：①切题——十八张题眼
  字表（THEME_WORDS），命中 ≥2 判切题（近似判断）；②四句齐整；③非抄——
  示范句库 FAMOUS_LINES，任一句相同即抄写。抄写/离题/不齐均中品无酬，评语
  分三句（口吻仍鼓励）。无头六用例全过；发现并修复题眼字表缺漏（勤学漏
  "书"、场屋补时妆眉烛）。边界案例如实记录：白话诗投勤学题（含"读书"题眼）
  按规则仍判上品。README §二/§六/§八、design_doc §六、questions.md 同步。
- **温书判定收紧（用户拍板：答错不加智力）**：`answer()` study 分支改
  `if (ok) addStat('zhi', 1)`（答错仍给解析、`maintained.zhi` 仍置位挡夜衰减，
  避免制造新死亡线）；hint/README §一/取舍 #3/design_doc §四同步。新基线
  （2026-11-04）：零死亡，55% 档同进士 20/二甲 19，85% 档一甲 28/状元 15；
  sim 磨书型策略期末智力仍满 10——对人类玩家（行动点有限、答错即白耗精力）
  才是真收紧，README 已注明。
- **题诗四重标准（用户两次拍板，已实施）**：字数对齐＋**非白话**（`BAIHUA_CHARS`
  10 字＋`BAIHUA_WORDS` 31 词＋句末"了的吗呢"类助词）＋**非默写**（示范诗
  `FAMOUS_LINES` ＋新增**名句库** `FAMOUS_EXTRA` 约 60 句常被默写的唐宋名句，
  标作者篇名）＋切题。凡例 §五与 poem/sell 按钮 hint 补齐为四条表述（上轮
  漏改处一并修复）。八例判定用例**入库** `poem_test.js`（repo 根目录，与
  sim.js 同款）全部通过：白话诗投勤学/山川均中品（白话"们"命中）——上一版
  的边界案例（白话诗投勤学仍上品）就此消除；默写《春晓》《登鹳雀楼》判中品。
  README §一/§二/§六/§八、design_doc §六、questions.md 同步；名句库如实
  声明为近似覆盖。
- **恢复三档（用户拍板）**：白话/默写判**下品**——分文不给＋当众出丑
  **人缘 −1**、评语转冷（"满座哄笑""围看的闲人笑出了声"）；离题/不齐仍
  中品（评语鼓励）。submitPoem 增 `if (g.grade === '下品') addStat('yuan', -1)`
  与下品行记；题笺、凡例 §五、poem/sell hint、README §一/§二/§六/§八、
  design_doc §四/§六全部同步。poem_test.js 八例期望更新后全过。注意事项：
  人缘 −1 计入夜结算死亡线——低人缘时出丑可能致"孤身无援"（主题上即
  "声名扫地"，已记 design_doc）。
