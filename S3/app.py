from utils.log import init_logger
from comply.sss import check_if_public

if __name__ == '__main__':
    logger = init_logger(__name__, testing_mode=False)
    logger.info('Checking for S3 buckets with public access')
    check_if_public()