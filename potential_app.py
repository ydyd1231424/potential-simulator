import random
import streamlit as st
import matplotlib.pyplot as plt

# 초기 확률 정의
initial_probs = {
    1: 0.20,
    2: 0.27,
    3: 0.31,
    4: 0.12,
    5: 0.05,
    6: 0.03,
    7: 0.02
}

# 현재 칸 제외 후 확률 조정 (3칸은 보정)
def adjust_probs(current):
    new_probs = initial_probs.copy()
    if current in new_probs:
        del new_probs[current]
    if current == 3:
        total = sum(new_probs.values())
        scale = 1 / total
        for k in new_probs:
            new_probs[k] *= scale
    return new_probs

# 확률에 따라 칸수 선택
def choose_slots(prob_dict):
    slots = list(prob_dict.keys())
    probs = list(prob_dict.values())
    return random.choices(slots, weights=probs, k=1)[0]

# 전체 슬롯 이미지 그리기
def draw_slots(additional):
    total_slots = 8 + additional
    fig, ax = plt.subplots(figsize=(total_slots, 1.5))

    # 파랑 4칸
    for i in range(4):
        rect = plt.Rectangle((i, 0), 1, 1, facecolor='blue', edgecolor='black', linewidth=1.5)
        ax.add_patch(rect)

    # 보라 4칸
    for i in range(4, 8):
        rect = plt.Rectangle((i, 0), 1, 1, facecolor='purple', edgecolor='black', linewidth=1.5)
        ax.add_patch(rect)

    # 황금 추가칸
    for i in range(8, total_slots):
        rect = plt.Rectangle((i, 0), 1, 1, facecolor='gold', edgecolor='black', linewidth=1.5)
        ax.add_patch(rect)

    ax.set_xlim(0, total_slots)
    ax.set_ylim(0, 1)
    ax.axis('off')
    return fig

# Streamlit 앱
st.title("🎲 잠재력 시뮬레이터")

if "current_additional" not in st.session_state:
    st.session_state.current_additional = choose_slots(initial_probs)

# 시각화
fig = draw_slots(st.session_state.current_additional)
st.pyplot(fig)

# 재설정 버튼
if st.button("🔁 재설정하기"):
    new_probs = adjust_probs(st.session_state.current_additional)
    st.session_state.current_additional = choose_slots(new_probs)
    st.experimental_rerun()
