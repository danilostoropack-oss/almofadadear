# Relatório de Auditoria e Implementação SEO — almofadadear.com.br

Data: 16/07/2026 · Escopo: auditoria completa + reestruturação total do site

---

## 1. Diagnóstico do site anterior

O site era uma landing page única (`index.html` + `/contato`) com bons fundamentos de conversão, mas sem capacidade de ranquear além de 1–2 consultas. Problemas encontrados:

**Críticos para SEO:**
- Apenas 2 URLs indexáveis — impossível construir autoridade temática (topical authority) para as dezenas de palavras-chave alvo.
- Imagens PNG de 2,0–2,7 MB cada (~50 MB no total) — LCP catastrófico no mobile, nota Lighthouse de performance muito baixa.
- CSS e JS inline (35 KB+ repetidos por página) — sem cache entre páginas.
- Sem breadcrumbs, sem hierarquia de conteúdo, sem links internos estruturados.
- Schema limitado (ProfessionalService + FAQ simples), sem Organization/WebSite/BreadcrumbList/Product/HowTo.
- FAQ com `div` + JS (invisível sem JavaScript); acordeão não semântico.
- Sem favicon, sem manifest, sem 404 personalizada.
- Sitemap com 2 URLs; robots.txt básico.
- Erro de sintaxe no JSON-LD (impedia rich results).

## 2. O que foi implementado

### Arquitetura (2 → 34 URLs em clusters temáticos)

```
Home (pillar)
├── /solucoes/ (hub)
│   ├── /almofada-de-ar/          ├── /papel-colmeia/
│   ├── /cushion-film/            ├── /papel-kraft/
│   ├── /colmeia-plastica/        ├── /maquina-de-almofada-de-ar/
│   ├── /manta-de-protecao/       └── /maquina-de-papel/
├── /embalagem-de-protecao/ (guia-mãe da categoria)
│   ├── /preenchimento-de-caixas/ (void fill)
│   ├── /embalagem-para-ecommerce/    ├── /embalagem-industrial/
│   ├── /embalagem-sustentavel/       ├── /protecao-para-transporte/
│   ├── /automacao-de-embalagem/      ├── /plastico-bolha/
│   └── /substituto-do-plastico-bolha/
├── /comparativos/ (hub)
│   ├── almofada-de-ar-vs-plastico-bolha/   ├── papel-colmeia-vs-plastico-bolha/
│   ├── almofada-de-ar-vs-papel-colmeia/    ├── almofada-de-ar-vs-papel-kraft/
│   └── almofada-de-ar-vs-isopor/
├── /segmentos/ autopecas · eletronicos · moda-e-calcados · moveis-e-decoracao
├── /guias/ como-escolher · como-reduzir-avarias · custo-e-roi
└── /contato/ + 404.html
```

- **~40.000 palavras** de conteúdo único em PT-BR (zero duplicação — títulos, descriptions e corpo verificados programaticamente).
- Cobertura natural das keywords alvo em PT e EN: almofada de ar, air pillow, cushion film, void fill, honeycomb paper, paper cushion, protective packaging, embalagem sustentável, máquina de embalagem etc.
- Links internos densos e contextuais entre pilar ↔ cluster ↔ comparativos (mínimo 8–12 links internos por página + footer com 21 links).

### SEO técnico (todas as páginas)
- Title e meta description únicos e otimizados por intenção de busca.
- Canonical, `robots` com `max-image-preview:large`, Open Graph completo, Twitter Cards.
- JSON-LD validado em 100% das páginas: **WebSite, ProfessionalService (com endereço São Paulo/SP), LocalBusiness (contato), BreadcrumbList, WebPage/CollectionPage/Article, FAQPage (10 páginas+), Product (soluções), HowTo (guias), ContactPage**.
- Sitemap.xml automático com as 33 URLs indexáveis, lastmod e prioridades.
- Robots.txt com bloqueio de `/tools/` (arquivos-fonte).
- Breadcrumb visível + schema em todas as páginas internas.
- 404 personalizada com navegação de recuperação.
- Favicon SVG + webmanifest + theme-color.

