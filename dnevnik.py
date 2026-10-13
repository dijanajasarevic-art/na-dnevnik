import streamlit as st
import sqlite3
import datetime

# -----------------------------------------------------------------------------
# 1. PODEŠAVANJE I MOBILNA ESTETIKA (TOPLI KAFENI TONOVI)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Naš Dnevnik Uspomena ☕",
    page_icon="☕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    /* Prilagođavanje za sve veličine ekrana (posebno mobilne telefone) */
    .stApp {
        background-color: #FAF6F0;
        color: #2F2119;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 650px !important;
    }

    /* Zaglavlje u stilu kafene sveske */
    .journal-header {
        text-align: center;
        background: linear-gradient(135deg, #4A2E1B, #6F4E37);
        color: #FAF5E4;
        padding: 24px 16px;
        border-radius: 16px;
        margin-bottom: 20px;
        box-shadow: 0 6px 18px rgba(74, 46, 27, 0.15);
    }
    .journal-header h1 {
        font-size: 24px;
        margin: 0;
        font-weight: 700;
        letter-spacing: 0.3px;
        color: #FFFFFF;
    }
    .journal-header p {
        font-size: 13px;
        margin-top: 6px;
        color: #EAD8C7;
        font-style: italic;
    }

    /* Kartica za uspomenu */
    .memory-card {
        background-color: #FFFFFF;
        border: 1px solid #E8DCCF;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 18px;
        box-shadow: 0 3px 12px rgba(60, 42, 33, 0.05);
        border-left: 5px solid #6F4E37;
    }
    
    .header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
        flex-wrap: wrap;
        gap: 6px;
    }
    
    .author-badge {
        display: inline-block;
        background-color: #F4EBE2;
        color: #4A2E1B;
        font-weight: 700;
        font-size: 13px;
        padding: 4px 10px;
        border-radius: 16px;
        border: 1px solid #D5C2AD;
    }

    .mood-pill {
        display: inline-block;
        background-color: #FFF6E5;
        color: #8C5311;
        font-weight: 600;
        font-size: 12px;
        padding: 4px 9px;
        border-radius: 16px;
        border: 1px solid #F0D4A8;
    }
    
    .date-tag {
        font-size: 12px;
        color: #8C7A6B;
        font-style: italic;
        width: 100%;
        margin-top: 2px;
    }

    .story-text {
        font-size: 14.5px;
        line-height: 1.55;
        color: #2F2119;
        margin-top: 8px;
        margin-bottom: 12px;
        white-space: pre-wrap;
    }

    /* Dugmad krupna i laka za dodir prstom */
    .stButton>button {
        background: linear-gradient(135deg, #6F4E37, #4A2E1B) !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        padding: 14px 20px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(74, 46, 27, 0.2) !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. BAZA PODATAKA (SQLITE)
# -----------------------------------------------------------------------------
def init_db():
    conn = sqlite3.connect("uspomene.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            entry_date TEXT NOT NULL,
            mood TEXT NOT NULL,
            content TEXT,
            image_bytes BLOB,
            audio_bytes BLOB,
            video_bytes BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Dodavanje kolone mood ako tabela već postoji od ranije
    try:
        c.execute("ALTER TABLE entries ADD COLUMN mood TEXT DEFAULT '☕ Opušteno'")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

def save_entry(author, entry_date, mood, content, img, audio, video):
    conn = sqlite3.connect("uspomene.db")
    c = conn.cursor()
    img_blob = img.read() if img else None
    audio_blob = audio.read() if audio else None
    video_blob = video.read() if video else None
    c.execute("""
        INSERT INTO entries (author, entry_date, mood, content, image_bytes, audio_bytes, video_bytes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (author, entry_date, mood, content, img_blob, audio_blob, video_blob))
    conn.commit()
    conn.close()

def get_all_entries():
    conn = sqlite3.connect("uspomene.db")
    c = conn.cursor()
    c.execute("SELECT author, entry_date, mood, content, image_bytes, audio_bytes, video_bytes FROM entries ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

init_db()

# -----------------------------------------------------------------------------
# 3. ZAGLAVLJE
# -----------------------------------------------------------------------------
st.markdown("""
<div class="journal-header">
    <h1>☕ Naš Dnevnik Uspomena</h1>
    <p>„Zabeleži trenutak pre nego što izbledi, uz gutljaj tople kafe.“ ✨</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. POLJA ZA UNOS NOVE USPOMENE
# -----------------------------------------------------------------------------
with st.expander("✍️ Dodaj novu priču dana (Dodirni ovde)", expanded=False):
    st.write("#### ☕ Novi list u spomenaru")
    
    author = st.text_input("Ko piše danas? (Tvoje ime / nadimak) 🌿", placeholder="npr. Dijana")
    entry_date = st.date_input("Datum zabeleške 📅", datetime.date.today())
    
    # Rubrika sa smajlijima i raspoloženjem
    mood_options = [
        "☕ Opušteno & mirno",
        "✨ Srećno & zahvalno",
        "🎉 Uzbuđeno & energično",
        "🥰 Voljeno & toplo",
        "💪 Produktivno & uspešno",
        "😴 Umorno & pospano",
        "🌧️ Osetljivo & melanholično"
    ]
    mood = st.selectbox("Kako se danas osećaš? (Raspoloženje dana) 💭", mood_options, index=0)
    
    content = st.text_area(
        "Šta se lepo, neobično ili važno desilo danas? 📖",
        placeholder="Napiši par rečenica, zabeleži utisak ili lepu anegdotu...",
        height=110
    )
    
    st.write("---")
    st.write("#### 📸 Zakači uspomene dana:")
    
    uploaded_img = st.file_uploader("Dodaj fotografiju 🖼️", type=["jpg", "jpeg", "png"])
    
    st.write("🎙️ **Glasovna poruka:** (Pritisni mikrofon i snimi glas)")
    recorded_audio = st.audio_input("Snimi glasovnu poruku")
    
    uploaded_video = st.file_uploader("Dodaj video zapis 🎬", type=["mp4", "mov"])
    
    st.write("")
    if st.button("Sačuvaj u dnevnik ☕✨"):
        if not author.strip():
            st.error("Upiši svoje ime pre čuvanja.")
        elif not content.strip() and not uploaded_img and not recorded_audio and not uploaded_video:
            st.warning("Upiši barem kratku rečenicu ili priloži neku fotografiju/glas.")
        else:
            save_entry(author.strip(), str(entry_date), mood, content.strip(), uploaded_img, recorded_audio, uploaded_video)
            st.success("Tvoja uspomena je uspešno upisana u naš dnevnik! ☕💛")
            st.rerun()

# -----------------------------------------------------------------------------
# 5. ZID ZAJEDNIČKIH PRIČA (PRIKAZ)
# -----------------------------------------------------------------------------
st.write("### 📜 Zid zajedničkih priča")
entries = get_all_entries()

if not entries:
    st.info("Dnevnik je još uvek prazan. Budi prva koja će upisati današnju kafu i misli!")
else:
    for item in entries:
        author_name, date_str, mood_tag, text_story, img_data, audio_data, video_data = item
        mood_display = mood_tag if mood_tag else "☕ Opušteno"
        
        with st.container():
            st.markdown(f"""
            <div class="memory-card">
                <div class="header-row">
                    <span class="author-badge">✍️ {author_name}</span>
                    <span class="mood-pill">{mood_display}</span>
                    <div class="date-tag">📅 {date_str}</div>
                </div>
                <div class="story-text">{text_story if text_story else "<i>(Objavljena uspomena bez pratećeg teksta)</i>"}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if img_data:
                st.image(img_data, use_container_width=True)
            if audio_data:
                st.audio(audio_data, format="audio/wav")
            if video_data:
                st.video(video_data)
            st.write("")