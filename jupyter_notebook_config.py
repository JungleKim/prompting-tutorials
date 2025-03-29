"""
프롬프트 엔지니어링 실습 프로젝트를 위한 JupyterLab 설정 파일
"""

c = get_config()  # noqa

# 기본 설정
c.ServerApp.open_browser = True
c.ServerApp.ip = '127.0.0.1'
c.ServerApp.port = 8888

# 노트북 자동 저장 간격 (30초)
c.ContentsManager.autosave_interval = 30

# 노트북 실행 타임아웃 (60초)
c.MappingKernelManager.kernel_info_timeout = 60

# 커널이 응답하지 않을 때 자동으로 재시작하는 설정
c.KernelManager.autorestart = True

# 마크다운 셀에서 MathJax 렌더링 활성화
c.ServerApp.enable_mathjax = True

# 파일 확장자별 처리기 설정
c.ServerApp.contents_manager_class = 'jupyter_server.services.contents.largefilemanager.LargeFileManager'

# 코드 실행 설정
c.ExecutePreprocessor.enabled = True
c.ExecutePreprocessor.timeout = 180  # 셀 실행 타임아웃 (180초)
c.ExecutePreprocessor.clear_before_execute = True  # 셀 실행 전에 출력 정리

# 출력 제한 설정
c.ServerApp.iopub_data_rate_limit = 10000000  # 출력 데이터 속도 제한 (바이트/초)
c.ServerApp.iopub_msg_rate_limit = 1000  # 출력 메시지 속도 제한 (메시지/초)
c.ServerApp.clear_output_timeout = 60  # 60초 동안 출력이 없으면 자동으로 정리

# IPython 자동 출력 개수 제한
c.InteractiveShell.cache_size = 5  # 출력 캐시 크기 제한
c.InteractiveShell.pprint = True  # 예쁘게 출력

# JupyterLab 특정 설정
c.ServerApp.terminado_settings = {'shell_command': ['/bin/bash']}  # 터미널 셸 설정

# JupyterLab 인터페이스 설정
c.ServerApp.cleanup_kernels = True
c.JupyterLab.clean_on_startup = True

# 로깅 레벨 설정
c.Application.log_level = 'INFO'

# 기본 애플리케이션으로 JupyterLab 사용
c.ServerApp.default_url = '/lab' 