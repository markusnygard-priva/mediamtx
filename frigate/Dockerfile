FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y wget git build-essential gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Go 1.24.0 manually
RUN wget https://go.dev/dl/go1.24.0.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.24.0.linux-amd64.tar.gz && \
    rm go1.24.0.linux-amd64.tar.gz

# Clone and build go2rtc with gstreamer integration
ENV PATH="/usr/local/go/bin:$PATH"
RUN git clone https://github.com/AlexxIT/go2rtc.git /opt/go2rtc && \
    cd /opt/go2rtc && \
    go build -tags gst -o /usr/local/bin/go2rtc

ENTRYPOINT ["/usr/local/bin/go2rtc"]
