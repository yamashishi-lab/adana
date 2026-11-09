import json
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hyper-Drive Architect: Apex Cosmos (Prototype Safe Mode)",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("🛸 Hyper-Drive Architect: Apex Cosmos")
st.caption(
    "※ プロトタイプ安全航行モード：RUD判定完全無効化・全ビークル/パラメータ100%成功・変形＆ワープ演出完全再現版"
)

# =========================================================================
# 🌌 SF機体・コア・マテリアル・航路データベース
# =========================================================================
VESSEL_CLASSES = {
    "【極超音速強襲艦】アーク・ロンギヌス (Arch-Longinus)": {
        "id": "arch_longinus",
        "style": "stealth_assault",
        "base_mass": 380.0,
        "warp_eff": 1.75,
        "desc": "多面体ステルス装甲と電磁砲身。加速時に外装がスライド展開し、内部放熱骨格が露出する重武装強襲艦。",
    },
    "【特異点重力艦】オベリスク・アイオーン (Aeon-Obelisk)": {
        "id": "aeon_obelisk",
        "style": "floating_monolith",
        "base_mass": 720.0,
        "warp_eff": 2.10,
        "desc": "船体から物理切断された4基の浮遊重力バインダーが旋回。中央の3軸ジャイロと黒孔特異点で空間を圧搾する。",
    },
    "【高機動可変翼機】ヴァルキリー・ノヴァ (Valkyrie-Nova)": {
        "id": "valkyrie_nova",
        "style": "variable_striker",
        "base_mass": 210.0,
        "warp_eff": 1.90,
        "desc": "前進翼からX字逆関節へと多段階変形する深宇宙迎撃機。チャージ時の溜めから一気に幾何学光帆を解放する。",
    },
    "【超時空・移動屋台】ネオ銀河軒 壱号機 (Neo-Gingaken)": {
        "id": "neo_gingaken",
        "style": "cyber_ramen",
        "base_mass": 18.0,
        "warp_eff": 2.50,
        "desc": "サイバーパンクのれんと発光提灯。スープ圧力限界をタキオン噴射へ直結させ、時空を暴力的に突破する特級怪奇艦。",
    },
}

POWER_SYSTEMS = {
    "量子真空・零点エネルギー抽出炉 (ZPE Siphon)": {
        "power_gw": 120000.0,
        "glow_hex": 0x38BDF8,
    },
    "マイクロ特異点・降着円盤コア (Kerr Blackhole)": {
        "power_gw": 240000.0,
        "glow_hex": 0xA855F7,
    },
    "超対称性・反物質対消滅ビーム炉 (Antimatter Torch)": {
        "power_gw": 320000.0,
        "glow_hex": 0xF43F5E,
    },
    "【怪異】ネコ・バタートースト共振永久機関": {
        "power_gw": 999999.0,
        "glow_hex": 0xFBBF24,
    },
}

WAYPOINTS = {
    "火星 オリンポス・テラフォーミング回廊 (Mars Base)": {
        "dist_au": 0.52,
        "color_hex": 0xC2410C,
        "type": "mars",
        "desc": "赤色惑星の軌道上に展開する第1電磁減速リングへダイブ。",
    },
    "木星 大赤斑・重力アンカー採掘ハブ (Jupiter Core)": {
        "dist_au": 4.20,
        "color_hex": 0xD97706,
        "type": "jupiter",
        "desc": "激しい雷雲と乱気流の直上、浮遊メガフロートへ突入。",
    },
    "土星リング 氷冠スターゲート「クロノス」 (Saturn Gate)": {
        "dist_au": 9.58,
        "color_hex": 0x94A3B8,
        "type": "saturn",
        "desc": "数億の氷塊が回転するリング間隙の超大型アレストリング。",
    },
    "特異点「ガルガンチュア」事象の地平面スレスレ観光 (Singularity)": {
        "dist_au": 18000.0,
        "color_hex": 0x1E1B4B,
        "type": "blackhole",
        "desc": "歪んだ光の輪に突っ込み、極限の重力時間遅延を測定する決死航行。",
    },
}

