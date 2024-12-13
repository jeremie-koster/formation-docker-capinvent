FROM tensorflow/tensorflow:2.18.0

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
COPY ./src/ /app

WORKDIR /app

ENV DOCKER_VOLUME_PATH="/examples"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]