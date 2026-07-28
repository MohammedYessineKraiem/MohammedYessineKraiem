#!/usr/bin/env python3
"""Renders a rotating quote-of-the-day SVG (light + dark) into assets/generated/.
Rotation is deterministic (day-of-year based) — no external API, no key required.
"""
import datetime
import os

QUOTES = [
    ("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra"),
    ("What hurts more, the pain of hard work or the pain of regret?", None),
    ("Failure is a design input.", None),
    ("Cache before you scale.", None),
    ("Explicit fallbacks always.", None),
    ("Secure by default.", None),
]

TEMPLATE = """<svg viewBox="0 0 1000 100" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Quote of the day: {alt}">
  <style>
    :root {{ --bone: {bone}; --rule: {rule}; --muted: {muted}; --accent: {accent}; }}
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; }}
    .draw {{ stroke-dasharray: 904; stroke-dashoffset: 904; animation: draw 1.3s cubic-bezier(.6,0,.2,1) forwards; }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    .fade {{ opacity: 0; animation: fade .8s ease .3s forwards; }}
    @keyframes fade {{ to {{ opacity: 1; }} }}
    @media (prefers-reduced-motion: reduce) {{ .draw,.fade {{ animation: none; }} .draw{{stroke-dashoffset:0}} .fade{{opacity:1}} }}
  </style>
  <line class="draw" x1="48" y1="24" x2="952" y2="24" stroke="var(--rule)"/>
  <text class="mono fade" x="500" y="60" font-size="15" fill="var(--bone)" text-anchor="middle">&#8220;{quote}&#8221;</text>
  <text class="mono fade" x="500" y="84" font-size="10.5" fill="var(--accent)" text-anchor="middle" letter-spacing="2">QUOTE OF THE DAY{author}</text>
</svg>
"""


def render(quote: str, author: str | None, bone: str, rule: str, muted: str, accent: str) -> str:
    author_txt = f" &#8212; {author.upper()}" if author else ""
    alt = quote.replace('"', "'")
    return TEMPLATE.format(
        alt=alt, quote=quote, author=author_txt,
        bone=bone, rule=rule, muted=muted, accent=accent,
    )


def main() -> None:
    day = datetime.datetime.now(datetime.timezone.utc).timetuple().tm_yday
    quote, author = QUOTES[day % len(QUOTES)]

    os.makedirs("assets/generated", exist_ok=True)

    light = render(quote, author, bone="#0A0000", rule="#4d0a0a", muted="#451c1c", accent="#540303")
    dark = render(quote, author, bone="#EDE4DE", rule="#6b1a1a", muted="#7a3a3a", accent="#e0334a")

    with open("assets/generated/quote-light.svg", "w", encoding="utf-8") as f:
        f.write(light)
    with open("assets/generated/quote-dark.svg", "w", encoding="utf-8") as f:
        f.write(dark)


if __name__ == "__main__":
    main()
