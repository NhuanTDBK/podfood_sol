import argparse


def main(
    order_path: str, 
    product_path: str,
    output_file_path: str,
):
    from pyspark.sql import SparkSession

    spark = (
        SparkSession.builder.appName("ETL Data Pipeline")
        .getOrCreate()
    )

    df_order = spark.read.csv(order_path)
    df_product = spark.read.csv(product_path)

    df_order.createOrReplaceTempView("order")
    df_product.createOrReplaceTempView("product")

    spark.sql("""
        select *
        from order join product using (product_id)
    """).write.csv(output_file_path)

    spark.stop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Utility to convert a file from a type to another"
    )

    parser.add_argument("--order-path", help="Output folder path, can use gs://format")
    parser.add_argument("--product-path", help="Output folder path, can use gs://format")
    parser.add_argument("--output-path", help="Output folder path, can use gs://format")


    args = parser.parse_args()

    output_file_path = args.output_path
    order_path = args.order_path
    product_path = args.product_path

    main(
        order_path,
        product_path,
        output_file_path,
    )

    # print("Write to {}".format(output_file_path))
