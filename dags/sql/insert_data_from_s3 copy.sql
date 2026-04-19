-- INSERT INTO clients (name, email, phone, address) VALUES
--         (
--         %(client_name)s, %(client_email)s, %(client_phone)s, %(client_address)s
--         );

-- insert into LVV.clients_data_stage 
-- select *
-- from s3('http://minio:9000/airflow-bucket/daily_export/bronze/2026-03-22.csv',
-- 'airflow_mc', 
-- 'airflow_mc', 
-- 'CSVWithNames',
-- 'ID UInt32,surname String,name String,patronymic String,city String,entry_date Date'
-- )

insert into %(db_name)s.%(table_name)s 
select *
from s3(%(s3_url_endpoint)s,
%(aws_public_key)s, 
%(aws_private_key)s, 
'CSVWithNames',
'ID UInt32,surname String,name String,patronymic String,city String,entry_date Date'
)