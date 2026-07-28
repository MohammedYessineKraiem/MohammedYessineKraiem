#!/usr/bin/env python3
"""Renders a live Paris weather-card SVG (light + dark) into assets/generated/.
Reads JSON already fetched from wttr.in (no API key required) at the path
given as argv[1] (defaults to weather.json in the current directory).
"""
import json
import os
import sys

TEMPLATE = """<svg viewBox="0 0 1000 110" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Live weather in Paris: {desc}, {temp}°C">
  <style>
    :root {{ --bone: {bone}; --rule: {rule}; --muted: {muted}; --accent: {accent}; }}
    .mono {{ font-family: ui-monospace, "SFMono-Regular", "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; }}
    .fade {{ opacity: 0; animation: fade .8s ease forwards; }}
    @keyframes fade {{ to {{ opacity: 1; }} }}
    .pulse {{ animation: pulse 2.6s ease-in-out infinite; }}
    @keyframes pulse {{ 0%,100%{{opacity:1}} 50%{{opacity:.4}} }}
    @media (prefers-reduced-motion: reduce) {{ .fade,.pulse {{ animation: none; opacity: 1; }} }}
  </style>
  <line x1="48" y1="24" x2="952" y2="24" stroke="var(--rule)"/>
  <text class="mono fade" x="48" y="16" font-size="10.5" fill="var(--muted)" letter-spacing="3">LIVE WEATHER &#8212; PARIS, FR</text>
  <circle class="pulse" cx="60" cy="66" r="4" fill="var(--accent)"/>
  <text class="mono fade" x="82" y="72" font-size="30" fill="var(--bone)">{temp}&#176;C</text>
  <text class="mono fade" x="270" y="72" font-size="14" fill="var(--muted)">{desc}</text>
  <text class="mono fade" x="952" y="72" font-size="11" fill="var(--muted)" text-anchor="end" letter-spacing="1">FEELS {feels}&#176;C &#183; HUMIDITY {humidity}%</text>
</svg>
"""


def render(temp, desc, feels, humidity, bone, rule, muted, accent) -> str:
    return TEMPLATE.format(
        temp=temp, desc=desc, feels=feels, humidity=humidity,
        bone=bone, rule=rule, muted=muted, accent=accent,
    )


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "weather.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    current = data["current_condition"][0]
    temp = current["temp_C"]
    feels = current["FeelsLikeC"]
    humidity = current["humidity"]
    desc = current["weatherDesc"][0]["value"]

    os.makedirs("assets/generated", exist_ok=True)

    light = render(temp, desc, feels, humidity, bone="#0A0000", rule="#4d0a0a", muted="#451c1c", accent="#540303")
    dark = render(temp, desc, feels, humidity, bone="#EDE4DE", rule="#6b1a1a", muted="#7a3a3a", accent="#e0334a")

    with open("assets/generated/weather-light.svg", "w", encoding="utf-8") as f:
        f.write(light)
    with open("assets/generated/weather-dark.svg", "w", encoding="utf-8") as f:
        f.write(dark)


if __name__ == "__main__":
    main()
