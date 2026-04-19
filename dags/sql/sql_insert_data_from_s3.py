
# Одной строкой для выполнения
def insert_data_from_s3(
        db_name: str,
        table_name: str,
        s3_url_endpoint: str,
        aws_public_key: str,
        aws_private_key: str,
        ) -> str:
    """Вставка данных в таблицу из S3"""
    return f"""
insert into {db_name}.{table_name} 
select *
from s3('{s3_url_endpoint}',
'{aws_public_key}', 
'{aws_private_key}', 
'CSVWithNames',
'ID UInt32,surname String,name String,patronymic String,city String,entry_date Date'
);

"""