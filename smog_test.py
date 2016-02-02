import mock
import pytest
from smog import SmogDataFetcher, requests

class TestSmogDataFetcher(object):

    def test_get_data(self):
        host = 'http://host.com'
        smog_data_fetcher = SmogDataFetcher(host)
        with mock.patch.object(requests, 'post') as r:
            mock_response = mock.Mock()
            mock_response.content = '{}'
            r.return_value = mock_response
            assert smog_data_fetcher.get_data() == {}

