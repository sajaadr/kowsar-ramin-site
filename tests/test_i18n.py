from pathlib import Path
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/"localization"/"LOCALIZATION_CANONICAL.json").read_text(encoding="utf-8"))

class I18nAuthorityTests(unittest.TestCase):
    def test_locale_and_key_parity(self):
        self.assertEqual(DATA["locale_order"],["en","tr","de","es","pt","it","fa","fr","az","hy","ka"])
        keys=set(DATA["locales"]["en"]["messages"])
        for code in DATA["locale_order"]:
            self.assertEqual(set(DATA["locales"][code]["messages"]),keys)
            self.assertTrue(all(v.strip() for v in DATA["locales"][code]["messages"].values()))
    def test_direction_and_routes(self):
        self.assertEqual(DATA["locales"]["fa"]["dir"],"rtl")
        for code in DATA["locale_order"]:
            if code!="fa": self.assertEqual(DATA["locales"][code]["dir"],"ltr")
        self.assertEqual(len(set(DATA["route_policy"].values())),len(DATA["locale_order"]))
    def test_language_placeholder(self):
        for code in DATA["locale_order"]:
            self.assertEqual(DATA["locales"][code]["messages"]["language.change_to"].count("{language}"),1)

if __name__=="__main__":
    unittest.main()
