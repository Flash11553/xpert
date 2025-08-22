# Yeni baza image (Debian Bullseye üzərindədir, dəstəklənir)
FROM nikolaik/python-nodejs:python3.10-nodejs20

# ffmpeg quraşdırılması
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Layihə fayllarını konteynerə kopyala
COPY . /app/
WORKDIR /app/

# Python paketləri
RUN python3 -m pip install --upgrade pip setuptools
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt

# Start command
CMD ["python3", "-m", "BrandrdXMusic"]
