FROM python:3.12-alpine

RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup

WORKDIR /app
COPY --chown=appuser:appgroup app.py .

ENV PORT=8081
ENV BACKEND_HOST="greca-central"
ENV BACKEND_PORT=8080
ENV NOMBRE_CLIENTE="carrito-san-antonio"

USER appuser
EXPOSE 8081

CMD ["python", "app.py"]
