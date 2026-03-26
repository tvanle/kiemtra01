#!/bin/bash
# Nginx Gateway
mkdir -p api_gateway_service

# Django Services
for s in customer staff laptop mobile; do
    if [ "$s" = "customer" ] || [ "$s" = "staff" ]; then
        proj="portal"
    else
        proj="catalog"
    fi
    mkdir -p ${s}_service/$proj/$proj
    mkdir -p ${s}_service/$proj/api
done
