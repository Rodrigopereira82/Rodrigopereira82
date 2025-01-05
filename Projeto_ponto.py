from datetime import datetime
import json
from dataclasses import dataclass, asdict

TIPO_PONTO = {
    0: "Entrada",
    1: "Saida"
}


class Colaborador:
    def __init__(self, nome, sobrenome):
        self.nome = str.capitalize(nome)
        self.sobrenome = str.capitalize(sobrenome)

    def nome_completo(self):
        return f"Colaborador: {self.nome} {self.sobrenome}"


class Ponto:
    def __init__(self, tipo_ponto):
        self.tipo_ponto = int(tipo_ponto)
        if self.tipo_ponto not in TIPO_PONTO:
            raise ValueError(
                "Favor digitar os valores 0 (entrada) ou 1 (saida)...")


@dataclass
class DadosPonto:
    nome: str
    sobrenome: str
    tipo_ponto: str
    data_hora_ponto: datetime


def registrar_ponto(nome, sobrenome, tipo_ponto):
    colaborador = Colaborador(nome=nome, sobrenome=sobrenome)
    ponto = Ponto(tipo_ponto=tipo_ponto)
    data_hora_ponto = datetime.now()

    dados_ponto = DadosPonto(
        nome=colaborador.nome,
        sobrenome=colaborador.sobrenome,
        tipo_ponto=TIPO_PONTO[ponto.tipo_ponto],
        data_hora_ponto=data_hora_ponto
    )

    return asdict(dados_ponto)


def lambda_handler(event, context):
    try:
        nome = event.get('nome')
        sobrenome = event.get('sobrenome')
        tipo_ponto = event.get('tipo_ponto')

        if nome is None or sobrenome is None or tipo_ponto is None:
            raise ValueError(
                "Atenção! Os parâmetros 'nome', 'sobrenome' e 'tipo_ponto' são de preenchimento obrigatórios.")

        resultado = registrar_ponto(nome, sobrenome, tipo_ponto)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Ponto registrado com sucesso!',
                'data': resultado
            }, default=str)
        }
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Erro de valor inválido.',
                'error': str(e)
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Erro interno do servidor.',
                'error': str(e)
            })
        }
