import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

from sedona.spark import *

sedona = SedonaContext.create(spark)

sedona.sql("SELECT ST_POINT(1., 2.) as geom").show()

job = Job(glueContext)
job.init(args['JOB_NAME'], args)
job.commit()