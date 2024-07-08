FROM debian:bookworm-slim as base


ARG DEBIAN_FRONTEND=noninteractive
ENV VIRTUAL_ENV=/opt/python/venv \
    APP_USER=app \
    TZ=Europe/Paris

USER root:root

# Create a dedicated user
RUN useradd -ms /bin/bash ${APP_USER}


# python execution environment
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    python3.11 python3.11-venv python3-pip
RUN python3 --version

RUN mkdir -p ${VIRTUAL_ENV} /app
COPY ./indus/scripts/docker-*.sh /
RUN chown ${APP_USER}:${APP_USER} /docker-*.sh /app ${VIRTUAL_ENV} \
    && chmod 770 /docker-*.sh

USER ${APP_USER}:${APP_USER}

RUN python3 --version

# we install virtual env only for the app user
RUN python3 -m venv $VIRTUAL_ENV

ENTRYPOINT [ "/docker-run-entrypoint.sh" ]

####################################################################################
FROM base as build_base

USER ${APP_USER}:${APP_USER}

RUN python3 --version

# we install poetry only for the app user
RUN . ${VIRTUAL_ENV}/bin/activate \
    && pip install poetry \
    && pip install twine

####################################################################################
FROM build_base as dev_env

USER root:root

# tools for debug
RUN apt-get install -y --no-install-recommends \
    sudo curl iputils-ping iproute2

RUN usermod -aG sudo ${APP_USER}
RUN passwd --delete ${APP_USER}

USER ${APP_USER}:${APP_USER}
COPY --chown=${APP_USER}:${APP_USER} ./indus/env/dev.bashrc /home/${APP_USER}/
RUN echo ". /home/${APP_USER}/dev.bashrc" >> /home/${APP_USER}/.bashrc