from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

# Definição do modelo de Receita
class Receita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

# Instância da aplicação FastAPI
app = FastAPI(title="API Livro de Receitas")

# Lista de receitas (agora uma lista de instâncias de Receita)
'''
receitas = [
    Receita(
        nome="pipoca doce",
        ingredientes=["5 colheres(sopa) de oleo", "5 colheres(sopa) de milho para pipoca", "5 colheres(sopa) de açucar", "3 colheres(sopa) de agua", "1 colher(sopa) de chocolate em po"],
        modo_de_preparo="Em uma panela, adicione todos os ingredientes e misture delicadamente. Desligue o fogo quando o intervalo de tempo entre os estouros da pipoca diminuir."
    ),
    Receita(
        nome="Arroz de forno à parmegiana",
        ingredientes=["2 xícaras de arroz", "150g de margarina", "2 tabletes de caldo de galinha", "2 ovos", "3 colheres (sopa) de queijo ralado", "100 g de presunto picado", "100 g de mussarela picada", "1 colher de extrato de tomate", "3 tomates sem pele"],
        modo_de_preparo="Bata no liquidificador o extrato e os tomates, com um pouco de água e um tablete de caldo de galinha (dissolvido em um pouquinho de água quente). Cozinhe o arroz com 1 tablete de caldo e 4 xícaras de água por 15 minutos. Bata os ovos, o queijo ralado, o presunto, a mussarela e misture com o arroz. Coloque num refratário com o molho forrando a forma e cobrindo com ele."
    ),
    Receita(
        nome="torta de limao",
        ingredientes=["200 g de biscoito de maisena", "150g de margarina", "1 caixa de creme de leite (200 g)", "suco de 4 limões", "raspas de 2 limões", "3 ou 4 claras de ovo", "3 colheres (sopa) de açúcar", "raspas de 2 limões para decorar"],
        modo_de_preparo="Triture o biscoito de maisena em um liquidificador ou processador. Junte a margarina e bata mais um pouco. Despeje a massa em uma forma de fundo removível (27 cm de diâmetro). Com as mãos, espalhe os biscoitos triturados no fundo e nas laterais da forma, cobrindo toda área de maneira uniforme. Leve ao forno médio (180° C), preaquecido, por aproximadamente 10 minutos."
    ),
    Receita(
        nome="Mousse de Maracujá",
        ingredientes=["1 lata de leite condensado", "1 lata de creme de leite", "1 pacote de gelatina em pó sem sabor", "1 maracujá (polpa)", "1/2 xícara de água"],
        modo_de_preparo="Dissolva a gelatina conforme as instruções da embalagem, utilizando a água quente. No liquidificador, bata o leite condensado, o creme de leite, a gelatina dissolvida e a polpa do maracujá até ficar bem homogêneo. Despeje a mistura em taças individuais ou em uma tigela grande. Leve à geladeira por pelo menos 3 horas ou até que fique firme. Decore com polpa de maracujá antes de servir."
    ),
    Receita(
        nome="Lasanha de Carne Moída",
        ingredientes=["500g de carne moída", "1 pacote de massa de lasanha pré-cozida", "2 colheres (sopa) de azeite de oliva", "1 cebola média picada", "2 dentes de alho picados", "1 lata de molho de tomate", "1/2 xícara de água", "200g de queijo mussarela fatiado", "100g de presunto fatiado", "Sal e pimenta-do-reino a gosto", "Queijo parmesão ralado a gosto"],
        modo_de_preparo="Em uma panela, aqueça o azeite e refogue a cebola e o alho até dourarem. Adicione a carne moída e refogue até que fique bem dourada. Acrescente o molho de tomate e a água, e cozinhe por 10 minutos, temperando com sal e pimenta. Em uma assadeira, faça camadas alternadas de molho de carne, massa de lasanha, queijo mussarela e presunto. Repita as camadas até acabar os ingredientes, finalizando com molho de carne por cima. Cubra com queijo parmesão ralado e leve ao forno preaquecido a 180°C por cerca de 30 minutos. Sirva quente."
    ),
    Receita(
        nome="Limonada",
        ingredientes=["4 limões", "1 litro de água", "1/2 xícara de açúcar", "Cubos de gelo a gosto"],
        modo_de_preparo="Esprema os limões, retirando todo o suco, ou utilize uma centrífuga. Em um jarro, misture o suco de limão, a água e o açúcar até dissolver completamente. Adicione cubos de gelo a gosto e misture. Sirva imediatamente, decorando com fatias de limão, se desejar."
    )
]
'''

receitas: List[Receita] = []

# Função para retornar o título da API
@app.get("/")
def retorno():
    return {"title": "Livro de Receitas"}

# Função para retornar todas as receitas
@app.get("/receitas")
def get_todas_receitas():
    return receitas

# Função para retornar uma receita específica
@app.get("/receitas/{receita}")
def receita(receita: str):
    for r in receitas:
        if r.nome.lower() == receita.lower():
            return r
    raise HTTPException(status_code=404, detail="Receita não encontrada")

# Função para criar uma nova receita
@app.post("/receitas", response_model=Receita, status_code=status.HTTP_201_CREATED)
def criar_receita(dados: Receita):

    for receita in receitas:
        if receita['nome'].lower() == dados.lower():
            return {"Receita já existente."}
        else:
            receitas.append(dados)
            return dados
