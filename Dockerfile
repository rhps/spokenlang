FROM python:3.6.7-slim

WORKDIR /opt/spokenlang/
COPY . ./
RUN apt-get update -y && apt-get install wget ffmpeg sox curl gnupg -y && \
	export GCSFUSE_REPO=gcsfuse-stretch && \
	echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" |  tee /etc/apt/sources.list.d/gcsfuse.list && \
	curl https://packages.cloud.google.com/apt/doc/apt-key.gpg |  apt-key add - && \
	apt-get update -y && apt-get install gcsfuse -y
RUN wget https://storage.googleapis.com/kaggle-datasets/35318/47705/spoken-language-identification.zip?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1543776700&Signature=FJ13944fzG3JAjkSBd8MGZkx8G9ztu7W%2FlPnG9suy4a3b4eops3obKS3lqRt1j1Q3oSMPMJWi6UxnQUpygWLoTC%2FHilO7ZyH7jsqv89t5KRgdF%2B8VeGA9hEcEBuT45Wgu0L1Zf9tv%2B7EAYGX5Lk8tdo97FSbog3ya5Nu3blj3Lnm2Ss%2ByNvWS30cWkjyJMD1UmRnmGqmQyq2VNGnW02xvDQnduvSM0IHaTLV2qTbICNA0YcD6jy4SjQohwmbcVHJD%2Bsw7ZMnRV%2BwF1Ysm54MtQAGpZ2ittjVtpiJjGzeNCFIiXAdUqqPVaWWN8%2FvyKZ%2FpXLtiwApNF9cloAnNkL%2BBw%3D%3D
#--directory-prefix=/opt/spokenlang/datasets

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-u", "cli.py"]
