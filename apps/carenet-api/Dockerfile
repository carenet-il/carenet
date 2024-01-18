FROM python:3.10-slim

WORKDIR /app

COPY apps/carenet-api/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY libs libs

COPY apps/carenet-api apps/carenet-api

EXPOSE 8000
# To download the models before running the app
RUN python3 apps/carenet-api/src/app.py

CMD ["python3", "apps/carenet-api/src/main.py"] 