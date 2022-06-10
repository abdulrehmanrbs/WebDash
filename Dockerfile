FROM python:3.10
ADD requirements.txt /requirements.txt
ADD main.py /main.py
ADD okteto-stack.yaml /okteto-stack.yaml
ADD Dockerfile /Dockerfile
RUN pip install -r requirements.txt
EXPOSE 8080
COPY ./app /app
CMD ["python", "main.py"]
