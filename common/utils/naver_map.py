from django.shortcuts import render
import requests
import json
def naver_map(address, request):
    normalized_address = ' '.join(address.split())
    vworld_key = "C5DD4C9E-0189-3CBF-8AFA-7BE8B0D09DF6"
    baseurl_search = "https://api.vworld.kr/req/search"

    parms_search = {
        "key": vworld_key,
        "request": "search",
        "query": normalized_address,
        "type": "address",
        "category": "parcel",
        "format": "json"
    }

    try:
        response = requests.get(baseurl_search, params=parms_search)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"API 요청 실패: {e}")

    response_json = response.json()
    item_x = response_json.get("response", {}).get("result", {}).get("items", [])[0].get("point", {}).get("x")
    item_y = response_json.get("response", {}).get("result", {}).get("items", [])[0].get("point", {}).get("y")

    # 첫 번째 API 요청 파라미터 설정
    baseurl_search = "https://api.vworld.kr/req/data"
    params_search = {
        "page": "1",
        "size": "1",
        "request": "GetFeature",
        "geomFilter": f"POINT({item_x} {item_y})",
        "data": "LP_PA_CBND_BUBUN",
        "format": "json",
        "key": vworld_key
    }

    try:
        # 첫 번째 API 요청 (주소 검색)
        response = requests.get(baseurl_search, params=params_search)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"API 요청 실패: {e}")

    response_json = response.json()
    items = []
    items = response_json.get("response", {}).get("result", {}).get(
        "featureCollection", {}).get("features", [])[0].get("geometry", {}).get("coordinates", [])[0]

    transformed_coordinates = [[[lat, lon]
                                for lon, lat in path] for path in items]

    polygon_paths = []
    polygon_paths = transformed_coordinates
    # polygon_paths = [
    #     [
    #         [35.147373835257326, 126.79203322494573],
    #         [35.14755604833613, 126.79258941275606],
    #         [35.147590671134544, 126.79277358828519],
    #         [35.14758075760663, 126.79277438176567],
    #         [35.147571260060865, 126.79283355570524],
    #         [35.14754233918198, 126.79287752536425],
    #         [35.14751096516151, 126.79279497146653],
    #         [35.14749401356581, 126.79274952766468],
    #         [35.14743830739503, 126.79260157637478],
    #         [35.14744565540955, 126.79260795541967],
    #         [35.14746926536196, 126.79258382922568],
    #         [35.14736357287228, 126.79225998384867],
    #         [35.147375703758726, 126.79226443017986],
    #         [35.147373140379585, 126.79225716101384],
    #         [35.1472841736161, 126.79200485653521],
    #         [35.14735572112381, 126.79202979260312],
    #         [35.147373835257326, 126.79203322494573]
    #     ]
    # ]

    context = {
        'naver_client_id': 'hmpfs1a6fl',
        'vworld_api_key': "6C934ED4-5978-324D-B7DE-AC3A0DDC3B38",
        "x": item_x,
        "y": item_y,
        "polygon_paths": json.dumps(polygon_paths)  # JSON 형식으로 변환
    }
    return render(request, 'naver_map.html', context)