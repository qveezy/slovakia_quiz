import random
import unicodedata as uni
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Slovakia Districts Quiz", layout="centered")


@st.cache_data
def load_data():
    return gpd.read_file("data/GeoJSON/epsg_3395/districts_epsg_3395.geojson")


def normalize_name(text: str) -> str:
    decomposed = uni.normalize("NFD", text)
    clean_chars = [char for char in decomposed if uni.category(char) != "Mn"]
    clean_str = "".join(clean_chars).lower()
    clean_str = clean_str.replace("-", " ")
    return " ".join(clean_str.split())


gdf = load_data()
total_districts = len(gdf)
all_names = gdf["NM3"].tolist()

# --- Sidebar Settings ---
st.sidebar.header("Game Settings")
mode = st.sidebar.radio("Choose Mode", ["Normal (Text Input)", "4 Variants (Buttons)"])
num_rounds = st.sidebar.slider(
    "Number of rounds (Max = All)",
    min_value=1,
    max_value=total_districts,
    value=total_districts,
)


def start_new_game(custom_indices=None):
    if custom_indices is not None:
        st.session_state.indices = list(custom_indices)
        random.shuffle(st.session_state.indices)
    else:
        st.session_state.indices = random.sample(range(total_districts), num_rounds)
        st.session_state.correct_indices = []
        st.session_state. score = 0

    st.session_state.wrong_indices = []
    st.session_state.feedback = None
    next_turn()


def next_turn():
    if st.session_state.indices:
        target = st.session_state.indices.pop()
        st.session_state.current_target = target
        name = gdf.iloc[target]["NM3"]

        wrong_pool = [n for n in all_names if n != name]
        variants = random.sample(wrong_pool, 3) + [name]
        random.shuffle(variants)
        st.session_state.current_variants = variants
        st.session_state.show_hint = False
    else:
        st.session_state.current_target = None


def submit_Answer(guess: str):
    target = st.session_state.current_target
    name = gdf.iloc[target]["NM3"]

    if normalize_name(guess) == normalize_name(name):
        st.session_state.score += 1
        st.session_state.correct_indices.append(target)
        st.session_state.feedback = ("success", f"Correct! It was {name}.")
    else:
        st.session_state.wrong_indices.append(target)
        st.session_state.feedback = ("error", f"Wrong! It was {name}.")

    next_turn()


if st.sidebar.button("Start / Restart Game"):
    start_new_game()
    st.rerun()

if "indices" not in st.session_state:
    start_new_game()

# --- Main Interface ---
st.title("Slovakia Districts Quiz")

if st.session_state.feedback:
    msg_type, msg_text = st.session_state.feedback
    if msg_type == "success":
        st.success(msg_text)
    else:
        st.error(msg_text)

target = st.session_state.current_target

if target is not None:
    name = gdf.iloc[target]["NM3"]
    left_count = len(st.session_state.indices) + 1

    col1, col2, col3 = st.columns(3)
    col1.metric("Score", st.session_state.score)
    col2.metric("Remaining", left_count)
    col3.metric("Mistakes", len(st.session_state.wrong_indices))

    # Render Map
    fig, ax = plt.subplots(figsize=(8, 6))
    gdf.plot(ax=ax, color="lightgray", edgecolor="white", linewidth=0.5)

    if st.session_state.correct_indices:
        gdf.iloc[st.session_state.correct_indices].plot(
            ax=ax, color="seagreen", edgecolor="white", linewidth=0.8
        )
    if st.session_state.wrong_indices:
        gdf.iloc[st.session_state.wrong_indices].plot(
            ax=ax, color="indianred", edgecolor="white", linewidth=0.8
        )
    gdf.iloc[[target]].plot(ax=ax, color="gold", edgecolor="black", linewidth=0.8)

    target_area = gdf.iloc[[target]].area.iloc[0]
    if target_area < 150_000_000:
        minx, miny, maxx, maxy = gdf.iloc[[target]].total_bounds
        pad = 15000
        ax.set_xlim(minx - pad, maxx + pad)
        ax.set_ylim(miny - pad, maxy + pad)

    ax.set_axis_off()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    # Hint Controls
    if st.button("Show Hint"):
        st.session_state.show_hint = True
    if st.session_state.show_hint:
        st.info(f"Hint: starts with '{name[0]}'")

    # Input Controls
    if mode == "Normal (Text Input)":
        with st.form(key=f"form_{target}", clear_on_submit=True):
            user_guess = st.text_input("District name:")
            submitted = st.form_submit_button("Submit Answer")
            if submitted and user_guess.strip():
                submit_Answer(user_guess.strip())
                st.rerun()
    else:
        st.write("Select the correct district:")
        btn_cols = st.columns(2)
        for i, option in enumerate(st.session_state.current_variants):
            if btn_cols[i % 2].button(option, key=f"opt_{target}_{i}", use_container_width=True):
                submit_Answer(option)
                st.rerun()

else:
    st.subheader("Game Over")
    st.write(
        f"Correct: {len(st.session_state.correct_indices)} | "
        f"Wrong: {len(st.session_state.wrong_indices)}"
    )

    if st.session_state.wrong_indices:
        wrong_names = gdf.iloc[st.session_state.wrong_indices]["NM3"].tolist()
        st.write("Mistakes in:", ", ".join(wrong_names))
        if st.button("Retry Mistakes Only"):
            start_new_game(custom_indices=st.session_state.wrong_indices)
            st.rerun()