def insert_data1_transactions(db_name: str) -> str:
    """Заполнение transactions 10k строк"""
    return f"""
INSERT INTO {db_name}.transactions 
SELECT 
    number AS transaction_id,
    number % 1000 AS user_id,
    randUniform(100, 10000) / 100 AS amount,
    multiIf(rand() % 3 = 0, 'USD', rand() % 2 = 0, 'EUR', 'RUB') AS currency,
    now64() - toIntervalDay(rand64() % 365) AS transaction_date,
    arrayElement(['success', 'pending', 'failed'], rand() % 3) AS status,
    multiIf(rand() % 3 = 0, 'USA', rand() % 2 = 0, 'EU', 'RUS') AS region
FROM numbers(10000);
"""

def insert_data2_server_logs(db_name: str) -> str:
    """Заполнение server_logs 10k строк"""
    return f"""
INSERT INTO {db_name}.server_logs 
SELECT 
    now64() - toIntervalSecond(rand64() % 86400) AS event_time,
    concat('Mozilla/5.0 (agent_', toString(rand() % 100), ')') AS user_agent,
    IPv4NumToString(rand64() % (2^32)) AS ip_address,
    randUniform(50, 5000) / 100 AS response_time,
    toInt16OrNull(if(rand() % 10 = 0, NULL, rand() % 500)) AS error_code,
    arrayJoin(['web', 'api', 'db']) || ['debug', 'info', 'error'][rand() % 3] AS tags,
    randUniform(1024, 1048576) AS bytes_sent,
    toUInt64OrNull(if(rand() % 5 = 0, NULL, rand() % 10000)) AS user_id
FROM numbers(10000);
"""

def insert_data3_sales(db_name: str) -> str:
    """Заполнение sales 10k строк"""
    return f"""
INSERT INTO {db_name}.sales 
SELECT 
    today() - toIntervalDay(rand() % 365) AS sale_date,
    multiIf(rand() % 4 = 0, 'Moscow', 1, 'SPb', 2, 'Novosibirsk', 'Kazan') AS region,
    arrayElement(['Electronics', 'Clothes', 'Books', 'Food'], rand() % 4) AS product_category,
    (randUniform(1000, 100000) / 100)::Decimal(15,2) AS revenue,
    randUniform(1, 100)::UInt16 AS quantity,
    randUniform(0, 50) / 100 AS discount,
    multiIf(rand() % 3 = 0, 'VIP', 1, 'Premium', 'Standard') AS customer_segment
FROM numbers(10000);
"""

def insert_data4_metrics(db_name: str) -> str:
    """Заполнение metrics 10k строк"""
    return f"""
INSERT INTO {db_name}.metrics 
SELECT 
    now64() - toIntervalMinute(rand64() % 1440) AS timestamp,
    concat('server_', toString(rand() % 10)) AS hostname,
    map('cpu', randUniform(0,100), 'mem', randUniform(0,100), 'disk', randUniform(0,100)) AS metrics,
    ['env', 'version'] AS labels_key,
    ['prod', '1.0'] AS labels_value,
    randUniform(0, 100) AS cpu_usage,
    randUniform(1024, 32768) AS memory_usage
FROM numbers(10000);
"""

def insert_data5_users(db_name: str) -> str:
    """Заполнение users 10k строк"""
    return f"""
INSERT INTO {db_name}.users 
SELECT 
    generateUUIDv4() AS user_uuid,
    now64() - toIntervalDay(rand64() % 730) AS created_at,
    concat('user', number, '@example.com') AS email,
    toJSONString(map('name', concat('User', number), 'age', randUniform(18,80))) AS profile_data,
    [randUniform(55, 60), randUniform(37, 38)] AS location,
    rand() % 2 AS is_active,
    arrayJoin(['music', 'sport', 'books', 'games']) AS preferences,
    now64() - toIntervalHour(rand64() % 24) AS last_login
FROM numbers(10000);
"""

def insert_data6_custom_data(db_name: str) -> str:
    """Заполнение custom_data_new 10k строк (TM1 стиль)"""
    return f"""
INSERT INTO {db_name}.custom_data_new 
SELECT 
    multiIf(rand() % 3 = 0, 'IT', 1, 'RU', 'US') AS country,
    concat('янв.', toString(rand() % 24 + 1)) AS month,
    randUniform(1000000, 9999999) AS code,
    randUniform(1000, 100000) AS value,
    randUniform(100, 1000) AS netto,
    randUniform(1, 100) AS quantity,
    randUniform(10000, 99999) AS region,
    randUniform(1, 1000) AS district,
    multiIf(rand() % 2 = 0, 'IM', 'EX') AS direction,
    concat('measure_', toString(rand() % 5)) AS measure,
    now64() - toIntervalDay(rand64() % 30) AS load_date
FROM numbers(10000);
"""

# Список всех INSERT команд
INSERT_COMMANDS = [
    insert_data1_transactions,
    insert_data2_server_logs,
    insert_data3_sales,
    insert_data4_metrics,
    insert_data5_users,
    insert_data6_custom_data
]
