import time
import json
from typing import List, Dict, Any, Optional

class ToolUsageTracker:
    def __init__(self):
        """도구 사용 기록 관리자 초기화"""
        self.tool_usage_history: List[Dict[str, Any]] = []
    
    def record_usage(self, tool_name: str, params: Dict[str, Any], result: Any, success: bool = True) -> None:
        """
        도구 사용 기록 추가
        
        Args:
            tool_name (str): 사용된 도구 이름
            params (Dict[str, Any]): 도구에 전달된 매개변수
            result (Any): 도구 실행 결과
            success (bool): 도구 실행 성공 여부
        """
        self.tool_usage_history.append({
            "timestamp": time.time(),
            "tool": tool_name,
            "params": params,
            "result": result,
            "success": success
        })
    
    def get_relevant_history(self, query: str, max_items: int = 3) -> List[Dict[str, Any]]:
        """
        현재 쿼리와 관련된 도구 사용 기록 검색
        
        Args:
            query (str): 검색할 쿼리
            max_items (int): 반환할 최대 기록 수
            
        Returns:
            List[Dict[str, Any]]: 관련된 도구 사용 기록 목록
        """
        relevant_history = []
        query_keywords = set(query.lower().split())
        
        for usage in reversed(self.tool_usage_history):
            # 도구 사용 기록을 문자열로 변환하여 키워드 매칭
            params_str = json.dumps(usage["params"], ensure_ascii=False).lower()
            result_str = str(usage["result"]).lower()
            
            # 쿼리의 키워드가 파라미터나 결과에 포함되어 있는지 확인
            if any(keyword in params_str or keyword in result_str for keyword in query_keywords):
                relevant_history.append(usage)
                
                if len(relevant_history) >= max_items:
                    break
        
        return relevant_history
    
    def get_tool_statistics(self) -> Dict[str, Dict[str, Any]]:
        """
        도구별 사용 통계 반환
        
        Returns:
            Dict[str, Dict[str, Any]]: 도구별 사용 횟수 및 성공률
        """
        stats = {}
        
        for usage in self.tool_usage_history:
            tool_name = usage["tool"]
            if tool_name not in stats:
                stats[tool_name] = {
                    "total_uses": 0,
                    "successful_uses": 0,
                    "success_rate": 0.0
                }
            
            stats[tool_name]["total_uses"] += 1
            if usage["success"]:
                stats[tool_name]["successful_uses"] += 1
            
            # 성공률 계산
            total = stats[tool_name]["total_uses"]
            successful = stats[tool_name]["successful_uses"]
            stats[tool_name]["success_rate"] = (successful / total) * 100
        
        return stats 