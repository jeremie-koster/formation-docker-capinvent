FROM --platform=linux/amd64 tensorflow/tensorflow:2.3.0

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
COPY src/app app/

WORKDIR /app

ENV DOCKER_VOLUME_PATH /examples/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]