# =========================================================================
# 🎛️ パラメータ設定UI
# =========================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🛸 機体設計 & ステルス装甲",
    "⚡ 時空駆動炉 & 慣性ダンパー",
    "🛡️ ハニカムシールド & 放熱系",
    "🎯 目的地航路 & フリップ減速",
])

with tab1:
  col1, col2 = st.columns(2)
  with col1:
    vessel_sel = st.selectbox("ベース艦種 (Chassis)", list(VESSEL_CLASSES.keys()))
    chassis_info = VESSEL_CLASSES[vessel_sel]
    hull_tint = st.color_picker("船体装甲プレート配色", "#1e293b")
    circuit_color = st.color_picker("エミッシブ回路（トロンライン）配色", "#00ffff")
  with col2:
    st.info(f"**艦種概要:** {chassis_info['desc']}")
    armor_thickness = st.slider("積層プレート厚み (mm)", 20, 250, 85, step=5)
    window_density = st.slider("船体居住区・窓発光密度", 100, 2000, 800, step=100)

with tab2:
  col1, col2 = st.columns(2)
  with col1:
    power_sel = st.selectbox("主推進動力炉", list(POWER_SYSTEMS.keys()))
    power_info = POWER_SYSTEMS[power_sel]
    warp_curvature = st.slider("空間曲率倍率 (Warp Factor)", 1.0, 9.9, 8.2, step=0.1)
  with col2:
    throttle_pct = st.slider("ドライブ出力リミッター (%)", 50, 160, 110, step=5)
    damper_rate = st.slider(
        "慣性ダンパー相殺率 (%)",
        99.000,
        99.999,
        99.998,
        step=0.001,
        format="%.3f%%",
    )
    st.caption("※ プロトタイプ中は安全リミッターにより過大Gは自動吸収されます。")

with tab3:
  col1, col2 = st.columns(2)
  with col1:
    deflector_pwr = st.slider("ハニカムデフレクター出力 (GW)", 200, 3000, 1600, step=50)
    deflector_radius = st.slider("シールド投影半径 (m)", 15.0, 60.0, 32.0, step=1.0)
  with col2:
    radiator_blades = st.slider("排熱スライドラジエーター枚数", 2, 8, 4, step=2)
    coolant_flow = st.slider("極低温ヘリウム循環レート (kL/s)", 50, 900, 480, step=10)
    st.caption("※ 船内温度は常に安全冷却範囲（300K〜550K）へ自動調整されます。")

with tab4:
  col1, col2 = st.columns(2)
  with col1:
    waypoint_sel = st.selectbox("到達目標宙域", list(WAYPOINTS.keys()))
    waypoint_info = WAYPOINTS[waypoint_sel]
    st.caption(f"**目的宙域環境:** {waypoint_info['desc']}")
  with col2:
    flip_ratio = st.slider(
        "反転逆噴射 (フリップ＆バーン) 開始位置比率",
        0.50,
        0.95,
        0.72,
        step=0.01,
    )
    st.caption("※ 航法AIが最適な減速Gカーブを自動計算し、100%確実にゲート内へ停止します。")

