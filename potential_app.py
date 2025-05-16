import random
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
from io import BytesIO
import urllib.request

# 초기 확률
initial_probs = {
    1: 0.20,
    2: 0.27,
    3: 0.31,
    4: 0.12,
    5: 0.05,
    6: 0.03,
    7: 0.02
}

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

def choose_slots(prob_dict):
    slots = list(prob_dict.keys())
    probs = list(prob_dict.values())
    return random.choices(slots, weights=probs, k=1)[0]

def gradient_rect(ax, xy, width, height, base_color):
    rect = patches.Rectangle(xy, width, height, facecolor=base_color, edgecolor='black', linewidth=1.5, alpha=0.9)
    ax.add_patch(rect)

def load_player_image(url):
    try:
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
        img = Image.open(BytesIO(image_data))
        return img
    except:
        return None

def draw_slots_with_player(additional, player_img):
    total_slots = 15
    fig, ax = plt.subplots(figsize=(15, 4))  # 높이 늘림

    # 왼쪽 텍스트 추가 (x=-1, y=0.9 위치)
    ax.text(-1, 0.9, "장타 억제력", fontsize=16, fontweight='bold', verticalalignment='center')

    # 선수 이미지 크기 조절
    zoom = 0.35
    if player_img:
        imagebox = OffsetImage(player_img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (7.5, 2.1), frameon=False, box_alignment=(0.5, 0))
        ax.add_artist(ab)

    rect_height = 1.8  # 칸 높이 키움

    # 파란색 4칸 (고정)
    for i in range(4):
        gradient_rect(ax, (i, 0), 1, rect_height, "#0033cc")

    # 보라색 4칸 (고정)
    for i in range(4, 8):
        gradient_rect(ax, (i, 0), 1, rect_height, "#660099")

    # 황금색 추가 칸
    for i in range(8, 8 + additional):
        gradient_rect(ax, (i, 0), 1, rect_height, "#FFD700")

    # 빈 칸 흰색
    for i in range(8 + additional, total_slots):
        rect = patches.Rectangle((i, 0), 1, rect_height, facecolor='white', edgecolor='black', linewidth=1.5)
        ax.add_patch(rect)

    ax.set_xlim(-1.5, total_slots)
    ax.set_ylim(0, 3)  # 세로 공간 충분히
    ax.axis('off')
    plt.tight_layout()
    return fig

st.title("🎲 잠재력 시뮬레이터 + 페디 선수")

if "current_additional" not in st.session_state:
    st.session_state.current_additional = choose_slots(initial_probs)

player_img_url = "https://hive-fn.qpyou.cn/webdev/community_cpbv22/upload/20231212_161818_%ED%8E%98%EB%94%94.png"
player_img = load_player_image(player_img_url)

fig = draw_slots_with_player(st.session_state.current_additional, player_img)
st.pyplot(fig)

if st.button("🔁 재설정하기"):
    new_probs = adjust_probs(st.session_state.current_additional)
    st.session_state.current_additional = choose_slots(new_probs)
    st.experimental_rerun()
