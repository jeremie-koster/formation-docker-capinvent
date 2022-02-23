FROM python:3.7

COPY requirements.txt tmp/requirements.txt
RUN python -m pip install --upgrade pip
RUN python3 -m pip install -r tmp/requirements.txt
COPY /app /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]