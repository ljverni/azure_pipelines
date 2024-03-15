#!/bin/bash

if [ -d "venv" ]; then
    venv/main/bin/python3 src/news/news_source/news_source_extract.py && venv/main/bin/python3 src/news/news_source/news_source_load.py   
else
    python3 news/news_source/news_source_extract.py && python3 news/news_source/news_source_load.py   
fi
