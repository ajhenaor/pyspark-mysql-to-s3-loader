FROM ubuntu:latest
LABEL maintainer="aj"

# Install OpenJDK 8
RUN \
  apt-get update && \
  apt-get install -y openjdk-8-jdk && \
  rm -rf /var/lib/apt/lists/*

# Install Python
RUN \
    apt-get update && \
    apt-get install -y python3 python3-dev python3-pip python-virtualenv && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .

# Define default command
CMD ["python3", "pyspark-mysql-to-s3-loader.py"]
