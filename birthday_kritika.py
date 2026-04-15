import streamlit as st
import base64
from pathlib import Path
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Happy Birthday Kritika 🎂",
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
    background: #0d0d0d !important;
    color: #f5e6d3;
    font-family: 'Lato', sans-serif;
  }}
  [data-testid="stHeader"] {{ background: transparent !important; }}
  .block-container {{ padding: 0 1rem 4rem 1rem !important; max-width: 760px; margin: auto; }}

  /* ── hero ── */
  .hero {{
    text-align: center;
    padding: 60px 20px 20px;
    position: relative;
  }}
  .hero-flowers {{
    width: 140px;
    margin: 0 auto 20px;
    animation: floatUp 3s ease-in-out infinite;
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
    color: #f7c5a0;
    margin: 0 0 6px;
    line-height: 1.15;
  }}
  .hero h2 {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.1rem, 4vw, 1.6rem);
    font-weight: 400;
    font-style: italic;
    color: #d4a07a;
    margin: 0 0 30px;
  }}
  .divider {{
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #c27d52, transparent);
    margin: 30px auto;
    width: 60%;
  }}

  /* ── photos ── */
  .photos-row {{
    display: flex;
    gap: 16px;
    justify-content: center;
    flex-wrap: wrap;
    margin: 30px 0;
  }}
  .photo-frame {{
    width: 200px;
    height: 200px;
    border-radius: 50%;
    overflow: hidden;
    border: 3px solid #c27d52;
    box-shadow: 0 0 24px #c27d5240;
    flex-shrink: 0;
  }}
  .photo-frame img {{
    width: 100%; height: 100%;
    object-fit: cover;
    object-position: center top;
  }}

  /* ── message card ── */
  .msg-card {{
    background: #161616;
    border: 1px solid #2a2a2a;
    border-radius: 18px;
    padding: 36px 32px;
    margin: 30px 0;
    text-align: center;
    box-shadow: 0 8px 32px #00000060;
  }}
  .msg-card .label {{
    font-size: .75rem;
    letter-spacing: .2em;
    text-transform: uppercase;
    color: #c27d52;
    margin-bottom: 14px;
  }}
  .msg-card p {{
    font-size: 1.05rem;
    line-height: 1.85;
    color: #e8d5c4;
    margin: 0;
  }}

  /* ── reasons grid ── */
  .reasons-title {{
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    text-align: center;
    color: #f7c5a0;
    margin: 40px 0 20px;
  }}
  .reason-card {{
    background: #111;
    border-left: 3px solid #c27d52;
    border-radius: 10px;
    padding: 18px 22px;
    margin-bottom: 14px;
  }}
  .reason-card .r-num {{
    font-size: .7rem;
    letter-spacing: .2em;
    color: #c27d52;
    text-transform: uppercase;
    margin-bottom: 6px;
  }}
  .reason-card p {{
    margin: 0;
    font-size: .97rem;
    color: #ddd0c4;
    line-height: 1.7;
  }}

  /* ── closing ── */
  .closing {{
    text-align: center;
    padding: 40px 20px 20px;
  }}
  .closing .big-heart {{
    font-size: 3rem;
    animation: pulse 1.2s ease-in-out infinite;
  }}
  @keyframes pulse {{
    0%,100% {{ transform: scale(1); }}
    50%      {{ transform: scale(1.2); }}
  }}
  .closing h3 {{
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    color: #f7c5a0;
    margin: 14px 0 8px;
  }}
  .closing p {{
    color: #aaa;
    font-size: .92rem;
    line-height: 1.7;
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

# ── Confetti script ───────────────────────────────────────────────────────────
st.markdown("""
<canvas id="confetti-canvas"></canvas>
<script>
(function(){
  const canvas = document.getElementById('confetti-canvas');
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  const colors = ['#f7c5a0','#c27d52','#e8d5c4','#fff','#d4a07a','#ff9999'];
  const pieces = Array.from({length:120},()=>({
    x: Math.random()*canvas.width,
    y: Math.random()*canvas.height - canvas.height,
    r: Math.random()*6+3,
    d: Math.random()*80+40,
    color: colors[Math.floor(Math.random()*colors.length)],
    tilt: Math.random()*10-10,
    tiltAngle: 0,
    tiltSpeed: Math.random()*.07+.05
  }));
  let angle = 0, stop = false;
  setTimeout(()=>stop=true, 6000);
  function draw(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    if(stop){ return; }
    angle += .01;
    pieces.forEach(p=>{
      p.tiltAngle += p.tiltSpeed;
      p.y += (Math.cos(angle+p.d)+1.5)*1.6;
      p.x += Math.sin(angle)*1.5;
      p.tilt = Math.sin(p.tiltAngle)*12;
      if(p.y > canvas.height){ p.y = -10; p.x = Math.random()*canvas.width; }
      ctx.beginPath();
      ctx.lineWidth = p.r/2;
      ctx.strokeStyle = p.color;
      ctx.moveTo(p.x+p.tilt+p.r/3, p.y);
      ctx.lineTo(p.x+p.tilt, p.y+p.tilt+p.r/3);
      ctx.stroke();
    });
    requestAnimationFrame(draw);
  }
  draw();
})();
</script>
""", unsafe_allow_html=True)

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <img class="hero-flowers"
       src="data:image/jpg;base64,{flowers_b64}"
       alt="flowers">
  <h1>Happy Birthday</h1>
  <h2>Kritika Tripathi ✨</h2>
</div>
""", unsafe_allow_html=True)

# ── Birthday song audio (Custom Music Player) ─────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-bottom:10px;">
  <p style="color:#c27d52; font-size:.8rem; letter-spacing:.15em; text-transform:uppercase; margin-bottom:10px;">
    🎵 Birthday Song
  </p>
</div>
""", unsafe_allow_html=True)

import streamlit.components.v1 as components

# Encode the mp3 file to support playing in the iframe widget
song_path = "Guzarish - Ghajini (128 kbps).mp3"
try:
    with open(song_path, "rb") as f:
        song_b64 = base64.b64encode(f.read()).decode()
    audio_data_uri = f"data:audio/mp3;base64,{song_b64}"
except FileNotFoundError:
    audio_data_uri = ""

player_html = f"""
<!DOCTYPE html>
<html>
<head>
<style>
  body {{
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #0d0d0d;
    overflow: hidden;
  }}
  .card {{
    position: relative;
    width: 250px;
    height: 120px;
    background: #191414;
    border-radius: 10px;
    padding: 10px;
    font-family: Arial, sans-serif;
  }}
  .top {{
    position: relative;
    width: 100%;
    display: flex;
    gap: 10px;
  }}
  .pfp {{
    position: relative;
    top: 5px;
    left: 5px;
    height: 40px;
    width: 40px;
    background-color: #d2d2d2;
    border-radius: 5px;
    display: flex;
    justify-content: center;
    align-items: center;
  }}
  .title-1 {{
    color: white;
    font-size: 19px;
    font-weight: bolder;
    margin: 0;
    margin-top: 2px;
  }}
  .title-2 {{
    color: white;
    font-size: 12px;
    font-weight: bold;
    margin: 0;
    margin-top: 2px;
  }}
  .time {{
    width: 90%;
    background-color: #5e5e5e;
    height: 6px;
    border-radius: 3px;
    position: absolute;
    left: 5%;
    bottom: 22px;
    cursor: pointer;
  }}
  .elapsed {{
    width: 0%;
    background-color: #1db954;
    height: 100%;
    border-radius: 3px;
  }}
  .controls {{
    color: white;
    display: flex;
    position: absolute;
    bottom: 30px;
    left: 0;
    width: 100%;
    justify-content: center;
    align-items: center;
  }}
  .controls svg {{
    cursor: pointer;
    transition: 0.1s;
    margin: 0 5px;
  }}
  .controls svg:hover {{
    color: #1db954;
  }}
  .volume, .air {{
    height: 100%;
    width: 30px;
  }}
  .volume {{
    opacity: 0;
    position: relative;
    transition: 0.2s;
  }}
  .volume .slider {{
    height: 4px;
    background-color: #5e5e5e;
    width: 100%;
    border-radius: 2px;
    margin-top: 8px;
  }}
  .volume .slider .green {{
    background-color: #1db954;
    height: 100%;
    width: 100%;
    border-radius: 3px;
  }}
  .volume .circle {{
    background-color: white;
    height: 6px;
    width: 6px;
    border-radius: 3px;
    position: absolute;
    right: -3px;
    top: 7px;
  }}
  .volume_button:hover ~ .volume {{
    opacity: 1;
  }}
  .timetext {{
    color: white;
    font-size: 8px;
    position: absolute;
    margin: 0;
  }}
  .time_now {{ bottom: 11px; left: 10px; }}
  .time_full {{ bottom: 11px; right: 10px; }}
  .playing {{
    display: flex;
    position: relative;
    justify-content: center;
    gap: 1px;
    width: 30px;
    height: 20px;
  }}
  .greenline {{
    background-color: #1db954;
    height: 20px;
    width: 2px;
    position: relative;
    transform-origin: bottom;
  }}
  .line-1 {{ animation: infinite playing 1s ease-in-out; animation-delay: 0.2s; }}
  .line-2 {{ animation: infinite playing 1s ease-in-out; animation-delay: 0.5s; }}
  .line-3 {{ animation: infinite playing 1s ease-in-out; animation-delay: 0.6s; }}
  .line-4 {{ animation: infinite playing 1s ease-in-out; animation-delay: 0s; }}
  .line-5 {{ animation: infinite playing 1s ease-in-out; animation-delay: 0.4s; }}
  @keyframes playing {{
    0% {{ transform: scaleY(0.1); }}
    33% {{ transform: scaleY(0.6); }}
    66% {{ transform: scaleY(0.9); }}
    100% {{ transform: scaleY(0.1); }}
  }}
</style>
</head>
<body>
  <div class="card">
    <div class="top">
      <div class="pfp">
        <div class="playing" id="playing-anim">
          <div class="greenline line-1"></div>
          <div class="greenline line-2"></div>
          <div class="greenline line-3"></div>
          <div class="greenline line-4"></div>
          <div class="greenline line-5"></div>
        </div>
      </div>
      <div class="texts">
        <p class="title-1">Guzarish</p>
        <p class="title-2">Ghajini</p>
      </div>
    </div>
    
    <div class="controls">
      <svg class="volume_button" id="mute-btn" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" height="20" width="24">
        <path clip-rule="evenodd" d="M11.26 3.691A1.2 1.2 0 0 1 12 4.8v14.4a1.199 1.199 0 0 1-2.048.848L5.503 15.6H2.4a1.2 1.2 0 0 1-1.2-1.2V9.6a1.2 1.2 0 0 1 1.2-1.2h3.103l4.449-4.448a1.2 1.2 0 0 1 1.308-.26Zm6.328-.176a1.2 1.2 0 0 1 1.697 0A11.967 11.967 0 0 1 22.8 12a11.966 11.966 0 0 1-3.515 8.485 1.2 1.2 0 0 1-1.697-1.697A9.563 9.563 0 0 0 20.4 12a9.565 9.565 0 0 0-2.812-6.788 1.2 1.2 0 0 1 0-1.697Zm-3.394 3.393a1.2 1.2 0 0 1 1.698 0A7.178 7.178 0 0 1 18 12a7.18 7.18 0 0 1-2.108 5.092 1.2 1.2 0 1 1-1.698-1.698A4.782 4.782 0 0 0 15.6 12a4.78 4.78 0 0 0-1.406-3.394 1.2 1.2 0 0 1 0-1.698Z" fill-rule="evenodd" />
      </svg>
      <div class="volume">
        <div class="slider"><div class="green"></div></div>
        <div class="circle"></div>
      </div>
      
      <svg id="prev-btn" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" height="24" width="24">
        <path clip-rule="evenodd" d="M12 21.6a9.6 9.6 0 1 0 0-19.2 9.6 9.6 0 0 0 0 19.2Zm.848-12.352a1.2 1.2 0 0 0-1.696-1.696l-3.6 3.6a1.2 1.2 0 0 0 0 1.696l3.6 3.6a1.2 1.2 0 0 0 1.696-1.696L11.297 13.2H15.6a1.2 1.2 0 1 0 0-2.4h-4.303l1.551-1.552Z" fill-rule="evenodd" />
      </svg>
      
      <div id="play-pause-btn" style="display: flex; align-items: center; justify-content: center;">
        <svg id="play-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" height="24" width="24" style="display: block;">
          <path clip-rule="evenodd" d="M12 21.6a9.6 9.6 0 1 0 0-19.2 9.6 9.6 0 0 0 0 19.2ZM9.6 8.4v7.2l6-3.6-6-3.6Z" fill-rule="evenodd"/>
        </svg>
        <svg id="pause-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" height="24" width="24" style="display: none;">
          <path clip-rule="evenodd" d="M21.6 12a9.6 9.6 0 1 1-19.2 0 9.6 9.6 0 0 1 19.2 0ZM8.4 9.6a1.2 1.2 0 1 1 2.4 0v4.8a1.2 1.2 0 1 1-2.4 0V9.6Zm6-1.2a1.2 1.2 0 0 0-1.2 1.2v4.8a1.2 1.2 0 1 0 2.4 0V9.6a1.2 1.2 0 0 0-1.2-1.2Z" fill-rule="evenodd" />
        </svg>
      </div>
      
      <svg id="next-btn" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" height="24" width="24">
        <path clip-rule="evenodd" d="M12 21.6a9.6 9.6 0 1 0 0-19.2 9.6 9.6 0 0 0 0 19.2Zm4.448-10.448-3.6-3.6a1.2 1.2 0 0 0-1.696 1.696l1.551 1.552H8.4a1.2 1.2 0 1 0 0 2.4h4.303l-1.551 1.552a1.2 1.2 0 1 0 1.696 1.696l3.6-3.6a1.2 1.2 0 0 0 0-1.696Z" fill-rule="evenodd" />
      </svg>
      
      <div class="air"></div>
      
      <svg id="heart-btn" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" stroke="currentColor" fill="none" height="20" width="24">
        <path d="M3.343 7.778a4.5 4.5 0 0 1 7.339-1.46L12 7.636l1.318-1.318a4.5 4.5 0 1 1 6.364 6.364L12 20.364l-7.682-7.682a4.501 4.501 0 0 1-.975-4.904Z" />
      </svg>
    </div>
    
    <div class="time" id="progress-container">
      <div class="elapsed" id="progress-bar"></div>
    </div>
    <p class="timetext time_now" id="time-current">0:00</p>
    <p class="timetext time_full" id="time-total">0:00</p>
    
    <audio id="audio" src="{audio_data_uri}" preload="auto" autoplay></audio>
  </div>

  <script>
    const audio = document.getElementById('audio');
    const playPauseBtn = document.getElementById('play-pause-btn');
    const playIcon = document.getElementById('play-icon');
    const pauseIcon = document.getElementById('pause-icon');
    const progressBar = document.getElementById('progress-bar');
    const progressContainer = document.getElementById('progress-container');
    const timeCurrent = document.getElementById('time-current');
    const timeTotal = document.getElementById('time-total');
    const greenLines = document.querySelectorAll('.greenline');
    const heartBtn = document.getElementById('heart-btn');

    greenLines.forEach(line => line.style.animationPlayState = 'paused');

    function formatTime(secs) {{
      if (isNaN(secs)) return "0:00";
      const m = Math.floor(secs / 60);
      const s = Math.floor(secs % 60);
      return m + ':' + (s < 10 ? '0' : '') + s;
    }}

    audio.addEventListener('loadedmetadata', () => {{
      timeTotal.textContent = formatTime(audio.duration);
    }});

    audio.addEventListener('timeupdate', () => {{
      timeCurrent.textContent = formatTime(audio.currentTime);
      const pct = (audio.currentTime / audio.duration) * 100;
      progressBar.style.width = pct + '%';
    }});

    progressContainer.addEventListener('click', (e) => {{
      const rect = progressContainer.getBoundingClientRect();
      const pct = (e.clientX - rect.left) / rect.width;
      audio.currentTime = pct * audio.duration;
    }});

    function updateIcons() {{
      if (audio.paused) {{
        playIcon.style.display = 'block';
        pauseIcon.style.display = 'none';
        greenLines.forEach(line => line.style.animationPlayState = 'paused');
      }} else {{
        playIcon.style.display = 'none';
        pauseIcon.style.display = 'block';
        greenLines.forEach(line => line.style.animationPlayState = 'running');
      }}
    }}

    function togglePlay() {{
      if (audio.paused) {{
        audio.play().then(updateIcons).catch(console.error);
      }} else {{
        audio.pause();
        updateIcons();
      }}
    }}

    playPauseBtn.addEventListener('click', togglePlay);

    heartBtn.addEventListener('click', () => {{
      if (heartBtn.getAttribute('fill') === 'none') {{
        heartBtn.setAttribute('fill', '#1db954');
        heartBtn.setAttribute('stroke', '#1db954');
      }} else {{
         heartBtn.setAttribute('fill', 'none');
         heartBtn.setAttribute('stroke', 'currentColor');
      }}
    }});

    audio.addEventListener('ended', () => {{
      updateIcons();
      progressBar.style.width = '0%';
      audio.currentTime = 0;
    }});

    // Listen to play/pause events directly in case autoplay fires immediately
    audio.addEventListener('play', updateIcons);
    audio.addEventListener('pause', updateIcons);
  </script>
</body>
</html>
"""
components.html(player_html, height=140)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── PHOTOS ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="photos-row">
  <div class="photo-frame">
    <img src="data:image/jpg;base64,{photo1_b64}" alt="Kritika">
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

# ── ANIMATED FLOWERS BUTTON ───────────────────────────────────────────────────
st.markdown("""
<style>
  .f-btn {
    height: 4em; width: 12em; display: flex; align-items: center; justify-content: center;
    background: transparent; border: 0px solid black; cursor: pointer; margin: 20px auto;
  }
  .f-wrapper {
    height: 2em; width: 8em; position: relative; background: transparent;
    display: flex; justify-content: center; align-items: center;
  }
  .f-text {
    font-size: 17px; z-index: 1; color: #000; padding: 4px 12px; margin: 0;
    border-radius: 4px; background: rgba(255, 255, 255, 0.7); transition: all 0.5s ease;
  }
  .f-btn .flower { display: grid; grid-template-columns: 1em 1em; position: absolute; transition: grid-template-columns 0.8s ease; }
  .flower1 { top: -12px; left: -13px; transform: rotate(5deg); }
  .flower2 { bottom: -5px; left: 8px; transform: rotate(35deg); }
  .flower3 { bottom: -15px; transform: rotate(0deg); }
  .flower4 { top: -14px; transform: rotate(15deg); }
  .flower5 { right: 11px; top: -3px; transform: rotate(25deg); }
  .flower6 { right: -15px; bottom: -15px; transform: rotate(30deg); }
  .f-btn .petal {
    height: 1em; width: 1em; border-radius: 40% 70% / 7% 90%;
    background: linear-gradient(#07a6d7, #93e0ee); border: 0.5px solid #96d1ec;
    z-index: 0; transition: width 0.8s ease, height 0.8s ease;
  }
  .two { transform: rotate(90deg); }
  .three { transform: rotate(270deg); }
  .four { transform: rotate(180deg); }
  .f-btn:hover .petal { background: linear-gradient(#0761d7, #93bdee); border: 0.5px solid #96b4ec; }
  .f-btn:hover .flower { grid-template-columns: 1.5em 1.5em; }
  .f-btn:hover .flower .petal { width: 1.5em; height: 1.5em; }
  .f-btn:hover .f-text { background: rgba(255, 255, 255, 0.4); }
  .f-btn:hover div.flower1 { animation: 15s linear 0s normal none infinite running flower1; }
  @keyframes flower1 { 0% { transform: rotate(5deg); } 100% { transform: rotate(365deg); } }
  .f-btn:hover div.flower2 { animation: 13s linear 1s normal none infinite running flower2; }
  @keyframes flower2 { 0% { transform: rotate(35deg); } 100% { transform: rotate(-325deg); } }
  .f-btn:hover div.flower3 { animation: 16s linear 1s normal none infinite running flower3; }
  @keyframes flower3 { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
  .f-btn:hover div.flower4 { animation: 17s linear 1s normal none infinite running flower4; }
  @keyframes flower4 { 0% { transform: rotate(15deg); } 100% { transform: rotate(375deg); } }
  .f-btn:hover div.flower5 { animation: 20s linear 1s normal none infinite running flower5; }
  @keyframes flower5 { 0% { transform: rotate(25deg); } 100% { transform: rotate(-335deg); } }
  .f-btn:hover div.flower6 { animation: 15s linear 1s normal none infinite running flower6; }
  @keyframes flower6 { 0% { transform: rotate(30deg); } 100% { transform: rotate(390deg); } }
</style>
<div style="display:flex; justify-content:center; margin: 30px 0;">
  <button class="f-btn">
    <div class="f-wrapper">
      <p class="f-text">Hover Me ✨</p>
      <div class="flower flower1"><div class="petal one"></div><div class="petal two"></div><div class="petal three"></div><div class="petal four"></div></div>
      <div class="flower flower2"><div class="petal one"></div><div class="petal two"></div><div class="petal three"></div><div class="petal four"></div></div>
      <div class="flower flower3"><div class="petal one"></div><div class="petal two"></div><div class="petal three"></div><div class="petal four"></div></div>
      <div class="flower flower4"><div class="petal one"></div><div class="petal two"></div><div class="petal three"></div><div class="petal four"></div></div>
      <div class="flower flower5"><div class="petal one"></div><div class="petal two"></div><div class="petal three"></div><div class="petal four"></div></div>
      <div class="flower flower6"><div class="petal one"></div><div class="petal two"></div><div class="petal three"></div><div class="petal four"></div></div>
    </div>
  </button>
</div>
""", unsafe_allow_html=True)

# ── REASONS (from PDF, reframed as friendship reasons) ────────────────────────
st.markdown('<div class="reasons-title">10 Things That Make You Special 🌺</div>', unsafe_allow_html=True)

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
  <img src="data:image/jpg;base64,{flowers_b64}" style="width:100px; opacity:.85; margin-bottom:16px;">
  <div class="big-heart">🧡</div>
  <h3>Here's to you, Kritika!</h3>
  <p>
    May your birthday be as wonderful as you are.<br>
    May this year be full of adventures, good food, great laughs,<br>
    and all the things that make your soul happy.<br><br>
    You deserve the absolute world. 🌙✨
  </p>
  <p style="margin-top:24px; font-size:.82rem; color:#555; letter-spacing:.08em;">
    Made with love • Happy Birthday 🎂
  </p>
</div>
""", unsafe_allow_html=True)
