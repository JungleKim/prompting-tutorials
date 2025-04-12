from typing import List, Dict, Any
from .helpers import get_completion

class ConversationManager:
    def __init__(self, max_tokens: int = 4000):
        """
        대화 관리자 초기화
        
        Args:
            max_tokens (int): 최대 허용 토큰 수
        """
        self.messages: List[Dict[str, str]] = []
        self.summary: str = ""
        self.max_tokens: int = max_tokens
        self.current_tokens: int = 0
    
    def add_message(self, role: str, content: str) -> None:
        """
        새 메시지 추가
        
        Args:
            role (str): 메시지 작성자의 역할 ('user', 'assistant', 'system' 등)
            content (str): 메시지 내용
        """
        msg = {"role": role, "content": content}
        tokens = self._estimate_tokens(content)
        
        # 최대 토큰 초과 시 요약 생성
        if self.current_tokens + tokens > self.max_tokens:
            self._summarize_conversation()
        
        self.messages.append(msg)
        self.current_tokens += tokens
    
    def _summarize_conversation(self) -> None:
        """대화 내용을 요약하고 메시지 목록 업데이트"""
        conversation = "\n".join([f"{m['role']}: {m['content']}" for m in self.messages])
        
        prompt = f"""
        다음은 이전 대화입니다:
        {conversation}
        
        기존 요약:
        {self.summary}
        
        이전 대화를 간결하게 요약하되, 중요한 정보는 모두 유지하세요.
        """
        
        self.summary = get_completion(prompt)
        
        # 요약으로 메시지 대체
        self.messages = [{"role": "system", "content": f"이전 대화 요약: {self.summary}"}]
        self.current_tokens = self._estimate_tokens(self.summary)
    
    def _estimate_tokens(self, text: str) -> int:
        """
        텍스트의 토큰 수 추정
        
        Args:
            text (str): 토큰 수를 추정할 텍스트
            
        Returns:
            int: 추정된 토큰 수
        """
        # 간단한 토큰 추정 (실제로는 더 정확한 토크나이저 사용)
        return int(len(text.split()) * 1.3)
    
    def get_context(self) -> List[Dict[str, str]]:
        """
        현재 대화 컨텍스트 반환
        
        Returns:
            List[Dict[str, str]]: 대화 메시지 목록
        """
        return self.messages 