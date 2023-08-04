FROM python:3.8-slim

WORKDIR /app

COPY main.py .
COPY dataset.csv .
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install Flask pandas scikit-learn

EXPOSE 8000

CMD ["python", "main.py"]

