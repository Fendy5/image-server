FROM python:3.11-alpine AS builder

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories \
    && apk update \
    && apk add git gcc g++ musl-dev libffi-dev glib-dev pkgconf openssl-dev make mysql-dev \
    && pkg-config --version
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple -r /requirements.txt \
    && mkdir -p /install/lib/python3.11/site-packages \
    && cp -rp /usr/local/lib/python3.11/site-packages /install/lib/python3.11


FROM python:3.11-alpine AS production

## 设置时区
ENV TZ=Asia/Shanghai

COPY --from=builder /install/lib /usr/local/lib
COPY --from=builder /usr/local/bin/ /usr/local/bin/
WORKDIR /app
COPY . /app

ENV DJANGO_ENV=production

# 创建日志目录并数据迁移
RUN mkdir "/app/logs"  \
    && python manage.py makemigrations && python manage.py migrate

## 暴露端口
EXPOSE 8000

## 运行uWSGI服务器
CMD ["uwsgi", "--http", "0.0.0.0:8000", "--module", "ImageProject.wsgi"]
