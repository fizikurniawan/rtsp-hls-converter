FROM python:3.11

ENV PYTHONUNBUFFERED=1

#Install Package
RUN apt update && apt install -y \
    build-essential \
    ffmpeg \
    supervisor


#Set Workdir & Copy App
WORKDIR /app
COPY . .

#Install Python Package with requirements file
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir output

#Expose Port
EXPOSE 8000

# CMD ["python3", "-m", "http.server", "--directory", "output", "8000"]
COPY conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]

