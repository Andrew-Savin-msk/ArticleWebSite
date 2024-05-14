FROM ubuntu:22.04

RUN sed -i 's/archive.ubuntu.com/mirror.us.leaseweb.net/' /etc/apt/sources.list \
    && apt-get update && apt-get install -y \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY . .

RUN chmod 664 ./instance/blog.db

RUN python3 -m venv venv
ENV PATH="/usr/src/app/venv/bin:$PATH"

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "start.py"]
