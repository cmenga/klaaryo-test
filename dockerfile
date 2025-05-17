FROM python:3.11.12-alpine3.21

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
  apk add --no-cache postgresql-client && \
  apk add --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
  /py/bin/pip install -r /tmp/requirements.txt && \
  sed -i 's/requires_system_checks = False/requires_system_checks = []/' \
    $(/py/bin/python -c "import django_grpc_framework.management.commands.grpcrunserver as m; print(m.__file__)") && \
  rm -rf /tmp && \
  apk del .tmp-build-deps && \
  adduser -H -D djangouser

ENV PATH="/py/bin:$PATH"
USER djangouser
