FROM apache/airflow:3.1.6

# ✅ 1. Копируем только requirements (кэшируется)
COPY --chown=airflow:root requirements.txt /requirements.txt

USER airflow

# ✅ 2. Multi-stage оптимизация pip + фиксация airflow
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir apache-airflow==3.1.6 -r /requirements.txt && \
    pip install t-tech-investments --index-url https://opensource.tbank.ru/api/v4/projects/238/packages/pypi/simple && \

    # Команда pip cache purge полностью удаляет все накопленные файлы кэша
    # , скачанные pip при установке Python-пакетов. Это безопасная операция, которая освобождает место на диске
    # , удаляя временные файлы, сохраненные для ускорения повторных установок.
    pip cache purge




# FROM apache/airflow:3.1.6

# COPY --chown=airflow:root requirements.txt /requirements.txt

# # 2. Устанавливаем зависимости
# USER airflow

# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt


# FROM apache/airflow:3.1.6

# # COPY --chown=airflow:root requirements.txt /requirements.txt
# # COPY requirements.txt /requirements.txt

# # COPY requirements.txt /

# COPY --chown=airflow:root requirements.txt /requirements.txt

# # 2. Устанавливаем зависимости
# USER airflow

# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt


# FROM apache/airflow:3.1.6

# RUN pip3 install --upgrade pip && \
#     pip3 install --no-cache-dir \
#     apache-airflow==3.1.6 \
#     -r /requirements.txt


# RUN pip3 install --upgrade pip && \
#     pip3 install --no-cache-dir \
#     apache-airflow==3.1.6 \
#     clickhouse-connect \
#     apache-airflow-providers-postgres