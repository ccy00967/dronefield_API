import requests

def serch_pnu(road, jibun):
    adrass = f"{road} {jibun}"
    normalized_address = ' '.join(adrass.split())
    
    vworld_key = "6C934ED4-5978-324D-B7DE-AC3A0DDC3B38"
    baseurl = "https://api.vworld.kr/req/search"
    response_pnu = requests.get(f"{baseurl}"
                               +f"?page=1&size=1"
                               +f"&request=search"
                               +f"&query={normalized_address}"
                               +f"&type=address"
                               +f"&category=parcel"
                               +f"&format=json"
                               +f"&key={vworld_key}")
    
    response_json = response_pnu.json()
    print(response_json)
    if response_pnu.status_code != 200 or response_json["response"].get("status") == "NOT_FOUND":
        raise ValueError("주소가 없습니다")

    items = response_json["response"].get("result", {}).get("items")
    if not items:
        raise ValueError("잘못된 주소입니다.")

    pnu = items[0].get("id")
    if pnu is None or not len(pnu) == 19:
        raise ValueError("잘못된 pnu값 입니다.")

    response_result = {
        "pnu": pnu,
        "adm_cd": pnu[:10]
    }

    baseurl = "https://api.vworld.kr/ned/data/ladfrlList"
    response_lndpclAr = requests.get(f"{baseurl}"
                                +f"?domain=https://dronefield.co.kr"
                                +f"&pnu={response_result["adm_cd"]}"
                                +f"&format=json"
                                +f"&key={vworld_key}")
    
    lndpclAr_json = response_lndpclAr.json()
    
    lndpclAr_list = lndpclAr_json.get("ladfrlVOList", {}).get("ladfrlVOList")
    
    if not lndpclAr_list:
        raise ValueError("lndpclAr 값이 없습니다.")

    response_result["lndpclAr"] = lndpclAr_list[0].get("lndpclAr", 11)

    return response_result
