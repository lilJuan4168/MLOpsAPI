FROM ubuntu:latest
WORKDIR /Project
RUN apt update
RUN apt upgrade -y
RUN apt install python3-pip -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]