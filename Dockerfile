# हल्के Python इमेज का उपयोग करें
FROM python:3.10-slim

# आवश्यक सिस्टम पैकेज स्थापित करें
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# कार्यशील निर्देशिका सेट करें
WORKDIR /Deendayal_botz

# स्रोत कोड कॉपी करें
COPY . .

# आवश्यकताओं को स्थापित करें
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# बॉट प्रारंभ करें
CMD ["bash", "./start.sh"]
