from pyspark.sql import SparkSession
from pyspark.sql import DataFrame


def get_df_from_s3(spark, file_format, source_path, **kwargs):
    """
    using spark_read to get dataframe object from source file
    :param spark:  sparkSession object
    :param file_format: source file format eg: csv xlsx parquet...
    :param source_path: source file s3 path
    :param kwargs: configurations params like header, row_tag..
    :return: dataframe
    """
    # read data from lz
    is_header = False if not kwargs.get("is_header") else True if kwargs.get("is_header").upper() == 'TRUE' else False
    sheet_name = 0 if kwargs.get("sheet_name") is None else kwargs.get("sheet_name")
    row_tag = kwargs.get("row_tag")
    skip_row = kwargs.get("skip_row")
    use_cols = kwargs.get("use_cols")
    excel_dtypes = kwargs.get("excel_dtypes")
    delimiter = "," if kwargs.get("delimiter") is None else \
        kwargs.get("delimiter").encode("utf-8").decode("unicode_escape")
    escape = "\\" if kwargs.get("escape") is None else \
        kwargs.get("escape").encode("utf-8").decode("unicode_escape")
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






