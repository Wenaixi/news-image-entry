"""跑两次 main.py，验证输出逐字节一致且是合规的 1024x1024 PNG。

用法：python verify.py
临时目录建在仓库内的 tmp-verify/ 下，运行前后自动清理。
"""

import hashlib
import os
import shutil
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK_DIR = ROOT / "tmp-verify"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576
EXPECTED_SIZE = (1024, 1024)


def run_once(output_dir: Path) -> bytes:
    env = dict(os.environ, MAKEFUN_OUTPUT_DIR=str(output_dir))
    subprocess.run([sys.executable, str(ROOT / "main.py")], check=True, env=env)
    return (output_dir / "entry.png").read_bytes()


def check(data: bytes) -> list[str]:
    errors = []
    if data[:8] != PNG_MAGIC:
        errors.append("前 8 字节不是 PNG 魔数")
    if len(data) > MAX_BYTES:
        errors.append(f"文件超过 1 MiB：{len(data)} 字节")
    if len(data) >= 24 and data[:8] == PNG_MAGIC:
        width, height = struct.unpack(">II", data[16:24])
        if (width, height) != EXPECTED_SIZE:
            errors.append(f"尺寸不是 1024x1024：{width}x{height}")
    return errors


def main() -> int:
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    WORK_DIR.mkdir()
    try:
        first = run_once(WORK_DIR / "run1")
        second = run_once(WORK_DIR / "run2")
    finally:
        shutil.rmtree(WORK_DIR, ignore_errors=True)

    errors = check(first) + check(second)
    if first != second:
        errors.append("两次运行输出不一致")
    if first[:8] == PNG_MAGIC and len(first) >= 24:
        width, height = struct.unpack(">II", first[16:24])
    else:
        width, height = 0, 0

    digest = hashlib.sha256(first).hexdigest()
    print(f"sha256: {digest}")
    print(f"bytes: {len(first)}")
    print(f"size: {width}x{height}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
