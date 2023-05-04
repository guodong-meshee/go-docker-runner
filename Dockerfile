From golang:latest

RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    vim \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

ADD utils.py .

CMD ["python3", "utils.py"]