from typing import List, Optional
from .helpers import get_chat_completion

# 노드 클래스 정의
class ThoughtNode:
    def __init__(self, content: str, parent=None, depth: int = 0):
        self.content = content
        self.parent = parent
        self.depth = depth
        self.children = []
        self.evaluation_score = None
    
    def add_child(self, child_node):
        self.children.append(child_node)
        
    def get_path_from_root(self):
        """루트부터 현재 노드까지의 경로를 반환합니다."""
        path = []
        current = self
        while current:
            path.append(current.content)
            current = current.parent
        return list(reversed(path))
    
    def __str__(self):
        return f"ThoughtNode(depth={self.depth}, content='{self.content[:50]}...', score={self.evaluation_score})"

# 초기 사고 생성 함수
def generate_initial_thoughts(problem: str, branching_factor: int) -> ThoughtNode:
    """문제에 대한 초기 접근법을 생성합니다."""
    messages = [{
        "role": "user",
        "content": f"""
        문제: {problem}
        
        이 문제에 접근할 수 있는 {branching_factor}가지 서로 다른 시작점을 생각해보세요. 
        각 접근법은 명확하고 구체적이어야 합니다.
        
        접근법 1:
        """
    }]
    
    try:
        content = get_chat_completion(messages, temperature=0.7)
        
        # 루트 노드 생성
        root = ThoughtNode(f"문제: {problem}\n\n{content}", depth=0)
        return root
    
    except Exception as e:
        print(f"초기 사고 생성 중 오류 발생: {e}")
        # 오류 발생 시 기본 노드 반환
        return ThoughtNode(f"문제: {problem}\n\n접근법을 생성할 수 없습니다.", depth=0)

# 사고 평가 함수
def evaluate_thought(node: ThoughtNode, problem: str) -> float:
    """현재 사고 노드의 유망성을 평가합니다."""
    path = node.get_path_from_root()
    current_reasoning = "\n".join(path)
    
    messages = [{
        "role": "user",
        "content": f"""
        문제: {problem}
        
        지금까지의 추론 과정:
        {current_reasoning}
        
        위 추론 과정이 문제 해결에 얼마나 유망한지 1-10 점 사이의 점수로 평가해주세요.
        평가 기준:
        - 논리적 타당성
        - 문제 해결 가능성
        - 접근법의 창의성
        - 효율성
        
        점수만 숫자로 응답해주세요.
        """
    }]
    
    try:
        score_text = get_chat_completion(messages, temperature=0.3, max_tokens=10)
        # 숫자가 아닌 문자 제거
        score_text = ''.join(c for c in score_text if c.isdigit() or c == '.')
        
        if score_text:
            score = float(score_text)
            # 점수 범위 제한
            score = max(1, min(10, score))
            node.evaluation_score = score
            return score
        else:
            # 숫자를 추출할 수 없는 경우 기본값 반환
            node.evaluation_score = 5.0
            return 5.0
    
    except Exception as e:
        print(f"사고 평가 중 오류 발생: {e}")
        # 오류 발생 시 기본 점수 반환
        node.evaluation_score = 5.0
        return 5.0

# 해결책 확인 함수
def is_solution(node: ThoughtNode, problem: str) -> bool:
    """현재 노드가 문제의 해결책인지 확인합니다."""
    if node.depth < 2:  # 최소 깊이 요구 (너무 빨리 종료되는 것 방지)
        return False
    
    path = node.get_path_from_root()
    current_reasoning = "\n".join(path)
    
    messages = [{
        "role": "user",
        "content": f"""
        문제: {problem}
        
        지금까지의 추론 과정:
        {current_reasoning}
        
        위 추론 과정이 문제의 완전한 해결책을 제공하나요? 예/아니오로만 답변해주세요.
        """
    }]
    
    try:
        answer = get_chat_completion(messages, temperature=0.3, max_tokens=10)
        return "예" in answer.lower() or "yes" in answer.lower()
    
    except Exception as e:
        print(f"해결책 확인 중 오류 발생: {e}")
        return False

# 유망성 확인 함수
def is_promising(evaluation_score: float, threshold: float = 5.0) -> bool:
    """평가 점수가 임계값을 넘는지 확인합니다."""
    return evaluation_score >= threshold

