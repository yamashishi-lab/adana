import json
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hyper-Drive Architect: Apex WaveRider",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("🛸 Hyper-Drive Architect: Apex WaveRider")
st.caption(
    "※ 地上メガカタパルト射出・極超音速大気圏突破・軌道上オービタルメカ変形・恒星間ワープ完全再現版 (Prototype Safe Mode)"
)

# =========================================================================
# 🔬 機体・動力炉・目的地データベース
# =========================================================================
VESSEL_DESIGNS = {
    "極超音速ウェイブライダー『ヴァルキリー SSTO』": {
        "id": "waverider_valkyrie",
        "style": "stealth_waverider",
        "catapult_mach": 14.5,
        "warp_eff": 1.85,
        "desc": "チタン合金フレームと炭素耐熱タイル。大気圏脱出後に上部装甲が観音開き展開し、超伝導ワープリングがせり出す次世代機。",
    },
    "磁気慣性核融合クルーザー『プロメテウス』": {
        "id": "prometheus_cruiser",
        "style": "magnetic_fusion",
        "catapult_mach": 11.0,
        "warp_eff": 2.10,
        "desc": "船尾に巨大なオープンフレーム磁気ノズルと超伝導ソレノイド支柱を露出。金箔多層断熱材と極太冷却パイピングを持つ重厚設計。",
    },
    "電磁カタパルト迎撃槍『ロンギヌス・インターセプター』": {
        "id": "longinus_spear",
        "style": "massdriver_spear",
        "catapult_mach": 18.2,
        "warp_eff": 1.95,
        "desc": "空気抵抗を極限まで削いだ細身のクサビ形状。宇宙到達時に外装整流シェルを爆砕パージし、深宇宙巡航コアが露見する超高速艇。",
    },
}

POWER_CORES = {
    "超伝導マグネティック・核融合パルス (D-He3 Pulse)": {
        "power_gw": 180000.0,
        "flame_hex": 0x38BDF8,
        "outer_hex": 0x1D4ED8,
        "spark_hex": 0x93C5FD,
    },
    "人工特異点・事象の地平面抽出炉 (Kerr Singularity)": {
        "power_gw": 320000.0,
        "flame_hex": 0xA855F7,
        "outer_hex": 0x6B21A8,
        "spark_hex": 0xE9D5FF,
    },
    "反物質ビーム・光子トーチコア (Antimatter Torch)": {
        "power_gw": 450000.0,
        "flame_hex": 0xF43F5E,
        "outer_hex": 0x9F1239,
        "spark_hex": 0xFECDD3,
    },
}

DESTINATIONS = {
    "火星 オリンポス・テラフォーミング軌道都市": {
        "dist_label": "0.52 AU (78,000,000 km)",
        "color_hex": 0xC2410C,
        "type": "mars",
        "desc": "赤色惑星の軌道上に展開する第1電磁減速リングへダイブ。",
    },
    "木星 大赤斑上空・浮遊採掘ステーション": {
        "dist_label": "4.20 AU (628,000,000 km)",
        "color_hex": 0xD97706,
        "type": "jupiter",
        "desc": "荒れ狂うガス巨大惑星の乱気流直上、巨大アンカーリングへ突入。",
    },
    "土星リング 氷冠スターゲート「クロノス」": {
        "dist_label": "9.58 AU (1,433,000,000 km)",
        "color_hex": 0x94A3B8,
        "type": "saturn",
        "desc": "数億の氷塊が回転するリング間隙に鎮座する超大型減速ゲート。",
    },
}

LAUNCH_CATAPULTS = {
    "相模湾 海上メガ・マスドライバー (全長12km / 仰角38°)": {
        "rail_len": 12.0,
        "angle_deg": 38.0,
        "exit_mach": 15.0,
    },
    "富士山斜面 軌道射出リニアチューブ (標高3,776m直結)": {
        "rail_len": 8.5,
        "angle_deg": 48.0,
        "exit_mach": 18.0,
    },
}

# =========================================================================
# 🎛️ パラメータ設定UI
# =========================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🛸 機体設計 & 航空宇宙マテリアル",
    "⚡ 地上電磁カタパルト & 射出設定",
    "🌌 時空駆動炉 & 慣性ダンパー",
    "🎯 目的地航路 & フリップ減速",
])

with tab1:
  col1, col2 = st.columns(2)
  with col1:
    vessel_sel = st.selectbox("ベース艦種 (Chassis)", list(VESSEL_DESIGNS.keys()))
    vessel_cfg = VESSEL_DESIGNS[vessel_sel]
    hull_primary = st.color_picker("チタン合金装甲プレート配色", "#1e293b")
    tile_color = st.color_picker("耐熱カーボンタイル配色", "#090d16")
  with col2:
    st.info(f"**艦種概要:** {vessel_cfg['desc']}")
    wings_span = st.slider("可動デルタ翼 / カナード展開幅 (m)", 14.0, 38.0, 24.0, step=1.0)
    radiator_blades = st.slider("軌道展開 放熱ラジエーターフィン数", 2, 8, 4, step=2)

