#!/usr/bin/env python3
"""
Migrate image paths to the canonical structure:
  /images/<tab_name>/<year>/<topic_name>/<filename>

Moves files/directories on disk and updates all references in content files.
"""

import os
import shutil
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

# ---------------------------------------------------------------------------
# Path mapping: (old_relative, new_relative)
# Sorted longest-first so more-specific prefixes are replaced before shorter ones.
# ---------------------------------------------------------------------------
DIRECTORY_MAPPINGS = [
    # posts/ — legacy date-prefixed or concept-only directories
    ("images/posts/202109_eastgate_software",       "images/posts/2021/eastgate_software"),
    ("images/posts/20231127_crnn",                  "images/posts/2023/crnn"),
    ("images/posts/20231203_onnx_runtime_py",       "images/posts/2023/onnx_runtime_py"),
    ("images/posts/20231207_cross_entropy",         "images/posts/2023/cross_entropy"),
    ("images/posts/2024-05-17-probability-statistic","images/posts/2024/probability_statistic"),
    ("images/posts/20240121_BERT",                  "images/posts/2024/bert"),
    ("images/posts/20240406_tmux",                  "images/posts/2024/tmux"),
    ("images/posts/20240602_maskrcnn",              "images/posts/2024/maskrcnn"),
    ("images/posts/20241014-kalapa",                "images/posts/2024/kalapa"),
    ("images/posts/collate_fn",                     "images/posts/2023/collate_fn"),
    ("images/posts/iou_loss",                       "images/posts/2023/iou_loss"),
    ("images/posts/metric_f1",                      "images/posts/2023/metric_f1"),
    ("images/posts/ssd",                            "images/posts/2023/ssd"),
    ("images/posts/transformer",                    "images/posts/2024/transformer"),
    ("images/posts/vscode_tips",                    "images/posts/2024/vscode_tips"),
    # posts/ 2026 cross-tab move (collection content stored under posts/ by mistake)
    ("images/posts/2026/trekking-samu-lan-2",       "images/mylife/2026/trekking_samu_lan_2"),
    # reading/
    ("images/reading/dive2ocr",                     "images/reading/2023/dive2ocr"),
    ("images/reading/dive-to-depp-learning",        "images/reading/2024/dive_to_deep_learning"),
    ("images/reading/2026/Emotional_Intelligence",  "images/reading/2026/emotional_intelligence"),
    # learning/
    ("images/learning/2026/claude-code-in-action",  "images/learning/2026/claude_code_in_action"),
    # mylife/ — flat legacy directories
    ("images/mylife/travel-ha-long-2022",           "images/mylife/2022/travel_ha_long"),
    ("images/mylife/running-long-bien-2022",        "images/mylife/2022/running_long_bien"),
    ("images/mylife/trekking-lao-than",             "images/mylife/2023/trekking_lao_than"),
    ("images/mylife/trekking-ta-chi-nhu",           "images/mylife/2023/trekking_ta_chi_nhu"),
    ("images/mylife/running-cat-ba-2024",           "images/mylife/2024/running_cat_ba"),
    ("images/mylife/running-quang-binh-2024",       "images/mylife/2024/running_quang_binh"),
    ("images/mylife/trekking-samu",                 "images/mylife/2024/trekking_samu"),
    ("images/mylife/gap-week-2024",                 "images/mylife/2024/gap_week"),
    ("images/mylife/2025/company-trip-da-lat",      "images/mylife/2025/company_trip_da_lat"),
    ("images/mylife/2025/hiking-bao-tang-lich-su-qsvn", "images/mylife/2025/hiking_bao_tang_lich_su_qsvn"),
]

# Special case: a flat file moved into a new directory
FILE_MAPPINGS = [
    (
        "images/reading/toinoigikhinoivechaybo.jpg",
        "images/reading/2024/toi_noi_gi_khi_noi_ve_chay_bo/toinoigikhinoivechaybo.jpg",
    ),
]

CONTENT_DIRS = [
    "_posts",
    "_readings",
    "_learnings",
    "_collections",
    "_journeys",
]


def move_directory(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    if dst.exists():
        print(f"  [SKIP] destination already exists: {dst}")
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst)
    shutil.rmtree(src)
    print(f"  [MOVE] {src} → {dst}")
    return True


def move_file(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    if dst.exists():
        print(f"  [SKIP] destination already exists: {dst}")
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    print(f"  [MOVE] {src} → {dst}")
    return True


def build_reference_replacements() -> list[tuple[str, str]]:
    """Return (old_url_prefix, new_url_prefix) pairs, longest first."""
    pairs = []
    for old_rel, new_rel in DIRECTORY_MAPPINGS:
        old_url = "/" + old_rel + "/"
        new_url = "/" + new_rel + "/"
        pairs.append((old_url, new_url))
    for old_rel, new_rel in FILE_MAPPINGS:
        old_url = "/" + old_rel
        new_url = "/" + new_rel
        pairs.append((old_url, new_url))
    # Sort by length of old prefix descending to avoid partial matches
    pairs.sort(key=lambda p: len(p[0]), reverse=True)
    return pairs


def update_content_file(path: Path, replacements: list[tuple[str, str]]) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text = text
    for old, new in replacements:
        new_text = new_text.replace(old, new)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main():
    moved_dirs = 0
    moved_files = 0
    updated_files = []

    print("=== Step 1: Move image directories ===")
    for old_rel, new_rel in DIRECTORY_MAPPINGS:
        src = REPO_ROOT / old_rel
        dst = REPO_ROOT / new_rel
        if move_directory(src, dst):
            moved_dirs += 1

    print("\n=== Step 2: Move flat image files ===")
    for old_rel, new_rel in FILE_MAPPINGS:
        src = REPO_ROOT / old_rel
        dst = REPO_ROOT / new_rel
        if move_file(src, dst):
            moved_files += 1

    print("\n=== Step 3: Update content file references ===")
    replacements = build_reference_replacements()
    for content_dir in CONTENT_DIRS:
        dir_path = REPO_ROOT / content_dir
        if not dir_path.exists():
            continue
        for md_file in sorted(dir_path.glob("*.md")):
            if update_content_file(md_file, replacements):
                updated_files.append(md_file.relative_to(REPO_ROOT))
                print(f"  [UPDATE] {md_file.relative_to(REPO_ROOT)}")

    print("\n=== Summary ===")
    print(f"  Directories moved : {moved_dirs}")
    print(f"  Files moved       : {moved_files}")
    print(f"  Content files updated: {len(updated_files)}")
    for f in updated_files:
        print(f"    {f}")


if __name__ == "__main__":
    main()
