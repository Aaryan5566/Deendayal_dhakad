
# Lightweight Python Image Use Karo
FROM python:3.10-slim

# System Packages Install Karna
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Working Directory Set Karna
WORKDIR /Deendayal_botz

# Source Code Copy Karna
COPY . .

# Permissions Fix
RUN chmod +x start.sh

# Python Dependencies Install Karna
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Bot Start Karna
CMD ["bash", "./start.sh"]