with tab2:
  col1, col2 = st.columns(2)
  with col1:
    catapult_sel = st.selectbox("地上電磁射出施設", list(LAUNCH_CATAPULTS.keys()))
    catapult_cfg = LAUNCH_CATAPULTS[catapult_sel]
    catapult_boost = st.slider("超伝導コイル電力チャージ率 (%)", 80, 150, 115, step=5)
  with col2:
    st.caption("※ 地上レール内で超伝導磁気浮上加速し、マッハ15超で大気圏へ射出されます。")
    launch_aoa = st.slider("大気圏突破 迎角 (AoA deg)", 1.0, 12.0, 4.5, step=0.5)

with tab3:
  col1, col2 = st.columns(2)
  with col1:
    power_sel = st.selectbox("主推進動力炉", list(POWER_CORES.keys()))
    power_cfg = POWER_CORES[power_sel]
    warp_curvature = st.slider("時空曲率倍率 (Warp Factor)", 1.0, 9.9, 8.5, step=0.1)
  with col2:
    throttle_pct = st.slider("ドライブ出力リミッター (%)", 50, 150, 110, step=5)
    damper_rate = st.slider(
        "慣性ダンパー相殺率 (%)",
        99.000,
        99.999,
        99.998,
        step=0.001,
        format="%.3f%%",
    )
    st.caption("※ プロトタイプ安全モード：生体保護リミッターにより過大Gは自動相殺されます。")

with tab4:
  col1, col2 = st.columns(2)
  with col1:
    dest_sel = st.selectbox("到達目標宙域", list(DESTINATIONS.keys()))
    dest_cfg = DESTINATIONS[dest_sel]
    st.caption(f"**目的宙域距離:** {dest_cfg['dist_label']}")
  with col2:
    flip_ratio = st.slider(
        "反転逆噴射 (フリップ＆バーン) 開始位置比率",
        0.55,
        0.90,
        0.75,
        step=0.01,
    )
    st.caption("※ 航法AIが最適な減速Gカーブを自動計算し、100%確実にゲート内へ停止します。")

