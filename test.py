from fastapi import FastAPI

from sqlalchemy import create_engine
from sqlalchemy.orm import session

from models import User, table_registry

app = FastAPI(title = 'API de teste')

engine = create_engine("sqlite:///:memory:", echo=False)

table_registry.metadata.create_all(engine)

with Session(engine) as session:
    noan = user(
        usuario = "noan", senha = "senha123", email = "noan@gmail.com"
    )
    session.add(noan)
    session.commit()
    session.refresh(noan)

print("DADOS DO USUARIO:", noan)
print("ID:", noan.id)
print("Criado em:", noan.created_at)    