#!/usr/bin/env python3
"""All 11 locales, Firefox+WebKit desktop/mobile smoke checks.
Chromium exhaustive visual QA is run by visual_i18n_qa.py.
"""
import json
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from threading import Thread
from functools import partial
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT / "site"
DATA=json.loads((ROOT / "localization" / "LOCALIZATION_CANONICAL.json").read_text(encoding="utf-8"))

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass

def run():
    server=ThreadingHTTPServer(("127.0.0.1",0),partial(QuietHandler,directory=str(SITE)))
    Thread(target=server.serve_forever,daemon=True).start()
    failures=[]
    try:
        with sync_playwright() as pw:
            for engine in ("firefox","webkit"):
                browser=getattr(pw,engine).launch(headless=True)
                try:
                    for mode,w,h in (("mobile",390,844),("desktop",1440,1000)):
                        for code in DATA["locale_order"]:
                            context=browser.new_context(viewport={"width":w,"height":h},
                                is_mobile=(mode=="mobile" and engine=="webkit"),
                                has_touch=(mode=="mobile"))
                            page=context.new_page()
                            errors=[]
                            page.on("pageerror",lambda ex,bag=errors:bag.append(str(ex)))
                            url=f"http://127.0.0.1:{server.server_port}"+DATA["route_policy"][code]
                            response=page.goto(url,wait_until="networkidle")
                            if not response or response.status!=200:
                                failures.append(f"{engine}/{mode}/{code}: HTTP")
                                context.close()
                                continue
                            info=page.evaluate("""() => {
                                const root=document.documentElement;
                                return {
                                    lang:root.lang,dir:root.dir,
                                    width:root.scrollWidth,viewport:innerWidth,
                                    font:getComputedStyle(document.body).fontFamily,
                                    cards:document.querySelectorAll('.identity-card').length,
                                    contactEmail:getComputedStyle(document.querySelector('#contact-email')).direction,
                                    contactPhone:getComputedStyle(document.querySelector('#contact-phone')).direction
                                };
                            }""")
                            if info["lang"]!=code or info["dir"]!=DATA["locales"][code]["dir"]:
                                failures.append(f"{engine}/{mode}/{code}: lang-dir")
                            if info["width"]>info["viewport"]+1:
                                failures.append(f"{engine}/{mode}/{code}: horizontal overflow")
                            if info["cards"]!=3:
                                failures.append(f"{engine}/{mode}/{code}: card count")
                            if code=="fa":
                                if "KR Estedad" not in info["font"]:
                                    failures.append(f"{engine}/{mode}/{code}: font family")
                                loaded=page.evaluate("""() => [...document.fonts].some(
                                    f=>f.family.replace(/["']/g,'')==='KR Estedad' && f.status==='loaded')""")
                                if not loaded:
                                    failures.append(f"{engine}/{mode}/{code}: font file not loaded")
                                if info["contactEmail"]!="ltr" or info["contactPhone"]!="ltr":
                                    failures.append(f"{engine}/{mode}/{code}: LTR contact isolation")
                            menu=page.locator(".language-menu summary")
                            if not menu.is_visible():
                                failures.append(f"{engine}/{mode}/{code}: language selector hidden")
                            else:
                                menu.click()
                                if not page.locator(".language-panel").is_visible() or page.locator(".language-option").count()!=len(DATA["locale_order"]):
                                    failures.append(f"{engine}/{mode}/{code}: selector")
                            if errors:
                                failures.append(f"{engine}/{mode}/{code}: script errors {errors}")
                            context.close()
                finally:
                    browser.close()
    finally:
        server.shutdown()
    if failures:
        print("FAIL cross-engine QA",*failures,sep="\n")
        raise SystemExit(1)
    print("PASS cross-engine QA: 11 locales x 2 viewports x 2 engines = 44 checks")

if __name__=="__main__":
    run()
