#!/usr/bin/env python3
"""Seeds assets/generated/ with lightweight placeholder SVGs so the README
never shows a broken image before the first GitHub Actions run overwrites
these with the real, live-fetched cards.
"""
import os

TEMPLATE = """<svg viewBox="0 0 1000 90" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label} — refreshing on first Action run">
  <style>
    :root {{ --bone: {bone}; --rule: {rule}; --muted: {muted}; }}
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; }}
  </style>
  <rect x="0.5" y="0.5" width="999" height="89" fill="none" stroke="var(--rule)" rx="2"/>
  <text class="mono" x="500" y="40" font-size="12" letter-spacing="2" fill="var(--muted)" text-anchor="middle">{label}</text>
  <text class="mono" x="500" y="60" font-size="10" letter-spacing="1" fill="var(--bone)" text-anchor="middle" opacity=".6">populated by GitHub Actions on first run</text>
</svg>
"""

CARDS = [
    ("stats", "GITHUB STATS"),
    ("top-langs", "TOP LANGUAGES"),
    ("activity-graph", "CONTRIBUTION ACTIVITY"),
    ("streak", "CONTRIBUTION STREAK"),
    ("trophy", "GITHUB TROPHIES"),
    ("quote", "QUOTE OF THE DAY"),
    ("weather", "LIVE WEATHER — PARIS"),
    ("snake", "CONTRIBUTION SNAKE"),
    ("metrics", "EXTENDED METRICS"),
]

PALETTES = {
    "light": dict(bone="#0A0000", rule="#4d0a0a", muted="#540303"),
    "dark": dict(bone="#EDE4DE", rule="#6b1a1a", muted="#c23b4a"),
}


def main() -> None:
    os.makedirs("assets/generated", exist_ok=True)
    for slug, label in CARDS:
        for mode, colors in PALETTES.items():
            path = f"assets/generated/{slug}-{mode}.svg"
            if os.path.exists(path):
                continue
            with open(path, "w", encoding="utf-8") as f:
                f.write(TEMPLATE.format(label=label, **colors))


if __name__ == "__main__":
    main()