# =========================================================================
# 💥 時空物理シミュレーション演算（地上射出 ➔ 軌道変形 ➔ ワープ ➔ ゲート）
# =========================================================================
def run_simulation(preview_only=False):
  if preview_only:
    return [{
        "t": -5.0,
        "phase": "PAD_INSPECTION",
        "alt_km": 0.05,
        "downrange_km": 0.0,
        "mach": 0.0,
        "vc": 0.0,
        "g": 1.0,
        "temp_k": 293.0,
        "morph_ring": 0.0,
        "morph_wings": 0.0,
        "warp_tunnel": 0.0,
        "plasma_alpha": 0.0,
        "space_ratio": 0.0,
        "progress": 0.0,
        "ship_time": 0.0,
        "earth_time": 0.0,
        "engine_active": False,
        "catapult_active": False,
        "rx": 0.0,
        "ry": 1.2,
        "pitch_deg": catapult_cfg["angle_deg"],
    }], None

  dt = 0.5
  history = []
  ship_t = 0.0
  earth_t = 0.0

  # カウントダウン（T-5.0 〜 T-0.0）
  for cd in range(11):
    t_cd = -5.0 + cd * 0.5
    history.append({
        "t": float(t_cd),
        "phase": "CATAPULT_CHARGE" if t_cd >= -3.0 else "PRE_FLIGHT",
        "alt_km": 0.05,
        "downrange_km": 0.0,
        "mach": 0.0,
        "vc": 0.0,
        "g": 1.0,
        "temp_k": 293.0,
        "morph_ring": 0.0,
        "morph_wings": 0.0,
        "warp_tunnel": 0.0,
        "plasma_alpha": 0.0,
        "space_ratio": 0.0,
        "progress": 0.0,
        "ship_time": 0.0,
        "earth_time": 0.0,
        "engine_active": False,
        "catapult_active": bool(t_cd >= -3.0),
        "rx": 0.0,
        "ry": 1.2,
        "pitch_deg": float(catapult_cfg["angle_deg"]),
    })

  total_sim_steps = 150
  c_angle_rad = np.radians(catapult_cfg["angle_deg"])
  exit_m = catapult_cfg["exit_mach"] * (catapult_boost / 100.0)

  cur_alt = 0.05
  cur_downrange = 0.0
  cur_mach = 0.0
  cur_vc = 0.0
  cur_progress = 0.0

  for step in range(total_sim_steps):
    t = float(step * dt)

    # 1. カタパルト射出（0 〜 3秒）
    if t <= 3.0:
      phase = "RAIL_ACCELERATION"
      cur_mach = (t / 3.0) * exit_m
      cur_alt = 0.05 + (t / 3.0) * 1.8 * np.sin(c_angle_rad)
      cur_downrange = (t / 3.0) * 1.8 * np.cos(c_angle_rad)
      cur_g = 12.5 * (catapult_boost / 100.0)
      plasma = 0.0
      morph_ring = 0.0
      morph_wings = 0.0
      warp_tun = 0.0
      space_r = 0.0
      eng_on = False
      pitch_deg = catapult_cfg["angle_deg"]
    # 2. 極超音速大気圏突破クライム（3 〜 14秒）
    elif cur_alt < 120.0:
      phase = "HYPERSONIC_CLIMB"
      eng_on = True
      cur_mach = min(32.0, cur_mach + 1.8 * dt)
      climb_speed = cur_mach * 340.0
      cur_alt += (climb_speed * np.sin(c_angle_rad) * dt) / 1000.0
      cur_downrange += (climb_speed * np.cos(c_angle_rad) * dt) / 1000.0
      cur_g = 4.2
      # 高度15km〜60kmで猛烈な空力加熱プラズマ
      if 15.0 <= cur_alt <= 75.0:
        plasma = float(np.sin(((cur_alt - 15.0) / 60.0) * np.pi) * 0.95)
      else:
        plasma = 0.0
      morph_ring = 0.0
      morph_wings = min(1.0, (cur_alt / 80.0))
      warp_tun = 0.0
      space_r = float(np.clip((cur_alt - 15.0) / 75.0, 0.0, 1.0))
      pitch_deg = float(catapult_cfg["angle_deg"] * (1.0 - space_r * 0.7))
    # 3. 軌道上メカ変形 ＆ ワープチャージ（14 〜 24秒）
    elif cur_progress < 0.05:
      phase = "ORBITAL_TRANSFORM"
      eng_on = False
      cur_alt = 140.0
      plasma = 0.0
      morph_ring = min(1.0, morph_ring + 0.12 * dt * 2.0)
      morph_wings = 1.0
      warp_tun = 0.0
      space_r = 1.0
      cur_g = 1.0
      cur_vc = 0.02
      cur_progress += 0.005
      pitch_deg = 0.0
    # 4. 恒星間ワープ超加速巡航（24秒 〜 フリップ減速）
    elif cur_progress < flip_ratio:
      phase = "WARP_CRUISE"
      eng_on = True
      target_vc = min(0.994, 0.15 + (warp_curvature / 10.0) * 0.84)
      cur_vc = min(target_vc, cur_vc + 0.11 * dt)
      cur_g = 1.8
      plasma = 0.0
      morph_ring = 1.0
      morph_wings = 1.0
      warp_tun = float(min(1.0, cur_vc * 1.15))
      space_r = 1.0
      cur_progress += (cur_vc * 0.016) * dt
      pitch_deg = 0.0
    # 5. 反転減速 ＆ ゲートアレスト進入
    else:
      phase = "DECEL_APPROACH"
      eng_on = True
      rem_dist = max(0.0001, 1.0 - cur_progress)
      cur_vc = max(0.008, min(cur_vc, rem_dist * 2.8))
      cur_g = 3.2
      plasma = 0.0
      morph_ring = max(0.2, cur_vc * 1.5)
      morph_wings = 1.0
      warp_tun = float(cur_vc)
      space_r = 1.0
      cur_progress = min(1.0, cur_progress + (cur_vc * 0.012) * dt)
      pitch_deg = 180.0  # 反転減速

    gamma = 1.0 / np.sqrt(max(0.001, 1.0 - (min(0.9995, cur_vc) ** 2)))
    ship_t += dt / gamma
    earth_t += dt * gamma
    temp_k = 293.0 + (cur_mach * 45.0 if cur_alt < 80 else cur_vc * 220.0)

    history.append({
        "t": float(t),
        "phase": phase,
        "alt_km": float(cur_alt),
        "downrange_km": float(cur_downrange),
        "mach": float(cur_mach),
        "vc": float(cur_vc),
        "g": float(cur_g),
        "temp_k": float(temp_k),
        "morph_ring": float(morph_ring),
        "morph_wings": float(morph_wings),
        "warp_tunnel": float(warp_tun),
        "plasma_alpha": float(plasma),
        "space_ratio": float(space_r),
        "progress": float(min(1.0, cur_progress)),
        "ship_time": float(ship_t),
        "earth_time": float(earth_t),
        "engine_active": eng_on,
        "catapult_active": False,
        "rx": float(cur_downrange * 0.1),
        "ry": float(cur_alt * 0.1 + 1.2),
        "pitch_deg": float(pitch_deg),
    })

    if cur_progress >= 0.998 and cur_vc <= 0.03:
      for _ in range(16):
        history.append({
            "t": float(t + 1.0),
            "phase": "ARRIVED",
            "alt_km": float(cur_alt),
            "downrange_km": float(cur_downrange),
            "mach": 0.0,
            "vc": 0.0,
            "g": 1.0,
            "temp_k": 310.0,
            "morph_ring": 0.0,
            "morph_wings": 1.0,
            "warp_tunnel": 0.0,
            "plasma_alpha": 0.0,
            "space_ratio": 1.0,
            "progress": 1.0,
            "ship_time": float(ship_t),
            "earth_time": float(earth_t),
            "engine_active": False,
            "catapult_active": False,
            "rx": float(cur_downrange * 0.1),
            "ry": float(cur_alt * 0.1 + 1.2),
            "pitch_deg": 0.0,
        })
      break

  return history, None


