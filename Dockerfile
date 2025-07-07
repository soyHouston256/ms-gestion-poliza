FROM python:3-slim
WORKDIR /app
RUN pip3 install "fastapi[standard]"
RUN pip3 install pydantic
RUN pip3 install mysql-connector-python
COPY . .
CMD ["fastapi", "run", "./main.py", "--port", "8002"]