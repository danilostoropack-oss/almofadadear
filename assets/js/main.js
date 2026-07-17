/* ============================================================
   Almofada de Ar — Script global
   Modal de análise, tracking de leads e abas de segmento.
   Carregado com defer em todas as páginas.
   ============================================================ */
(function () {
  'use strict';

  /* ── Modal de análise ── */
  var modalBg = document.getElementById('modalBg');

  window.openModal = function (src) {
    if (!modalBg) return;
    modalBg.classList.add('open');
    var form = document.getElementById('modalForm');
    var ok = document.getElementById('modalSuccess');
    if (form) form.style.display = 'block';
    if (ok) ok.style.display = 'none';
    document.body.style.overflow = 'hidden';
    window._modalSrc = src || 'modal';
  };

  window.closeModal = function () {
    if (!modalBg) return;
    modalBg.classList.remove('open');
    document.body.style.overflow = '';
  };

  if (modalBg) {
    modalBg.addEventListener('click', function (e) {
      if (e.target === modalBg) window.closeModal();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') window.closeModal();
    });
  }

  /* Chave do Web3Forms vinculada a contato@almofadadear.com.br */
  var WEB3FORMS_ACCESS_KEY = '3075a4a3-c792-4660-92a0-2b755495375e';

  window.submitModal = function () {
    var nome = (document.getElementById('mNome') || {}).value || '';
    var phone = (document.getElementById('mPhone') || {}).value || '';
    nome = nome.trim(); phone = phone.trim();
    if (!nome || !phone) { alert('Preencha Nome e WhatsApp.'); return; }
    var empresa = ((document.getElementById('mEmpresa') || {}).value || '').trim();
    var segmento = (document.getElementById('mSegmento') || {}).value || '';
    var msg = ((document.getElementById('mMsg') || {}).value || '').trim();
    var texto = 'Olá! Quero uma análise gratuita da minha operação de embalagem.\n' +
      'Nome: ' + nome + '\nContato: ' + phone +
      (empresa ? '\nEmpresa: ' + empresa : '') +
      (segmento ? '\nSegmento: ' + segmento : '') +
      (msg ? '\nDetalhes: ' + msg : '');

    if (WEB3FORMS_ACCESS_KEY) {
      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
        body: JSON.stringify({
          access_key: WEB3FORMS_ACCESS_KEY,
          subject: 'Nova solicitação de diagnóstico — ' + nome,
          from_name: 'Site Almofada de Ar',
          to: 'contato@almofadadear.com.br',
          nome: nome,
          empresa: empresa || '-',
          whatsapp: phone,
          segmento: segmento || '-',
          mensagem: msg || '-',
          origem: (window._modalSrc || 'modal') + ' | ' + location.pathname
        })
      }).catch(function () { /* WhatsApp cobre o envio */ });
    }

    window.open('https://wa.me/5511963073163?text=' + encodeURIComponent(texto), '_blank');
    var form = document.getElementById('modalForm');
    var ok = document.getElementById('modalSuccess');
    if (form) form.style.display = 'none';
    if (ok) ok.style.display = 'block';
    setTimeout(window.closeModal, 3000);
  };

  /* ── Lead tracking (localStorage) ── */
  function trackLead(source) {
    try {
      var leads = JSON.parse(localStorage.getItem('almofada_leads') || '[]');
      leads.push({ ts: new Date().toISOString(), source: source, page: location.pathname });
      localStorage.setItem('almofada_leads', JSON.stringify(leads));
    } catch (e) { /* noop */ }
  }
  var waFloat = document.querySelector('.wa-float');
  if (waFloat) waFloat.addEventListener('click', function () { trackLead('wa-float'); });
  document.querySelectorAll('[data-track]').forEach(function (el) {
    el.addEventListener('click', function () { trackLead(el.getAttribute('data-track')); });
  });

  /* ── Abas de segmento (home) ── */
  var tabs = document.getElementById('segTabs');
  var mosaic = document.getElementById('aplicMosaic');
  if (tabs && mosaic) {
    tabs.addEventListener('click', function (e) {
      var btn = e.target.closest('.seg-tab');
      if (!btn) return;
      var seg = btn.dataset.seg;
      tabs.querySelectorAll('.seg-tab').forEach(function (t) { t.classList.remove('active'); });
      btn.classList.add('active');
      mosaic.querySelectorAll('.aplic-photo').forEach(function (card) {
        card.classList.toggle('visible', seg === 'todos' || card.dataset.seg === seg);
        card.classList.remove('aplic-tall');
      });
      var first = mosaic.querySelector('.aplic-photo.visible');
      if (first) first.classList.add('aplic-tall');
    });
  }
})();
