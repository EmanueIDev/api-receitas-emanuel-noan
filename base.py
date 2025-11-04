from http import HTTPStatus
import re
from fastapi import FastAPI, HTTPException, status
from typing import List
from schema import ReceitaBase, Receita, BaseUsuario, UsuarioPublic, Usuario, Usuario, BaseUsuario, UsuarioPublic

usuarios: List[Usuario] = []

app = FastAPI(title="API Livro de Receitas")

receitas: List[Receita] = []
usuarios: List[Usuario] = []
proximo_id = 1
proximo_id_usuario = 1

# ======================================================
# FUNÇÕES AUXILIARES
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

def obter_usuario_por_id(id: int):
    for usuario in usuarios:
        if usuario.id == id:
            return usuario
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=f"Usuário com id {id} não encontrado."
    )

def validar_senha(senha: str) -> str:
    if not senha:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="A senha não pode estar vazia.")
    
    if not re.search(r"[A-Za-z]", senha):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="A senha deve conter pelo menos uma letra.")
    
    if not re.search(r"[0-9]", senha):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="A senha deve conter pelo menos um número.")
    
    return senha
    



# ======================================================
# ROTAS
# ======================================================

@app.get("/")
def retorno():
    return {"title": "Livro de Receitas"}


@app.get("/receitas", response_model=List[Receita], status_code=HTTPStatus.OK)
def get_todas_receitas():
    return receitas


@app.get("/receitas/nome/{nome_receita}", response_model=Receita)
def get_receita_por_nome(nome_receita: str):
    return obter_receita_por_nome(nome_receita)


@app.get("/receitas/id/{id_receita}", response_model=Receita)
def get_receita_por_id(id_receita: int):
    return obter_receita_por_id(id_receita)


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


@app.put("/receitas/{id}", response_model=Receita, status_code=HTTPStatus.OK)
def update_receita(id: int, dados: ReceitaBase):
    receita_existente = obter_receita_por_id(id)

    nome = validar_nome(dados.nome)
    ingredientes = validar_ingredientes(dados.ingredientes)
    modo_de_preparo = validar_modo_de_preparo(dados.modo_de_preparo)

    # Verifica duplicidade de nome em outras receitas
    for r in receitas:
        if r.id != id and r.nome.lower() == nome.lower():
            raise HTTPException(status_code=400, detail="Já existe outra receita com esse nome.")

    receita_atualizada = Receita(
        id=id,
        nome=nome,
        ingredientes=ingredientes,
        modo_de_preparo=modo_de_preparo
    )

    index = receitas.index(receita_existente)
    receitas[index] = receita_atualizada
    return receita_atualizada


@app.delete("/receitas/{id}", status_code=HTTPStatus.OK)
def deletar_receita(id: int):
    if not receitas:
        raise HTTPException(status_code=404, detail="Não há receitas para excluir.")

    for i, receita in enumerate(receitas):
        if receita.id == id:
            receita_removida = receitas.pop(i)
            return {
                "mensagem": f"Receita '{receita_removida.nome}' foi excluída com sucesso.",
                "receita_excluida": receita_removida
            }

    raise HTTPException(status_code=404, detail="Receita não encontrada.")


@app.post("/usuarios", status_code=HTTPStatus.CREATED, response_model=UsuarioPublic)
def create_usuario(dados: BaseUsuario):
    """
    Cria um novo usuário.
    Valida se o email já existe e se os dados estão corretos.
    """
    global proximo_id_usuario

    nome_usuario = validar_nome_usuario(dados.nome_usuario)
    email = validar_email(dados.email)
    senha = validar_senha(dados.senha)


    if email_existe(email):
        raise HTTPException(status_code=400, detail="Já existe um usuário com esse email.")

    novo_usuario = Usuario(
        id=proximo_id_usuario,
        nome_usuario = nome_usuario,
        email=email,
        senha = senha
    )

    usuarios.append(novo_usuario)
    proximo_id_usuario += 1
    return novo_usuario

@app.get("/usuarios", response_model=List[UsuarioPublic], status_code=HTTPStatus.OK)
def get_todos_usuarios():
    if not usuarios:
        raise HTTPException(status_code=404, detail="Não há usuários cadastrados.")
    return usuarios


@app.get("/usuarios/nome/{nome_usuario}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_nome(nome_usuario: str):
    for u in usuarios:
        if u.nome_usuario.lower() == nome_usuario.lower():
            return u
    raise HTTPException(status_code=404, detail="Usuário não encontrado.")

@app.get("/usuarios/id/{id_usuario}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def get_usuario_por_id(id_usuario: int):
    for r in usuarios:
        if r.id == id_usuario:
            return r
    raise HTTPException(status_code=404, detail="Usuario não encontrado.")


@app.put("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def update_usuario(id: int, dados: BaseUsuario):
    usuario_existente = obter_usuario_por_id(id)

    # Validações (seguindo a mesma ideia das receitas)
    nome_usuario = validar_nome_usuario(dados.nome_usuario)
    email = validar_email(dados.email)
    senha = validar_senha(dados.senha)

    # Verifica duplicidade de e-mail em outros usuários
    for u in usuarios:
        if u.id != id and u.email.lower() == email.lower():
            raise HTTPException(status_code=400, detail="Já existe outro usuário com esse e-mail.")

    usuario_atualizado = UsuarioPublic(
        id=id,
        nome_usuario = nome_usuario,
        email=email,
        senha = senha
    )

    # Atualiza o registro na lista (ou base de dados em memória)
    index = usuarios.index(usuario_existente)
    usuarios[index] = usuario_atualizado

    return usuario_atualizado

@app.delete("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def delete_usuario(id: int):
    if not usuarios:
        raise HTTPException(status_code=404, detail="Não há usuários para excluir.")
    
    for i, usuario in enumerate(usuarios):
        if usuario.id == id:
            usuario_removido = usuarios.pop(i)
            return usuario_removido

    raise HTTPException(status_code=404, detail="Usuário não encontrado.")