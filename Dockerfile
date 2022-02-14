FROM python:3.9

# Dependencies
COPY poetry.lock pyproject.toml .tool-versions ./
RUN pip install poetry
RUN poetry install

# Copy in app code
ADD app ./workspace/app
WORKDIR /workspace

# Ports etc
EXPOSE 3000

# Use the poetry venv to run the api
ENTRYPOINT ["poetry", "run", "python3", "./app/server.py"]
