FROM python:3.9

COPY . .

ADD initialize_db.sql /docker-entrypoint-initdb.d

RUN pip install -r requirements.txt

ARG username
ENV sql_user $username

ARG password
ENV sql_pwd $password

EXPOSE 3306
EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "aspen_capital_war.py" ]