#!/bin/bash

mkdir -p /workshop/containers

chown ubuntu:ubuntu -R /workshop

if [[ $(cat /proc/swaps | wc -l) -le 1 && ! -f /swap.img ]]; then
  dd if=/dev/zero of=/swap.img count=1024 bs=1M
  chmod 0600 /swap.img
  mkswap /swap.img
  swapon /swap.img
fi

