# Run this docker file from the parent directory, see README.md
FROM alpine:3.16

# Upgrade and install 
RUN apk -U upgrade \
    && apk add --no-cache \
                python3 \
                py3-pip \
                py3-virtualenv

# Copy App
COPY app/ /eon-bot/app/
# Copy requirements.txt
COPY requirements.txt /eon-bot/requirements.txt

WORKDIR /eon-bot

# Create virtual environment
RUN mkdir /eon-bot/venv \
    && python3 -m venv /eon-bot/venv \
    && . /eon-bot/venv/bin/activate \
    && pip3 install -r requirements.txt \
    && python3 -m pip install -U py-cord --pre
    # We need a later package of py-cord therefor additional pip install command

COPY docker/entrypoint.sh /eon-bot/
RUN chmod +x /eon-bot/entrypoint.sh
ENTRYPOINT ["/eon-bot/entrypoint.sh"]
CMD [""]