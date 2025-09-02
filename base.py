from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

# Modelo base agora com tudo em uma lista só
class ReceitaBase(BaseModel):
    nome: str
    ingredientes: List[str]  # Inclui ingredientes + modo de preparo como strings

class Receita(ReceitaBase):
    id: int

# Instância da aplicação
app = FastAPI(title="API Livro de Receitas")

receitas: List[Receita] = []
proximo_id = 1

@app.get("/")
def retorno():
    return {"title": "Livro de Receitas"}

@app.get("/receitas", response_model=List[Receita])
def get_todas_receitas():
    return receitas

@app.get("/receitas/nome/{nome_receita}", response_model=Receita)
def get_receita_por_nome(nome_receita: str):
    for r in receitas:
        if r.nome.lower() == nome_receita.lower():
            return r
    raise HTTPException(status_code=404, detail="Receita não encontrada")

@app.post("/receitas", response_model=Receita, status_code=status.HTTP_201_CREATED)
def criar_receita(dados: ReceitaBase):
    global proximo_id
    for receita in receitas:
        if receita.nome.lower() == dados.nome.lower():
            raise HTTPException(status_code=400, detail="Receita já existente.")
    nova_receita = Receita(
        id=proximo_id,
        nome=dados.nome,
        ingredientes=dados.ingredientes
    )
    receitas.append(nova_receita)
    proximo_id += 1
    return nova_receita
