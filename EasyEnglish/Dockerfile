FROM python:3.13-slim
RUN groupadd -r groupdjango && useradd -r -g groupdjango userdj

ENV PYTHONDONTWRITEBYTCODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
WORKDIR /home/easyenglish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

USER userdj