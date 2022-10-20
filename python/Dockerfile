FROM python:3.8.9-slim

WORKDIR /code


COPY requirements.txt ./
RUN apt update --yes
RUN apt-get install tk --yes
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 50051

COPY . .
CMD [ "python", "blog_server.py" ]