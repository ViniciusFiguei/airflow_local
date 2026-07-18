import json
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


MOEDAS = {
    "USD": "dolar",
    "GTQ": "quetzal da Guatemala",
    "MXN": "peso mexicano",
    "AUD": "dólar australiano",
}
API_URL = "https://open.er-api.com/v6/latest/BRL"


def buscar_cotacoes() -> dict:
    requisicao = Request(
        API_URL,
        headers={"User-Agent": "cotacoes-moedas/1.0"},
    )

    with urlopen(requisicao, timeout=10) as resposta:
        return json.load(resposta)


def main() -> None:
    try:
        dados = buscar_cotacoes()
        taxas = dados["rates"]
        atualizado_em = datetime.fromtimestamp(int(dados["time_last_update_unix"]))

        for codigo, nome in MOEDAS.items():
            valor = 1 / float(taxas[codigo])

            print(f"A cotação do {nome} hoje é essa: R$ {valor:.4f}")

        print(f"Atualizada em: {atualizado_em:%d/%m/%Y %H:%M:%S}")
        print("Fonte: https://www.exchangerate-api.com")
    except (HTTPError, URLError, TimeoutError) as erro:
        print(f"Nao foi possivel consultar a cotacao: {erro}")
    except (KeyError, TypeError, ValueError, ZeroDivisionError, json.JSONDecodeError) as erro:
        print(f"A API retornou uma resposta inesperada: {erro}")


if __name__ == "__main__":
    main()
