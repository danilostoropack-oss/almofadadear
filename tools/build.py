#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build estático do site Almofada de Ar.

Lê os arquivos de conteúdo em tools/pages/*.page (front matter JSON + corpo HTML),
envolve cada um no template global (head SEO, nav, breadcrumb, hero, FAQ,
páginas relacionadas, CTA e footer) e grava o HTML final na raiz do site.
Também gera o sitemap.xml automaticamente com todas as URLs publicadas.

Uso:  python3 tools/build.py
"""
import json
import os
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_DIR = os.path.join(ROOT, "tools", "pages")
BASE_URL = "https://www.almofadadear.com.br"
TODAY = date.today().isoformat()

PHONE_HUMAN = "(11) 96307-3163"
PHONE_INTL = "+5511963073163"
EMAIL = "contato@almofadadear.com.br"

LOGO_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/>'
            '<path d="M2 12l10 5 10-5"/></svg>')

WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>')


def head(meta):
    url = BASE_URL + meta["path"]
    og_image = BASE_URL + meta.get("og_image", "/unboxing.webp")
    schemas = []

    # BreadcrumbList
    items = []
    for i, (name, href) in enumerate(meta["breadcrumb"], 1):
        item = {"@type": "ListItem", "position": i, "name": name}
        if href:
            item["item"] = BASE_URL + href
        items.append(item)
    schemas.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})

    # WebPage
    schemas.append({
        "@context": "https://schema.org", "@type": meta.get("page_type", "WebPage"),
        "@id": url, "url": url, "name": meta["title"],
        "description": meta["description"], "inLanguage": "pt-BR",
        "isPartOf": {"@type": "WebSite", "@id": BASE_URL + "/#website"},
        "primaryImageOfPage": {"@type": "ImageObject", "url": og_image},
        "dateModified": TODAY,
    })

    # FAQPage
    if meta.get("faq"):
        schemas.append({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q["q"],
                 "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
                for q in meta["faq"]
            ],
        })

    # Schemas extras definidos na página
    for extra in meta.get("schema", []):
        extra.setdefault("@context", "https://schema.org")
        schemas.append(extra)

    jsonld = "\n".join(
        '  <script type="application/ld+json">%s</script>'
        % json.dumps(s, ensure_ascii=False, separators=(",", ":"))
        for s in schemas
    )

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{meta["title"]}</title>
  <meta name="description" content="{meta["description"]}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Almofada de Ar — Embalagens de Proteção">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{meta["title"]}">
  <meta property="og:description" content="{meta["description"]}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{meta["title"]}">
  <meta name="twitter:description" content="{meta["description"]}">
  <meta name="twitter:image" content="{og_image}">
  <meta name="theme-color" content="#0a0f1e">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="stylesheet" href="/assets/css/style.css">
  <script src="/assets/js/main.js" defer></script>
{jsonld}
</head>"""


def nav():
    return f"""
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
<nav class="topnav" aria-label="Navegação principal">
  <div class="wrap nav-inner">
    <a href="/" class="logo-wrap" aria-label="Almofada de Ar — página inicial">
      <div class="logo-icon">{LOGO_SVG}</div>
      <div class="logo-txt">
        <span class="n">Especialista em Embalagens de Proteção</span>
        <span class="s">Almofada de ar · Papel colmeia · Consultoria técnica</span>
      </div>
    </a>
    <div class="nav-links">
      <a href="/solucoes/">Soluções</a>
      <a href="/comparativos/">Comparativos</a>
      <a href="/guias/como-escolher-embalagem-de-protecao/">Como escolher</a>
    </div>
    <div class="nav-right">
      <a href="tel:{PHONE_INTL}" class="nav-tel">&#128222; <em>{PHONE_HUMAN}</em></a>
      <a href="/contato/" class="btn-nav" data-track="nav-cta">Solicitar Análise</a>
    </div>
  </div>
</nav>"""


def breadcrumb_nav(crumbs):
    lis = []
    for name, href in crumbs:
        if href:
            lis.append(f'<li><a href="{href}">{name}</a></li>')
        else:
            lis.append(f'<li><span aria-current="page">{name}</span></li>')
    return (f'<nav class="breadcrumb" aria-label="Trilha de navegação">'
            f'<div class="wrap"><ol>{"".join(lis)}</ol></div></nav>')


def page_hero(meta):
    wa_text = meta.get("wa_text", "Olá! Quero uma análise da minha operação de embalagem.")
    from urllib.parse import quote
    wa_url = f"https://wa.me/5511963073163?text={quote(wa_text)}"
    return f"""
<header class="page-hero">
  {breadcrumb_nav(meta["breadcrumb"])}
  <div class="wrap">
    <span class="tag-inline">{meta.get("eyebrow", "Embalagens de Proteção")}</span>
    <h1>{meta["h1"]}</h1>
    <p class="lead">{meta["lead"]}</p>
    <div class="hero-btns">
      <a href="/contato/" class="btn-primary" data-track="hero-cta">Solicitar Análise Gratuita</a>
      <a href="{wa_url}" target="_blank" rel="noopener" class="btn-ghost" data-track="hero-wa">&#128172; Falar no WhatsApp</a>
    </div>
  </div>
</header>"""


def faq_section(meta):
    if not meta.get("faq"):
        return ""
    items = "\n".join(
        f"""      <details class="faq-item">
        <summary><h3 style="font-size:inherit;font-weight:inherit;display:inline;">{q["q"]}</h3></summary>
        <div class="faq-a"><p>{q["a"]}</p></div>
      </details>"""
        for q in meta["faq"]
    )
    return f"""
<section class="section bg-navy" aria-labelledby="faq-titulo">
  <div class="wrap">
    <div class="sh">
      <span class="sh-tag">Dúvidas frequentes</span>
      <h2 id="faq-titulo">Perguntas sobre {meta.get("faq_topic", meta["breadcrumb"][-1][0].lower())}</h2>
    </div>
    <div class="faq-list">
{items}
    </div>
  </div>
</section>"""


def related_section(meta):
    if not meta.get("related"):
        return ""
    cards = "\n".join(
        f"""      <a class="related-card" href="{r["href"]}">
        <strong>{r["title"]}</strong>
        <span>{r["desc"]}</span>
      </a>"""
        for r in meta["related"]
    )
    return f"""
<aside class="related" aria-label="Conteúdo relacionado">
  <div class="wrap">
    <h2>Continue explorando</h2>
    <div class="related-grid">
{cards}
    </div>
  </div>
</aside>"""


def cta_final(meta):
    from urllib.parse import quote
    wa_text = meta.get("wa_text", "Olá! Quero uma análise da minha operação de embalagem.")
    wa_url = f"https://wa.me/5511963073163?text={quote(wa_text)}"
    title = meta.get("cta_title", "Quer saber qual proteção faz sentido para a sua operação?")
    text = meta.get("cta_text", "Análise técnica gratuita, sem compromisso. Diagnóstico personalizado para o seu tipo de produto e volume de pedidos.")
    return f"""
<section class="cta-final">
  <div class="wrap">
    <h2>{title}</h2>
    <p>{text}</p>
    <div class="cta-btns">
      <a href="/contato/" class="btn-cta-primary" data-track="cta-final">Solicitar Análise Gratuita</a>
      <a href="{wa_url}" target="_blank" rel="noopener" class="btn-cta-wa" data-track="cta-final-wa">&#128172; Conversar no WhatsApp</a>
      <a href="mailto:{EMAIL}?subject=An%C3%A1lise%20de%20embalagem" class="btn-cta-ghost">&#9993; {EMAIL}</a>
    </div>
  </div>
</section>"""


def footer():
    return f"""
<footer>
  <div class="wrap">
    <div class="footer-inner">
      <div class="footer-brand">
        <span class="fn">Almofada <em>de Ar</em></span>
        <p>Consultoria especializada em embalagens de proteção: almofada de ar, papel colmeia, colmeia plástica e sistemas automáticos. São Paulo · atendimento em todo o Brasil.</p>
        <p class="tel">&#128222; {PHONE_HUMAN}</p>
        <p class="tel">&#9993; <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div>
        <h2 class="f-title">Soluções</h2>
        <ul>
          <li><a href="/almofada-de-ar/">Almofada de Ar</a></li>
          <li><a href="/cushion-film/">Cushion Film</a></li>
          <li><a href="/papel-colmeia/">Papel Colmeia</a></li>
          <li><a href="/papel-kraft/">Papel Kraft</a></li>
          <li><a href="/colmeia-plastica/">Colmeia Plástica</a></li>
          <li><a href="/manta-de-protecao/">Manta de Proteção</a></li>
          <li><a href="/maquina-de-almofada-de-ar/">Máquina de Almofada de Ar</a></li>
          <li><a href="/maquina-de-papel/">Máquina de Papel</a></li>
        </ul>
      </div>
      <div>
        <h2 class="f-title">Aplicações</h2>
        <ul>
          <li><a href="/embalagem-de-protecao/">Embalagem de Proteção</a></li>
          <li><a href="/preenchimento-de-caixas/">Preenchimento de Caixas</a></li>
          <li><a href="/embalagem-para-ecommerce/">E-commerce</a></li>
          <li><a href="/embalagem-industrial/">Indústria</a></li>
          <li><a href="/embalagem-sustentavel/">Sustentável</a></li>
          <li><a href="/protecao-para-transporte/">Transporte</a></li>
          <li><a href="/automacao-de-embalagem/">Automação</a></li>
        </ul>
      </div>
      <div>
        <h2 class="f-title">Conteúdo</h2>
        <ul>
          <li><a href="/comparativos/">Comparativos Técnicos</a></li>
          <li><a href="/substituto-do-plastico-bolha/">Substituto do Plástico Bolha</a></li>
          <li><a href="/guias/como-escolher-embalagem-de-protecao/">Como Escolher Embalagem</a></li>
          <li><a href="/guias/como-reduzir-avarias-no-transporte/">Como Reduzir Avarias</a></li>
          <li><a href="/guias/custo-e-roi-da-embalagem/">Custo e ROI da Embalagem</a></li>
          <li><a href="/contato/">Contato</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Almofada de Ar · Especialista em Embalagens de Proteção · São Paulo, Brasil</span>
      <span><a href="mailto:{EMAIL}">{EMAIL}</a> · {PHONE_HUMAN}</span>
    </div>
  </div>
</footer>

<a href="https://wa.me/5511963073163?text=Ol%C3%A1%2C%20gostaria%20de%20falar%20com%20um%20especialista%20em%20embalagens." class="wa-float" target="_blank" rel="noopener" aria-label="Falar com especialista no WhatsApp">
  {WA_SVG}
  <span>Falar com especialista</span>
</a>"""


def build_page(meta, body):
    html = (
        head(meta)
        + "\n<body>\n"
        + nav()
        + page_hero(meta)
        + f'\n<main id="conteudo">\n{body}\n'
        + faq_section(meta)
        + "\n</main>\n"
        + related_section(meta)
        + cta_final(meta)
        + footer()
        + "\n</body>\n</html>\n"
    )
    rel = meta["path"].strip("/")
    out_dir = os.path.join(ROOT, *rel.split("/")) if rel else ROOT
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return meta["path"]


def build_sitemap(paths):
    """Gera sitemap.xml com home, contato e todas as páginas geradas."""
    urls = ["/", "/contato/"] + sorted(paths)
    entries = "\n".join(
        f"""  <url>
    <loc>{BASE_URL}{p}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{"weekly" if p == "/" else "monthly"}</changefreq>
    <priority>{"1.0" if p == "/" else ("0.9" if p.count("/") == 2 else "0.8")}</priority>
  </url>"""
        for p in urls
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>
"""
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)


def main():
    if not os.path.isdir(PAGES_DIR):
        sys.exit("tools/pages/ não encontrado")
    paths = []
    for fname in sorted(os.listdir(PAGES_DIR)):
        if not fname.endswith(".page"):
            continue
        raw = open(os.path.join(PAGES_DIR, fname), encoding="utf-8").read()
        meta_raw, body = raw.split("---BODY---", 1)
        meta = json.loads(meta_raw)
        paths.append(build_page(meta, body.strip()))
        print("OK", meta["path"])
    build_sitemap(paths)
    print(f"\n{len(paths)} páginas geradas + sitemap.xml")


if __name__ == "__main__":
    main()