### Performance / Core Web Vitals
- **Imagens: ~50 MB → ~2,5 MB** (25 imagens convertidas para WebP, redimensionadas para máx. 1200px, qualidade 78). Maior ganho de LCP possível.
- CSS e JS externalizados (`/assets/`) — cache compartilhado entre as 34 páginas.
- `loading="lazy"` em todas as imagens abaixo da dobra; `fetchpriority="high"` na imagem do hero; `width`/`height` em imagens (elimina CLS).
- JS com `defer` (sem bloqueio de renderização); fontes do sistema (zero webfont = zero FOUT/atraso).
- FAQ com `<details>/<summary>` nativos — funciona sem JS e é lido por crawlers.

### Semântica, acessibilidade e SEO para IA
- HTML5 semântico: `<main>`, `<nav aria-label>`, `<article>`, `<aside>`, hierarquia H1→H2→H3 única e correta em todas as páginas.
- Skip-link, `aria-current` em breadcrumbs, `alt` descritivo em 100% das imagens, labels ligados aos campos de formulário, foco visível.
- Conteúdo estruturado em perguntas e respostas diretas (FAQ visível + schema) — o formato preferido de AI Overviews, Gemini, ChatGPT e Perplexity.
- Definições no primeiro parágrafo de cada página ("X é...") — otimizado para featured snippets e citação por LLMs.

### Conversão
- CTA em 3 camadas em todas as páginas: nav (Solicitar Análise), hero (Análise Gratuita + WhatsApp) e CTA final (formulário + WhatsApp + email).
- WhatsApp flutuante em todas as páginas, com mensagem pré-preenchida contextual por página.
- Tracking de leads por origem/página (localStorage + campo `origem` no Web3Forms).
- Formulário de contato ampliado (segmentos novos: Moda, Móveis).

### Código e manutenção
- Sistema de build documentado (`tools/build.py` + `tools/pages/*.page` + `README.md`): criar nova página = 1 arquivo de conteúdo + 1 comando. O sitemap se regenera sozinho.
- Zero duplicação de template; correções de layout em um único CSS.

## 3. Conformidade com Google Search Essentials

- Nenhuma técnica black hat: sem keyword stuffing, sem texto oculto, sem doorway pages.
- Comparativos honestos que mostram onde cada material **perde** (inclusive os ofertados) — o padrão de "conteúdo útil" que o Google recompensa.
- Fase 1 sem páginas de marcas concorrentes (decisão conjunta): a demanda "alternativa ao plástico bolha / melhor embalagem" é capturada por comparativos genéricos, sem risco CONAR/marca.
- Sem avaliações ou notas falsas (nenhum AggregateRating fabricado).

## 4. Próximos passos recomendados (por prioridade)

1. **Google Search Console**: cadastrar a propriedade, enviar o sitemap e monitorar indexação das 33 URLs (primeiras 2–6 semanas são críticas).
2. **Google Business Profile**: criar perfil "Consultoria em embalagens" em São Paulo — ativa o pacote local e valida o LocalBusiness schema.
3. **Google Analytics 4** (ou Plausible): hoje o tracking é só localStorage; sem analytics não há como medir o funil.
4. **Fase 2 de conteúdo** (quando as páginas atuais indexarem): páginas de alternativas a marcas (Ranpak, Sealed Air etc.) com tom técnico-comparativo; mais comparativos (cushion vs foam, colmeia vs kraft); páginas por cidade se o atendimento presencial expandir.
5. **Backlinks / autoridade externa**: guest posts em portais de logística e e-commerce (Ecommerce Brasil, Mundo Logística), cadastros em diretórios B2B, LinkedIn com artigos apontando para os guias.
6. **Prova social real**: depoimentos de clientes com nome/empresa (permitem Review schema legítimo no futuro) e fotos reais da operação.
7. **Limpeza do repositório**: os PNG originais (~50 MB) não são mais referenciados — podem ser movidos para fora do repo para acelerar deploys.
8. **Cache headers**: GitHub Pages já aplica cache básico; se migrar para Cloudflare Pages (gratuito), ganha Brotli, HTTP/3 e cache configurável — nota Lighthouse ainda mais alta.
9. **Vídeo**: um vídeo de 60s do insuflador em operação na home (com VideoObject schema) aumenta tempo na página e chance de Google Discover.
10. **Atualização contínua**: revisar 2–3 páginas por mês (o `dateModified` do build sinaliza frescor) e expandir FAQs com perguntas reais dos leads.
