#!/usr/bin/env python3
"""
Mac上でページの表示確認をするスクリプト

使い方:
  python preview.py          # 全ページを表示
  python preview.py weather  # 指定ページのみ表示
"""

import sys
import pages


def main():
    if len(sys.argv) > 1:
        name = sys.argv[1]
        page = pages.PAGE_NAMES.get(name)
        if not page:
            available = list(pages.PAGE_NAMES.keys())
            print(f"Unknown page '{name}'. Available: {available}")
            sys.exit(1)
        pages_to_show = [page]
    else:
        pages_to_show = pages.PAGES

    for page in pages_to_show:
        img = page.create_image()
        img.show()


if __name__ == "__main__":
    main()
