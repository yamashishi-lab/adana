import json
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hyper-Drive Architect: Apex WaveRider Pro",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("🛸 Hyper-Drive Architect: Apex WaveRider Pro")
st.caption(
    "※ 4K実写級：海上メガ・マスドライバー射出・富士山麓絶景・精密モジュールSSTO・ワープ跳躍完全版 (Safe Mode)"
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
    "富士山麓 軌道射出リニアチューブ (標高3,776m直結)": {
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
# 💥 時空物理シミュレーション演算
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
    elif cur_alt < 120.0:
      phase = "HYPERSONIC_CLIMB"
      eng_on = True
      cur_mach = min(32.0, cur_mach + 1.8 * dt)
      climb_speed = cur_mach * 340.0
      cur_alt += (climb_speed * np.sin(c_angle_rad) * dt) / 1000.0
      cur_downrange += (climb_speed * np.cos(c_angle_rad) * dt) / 1000.0
      cur_g = 4.2
      if 15.0 <= cur_alt <= 75.0:
        plasma = float(np.sin(((cur_alt - 15.0) / 60.0) * np.pi) * 0.95)
      else:
        plasma = 0.0
      morph_ring = 0.0
      morph_wings = min(1.0, (cur_alt / 80.0))
      warp_tun = 0.0
      space_r = float(np.clip((cur_alt - 15.0) / 75.0, 0.0, 1.0))
      pitch_deg = float(catapult_cfg["angle_deg"] * (1.0 - space_r * 0.7))
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
      pitch_deg = 180.0

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
# 📺 Three.js + Web Audio 最適化描画テンプレート (PiP完全レスポンシブ移植)
# =========================================================================
html_markup = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{box-sizing:border-box;}body,html{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:#000206;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#fff;user-select:none;}
#canvas-main{width:100%;height:100%;display:block;position:absolute;top:0;left:0;z-index:1;}
.top-banner{position:absolute;top:0;left:0;width:100%;min-height:42px;background:linear-gradient(180deg,rgba(2,6,16,0.96) 0%,rgba(3,10,24,0.92) 100%);border-bottom:1px solid rgba(56,189,248,0.22);display:flex;align-items:center;justify-content:space-between;padding:4px 14px;z-index:20;flex-wrap:wrap;gap:6px 12px;box-shadow:0 4px 20px rgba(0,0,0,0.7);}
.banner-group{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}
.pip-container{position:absolute;top:48px;right:8px;width:410px;max-width:calc(100vw - 16px);height:235px;border:2px solid rgba(56,189,248,0.95);border-radius:6px;z-index:60;box-shadow:0 14px 45px rgba(0,0,0,0.98);background:#071526;overflow:hidden;cursor:pointer;transition:height 0.25s ease;}
#canvas-pip{width:100%;height:100%;display:block;}
.pip-tag{position:absolute;top:6px;left:12px;font-size:10px;font-weight:800;color:#fff;background:rgba(15,23,42,0.94);padding:3px 8px;border-radius:2px;letter-spacing:1px;font-family:monospace;z-index:65;pointer-events:none;border-left:2px solid #38bdf8;}
.pip-hint{position:absolute;top:6px;right:12px;font-size:9px;font-family:monospace;color:#94a3b8;background:rgba(15,23,42,0.94);padding:3px 6px;border-radius:2px;z-index:65;pointer-events:none;}
.hud-bottom{position:absolute;bottom:0;left:0;width:100%;height:75px;background:rgba(2,6,23,0.95);border-top:1px solid rgba(255,255,255,0.15);padding:8px 24px;display:flex;align-items:center;justify-content:space-between;z-index:20;}
.telem-box{display:flex;flex-direction:column;}
.telem-lbl{font-size:9px;color:#94a3b8;letter-spacing:1px;}
.telem-val{font-size:clamp(14px,1.8vw,18px);font-weight:900;font-family:monospace;color:#f8fafc;}
.banner{display:none;position:absolute;top:150px;left:50%;transform:translateX(-50%);padding:22px 36px;border-radius:8px;z-index:80;text-align:center;}
.banner-success{background:rgba(6,78,59,0.95);border:2px solid #10b981;box-shadow:0 0 60px rgba(16,185,129,0.8);}
</style></head>
<body>
<canvas id="canvas-main"></canvas>
<div id="pip-box" class="pip-container" title="クリックでCAM 02の表示/非表示を切り替え">
    <canvas id="canvas-pip"></canvas>
    <div id="pip-tag" class="pip-tag">CAM 02: GROUND CATAPULT TRACKER</div>
    <div id="pip-hint" class="pip-hint">[CLICK TO TOGGLE]</div>
</div>
<div class="top-banner" id="top-banner-bar">
    <div class="banner-group">
        <span style="color:#38bdf8;font-weight:800;font-size:11px;letter-spacing:1.5px;">WAVERIDER SSTO</span>
        <span style="color:rgba(255,255,255,0.2);">|</span>
        <span style="color:#94a3b8;font-family:monospace;font-size:10px;">PHASE: <strong id="h-phase" style="color:#f59e0b;">STANDBY</strong></span>
    </div>
    <div class="banner-group" style="font-family:monospace;font-size:10px;">
        <span style="color:#94a3b8;">ALT: <strong id="h-alt" style="color:#f8fafc;">0.0 km</strong></span>
        <span style="color:#94a3b8;">SPEED: <strong id="h-speed" style="color:#38bdf8;">M 0.0</strong></span>
        <span style="color:#94a3b8;">SHIP: <strong id="h-stime">00:00.0</strong></span>
    </div>
</div>
<div class="banner banner-success" id="b-success">
    <div style="font-size:20px;font-weight:900;color:#6ee7b7;">🎉 INTERPLANETARY WARP COMPLETE 🎉</div>
    <div style="font-size:12px;margin-top:6px;color:#ecfdf5;">DESTINATION MAGNETIC ARREST LOCK ESTABLISHED</div>
</div>
<div class="hud-bottom">
    <div class="telem-box"><div class="telem-lbl">WARP VELOCITY</div><div class="telem-val"><span id="t-vc">0.00</span> <span style="font-size:10px;color:#94a3b8;">c</span></div></div>
    <div class="telem-box"><div class="telem-lbl">MISSION PROGRESS</div><div class="telem-val"><span id="t-dist">0.0</span> <span style="font-size:10px;color:#94a3b8;">%</span></div></div>
    <div class="telem-box"><div class="telem-lbl">STRUCTURAL LOAD</div><div class="telem-val"><span id="t-g">1.0</span> <span style="font-size:10px;color:#94a3b8;">G</span></div></div>
    <div class="telem-box"><div class="telem-lbl">LORENTZ FACTOR (γ)</div><div class="telem-val"><span id="t-gamma">1.00</span> <span style="font-size:10px;color:#94a3b8;">x</span></div></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
window.addEventListener('DOMContentLoaded',()=>{
try{
const data=__SIM_DATA__;const cfg=__SIM_CFG__;
const cMain=document.getElementById('canvas-main'),cPip=document.getElementById('canvas-pip');
const wMain=window.innerWidth,hMain=window.innerHeight;
const pipBox=document.getElementById('pip-box'),topBannerBar=document.getElementById('top-banner-bar');
let pipVisible=true;

function updatePipPosition(){if(pipBox&&topBannerBar){const rect=topBannerBar.getBoundingClientRect();pipBox.style.top=Math.round(rect.bottom+4)+'px';}}
updatePipPosition();
function resizePipRenderer(){if(pipBox&&pipVisible){const w=pipBox.clientWidth||410,h=235;rendererPip.setSize(w,h,false);cameraPip.aspect=w/h;cameraPip.updateProjectionMatrix();}}
window.addEventListener('resize',()=>{updatePipPosition();resizePipRenderer();});

pipBox.addEventListener('click',()=>{
    pipVisible=!pipVisible;cPip.style.visibility=pipVisible?'visible':'hidden';
    document.getElementById('pip-tag').style.display=pipVisible?'block':'none';
    pipBox.style.height=pipVisible?'235px':'32px';
    document.getElementById('pip-hint').innerText=pipVisible?'[CLICK TO HIDE]':'[CLICK TO SHOW]';
    if(pipVisible){resizePipRenderer();rendererPip.render(scene,cameraPip);}
});

// --- Three.js 最適化レンダラー ---
const rendererMain=new THREE.WebGLRenderer({canvas:cMain,antialias:true,powerPreference:"high-performance"});
rendererMain.setPixelRatio(Math.min(window.devicePixelRatio,1.5));rendererMain.setSize(wMain,hMain);
rendererMain.toneMapping=THREE.ACESFilmicToneMapping;rendererMain.toneMappingExposure=1.35;

const rendererPip=new THREE.WebGLRenderer({canvas:cPip,antialias:true});
rendererPip.setPixelRatio(1.0);rendererPip.setSize(410,235);
rendererPip.toneMapping=THREE.ACESFilmicToneMapping;

const scene=new THREE.Scene();scene.fog=new THREE.FogExp2(0x38bdf8,0.000035);

const cameraMain=new THREE.PerspectiveCamera(35,wMain/hMain,0.5,100000);
const cameraPip=new THREE.PerspectiveCamera(22,410/235,1.0,100000);

const sunLight=new THREE.DirectionalLight(0xffedd5,4.5);sunLight.position.set(1200,1800,900);scene.add(sunLight);
scene.add(new THREE.AmbientLight(0x1e293b,1.6));

// --- Web Audio SF音響シンセシス ---
const AudioCtx=window.AudioContext||window.webkitAudioContext;let actx=null,oscWarp=null,gainWarp=null,subBass=null,catapultHum=null;
function initSFX(){
    if(!actx){
        actx=new AudioCtx();
        const hOsc=actx.createOscillator();hOsc.type='sine';hOsc.frequency.value=220;
        catapultHum=actx.createGain();catapultHum.gain.value=0.0001;
        hOsc.connect(catapultHum);catapultHum.connect(actx.destination);hOsc.start(0);

        oscWarp=actx.createOscillator();oscWarp.type='sawtooth';
        const bp=actx.createBiquadFilter();bp.type='bandpass';bp.frequency.value=750;bp.Q.value=3.5;
        gainWarp=actx.createGain();gainWarp.gain.value=0.0001;
        oscWarp.connect(bp);bp.connect(gainWarp);gainWarp.connect(actx.destination);oscWarp.start(0);

        const sOsc=actx.createOscillator();sOsc.type='sine';sOsc.frequency.value=36;
        subBass=actx.createGain();subBass.gain.value=0.0001;
        sOsc.connect(subBass);subBass.connect(actx.destination);sOsc.start(0);
    }
    if(actx.state==='suspended')actx.resume();
}
window.addEventListener('click',initSFX,{once:true});

// --- PBR環境マップ＆高精細テクスチャ生成 ---
function createEnvMap(){
    const cvs=document.createElement('canvas');cvs.width=512;cvs.height=256;const ctx=cvs.getContext('2d');
    const g=ctx.createLinearGradient(0,0,0,256);
    g.addColorStop(0,'#030712');g.addColorStop(0.35,'#1e3a8a');g.addColorStop(0.5,'#bae6fd');g.addColorStop(0.6,'#0284c7');g.addColorStop(1,'#041e3a');
    ctx.fillStyle=g;ctx.fillRect(0,0,512,256);
    return new THREE.CanvasTexture(cvs);
}
const envMapTex=createEnvMap();envMapTex.mapping=THREE.EquirectangularReflectionMapping;scene.environment=envMapTex;

function createTileTexture(){
    const cvs=document.createElement('canvas');cvs.width=512;cvs.height=512;const ctx=cvs.getContext('2d');
    ctx.fillStyle='#111827';ctx.fillRect(0,0,512,512);
    ctx.strokeStyle='#1f2937';ctx.lineWidth=1.5;
    for(let x=0;x<512;x+=24){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,512);ctx.stroke();}
    for(let y=0;y<512;y+=24){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(512,y);ctx.stroke();}
    return new THREE.CanvasTexture(cvs);
}
const tileTex=createTileTexture();tileTex.wrapS=THREE.RepeatWrapping;tileTex.wrapT=THREE.RepeatWrapping;tileTex.repeat.set(12,12);

const titaniumMat=new THREE.MeshStandardMaterial({color:cfg.hull_color,roughness:0.18,metalness:0.92,envMap:envMapTex,envMapIntensity:1.8});
const carbonTileMat=new THREE.MeshStandardMaterial({color:cfg.tile_color,roughness:0.75,metalness:0.15,bumpMap:tileTex,bumpScale:0.025});
const goldFoilMat=new THREE.MeshStandardMaterial({color:0xd97706,roughness:0.35,metalness:0.95});
const pipeMat=new THREE.MeshStandardMaterial({color:0x94a3b8,roughness:0.25,metalness:0.95});
const canopyMat=new THREE.MeshPhysicalMaterial({color:0x38bdf8,roughness:0.1,metalness:0.9,transparent:true,opacity:0.82,transmission:0.6});
const coilGlowMat=new THREE.MeshBasicMaterial({color:0x38bdf8});
const plasmaMat=new THREE.MeshBasicMaterial({color:0xd946ef,transparent:true,opacity:0.0,blending:THREE.AdditiveBlending,side:THREE.DoubleSide});
const flameMat=new THREE.MeshBasicMaterial({color:cfg.flame_hex,transparent:true,opacity:0.85,blending:THREE.AdditiveBlending,side:THREE.DoubleSide});

// --- 美しいリアル地上・富士山・海・橋脚シーン ---
const groundGroup=new THREE.Group();scene.add(groundGroup);
const ocean=new THREE.Mesh(new THREE.PlaneGeometry(50000,50000),new THREE.MeshStandardMaterial({color:0x0c2d48,roughness:0.12,metalness:0.85}));
ocean.rotation.x=-Math.PI/2;groundGroup.add(ocean);

// 富士山麓コーン
const mtnMat=new THREE.MeshStandardMaterial({color:0x22303c,roughness:0.9});
const mtn=new THREE.Mesh(new THREE.ConeGeometry(9000,3200,32),mtnMat);mtn.position.set(12000,1600,-18000);groundGroup.add(mtn);
const snowCap=new THREE.Mesh(new THREE.ConeGeometry(3200,1150,32),new THREE.MeshStandardMaterial({color:0xffffff,roughness:0.5}));
snowCap.position.set(12000,2620,-18000);groundGroup.add(snowCap);

// 巨大メガカタパルトレール ＆ 橋脚群
const railLen3D=cfg.catapult_len*150.0,catAngleRad=THREE.MathUtils.degToRad(cfg.catapult_angle);
const railGroup=new THREE.Group();groundGroup.add(railGroup);
const railSpine=new THREE.Mesh(new THREE.BoxGeometry(12,8,railLen3D),titaniumMat);
railSpine.position.set(0,railLen3D*0.5*Math.sin(catAngleRad)+2.0,railLen3D*0.5*Math.cos(catAngleRad));
railSpine.rotation.x=catAngleRad;railGroup.add(railSpine);

const catapultCoils=[];
for(let c=0;c<24;c++){
    const cMesh=new THREE.Mesh(new THREE.TorusGeometry(14,0.6,12,32),coilGlowMat);
    const zDist=(c/24)*railLen3D;
    cMesh.position.set(0,zDist*Math.sin(catAngleRad)+2.0,zDist*Math.cos(catAngleRad));
    cMesh.rotation.x=catAngleRad;railGroup.add(cMesh);catapultCoils.push(cMesh);
}

// 雲海デッキ (高度1.3km)
const cloudGroup=new THREE.Group();groundGroup.add(cloudGroup);
const cloudGeo=new THREE.PlaneGeometry(400,200);
for(let ci=0;ci<40;ci++){
    const cp=new THREE.Mesh(cloudGeo,new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0.35,depthWrite:false}));
    cp.rotation.x=-Math.PI/2;cp.position.set((Math.random()-0.5)*35000,1300,(Math.random()-0.5)*35000);
    cloudGroup.add(cp);
}

// --- 宇宙・星々 ---
const starGeo=new THREE.BufferGeometry(),starCount=4000;
const starPos=new Float32Array(starCount*3);
for(let i=0;i<starCount*3;i+=3){starPos[i]=(Math.random()-0.5)*15000;starPos[i+1]=(Math.random()-0.5)*15000;starPos[i+2]=(Math.random()-0.5)*25000;}
starGeo.setAttribute('position',new THREE.BufferAttribute(starPos,3));
const starPoints=new THREE.Points(starGeo,new THREE.PointsMaterial({color:0xffffff,size:2.8,transparent:true,opacity:0.8}));
scene.add(starPoints);

// --- 精密モジュール組み立て式SSTO ---
const vesselGroup=new THREE.Group();scene.add(vesselGroup);
const slidingDorsalDoors=[],warpRingGroup=new THREE.Group();

// 1. スプライン曲線ボディ ＆ 金色キャノピー
const bodyPts=[new THREE.Vector2(0.1,16.0),new THREE.Vector2(1.2,12.0),new THREE.Vector2(3.2,4.0),new THREE.Vector2(4.8,-8.0),new THREE.Vector2(4.2,-14.0),new THREE.Vector2(2.5,-16.0)];
const bodyCoreGeo=new THREE.LatheGeometry(bodyPts,24);bodyCoreGeo.scale(1.8,0.45,1.0);
const bodyCore=new THREE.Mesh(bodyCoreGeo,titaniumMat);bodyCore.rotation.x=Math.PI/2;vesselGroup.add(bodyCore);
const heatBelly=new THREE.Mesh(bodyCoreGeo,carbonTileMat);heatBelly.position.y=-0.25;heatBelly.scale.set(1.01,1.01,1.01);vesselGroup.add(heatBelly);

const canopy=new THREE.Mesh(new THREE.ConeGeometry(1.4,7.0,16),canopyMat);canopy.scale.set(1.0,0.5,1.8);canopy.rotation.x=Math.PI/2;canopy.position.set(0,0.6,8.2);vesselGroup.add(canopy);

// 2. デルタ主翼 ＆ Vテイル尾翼
const wingShape=new THREE.Shape();wingShape.moveTo(0,4);wingShape.lineTo(cfg.wings_span*0.5,-6);wingShape.lineTo(0,-12);wingShape.closePath();
const mainWing=new THREE.Mesh(new THREE.ShapeGeometry(wingShape),titaniumMat);mainWing.rotation.x=Math.PI/2;mainWing.position.y=-0.1;vesselGroup.add(mainWing);

for(let side of [-1,1]){
    const vTail=new THREE.Mesh(new THREE.BoxGeometry(0.2,4.5,6.0),titaniumMat);
    vTail.position.set(side*2.5,2.2,-12.5);vTail.rotation.z=side*0.25;vesselGroup.add(vTail);
}

// 3. 配管・MLI断熱材グリーブル
const greebleGroup=new THREE.Group();greebleGroup.position.set(0,0,-12.0);vesselGroup.add(greebleGroup);
for(let i=0;i<4;i++){
    const ang=(i/4)*Math.PI*2;
    const pipe=new THREE.Mesh(new THREE.CylinderGeometry(0.1,0.1,16,8),pipeMat);pipe.position.set(Math.cos(ang)*3.6,Math.sin(ang)*1.2,1.0);pipe.rotation.x=Math.PI/2;greebleGroup.add(pipe);
    const mli=new THREE.Mesh(new THREE.BoxGeometry(1.0,0.5,3.0),goldFoilMat);mli.position.set(Math.cos(ang)*3.2,Math.sin(ang)*1.0,0.0);greebleGroup.add(mli);
}

// 4. 観音開き上部装甲 ＆ ワープリング
for(let side of [-1,1]){
    const door=new THREE.Mesh(new THREE.BoxGeometry(3.5,0.4,14),titaniumMat);door.position.set(side*2.2,1.2,-2.0);vesselGroup.add(door);
    slidingDorsalDoors.push({mesh:door,side:side});
}
warpRingGroup.position.set(0,0.5,-2.0);vesselGroup.add(warpRingGroup);
const warpTorus1=new THREE.Mesh(new THREE.TorusGeometry(5.5,0.35,16,48),coilGlowMat);warpRingGroup.add(warpTorus1);
const warpTorus2=new THREE.Mesh(new THREE.TorusGeometry(6.2,0.25,16,48),titaniumMat);warpRingGroup.add(warpTorus2);

// 5. 空力加熱プラズマシェル ＆ 推進エンジン炎
const plasmaShell=new THREE.Mesh(new THREE.ConeGeometry(7.5,36,16,1,true),plasmaMat);plasmaShell.position.z=-4;plasmaShell.rotation.x=-Math.PI/2;vesselGroup.add(plasmaShell);
const mainPlume=new THREE.Mesh(new THREE.ConeGeometry(3.2,28,16,1,true),flameMat);mainPlume.position.set(0,0,-30);mainPlume.rotation.x=Math.PI/2;mainPlume.visible=false;vesselGroup.add(mainPlume);

// --- 目的地の惑星＆ゲート ---
const destGroup=new THREE.Group();destGroup.position.set(0,0,16000);scene.add(destGroup);
const planetMesh=new THREE.Mesh(new THREE.SphereGeometry(1100,48,48),new THREE.MeshStandardMaterial({color:cfg.dest_color,roughness:0.85}));
destGroup.add(planetMesh);
if(cfg.dest_type==='saturn'){
    const ringMesh=new THREE.Mesh(new THREE.RingGeometry(1300,2200,64),new THREE.MeshStandardMaterial({color:0xa8a29e,side:THREE.DoubleSide}));
    ringMesh.rotation.x=Math.PI/2.3;destGroup.add(ringMesh);
}
const catchGate=new THREE.Mesh(new THREE.TorusGeometry(42,2.5,16,48),new THREE.MeshStandardMaterial({color:0x38bdf8,metalness:0.95,roughness:0.2}));
catchGate.position.set(0,0,-1600);destGroup.add(catchGate);

// --- 最適化アニメーションループ ---
const tStart=performance.now();let isEnded=false;

function animate(now){
    if(isEnded)return;requestAnimationFrame(animate);
    const elapsed=(now-tStart)/1000.0;
    const simT=cfg.is_preview?-5.0:(-5.0+elapsed*1.8);

    let idx=0;while(idx<data.length-1&&data[idx+1].t<=simT)idx++;
    const p=data[idx];

    // カタパルト通電
    if(p.phase==="RAIL_ACCELERATION"||p.catapult_active){
        catapultCoils.forEach((cl,i)=>{
            const shift=(now*0.012+i*0.3)%Math.PI;
            cl.material.color.setRGB(0.2+Math.sin(shift)*0.8,0.7+Math.sin(shift)*0.3,1.0);
        });
        if(catapultHum&&actx)catapultHum.gain.setTargetAtTime(0.45,actx.currentTime,0.05);
    }else{
        if(catapultHum&&actx)catapultHum.gain.setTargetAtTime(0.0001,actx.currentTime,0.15);
    }

    // メカ変形
    slidingDorsalDoors.forEach(sd=>{sd.mesh.position.x=sd.side*(2.2+p.morph_ring*3.2);});
    warpRingGroup.position.y=0.5+p.morph_ring*3.8;
    warpTorus1.rotation.z+=0.04+p.vc*0.3;warpTorus2.rotation.z-=0.03+p.vc*0.3;

    plasmaMat.opacity=p.plasma_alpha;
    mainPlume.visible=p.engine_active;
    mainPlume.scale.set(1.0+p.vc*2.0,1.0+Math.random()*0.3+p.vc*4.0,1.0+p.vc*2.0);

    // 機体位置
    if(p.phase==="RAIL_ACCELERATION"||p.phase==="HYPERSONIC_CLIMB"||p.phase==="PRE_FLIGHT"){
        vesselGroup.position.set(p.rx,p.ry,p.downrange_km*0.1);
        vesselGroup.rotation.set(-THREE.MathUtils.degToRad(p.pitch_deg),0,0);
        groundGroup.visible=true;
    }else{
        const zProg=p.progress*14200.0;
        vesselGroup.position.set(0,p.ry,zProg);
        vesselGroup.rotation.set(-THREE.MathUtils.degToRad(p.pitch_deg),0,0);
        groundGroup.visible=(p.alt_km<450.0);
    }

    // ワープストレッチ ＆ 音響
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
        setTimeout(()=>{isEnded=true;},4000);
    }

    // メインカメラ
    camMain.position.set(vesselGroup.position.x-35.0,vesselGroup.position.y+18.0,vesselGroup.position.z-65.0);
    camMain.lookAt(vesselGroup.position.x,vesselGroup.position.y,vesselGroup.position.z+25.0);

    // PiPカメラ (CAM 02)
    if(p.phase==="WARP_CRUISE"||p.phase==="DECEL_APPROACH"||p.phase==="ARRIVED"){
        camPip.position.set(0,50,14400);camPip.lookAt(vesselGroup.position);
    }else{
        camPip.position.set(150.0,35.0,220.0);camPip.lookAt(vesselGroup.position);
    }
    rendererPip.render(scene,cameraPip);
    rendererMain.render(scene,cameraMain);

    // HUD更新
    document.getElementById('h-phase').innerText=p.phase;
    document.getElementById('h-alt').innerText=`${p.alt_km.toFixed(1)} km`;
    document.getElementById('h-speed').innerText=`M ${p.mach.toFixed(1)}`;
    document.getElementById('h-stime').innerText=`T+ ${p.ship_time.toFixed(1)}s`;
    document.getElementById('t-vc').innerText=p.vc.toFixed(3);
    document.getElementById('t-dist').innerText=(p.progress*100.0).toFixed(1);
    document.getElementById('t-g').innerText=p.g.toFixed(1);
    const gamma=1.0/Math.sqrt(Math.max(0.001,1.0-Math.min(0.9995,p.vc)**2));
    document.getElementById('t-gamma').innerText=gamma.toFixed(2);
}
requestAnimationFrame(animate);

window.addEventListener('resize',()=>{
    updatePipPosition();resizePipRenderer();
    const w=window.innerWidth,h=window.innerHeight;
    rendererMain.setSize(w,h);camMain.aspect=w/h;camMain.updateProjectionMatrix();
});
}catch(err){console.error("Render Error:",err);}
});
</script></body></html>"""

final_html = (
    html_markup.replace("__SIM_DATA__", sim_json)
    .replace("__SIM_CFG__", cfg_json)
)

components.html(final_html, height=880)

if launch_clicked:
  st.markdown("---")
  st.success("🎉 **ミッション完全成功**: 海上メガカタパルト射出、富士山麓上空突破、軌道上ワープ変形、目的宙域ゲート到達シーケンスが設計通り正常に完了しました。")
