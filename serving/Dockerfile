FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install -U pip && pip install streamlit==1.37.* duckdb==1.1.*
EXPOSE 8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_PORT=8501
CMD ["streamlit","run","app.py"]
