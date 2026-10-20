#!/usr/bin/env python3
import json
import os
import threading
import time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DATA = json.loads((ROOT / "localization" / "LOCALIZATION_CANONICAL.json").read_text(encoding="utf-8"))
OUT = ROOT / "qa-artifacts" / "i18n-visual"
OUT.mkdir(parents=True, exist_ok=True)

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def start_server():
    os.chdir(SITE)
    server = ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server

VIEWPORTS = [
    ("narrow", 360, 640),
    ("mobile", 390, 844),
    ("tablet", 768, 1024),
    ("desktop", 1440, 1000),
]

def main():
    server = start_server()
    base = f"http://127.0.0.1:{server.server_port}/"
    failures = []
    summary = {}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            for code in DATA["locale_order"]:
                route = DATA["route_policy"][code].lstrip("/")
                locale_result = {}
                for name, width, height in VIEWPORTS:
                    context = browser.new_context(viewport={"width": width, "height": height})
                    page = context.new_page()
                    console_errors = []
                    page_errors = []
                    page.on("console", lambda msg, bag=console_errors: bag.append(msg.text) if msg.type == "error" else None)
                    page.on("pageerror", lambda exc, bag=page_errors: bag.append(str(exc)))
                    response = page.goto(urljoin(base, route), wait_until="networkidle")
                    if not response or response.status != 200:
                        failures.append(f"{code}/{name}: HTTP {None if not response else response.status}")
                        context.close()
                        continue

                    metrics = page.evaluate("""() => {
                      const root = document.documentElement;
                      const cards = [...document.querySelectorAll('.identity-card')];
                      const compact = [...document.querySelectorAll('.button, .contact-card, .share-button')];
                      const box = el => ({clientW:el.clientWidth, scrollW:el.scrollWidth, clientH:el.clientHeight, scrollH:el.scrollHeight});
                      return {
                        lang: root.lang,
                        dir: root.dir || getComputedStyle(root).direction,
                        bodyWidth: root.scrollWidth,
                        innerWidth: innerWidth,
                        cards: cards.map(box),
                        compact: compact.map(box),
                        emailDir: getComputedStyle(document.querySelector('#contact-email')).direction,
                        phoneDir: getComputedStyle(document.querySelector('#contact-phone')).direction
                      };
                    }""")
                    expected = DATA["locales"][code]
                    if metrics["lang"] != expected["bcp47"]:
                        failures.append(f"{code}/{name}: lang {metrics['lang']}")
                    if metrics["dir"] != expected["dir"]:
                        failures.append(f"{code}/{name}: dir {metrics['dir']}")
                    if metrics["bodyWidth"] > metrics["innerWidth"] + 1:
                        failures.append(f"{code}/{name}: horizontal overflow {metrics['bodyWidth']}>{metrics['innerWidth']}")
                    for idx, box in enumerate(metrics["cards"]):
                        if box["scrollH"] > box["clientH"] + 2 or box["scrollW"] > box["clientW"] + 2:
                            failures.append(f"{code}/{name}: identity-card[{idx}] overflow {box}")
                    for idx, box in enumerate(metrics["compact"]):
                        if box["scrollW"] > box["clientW"] + 2:
                            failures.append(f"{code}/{name}: compact[{idx}] horizontal overflow {box}")
                    if code == "fa" and (metrics["emailDir"] != "ltr" or metrics["phoneDir"] != "ltr"):
                        failures.append(f"fa/{name}: mixed-Latin contact fields not LTR")

                    trigger = page.locator(".language-menu summary")
                    if not trigger.is_visible():
                        failures.append(f"{code}/{name}: language trigger not visible")
                    else:
                        bb = trigger.bounding_box()
                        if not bb or bb["x"] < -1 or bb["y"] < -1 or bb["x"] + bb["width"] > width + 1:
                            failures.append(f"{code}/{name}: language trigger outside viewport {bb}")
                        trigger.click()
                        options = page.locator(".language-option")
                        if options.count() != len(DATA["locale_order"]):
                            failures.append(f"{code}/{name}: language option count {options.count()}")
                        panel = page.locator(".language-panel")
                        if not panel.is_visible():
                            failures.append(f"{code}/{name}: language panel not visible")
                        else:
                            pbb = panel.bounding_box()
                            if not pbb or pbb["x"] < -1 or pbb["x"] + pbb["width"] > width + 1:
                                failures.append(f"{code}/{name}: language panel horizontal bounds {pbb}")
                        for i in range(options.count()):
                            ob=options.nth(i).bounding_box()
                            if ob and ob["height"] < 43:
                                failures.append(f"{code}/{name}: option[{i}] target height {ob['height']}")
                    if console_errors:
                        failures.append(f"{code}/{name}: console errors {console_errors}")
                    if page_errors:
                        failures.append(f"{code}/{name}: page errors {page_errors}")

                    if name in ("mobile","desktop"):
                        page.locator(".language-menu").evaluate("(el) => el.removeAttribute('open')")
                        page.screenshot(path=str(OUT / f"{code}-{name}.png"), full_page=True)
                    locale_result[name] = {"console_errors": console_errors, "page_errors": page_errors}
                    context.close()
                summary[code] = locale_result
            browser.close()
    finally:
        server.shutdown()

    (OUT / "summary.json").write_text(json.dumps({"failures": failures, "locales": summary}, ensure_ascii=False, indent=2), encoding="utf-8")
    if failures:
        print("FAIL visual i18n QA")
        for failure in failures:
            print("-", failure)
        raise SystemExit(1)
    print(f"PASS visual i18n QA: {len(DATA['locale_order'])} locales x {len(VIEWPORTS)} viewports")

if __name__ == "__main__":
    main()