# =========================================================================
# 💥 時空物理シミュレーション演算（全設定成功・完全保証ロジック）
# =========================================================================
def run_simulation(preview_only=False):
  if preview_only:
    return [{
        "t": 0.0,
        "ship_time": 0.0,
        "earth_time": 0.0,
        "pos": 0.0,
        "vc": 0.0,
        "raw_g": 0.0,
        "eff_g": 0.0,
        "temp_k": 300.0,
        "phase": "PAD_INSPECTION",
        "exploded": False,
        "reason": None,
        "morph_charge": 0.0,
        "morph_spread": 0.0,
    }], None

  dt = 0.5
  total_steps = 145
  history = []

  mass = chassis_info["base_mass"] * (armor_thickness / 70.0)
  max_thrust = (
      power_info["power_gw"]
      * (throttle_pct / 100.0)
      * chassis_info["warp_eff"]
      * 22.0
  )
  cur_temp = 295.0

  vc = 0.0
  progress = 0.0
  s_time = 0.0
  e_time = 0.0

  for step in range(total_steps):
    t = step * dt

    # 100% 成功する理想的な航行プロファイル
    if t < 10.0:
      phase = "LAUNCH_CATAPULT"
      morph_charge = min(1.0, t / 8.0)
      morph_spread = 0.0
      raw_g = (max_thrust * 0.25) / (mass * 9.8)
      vc = min(0.12, (t / 10.0) * 0.12)
      progress += (vc * 0.003) * dt
    elif progress < flip_ratio:
      phase = "WARP_CRUISE"
      morph_charge = 1.0
      morph_spread = min(1.0, (t - 10.0) / 4.0)
      target_vc = min(0.994, 0.12 + (warp_curvature / 10.0) * 0.86)
      vc = min(target_vc, vc + 0.09 * dt)
      raw_g = max_thrust / (mass * 9.8)
      progress += (vc * 0.016) * dt
    else:
      phase = "BRAKING_LOCK"
      morph_charge = max(0.1, 1.0 - (progress - flip_ratio) * 2.8)
      morph_spread = max(0.2, 1.0 - (progress - flip_ratio) * 2.2)
      raw_g = (max_thrust * 1.2) / (mass * 9.8)
      # ゲート位置(1.0)に向かって綺麗に0へ減速収束
      rem_dist = max(0.0001, 1.0 - progress)
      vc = max(0.005, min(vc, rem_dist * 2.8))
      progress = min(1.0, progress + (vc * 0.012) * dt)

    # 実効Gを人体・機体にとって安全かつダイナミックな範囲（0.8G〜4.5G）へクランプ
    eff_g = min(4.5, max(0.8, raw_g * 0.00008))

    # 相対論的時間遅延
    gamma = 1.0 / np.sqrt(max(0.001, 1.0 - (min(0.9995, vc) ** 2)))
    s_time += dt / gamma
    e_time += dt * gamma

    # 温度をビジュアル演出に最適な範囲（300K〜540K）へ制御
    target_temp = 300.0 + (vc * 240.0)
    cur_temp += (target_temp - cur_temp) * 0.15

    history.append({
        "t": float(t),
        "ship_time": float(s_time),
        "earth_time": float(e_time),
        "pos": float(min(1.0, progress)),
        "vc": float(vc),
        "raw_g": float(raw_g),
        "eff_g": float(eff_g),
        "temp_k": float(cur_temp),
        "phase": phase,
        "exploded": False,
        "reason": None,
        "morph_charge": float(morph_charge),
        "morph_spread": float(morph_spread),
    })

    # 到着完了判定
    if progress >= 0.998 and vc <= 0.04:
      for _ in range(16):
        history.append({
            "t": float(t + 1.0),
            "ship_time": float(s_time),
            "earth_time": float(e_time),
            "pos": 1.0,
            "vc": 0.0,
            "raw_g": 0.0,
            "eff_g": 1.0,
            "temp_k": 310.0,
            "phase": "ARRIVED",
            "exploded": False,
            "reason": None,
            "morph_charge": 0.0,
            "morph_spread": 0.0,
        })
      break

  return history, None


# =========================================================================
# 🚀 実行スイッチ & フロントエンド設定
# =========================================================================
st.markdown("---")
col_b1, col_b2 = st.columns([3, 1])
with col_b1:
  engage_clicked = st.button(
      "⚡ HYPER-DRIVE ENGAGE (安全ワープ跳躍点火)",
      use_container_width=True,
      type="primary",
  )
with col_b2:
  st.caption("※ プロトタイプ中はどの設定でも100%成功し、到着演出まで完走します。")

sim_records, sim_fail = run_simulation(preview_only=(not engage_clicked))

