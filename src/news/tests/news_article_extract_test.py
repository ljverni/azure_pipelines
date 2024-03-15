
import pytest
import src.news.news_article.news_article_extract as news_article
from unittest.mock import Mock, patch
import json
from datetime import datetime as dt


@pytest.fixture
def mock_requests_get():
    with patch('src.news.news_article.news_article_extract.requests.get') as mock_get:
        yield mock_get
    

def test_extract_success(mock_requests_get):
    successful_response = Mock()
    successful_response.status_code = 200
    successful_response.json.return_value = {'results': [1, 2, 3]}

    mock_requests_get.return_value = successful_response

    result, row_count = news_article.extract('app_key', 'headers', 'endpoint', 'params')
    
    assert type(row_count) == int
    assert result == json.dumps([1, 2, 3])

def test_extract_failure(mock_requests_get):
    failed_response = Mock()
    failed_response.status_code = 400

    mock_requests_get.return_value = failed_response

    with pytest.raises(Exception, match=r'Response status: 400'):
        news_article.extract('app_key', 'headers', 'endpoint', 'params')


@pytest.fixture
def mock_azure_blob_handler():
    with patch('src.news.news_article.news_article_extract.AzureBlobHandler') as mock_handler:
        yield mock_handler

def test_load(mock_azure_blob_handler):
    mock_blob_handler_instance = Mock()
    mock_azure_blob_handler.return_value = mock_blob_handler_instance

    mock_blob_handler_instance.load_blob.return_value = '123'
    container_details = {
            'account_url': 'account_url',
            'container': 'container',
            'entity': 'entity',
            'file_format': 'file_format'
            }
    result_batch_no = news_article.load(container_details, 'file_content')
    
    assert result_batch_no.isnumeric()




