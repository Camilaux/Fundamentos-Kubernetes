FROM python:3.12-alpine

# Usuario sin privilegios por seguridad
RUN addgroup -g 10001 -S appgroup && \
    adduser -u 10001 -S appuser -G appgroup

WORKDIR /app
COPY --chown=appuser:appgroup app.py .

ENV PORT=8080
ENV NOMBRE_SERVICIO="greca-central"

USER appuser
EXPOSE 8080

CMD ["python", "app.py"]
