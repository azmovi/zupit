FROM python:3.12

WORKDIR /code

COPY pyproject.toml uv.lock README.md /code/
COPY zupit/ /code/zupit/



RUN pip install --upgrade pip
RUN pip install .

COPY ./zupit/ /code/


CMD ["fastapi", "dev", "app.py"]
