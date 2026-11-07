# 🛡️ Canal Seguro

Protótipo educativo de um canal para **relatar casos de cyberbullying** e acompanhar o andamento deles, feito com Python e [Streamlit](https://streamlit.io).

> ⚠️ **Projeto de demonstração.** Nenhum relato é enviado para a polícia ou para qualquer órgão real. Use **apenas dados fictícios** (nomes e telefones inventados).
> Em risco imediato, ligue **190**. Apoio emocional: **CVV 188**.

---

## O que o app faz

O app tem três perfis de uso:

| Perfil | O que faz |
|---|---|
| **Vítima** | Entra com nome completo, telefone, cidade e aceite de uso dos dados. Faz relatos e consulta o andamento pelo protocolo. |
| **Anônimo** | Entra sem informar nenhum dado pessoal. Faz relatos e acompanha o caso só pelo protocolo. |
| **Autoridade** | Entra com usuário, senha e identificação do agente (nome, matrícula e unidade). Vê os relatos, atualiza o status, registra providências e responde à vítima. |

### Principais recursos

- Tela de início com explicação do fluxo e contadores animados (relatos recebidos e casos concluídos).
- Formulário de relato com tipo de ocorrência, plataforma, data, cidade, local, indicação de risco e evidências.
- **Protocolo** gerado automaticamente (ex.: `CB-482913`), que pode ser copiado com um clique.
- Acompanhamento do caso pela vítima: status, providência, agente responsável e mensagem de orientação.
- Painel da autoridade com cartões de prioridade (casos com risco ficam em destaque), observação interna e registro de quem atendeu e quando.
- Download de cada relato em **Markdown** (`.md`).
- Validação de dados: nome completo, telefone com DDD e bloqueio de e-mail, telefone ou CPF nos textos livres.

---

## Como rodar

### 1. Requisitos

- Python 3.9 ou mais novo
- Streamlit 1.30 ou mais novo

### 2. Instalar

No terminal (PowerShell), dentro da pasta do projeto:

```powershell
C:\Python313\python.exe -m pip install streamlit
```

Ou, usando o arquivo `requirements.txt`:

```powershell
C:\Python313\python.exe -m pip install -r requirements.txt
```

### 3. Executar

```powershell
cd C:\Users\Unigran\Desktop\hackton2
C:\Python313\python.exe -m streamlit run app.py
```

O navegador abre em `http://localhost:8501`.

> Aplicativos Streamlit **não** rodam com `python app.py`. Use sempre `streamlit run`.

### Acesso de demonstração da autoridade

| Campo | Valor |
|---|---|
| Usuário | `policia` |
| Senha | `demo123` |
| Nome do agente, matrícula e unidade | qualquer valor fictício (matrícula com 4 ou mais caracteres) |

---

## Estrutura do projeto

```
hackton2/
├── app.py          # Arquivo principal: decide qual tela mostrar
├── login.py        # Tela de entrada (abas Vítima, Anônimo e Autoridade)
├── inicio.py       # Tela de início (cartões e contadores)
├── vitima.py       # Fazer relato e consultar protocolo
├── autoridade.py   # Painel da autoridade
├── dados.py        # Textos, opções, leitura/gravação do JSON e validações
├── layout.py       # Funções que montam o visual e ligam o CSS e o JavaScript
├── estilo.css      # Visual do app (cores, cartões, abas, botões)
├── script.js       # Animações e botão de copiar protocolo
├── requirements.txt
└── relatos.json    # Criado automaticamente ao enviar o primeiro relato
```

### Como as partes se conectam

- `app.py` liga o estilo e o script, lê o perfil guardado em `st.session_state` e chama a tela certa.
- `login.py` mostra `inicio.py` e as três abas de entrada. Ao entrar, grava o perfil e os dados em `st.session_state`.
- `vitima.py` e `autoridade.py` leem e gravam os relatos pelas funções do `dados.py`.
- `layout.py` lê o `estilo.css` (colocado em uma tag `<style>`) e o `script.js`, que roda em um iframe invisível, porque o Streamlit bloqueia `<script>` dentro do `st.markdown`.

---

## Como os dados são guardados

Os relatos ficam em um arquivo **`relatos.json`**, na mesma pasta do app. Cada relato é um dicionário com campos como:

```json
{
  "protocolo": "CB-482913",
  "status": "Recebido",
  "providencia": "Nenhuma ainda",
  "nome_completo": "Maria de Teste",
  "telefone": "(67) 91234-5678",
  "cidade": "Campo Grande",
  "local": "Escola",
  "tipo": "Ameaças",
  "plataforma": "WhatsApp",
  "quando": "07/11/2026",
  "risco": false,
  "prints": true,
  "descricao": "Texto do relato...",
  "resposta": "",
  "observacao": "",
  "agente": "",
  "atualizado_em": ""
}
```

Status possíveis: `Recebido`, `Em análise`, `Encaminhado` e `Concluído`.

---

## Personalização rápida

- **Cores do app:** edite o bloco `:root` no começo do `estilo.css` (`--acento`, `--acento-2`, `--ciano`).
- **Tipos de ocorrência, plataformas, locais, status e providências:** edite as listas no início do `dados.py`.
- **Acesso de demonstração da autoridade:** edite `USUARIO_DEMO` e `SENHA_DEMO` no `login.py`.

---

## Limitações (é um protótipo)

- **Login de demonstração:** usuário e senha ficam escritos no código. Não há verificação real de identidade.
- **Dados em arquivo JSON:** não há criptografia, controle de acesso nem backup. Duas pessoas gravando ao mesmo tempo podem sobrescrever uma à outra.
- **Dados pessoais:** o `relatos.json` guarda nome e telefone. Mesmo no protótipo, use só dados inventados e não envie esse arquivo para repositórios públicos (adicione `relatos.json` ao `.gitignore`).
- **Sem envio real:** nada é encaminhado a nenhum órgão.
- **Visual:** parte dos estilos usa seletores internos do Streamlit, que podem mudar entre versões. A fonte Inter vem do Google Fonts e precisa de internet.

### Para virar um sistema real

- Autenticação segura e senhas guardadas com hash.
- Banco de dados com criptografia e controle de acesso por perfil.
- Adequação à **LGPD**, com atenção especial a dados de menores de idade (consentimento do responsável, retenção e exclusão).
- Integração oficial com os órgãos de proteção, feita com as instituições envolvidas.

---

## Ideias para evoluir

- Filtros no painel por cidade, status e prioridade.
- Exportar todos os relatos em planilha.
- Modo escuro com botão no topo.
- Gráficos de relatos por tipo e plataforma.

---

## Equipe

Preencha com os nomes do time, a instituição e o evento (hackathon).
