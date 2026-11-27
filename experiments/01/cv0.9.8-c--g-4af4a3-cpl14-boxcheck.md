# cv0.9.8-c--g-4af4a3-cpl14-boxcheck

## 摘要

（存包时没给 `--summary`）

**各步运行**（产物 manifest，最近一轮先后）：

| 步 | 页 | cv | 最后一轮起 → 止（洛杉矶） | 耗时合计 |
|---|---|---|---|---|
| page_survey | 113 | 0.9.6 | 11-26 17:35 → 11-26 17:36 | 0.0 分 |
| invert_detect | 113 | 0.9.6 | 11-26 17:36 → 11-26 17:36 | 0.3 分 |
| column_end | 113 | 0.9.6 | 11-26 17:38 → 11-26 17:38 | 0.3 分 |
| border_detect | 113 | 0.9.8 | 11-27 11:18 → 11-27 11:19 | 4.7 分 |
| border_detect_gate | 113 | 0.9.8 | 11-27 11:20 → 11-27 11:20 | 0.5 分 |
| seal_detect | 113 | 0.9.8 | 11-27 11:20 → 11-27 11:20 | 0.4 分 |
| column_warp | 113 | 0.9.6、0.9.8 | 11-26 17:37 → 11-27 11:20 | 1.7 分 |
| column_band | 113 | 0.9.8 | 11-27 11:20 → 11-27 11:20 | 0.3 分 |
| column_geometry | 113 | 0.9.8 | 11-27 11:20 → 11-27 11:20 | 0.1 分 |
| row_segment | 113 | 0.9.8 | 11-27 11:20 → 11-27 11:21 | 1.0 分 |
| cell_shrink | 113 | 0.9.6、0.9.8 | 11-26 17:40 → 11-27 11:21 | 1.8 分 |
| cut_gate | 113 | 0.9.8 | 11-27 11:21 → 11-27 11:21 | 0.1 分 |
| glyph_match | 113 | 0.9.6、0.9.8 | 11-26 17:45 → 11-27 11:25 | 14.6 分 |
| rare_candidates | 113 | 0.9.6、0.9.8 | 11-26 17:48 → 11-27 11:25 | 2.2 分 |
| align_ref | 113 | 0.9.6、0.9.8 | 11-26 17:48 → 11-27 11:25 | 0.0 分 |
| context_decide | 113 | 0.9.6、0.9.8 | 11-26 17:48 → 11-27 11:25 | 0.1 分 |
| seed_admit | 113 | 0.9.8 | 11-27 11:30 → 11-27 11:30 | 1.7 分 |

## 基本信息

- 册：01
- 存包：2026-11-27T19:31:18Z
- 基线（存包时该册的 main）：`cv0.9.6-c--g-5825dc-gridfix`
- 包：`products/98y6h42f41/01/cv0.9.8-c--g-4af4a3-cpl14-boxcheck`（1940 个文件，5.5 MB）；取回 `guji products pack fetch 01 --label cv0.9.8-c--g-4af4a3-cpl14-boxcheck --to <目录>`

## 版本

| cv | cv commit | 语料库 | 底库 | 字形库钉号 | 人裁指纹 | 中心库 rev（seed_admit 跑时） |
|---|---|---|---|---|---|---|
| 0.9.8 | ac170dde0dc4 | — | — | — | h1:158:4af4a373b8b5f9f3 | 98y6h42f41@main:1556705 |

## 册配置（存包时）

```yaml
# 《朱楓林集》第 1 册：Commons CADAL02039211《朱楓林集（一）》，113 页（一页一半叶）。
# 页型：1 书衣；2–9 序（大字六行十四字，按页列数 6，见 params）；10–36 目錄；37–113 卷一（誥、詔、表等，多抬头）。
id: "01"
cv_version: v0.9.8   # 2026-11-27 改钉：v0.9.8 有按页每列字数 chars_per_line_pages、字框几何闸 seg_box_check（出 v0.1 时钉 v0.9.6）
title: 朱楓林集 第1册
raw_dir: data_full/01
raw_pattern: "{page}.png"
dev_set: [50, 51, 86, 104]
# 序（2–9 页）六行十四字：按页每列字数（cv v0.9.8，2026-11-27）。之前按正文 20 字凑格，短列劈字、空隙切成碎格（实验记录/2026-11-27-网站标注与字框检查.md）。
chars_per_line_pages: {"2-9": 14}
page_kinds:
  cover: [1]
params:
  # 序（2–9 页）大字六行十四字，按页覆盖列数（Sheldon 2026-11-26：要能按页设行数、字数）。
  # 按页列数 expected_cols_pages 要写全 border_detect、column_geometry、border_detect_gate、column_gate、cut_gate
  # （2026-11-27 前只写了前两处，2–9 页整页被闸拒）；每列字数见顶层 chars_per_line_pages。
  # 边列过窄修正（2026-11-26，实验记录/切分体检-边列过窄.md）：自由模式在 23 页把穿字的假线当内框，
  # 首／末列被切窄；10–113 页改网格模式（列距 150px）。副本实测待审 6.31% → 4.34%，第 1 列 15.2% → 4.4%。
  border_detect:
    column_grid_pages: ["10-113"]
    grid_col_pitch: 150
    expected_cols_pages: {2: 6, 3: 6, 4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6}
  column_geometry:
    expected_cols_pages: {2: 6, 3: 6, 4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6}
  # cv v0.9.7 起 2b side_cut 缺省开；本册改钉 0.9.8 只为序页按页字数，先关着，免得 10–113 页整页重切、
  # 网站标注格号跟着动（side_cut 对本书的效果另做 A/B 再定）。
  column_band:
    side_cut: false
  border_detect_gate:
    expected_cols_pages: {2: 6, 3: 6, 4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6}
  column_gate:
    expected_cols_pages: {2: 6, 3: 6, 4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6}
  cut_gate:
    expected_cols_pages: {2: 6, 3: 6, 4: 6, 5: 6, 6: 6, 7: 6, 8: 6, 9: 6}
  # 第 9 页序末两方小印（seal_detect 按殿本调，没认出），人核覆盖；bbox 规范空间（右上原点）。
  seal_detect:
    overrides:
      9:
        - {kind: crisp, bbox: [1230, 1330, 1480, 1615]}
        - {kind: crisp, bbox: [1255, 1890, 1485, 2165]}
  # 字框几何闸（cv v0.9.8）：碎格、框线扁条、墨点、一字劈两框、过高框退回待审（seg_defect）。
  # 01 册 rev-001-r0 包扫全册，自动放行命中 2 格（3:4:7 碎格成「一」、25:2:6 其二劈三框）都是真错，全开。
  seed_admit:
    seg_box_check: [all]
```

## 前后对比

（存包时没给 `--report <diff 目录>`）

## 记事

- 2026-11-27T19:31:21Z ★ 标为 main
