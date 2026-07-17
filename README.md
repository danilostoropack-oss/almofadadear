# Almofada de Ar — almofadadear.com.br

Site estático de geração de leads para embalagens de proteção (almofada de ar, papel colmeia, void fill), hospedado no GitHub Pages.

## Estrutura

```
/
├── index.html              # Home (pillar page) — editada manualmente
├── contato/index.html      # Página de contato — editada manualmente
├── 404.html                # Página de erro
├── assets/
│   ├── css/style.css       # Folha de estilo global (todas as páginas)
│   └── js/main.js          # JS global (modal, tracking, abas)
├── img/                    # Imagens WebP otimizadas (usar sempre .webp)
├── tools/
│   ├── build.py            # Gerador de páginas + sitemap
│   └── pages/*.page        # Conteúdo das páginas internas (JSON + HTML)
├── sitemap.xml             # Gerado automaticamente pelo build
├── robots.txt
├── favicon.svg
└── site.webmanifest
```

## Como editar ou criar páginas internas

1. Edite (ou crie) um arquivo em `tools/pages/*.page`. Formato: front matter JSON com metadados (title, description, breadcrumb, FAQ, related, schema) seguido de `---BODY---` e o HTML do conteúdo.
2. Rode o build:

```bash
python3 tools/build.py
```

O script regenera todas as páginas internas **e o sitemap.xml** com a data atual.

⚠️ **Não edite manualmente** os `index.html` das pastas internas (`/almofada-de-ar/`, `/comparativos/...` etc.) — eles são sobrescritos pelo build. Edição manual só em `index.html` (home), `contato/` e `404.html`.

## Convenções

- URLs com barra final (`/almofada-de-ar/`), canônico em `https://www.almofadadear.com.br`.
- Imagens: sempre WebP, máx. 1200px de largura, com `alt` descritivo, `width`/`height` e `loading="lazy"` (exceto a primeira imagem do hero).
- Cada página tem: title/description únicos, BreadcrumbList + WebPage + FAQPage (quando há FAQ) em JSON-LD, e links internos para o cluster.
- Os PNG originais em `img/` são fonte — não referenciá-los em HTML.
