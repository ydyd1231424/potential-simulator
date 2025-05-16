import random
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.colors import LinearSegmentedColormap
import urllib.request
from PIL import Image
from io import BytesIO

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
    fig, ax = plt.subplots(figsize=(15, 3))  # 세로 공간 여유

    # 선수 이미지 크기 조절
    zoom = 0.3
    if player_img:
        imagebox = OffsetImage(player_img, zoom=zoom)
        # 선수 이미지를 칸 중앙 위쪽에 위치시키기 (x축: 7.5 = 15칸의 중간, y축: 1.5 위쪽)
        ab = AnnotationBbox(imagebox, (7.5, 1.5), frameon=False, box_alignment=(0.5, 0))
        ax.add_artist(ab)

    # 파란색 4칸
    for i in range(4):
        gradient_rect(ax, (i, 0), 1, 1, "#0033cc")

    # 보라색 4칸
    for i in range(4, 8):
        gradient_rect(ax, (i, 0), 1, 1, "#660099")

    # 황금색 추가 칸
    for i in range(8, 8 + additional):
        gradient_rect(ax, (i, 0), 1, 1, "#FFD700")

    # 빈 칸 흰색
    for i in range(8 + additional, total_slots):
        rect = patches.Rectangle((i, 0), 1, 1, facecolor='white', edgecolor='black', linewidth=1.5)
        ax.add_patch(rect)

    ax.set_xlim(0, total_slots)
    ax.set_ylim(0, 2)  # 세로 높이 늘림 (이미지 공간)
    ax.axis('off')
    plt.tight_layout()
    return fig

st.title("🎲 잠재력 시뮬레이터 + 페디 선수")

if "current_additional" not in st.session_state:
    st.session_state.current_additional = choose_slots(initial_probs)

player_img_url = "https://cpbv-community.com2us.com/image/2022-04-22-XaO1512wDw6VURt.png"
player_img = load_player_image(player_img_url)

fig = draw_slots_with_player(st.session_state.current_additional, player_img)
st.pyplot(fig)

if st.button("🔁 재설정하기"):
    new_probs = adjust_probs(st.session_state.current_additional)
    st.session_state.current_additional = choose_slots(new_probs)
    st.experimental_rerun()
