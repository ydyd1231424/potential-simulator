import random
import streamlit as st
import matplotlib.pyplot as plt

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

def draw_slots(n):
    fig, ax = plt.subplots(figsize=(7, 1))
    for i in range(7):
        rect = plt.Rectangle((i, 0), 1, 1, edgecolor='black',
                             facecolor='black' if i < n else 'white')
        ax.add_patch(rect)
    ax.set_xlim(0, 7)
    ax.set_ylim(0, 1)
    ax.axis('off')
    return fig

st.title("🔲 잠재력 칸수 시뮬레이터")

if "current_slots" not in st.session_state:
    st.session_state.current_slots = choose_slots(initial_probs)

fig = draw_slots(st.session_state.current_slots)
st.pyplot(fig)

if st.button("🔁 재설정하기"):
    new_probs = adjust_probs(st.session_state.current_slots)
    st.session_state.current_slots = choose_slots(new_probs)
    st.experimental_rerun()
