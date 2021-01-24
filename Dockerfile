FROM alpine

ENV TZ "Asia/Shanghai"

RUN mkdir -p /app
WORKDIR /app
COPY ./requirements.txt /app/


RUN echo "https://mirror.tuna.tsinghua.edu.cn/alpine/latest-stable/main" > /etc/apk/repositories
RUN echo "https://mirror.tuna.tsinghua.edu.cn/alpine/latest-stable/community" >> /etc/apk/repositories


RUN apk update \
    && apk add git openssh bash bash-completion curl wget unzip \
    && apk add --virtual build-deps gcc g++ python3-dev musl-dev 

RUN echo "**** install Python ****" && \
    apk add --no-cache python3 && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com \
    --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

RUN rm -rf /var/cache/apk/*

RUN pip3 install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com -r requirements.txt

RUN mkdir -p /app/temp
RUN mkdir -p /app/logs
WORKDIR /app
COPY ./ /app/

CMD ["python3", "/app/extract_phone_region.py"]