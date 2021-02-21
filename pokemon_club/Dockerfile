# Use Python37
FROM python:3.7

# Copy requirements.txt to the docker image and install packages
COPY requirements.txt /

RUN pip install -r requirements.txt

# Set the WORKDIR to be the folder
COPY . /app

# Expose port 5000
EXPOSE 5000
ENV PORT 5000
WORKDIR /app

# Nebula Graph
ENV NG_GCP_PROPJECT_ID=
ENV NG_GCP_PASSWORD_SECRET_ID=
ENV NG_GCP_USER_SECRET_ID=
ENV NG_GCP_CREDENTIAL_VERSION "latest"
ENV NG_ENDPOINTS "127.0.0.1:9669,"
ENV NG_MAX_CONN_POOL_SIZE 10

# Use gunicorn as the entrypoint
CMD exec gunicorn --bind :$PORT main:app --workers 1 --threads 1 --timeout 60
