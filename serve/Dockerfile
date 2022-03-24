FROM python:3.6-buster

RUN pip install tensorflow streamlit

COPY app.py model.h5 tokenizer.pkl sequences.txt ./

#CMD ["python", "app.py"]
ENTRYPOINT ["streamlit", "run", "app.py"]
