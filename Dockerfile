# start from a small, official Python image (3.12 — matches what works for you)
FROM python:3.12-slim

# set the working folder inside the container
WORKDIR /app

# copy the requirements list in first, then install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy your app code and the Chroma database into the container
COPY src/ ./src/
COPY chroma_db/ ./chroma_db/

# tell the container which command to run when it starts
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]