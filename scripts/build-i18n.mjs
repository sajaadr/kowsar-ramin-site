#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.resolve(here,'..');
const data=JSON.parse(await fs.readFile(path.join(root,'localization','LOCALIZATION_CANONICAL.json'),'utf8'));
const template=await fs.readFile(path.join(root,'localization','index.template.html'),'utf8');
const esc=(v)=>String(v).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
const urlFor=(code)=>'https://kowsar-ramin.pages.dev'+data.route_policy[code];
const hreflangs=()=>data.locale_order.map(code=>`  <link rel="alternate" hreflang="${esc(data.locales[code].bcp47)}" href="${esc(urlFor(code))}" />`).join('\n')+`\n  <link rel="alternate" hreflang="x-default" href="${esc(urlFor('en'))}" />`;

function menu(current){
  const cur=data.locales[current];
  const globe='<svg class="language-globe" aria-hidden="true" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.4 2.5 3.6 5.5 3.6 9S14.4 18.5 12 21M12 3C9.6 5.5 8.4 8.5 8.4 12S9.6 18.5 12 21"/></svg>';
  const chevron='<svg class="language-chevron" aria-hidden="true" viewBox="0 0 16 16" fill="none"><path d="m4 6 4 4 4-4"/></svg>';
  let items='';
  for(const code of data.locale_order){
    const d=data.locales[code];
    if(code===current){
      items+=`            <li><span class="language-option is-current" aria-current="page" lang="${esc(d.bcp47)}" dir="${esc(d.dir)}"><span class="language-check" aria-hidden="true">✓</span>${esc(d.native_name)}</span></li>\n`;
    } else {
      const aria=d.messages['language.change_to'].replace('{language}',d.native_name);
      items+=`            <li><a class="language-option" href="${esc(data.route_policy[code])}" rel="alternate" hreflang="${esc(d.bcp47)}" lang="${esc(d.bcp47)}" dir="${esc(d.dir)}" data-analytics="language" data-language="${esc(code)}" aria-label="${esc(aria)}"><span class="language-check" aria-hidden="true"></span>${esc(d.native_name)}</a></li>\n`;
    }
  }
  return `<details class="language-menu">
        <summary aria-label="${esc(cur.messages['language.selector_label'])}">${globe}<span class="language-current" lang="${esc(cur.bcp47)}" dir="${esc(cur.dir)}">${esc(cur.native_name)}</span>${chevron}</summary>
        <nav class="language-panel" aria-label="${esc(cur.messages['language.selector_label'])}">
          <ul>
${items}          </ul>
        </nav>
      </details>`;
}
function render(code){
  const d=data.locales[code];
  const values={lang:d.bcp47,dir:d.dir,og_locale:d.og_locale,canonical_url:urlFor(code),hreflang_links:hreflangs(),language_menu:menu(code),...d.messages};
  return template.replace(/\{\{([^}]+)\}\}/g,(m,k)=>{
    if(!(k in values)) throw new Error('Unresolved token '+k);
    return (k==='hreflang_links'||k==='language_menu') ? values[k] : esc(values[k]);
  });
}
for(const code of data.locale_order){
  const out=render(code);
  if(out.includes('{{')) throw new Error('Unresolved token in '+code);
  const file=code==='en'?path.join(root,'site','index.html'):path.join(root,'site',code,'index.html');
  await fs.mkdir(path.dirname(file),{recursive:true});
  await fs.writeFile(file,out,'utf8');
}
console.log(`PASS built ${data.locale_order.length} locale pages`);
