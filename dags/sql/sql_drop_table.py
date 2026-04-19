def drop_all_tables(db_name: str) -> str:
    """Возвращает SQL команду DROP для всех 6 таблиц"""
    return f"""
-- Удаление таблиц из базы {db_name}
DROP TABLE IF EXISTS {db_name}.transactions;
DROP TABLE IF EXISTS {db_name}.server_logs; 
DROP TABLE IF EXISTS {db_name}.sales;
DROP TABLE IF EXISTS {db_name}.metrics;
DROP TABLE IF EXISTS {db_name}.users;
DROP TABLE IF EXISTS {db_name}.custom_data_new;
"""

# Одной строкой для выполнения
def drop_all_tables_single(db_name: str) -> str:
    """Один запрос DROP для всех таблиц"""
    return f"""
DROP TABLE IF EXISTS {db_name}.transactions, 
{db_name}.server_logs, 
{db_name}.sales, 
{db_name}.metrics, 
{db_name}.users, 
{db_name}.custom_data_new;
"""