FROM python:3
USER root

RUN apt -y update \
    && apt -y upgrade \
    && apt install -y python3 python3-dev python3-pip
RUN apt -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

RUN apt install -y vim less
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9

RUN pip install -U pip
RUN mkdir /code
 
ENV LANG ja_JP.utf8
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt

# コンテナのタイムゾーンがデフォルトでUTCになっているので、ホストOSの/etc/localtimeを読み込み専用でマウント
VOLUME /etc/localtime:/etc/localtime:ro


# そのままapt-getでインストールするとパスワードを聞かれる箇所で止まってしまうので、予め設定しておく。この例ではパスワードは「root」。
RUN echo "mysql-server mysql-server/root_password password root" | debconf-set-selections && \
    echo "mysql-server mysql-server/root_password_again password root" | debconf-set-selections && \
    apt-get -y install mysql-server


# my.cnfを編集
# bind-address行をコメントアウトして、外部から接続出来るようにする
RUN sed -i -e "s/^bind-address\s*=\s*\(.*\)/#bind-address = \1/" /etc/mysql/my.cnf

# デフォルトの文字コードをUTF-8に設定
RUN sed -i -e "s/\(\[mysqld\]\)/\1\ncharacter-set-server = utf8/g" /etc/mysql/my.cnf
RUN sed -i -e "s/\(\[client\]\)/\1\ndefault-character-set = utf8/g" /etc/mysql/my.cnf
RUN sed -i -e "s/\(\[mysqldump\]\)/\1\ndefault-character-set = utf8/g" /etc/mysql/my.cnf
RUN sed -i -e "s/\(\[mysql\]\)/\1\ndefault-character-set = utf8/g" /etc/mysql/my.cnf


# 一度MySQLサーバを起動し、外部から接続した際の権限を設定する。
# この場合は172.17.0.0/16から接続した際の権限。
RUN mysqld_safe & \
    sleep 10 && \
    echo "grant all on *.* to root@'172.17.%.%' identified by 'root' with grant option" | mysql -uroot -proot


# コマンドを指定せずにdocker runした際にデフォルトで実行するコマンドを指定
ENTRYPOINT ["mysqld_safe"]