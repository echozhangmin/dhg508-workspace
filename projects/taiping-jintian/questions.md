# Questions — 太平天国 / 金田起义 (Week 2)

## 1851 date (follow-ups from the date-evidence work)

- **Page-verify a 卷一–卷五 memorial.** The memorials naming 金田 with an explicit
  道光三十年/咸豐元年 date are in the sibling scans (卷二 = `02080989.cn`, 卷三 = `02080990.cn`;
  vol.1 = `02080988.cn` contains 卷首+目錄 only, 136 leaves). Machine OCR fails on the woodblock
  text, so each page needs vision reading. Next: open 卷二 leaf-by-leaf at the 咸豐元年 range.
- **《清史稿》 wording.** Quote-checked from a compiled transcription; verify against a standard
  edition (中華書局標點本, 卷三百九十三) before citing in final work.
- **Granularity of Meadows' dates.** "4th March 1851" (金田西移) and his "1850" for the outbreak
  ("Kwangse rebellion broke out") use different events — need the 1850 passage's page verified
  before using both.
- **咸豐元年正月→Gregorian conversion.** Cross-check 正月初一 (1851-02-01?) against an independent
  兼查 tools (e.g.氣象/农历 table) rather than one converter.

## From earlier

- **Guiping / Thistle Mount page check.** Meadows names "Thistle mount in the Kwei ping district"
  (紫荆山, 桂平县) in the machine text, but I have not yet located and OCR-checked the page image for
  that passage.
- **A Chinese primary source with the date inside.** Ideally a Qing memorial (奏折) or 《太平天日》 /
  《太平天国起义记》 scan naming the date 十二月初十日 in 咸豐-years.
- **Date system.** Right as Gregorian 1851-01-11 = 道光三十年十二月初十 (lunar). Confirm no source
  discrepancy of a day.
- **"爆发" definition.** 团营 assembly (July 1850) vs. armed 起义 (11 Jan 1851); state the choice.
- **Machine-OCR accuracy.** Re-run methods 1/2 later (with a key / Python 3.12) and compare accuracy.

## Week 3 — 六王小库 / 天国掌故 skill

- **画像真伪。** 六王均无可信的当时真容：洪秀全现用 1853 年欧洲石印「疑似画像」，其余为
  桂林太平天国纪念馆现代铜像。需查是否还有更可靠的当时图像（或明确弃用画像只留文字描述）。
- **生年异说。** 萧朝贵 1820/1826、冯云山 1815/1822、韦昌辉 1823/1826，均未定；库中照实并列，
  待找一手史料（如《天兄圣旨》《贼情汇纂》）定夺。
- **洪秀全死因。** 病逝（主流）与曾国藩奏报「服毒自尽」两说，库中并存。
- **石达开出走兵力。** 旧说「率军二十万」与今研究（初离天京仅数千人）冲突，库中未采用数字。
- **库的边界。** 现仅收开国六王（天王+五王），未收幼天王、干王、忠王等；是否扩展待定。

## Week 4 — 关系型库 + 渐进 skill

- **永安建制确切月日。** 通行作 1851 年 12 月，但该农历月入公历 1852-01；需要一条
  带明确日期的第一手（《钦定剿平粤匪方略》相关卷、或《天父天兄圣旨》）来定。
- **页级一手证据仍偏少。** 300+ 行里，多数人物的 `locator` 是维基条目的段落；真正
  页级的一手来源只有 Meadows p.5 / p.155 与《剿平粤匪方略》卷首目錄。待把卷二、卷三
  逐页 vision OCR，给关键事件补上页码出处。
- **家世/子嗣缺表。** Q2 暴露：库中没有 family/子嗣 关系，石达开诸子、洪秀全诸子都查不到。
  考虑加 `relations(person_id, relation, person_id|name_raw, …)` 表（仍带出处）。
- **西文转写未入 `name_variants`。** Meadows 用 Hung Seu-tsuen / Yang Sew-tsing 等拼法，
  尚未逐页核到页码，故未收录；补页后应作为 `kind='transliteration'` 入表。
- **画像真伪（承 Week 3）。** 库 v4 暂未收图片表；若收，需单列 `portrait_note` 并一律
  标注「非当时真容」。
