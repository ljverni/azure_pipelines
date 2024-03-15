#!/bin/bash

if [ -d "venv" ]; then
    venv/main/bin/python3 src/news/news_article/news_article_extract.py && venv/main/bin/python3 src/news/news_article/news_article_load.py   
else
    python3 news/news_article/news_article_extract.py && python3 news/news_article/news_article_load.py   
fi
