FROM python:3.6-alpine
COPY . /app
WORKDIR /app
RUN chmod +x sayhello.sh
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev build-base dos2unix
RUN pip3 install --upgrade pip setuptools wheel && pip3 install setuptools
RUN pip install -r requirements.txt
#ENTRYPOINT ["python"]
#CMD ["sayhello.sh", "app.py"]



ENTRYPOINT ["bash", "sayhello.sh"]