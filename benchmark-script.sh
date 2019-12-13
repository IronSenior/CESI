#!/bin/bash

for i in {1..8};do
    kernprof -l -v benchmark.py;
done
