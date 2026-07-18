FROM apache/airflow:2.10.5

# RUN PYTHON_VERSION=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')") \
#     && pip install --no-cache-dir "apache-airflow-providers-microsoft-mssql" \
#        --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.5/constraints-${PYTHON_VERSION}.txt"

RUN PYTHON_VERSION=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')") \
      && pip install --no-cache-dir "apache-airflow-providers-microsoft-mssql" \
         --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.5/constraints-${PYTHON_VERSION}.txt" \
      && pip install --no-cache-dir pysftp