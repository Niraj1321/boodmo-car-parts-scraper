import requests

cookies = {
    'client_id': 'd8700f92d8b149525741866b1d37ff8d',
    'sbjs_migrations': '1418474375998%3D1',
    'sbjs_current_add': 'fd%3D2026-04-12%2015%3A14%3A35%7C%7C%7Cep%3Dhttps%3A%2F%2Fboodmo.com%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_first_add': 'fd%3D2026-04-12%2015%3A14%3A35%7C%7C%7Cep%3Dhttps%3A%2F%2Fboodmo.com%2F%7C%7C%7Crf%3D%28none%29',
    'sbjs_current': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
    'sbjs_first': 'typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29',
    'sbjs_udata': 'vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F146.0.0.0%20Safari%2F537.36',
    'WZRK_G': '7450178193944c278486d152a420fab8',
    '_gcl_au': '1.1.940376652.1775987077',
    '_gid': 'GA1.2.554979829.1775987078',
    '_ga': 'GA1.1.1414854695.1775987078',
    '_fbp': 'fb.1.1775987078078.525932154697295194',
    '_ga_BJ1YLK4EDR': 'GS2.1.s1775987077$o1$g1$t1775988917$j60$l0$h0',
    'WZRK_S_R9Z-W84-ZK5Z': '%7B%22p%22%3A7%2C%22s%22%3A1775987076%2C%22t%22%3A1775987885%7D',
    'g_state': '{"i_l":0,"i_ll":1775988918019,"i_b":"yDmiT+yZ60xcGGC24VRD8QpAK9mfXWRYlmIXR6Zj0hs","i_e":{"enable_itp_optimization":0},"i_et":1775988918019}',
    'sbjs_session': 'pgs%3D7%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fboodmo.com%2F',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8,it;q=0.7',
    'accept-version': 'v1',
    'priority': 'u=1, i',
    'referer': 'https://boodmo.com/',
    'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'x-api': 'CustomerAPI',
    'x-boo-sign': 'df010425527476b137a921a71a94eddc',
    'x-client-app': 'web',
    'x-client-build': '260408.1546',
    'x-client-id': 'd8700f92d8b149525741866b1d37ff8d',
    'x-client-token': '6ce5879e-ced2-5ca0-8a87-f08718bce01a',
    'x-client-version': '7.3.15',
    'x-date': '2026-04-12T10:15:18.250Z',
    # 'cookie': 'client_id=d8700f92d8b149525741866b1d37ff8d; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2026-04-12%2015%3A14%3A35%7C%7C%7Cep%3Dhttps%3A%2F%2Fboodmo.com%2F%7C%7C%7Crf%3D%28none%29; sbjs_first_add=fd%3D2026-04-12%2015%3A14%3A35%7C%7C%7Cep%3Dhttps%3A%2F%2Fboodmo.com%2F%7C%7C%7Crf%3D%28none%29; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F146.0.0.0%20Safari%2F537.36; WZRK_G=7450178193944c278486d152a420fab8; _gcl_au=1.1.940376652.1775987077; _gid=GA1.2.554979829.1775987078; _ga=GA1.1.1414854695.1775987078; _fbp=fb.1.1775987078078.525932154697295194; _ga_BJ1YLK4EDR=GS2.1.s1775987077$o1$g1$t1775988917$j60$l0$h0; WZRK_S_R9Z-W84-ZK5Z=%7B%22p%22%3A7%2C%22s%22%3A1775987076%2C%22t%22%3A1775987885%7D; g_state={"i_l":0,"i_ll":1775988918019,"i_b":"yDmiT+yZ60xcGGC24VRD8QpAK9mfXWRYlmIXR6Zj0hs","i_e":{"enable_itp_optimization":0},"i_et":1775988918019}; sbjs_session=pgs%3D7%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fboodmo.com%2F',
}

response = requests.get(
    'https://boodmo.com/api/v1/customer/api/catalog/vehicle/car-maker-list',
    cookies=cookies,
    headers=headers,
)

if response.status_code==200:
    car_maker=[]
    json_dic=response.json()
    car_maker_list=json_dic['items']

    for car_dic in car_maker_list:
        car_maker.append({'id':car_dic['id'],'slug':car_dic['slug']})

    print('')
