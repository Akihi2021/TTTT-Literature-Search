FROM silverlogic/python3.8

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install RandomWords

COPY . /app

ENTRYPOINT ["python"]


CMD ["entrypoint.py"]