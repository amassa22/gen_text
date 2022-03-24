NAME := gen_text
TAG := $(shell date +%F)
DATA_DIR := ${PWD}/data
DATA_FILE_PATH := /data/ufc.csv
.PHONY : all



build-serve: serve/Dockerfile
	docker build -f serve/Dockerfile -t ${NAME}_serve:${TAG} -t ${NAME}_serve:latest serve/

rm-serve:
	docker rm ${NAME}_serve

stop-serve:
	docker stop ${NAME}_serve

stop-rm-serve: stop-serve rm-serve

run-serve:
	docker run -d --name ${NAME}_serve -e STREAMLIT_SERVER_PORT=80 -p 8080:80 ${NAME}_serve:latest 
	#docker run -t --name ufc-serve -e MODEL_NAME=my_model -v ${DATA_DIR}:/data -v "/Users/lex/PycharmProjects/ufc/models/my_model:/models/my_model"  -p 8501:8501 tensorflow/serving:latest-devel
	#docker run -it --name ufc-serve -e MODEL_NAME=my_model -v ${DATA_DIR}:/data -v "/Users/lex/PycharmProjects/ufc/models/my_model:/models/my_model"  -p 8501:8501 --entrypoint bash tensorflow/serving

all-serve:	build-serve stop-rm-serve run-serve
