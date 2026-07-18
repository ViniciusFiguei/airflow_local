import json
import logging
from datetime import timedelta
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import pendulum
from airflow.decorators import dag, task
from airflow.exceptions import AirflowException


API_URL = "https://open.er-api.com/v6/latest/BRL"
MOEDAS = {
    "USD": "dolar",
    "GTQ": "quetzal da Guatemala",
    "MXN": "peso mexicano",
    "AUD": "dólar australiano",
}
LOGGER = logging.getLogger(__name__)


def buscar_cotacoes() -> dict:
    requisicao = Request(
        API_URL,
        headers={"User-Agent": "cotacoes-moedas-airflow/1.0"},
    )

    with urlopen(requisicao, timeout=10) as resposta:
        return json.load(resposta)


@dag(
    dag_id="cotacoes_moedas",
    description="Consulta cotações de moedas em reais.",
    schedule="*/5 * * * *",
    start_date=pendulum.datetime(2026, 7, 17, tz="America/Sao_Paulo"),
    catchup=False,
    max_active_runs=1,
    default_args={
        "owner": "data",
        "retries": 2,
        "retry_delay": timedelta(minutes=1),
    },
    tags=["cotacoes", "moedas"],
)
def cotacoes_moedas():
    @task(task_id="consultar_cotacoes")
    def consultar_cotacoes() -> None:
        try:
            dados = buscar_cotacoes()
            if dados.get("result") != "success":
                raise ValueError(f"Resultado da API: {dados.get('result')}")

            taxas = dados["rates"]
            atualizado_em = pendulum.from_timestamp(
                int(dados["time_last_update_unix"]),
                tz="America/Sao_Paulo",
            )

            for codigo, nome in MOEDAS.items():
                valor = 1 / float(taxas[codigo])
                LOGGER.info(
                    "A cotação do %s hoje é essa: R$ %.4f",
                    nome,
                    valor,
                )

            LOGGER.info(
                "Cotações atualizadas em: %s",
                atualizado_em.format("DD/MM/YYYY HH:mm:ss"),
            )
            LOGGER.info("Fonte: https://www.exchangerate-api.com")
        except (HTTPError, URLError, TimeoutError) as erro:
            raise AirflowException(
                f"Não foi possível consultar as cotações: {erro}"
            ) from erro
        except (
            KeyError,
            TypeError,
            ValueError,
            ZeroDivisionError,
            json.JSONDecodeError,
        ) as erro:
            raise AirflowException(
                f"A API retornou uma resposta inesperada: {erro}"
            ) from erro

    consultar_cotacoes()


dag = cotacoes_moedas()
