#!/bin/bash

for i in {1..20};do
    kernprof -l -v benchmark.py;
done
