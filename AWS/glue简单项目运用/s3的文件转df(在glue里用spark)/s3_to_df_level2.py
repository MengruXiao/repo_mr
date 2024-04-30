from pyspark.sql import SparkSession
from pyspark.sql import DataFrame


def get_df_from_s3(spark, file_format, source_path, **kwargs):
    is_header = True
    delimiter = ","
    escape = "\\"
    file_format = file_format.lower()
    lz_df: DataFrame
    if file_format in ['csv', 'txt']:
        lz_df = spark.read.csv(source_path, header=is_header, sep=delimiter, escape=escape)
    else:
        local_logger.error(f"Invalid source file format found: {file_format}")
        raise Exception("Undefined file format")

    return lz_df


spark = SparkSession.builder.getOrCreate()

lz_df = get_df_from_s3(spark, 'csv', 's3://ph-cdp-landing-pre-dev-cn-north-1/enriched_em/merge_target/20240312144854/')
lz_df.show()

# 怎么把处理好的df再放到raw下面呢






