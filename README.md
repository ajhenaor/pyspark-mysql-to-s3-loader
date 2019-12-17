# Project specification
The aim of this project is providing an easy way to load data from a MySQL database to AWS S3. Basically, the idea is that loading data should easy as providing a MySQL connection, a SQL query to select the data, and the S3 bucket information where the data should be stored. To do that, in this project a Python script is specified. The script can be run by launching a the docker image that is specified in the Dockerfile of this project.

### Input parameters
The script expects as environment variables next parameters

| Name  | Description  |
|---|---|
| AWS_ACCESS_KEY_ID | AWS role access key |
| AWS_SECRET_ACCESS_KEY | AWS secret access key|
| host | IP address where MySQL DB is located |
| user | User to connect to MySQL DB|
| port | Port through where MySQL DB can be accessed|
| password | Password to access MySQL DB |
| dbname | DB name|
| bucket_name | S3 bucket where data is going to be loaded |
| prefix | S3 Bucket prefix where data is going to be loaded |
| table | DB table to loaded|
| query | Query to select data from MySQL table |
| columnTypes | YAML file where data column types are specified |
