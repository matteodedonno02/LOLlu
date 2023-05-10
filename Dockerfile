FROM python:3.10.7

WORKDIR /LOLlu

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]