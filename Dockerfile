FROM python:3.12

WORKDIR /code

COPY pyproject.toml uv.lock README.md /code/
COPY zupit/ /code/zupit/



RUN pip install --upgrade pip
RUN pip install .
RUN opentelemetry-bootstrap -a install

COPY ./zupit/ /code/


CMD ["opentelemetry-instrument", "fastapi", "dev", "--host", "0.0.0.0", "zupit/app.py"]
