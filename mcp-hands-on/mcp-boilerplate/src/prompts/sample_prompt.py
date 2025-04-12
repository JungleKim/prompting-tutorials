# 샘플 프롬프트 템플릿
SAMPLE_PROMPT = """
당신은 {role} 역할을 하는 AI 비서입니다.

사용자가 요청한 내용: {user_query}

다음 정보를 고려하여 도움을 제공해 주세요:
- {context}

응답 형식:
1. 질문 요약
2. 상세 답변
3. 추가 제안 사항 (해당되는 경우)
"""

# 샘플 프롬프트 변수 기본값
DEFAULT_PROMPT_VARS = {
    "role": "지식 도우미",
    "user_query": "이 질문을 도와주세요",
    "context": "관련 정보나 지식을 여기에 채워넣습니다."
}

def get_formatted_prompt(variables=None):
    """
    변수를 채워 넣은 형식화된 프롬프트를 생성합니다.
    
    Args:
        variables: 프롬프트에 채워 넣을 변수 딕셔너리
        
    Returns:
        형식화된 프롬프트 문자열
    """
    if variables is None:
        variables = DEFAULT_PROMPT_VARS
    
    # 기본값과 제공된 변수 병합
    all_vars = {**DEFAULT_PROMPT_VARS, **variables}
    
    # 프롬프트 형식화
    return SAMPLE_PROMPT.format(**all_vars) 