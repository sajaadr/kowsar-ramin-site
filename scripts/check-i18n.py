#!/usr/bin/env python3
import json, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'localization' / 'LOCALIZATION_CANONICAL.json'
data = json.loads(P.read_text(encoding='utf-8'))

assert data['schema'] == 'KR_LOCALIZATION/1'
assert data['source_locale'] == 'en'
order = data['locale_order']
assert order == ['en','tr','de','es','pt','it','fa','fr','az','hy','ka']
assert set(data['route_policy']) == set(order)
assert len(set(data['route_policy'].values())) == len(order)

source = data['locales']['en']['messages']
keys = set(source)
assert keys
for code in order:
    loc = data['locales'][code]
    msgs = loc['messages']
    assert set(msgs) == keys, f'{code}: key mismatch'
    assert all(isinstance(v, str) and v.strip() for v in msgs.values()), f'{code}: blank value'
    assert msgs['language.change_to'].count('{language}') == 1, f'{code}: placeholder mismatch'
    for key, value in msgs.items():
        assert value == unicodedata.normalize('NFC', value), f'{code}:{key}: non-NFC'
        assert '<script' not in value.lower(), f'{code}:{key}: markup injection'
assert data['locales']['fa']['dir'] == 'rtl'
assert all(data['locales'][c]['dir'] == 'ltr' for c in order if c != 'fa')
print(f'PASS i18n canonical: {len(order)} locales x {len(keys)} keys')
