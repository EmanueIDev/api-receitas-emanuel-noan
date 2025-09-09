from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Annotated

class ReceitaBase(BaseModel):
    nome: Annotated[str, Field(min_length=2, max_length=50)]
    ingredientes: Annotated[list[str], Field(min_items=1, max_items=20)]
    modo_de_preparo: str

class Receita(ReceitaBase):
    id: int

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

@app.get("/receitas/id/{id_receita}", response_model=Receita)
def get_receita_por_id(id_receita: int):
    for r in receitas:
        if r.id == id_receita:
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
        ingredientes=dados.ingredientes,
        modo_de_preparo=dados.modo_de_preparo
    )

    receitas.append(nova_receita)
    proximo_id += 1

    return nova_receita

@app.put("/receitas/{id}", response_model=Receita)
def update_receita(id: int, dados: ReceitaBase):
    if dados.nome.strip() == "" or dados.modo_de_preparo.strip() == "":
        raise HTTPException(
            status_code=400, detail="Nome e modo de preparo não podem ser vazios."
        )

    if any(ingrediente.strip() == "" for ingrediente in dados.ingredientes):
        raise HTTPException(
            status_code=400, detail="Nenhum ingrediente pode estar vazio."
        )

    if not (2 <= len(dados.nome.strip()) <= 50):
        raise HTTPException(
            status_code=400,
            detail="O nome da receita deve ter entre 2 e 50 caracteres.",
        )

    if not (1 <= len(dados.ingredientes) <= 20):
        raise HTTPException(
            status_code=400,
            detail="A receita deve ter entre 1 e 20 ingredientes.",
        )

    for i in range(len(receitas)):
        if receitas[i].id == id:
            for r in receitas:
                if r.id != id and r.nome.lower() == dados.nome.lower():
                    raise HTTPException(
                        status_code=400,
                        detail="Já existe uma receita com esse nome.",
                    )
                
            receita_atualizada = Receita(
                id=id,
                nome=dados.nome.strip(),
                ingredientes=[ing.strip() for ing in dados.ingredientes],
                modo_de_preparo=dados.modo_de_preparo.strip(),
            )

            receitas[i] = receita_atualizada
            return receita_atualizada

    raise HTTPException(status_code=404, detail="Receita não encontrada.")



