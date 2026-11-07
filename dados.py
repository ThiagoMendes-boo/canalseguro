import json
import os
import random

# ---------- TEXTOS E OPÇÕES ----------
AVISO = (
    "PROTÓTIPO EDUCATIVO: nenhum relato é enviado para a polícia. "
    "Use apenas dados fictícios (nomes e telefones inventados). "
    "Em risco imediato, ligue 190. Apoio emocional: CVV 188."
)
TIPOS = [
    "Mensagens ofensivas ou humilhantes",
    "Ameaças",
    "Exposição de fotos, vídeos ou prints",
    "Perfil falso usado para me atacar",
    "Exclusão ou ataques em grupos",
]
PLATAFORMAS = ["WhatsApp", "Instagram", "TikTok", "Discord", "Jogo online", "Outra"]
LOCAIS = ["Escola", "Casa", "Internet / redes sociais", "Rua ou bairro", "Outro"]
STATUS = ["Recebido", "Em análise", "Encaminhado", "Concluído"]
PROVIDENCIAS = [
    "Nenhuma ainda",
    "Contato com a vítima",
    "Contato com a escola",
    "Encaminhado ao Conselho Tutelar",
    "Boletim de ocorrência registrado",
    "Investigação iniciada",
]

# ---------- ARQUIVO JSON (o "banco de dados") ----------
# O arquivo relatos.json fica na mesma pasta do app.
# Ele guarda uma lista de relatos. Exemplo de um relato dentro dele:
# {"protocolo": "CB-123456", "status": "Recebido", "cidade": "Campo Grande", ...}
ARQUIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "relatos.json")


def pegar_relatos():
    # Lê o arquivo JSON e devolve a lista de relatos
    if not os.path.exists(ARQUIVO):
        return []  # ainda não existe nenhum relato
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        return []  # arquivo vazio ou quebrado


def salvar_relatos(relatos):
    # Escreve a lista inteira de relatos no arquivo JSON
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(relatos, arquivo, ensure_ascii=False, indent=2)


# ---------- FUNÇÕES ÚTEIS ----------
def tem_dado_pessoal(texto):
    # Usada nos textos livres (relato e mensagens): procura "@" ou muitos números
    if "@" in texto:
        return True
    quantidade_de_numeros = 0
    for letra in texto:
        if letra.isdigit():
            quantidade_de_numeros += 1
    return quantidade_de_numeros >= 8


def telefone_valido(telefone):
    # Conta só os números: um telefone com DDD tem 10 ou 11
    quantidade_de_numeros = 0
    for letra in telefone:
        if letra.isdigit():
            quantidade_de_numeros += 1
    return quantidade_de_numeros == 10 or quantidade_de_numeros == 11


def nome_completo_valido(nome):
    # Precisa ter pelo menos duas palavras (nome e sobrenome)
    return len(nome.split()) >= 2


def achar_relato(protocolo, relatos=None):
    # Se a lista não for informada, lê do arquivo
    if relatos is None:
        relatos = pegar_relatos()
    protocolo = protocolo.strip().upper()
    for relato in relatos:
        if relato["protocolo"] == protocolo:
            return relato
    return None


def criar_protocolo():
    # Gera um código como CB-482913 que ainda não existe
    while True:
        protocolo = "CB-" + str(random.randint(100000, 999999))
        if achar_relato(protocolo) is None:
            return protocolo


def relato_em_markdown(relato):
    # Monta um texto em Markdown (.md) com os dados de um relato
    if relato["prints"]:
        evidencias = "sim"
    else:
        evidencias = "não"
    if relato["risco"]:
        risco = "SIM"
    else:
        risco = "não"

    linhas = [
        "# Relato " + relato["protocolo"],
        "",
        "## Situação",
        "- **Status:** " + relato["status"],
        "- **Providência:** " + relato["providencia"],
        "- **Risco informado:** " + risco,
        "- **Atendido por:** " + (relato["agente"] or "ninguém ainda"),
        "- **Última atualização:** " + (relato["atualizado_em"] or "-"),
        "",
        "## Contato",
        "- **Nome:** " + relato["nome_completo"],
        "- **Telefone:** " + relato["telefone"],
        "",
        "## Ocorrência",
        "- **Tipo:** " + relato["tipo"],
        "- **Plataforma:** " + relato["plataforma"],
        "- **Quando:** " + relato["quando"],
        "- **Cidade:** " + relato["cidade"],
        "- **Local:** " + relato["local"],
        "- **Detalhe do local:** " + (relato["local_detalhe"] or "-"),
        "- **Evidências guardadas:** " + evidencias,
        "",
        "## Relato",
        relato["descricao"],
        "",
        "## Mensagem para a vítima",
        relato["resposta"] or "-",
        "",
        "## Observação interna",
        relato["observacao"] or "-",
    ]
    return "\n".join(linhas)
# ---------- GESTÃO DE UTILIZADORES / CADASTRO ----------
ARQUIVO_USUARIOS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "usuarios.json"
)


def pegar_usuarios():
    """Lê o ficheiro usuarios.json e devolve a lista de utilizadores cadastrados."""
    if not os.path.exists(ARQUIVO_USUARIOS):
        return []
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except json.JSONDecodeError:
        return []


def salvar_usuario(novo_usuario):
    """Adiciona um novo utilizador ao ficheiro usuarios.json."""
    usuarios = pegar_usuarios()
    usuarios.append(novo_usuario)
    with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as arquivo:
        json.dump(usuarios, arquivo, ensure_ascii=False, indent=2)


def buscar_usuario(email_ou_usuario):
    """Procura um utilizador registado pelo e-mail ou nome de utilizador."""
    termo = email_ou_usuario.strip().lower()
    for u in pegar_usuarios():
        if u.get("email", "").lower() == termo or u.get("usuario", "").lower() == termo:
            return u
    return None