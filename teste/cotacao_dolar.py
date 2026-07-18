import json
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL"


def buscar_cotacao_dolar() -> dict:
    requisicao = Request(
        API_URL,
        headers={"User-Agent": "cotacao-dolar/1.0"},
    )

    with urlopen(requisicao, timeout=10) as resposta:
        dados = json.load(resposta)

    return dados["USDBRL"]


def main() -> None:
    try:
        cotacao = buscar_cotacao_dolar()
        valor = float(cotacao["bid"])
        atualizado_em = datetime.fromtimestamp(int(cotacao["timestamp"]))

        print(f"A cotação do dolar hoje é essa: R$ {valor:.2f}")
        print(f"Atualizada em: {atualizado_em:%d/%m/%Y %H:%M:%S}")
    except (HTTPError, URLError, TimeoutError) as erro:
        print(f"Nao foi possivel consultar a cotacao: {erro}")
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as erro:
        print(f"A API retornou uma resposta inesperada: {erro}")


if __name__ == "__main__":
    main()
