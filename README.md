# Conda
conda create --name get_text
conda env export --name gen_text -f environment.ym
conda env create -f environment.yml $PWD/gen_text
conda activate get_text

# Docker
docker build -t gentext:latest .
docker rm gentext
docker run -d --name gentext gentext:latest
docker logs -f gentext

# Docker serve
docker build -t gentext-serve:latest .
docker rm gentext-serve
docker run -d -p 8080:80 --name gentext-serve gentext-serve:latest
docker logs -f gentext-serve