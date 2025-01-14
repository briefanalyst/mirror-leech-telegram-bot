#VERSION: 2.14
# AUTHORS: b0nk
# CONTRIBUTORS: Diego de las Heras (ngosang@hotmail.es)

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the author nor the names of its contributors may be
#      used to endorse or promote products derived from this software without
#      specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import json
import time
from urllib.parse import urlencode, unquote

from novaprinter import prettyPrinter
from helpers import retrieve_url


class rarbg(object):
    url = 'https://proxyrarbg.org'
    name = 'RARBG'
    supported_categories = {
        'all': '4;14;17;18;23;25;27;28;32;33;40;41;42;44;45;46;47;48;49;50;51;52;53;54',
        'movies': '14;17;42;44;45;46;47;48;50;51;52;54',
        'tv': '18;41;49',
        'music': '23;25',
        'games': '27;28;32;40;53',
        'software': '33'
    }

    def search(self, what, cat='all'):
        base_url = "https://torrentapi.org/pubapi_v2.php?%s"
        app_id = "qbittorrent"

        # get token
        params = urlencode({'get_token': 'get_token', 'app_id': app_id})
        response = retrieve_url(base_url % params)
        j = json.loads(response)
        token = j['token']
        time.sleep(2.1)

        # get response json
        what = unquote(what)
        category = self.supported_categories[cat]
        params = urlencode({'mode': 'search',
                            'search_string': what,
                            'ranked': 0,
                            'category': category,
                            'limit': 100,
                            'sort': 'seeders',
                            'format': 'json_extended',
                            'token': token,
                            'app_id': 'qbittorrent'})
        response = retrieve_url(base_url % params)
        j = json.loads(response)

        # check empty response
        if 'torrent_results' not in j:
            return

        # parse results
        for result in j['torrent_results']:
            res = {'link': result['download'],
                   'name': result['title'],
                   'size': str(result['size']) + " B",
                   'seeds': result['seeders'],
                   'leech': result['leechers'],
                   'engine_url': self.url,
                   'desc_link': result['info_page'] + "&app_id=" + app_id}
            prettyPrinter(res)
