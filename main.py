"""把仓库根目录中的新闻头版图复制到输出目录的 entry.png。

输出目录取自环境变量 MAKEFUN_OUTPUT_DIR；未设置时使用 /output。

程序不访问网络，输出内容只取决于仓库里的 entry.png，因此同样的源文件
每次运行都会得到逐字节相同的结果。复制完成后把输出文件的 sha256 打印到
stderr，便于核对，不影响文件本身。
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)
    target = output_dir / "entry.png"
    if target.exists():
        target.unlink()
    shutil.copyfile(SOURCE, target)
    print(f"sha256: {sha256_of(target)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
