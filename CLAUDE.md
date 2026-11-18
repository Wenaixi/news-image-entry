# CLAUDE.md

## 项目定位

make.fun 比赛 news-image-20261117 的参赛仓库：交付一张汇总 2026 年 11 月 17 日世界新闻的图片，由能看图的 AI 评委两两对比打分。评分对象是图片本身，不是代码。

## 运行契约

- `main.py`：Python 3.13，仅标准库，不联网。把仓库根目录的 `entry.png` 复制到 `$MAKEFUN_OUTPUT_DIR/entry.png`，变量未设置时用 `/output`。
- 输出目录用 `os.makedirs(..., exist_ok=True)` 创建；复制前若目标已存在先删除；复制用 `shutil.copyfile` 保证字节一致。
- 复制后把输出文件的 sha256 打印到 stderr，不改变文件内容。
- 两次运行必须逐字节相同：输出只取决于仓库内的 `entry.png`，没有任何外部输入。
- `verify.py`：跑两遍 `main.py`（输出到仓库内 `tmp-verify/run1`、`run2`），断言逐字节一致、PNG 魔数、尺寸 1024x1024、不超过 1 MiB，打印 PASS/FAIL 与 sha256。

## 交付物

- `entry.png`：1024x1024 PNG，122826 字节，sha256 `0d94a7a20517e18b9a587b6a77423e73f5ee214ff7af9ee6fcd6baf4f8c2edeb`。
- `README.md`：严格按赛事模板，badge 与链接 URL 不可改动。
- `LICENSE`：MIT 全文，首行 `SPDX-License-Identifier: MIT`，版权人 Wenaixi，年份 2026。
- `.makefun/owner.json`：`{"wallet": "8qUCLdUqnF5YhkXwES5Lqnz3oLwos3Bw4eRojr6i4HYg"}`。
- `.gitignore`：忽略 `__pycache__/`、`*.pyc`、`out/`、`tmp*/`。

## 环境注意事项（Windows 本机）

- 本机 Python 为 3.12.8，比赛运行时为 3.13；代码只使用两者都存在的标准库接口。
- 本机 `tempfile.mkdtemp` 生成的目录带无法访问的 ACL（`icacls` 也读不了），因此 `verify.py` 不用 `tempfile`，改为在仓库内创建固定目录 `tmp-verify/` 并自行清理。
- 系统 Temp 目录在沙箱内不可写，验证目录必须留在仓库内，且被 `.gitignore` 的 `tmp*/` 覆盖。

## 常用命令

```sh
python verify.py        # 端到端验证，期望输出 PASS
python main.py          # 复制图片到 $MAKEFUN_OUTPUT_DIR 或 /output
```
