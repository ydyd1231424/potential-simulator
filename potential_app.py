import random
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
from io import BytesIO
import urllib.request
import matplotlib.font_manager as fm

def get_korean_font():
    candidates = ['Malgun Gothic', '맑은 고딕', 'NanumGothic', '나눔고딕', 'AppleGothic', 'Apple SD Gothic Neo']
    font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
    font_names = [fm.FontProperties(fname=fp).get_name() for fp in font_list]
    for c in candidates:
        if c in font_names:
            return c
    return None

korean_font = get_korean_font()
if korean_font:
    plt.rcParams['font.family'] = korean_font
else:
    print("한글 폰트를 찾지 못했습니다. 한글이 깨질 수 있습니다.")

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

    zoom = 0.35
    if player_img:
        imagebox = OffsetImage(player_img, zoom=zoom)
        ab = AnnotationBbox(imagebox, (total_slots/2, 2.1), frameon=False, box_alignment=(0.5, 0))
        ax.add_artist(ab)

    rect_height = 1.8

    # 좌우 균형 맞추기 위해 전체 너비 기준으로 시작점 조절
    # 총 15칸, x축 0~15이므로 0부터 그리기
    start_x = 0

    # 파란색 4칸 (고정)
    for i in range(4):
        gradient_rect(ax, (start_x + i, 0), 1, rect_height, "#0033cc")
    # 보라색 4칸 (고정)
    for i in range(4, 8):
        gradient_rect(ax, (start_x + i, 0), 1, rect_height, "#660099")
    # 황금색 추가 칸
    for i in range(8, 8 + additional):
        gradient_rect(ax, (start_x + i, 0), 1, rect_height, "#FFD700")
    # 빈 칸 흰색
    for i in range(8 + additional, total_slots):
        rect = patches.Rectangle((start_x + i, 0), 1, rect_height, facecolor='white', edgecolor='black', linewidth=1.5)
        ax.add_patch(rect)

    # 추가 칸수가 7이고 전체 15칸일 때 'SR+' 텍스트 추가
    if additional == 7:
        # SR+ 텍스트 위치: 오른쪽 끝 황금 칸 바로 위 (x좌표, y좌표 조정)
        sr_x = start_x + 8 + additional - 0.5  # 추가칸 중 마지막 칸 중앙쯤
        sr_y = rect_height + 0.3  # 칸 위쪽으로 약간 띄움
        ax.text(sr_x, sr_y, "SR+", fontsize=28, fontweight='bold', color='#FFD700', verticalalignment='bottom', horizontalalignment='center')

    # x축 0~15 칸 만큼 범위 설정 (start_x 기준)
    ax.set_xlim(start_x - 0.5, start_x + total_slots + 0.5)
    ax.set_ylim(0, 3)
    ax.axis('off')
    plt.tight_layout()
    return fig

st.title("각성 잠재 시뮬레이터")

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
