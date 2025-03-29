
import json
import time
import tiktoken


def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    텍스트의 토큰 수를 계산합니다.
    
    Args:
        text (str): 토큰 수를 계산할 텍스트
        model (str): 토큰화에 사용할 모델
        
    Returns:
        int: 토큰 수
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except KeyError:
        # 모델이 tiktoken에 없을 경우 기본 인코딩 사용
        print(f"경고: {model}에 대한 토큰 인코딩을 찾을 수 없습니다. cl100k_base를 사용합니다.")
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))


def print_with_token_count(text: str, model: str = "gpt-3.5-turbo") -> None:
    """
    텍스트와 함께 토큰 수를 출력합니다.
    
    Args:
        text (str): 출력할 텍스트
        model (str): 토큰화에 사용할 모델
    """
    token_count = count_tokens(text, model)
    print(f"{text}\n\n토큰 수: {token_count}")

def log_interaction(log_file: str = "interactions.json"):
    """
    프롬프트와 응답을 로그 파일에 기록하는 데코레이터.
    
    Args:
        log_file (str): 로그 파일 경로
        
    Returns:
        callable: 데코레이터 함수
    """
    def decorator(func):
        from functools import wraps
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 원래 함수 실행
            result = func(*args, **kwargs)
            
            # 프롬프트와 응답 추출
            if func.__name__ == "get_completion":
                prompt = args[0] if args else kwargs.get("prompt", "")
                response = result
            elif func.__name__ == "get_chat_completion":
                prompt = json.dumps([msg.get("content", "") for msg in args[0]], ensure_ascii=False) if args else json.dumps([msg.get("content", "") for msg in kwargs.get("messages", [])], ensure_ascii=False)
                response = result
            else:
                # 다른 함수에도 적용 가능하도록 일반적인 로깅
                prompt = str(args) + str(kwargs)
                response = str(result)
            
            # 로그 저장
            log_entry = {
                "timestamp": time.time(),
                "function": func.__name__,
                "prompt": prompt,
                "response": response,
                "token_count": {
                    "prompt": count_tokens(prompt),
                    "response": count_tokens(response),
                    "total": count_tokens(prompt) + count_tokens(response)
                }
            }
            
            logs = []
            if os.path.exists(log_file):
                with open(log_file, "r", encoding="utf-8") as f:
                    try:
                        logs = json.load(f)
                    except json.JSONDecodeError:
                        logs = []
            
            logs.append(log_entry)
            
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
                
            return result
        
        return wrapper
    
    return decorator

