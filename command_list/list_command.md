echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

Эта команда создает файл .env для настройки Apache Airflow в Docker-среде. Она записывает UID текущего пользователя и GID=0 (root) как переменные окружения.

Разбор команды
echo -e выводит текст с интерпретацией escape-последовательностей (здесь \n для новой строки).

"AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" формирует две строки:

AIRFLOW_UID=число — ID текущего пользователя (подстановкой $(id -u)).

AIRFLOW_GID=0 — группа root для прав доступа.

> .env перезаписывает (или создает) файл .env с этими переменными.


rm: cannot remove clickhouse/: Permission denied
sudo chown $USER:$USER ./clickhouse
rm -r ./clickhouse


docker-compose up airflow-init

копирование всего каталога в другой. Пример:
cp -r /home/ya_esteroot/airflow-docker/* /home/ya_esteroot/DE_projects/airflow-docker-2/

создать папку и перенести туда файлы. Пример:
cd DE_projects && mkdir airflow-docker-2 && cp -r /home/ya_esteroot/airflow-docker/* /home/ya_esteroot/DE_projects/airflow-docker-2/



cd DE_projects && mkdir airflow-docker-2 && cp -r /home/ya_esterootairflow-docker/* /home/ya_esteroot/DE_projects/airflow-docker-2/

mkdir airflow-t-insvestment && cp -r /home/ya_esteroot/DE_projects/airflow-docker-2/* /home/ya_esteroot/DE_projects/airflow-t-insvestment/



ssh-keygen -t ed25519 -C "vl301297@gmail.com"

Запуск SSH-агента и добавление ключа
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa