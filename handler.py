import json
import boto3
import time

CLUSTER_NAME='redshift-cluster-1'
DATABASE_NAME='json_database'
DB_USER='awsuser'

sql="COPY public.users FROM 's3://s3-backet-redshift/test_2022-04-04-16-24-56.json' " + \
        "iam_role 'arn:aws:iam::009554248005:role/RedshiftAccessS3' " + \
        "FORMAT AS JSON 'auto' " + \
        "REGION AS 'ap-northeast-1';"

client = boto3.client('redshift-data')

def lambda_handler(event, context):
    result = client.execute_statement(
        ClusterIdentifier=CLUSTER_NAME,
        Database=DATABASE_NAME,
        DbUser=DB_USER,
        Sql=sql,
    )
    
    # 実行IDを取得
    id = result['Id']
    # クエリが終わるのを待つフラグ
    statement = ''
    status = ''
    while status != 'FINISHED' and status != 'FAILED' and status != 'ABORTED':
        statement = client.describe_statement(Id=id)
        status = statement['Status']
        print("Status:", status)
        time.sleep(1)
    # 失敗している
    print("Status:", status)
    
    # try:
    #     statement = client.get_statement_result(Id=id)
    #     print(json.dumps(statement, indent=4, default=str))
    # except Exception as e:
    #     print(e)