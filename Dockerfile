FROM silverlogic/python3.8

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT ["python"]

CMD ["entrypoint.py"]