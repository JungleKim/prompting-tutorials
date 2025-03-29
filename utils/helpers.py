"""
프롬프트 엔지니어링 실습을 위한 유틸리티 함수 모음
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from openai import OpenAI
from log import log_interaction

# 기본 모델 설정
DEFAULT_MODEL = "gpt-4o"
FALLBACK_MODELS = ["gpt-4o-mini", "gpt-3.5-turbo"]

# .env 파일 로드
load_dotenv()

def get_available_model(api_key):
    """
    사용 가능한 모델을 찾는 함수
    
    Args:
        api_key (str): OpenAI API 키
        
    Returns:
        str: 사용 가능한 모델 이름
    """
    # 환경 변수에서 모델명 가져오기
    model = os.getenv("MODEL", DEFAULT_MODEL)
    
    # 클라이언트 초기화
    client = OpenAI(api_key=api_key)
    
    try:
        # 설정된 모델로 테스트 요청
        client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "테스트"}],
            max_tokens=5
        )
        # 성공하면 해당 모델 반환
        return model
    except Exception as e:
        print(f"경고: 모델 '{model}'을 사용할 수 없습니다. 오류: {str(e)}")
        print("대체 모델을 시도합니다...")
        
        # 대체 모델 시도
        for fallback_model in FALLBACK_MODELS:
            try:
                client.chat.completions.create(
                    model=fallback_model,
                    messages=[{"role": "user", "content": "테스트"}],
                    max_tokens=5
                )
                print(f"'{fallback_model}' 모델을 사용합니다.")
                return fallback_model
            except Exception:
                continue
    
    # 모든 모델이 실패하면 기본값 반환
    print(f"경고: 모든 모델 시도가 실패했습니다. 기본 모델 '{DEFAULT_MODEL}'을 사용합니다.")
    return DEFAULT_MODEL

# API 키와 모델 초기화
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

# 사용 가능한 모델 확인
CURRENT_MODEL = get_available_model(api_key)

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=api_key)

@log_interaction()
def get_completion(
    prompt: str,
    model: str = CURRENT_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 1000,
    stop: Optional[List[str]] = None
) -> str:
    """
    OpenAI API를 사용하여 프롬프트에 대한 응답을 받습니다.
    
    Args:
        prompt (str): 모델에게 보낼 프롬프트
        model (str): 사용할 모델 이름
        temperature (float): 응답의 창의성 정도 (0.0 ~ 1.0)
        max_tokens (int): 응답의 최대 토큰 수
        stop (List[str], optional): 생성을 중단시키는 토큰 목록
        
    Returns:
        str: 모델의 응답
    """
    try:
        messages = [{"role": "user", "content": prompt}]
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = f"API 호출 중 오류 발생: {str(e)}"
        print(error_msg)
        # 모델 오류시 폴백 시도
        if model != FALLBACK_MODELS[-1]:  # 마지막 폴백 모델이 아니면
            print(f"{FALLBACK_MODELS[-1]} 모델로 재시도합니다...")
            return get_completion(
                prompt, 
                model=FALLBACK_MODELS[-1], 
                temperature=temperature, 
                max_tokens=max_tokens, 
                stop=stop
            )
        return error_msg


@log_interaction()
def get_chat_completion(
    messages: List[Dict[str, str]],
    model: str = CURRENT_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 2000
) -> str:
    """
    OpenAI API를 사용하여 채팅 형식의 프롬프트에 대한 응답을 받습니다.
    
    Args:
        messages (List[Dict[str, str]]): 대화 메시지 목록
        model (str): 사용할 모델 이름
        temperature (float): 응답의 창의성 정도 (0.0 ~ 1.0)
        max_tokens (int): 응답의 최대 토큰 수
        
    Returns:
        str: 모델의 응답
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = f"API 호출 중 오류 발생: {str(e)}"
        print(error_msg)
        # 모델 오류시 폴백 시도
        if model != FALLBACK_MODELS[-1]:  # 마지막 폴백 모델이 아니면
            print(f"{FALLBACK_MODELS[-1]} 모델로 재시도합니다...")
            return get_chat_completion(
                messages, 
                model=FALLBACK_MODELS[-1], 
                temperature=temperature, 
                max_tokens=max_tokens
            )
        return error_msg



def create_few_shot_prompt(
    instruction: str,
    examples: List[Dict[str, str]],
    query: str
) -> str:
    """
    Few-shot 프롬프트를 생성합니다.
    
    Args:
        instructions (str): 모델에게 줄 지시사항
        examples (List[Dict[str, str]]): 예시 목록 (각 예시는 'input'과 'output' 키를 포함)
        query (str): 실제 질문
        
    Returns:
        str: 완성된 프롬프트
    """
    prompt = instruction + "\n\n"
    
    # 예시 추가
    for i, example in enumerate(examples):
        prompt += f"예시 {i+1}:\n"
        prompt += f"입력: {example['input']}\n"
        prompt += f"출력: {example['output']}\n\n"
    
    # 실제 질문 추가
    prompt += f"이제 다음 입력에 대한 출력을 생성해주세요:\n"
    prompt += f"입력: {query}\n"
    prompt += f"출력:"
    
    return prompt 