FROM postgres:latest AS builder

WORKDIR /app

COPY ./sql/physical_model.postgres /docker-entrypoint-initdb.d/physical_model.sql


FROM postgres:latest AS production

COPY --from=builder /docker-entrypoint-initdb.d/physical_model.sql \
    /docker-entrypoint-initdb.d/physical_model.sql