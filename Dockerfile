FROM node:20-bookworm-slim AS frontend-build
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci \
    && ARCH="$(node -p "process.arch")" \
    && if [ "$ARCH" = "arm64" ]; then npm install --no-save @rollup/rollup-linux-arm64-gnu; \
       elif [ "$ARCH" = "x64" ]; then npm install --no-save @rollup/rollup-linux-x64-gnu; \
       fi

COPY frontend/ ./
RUN npm run build -- --base=/indiancalendars/

FROM python:3.12-slim
WORKDIR /usr/local/indiancalendars

RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY start.sh basicFunctionsGraphsAnimations.py transliterate.py ./
COPY backend/main.py backend/config.py ./backend/
COPY jyotish_ganit/panchanga.py ./jyotish_ganit/
COPY --from=frontend-build /app/frontend/dist /usr/share/nginx/html/indiancalendars
COPY nginx.conf /etc/nginx/sites-enabled/default

RUN chmod +x /usr/local/indiancalendars/start.sh

EXPOSE 80
CMD ["/usr/local/indiancalendars/start.sh"]
