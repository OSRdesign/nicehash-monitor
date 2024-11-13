import hmac
import json
import time
import uuid
from hashlib import sha256
from urllib.parse import urlencode
import http.client
from config import API_KEY, API_SECRET, ORGANIZATION_ID, BASE_URL

class NiceHashAPI:
    def __init__(self):
        self.api_key = API_KEY
        self.api_secret = API_SECRET
        self.org_id = ORGANIZATION_ID

    def _get_epoch_ms(self):
        return int(time.time() * 1000)

    def _create_nonce(self):
        return str(uuid.uuid4())

    def _sign(self, method, path, query, body):
        time = self._get_epoch_ms()
        nonce = self._create_nonce()

        message = f'{self.api_key}\00{str(time)}\00{nonce}\00\00{self.org_id}\00\00{method.upper()}\00{path}\00{query}'

        if body:
            message += '\00' + json.dumps(body)

        signature = hmac.new(
            self.api_secret.encode(),
            message.encode(),
            sha256
        ).hexdigest()

        return {
            'X-Time': str(time),
            'X-Nonce': nonce,
            'X-Auth': f'{self.api_key}:{signature}',
            'X-Organization-Id': self.org_id,
            'Content-Type': 'application/json'
        }

    def get_mining_data(self):
        method = 'GET'
        path = '/main/api/v2/mining/rigs2'
        query = ''
        
        headers = self._sign(method, path, query, None)
        
        conn = http.client.HTTPSConnection(BASE_URL.replace('https://', ''))
        conn.request(method, f"{path}{query}", headers=headers)
        
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        conn.close()
        
        return data

    def get_wallet_balance(self):
        method = 'GET'
        path = '/main/api/v2/accounting/accounts2'
        query = ''
        
        headers = self._sign(method, path, query, None)
        
        conn = http.client.HTTPSConnection(BASE_URL.replace('https://', ''))
        conn.request(method, f"{path}{query}", headers=headers)
        
        response = conn.getresponse()
        data = json.loads(response.read().decode())
        conn.close()
        
        return data