from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

# Modelo base
class ReceitaBase(BaseModel):
    nome: constr(min_length=2, max_length=50)
    ingredientes: List[str]
    modo_de_preparo: str

# Modelo com ID
class Receita(ReceitaBase):
    id: int

# Instância da aplicação
app = FastAPI(title="API Livro de Receitas")

# Banco de dados em memória
receitas: List[Receita] = []
proximo_id = 1

# Página inicial
@app.get("/")
def retorno():
    return {"title": "Livro de Receitas"}

# Buscar todas as receitas
@app.get("/receitas", response_model=List[Receita])
def get_todas_receitas():
    return receitas

# Buscar por nome
@app.get("/receitas/nome/{nome_receita}", response_model=Receita)
def get_receita_por_nome(nome_receita: str):
    for r in receitas:
        if r.nome.lower() == nome_receita.lower():
            return r
    raise HTTPException(status_code=404, detail="Receita não encontrada")

# Buscar por ID (corrigido)
@app.get("/receitas/id/{id_receita}", response_model=Receita)
def get_receita_por_id(id_receita: int):
    for r in receitas:
        if r.id == id_receita:
            return r
    raise HTTPException(status_code=404, detail="Receita não encontrada")

# Criar nova receita
@app.post("/receitas", response_model=Receita, status_code=status.HTTP_201_CREATED)
def criar_receita(dados: ReceitaBase):
    global proximo_id

    for receita in receitas:
        if receita.nome.lower() == dados.nome.lower():
            raise HTTPException(status_code=400, detail="Receita já existente.")

    nova_receita = Receita(
        id=proximo_id,
        nome=dados.nome,
        ingredientes=dados.ingredientes,
        modo_de_preparo=dados.modo_de_preparo
    )

    receitas.append(nova_receita)
    proximo_id += 1

    return nova_receita
