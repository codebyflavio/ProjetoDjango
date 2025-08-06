// js/ui.js

export function aplicarPermissoes(usuario) {
  if (usuario.tipo === 'editor') {
    habilitarEdicao();
  } else {
    desabilitarEdicao();
  }
}

function habilitarEdicao() {
  document.querySelectorAll('[data-editavel]').forEach(el => {
    el.removeAttribute('disabled');
    el.classList.remove('modo-visualizacao');
  });
}

function desabilitarEdicao() {
  document.querySelectorAll('[data-editavel]').forEach(el => {
    el.setAttribute('disabled', true);
    el.classList.add('modo-visualizacao');
  });
}
