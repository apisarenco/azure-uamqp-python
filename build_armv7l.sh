#!/bin/bash
set -e

# To execute this script:
# docker run --rm -v $PWD:/data local/armv7l /data/build_armv7l.sh

export CPATH="/opt/uamqp/openssl/include"
export LIBRARY_PATH="/opt/uamqp/openssl/lib"
export OPENSSL_ROOT_DIR="/opt/uamqp/openssl"
export OPENSSL_INCLUDE_DIR="/opt/uamqp/openssl/include"
export UAMQP_SUPPRESS_LINK_FLAGS=True
export LDFLAGS="/opt/uamqp/openssl/lib/libssl.a /opt/uamqp/openssl/lib/libcrypto.a"
export CFLAGS="-I/opt/uamqp/openssl/include"

# Build the wheels
pushd /data
/usr/local/bin/python3.4 setup.py bdist_wheel
/usr/local/bin/python3.5 setup.py bdist_wheel
/usr/local/bin/python3.6 setup.py bdist_wheel
/usr/local/bin/python3.7 setup.py bdist_wheel