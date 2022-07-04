# Run this docker file from the parent directory, see README.md
FROM ubuntu:22.04

# Upgrade and install 
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get -y install \
                python3 \
                python3-venv \
                python3-pip \
    && apt-get autoremove \
    && apt-get autoclean \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy App
COPY src/ app/src/
# Copy requirements.txt
COPY requirements.txt app/requirements.txt

WORKDIR /app

# Create virtual environment
RUN mkdir /app/venv \
    && python3 -m venv /app/venv \
    && . /app/venv/bin/activate \
    && pip3 install -r requirements.txt \
    && python3 -m pip install -U py-cord --pre
    # We need a later package of py-cord therefor additional pip install command

COPY docker/entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD [""]