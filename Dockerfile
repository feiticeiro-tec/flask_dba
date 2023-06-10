FROM python:3.10
RUN pip install -r requirements.txt
RUN pip install pre-commit
RUN pre-commit install