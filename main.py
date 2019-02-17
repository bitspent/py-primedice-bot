import requests
import json

# replace token-access-keys by your key

def headers():
    return {
        'origin': 'https://primedice.com',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,fr;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'content-type': 'application/json',
        'accept': '*/*',
        'referer': 'https://primedice.com/',
        'authority': 'api.primedice.com',
        'x-lockdown-token': 'undefined',
        'x-access-token': '<token-access-keys>',
        'dnt': '1'
    }

def balance(coin): 
    data = '[{"operationName":"Balances","variables":{"available":true},"query":"query Balances($available: Boolean = false, $vault: Boolean = false) {\\n  user {\\n    id\\n    balances {\\n      available @include(if: $available) {\\n        currency\\n        amount\\n        __typename\\n      }\\n      vault @include(if: $vault) {\\n        currency\\n        amount\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n"}]'
    response = requests.post('https://api.primedice.com/graphql', headers=headers(), data=data)
    coins = response.json()[0]['data']['user']['balances']
    out = [ x['available'] for x in coins if x['available']['currency'] == coin] 
    return out[0]['amount']*100000000    

def roll(amount, condition, target,coin):  
    data = '[{"operationName":null,"variables":{"currency":"'+str(coin)+'","amount":' + str(amount) + 'e-8,"target":' + str(target) + ',"condition":"' + condition + '"},"query":"mutation ($amount: Float!, $target: Float!, $condition: BetGamePrimediceConditionEnum!, $currency: CurrencyEnum!) {\\n  primediceRoll(amount: $amount, target: $target, condition: $condition, currency: $currency) {\\n    ...BetFragment\\n    ...PrimediceBetStateFragment\\n    __typename\\n  }\\n}\\n\\nfragment BetFragment on Bet {\\n  id\\n  iid\\n  payoutMultiplier\\n  amountMultiplier\\n  amount\\n  payout\\n  updatedAt\\n  currency\\n  game\\n  user {\\n    id\\n    name\\n    __typename\\n  }\\n  __typename\\n}\\n\\nfragment PrimediceBetStateFragment on Bet {\\n  state {\\n    ... on BetGamePrimedice {\\n      result\\n      target\\n      condition\\n      __typename\\n    }\\n    __typename\\n  }\\n  __typename\\n}\\n"}]'
    response = requests.post('https://api.primedice.com/graphql', headers=headers(), data=data)        
    success = str(response) == '<Response [200]>'
    _json = response.json()[0]
    result = _json['data']['primediceRoll']['state']['result']
    payout = _json['data']['primediceRoll']['payout']    
    return success, result, payout

# get user Bitcoin balance in satoshis
bal = balance('btc')

# do a dice roll: 100 Satoshi
succ, res, pay = roll(100, 'above', 70)

# show operation success, roll result, payout
# payout is 0 on lost
print('success', succ, 'dice roll result', res, 'payout', pay)
