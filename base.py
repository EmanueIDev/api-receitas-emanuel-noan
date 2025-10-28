from http import HTTPStatus
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Annotated
from schema import ReceitaBase, Receita, Usuario, BaseUsuario, UsuarioPublic

usuarios: List[Usuario] = []

app = FastAPI(title="API Livro de Receitas")

receitas: List[Receita] = []
proximo_id = 1

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
  





