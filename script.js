// ========== CANAL SEGURO: script.js ==========
// O Streamlit não deixa rodar JavaScript direto no st.markdown.
// Por isso o layout.py coloca este arquivo em um iframe invisível,
// e aqui usamos "window.parent" para mexer na página principal.

(function () {
  const pai = window.parent;
  const doc = pai.document;

  // 1) Faz os elementos com a classe "revelar" aparecerem um depois do outro
  function revelar() {
    const itens = doc.querySelectorAll(".revelar:not(.visivel)");
    itens.forEach(function (el, i) {
      setTimeout(function () {
        el.classList.add("visivel");
      }, i * 120);
    });
  }

  // 2) Faz os números com a classe "contador" subirem de 0 até o valor
  function contar() {
    const itens = doc.querySelectorAll(".contador:not(.contado)");
    itens.forEach(function (el) {
      el.classList.add("contado");
      const alvo = parseInt(el.textContent, 10) || 0;
      if (alvo === 0) return;

      let atual = 0;
      const passo = Math.max(1, Math.ceil(alvo / 30));
      el.textContent = "0";
      const timer = setInterval(function () {
        atual = Math.min(alvo, atual + passo);
        el.textContent = atual;
        if (atual >= alvo) clearInterval(timer);
      }, 40);
    });
  }

  // 3) Copia o texto para a área de transferência
  function copiar(texto) {
    if (pai.navigator.clipboard) {
      pai.navigator.clipboard.writeText(texto).catch(function () {
        copiarPlanoB(texto);
      });
    } else {
      copiarPlanoB(texto);
    }
  }

  function copiarPlanoB(texto) {
    const caixa = doc.createElement("textarea");
    caixa.value = texto;
    doc.body.appendChild(caixa);
    caixa.select();
    doc.execCommand("copy");
    doc.body.removeChild(caixa);
  }

  // 4) Clicar no protocolo copia o código
  function aoClicar(evento) {
    const caixa = evento.target.closest(".protocolo");
    if (!caixa) return;
    copiar(caixa.textContent.trim());
    caixa.classList.add("copiado");
    setTimeout(function () {
      caixa.classList.remove("copiado");
    }, 1500);
  }

  // Remove o clique antigo (se a página recarregou o script) e coloca o novo
  if (pai.__canalCliqueAntigo) {
    doc.removeEventListener("click", pai.__canalCliqueAntigo);
  }
  pai.__canalCliqueAntigo = aoClicar;
  doc.addEventListener("click", aoClicar);

  // 5) A cada mudança na tela (o Streamlit redesenha tudo), roda de novo
  let esperando = false;
  function rodar() {
    if (esperando) return;
    esperando = true;
    setTimeout(function () {
      esperando = false;
      revelar();
      contar();
    }, 100);
  }

  if (pai.__canalObservadorAntigo) {
    pai.__canalObservadorAntigo.disconnect();
  }
  const observador = new pai.MutationObserver(rodar);
  observador.observe(doc.body, { childList: true, subtree: true });
  pai.__canalObservadorAntigo = observador;

  rodar(); // primeira vez
})();
