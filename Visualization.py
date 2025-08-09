#1. HANK 모델 계산 구조도
from graphviz import Digraph

# 구조도 객체 생성
dot = Digraph(comment='HANK Model Structure')
dot.attr(rankdir='TB', splines='ortho', nodesep='1.0') # 세로 방향, 직선 연결

# 노드 스타일 설정
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue', fontname='Malgun Gothic')

# 외부 루프 (일반 균형)
with dot.subgraph(name='cluster_outer') as c:
    c.attr(label='외부 루프 (Outer Loop): 일반 균형 (GE)', style='rounded', color='grey', fontname='Malgun Gothic', fontsize='16')
    c.node('GE_Loop', '시장 청산 가격(r, w) 찾기', height='1.2')
    
    # 내부 루프 (부분 균형)
    with c.subgraph(name='cluster_inner') as sc:
        sc.attr(label='내부 루프 (Inner Loop): 부분 균형 (PE)', style='rounded', color='dimgrey', fontname='Malgun Gothic', fontsize='14')
        sc.node('PE_Loop', '주어진 가격(r, w) 하에서\n가계 최적화 문제 풀이 (HJB)', height='1.2')

# 파일로 저장
dot.render('hank_structure', format='png', view=True)

print("'hank_structure.png' 파일이 생성되었습니다.")

#2. GE Solver 상세 순서도 
from graphviz import Digraph

# 순서도 객체 생성
dot = Digraph(comment='HANK GE Solver Flowchart')
dot.attr(rankdir='TB', splines='ortho', nodesep='0.6', compound='true') # 세로 방향, 직선 연결

# 노드 스타일 기본 설정
dot.attr('node', shape='box', style='rounded,filled', fontname='Malgun Gothic')

# --- 외부 루프 및 전역 노드 정의 ---
dot.node('A', 'Start: GE Solver', shape='ellipse', fillcolor='lightgrey')
dot.node('B', '1. 초기 가격 추측 (r, w)\n[SolveSteadyStateEqum.f90],\n[InitialSteadyState.f90]', fillcolor='#f9f2ff') # 보라색 계열
dot.node('E', '3. 정상상태 분포 계산 (KFE)\n[StationaryDistribution.f90]', fillcolor='#ebf2ff')
dot.node('F', '4. 총량 변수 계산 (Aggregation)\n[DistributionStatistics.f90]', fillcolor='#ebf2ff')
dot.node('G', '5. 시장 청산 확인\n(자본 수요 == 공급?)\n[SolveSteadyStateEqum.f90]', shape='diamond', fillcolor='#ffffcc')
dot.node('H', '6. 가격 업데이트 (r, w 조정)\n[FnDiscountRate.f90]', fillcolor='#f9f2ff')
dot.node('I', 'End: 균형 찾음!', shape='ellipse', fillcolor='#dff0d8') # 녹색 계열

# --- 내부 루프(HJB)를 별도의 클러스터(박스)로 묶어 표현 ---
with dot.subgraph(name='cluster_hjb') as c:
    c.attr(label='내부 루프: 가계 문제 풀이\n[IterateBellman.f90]', style='rounded', color='dimgrey', fontname='Malgun Gothic', fontsize='14')
    c.attr('node', shape='box', style='rounded,filled', fontname='Malgun Gothic', fillcolor='#ebf2ff')
    
    # 내부 루프의 노드 정의
    c.node('C', '2. HJB 방정식 1회 반복 수행\n[HJBUpdate.f90]')
    c.node('D', '가치함수 V 수렴?', shape='diamond')

    # 내부 루프의 흐름 정의
    c.edge('C', 'D')
    c.edge('D', 'C', label=' No', fontname='Malgun Gothic')

# --- 전체 흐름 연결 ---
dot.edge('A', 'B')
dot.edge('B', 'C', lhead='cluster_hjb') # 외부 -> 내부 루프 진입
dot.edge('D', 'E', ltail='cluster_hjb', label=' Yes', fontname='Malgun Gothic') # 내부 -> 외부 루프 탈출
dot.edge('E', 'F')
dot.edge('F', 'G')
dot.edge('G', 'H', label=' No (불균형)', fontname='Malgun Gothic')
dot.edge('H', 'C', lhead='cluster_hjb') # 외부 루프 -> 내부 루프 재진입
dot.edge('G', 'I', label=' Yes (균형)', fontname='Malgun Gothic')

# 파일로 저장
dot.render('hank_solver_flowchart', format='png', view=True)

print("'hank_solver_flowchart.png' 파일이 생성되었습니다.")