# =========================================================================
# 🚀 実行スイッチ & フロントエンド設定
# =========================================================================
st.markdown("---")
c_run1, c_run2 = st.columns([3, 1])
with c_run1:
  launch_clicked = st.button(
      "🔴 LAUNCH & WARP SEQUENCE (電磁射出 ➔ ワープ跳躍開始)",
      use_container_width=True,
      type="primary",
  )
with c_run2:
  st.caption("※ プロトタイプ安全設計：全パラメータで100%成功し、到着演出まで完走します。")

sim_records, sim_fail = run_simulation(preview_only=(not launch_clicked))

client_config = {
    "is_preview": not launch_clicked,
    "vessel_id": vessel_cfg["id"],
    "style": vessel_cfg["style"],
    "hull_color": int(hull_primary.lstrip("#"), 16),
    "tile_color": int(tile_color.lstrip("#"), 16),
    "flame_hex": power_cfg["flame_hex"],
    "outer_hex": power_cfg["outer_hex"],
    "spark_hex": power_cfg["spark_hex"],
    "dest_type": dest_cfg["type"],
    "dest_color": dest_cfg["color_hex"],
    "radiator_count": radiator_blades,
    "wings_span": wings_span,
    "catapult_angle": catapult_cfg["angle_deg"],
    "catapult_len": catapult_cfg["rail_len"],
}

sim_json = json.dumps(sim_records)
cfg_json = json.dumps(client_config)

