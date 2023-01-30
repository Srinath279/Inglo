FROM python:3.9

ADD requirements.txt .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

WORKDIR /backend

# CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "15400"]

CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app
