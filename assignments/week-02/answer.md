# Week 2 作业 · 太平天国运动第一次爆发的地方（和时间）

## 问题与答案

**问题（1950年以前）：** 太平天国运动最开始爆发的地方（和时间）在哪里？

**答案：** 金田起义 —— **1851年1月11日（清道光三十年十二月初十日），广西桂平县金田村**
（今广西贵港市桂平市金田镇）。洪秀全领导拜上帝会会众誓师起义，建号"太平天国"。

**注意区分**：拜上帝会1843年创立于广东花县（组织期）；1850年7月"团营"令后各地会众向金田村
集结（动员期）；1851年1月11日金田誓师建号才是**武装起义/爆发点**。

## 两处证据

**证据一（二手，无需OCR）— 中国国家博物馆"金田起义"词条**

> "1851年1月11日（道光三十年十二月十日），洪秀全和杨秀清、肖朝贵、冯云山、韦昌辉、石达开等人
> 率众约两万人在**广西桂平金田村**发动武装起义，建号太平天国。"

出处：chnmuseum.cn（故宫/国博一类的机构性来源；金田起义地址为第一批全国重点文物保护单位）。
另以 Britannica "Taiping Rebellion"（传教于广西农民 → 率众起事）互证。

**证据二（需OCR的第一手/当时文献）— Thomas Taylor Meadows, *The Chinese and Their Rebellions* (1856)**

- p.5（IA leaf n77）："*The province of **Kwangse** [广西]，in which the present religious movement
  took its rise …*" —— 运动起于广西。
- p.155（IA leaf n229）脚注，转引《京报》所刊奏折："*the Tae pings left their camp at **Kin teen**
  [金田] on the **4th March, 1851***" —— 当时官方文书把太平军驻扎金田并离开的日期定在1851年。
- 补充一手证据：《欽定剿平粵匪方略》卷首目錄（御制序作于同治十一年）记载
  **卷一至卷五 = 道光三十年五月庚戌 至 咸豐元年六月乙亥**，即官方记录把起事年份框在
  1850–1851（咸豐元年即1851）。

可靠性：Meadows 是在华英国领事译员、1856年成书，紧贴事件；国家博物馆是机构性权威叙述。
局限：Meadows 为英国视角，只到"省"级（Kwangse）；精确定点（桂平金田村）依靠博物馆+清官方编年。

## OCR 方法（按作业规定的顺序尝试）

1. **LLM API（OpenRouter / DeepSeek）**：没能运行 —— 按官方指南（`deepseek-flash`，
   base64 内嵌图）准备好脚本 `projects/taiping-jintian/ocr/llm_ocr.py` 并取得了 key，但官方端点
   判定该 key 无效（"Your api key: ****GRtE is invalid"），key 格式（67 位）也与官方 DeepSeek /
   OpenRouter key 不符，疑似第三方中转平台的 key；OpenRouter 在本网络下请求进不了认证环节
   （假 key 也返回同样 401）。key 只存在被 git 忽略的环境文件里，不入库。
2. **PaddleOCR**：装不上 —— `paddlepaddle` 在 Python 3.14 没有wheel（已验证报"No matching
   distribution found"），也没有 tesseract/Docker。
3. **OpenCode 视觉（允许的最后手段）**：用视觉直接读扫描页，产出见
   `projects/taiping-jintian/sources/processed/`。

**核对结果（举实锤）**：与 Internet Archive 自带机器OCR逐词对比，发现机器OCR把逗号读成 `^`、
"exact," 读成 "exacts"、"four" 读成 "**fbur**"、"They" 读成 "**Th^y**"、页码 5 误标为 6；木刻中文
（剿平粤匪方略）的机器OCR完全失效（关键词命中为 0），只能靠视觉阅读。所引用的关键句子两种独立
读法一致，故采信。

## 文件链接

- 详细论证（1851纪年证据）：`projects/taiping-jintian/date-evidence-1851.md`
- 原始扫描（未改动）：`projects/taiping-jintian/sources/raw/`
- OCR文本：`projects/taiping-jintian/sources/processed/`
- 未解决问题：`projects/taiping-jintian/questions.md`

（另做了义和团起因项目，见 `projects/yihetuan-causes/` 与 `assignments/week-02/answer-boxer.md`，作为第二题备用。）
