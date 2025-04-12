import json
class Tool:
    def __init__(self, name, description, params_schema):
        self.name = name
        self.description = description
        self.params_schema = params_schema
        
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "params": self.params_schema
        }
    
    def execute(self, params):
        # 각 도구마다 오버라이드하여 구현
        raise NotImplementedError
    

def serialize_tools(tools):
    return json.dumps([tool.to_dict() for tool in tools], ensure_ascii=False)

def create_react_prompt(query, tools_json):
    return f"""
    당신은 사용자 질문에 답변하는 AI 어시스턴트입니다. 다음 도구들을 사용할 수 있습니다:
    
    {tools_json}
    
    사용자의 질문에 답하기 위해 다음 형식으로 응답하세요:
    {{
        "thoughts": "문제 해결을 위한 사고 과정",
        "use_tool": true|false,
        "tool_name": "사용할 도구 이름", (use_tool이 true인 경우에만)
        "tool_params": {{도구에 필요한 매개변수}}, (use_tool이 true인 경우에만)
        "answer": "사용자 질문에 대한 최종 답변" (use_tool이 false인 경우에만)
    }}
    
    응답 규칙:
    - 구조화된 JSON 형식으로만 응답해야 합니다
    - ```json 등 Wrapping을 사용하지 말아야 합니다
    - 복잡한 문제는 여러 단계로 나누어 해결하세요
    - 도구를 사용할 때는 정확한 매개변수를 제공하세요
    
    사용자 질문: {query}
    """
