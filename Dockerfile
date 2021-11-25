FROM python:alpine
WORKDIR /app
COPY requirements.text requirements.text
RUN pip3 install -r requirements.text
COPY . .
ENV FLASK_APP=app/PttStockAPI.py
EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]