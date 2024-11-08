#!/bin/bash

# Define file paths
README="README.md"
BENCHMARK="results/benchmark/1/benchmark.md"

# Use sed to replace the existing Results Table section
sed -i '' '/## 📊 Results Table/,/## [^#]/{
    /## 📊 Results Table/!{
        /## [^#]/!d
    }
    r '"$BENCHMARK"'
    d
}' "$README"