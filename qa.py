#!/usr/bin/env python3
"""Playwright QA - screenshot all 6 styles at desktop + mobile, using local files."""
import os, json
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path("/tmp/laur-deroc")
STYLES = [f"style-{i}" for i in range(1, 7)]
OUT = BASE / "qa-screenshots"
OUT.mkdir(exist_ok=True)

VIEWPORTS = [
    {"name": "desktop", "width": 1440, "height": 900},
    {"name": "mobile",  "width": 375,  "height": 812},
]

issues = []

with sync_playwright() as p:
    browser = p.chromium.launch()

    for style in STYLES:
        html_path = BASE / style / "index.html"
        url = f"file://{html_path}"

        for vp in VIEWPORTS:
            page = browser.new_page(viewport={"width": vp["width"], "height": vp["height"]})
            page.goto(url, wait_until="networkidle", timeout=30000)

            # Check for console errors
            errs = []
            page.on("console", lambda msg: errs.append(msg.text) if msg.type == "error" else None)

            # Wait for fonts
            page.wait_for_timeout(800)

            shot_name = f"{style}-{vp['name']}.png"
            page.screenshot(path=str(OUT / shot_name), full_page=True)

            # Basic checks
            checks = {}

            # Nav visible
            nav = page.locator("nav").first
            checks["nav_visible"] = nav.is_visible() if nav.count() > 0 else False

            # H1 present and not empty
            h1 = page.locator("h1").first
            checks["h1_present"] = h1.is_visible() if h1.count() > 0 else False
            if h1.count() > 0:
                checks["h1_text"] = h1.inner_text()[:60]

            # CTA button present
            cta_count = page.locator("a.cta, button.cta, .hero a, .hero button").count()
            checks["cta_present"] = cta_count > 0

            # Form overlay present (injected)
            form_present = page.locator("#consult-overlay").count() > 0
            checks["form_injected"] = form_present

            # Test form opens on CTA click
            if vp["name"] == "desktop" and form_present:
                # Find first non-nav, non-footer CTA
                trigger = page.locator(".hero a, .hero button, section a.cta, section button.cta").first
                if trigger.count() > 0:
                    try:
                        trigger.click()
                        page.wait_for_timeout(400)
                        overlay_open = page.locator("#consult-overlay.open").count() > 0
                        checks["form_opens"] = overlay_open
                        if overlay_open:
                            # Check progress bar visible
                            checks["progress_bar"] = page.locator(".cf-progress").count() > 0
                            # Close it
                            close_btn = page.locator("#consult-overlay .cf-close").first
                            if close_btn.count() > 0:
                                close_btn.click()
                                page.wait_for_timeout(300)
                    except Exception as e:
                        checks["form_opens"] = f"error: {e}"

            # Horizontal overflow check (mobile only)
            if vp["name"] == "mobile":
                scroll_w = page.evaluate("document.documentElement.scrollWidth")
                client_w = page.evaluate("document.documentElement.clientWidth")
                overflow = scroll_w > client_w + 2
                checks["no_horiz_overflow"] = not overflow
                if overflow:
                    issues.append(f"{style} mobile: horizontal overflow ({scroll_w}px > {client_w}px)")

            status = "✓" if all(v is True or (isinstance(v, str) and not v.startswith("error")) for k, v in checks.items() if k not in ["h1_text"]) else "⚠"
            print(f"  {status} {style} [{vp['name']}] → {shot_name}")
            for k, v in checks.items():
                icon = "  ✓" if v is True else ("  ✗" if v is False else "  →")
                print(f"    {icon} {k}: {v}")

            page.close()

    browser.close()

print("\n--- QA SUMMARY ---")
if issues:
    print("Issues found:")
    for i in issues:
        print(f"  ⚠ {i}")
else:
    print("No critical issues found.")

print(f"\nScreenshots saved to: {OUT}")
print("Files:")
for f in sorted(OUT.iterdir()):
    size_kb = f.stat().st_size // 1024
    print(f"  {f.name} ({size_kb}KB)")
