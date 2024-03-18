FROM python:3-alpine3.12
WORKDIR ./app
ADD  requirements.txt /app
COPY . /app
RUN export PYTHONPATH=/usr/bin/python
RUN pip install -r requirements.txt
ENV PORT=5000
EXPOSE 5000
CMD python ./app.py
#CMD ["python3", "-m", "./app.py", "run", "--host=0.0.0.0"]
