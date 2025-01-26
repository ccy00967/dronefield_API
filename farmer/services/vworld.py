import requests
import logging
from typing import Dict, Any

# 로깅 설정 (필요에 따라 설정 파일에서 관리)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

def serch_pnu(road: str, jibun: str) -> Dict[str, Any]:
    """
    주어진 도로명과 지번을 기반으로 PNU와 관련된 정보를 조회합니다.

    Args:
        road (str): 도로명 주소.
        jibun (str): 지번 주소.

    Returns:
        Dict[str, Any]: 조회된 PNU, adm_cd, lndpclAr 정보를 포함한 딕셔너리.

    Raises:
        ValueError: 주소가 없거나, PNU 값이 잘못된 경우.
    """
    # 주소를 결합하고 공백을 정규화
    adrass = f"{road} {jibun}"
    normalized_address = ' '.join(adrass.split())
    logger.debug(f"Normalized Address: {normalized_address}")
    
    # VWorld API 키 및 기본 URL 설정
    vworld_key = "6C934ED4-5978-324D-B7DE-AC3A0DDC3B38"
    baseurl_search = "https://api.vworld.kr/req/search"
    
    # 첫 번째 API 요청 파라미터 설정
    params_search = {
        "page": "1",
        "size": "1",
        "request": "search",
        "query": normalized_address,
        "type": "address",
        "category": "parcel",
        "format": "json",
        "key": vworld_key
    }
    
    try:
        # 첫 번째 API 요청 (주소 검색)
        response_pnu = requests.get(baseurl_search, params=params_search)
        response_pnu.raise_for_status()
        logger.debug(f"Search Response: {response_pnu.json()}")
    except requests.exceptions.RequestException as e:
        logger.error(f"API 요청 실패 (주소 검색): {e}")
        raise ValueError(f"API 요청 실패: {e}")
    
    response_json = response_pnu.json()
    
    # 주소 검색 결과 상태 확인
    if response_json.get("response", {}).get("status") == "NOT_FOUND":
        raise ValueError("주소가 없습니다.")
    
    # 검색 결과에서 items 추출
    items = response_json.get("response", {}).get("result", {}).get("items", [])
    if not items:
        raise ValueError("잘못된 주소입니다.")
    
    # PNU 값 추출 및 검증
    pnu = items[0].get("id")
    if not pnu:
        raise ValueError("PNU 값이 없습니다.")
    if len(pnu) != 19:
        raise ValueError("잘못된 PNU 값입니다.")
    
    response_result = {
        "pnu": pnu,
        "adm_cd": pnu[:10]
    }
    logger.debug(f"PNU: {pnu}, adm_cd: {response_result['adm_cd']}")
    
    # 두 번째 API 요청 파라미터 설정
    baseurl_lndpclAr = "https://api.vworld.kr/ned/data/ladfrlList"
    params_lndpclAr = {
        "domain": "https://dronefield.co.kr",
        "pnu": response_result["adm_cd"],
        "format": "json",
        "key": vworld_key
    }
    
    try:
        # 두 번째 API 요청 (lndpclAr 조회)
        response_lndpclAr = requests.get(baseurl_lndpclAr, params=params_lndpclAr)
        response_lndpclAr.raise_for_status()
        logger.debug(f"Land Area Response: {response_lndpclAr.json()}")
    except requests.exceptions.RequestException as e:
        logger.error(f"API 요청 실패 (lndpclAr 조회): {e}")
        raise ValueError(f"API 요청 실패: {e}")
    
    lndpclAr_json = response_lndpclAr.json()
    lndpclAr_list = lndpclAr_json.get("ladfrlVOList", {}).get("ladfrlVOList", [])
    
    if not lndpclAr_list:
        raise ValueError("lndpclAr 값이 없습니다.")
    
    # lndpclAr 값 추출 및 기본값 설정
    lndpclAr = lndpclAr_list[0].get("lndpclAr", 11)
    response_result["lndpclAr"] = lndpclAr
    logger.debug(f"Land Area (lndpclAr): {lndpclAr}")
    
    return response_result
