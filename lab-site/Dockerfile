FROM python:3.13-slim AS build
WORKDIR /handbook

COPY build.py ./
COPY guides/ guides/
COPY starters/ starters/
COPY web/ web/
RUN python build.py

FROM nginx:stable-alpine
COPY --from=build /handbook/dist/ /usr/share/nginx/html/

EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1/index.html || exit 1
