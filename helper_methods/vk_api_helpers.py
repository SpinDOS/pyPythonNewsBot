import requests
import os
from urllib.parse import urlencode

_VK_API_KEY = os.environ.get('VK_API_KEY')


def make_vk_api_request(method, extra_params=None):
    api_params = {'v': 5.62}
    if _VK_API_KEY:
        api_params['access_token'] = _VK_API_KEY
    if extra_params:
        url_params = '%s&%s' % (urlencode(extra_params),
                                urlencode(api_params)) # api params must be in the end
    else:
        url_params = urlencode(api_params)
    url = 'https://api.vk.com/method/%s?%s' % (method, url_params)
    vk_response = requests.get(url).json()
    if 'error' in vk_response:
        raise Exception(vk_response['error'])
    return vk_response['response']
