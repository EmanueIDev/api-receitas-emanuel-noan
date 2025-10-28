from http import HTTPStatus
from fastapi import FastAPI, HTTPException, status
from typing import List
from schema import ReceitaBase, Receita, BaseUsuario, UsuarioPublic, Usuario

app = FastAPI(title="API Livro de Receitas")

receitas: List[Receita] = []
usuarios: List[Usuario] = []
proximo_id = 1
proximo_id_usuario = 1

# ======================================================
# FUNÇÕES AUXILIARES - RECEITAS
# ======================================================

def receita_existe(nome: str) -> bool:
    """Verifica se já existe uma receita com o mesmo nome."""
    return any(receita.nome.lower() == nome.lower() for receita in receitas)

def validar_nome(nome: str) -> str:
    """Valida o nome da receita."""
    nome = nome.strip()
    if not nome:
        raise HTTPException(status_code=400, detail="O nome da receita não pode ser vazio.")
    if not (2 <= len(nome) <= 50):
        raise HTTPException(status_code=400, detail="O nome da receita deve ter entre 2 e 50 caracteres.")
    return nome

def validar_ingredientes(ingredientes: List[str]) -> List[str]:
    """Valida a lista de ingredientes."""
    if not ingredientes:
        raise HTTPException(status_code=400, detail="A receita deve ter pelo menos 1 ingrediente.")
    if len(ingredientes) > 20:
        raise HTTPException(status_code=400, detail="A receita não pode ter mais de 20 ingredientes.")
    if any(ing.strip() == "" for ing in ingredientes):
        raise HTTPException(status_code=400, detail="Nenhum ingrediente pode estar vazio.")
    return [ing.strip() for ing in ingredientes]

def validar_modo_de_preparo(modo_de_preparo: str) -> str:
    """Valida o modo de preparo."""
    modo_de_preparo = modo_de_preparo.strip()
    if not modo_de_preparo:
        raise HTTPException(status_code=400, detail="O modo de preparo não pode ser vazio.")
    return modo_de_preparo

def obter_receita_por_id(id_receita: int) -> Receita:
    """Retorna a receita pelo ID ou lança exceção."""
    for r in receitas:
        if r.id == id_receita:
            return r
    raise HTTPException(status_code=404, detail="Receita não encontrada.")

def obter_receita_por_nome(nome_receita: str) -> Receita:
    """Retorna a receita pelo nome ou lança exceção."""
    for r in receitas:
        if r.nome.lower() == nome_receita.lower():
            return r
    raise HTTPException(status_code=404, detail="Receita não encontrada.")


# ======================================================
# FUNÇÕES AUXILIARES - USUÁRIOS
# ======================================================

def email_existe(email: str) -> bool:
    """Verifica se já existe um usuário com o mesmo email."""
    return any(usuario.email.lower() == email.lower() for usuario in usuarios)

def validar_nome_usuario(nome: str) -> str:
    """Valida o nome do usuário."""
    nome = nome.strip()
    if not nome:
        raise HTTPException(status_code=400, detail="O nome do usuário não pode ser vazio.")
    if not (2 <= len(nome) <= 50):
        raise HTTPException(status_code=400, detail="O nome do usuário deve ter entre 2 e 50 caracteres.")
    return nome

def validar_email(email: str) -> str:
    """Valida o email do usuário."""
    email = email.strip().lower()
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Email inválido.")
    return email


# ======================================================
# ROTAS
# ======================================================

@app.get("/")
def retorno():
    return {"title": "Livro de Receitas"}

@app.post("/receitas", response_model=Receita, status_code=status.HTTP_201_CREATED)
def criar_receita(dados: ReceitaBase):
    global proximo_id

    if receita_existe(dados.nome):
        raise HTTPException(status_code=400, detail="Já existe uma receita com esse nome.")

    nome = validar_nome(dados.nome)
    ingredientes = validar_ingredientes(dados.ingredientes)
    modo_de_preparo = validar_modo_de_preparo(dados.modo_de_preparo)

    nova_receita = Receita(
        id=proximo_id,
        nome=nome,
        ingredientes=ingredientes,
        modo_de_preparo=modo_de_preparo
    )

    receitas.append(nova_receita)
    proximo_id += 1
    return nova_receita


# ======================================================
# ROTA DE CRIAÇÃO DE USUÁRIOS
# ======================================================

@app.post("/usuarios", status_code=HTTPStatus.CREATED, response_model=UsuarioPublic)
def create_usuario(dados: BaseUsuario):
    """
    Cria um novo usuário.
    Valida se o email já existe e se os dados estão corretos.
    """
    global proximo_id_usuario

    nome = validar_nome_usuario(dados.nome)
    email = validar_email(dados.email)

    if email_existe(email):
        raise HTTPException(status_code=400, detail="Já existe um usuário com esse email.")

    novo_usuario = Usuario(
        id=proximo_id_usuario,
        nome=nome,
        email=email
    )

    usuarios.append(novo_usuario)
    proximo_id_usuario += 1
    return novo_usuario




  





