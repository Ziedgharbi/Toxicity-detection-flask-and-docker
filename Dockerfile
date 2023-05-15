# Python 3.9
From  python:3.9-buster

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["python"]
CMD ["prediction.py"]
