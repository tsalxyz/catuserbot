#FROM tsalxyz/catuserbot:slim-buster

#clonning repo 
#RUN git clone https://github.com/tsalxyz/catuserbot.git /root/userbot
#working directory 
#WORKDIR /root/userbot

# Install requirements
#RUN pip3 install --no-cache-dir requirements.txt

#ENV PATH="/home/userbot/bin:$PATH"

#CMD ["python3","-m","userbot"]


# this docker will installed latest build version of NodeJs and Python version
FROM tsalxyz/python-nodejs:latest
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY . /app/
WORKDIR /app/
RUN pip3 install --no-cache-dir requirements.txt
CMD ["python3", "-m", "userbot"]
