FROM python:3

WORKDIR /usr/src/app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./send.py", "-f", "tcp://*:14639", "-n", "tcp://myhost:14641" ]
