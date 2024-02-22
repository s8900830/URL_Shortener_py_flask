FROM python:3

WORKDIR /usr/src/app

COPY requirement.txt ./
RUN pip install --no-cache-dir -r requirement.txt

COPY . .

CMD [ "python", "./URL_Short/app.py" ]