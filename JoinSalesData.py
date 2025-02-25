import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
import re

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Amazon S3
AmazonS3_node1740506049550 = glueContext.create_dynamic_frame.from_catalog(database="customerdata", table_name="sales_data_csv", transformation_ctx="AmazonS3_node1740506049550")

# Script generated for node Amazon S3
AmazonS3_node1740506048486 = glueContext.create_dynamic_frame.from_catalog(database="customerdata", table_name="customer_data_csv", transformation_ctx="AmazonS3_node1740506048486")

# Script generated for node Renamed keys for Join
RenamedkeysforJoin_node1740506149749 = ApplyMapping.apply(frame=AmazonS3_node1740506049550, mappings=[("invoice_no", "string", "right_invoice_no", "string"), ("customer_id", "string", "right_customer_id", "string"), ("category", "string", "right_category", "string"), ("quantity", "long", "right_quantity", "long"), ("price", "double", "right_price", "double"), ("invoice_date", "string", "right_invoice_date", "string"), ("shopping_mall", "string", "right_shopping_mall", "string")], transformation_ctx="RenamedkeysforJoin_node1740506149749")

# Script generated for node Join
Join_node1740506134672 = Join.apply(frame1=AmazonS3_node1740506048486, frame2=RenamedkeysforJoin_node1740506149749, keys1=["customer_id"], keys2=["right_customer_id"], transformation_ctx="Join_node1740506134672")

# Script generated for node Filter
Filter_node1740506796296 = Filter.apply(frame=Join_node1740506134672, f=lambda row: (row["right_price"] >= 900 and bool(re.match("Credit Card", row["payment_method"]))), transformation_ctx="Filter_node1740506796296")

# Script generated for node Select Fields
SelectFields_node1740507259244 = SelectFields.apply(frame=Filter_node1740506796296, paths=["customer_id", "right_price", "right_shopping_mall", "payment_method", "gender", "age", "right_quantity", "right_category"], transformation_ctx="SelectFields_node1740507259244")

# Script generated for node Rename Field
RenameField_node1740507536058 = RenameField.apply(frame=SelectFields_node1740507259244, old_name="right_price", new_name="price", transformation_ctx="RenameField_node1740507536058")

# Script generated for node Rename Field
RenameField_node1740507575219 = RenameField.apply(frame=RenameField_node1740507536058, old_name="right_shopping_mall", new_name="shopping_mall", transformation_ctx="RenameField_node1740507575219")

# Script generated for node Rename Field
RenameField_node1740507618579 = RenameField.apply(frame=RenameField_node1740507575219, old_name="right_quantity", new_name="quantity", transformation_ctx="RenameField_node1740507618579")

# Script generated for node Rename Field
RenameField_node1740507659324 = RenameField.apply(frame=RenameField_node1740507618579, old_name="right_category", new_name="category", transformation_ctx="RenameField_node1740507659324")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=RenameField_node1740507659324, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1740504256948", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1740507766419 = glueContext.getSink(path="s3://my-stock-data-bucket1/customersSales/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1740507766419")
AmazonS3_node1740507766419.setCatalogInfo(catalogDatabase="customerdata",catalogTableName="customersales")
AmazonS3_node1740507766419.setFormat("glueparquet", compression="snappy")
AmazonS3_node1740507766419.writeFrame(RenameField_node1740507659324)
job.commit()