client_config = {
    "is_preview": not engage_clicked,
    "vessel_id": chassis_info["id"],
    "style": chassis_info["style"],
    "hull_color": int(hull_tint.lstrip("#"), 16),
    "circuit_color": int(circuit_color.lstrip("#"), 16),
    "core_glow": power_info["glow_hex"],
    "dest_type": waypoint_info["type"],
    "dest_color": waypoint_info["color_hex"],
    "radiator_count": radiator_blades,
    "window_density": window_density,
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
.pip-tag{position:absolute;top:6px;left:10px;background:rgba(15,23,42,0.9);padding:3px 8px;font-size:9px;font-weight:bold;color:#38bdf8;border-left:2px solid #38bdf8;}
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
    <div class="pip-tag">CAM 02: DESTINATION GATE OBSERVATORY</div>
</div>
<div class="hud-top">
    <div>SHIP: <strong id="h-ship" style="color:#38bdf8;">ARCH-LONGINUS</strong> | PHASE: <strong id="h-phase" style="color:#f59e0b;">INSPECTION</strong></div>
    <div>INTERNAL TEMP: <strong id="h-temp" style="color:#34d399;">295 K</strong> | SHIP: <strong id="h-stime">00:00.0</strong> | EARTH: <strong id="h-etime">00:00.0</strong></div>
</div>
<div class="banner banner-success" id="b-success">
    <div style="font-size:20px;font-weight:900;color:#6ee7b7;">🎉 CAPTURE COMPLETE 🎉</div>
    <div style="font-size:12px;margin-top:6px;color:#ecfdf5;">MAGNETIC ARREST RING LOCK SUCCESSFUL - ALL CREW SAFE</div>
</div>
<div class="hud-bottom">
    <div class="telem-box"><div class="telem-lbl">WARP VELOCITY</div><div class="telem-val"><span id="t-vc">0.00</span> <span style="font-size:10px;color:#94a3b8;">c (Light Speed)</span></div></div>
    <div class="telem-box"><div class="telem-lbl">MISSION PROGRESS</div><div class="telem-val"><span id="t-dist">0.0</span> <span style="font-size:10px;color:#94a3b8;">%</span></div></div>
    <div class="telem-box"><div class="telem-lbl">EFFECTIVE LOAD</div><div class="telem-val"><span id="t-g">1.0</span> <span style="font-size:10px;color:#94a3b8;">G (Safe Range)</span></div></div>
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
const rMain=new THREE.WebGLRenderer({canvas:cMain,antialias:true});rMain.setSize(wMain,hMain);rMain.toneMapping=THREE.ACESFilmicToneMapping;
const rPip=new THREE.WebGLRenderer({canvas:cPip,antialias:true});rPip.setSize(380,220);
const scene=new THREE.Scene();

const camMain=new THREE.PerspectiveCamera(35,wMain/hMain,0.5,100000);
const camPip=new THREE.PerspectiveCamera(25,380/220,1.0,100000);

const sunLight=new THREE.DirectionalLight(0xffffff,3.8);sunLight.position.set(600,1000,500);scene.add(sunLight);
scene.add(new THREE.AmbientLight(0x0f172a,1.8));

// --- Web Audio SF音響シンセシス ---
const AudioCtx=window.AudioContext||window.webkitAudioContext;let actx=null,oscWarp=null,gainWarp=null,oscSub=null,gainSub=null;
function initSFX(){
    if(!actx){
        actx=new AudioCtx();
        oscWarp=actx.createOscillator();oscWarp.type='sawtooth';
        const bp=actx.createBiquadFilter();bp.type='bandpass';bp.frequency.value=650;bp.Q.value=3.5;
        gainWarp=actx.createGain();gainWarp.gain.value=0.0001;
        oscWarp.connect(bp);bp.connect(gainWarp);gainWarp.connect(actx.destination);oscWarp.start(0);

        oscSub=actx.createOscillator();oscSub.type='sine';oscSub.frequency.value=35;
        gainSub=actx.createGain();gainSub.gain.value=0.0001;
        oscSub.connect(gainSub);gainSub.connect(actx.destination);oscSub.start(0);
    }
    if(actx.state==='suspended')actx.resume();
}
window.addEventListener('click',initSFX,{once:true});

// --- Canvasプロシージャルテクスチャ生成 ---
function createNeonGreebleTexture(lineColHex,winCount){
    const cvs=document.createElement('canvas');cvs.width=512;cvs.height=512;const ctx=cvs.getContext('2d');
    ctx.fillStyle='#000000';ctx.fillRect(0,0,512,512);
    ctx.strokeStyle='#'+lineColHex.toString(16).padStart(6,'0');ctx.lineWidth=2.5;ctx.shadowBlur=8;ctx.shadowColor=ctx.strokeStyle;
    for(let i=0;i<16;i++){
        ctx.beginPath();let x=Math.random()*512,y=Math.random()*512;ctx.moveTo(x,y);
        for(let j=0;j<4;j++){x+=((Math.random()-0.5)*120);y+=((Math.random()-0.5)*120);ctx.lineTo(x,y);}
        ctx.stroke();
    }
    ctx.fillStyle='#ffffff';ctx.shadowBlur=4;ctx.shadowColor='#ffffff';
    for(let k=0;k<winCount;k++){ctx.fillRect(Math.random()*512,Math.random()*512,1.8,1.8);}
    return new THREE.CanvasTexture(cvs);
}
const greebleTex=createNeonGreebleTexture(cfg.circuit_color,cfg.window_density);

// --- マテリアル構築 ---
const armorMat=new THREE.MeshStandardMaterial({color:cfg.hull_color,roughness:0.25,metalness:0.85,bumpMap:greebleTex,bumpScale:0.02});
const innerFrameMat=new THREE.MeshStandardMaterial({color:0x09090b,roughness:0.85,metalness:0.1});
const neonMat=new THREE.MeshBasicMaterial({map:greebleTex,color:cfg.circuit_color,transparent:true,opacity:0.95});
const coreMat=new THREE.MeshBasicMaterial({color:cfg.core_glow});
const radHeatMat=new THREE.MeshStandardMaterial({color:0x18181b,emissive:0xff2200,emissiveIntensity:0.0});

// --- 背景の星間空間 ---
const starGeo=new THREE.BufferGeometry(),starCount=5000;
const starPos=new Float32Array(starCount*3);
for(let i=0;i<starCount*3;i+=3){starPos[i]=(Math.random()-0.5)*14000;starPos[i+1]=(Math.random()-0.5)*14000;starPos[i+2]=(Math.random()-0.5)*20000;}
starGeo.setAttribute('position',new THREE.BufferAttribute(starPos,3));
const starPoints=new THREE.Points(starGeo,new THREE.PointsMaterial({color:0xffffff,size:2.8,transparent:true,opacity:0.8}));
scene.add(starPoints);

// --- 船体ビークルモデリング ---
const vesselGroup=new THREE.Group();scene.add(vesselGroup);
const floatingBinders=[],slidingArmor=[],radiatorPanels=[];
let gyroX=null,gyroY=null,gyroZ=null,blackHoleCore=null,shieldMesh=null;

// 1. 内部フレーム
const skeleton=new THREE.Mesh(new THREE.BoxGeometry(2.4,2.4,32),innerFrameMat);vesselGroup.add(skeleton);

// 2. ハニカムデフレクターシールド
const shieldGeo=new THREE.IcosahedronGeometry(22,2);
shieldMesh=new THREE.Mesh(shieldGeo,new THREE.MeshBasicMaterial({color:cfg.circuit_color,wireframe:true,transparent:true,opacity:0.0}));
shieldMesh.position.z=14;vesselGroup.add(shieldMesh);

if(cfg.vessel_id==='arch_longinus'){
    const bowFacet=new THREE.Mesh(new THREE.CylinderGeometry(0.5,4.8,28,4),armorMat);
    bowFacet.scale.set(1.9,0.38,1.0);bowFacet.rotation.x=Math.PI/2;bowFacet.position.z=6;vesselGroup.add(bowFacet);

    const circuitPlate=new THREE.Mesh(new THREE.PlaneGeometry(3.5,24),neonMat);
    circuitPlate.rotation.x=-Math.PI/2;circuitPlate.position.set(0,0.8,4);vesselGroup.add(circuitPlate);

    for(let side of [-1,1]){
        const sArmor=new THREE.Mesh(new THREE.BoxGeometry(1.6,1.4,22),armorMat);
        sArmor.position.set(side*3.2,0,-2);vesselGroup.add(sArmor);slidingArmor.push({mesh:sArmor,side:side});
    }
}else if(cfg.vessel_id==='aeon_obelisk'){
    gyroX=new THREE.Mesh(new THREE.TorusGeometry(6.5,0.3,16,48),coreMat);vesselGroup.add(gyroX);
    gyroY=new THREE.Mesh(new THREE.TorusGeometry(5.2,0.3,16,48),armorMat);vesselGroup.add(gyroY);
    gyroZ=new THREE.Mesh(new THREE.TorusGeometry(4.0,0.3,16,48),coreMat);vesselGroup.add(gyroZ);
    blackHoleCore=new THREE.Mesh(new THREE.SphereGeometry(2.8,32,32),new THREE.MeshBasicMaterial({color:0x000000}));
    vesselGroup.add(blackHoleCore);
    const accretionRing=new THREE.Mesh(new THREE.RingGeometry(3.2,5.5,32),new THREE.MeshBasicMaterial({color:cfg.core_glow,side:THREE.DoubleSide}));
    accretionRing.rotation.x=Math.PI/2.5;vesselGroup.add(accretionRing);

    for(let i=0;i<4;i++){
        const ang=(i/4)*Math.PI*2;
        const bMesh=new THREE.Mesh(new THREE.ConeGeometry(1.2,16,4),armorMat);
        bMesh.scale.set(1.5,1.0,0.4);bMesh.rotation.x=Math.PI/2;bMesh.rotation.z=ang;
        vesselGroup.add(bMesh);floatingBinders.push({mesh:bMesh,baseAng:ang,dist:11.0});
    }
}else if(cfg.vessel_id==='valkyrie_nova'){
    const needleNose=new THREE.Mesh(new THREE.ConeGeometry(1.2,32,6),armorMat);
    needleNose.scale.set(1.6,0.4,1.0);needleNose.rotation.x=Math.PI/2;needleNose.position.z=8;vesselGroup.add(needleNose);

    for(let i=0;i<4;i++){
        const ang=(i/4)*Math.PI*2+Math.PI/4;
        const wing=new THREE.Mesh(new THREE.BoxGeometry(9.0,0.25,4.5),armorMat);
        wing.position.set(Math.cos(ang)*4.5,Math.sin(ang)*4.5,-4);
        wing.rotation.z=ang;vesselGroup.add(wing);slidingArmor.push({mesh:wing,side:(i%2===0?1:-1)});
    }
}else{
    const cyberCart=new THREE.Mesh(new THREE.BoxGeometry(6.5,4.5,9.0),armorMat);vesselGroup.add(cyberCart);
    const soupCore=new THREE.Mesh(new THREE.SphereGeometry(2.2,16,16),new THREE.MeshBasicMaterial({color:0xffffff}));
    soupCore.position.set(0,-1.2,0);vesselGroup.add(soupCore);
    const signBoard=new THREE.Mesh(new THREE.PlaneGeometry(5.0,2.5),neonMat);
    signBoard.position.set(0,3.2,4.6);vesselGroup.add(signBoard);
}

// 排熱ラジエーターブレード
for(let r=0;r<cfg.radiator_count;r++){
    const ang=(r/cfg.radiator_count)*Math.PI*2;
    const rBlade=new THREE.Mesh(new THREE.BoxGeometry(0.18,4.5,12.0),radHeatMat);
    rBlade.position.set(Math.cos(ang)*2.8,Math.sin(ang)*2.8,-10);rBlade.rotation.z=ang;
    vesselGroup.add(rBlade);radiatorPanels.push(rBlade);
}

// --- 目的地の惑星＆ゲート ---
const destGroup=new THREE.Group();destGroup.position.set(0,0,15000);scene.add(destGroup);
const planet=new THREE.Mesh(new THREE.SphereGeometry(950,48,48),new THREE.MeshStandardMaterial({color:cfg.dest_color,roughness:0.8}));
destGroup.add(planet);
if(cfg.dest_type==='saturn'){
    const pRings=new THREE.Mesh(new THREE.RingGeometry(1200,2100,64),new THREE.MeshStandardMaterial({color:0xa8a29e,side:THREE.DoubleSide}));
    pRings.rotation.x=Math.PI/2.3;destGroup.add(pRings);
}
// 電磁減速アレストゲート
const catchGate=new THREE.Mesh(new THREE.TorusGeometry(36,2.2,16,48),new THREE.MeshStandardMaterial({color:0x38bdf8,metalness:0.95,roughness:0.15}));
catchGate.position.set(0,0,-1400);destGroup.add(catchGate);

// --- アニメーションループ ---
const tStart=performance.now();let isCompleted=false;

function animate(now){
    if(isCompleted)return;requestAnimationFrame(animate);
    const elapsed=(now-tStart)/1000.0;
    const simT=cfg.is_preview?0.0:elapsed*1.8;

    let idx=0;while(idx<data.length-1&&data[idx+1].t<=simT)idx++;
    const p=data[idx];

    // 1. 変形ギミック・スライドアニメーション
    slidingArmor.forEach(sa=>{
        sa.mesh.position.x=sa.side*(2.8+p.morph_spread*2.2);
    });
    // 2. 浮遊バインダーのフォーメーション展開
    floatingBinders.forEach(fb=>{
        const curDist=fb.dist+p.morph_spread*6.5;
        const curAng=fb.baseAng+(p.phase==="WARP_CRUISE"?now*0.002:0.0);
        fb.mesh.position.set(Math.cos(curAng)*curDist,Math.sin(curAng)*curDist,-6+p.morph_spread*3.0);
    });
    // 3. 3軸ジャイロ回転
    if(gyroX&&gyroY&&gyroZ){
        const spinSpeed=0.03+p.vc*0.25;
        gyroX.rotation.x+=spinSpeed;gyroY.rotation.y+=spinSpeed*1.3;gyroZ.rotation.z+=spinSpeed*0.7;
    }
    // 4. ハニカムシールドのフラッシュ発光
    if(shieldMesh){
        shieldMesh.rotation.z+=0.01;
        shieldMesh.material.opacity=(p.vc>0.3)?(0.25+Math.random()*0.15):0.0;
    }

    // 排熱赤熱
    const heatVal=Math.min(2.0,Math.max(0.0,(p.temp_k-320.0)/1200.0));
    radHeatMat.emissiveIntensity=heatVal;

    // ワープ進行・空間ストレッチ
    const zPos=p.pos*13600;
    vesselGroup.position.set(0,0,zPos);

    if(p.phase==="WARP_CRUISE"){
        vesselGroup.scale.set(1.0,1.0,1.0+p.vc*4.0);
        camMain.fov=THREE.MathUtils.lerp(camMain.fov,80.0,0.1);
        if(oscWarp&&actx){
            oscWarp.frequency.setTargetAtTime(500+p.vc*1400,actx.currentTime,0.1);
            gainWarp.gain.setTargetAtTime(0.75,actx.currentTime,0.1);
            gainSub.gain.setTargetAtTime(0.85,actx.currentTime,0.1);
        }
    }else{
        vesselGroup.scale.set(1.0,1.0,1.0);
        camMain.fov=THREE.MathUtils.lerp(camMain.fov,35.0,0.08);
        if(gainWarp&&actx){
            gainWarp.gain.setTargetAtTime(0.0001,actx.currentTime,0.2);
            gainSub.gain.setTargetAtTime(0.0001,actx.currentTime,0.2);
        }
    }
    camMain.updateProjectionMatrix();

    if(p.phase==="ARRIVED"&&document.getElementById('b-success').style.display!=='block'){
        document.getElementById('b-success').style.display='block';
    }

    // カメラワーク（CAM 01: 追従）
    camMain.position.set(0,18+p.vc*8,zPos-60-p.vc*28);
    camMain.lookAt(0,0,zPos+30);

    // カメラワーク（CAM 02: 目的地の観測所）
    camPip.position.set(0,45,13400);
    camPip.lookAt(vesselGroup.position);
    rPip.render(scene,camPip);

    // メイン描画
    rMain.render(scene,camMain);

    // テレメトリHUD
    document.getElementById('h-ship').innerText=cfg.vessel_id.toUpperCase();
    document.getElementById('h-phase').innerText=p.phase;
    document.getElementById('h-temp').innerText=`${Math.round(p.temp_k)} K`;
    document.getElementById('h-stime').innerText=`T+ ${p.ship_time.toFixed(1)}s`;
    document.getElementById('h-etime').innerText=`T+ ${p.earth_time.toFixed(1)}s`;
    document.getElementById('t-vc').innerText=p.vc.toFixed(3);
    document.getElementById('t-dist').innerText=(p.pos*100.0).toFixed(1);
    document.getElementById('t-g').innerText=p.eff_g.toFixed(1);
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

if engage_clicked:
  st.markdown("---")
  st.success("🎉 **プロトタイプ航行完了**: 全機体システムおよび減速ゲートアレスト機構の正常動作を確認しました。")
