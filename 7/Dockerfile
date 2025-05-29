# Base image with Swift
FROM swift:6.0-jammy

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libssl-dev \
    zlib1g-dev \
    libsqlite3-dev \
    curl \
    git \
    libcurl4-openssl-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Vapor toolbox
# RUN git config http.version HTTP/1.1
RUN git config --global http.postBuffer 157286400
RUN git clone https://github.com/vapor/toolbox.git && \
    cd toolbox && \
    swift build -c release && \
    mv .build/release/vapor /usr/local/bin && \
    cd .. && \
    rm -rf toolbox

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV SWIFT_BACKTRACE=1

# Expose default Vapor port
EXPOSE 8080

# Set default command to run when container starts
CMD ["bash"]

# A volume allows for persistence of data
VOLUME ["/app"]
