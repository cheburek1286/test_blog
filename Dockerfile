FROM python:3.6-alpine

RUN adduser -D test_blog

WORKDIR /home/test_blog

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY main.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP main.py

RUN chown -R test_blog:test_blog ./
USER test_blog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]