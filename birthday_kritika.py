import streamlit as st
import base64
from pathlib import Path

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Happy Birthday Kritika 🌸",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Helper: image → base64 ────────────────────────────────────────────────────
def img_to_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

photo1_b64   = img_to_b64("photo1.jpg")
photo2_b64   = img_to_b64("photo2.jpg")
flowers_b64  = img_to_b64("flowers.jpg")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400&display=swap');

  /* ── global reset ── */
  html, body, [data-testid="stAppViewContainer"] {{
    background: linear-gradient(160deg, #1a0a0f 0%, #2d0a1a 40%, #1a0d20 70%, #0d0a1a 100%) !important;
    color: #f5e6d3;
    font-family: 'Lato', sans-serif;
  }}
  [data-testid="stHeader"] {{ background: transparent !important; }}
  .block-container {{ padding: 0 1rem 4rem 1rem !important; max-width: 780px; margin: auto; }}

  /* ── floating petals background ── */
  .petal {{
    position: fixed;
    top: -40px;
    animation: fall linear infinite;
    opacity: 0.7;
    pointer-events: none;
    z-index: 0;
    font-size: 1.2rem;
  }}
  @keyframes fall {{
    0%   {{ transform: translateY(0) rotate(0deg); opacity: 0.8; }}
    100% {{ transform: translateY(110vh) rotate(360deg); opacity: 0; }}
  }}

  /* ── hero ── */
  .hero {{
    text-align: center;
    padding: 60px 20px 20px;
    position: relative;
    z-index: 1;
  }}
  .hero-flowers {{
    width: 140px;
    margin: 0 auto 20px;
    animation: floatUp 3s ease-in-out infinite;
    filter: drop-shadow(0 0 18px #ff6b9580);
  }}
  @keyframes floatUp {{
    0%,100% {{ transform: translateY(0); }}
    50%      {{ transform: translateY(-12px); }}
  }}
  .hero h1 {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 7vw, 3.4rem);
    font-weight: 700;
    letter-spacing: .04em;
    background: linear-gradient(135deg, #ffb7c5, #ff6b95, #e8a0bf);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 6px;
    line-height: 1.15;
    text-shadow: none;
  }}
  .hero h2 {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.1rem, 4vw, 1.6rem);
    font-weight: 400;
    font-style: italic;
    color: #e8a0bf;
    margin: 0 0 30px;
  }}
  .divider {{
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #ff6b95, #c8a8d8, #ff6b95, transparent);
    margin: 30px auto;
    width: 70%;
  }}

  /* ── sakura decoration ── */
  .sakura-row {{
    text-align: center;
    font-size: 1.4rem;
    letter-spacing: 6px;
    margin: 10px 0;
    opacity: 0.6;
  }}

  /* ── photos ── */
  .photos-row {{
    display: flex;
    gap: 24px;
    justify-content: center;
    flex-wrap: wrap;
    margin: 30px 0;
    position: relative;
    z-index: 1;
  }}
  .photo-frame {{
    width: 210px;
    height: 210px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid #ff6b95;
    box-shadow: 0 0 30px #ff6b9550, 0 0 60px #c8a8d820;
    flex-shrink: 0;
    background: #2a1020;
  }}
  .photo-frame img {{
    width: 100%; height: 100%;
    object-fit: cover;
    object-position: center top;
  }}
  /* Fix rotation for photo1 specifically */
  .photo-frame.fix-rotate img {{
    transform: rotate(0deg);
    object-position: center center;
  }}

  /* ── message card ── */
  .msg-card {{
    background: linear-gradient(135deg, #1e0a14 0%, #2a1020 50%, #1a0a1e 100%);
    border: 1px solid #ff6b9540;
    border-radius: 20px;
    padding: 38px 34px;
    margin: 30px 0;
    text-align: center;
    box-shadow: 0 8px 40px #00000060, inset 0 1px 0 #ff6b9530;
    position: relative;
    z-index: 1;
  }}
  .msg-card::before {{
    content: "🌸";
    position: absolute;
    top: -14px; left: 50%;
    transform: translateX(-50%);
    font-size: 1.8rem;
    background: #1e0a14;
    padding: 0 8px;
  }}
  .msg-card .label {{
    font-size: .75rem;
    letter-spacing: .2em;
    text-transform: uppercase;
    color: #ff6b95;
    margin-bottom: 14px;
  }}
  .msg-card p {{
    font-size: 1.05rem;
    line-height: 1.9;
    color: #f0d8e8;
    margin: 0;
  }}

  /* ── reasons grid ── */
  .reasons-title {{
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    text-align: center;
    background: linear-gradient(135deg, #ffb7c5, #c8a8d8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 40px 0 20px;
    position: relative;
    z-index: 1;
  }}
  .reason-card {{
    background: linear-gradient(135deg, #150810 0%, #1e0a18 100%);
    border-left: 3px solid #ff6b95;
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 14px;
    box-shadow: 0 2px 16px #00000040;
    position: relative;
    z-index: 1;
    transition: transform .2s, box-shadow .2s;
  }}
  .reason-card:hover {{
    transform: translateX(4px);
    box-shadow: 0 4px 24px #ff6b9520;
  }}
  .reason-card .r-num {{
    font-size: .7rem;
    letter-spacing: .2em;
    color: #ff6b95;
    text-transform: uppercase;
    margin-bottom: 6px;
  }}
  .reason-card p {{
    margin: 0;
    font-size: .97rem;
    color: #e8d0e0;
    line-height: 1.75;
  }}

  /* ── closing ── */
  .closing {{
    text-align: center;
    padding: 40px 20px 20px;
    position: relative;
    z-index: 1;
  }}
  .closing .big-heart {{
    font-size: 3rem;
    display: inline-block;
    animation: pulse 1.2s ease-in-out infinite;
  }}
  @keyframes pulse {{
    0%,100% {{ transform: scale(1); }}
    50%      {{ transform: scale(1.25); }}
  }}
  .closing h3 {{
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    background: linear-gradient(135deg, #ffb7c5, #c8a8d8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 14px 0 8px;
  }}
  .closing p {{
    color: #c8a8d8;
    font-size: .95rem;
    line-height: 1.8;
  }}

  /* ── audio player override ── */
  audio {{
    filter: hue-rotate(310deg) saturate(1.5) !important;
  }}

  /* ── confetti canvas ── */
  #confetti-canvas {{
    position: fixed; top:0; left:0;
    width:100%; height:100%;
    pointer-events: none;
    z-index: 9999;
  }}
</style>
""", unsafe_allow_html=True)

# ── Cherry Blossom Petal Rain ─────────────────────────────────────────────────
petal_html = ""
import random
petals = ["🌸", "🌺", "🌷", "✿", "❀"]
for i in range(18):
    left = random.randint(0, 100)
    delay = random.uniform(0, 12)
    duration = random.uniform(8, 18)
    petal = random.choice(petals)
    petal_html += f'<div class="petal" style="left:{left}%;animation-delay:{delay:.1f}s;animation-duration:{duration:.1f}s;">{petal}</div>\n'

st.markdown(petal_html, unsafe_allow_html=True)

# ── Confetti script ───────────────────────────────────────────────────────────
st.markdown("""
<canvas id="confetti-canvas"></canvas>
<script>
(function(){{
  const canvas = document.getElementById('confetti-canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  // Cherry blossom pink palette
  const colors = ['#ffb7c5','#ff6b95','#e8a0bf','#c8a8d8','#fff0f5','#ff9eb5','#f48fb1'];
  const pieces = Array.from({{length:140}},()=>{{
    return {{
      x: Math.random()*canvas.width,
      y: Math.random()*canvas.height - canvas.height,
      r: Math.random()*5+2,
      d: Math.random()*80+40,
      color: colors[Math.floor(Math.random()*colors.length)],
      tilt: Math.random()*10-10,
      tiltAngle: 0,
      tiltSpeed: Math.random()*.07+.04,
      shape: Math.random() > 0.5 ? 'circle' : 'petal'
    }};
  }});
  let angle = 0, stop = false;
  setTimeout(()=>stop=true, 7000);
  function draw(){{
    ctx.clearRect(0,0,canvas.width,canvas.height);
    if(stop){{ return; }}
    angle += .01;
    pieces.forEach(p=>{{
      p.tiltAngle += p.tiltSpeed;
      p.y += (Math.cos(angle+p.d)+1.4)*1.5;
      p.x += Math.sin(angle)*1.2;
      p.tilt = Math.sin(p.tiltAngle)*12;
      if(p.y > canvas.height){{ p.y = -10; p.x = Math.random()*canvas.width; }}
      ctx.beginPath();
      if(p.shape === 'circle'){{
        ctx.arc(p.x, p.y, p.r, 0, 2*Math.PI);
        ctx.fillStyle = p.color;
        ctx.fill();
      }} else {{
        ctx.lineWidth = p.r/2;
        ctx.strokeStyle = p.color;
        ctx.moveTo(p.x+p.tilt+p.r/3, p.y);
        ctx.lineTo(p.x+p.tilt, p.y+p.tilt+p.r/3);
        ctx.stroke();
      }}
    }});
    requestAnimationFrame(draw);
  }}
  draw();
}})();
</script>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="sakura-row">🌸 ✿ 🌸 ✿ 🌸</div>
  <img class="hero-flowers"
       src="data:image/jpg;base64,{flowers_b64}"
       alt="flowers">
  <h1>Happy Birthday</h1>
  <h2>Kritika Tripathi ✨</h2>
  <div class="sakura-row" style="opacity:0.4; font-size:1rem;">— 🌷 wishing you all the magic 🌷 —</div>
</div>
""", unsafe_allow_html=True)

# ── Birthday song audio — Guzarish ───────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-bottom:8px; position:relative; z-index:1;">
  <p style="color:#ff6b95; font-size:.8rem; letter-spacing:.18em; text-transform:uppercase; margin-bottom:10px;">
    🎵 Guzarish — Javed Ali
  </p>
""", unsafe_allow_html=True)

# Direct mp3 link from pagalworld
st.audio("https://pagalworld.is/Guzarish - Ghajini (128 kbps).mp3", format="audio/mp3")

st.markdown("""
  <p style="color:#7a5060; font-size:.78rem; margin-top:6px; text-align:center;">
    (Press ▶ for the vibe 🎶)
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── PHOTOS ────────────────────────────────────────────────────────────────────
# photo1 gets fix-rotate class (the one that appeared rotated/tilted)
st.markdown(f"""
<div class="photos-row">
  <div class="photo-frame fix-rotate">
    <img src="data:image/jpg;base64,{photo1_b64}" alt="Kritika" style="transform:rotate(0deg); object-fit:cover; object-position:center center;">
  </div>
  <div class="photo-frame">
    <img src="data:image/jpg;base64,{photo2_b64}" alt="Kritika">
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── MAIN MESSAGE ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="msg-card">
  <div class="label">A message for you</div>
  <p>
    Hey Kritika! 🌸<br><br>
    On this beautiful day, just want you to know how glad I am to have you as a friend.
    Your smile can light up any room, and your kindness makes everything around you better.
    You deserve all the happiness, laughter, and amazing things life has to offer —
    today and always.<br><br>
    Wishing you the most magical birthday ever. May this year bring you everything
    you've ever wished for and more. 🎂✨
    <br><br>
    — From your friend, with love 💛
  </p>
</div>
""", unsafe_allow_html=True)

# ── REASONS ──────────────────────────────────────────────────────────────────
st.markdown('<div class="reasons-title">🌸 10 Things That Make You Special 🌸</div>', unsafe_allow_html=True)

reasons = [
    ("Your Smile", "Your smile is genuinely one of the most warm and beautiful things — it lights up every conversation and makes everything feel okay."),
    ("Your Kindness", "You have a heart that's pure and beautiful. Your empathy and care for people around you is something truly rare."),
    ("Your Strength", "You face challenges with so much grace and courage. You inspire the people around you without even realising it."),
    ("Making People Better", "Just being around you makes people want to be better — kinder, funnier, more real. That's a gift not everyone has."),
    ("The Memories", "Every moment we've spent laughing, chatting, and being ridiculous together is a memory I genuinely treasure. 💖"),
    ("Your Realness", "You're unapologetically yourself — no pretences, no drama. That authenticity is so refreshing and so rare."),
    ("Your Laugh", "Your laugh is infectious. Once you start, everyone around you can't help but smile too."),
    ("Your Energy", "You bring this calm yet bright energy to everything. Whether you're happy or just vibing, you make the space better."),
    ("Your Support", "You show up for the people you care about in ways that really matter. That loyalty is everything."),
    ("Simply You", "There are so many reasons to celebrate you today, Kritika — but the biggest one is just that you exist and you're you. Happy Birthday! 🎉"),
]

for i, (title, text) in enumerate(reasons, 1):
    st.markdown(f"""
    <div class="reason-card">
      <div class="r-num">Reason #{i} — {title}</div>
      <p>{text}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── CLOSING ──────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="closing">
  <img src="data:image/jpg;base64,{flowers_b64}" style="width:100px; opacity:.9; margin-bottom:16px; filter:drop-shadow(0 0 14px #ff6b9560);">
  <div class="sakura-row">🌸 🌸 🌸</div>
  <div class="big-heart">🩷</div>
  <h3>Here's to you, Kritika!</h3>
  <p>
    May your birthday be as wonderful as you are.<br>
    May this year be full of adventures, good food, great laughs,<br>
    and all the things that make your soul happy.<br><br>
    You deserve the absolute world. 🌙✨
  </p>
  <div class="sakura-row" style="margin-top:20px; opacity:0.5;">🌺 ✿ 🌸 ✿ 🌺</div>
  <p style="margin-top:20px; font-size:.82rem; color:#5a2840; letter-spacing:.1em;">
    Made with love • Happy Birthday 🎂 • Cherry Blossom Edition 🌸
  </p>
</div>
""", unsafe_allow_html=True)
