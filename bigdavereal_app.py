import streamlit as st  
import os
from pathlib import Path
import json

UPLOAD_DIR = Path("strain_photos")
UPLOAD_DIR.mkdir(exist_ok=True)

# Session state init
for key in ["logged_in", "registered", "auth_pass", "users", "username", "page"]:
    if key not in st.session_state:
        st.session_state[key] = False if key in ["logged_in", "registered", "auth_pass"] else "" if key == "username" else "Home" if key == "page" else {}

# CSS Styling and Animations including SVG text animation for Strains page
st.markdown("""
    <style>
    @keyframes bounce {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-10px); }
    }

    .title {
        font-family: 'Arial Black', sans-serif;
        font-size: 50px;
        color: #6a0dad;
        animation: bounce 2s infinite;
        text-align: center;
        margin-bottom: 20px;
    }

    .shiny-text {
        font-size: 30px;
        font-weight: bold;
        background: linear-gradient(to right, #fff, #6a0dad, #fff);
        background-size: 200% auto;
        color: #000;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 2s linear infinite;
        text-align: center;
    }

    @keyframes shine {
        0% { background-position: 200% center; }
        100% { background-position: -200% center; }
    }

    .button:hover {
        background-color: #6a0dad !important;
        color: white !important;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    
    @keyframes float {
      0%, 100% {
        transform: translateY(0) scale(1);
      }
      50% {
        transform: translateY(-10px) scale(1.03);
      }
    }

    .photo-container img {
        border-radius: 15px;
        animation: fadeIn 1.2s ease-in-out, float 4s ease-in-out infinite;
        transition: transform 0.4s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .photo-container img:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        animation-play-state: paused;
    }

    /* SVG Text Animation for Strains page */
    .svg-text {
        width: 100%;
        text-align: center;
        margin: 20px 0;
    }

    svg {
        width: 100%;
        height: 80px;
    }

    .animated-text {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        font-weight: bold;
        font-size: 40px;
        fill: none;
        stroke: #8d17e8;
        stroke-width: 1.5;
        stroke-dasharray: 400;
        stroke-dashoffset: 400;
        animation: dash 4s ease forwards infinite alternate;
    }

    @keyframes dash {
        to {
            stroke-dashoffset: 0;
        }
    }

    .animated-text-fill {
        font-family: 'Comic Sans MS', cursive, sans-serif;
        font-weight: bold;
        font-size: 40px;
        fill: url(#grad1);
        stroke: none;
        opacity: 0;
        animation: fillFade 4s ease forwards infinite alternate;
        animation-delay: 2s;
    }

    @keyframes fillFade {
        to {
            opacity: 1;
        }
    }

    /* Contact card styles */
    .contact-card {
        background: rgba(10, 10, 10, 0.8);
        border: 2px solid;
        border-image: linear-gradient(45deg, #6a0dad, #b19cd9) 1;
        border-radius: 20px;
        padding: 30px;
        margin: auto;
        width: 80%;
        color: white;
        animation: fadeIn 2s ease-in-out;
        box-shadow: 0 0 15px #6a0dad;
    }

    .contact-card h2 {
        font-family: 'Arial Black', sans-serif;
        font-size: 36px;
        text-align: center;
        background: linear-gradient(to right, #fff, #6a0dad, #fff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
    }

    .contact-card a {
        display: block;
        font-size: 22px;
        text-align: center;
        margin-top: 15px;
        color: #b19cd9;
        text-decoration: none;
        transition: transform 0.3s ease, color 0.3s ease;
    }

    .contact-card a:hover {
        color: #fff;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# 📸 Home photo section using columns
def home_photo_containers():
    photos = [
        "https://th.bing.com/th/id/OIP.F1m_SEFcLavcoV2IVkwn-QAAAA?r=0&rs=1&pid=ImgDetMain&cb=idpwebp2&o=7&rm=3",
        "https://i.etsystatic.com/9818784/r/il/efb378/3832450398/il_fullxfull.3832450398_f3p2.jpg",
        "https://www.healingself.in/images/newimages/karmic-healing.jpg"
    ]
    cols = st.columns(len(photos))
    for col, url in zip(cols, photos):
        with col:
            st.markdown(f"<div class='photo-container'><img src='{url}' style='width:100%'></div>", unsafe_allow_html=True)

# 🎯 Homepage header
def show_home():
    st.markdown("<div class='title'>How High Are You?</div>", unsafe_allow_html=True)
    st.markdown("<div class='shiny-text'>Smoke Weed Everyday!</div>", unsafe_allow_html=True)
    home_photo_containers()

# 👤 Register system
def register():
    st.subheader("Register")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    if st.button("Register"):
        if username and password:
            if username in st.session_state.users:
                st.warning("Someone already taken your shit.")
            else:
                st.session_state.users[username] = password
                st.success("Registration successful! You can now login.")
                st.session_state.registered = True
                st.session_state.auth_mode = "login"
        else:
            st.warning("Please fill out all fields.")

# 🔑 Login
def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if st.session_state.users.get(username) == password:
            st.success("Logged in successfully.(Click Again to Enjoy!)")
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.error("Invalid credentials")

def logout():
    for key in ["logged_in", "username", "auth_pass"]:
        st.session_state[key] = False if key != "username" else ""
    st.session_state.page = "Home"
    st.success("Logged out.")

# 🔁 Navigation bar
def navbar():
    st.markdown("<h2 style='text-align:center;'>🤖 BigDave's Output 🤖</h2>", unsafe_allow_html=True)
    st.session_state.page = st.selectbox("Navigate", ["Home", "Strains", "Contact Us", "Manage Photos"])
    if st.button("Log Out"):
        logout()

# 🧠 Load/save photo descriptions
def load_metadata(category_dir):
    meta_path = category_dir / "metadata.json"
    return json.load(open(meta_path)) if meta_path.exists() else {}

def save_metadata(category_dir, metadata):
    with open(category_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

# SVG Animated heading generator
def svg_animated_heading(text):
    svg_code = f"""
    <div class="svg-text">
      <svg viewBox="0 0 600 80" preserveAspectRatio="xMidYMid meet">
        <defs>
          <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#6a0dad"/>
            <stop offset="50%" stop-color="#ff00cc"/>
            <stop offset="100%" stop-color="#6a0dad"/>
          </linearGradient>
        </defs>
        <text class="animated-text" x="50%" y="60%" dominant-baseline="middle" text-anchor="middle">{text}</text>
        <text class="animated-text-fill" x="50%" y="60%" dominant-baseline="middle" text-anchor="middle">{text}</text>
      </svg>
    </div>
    """
    return svg_code

# 🌿 Display uploaded strain images
def display_strains():
    categories = ["Spiritual Arts", "Zodiac Sign", "Ai Arts", "Robots"]
    for category in categories:
        # Use SVG animated heading instead of plain text
        st.markdown(svg_animated_heading(category), unsafe_allow_html=True)

        category_dir = UPLOAD_DIR / category
        category_dir.mkdir(exist_ok=True)
        metadata = load_metadata(category_dir)
        images = sorted(list(category_dir.glob("*.jpg")) + list(category_dir.glob("*.png")))

        if not images:
            st.info(f"No images uploaded yet in {category}")
            continue

        cols_per_row = 3
        for i in range(0, len(images), cols_per_row):
            cols = st.columns(cols_per_row)
            for col_idx, img_path in enumerate(images[i:i+cols_per_row]):
                col = cols[col_idx]
                with col:
                    st.image(str(img_path), use_container_width=True)
                    key_desc = f"{category}_{img_path.name}_desc"
                    desc = metadata.get(img_path.name, "")
                    new_desc = st.text_input("Description:", value=desc, key=key_desc, max_chars=100)
                    if new_desc != desc:
                        metadata[img_path.name] = new_desc
                        save_metadata(category_dir, metadata)

# 📞 Contact info
def contact():
    st.markdown("""
    <div class='contact-card'>
        <h2>Contact Us</h2>
        <a href="https://facebook.com/weedshop420" target="_blank">📘 Facebook</a>
        <a href="https://t.me/weedshop420" target="_blank">📱 Telegram</a>
        <a href="https://line.me/R/ti/p/@weedshop420" target="_blank">💬 Line</a>
    </div>
    """, unsafe_allow_html=True)

# 📤 Upload + 🗑️ Delete photos
def manage_photos():
    st.subheader("Manage Photos")
    if not st.session_state.auth_pass:
        pwd = st.text_input("Enter admin password to manage photos", type="password")
        if pwd == "bigrast":
            st.session_state.auth_pass = True
            st.success("Access granted!")
        else:
            st.warning("Don't try this shit!")
            return

    categories = ["Spiritual Arts", "Zodiac Sign", "Ai Arts", "Robots"]
    selected_cat = st.selectbox("Choose category", categories)
    category_dir = UPLOAD_DIR / selected_cat
    category_dir.mkdir(parents=True, exist_ok=True)

    st.markdown("**Upload new photo(s) to selected category**")
    uploads = st.file_uploader("Upload image(s)", type=["png", "jpg"], accept_multiple_files=True, key="uploader")
    if uploads:
        for uploaded in uploads:
            save_path = category_dir / uploaded.name
            if save_path.exists():
                st.warning(f"{uploaded.name} already exists.")
            else:
                with open(save_path, "wb") as f:
                    f.write(uploaded.read())
                st.success(f"Uploaded: {uploaded.name}")

    images = sorted(list(category_dir.glob("*.jpg")) + list(category_dir.glob("*.png")))
    if images:
        st.markdown("**Delete a photo from selected category**")
        selected_img = st.selectbox("Select photo to delete", [img.name for img in images])
        if st.button("Delete Photo"):
            try:
                os.remove(category_dir / selected_img)
                metadata = load_metadata(category_dir)
                if selected_img in metadata:
                    metadata.pop(selected_img)
                    save_metadata(category_dir, metadata)
                st.success(f"Deleted {selected_img}")
            except Exception as e:
                st.error(f"Failed to delete: {e}")
    else:
        st.info("No images in this category yet.")

# 🚀 App start
show_home()

if not st.session_state.logged_in:
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = ""

    st.markdown("## Welcome from My App! 🤖")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login"):
            st.session_state.auth_mode = "login"
    with col2:
        if st.button("📝 Register"):
            st.session_state.auth_mode = "register"

    if st.session_state.auth_mode == "register":
        register()
    elif st.session_state.auth_mode == "login":
        login()
else:
    navbar()
    if st.session_state.page == "Home":
        st.write(f"Hi!, I'm BigDaveReal.@420, {st.session_state.username}! 🤖")
    elif st.session_state.page == "Strains":
        display_strains()
    elif st.session_state.page == "Contact Us":
        contact()
    elif st.session_state.page == "Manage Photos":
        manage_photos()
