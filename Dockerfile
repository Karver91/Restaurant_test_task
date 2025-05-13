FROM python:3.12-slim

WORKDIR /backup

COPY ./requirements.txt /backup/requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /backup/requirements.txt

COPY . /backup

# CMD ["python3", "-m", "src.main"]
RUN chmod +x app_start.sh

CMD ["bash", "app_start.sh"]
