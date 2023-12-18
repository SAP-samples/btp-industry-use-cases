FROM python:3.9-slim-bookworm

RUN pip install --no-cache-dir "flask<3" "pillow<11" "numpy<2" tflite-runtime~=2.13.0 pandas==2.1.1 requests keras==2.14.0 numpy==1.26.1 scikit_learn==1.3.2 tensorflow==2.14.0

COPY app /app
EXPOSE 80
WORKDIR /app

CMD python -u app.py
