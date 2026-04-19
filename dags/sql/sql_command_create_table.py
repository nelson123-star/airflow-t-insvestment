

def SQL_command1(db_name):
    return f"""
    CREATE TABLE IF NOT EXISTS {db_name}.transactions (
    transaction_id UInt64,
    user_id UInt32,
    amount Float64,
    currency Enum8('USD' = 1, 'EUR' = 2, 'RUB' = 3),
    transaction_date DateTime64(3),
    status LowCardinality(String),
    region FixedString(3)
    ) ENGINE = MergeTree()
    PARTITION BY toYYYYMM(transaction_date)
    ORDER BY (user_id, transaction_date);
"""

def SQL_command2(db_name):
    return f"""
CREATE TABLE IF NOT EXISTS {db_name}.server_logs (
    event_time DateTime64(3),
    user_agent String,
    ip_address IPv4,
    response_time Float32,
    error_code Nullable(Int16),
    tags Array(String),
    bytes_sent UInt64,
    user_id Nullable(UInt64)
) ENGINE = MergeTree()
ORDER BY (event_time, ip_address)
"""

def SQL_command3(db_name):
    return f"""
CREATE TABLE IF NOT EXISTS {db_name}.sales (
    sale_date Date,
    region LowCardinality(String),
    product_category LowCardinality(String),
    revenue Decimal(15,2),
    quantity UInt16,
    discount Float32,
    customer_segment Enum16('VIP' = 1, 'Premium' = 2, 'Standard' = 3)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(sale_date)
ORDER BY (region, sale_date)
"""

def SQL_command4(db_name):
    return f"""
CREATE TABLE IF NOT EXISTS {db_name}.metrics (
    timestamp DateTime64(3, 'UTC'),
    hostname LowCardinality(String),
    metrics Map(String, Float64),
    labels Nested (key String, value String),
    cpu_usage Float32,
    memory_usage UInt64
) ENGINE = MergeTree()
ORDER BY (hostname, timestamp)
"""

def SQL_command5(db_name):
    return f"""
CREATE TABLE IF NOT EXISTS {db_name}.users (
    user_uuid UUID,
    created_at DateTime64(3),
    email String,
    profile_data JSON,
    location Point,
    is_active UInt8,
    preferences Array(String),
    last_login DateTime64(3)
) ENGINE = MergeTree()
ORDER BY (created_at, user_uuid)
"""

def SQL_command6(db_name):
    return f"""
CREATE TABLE IF NOT EXISTS {db_name}.custom_data_new (
    country String,
    month String,
    code UInt64,
    value Float64,
    netto Float64,
    quantity UInt64,
    region UInt64,
    district UInt64,
    direction Enum8('IM' = 1, 'EX' = 2, 'ShT' = 3),
    measure LowCardinality(String),
    load_date DateTime64(3)
) ENGINE = MergeTree()
PARTITION BY toYYYYMM(load_date)
ORDER BY (country, month, load_date)
"""