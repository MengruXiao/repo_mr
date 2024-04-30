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

    elif file_format == 'parquet':
        lz_df = spark.read.parquet(source_path)

    elif file_format == 'xml':
        lz_df = spark.read.format('com.databricks.spark.xml').options(rowTag=row_tag).load(source_path)

    elif file_format == 'json':
        lz_df = spark.read.json(source_path)
        dtypes_tp = lz_df.dtypes[0]
        if dtypes_tp[1][:5] == 'array':
            lz_df = lz_df.withColumn("nest", explode(dtypes_tp[0])).select("nest.*")
        elif dtypes_tp[1] == "string":
            for col in lz_df.dtypes:
                col_name = col[0]
                if col[1][:5] in ('struc', 'array'):
                    lz_df = lz_df.withColumn(col_name, to_json(col_name))
        else:
            raise Exception("Currently not support such structure")

    elif file_format.lower() == 'xlsx' or 'xlsm' or 'xls' or 'xlsb':
        s3_source_excel_transfer(lz_folder=source_path,
                                 sheet_name=sheet_name,
                                 ext=file_format,
                                 skip_row=skip_row,
                                 use_cols=use_cols,
                                 excel_dtypes=excel_dtypes
                                 )
        source_path = source_path if source_path.endswith("/") else source_path + "/"
        lz_df = spark.read.csv(source_path + "sheet/", header=is_header,  sep="\1", quote="\2", lineSep="\3")

    else:
        local_logger.error(f"Invalid source file format found: {file_format}")
        raise Exception("Undefined file format")

    return lz_df
