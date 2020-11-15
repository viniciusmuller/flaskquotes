FROM python:alpine

# Downloading dependencies
COPY src /src
COPY requirements.txt /src/requirements.txt 
RUN pip install -r /src/requirements.txt

# Running the application
WORKDIR /src
ENTRYPOINT ["flask", "run"]
EXPOSE 5000
