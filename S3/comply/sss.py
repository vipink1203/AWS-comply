import boto3
import botocore
from utils.log import init_logger
from prettytable import PrettyTable

logger = init_logger(__name__, testing_mode=False)

s3 = boto3.resource('s3')
public = []
denied = []
pubTable = PrettyTable()
deniedTable = PrettyTable()

def check_if_public():
    pubTable.field_names = ['Public_Buckets']
    deniedTable.field_names = ['Access_Denied']
    for bucket in s3.buckets.all():
        try: 
            for grant in s3.BucketAcl(bucket.name).grants:
                if grant['Grantee']['Type'] == 'Group' and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
                    buckStr = str(bucket)
                    public.append([buckStr.strip('s3/.Bucket').strip("(name='").strip("')")])      
        except botocore.exceptions.ClientError:
            buckStr = str(bucket)
            denied.append([buckStr.strip('s3/.Bucket').strip("(name='").strip("')")])  
    if len(public) != 0:
        logger.error('Found Public buckets')
        for i in public:
            pubTable.add_row(i)
        print(pubTable)
        
    if len(denied) != 0:
        logger.info('Found some buckets to which you do not have access.')
        for i in denied:
            deniedTable.add_row(i)
        print(deniedTable)
