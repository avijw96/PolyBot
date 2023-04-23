FROM python:3.10 
WORKDIR /PolyApp
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV TELEGRAM_TOKEN=5789274911:AAG97ny4zSXEKPhbpOuCXBj1-lUgq0jR01A
CMD ["python3", "bot.py"]