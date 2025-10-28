from pydantic import BaseModel, Field
from typing import List, Annotated

class ReceitaBase(BaseModel):
    nome: Annotated[str, Field(min_length=2, max_length=50)]
    ingredientes: Annotated[list[str], Field(min_items=1, max_items=20)]
    modo_de_preparo: str

class Receita(ReceitaBase):
    id: int

class Usuario(BaseModel):
    id: int
    nome_usuario: str
    email: str
    senha: str

class BaseUsuario(BaseModel):
    nome_usuario: str
    email: str
    senha: str

class UsuarioPublic(BaseModel):
    id: int
    nome_usuario: str
    email: str      