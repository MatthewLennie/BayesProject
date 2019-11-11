# This design pattern used to enable installing from yml or env definitions later. 
FROM continuumio/miniconda3

# Short list of requirements in this case. 

RUN conda install --yes scikit-learn=0.20.0
#RUN pip install flask escape request
RUN pip install pika
RUN pip install retry
RUN pip install joblib
CMD ["conda","list"]
