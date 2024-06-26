FROM python:3.6
WORKDIR /app
ADD . /app
COPY requirements.txt /app
RUN python3 -m pip install -r requirements.txt
RUN python -m webbrowser -t "http://www.python.org"
EXPOSE 5000
CMD ["python","app.py"]