# =========================================================================
# 📺 Three.js + Web Audio 一体型描画テンプレート
# =========================================================================
html_markup = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{box-sizing:border-box;}body,html{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:#000206;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#fff;user-select:none;}
#canvas-main{width:100%;height:100%;display:block;position:absolute;top:0;left:0;z-index:1;}
.hud-top{position:absolute;top:0;left:0;width:100%;min-height:44px;background:linear-gradient(180deg,rgba(3,7,18,0.95) 0%,rgba(3,7,18,0.85) 100%);border-bottom:1px solid rgba(56,189,248,0.3);display:flex;align-items:center;justify-content:space-between;padding:4px 18px;z-index:20;font-family:monospace;font-size:11px;}
.pip-box{position:absolute;top:54px;right:14px;width:380px;height:220px;border:2px solid #38bdf8;border-radius:6px;background:#020617;overflow:hidden;z-index:60;box-shadow:0 12px 45px rgba(0,0,0,0.95);}
#canvas-pip{width:100%;height:100%;display:block;}
.pip-tag{position:absolute;top:6px;left:10px;background:rgba(15,23,42,0.92);padding:3px 8px;font-size:9px;font-weight:bold;color:#38bdf8;border-left:2px solid #38bdf8;}
.hud-bottom{position:absolute;bottom:0;left:0;width:100%;height:75px;background:rgba(2,6,23,0.95);border-top:1px solid rgba(255,255,255,0.15);padding:8px 24px;display:flex;align-items:center;justify-content:space-between;z-index:20;}
.telem-box{display:flex;flex-direction:column;}
.telem-lbl{font-size:9px;color:#94a3b8;letter-spacing:1px;}
.telem-val{font-size:clamp(14px,1.8vw,18px);font-weight:900;font-family:monospace;color:#f8fafc;}
.banner{display:none;position:absolute;top:150px;left:50%;transform:translateX(-50%);padding:22px 36px;border-radius:8px;z-index:80;text-align:center;}
.banner-success{background:rgba(6,78,59,0.95);border:2px solid #10b981;box-shadow:0 0 60px rgba(16,185,129,0.8);}
</style></head>
<body>
<canvas id="canvas-main"></canvas>
<div class="pip-box">
    <canvas id="canvas-pip"></canvas>
    <div class="pip-tag" id="pip-label">CAM 02: GROUND CATAPULT TRACKER</div>
</div>
<div class="hud-top">
    <div>SHIP: <strong id="h-ship" style="color:#38bdf8;">WAVERIDER SSTO</strong> | PHASE: <strong id="h-phase" style="color:#f59e0b;">STANDBY</strong></div>
    <div>ALT: <strong id="h-alt" style="color:#f8fafc;">0.0 km</strong> | SPEED: <strong id="h-speed" style="color:#38bdf8;">M 0.0</strong> | SHIP: <strong id="h-stime">00:00.0</strong> | EARTH: <strong id="h-etime">00:00.0</strong></div>
</div>
<div class="banner banner-success" id="b-success">
    <div style="font-size:20px;font-weight:900;color:#6ee7b7;">🎉 INTERPLANETARY WARP COMPLETE 🎉</div>
    <div style="font-size:12px;margin-top:6px;color:#ecfdf5;">DESTINATION MAGNETIC ARREST LOCK ESTABLISHED</div>
</div>
<div class="hud-bottom">
    <div class="telem-box"><div class="telem-lbl">WARP VELOCITY</div><div class="telem-val"><span id="t-vc">0.00</span> <span style="font-size:10px;color:#94a3b8;">c (Light Speed)</span></div></div>
    <div class="telem-box"><div class="telem-lbl">MISSION PROGRESS</div><div class="telem-val"><span id="t-dist">0.0</span> <span style="font-size:10px;color:#94a3b8;">%</span></div></div>
    <div class="telem-box"><div class="telem-lbl">STRUCTURAL LOAD</div><div class="telem-val"><span id="t-g">1.0</span> <span style="font-size:10px;color:#94a3b8;">G (Compensated)</span></div></div>
    <div class="telem-box"><div class="telem-lbl">LORENTZ FACTOR (γ)</div><div class="telem-val"><span id="t-gamma">1.00</span> <span style="font-size:10px;color:#94a3b8;">x</span></div></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
window.addEventListener('DOMContentLoaded',()=>{
try{
const data=__SIM_DATA__;const cfg=__SIM_CFG__;
const cMain=document.getElementById('canvas-main'),cPip=document.getElementById('canvas-pip');
const wMain=window.innerWidth,hMain=window.innerHeight;

// --- Three.js レンダラー ---
const rMain=new THREE.WebGLRenderer({canvas:cMain,antialias:true});rMain.setSize(wMain,hMain);
rMain.toneMapping=THREE.ACESFilmicToneMapping;rMain.toneMappingExposure=1.35;
const rPip=new THREE.WebGLRenderer({canvas:cPip,antialias:true});rPip.setSize(380,220);
rPip.toneMapping=THREE.ACESFilmicToneMapping;
const scene=new THREE.Scene();

const camMain=new THREE.PerspectiveCamera(35,wMain/hMain,0.5,100000);
const camPip=new THREE.PerspectiveCamera(22,380/220,1.0,100000);

const sunLight=new THREE.DirectionalLight(0xffedd5,4.5);sunLight.position.set(1200,1800,900);scene.add(sunLight);
scene.add(new THREE.AmbientLight(0x1e293b,1.6));

// --- Web Audio SF音響シンセシス ---
const AudioCtx=window.AudioContext||window.webkitAudioContext;let actx=null,oscWarp=null,gainWarp=null,subBass=null,catapultHum=null;
function initSFX(){
    if(!actx){
        actx=new AudioCtx();
        // 電磁カタパルト高周波ハム
        const hOsc=actx.createOscillator();hOsc.type='sine';hOsc.frequency.value=220;
        catapultHum=actx.createGain();catapultHum.gain.value=0.0001;
        hOsc.connect(catapultHum);catapultHum.connect(actx.destination);hOsc.start(0);

        // ワープ周波数チャープ
        oscWarp=actx.createOscillator();oscWarp.type='sawtooth';
        const bp=actx.createBiquadFilter();bp.type='bandpass';bp.frequency.value=750;bp.Q.value=3.5;
        gainWarp=actx.createGain();gainWarp.gain.value=0.0001;
        oscWarp.connect(bp);bp.connect(gainWarp);gainWarp.connect(actx.destination);oscWarp.start(0);

        // 重低音サブベース
        const sOsc=actx.createOscillator();sOsc.type='sine';sOsc.frequency.value=36;
        subBass=actx.createGain();subBass.gain.value=0.0001;
        sOsc.connect(subBass);subBass.connect(actx.destination);sOsc.start(0);
    }
    if(actx.state==='suspended')actx.resume();
}
window.addEventListener('click',initSFX,{once:true});

// --- PBR環境マップ＆テクスチャ生成 ---
function createEnvMap(){
    const cvs=document.createElement('canvas');cvs.width=512;cvs.height=256;const ctx=cvs.getContext('2d');
    const g=ctx.createLinearGradient(0,0,0,256);
    g.addColorStop(0,'#030712');g.addColorStop(0.35,'#1e3a8a');g.addColorStop(0.5,'#bae6fd');g.addColorStop(0.6,'#0284c7');g.addColorStop(1,'#041e3a');
    ctx.fillStyle=g;ctx.fillRect(0,0,512,256);
    return new THREE.CanvasTexture(cvs);
}
const envMapTex=createEnvMap();envMapTex.mapping=THREE.EquirectangularReflectionMapping;scene.environment=envMapTex;

// 耐熱カーボンタイル＆溶接パネルテクスチャ
function createTileTexture(){
    const cvs=document.createElement('canvas');cvs.width=512;cvs.height=512;const ctx=cvs.getContext('2d');
    ctx.fillStyle='#111827';ctx.fillRect(0,0,512,512);
    ctx.strokeStyle='#1f2937';ctx.lineWidth=1.5;
    for(let x=0;x<512;x+=24){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,512);ctx.stroke();}
    for(let y=0;y<512;y+=24){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(512,y);ctx.stroke();}
    return new THREE.CanvasTexture(cvs);
}
const tileTex=createTileTexture();tileTex.wrapS=THREE.RepeatWrapping;tileTex.wrapT=THREE.RepeatWrapping;tileTex.repeat.set(12,12);

// --- マテリアル構築 ---
const titaniumMat=new THREE.MeshStandardMaterial({color:cfg.hull_color,roughness:0.18,metalness:0.92,envMap:envMapTex,envMapIntensity:1.8});
const carbonTileMat=new THREE.MeshStandardMaterial({color:cfg.tile_color,roughness:0.75,metalness:0.15,bumpMap:tileTex,bumpScale:0.025});
const goldFoilMat=new THREE.MeshStandardMaterial({color:0xd97706,roughness:0.35,metalness:0.95,bumpMap:tileTex,bumpScale:0.04});
const pipeMat=new THREE.MeshStandardMaterial({color:0x94a3b8,roughness:0.25,metalness:0.95});
const coilGlowMat=new THREE.MeshBasicMaterial({color:0x38bdf8});
const plasmaMat=new THREE.MeshBasicMaterial({color:0xd946ef,transparent:true,opacity:0.0,blending:THREE.AdditiveBlending,side:THREE.DoubleSide});
const flameMat=new THREE.MeshBasicMaterial({color:cfg.flame_hex,transparent:true,opacity:0.85,blending:THREE.AdditiveBlending,side:THREE.DoubleSide});

// --- 地上＆電磁カタパルト施設モデリング ---
const groundGroup=new THREE.Group();scene.add(groundGroup);
const ocean=new THREE.Mesh(new THREE.PlaneGeometry(35000,35000),new THREE.MeshStandardMaterial({color:0x0c2d48,roughness:0.12,metalness:0.85}));
ocean.rotation.x=-Math.PI/2;groundGroup.add(ocean);

// 全長10km超巨大リニアカタパルトレール
const railLen3D=cfg.catapult_len*150.0,catAngleRad=THREE.MathUtils.degToRad(cfg.catapult_angle);
const railGroup=new THREE.Group();groundGroup.add(railGroup);
const railSpine=new THREE.Mesh(new THREE.BoxGeometry(12,8,railLen3D),titaniumMat);
railSpine.position.set(0,railLen3D*0.5*Math.sin(catAngleRad)+2.0,railLen3D*0.5*Math.cos(catAngleRad));
railSpine.rotation.x=catAngleRad;railGroup.add(railSpine);

// カタパルト超伝導コイルリング列
const catapultCoils=[];
for(let c=0;c<28;c++){
    const cMesh=new THREE.Mesh(new THREE.TorusGeometry(14,0.6,12,32),coilGlowMat);
    const zDist=(c/28)*railLen3D;
    cMesh.position.set(0,zDist*Math.sin(catAngleRad)+2.0,zDist*Math.cos(catAngleRad));
    cMesh.rotation.x=catAngleRad;railGroup.add(cMesh);catapultCoils.push(cMesh);
}

// --- 宇宙・大気層・星々 ---
const atmoMesh=new THREE.Mesh(new THREE.SphereGeometry(62000,32,24),new THREE.MeshBasicMaterial({color:0x38bdf8,transparent:true,opacity:0.0,side:THREE.BackSide,blending:THREE.AdditiveBlending}));
scene.add(atmoMesh);
const starGeo=new THREE.BufferGeometry(),starCount=5000;
const starPos=new Float32Array(starCount*3);
for(let i=0;i<starCount*3;i+=3){starPos[i]=(Math.random()-0.5)*15000;starPos[i+1]=(Math.random()-0.5)*15000;starPos[i+2]=(Math.random()-0.5)*25000;}
starGeo.setAttribute('position',new THREE.BufferAttribute(starPos,3));
const starPoints=new THREE.Points(starGeo,new THREE.PointsMaterial({color:0xffffff,size:2.8,transparent:true,opacity:0.8}));
scene.add(starPoints);

// --- リアルSF機体モデリング（ウェイブライダー／流線型／積層アーマー／配管グリーブル） ---
const vesselGroup=new THREE.Group();scene.add(vesselGroup);
const slidingDorsalDoors=[],warpRingGroup=new THREE.Group();

// 1. スプライン曲線による滑らかな極超音速リフティングボディ (Lathe / Convex)
const bodyPts=[];
bodyPts.push(new THREE.Vector2(0.1,16.0));
bodyPts.push(new THREE.Vector2(1.2,12.0));
bodyPts.push(new THREE.Vector2(3.2,4.0));
bodyPts.push(new THREE.Vector2(4.8,-8.0));
bodyPts.push(new THREE.Vector2(4.2,-14.0));
bodyPts.push(new THREE.Vector2(2.5,-16.0));
const bodyCoreGeo=new THREE.LatheGeometry(bodyPts,24);bodyCoreGeo.scale(1.8,0.45,1.0);
const bodyCore=new THREE.Mesh(bodyCoreGeo,titaniumMat);bodyCore.rotation.x=Math.PI/2;vesselGroup.add(bodyCore);

// 2. 腹部・耐熱カーボンタイル層（二重積層）
const heatBelly=new THREE.Mesh(bodyCoreGeo,carbonTileMat);
heatBelly.position.y=-0.25;heatBelly.scale.set(1.01,1.01,1.01);vesselGroup.add(heatBelly);

// 3. 配管・超伝導ソレノイド支柱・金箔MLIグリーブル群
const greebleGroup=new THREE.Group();greebleGroup.position.set(0,0,-12.0);vesselGroup.add(greebleGroup);
for(let i=0;i<6;i++){
    const ang=(i/6)*Math.PI*2;
    const pipe=new THREE.Mesh(new THREE.CylinderGeometry(0.12,0.12,18,8),pipeMat);
    pipe.position.set(Math.cos(ang)*3.8,Math.sin(ang)*1.4,2.0);pipe.rotation.x=Math.PI/2;greebleGroup.add(pipe);
    const mliSheet=new THREE.Mesh(new THREE.BoxGeometry(1.2,0.6,3.5),goldFoilMat);
    mliSheet.position.set(Math.cos(ang)*3.4,Math.sin(ang)*1.2,0.0);greebleGroup.add(mliSheet);
}

// 4. 観音開き上部装甲ドア ＆ せり出し式ワープリング
for(let side of [-1,1]){
    const door=new THREE.Mesh(new THREE.BoxGeometry(3.5,0.4,14),titaniumMat);
    door.position.set(side*2.2,1.2,-2.0);vesselGroup.add(door);
    slidingDorsalDoors.push({mesh:door,side:side});
}
// ワープリング（内部に格納されており、宇宙空間でせり上がる）
warpRingGroup.position.set(0,0.5,-2.0);vesselGroup.add(warpRingGroup);
const warpTorus1=new THREE.Mesh(new THREE.TorusGeometry(5.5,0.35,16,48),coilGlowMat);warpRingGroup.add(warpTorus1);
const warpTorus2=new THREE.Mesh(new THREE.TorusGeometry(6.2,0.25,16,48),titaniumMat);warpRingGroup.add(warpTorus2);

// 5. 空力加熱プラズマシェル ＆ 推力プルーム
const plasmaShell=new THREE.Mesh(new THREE.ConeGeometry(7.5,36,16,1,true),plasmaMat);
plasmaShell.position.z=-4;plasmaShell.rotation.x=-Math.PI/2;vesselGroup.add(plasmaShell);

const mainPlume=new THREE.Mesh(new THREE.ConeGeometry(3.2,28,16,1,true),flameMat);
mainPlume.position.set(0,0,-30);mainPlume.rotation.x=Math.PI/2;mainPlume.visible=false;vesselGroup.add(mainPlume);

// --- 目的地の惑星＆減速ゲート ---
const destGroup=new THREE.Group();destGroup.position.set(0,0,16000);scene.add(destGroup);
const planetMesh=new THREE.Mesh(new THREE.SphereGeometry(1100,48,48),new THREE.MeshStandardMaterial({color:cfg.dest_color,roughness:0.85}));
destGroup.add(planetMesh);
if(cfg.dest_type==='saturn'){
    const ringMesh=new THREE.Mesh(new THREE.RingGeometry(1300,2200,64),new THREE.MeshStandardMaterial({color:0xa8a29e,side:THREE.DoubleSide}));
    ringMesh.rotation.x=Math.PI/2.3;destGroup.add(ringMesh);
}
const catchGate=new THREE.Mesh(new THREE.TorusGeometry(42,2.5,16,48),new THREE.MeshStandardMaterial({color:0x38bdf8,metalness:0.95,roughness:0.2}));
catchGate.position.set(0,0,-1600);destGroup.add(catchGate);

// --- アニメーションループ ---
const tStart=performance.now();let isEnded=false;

function animate(now){
    if(isEnded)return;requestAnimationFrame(animate);
    const elapsed=(now-tStart)/1000.0;
    const simT=cfg.is_preview?-5.0:(-5.0+elapsed*1.8);

    let idx=0;while(idx<data.length-1&&data[idx+1].t<=simT)idx++;
    const p=data[idx];

    // 1. カタパルトコイル順次通電エフェクト
    if(p.phase==="RAIL_ACCELERATION"||p.catapult_active){
        catapultCoils.forEach((cl,i)=>{
            const phaseShift=(now*0.012+i*0.3)%Math.PI;
            cl.material.color.setRGB(0.2+Math.sin(phaseShift)*0.8,0.7+Math.sin(phaseShift)*0.3,1.0);
        });
        if(catapultHum&&actx){catapultHum.gain.setTargetAtTime(0.45,actx.currentTime,0.05);}
    }else{
        if(catapultHum&&actx){catapultHum.gain.setTargetAtTime(0.0001,actx.currentTime,0.15);}
    }

    // 2. オービタルメカ変形（観音開き装甲ドアスライド ＆ ワープリングせり出し）
    slidingDorsalDoors.forEach(sd=>{
        sd.mesh.position.x=sd.side*(2.2+p.morph_ring*3.2);
    });
    warpRingGroup.position.y=0.5+p.morph_ring*3.8;
    warpTorus1.rotation.z+=0.04+p.vc*0.3;warpTorus2.rotation.z-=0.03+p.vc*0.3;

    // 3. 空力加熱プラズマシェル＆大気層
    plasmaMat.opacity=p.plasma_alpha;
    atmoMesh.material.opacity=Math.min(0.42,p.space_ratio*0.45);
    mainPlume.visible=p.engine_active;
    mainPlume.scale.set(1.0+p.vc*2.0,1.0+Math.random()*0.3+p.vc*4.0,1.0+p.vc*2.0);

    // 4. 機体座標・回転追従
    if(p.phase==="RAIL_ACCELERATION"||p.phase==="HYPERSONIC_CLIMB"||p.phase==="PRE_FLIGHT"){
        vesselGroup.position.set(p.rx,p.ry,p.downrange_km*0.1);
        vesselGroup.rotation.set(-THREE.MathUtils.degToRad(p.pitch_deg),0,0);
        groundGroup.visible=true;
    }else{
        // 宇宙空間ワープ航行
        const zProg=p.progress*14200.0;
        vesselGroup.position.set(0,p.ry,zProg);
        vesselGroup.rotation.set(-THREE.MathUtils.degToRad(p.pitch_deg),0,0);
        groundGroup.visible=(p.alt_km<450.0);
    }

    // 5. ワープストレッチ＆音響
    if(p.phase==="WARP_CRUISE"){
        vesselGroup.scale.set(1.0,1.0,1.0+p.vc*3.8);
        camMain.fov=THREE.MathUtils.lerp(camMain.fov,85.0,0.1);
        if(oscWarp&&actx){
            oscWarp.frequency.setTargetAtTime(550+p.vc*1200,actx.currentTime,0.1);
            gainWarp.gain.setTargetAtTime(0.75,actx.currentTime,0.1);
            subBass.gain.setTargetAtTime(0.85,actx.currentTime,0.1);
        }
    }else{
        vesselGroup.scale.set(1.0,1.0,1.0);
        camMain.fov=THREE.MathUtils.lerp(camMain.fov,35.0,0.08);
        if(gainWarp&&actx){gainWarp.gain.setTargetAtTime(0.0001,actx.currentTime,0.2);subBass.gain.setTargetAtTime(0.0001,actx.currentTime,0.2);}
    }
    camMain.updateProjectionMatrix();

    if(p.phase==="ARRIVED"&&document.getElementById('b-success').style.display!=='block'){
        document.getElementById('b-success').style.display='block';
    }

    // カメラワーク（CAM 01: 追従）
    camMain.position.set(vesselGroup.position.x-35.0,vesselGroup.position.y+18.0,vesselGroup.position.z-65.0);
    camMain.lookAt(vesselGroup.position.x,vesselGroup.position.y,vesselGroup.position.z+25.0);

    // カメラワーク（CAM 02: 地上追尾望遠 ➔ 宇宙では目的地の観測ゲート）
    if(p.phase==="WARP_CRUISE"||p.phase==="DECEL_APPROACH"||p.phase==="ARRIVED"){
        camPip.position.set(0,50,14400);
        camPip.lookAt(vesselGroup.position);
        document.getElementById('pip-label').innerText="CAM 02: DESTINATION GATE OBSERVATORY";
    }else{
        camPip.position.set(150.0,35.0,220.0);
        camPip.lookAt(vesselGroup.position);
        document.getElementById('pip-label').innerText="CAM 02: GROUND OPTICAL TRACKER";
    }
    rPip.render(scene,camPip);

    // メイン描画
    rMain.render(scene,camMain);

    // テレメトリHUD更新
    document.getElementById('h-ship').innerText=cfg.vessel_id.toUpperCase();
    document.getElementById('h-phase').innerText=p.phase;
    document.getElementById('h-alt').innerText=`${p.alt_km.toFixed(1)} km`;
    document.getElementById('h-speed').innerText=`M ${p.mach.toFixed(1)}`;
    document.getElementById('h-stime').innerText=`T+ ${p.ship_time.toFixed(1)}s`;
    document.getElementById('h-etime').innerText=`T+ ${p.earth_time.toFixed(1)}s`;
    document.getElementById('t-vc').innerText=p.vc.toFixed(3);
    document.getElementById('t-dist').innerText=(p.progress*100.0).toFixed(1);
    document.getElementById('t-g').innerText=p.g.toFixed(1);
    const gamma=1.0/Math.sqrt(Math.max(0.001,1.0-Math.min(0.9995,p.vc)**2));
    document.getElementById('t-gamma').innerText=gamma.toFixed(2);
}
requestAnimationFrame(animate);

window.addEventListener('resize',()=>{
    const w=window.innerWidth,h=window.innerHeight;
    rMain.setSize(w,h);camMain.aspect=w/h;camMain.updateProjectionMatrix();
});
}catch(e){console.error(e);}
});
</script></body></html>"""

final_html = (
    html_markup.replace("__SIM_DATA__", sim_json)
    .replace("__SIM_CFG__", cfg_json)
)

components.html(final_html, height=880)

if launch_clicked:
  st.markdown("---")
  st.success("🎉 **ミッション完全成功**: 地上電磁射出から大気圏極超音速突破、軌道上ワープ変形、目的宙域ゲート到達シーケンスが設計通り正常に完了しました。")
