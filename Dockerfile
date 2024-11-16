FROM geoips-python3.10

# Define build-time arguments with default values
ARG USER=geoips_user
ARG GROUP=${USER}
ARG USER_ID=25000
ARG GROUP_ID=25000
ARG PLUGIN=PLUGIN

# Set environment variables for use during build and runtime
ENV PLUGIN_NAME=${PLUGIN}
ENV PLUGIN_DIR="$GEOIPS_PACKAGES_DIR/$PLUGIN_NAME"
ENV PLUGIN_DATA_DIR="$GEOIPS_TESTDATA_DIR/$PLUGIN_NAME"

USER root

# Create the group and user if they don't exist, and set up directories
RUN set -eux; \
    if ! getent group "${GROUP_ID}" >/dev/null; then \
        groupadd -g "${GROUP_ID}" "${GROUP}"; \
    fi; \
    if ! id -u "${USER}" >/dev/null 2>&1; then \
        useradd --gid "${GROUP_ID}" --uid "${USER_ID}" -m "${USER}"; \
    fi; \
    mkdir -p "$PLUGIN_DIR"; \
    mkdir -p "$PLUGIN_DATA_DIR"; \
    ls "$GEOIPS_PACKAGES_DIR" "$GEOIPS_TESTDATA_DIR"; \
    chown -R "${USER_ID}:${GROUP_ID}" "$PLUGIN_DATA_DIR" "$PLUGIN_DIR"

# Switch to the new user
USER ${USER}

# Set the working directory
WORKDIR ${PLUGIN_DIR}

# Copy and install Python dependencies separately to leverage caching
# COPY --chown=${USER_ID}:${GROUP_ID} requirements.txt ./requirements.txt
# RUN python3 -m pip install --user -r requirements.txt

# Copy the application code
COPY --chown=${USER_ID}:${GROUP_ID} . .

# Install the plugin in editable mode
RUN python3 -m pip install --user -e .; \
    create_plugin_registries

# Update PATH for the user's local bin directory
ENV PATH=$PATH:/home/${USER}/.local/bin


