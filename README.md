# Project specification
The aim of this project is based on the concept that loading data into a data lake or a data warehouse should be achieved by simply providing some information related to the data source and to the place where the data is going to be stored. Particularly, in our case from MySQL databases to AWS S3. To do that, in this project a Python script implementing such functionality is written. The script is a Docker image that can be built by using the Dockerfile of this project.

### Input parameters
The script expects as environment variables next parameters

| Name  | Description  |
|---|---|
| exec_date | Date of the execution. This parameter is added as a new column in the data extracted in order use it as a control field of where data is uploaded |
| date_to_work | Origin date of data, e.g., you may be running the script on the 2019-12-01, but the data may be originated the 2019-06-01. So, this date should be specified in order to overwrite data on AWS S3 |
| host | IP address where MySQL DB is located |
| user | User to connect to MySQL DB|
| port | Port through where MySQL DB can be accessed|
| password | Password to access MySQL DB |
| dbname | DB name|
| table | DB table to loaded|
| query | Query to select data from MySQL table |
| columnTypes | YAML file where data column types are specified |
| AWS_ACCESS_KEY_ID | AWS role access key |
| AWS_SECRET_ACCESS_KEY | AWS secret access key|
| bucket_name | S3 bucket where data is going to be loaded |
| prefix | S3 Bucket prefix where data is going to be loaded |
