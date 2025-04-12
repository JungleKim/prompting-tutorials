import json
from typing import Dict, Any

# 샘플 데이터
SAMPLE_DATA = {
    "name": "샘플 리소스",
    "type": "텍스트",
    "contents": [
        "이것은 MCP 리소스 예제입니다.",
        "리소스는 LLM이 읽을 수 있는 데이터를 제공합니다."
    ],
    "metadata": {
        "author": "MCP 보일러플레이트",
        "version": "1.0.0"
    }
}

async def get_sample_resource() -> str:
    """
    샘플 리소스 데이터를 가져옵니다.
    
    Returns:
        형식화된 리소스 데이터 문자열
    """
    # JSON 형식으로 변환 (필요시 다른 형식으로 변경 가능)
    return json.dumps(SAMPLE_DATA, ensure_ascii=False, indent=2)

async def get_resource_by_id(resource_id: str) -> Dict[str, Any]:
    """
    ID로 리소스를 가져오는 예제 함수입니다.
    
    Args:
        resource_id: 리소스 ID
        
    Returns:
        리소스 데이터 딕셔너리
    """
    # 실제 구현에서는 데이터베이스나 API에서 가져올 수 있습니다
    return SAMPLE_DATA 