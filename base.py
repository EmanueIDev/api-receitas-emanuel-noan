from fastapi import FastAPI

app = FastAPI(title="API")

receitas = {
    "pipoca doce": {
        'nome': 'Pipoca Doce',
        'ingredientes': [
            '5 colheres(sopa) de óleo',
            '5 colheres(sopa) de milho para pipoca',
            '5 colheres(sopa) de açúcar',
            '3 colheres(sopa) de água',
            '1 colher(sopa) de chocolate em pó'
        ],
        'utensilios': ['panela', 'bowl', 'espátula', 'pipoqueira'],
        'modo de preparo': [
            'Em uma panela, adicione todos os ingredientes e misture delicadamente.',
            'Desligue o fogo quando o intervalo de tempo entre os estouros da pipoca diminuir.'
        ]
    },
    "arroz de forno à parmegiana": {
        'nome': 'Arroz de Forno à Parmegiana',
        'ingredientes': [
            '2 xícaras de arroz',
            '150g de margarina',
            '2 tabletes de caldo de galinha',
            '2 ovos',
            '3 colheres (sopa) de queijo ralado',
            '100 g de presunto picado',
            '100 g de mussarela picada',
            '1 colher de extrato de tomate',
            '3 tomates sem pele'
        ],
        'utensilios': ['Panela', 'Assadeira', 'Colher de pau', 'Faca', 'Tábua de corte', 'Ralador', 'Tigela', 'Colher de sopa'],
        'modo de preparo': [
            'Bata no liquidificador o extrato e os tomates, com um pouco de água e um tablete de caldo de galinha.',
            'Cozinhe o arroz com 1 tablete de caldo e 4 xícaras de água por 15 minutos.',
            'Bata os ovos, o queijo ralado, o presunto, a mussarela e misture com o arroz.',
            'Coloque num refratário com o molho forrando a forma e cobrindo com ele.'
        ]
    },
    "torta de limao": {
        'nome': 'Torta de Limão',
        'ingredientes': [
            '200 g de biscoito de maisena',
            '150g de margarina',
            '1 caixa de creme de leite (200 g)',
            'suco de 4 limões',
            'raspas de 2 limões',
            '3 ou 4 claras de ovo',
            '3 colheres (sopa) de açúcar',
            'raspas de 2 limões para decorar'
        ],
        'utensilios': ['Assadeira', 'Liquidificador', 'Fouet', 'Colher para sobremesa'],
        'modo de preparo': [
            'Triture o biscoito no liquidificador ou processador.',
            'Junte a margarina e bata mais um pouco.',
            'Despeje em forma removível e espalhe com as mãos.',
            'Leve ao forno preaquecido (180° C) por 10 minutos.'
        ]
    },
    "mousse de maracujá": {
        "nome": "Mousse de Maracujá",
        "ingredientes": [
            "1 lata de leite condensado",
            "1 lata de creme de leite",
            "1 pacote de gelatina em pó sem sabor",
            "1 maracujá (polpa)",
            "1/2 xícara de água"
        ],
        "utensilios": ["Liquidificador", "Panela", "Tigela", "Colher de sopa"],
        "modo de preparo": [
            "Dissolva a gelatina conforme instruções da embalagem.",
            "No liquidificador, bata todos os ingredientes.",
            "Despeje em taças e leve à geladeira por 3 horas.",
            "Decore com polpa antes de servir."
        ]
    },
    "lasanha de carne moída": {
        "nome": "Lasanha de Carne Moída",
        "ingredientes": [
            "500g de carne moída",
            "1 pacote de massa de lasanha pré-cozida",
            "2 colheres (sopa) de azeite",
            "1 cebola média picada",
            "2 dentes de alho picados",
            "1 lata de molho de tomate",
            "1/2 xícara de água",
            "200g de queijo mussarela",
            "100g de presunto",
            "Sal e pimenta a gosto",
            "Queijo parmesão ralado"
        ],
        "utensilios": ["Panela", "Frigideira", "Assadeira", "Colher de pau", "Faca", "Tábua de corte"],
        "modo de preparo": [
            "Refogue cebola e alho no azeite.",
            "Adicione carne moída, depois o molho, cozinhe 10 min.",
            "Monte a lasanha em camadas e leve ao forno 30 min."
        ]
    },
    "limonada": {
        "nome": "Limonada",
        "ingredientes": [
            "4 limões",
            "1 litro de água",
            "1/2 xícara de açúcar",
            "Cubos de gelo"
        ],
        "utensilios": ["Espremedor", "Jarro", "Colher"],
        "modo de preparo": [
            "Esprema os limões.",
            "Misture com água e açúcar até dissolver.",
            "Adicione gelo e sirva."
        ]
    }
}


@app.get("/")
def home():
    return {"title": "Livro de Receitas"}


@app.get("/receitas")
def listar_receitas():
    return {"receitas": list(receitas.keys())}


@app.get("/receitas/{nome_receita}")
def obter_receita(nome_receita: str):
    receita = receitas.get(nome_receita.lower())
    if receita:
        return receita
    return {"erro": "Receita não existente"}
