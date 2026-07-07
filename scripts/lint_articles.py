#!/usr/bin/env python3
"""손글 Hugo 아티클 린터 — CJK 볼드 미닫힘 + Sources 카운트 정합.
사용: python3 scripts/lint_articles.py [content/posts]
종료코드: ERROR 있으면 1, 없으면 0. WARN은 0."""

from __future__ import annotations
import re
import sys
import glob
import os

# 규칙1(ERROR): 닫는 ** 가 [닫는 구두점] + ** + [한글] 로 붙은 경우.
#   CommonMark 우측 플랭킹 실패로 볼드가 안 닫힘. (예: "…"**는)
#   앞이 한글이면(라**는) 정상이므로 제외 — 구두점 앞일 때만 잡는다.
BOLD_BUG = re.compile(r'[)\]}"\'’”».,!?;:]\*\*[가-힣]')
# 규칙3(WARN): 콘텐츠 라인의 ** 개수가 홀수(미닫힘 가능성). 코드펜스/프론트매터 제외.
SUMMARY_COUNT = re.compile(r"참고\s*자료\s*\((\d+)\)|Sources\s*\((\d+)\)")


def lint_file(path: str) -> tuple[list[str], list[str]]:
    errors, warns = [], []
    txt = open(path, encoding="utf-8").read()
    lines = txt.splitlines()

    # 프론트매터/코드펜스 마스킹
    in_fm = False
    in_code = False
    body_lines = []
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        if i == 1 and s == "---":
            in_fm = True
            continue
        if in_fm and s == "---":
            in_fm = False
            continue
        if in_fm:
            continue
        if s.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        body_lines.append((i, ln))

    for i, ln in body_lines:
        if BOLD_BUG.search(ln):
            errors.append(
                f"{path}:{i} CJK 볼드 미닫힘([구두점]**[한글]): {ln.strip()[:90]}"
            )
        if ln.count("**") % 2 == 1:
            warns.append(f"{path}:{i} 홀수 개의 ** (미닫힘 가능): {ln.strip()[:90]}")

    # Sources 카운트 정합: <details class="sources"> ~ </details> 블록마다
    for m in re.finditer(r'<details class="sources">(.*?)</details>', txt, re.S):
        block = m.group(1)
        li = len(re.findall(r"<li\b", block))
        cm = SUMMARY_COUNT.search(block)
        if cm:
            declared = int(cm.group(1) or cm.group(2))
            if declared != li:
                errors.append(
                    f"{path} Sources 카운트 불일치: summary=({declared}) vs <li>={li}"
                )
        else:
            warns.append(f"{path} Sources 블록에 카운트 표기(N) 없음")
    return errors, warns


def main(argv):
    root = argv[1] if len(argv) > 1 else "content/posts"
    files = sorted(glob.glob(os.path.join(root, "**", "*.md"), recursive=True))
    all_err, all_warn = [], []
    for f in files:
        e, w = lint_file(f)
        all_err += e
        all_warn += w
    for w in all_warn:
        print(f"WARN  {w}")
    for e in all_err:
        print(f"ERROR {e}")
    print(f"\n스캔 {len(files)}개 · ERROR {len(all_err)} · WARN {len(all_warn)}")
    return 1 if all_err else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