# 사고 확장 함수
def expand_thought(node: ThoughtNode, branching_factor: int) -> List[ThoughtNode]:
    """현재 사고를 확장하여 여러 다음 단계 사고를 생성합니다."""
    path = node.get_path_from_root()
    current_reasoning = "\n".join(path)
    
    messages = [{
        "role": "user",
        "content": f"""
        문제: {path[0].split('문제: ')[1] if '문제: ' in path[0] else path[0]}
        
        지금까지의 추론 과정:
        {current_reasoning}
        
        위 추론을 계속 진행하려면, 다음에 고려할 수 있는 {branching_factor}가지 다른 방향은 무엇인가요?
        각 방향은 구체적이고 서로 다른 접근법이어야 합니다.
        
        다음 단계 1:
        """
    }]
    
    try:
        content = get_chat_completion(messages, temperature=0.7)
        
        # 각 접근법 분리하기 위한 마커 생성
        markers = [f"다음 단계 {i+1}:" for i in range(branching_factor)]
        markers.append("END_OF_RESPONSE")  # 끝 표시
        
        # 접근법 분리
        thoughts = []
        for i in range(len(markers)-1):
            start_marker = markers[i]
            end_marker = markers[i+1]
            
            start_idx = content.find(start_marker)
            if start_idx == -1:
                continue
                
            start_idx += len(start_marker)
            end_idx = content.find(end_marker, start_idx) if end_marker in content else len(content)
            
            thought_content = content[start_idx:end_idx].strip()
            if thought_content:
                child_node = ThoughtNode(thought_content, parent=node, depth=node.depth+1)
                node.add_child(child_node)
                thoughts.append(child_node)
        
        # 명시적인 마커가 없는 경우, 전체 응답을 하나의 사고로 처리
        if not thoughts and content:
            child_node = ThoughtNode(content, parent=node, depth=node.depth+1)
            node.add_child(child_node)
            thoughts.append(child_node)
            
        return thoughts
    
    except Exception as e:
        print(f"사고 확장 중 오류 발생: {e}")
        # 오류 발생 시 빈 리스트 반환
        return []

# 최상위 K개 선택 함수
def select_top_k(nodes: List[ThoughtNode], k: int) -> List[ThoughtNode]:
    """평가 점수가 가장 높은 상위 K개 노드를 선택합니다."""
    if not nodes:
        return []
    
    # 평가 점수로 정렬
    sorted_nodes = sorted(nodes, key=lambda x: x.evaluation_score if x.evaluation_score is not None else 0, reverse=True)
    
    # 상위 K개 반환
    return sorted_nodes[:min(k, len(sorted_nodes))]

# 최선의 해결책 선택 함수
def select_best_solution(nodes: List[ThoughtNode]) -> Optional[ThoughtNode]:
    """가장 평가 점수가 높은 노드를 최종 해결책으로 선택합니다."""
    if not nodes:
        return None
    
    # 평가 점수로 정렬
    sorted_nodes = sorted(nodes, key=lambda x: x.evaluation_score if x.evaluation_score is not None else 0, reverse=True)
    
    return sorted_nodes[0] if sorted_nodes else None

# 메인 Tree of Thoughts 함수
def tree_of_thoughts(problem: str, max_steps: int = 3, branching_factor: int = 3, beam_width: int = 2):
    """Tree of Thoughts 알고리즘을 BFS 전략으로 실행합니다."""
    print(f"문제: {problem}")
    print(f"최대 단계: {max_steps}, 분기 계수: {branching_factor}, 빔 너비: {beam_width}")
    print("Tree of Thoughts 탐색을 시작합니다...")
    
    # 초기 상태 설정
    root = generate_initial_thoughts(problem, branching_factor)
    print(f"초기 사고 생성 완료: {root.content[:100]}...")
    
    # BFS 탐색
    frontier = [root]
    all_nodes = [root]  # 생성된 모든 노드 추적
    
    for step in range(max_steps):
        print(f"\n===== 단계 {step+1}/{max_steps} =====")
        next_frontier = []
        
        for i, node in enumerate(frontier):
            print(f"\n[노드 {i+1}/{len(frontier)}] 평가 중...")
            # 각 노드에 대해 평가
            evaluation = evaluate_thought(node, problem)
            print(f"평가 점수: {evaluation}/10")
            
            # 해결책 확인
            if is_solution(node, problem):
                print("해결책 발견!")
                return node
            
            # 유망한 노드만 확장
            if is_promising(evaluation):
                print("유망한 노드로 판단되어 확장합니다...")
                # 새로운 사고 생성 및 확장
                children = expand_thought(node, branching_factor)
                print(f"{len(children)}개의 하위 사고 생성됨")
                next_frontier.extend(children)
                all_nodes.extend(children)
            else:
                print("유망하지 않은 노드로 판단되어 확장하지 않습니다.")
        
        # 다음 단계로 이동
        frontier = select_top_k(next_frontier, k=beam_width)
        print(f"\n다음 단계로 {len(frontier)}/{len(next_frontier)}개 노드 선택됨")
        
        if not frontier:
            print("더 이상 탐색할 노드가 없습니다.")
            break
    
    # 최종 선택
    best_solution = select_best_solution(all_nodes)
    if best_solution:
        print("\n===== 최종 해결책 =====")
        path = best_solution.get_path_from_root()
        for i, step in enumerate(path):
            print(f"\n[단계 {i}] {step}")
        print(f"\n최종 평가 점수: {best_solution.evaluation_score}/10")
    else:
        print("\n해결책을 찾지 못했습니다.")
    
    return best_solution

if __name__ == "__main__":
    problem = "온라인 쇼핑몰의 고객 이탈률을 줄이기 위한 전략을 세워보세요."
    solution = tree_of_thoughts(
        problem=problem,
        max_steps=3,  # 최대 단계 수
        branching_factor=3,  # 각 노드에서 생성할 하위 사고 수
        beam_width=2  # 각 단계에서 유지할 상위 노드 수
    )