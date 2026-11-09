import json
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hyper-Drive Architect: Chrono & Cosmos",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("🛸 Hyper-Drive Architect: Chrono & Cosmos")
st.caption(
    "※ 恒星間航行シミュレーター：架空ビークル造形・可変変形・相対論的時間遅延・SF版RUD完全再現版"
)

# =========================================================================
# 🌌 データベース：シャーシ・動力炉・目的地・マテリアル
# =========================================================================
CHASSIS_TYPES = {
    "アルクビエレ・デュアルリング艦 (Warp Ring Cruiser)": {
        "id": "ring_cruiser",
        "base_mass": 420.0,
        "warp_eff": 1.45,
        "heat_cap": 8500.0,
        "desc": "二重反転超伝導リングによる空間歪曲航行。安定したワープバブルを形成する正統派巡洋艦。",
    },
    "ソーラー・ヴァルキリー (Laser-Sail Clipper)": {
        "id": "solar_valkyrie",
        "base_mass": 180.0,
        "warp_eff": 1.15,
        "heat_cap": 6200.0,
        "desc": "6枚の結晶光帆を展開。母星側レーザーと太陽風を受け、優美に加速する長距離高速帆船。",
    },
    "重力制御モノリス「オベリスク」 (Zero-Point Monolith)": {
        "id": "monolith",
        "base_mass": 980.0,
        "warp_eff": 1.85,
        "heat_cap": 14000.0,
        "desc": "推進器を持たない鏡面八面体。上下に船体が割れ、内部の特異点コアから重力場を直接生み出す。",
    },
    "恒星間レールガン突撃艇「ロンギヌス」 (Mass-Driver Striker)": {
        "id": "longinus",
        "base_mass": 320.0,
        "warp_eff": 1.05,
        "heat_cap": 9500.0,
        "desc": "全長の8割が電磁加速砲身。装甲が横にスライド展開し内部ラジエーターを露出させて超加速する強襲艇。",
    },
    "次元潜航トリマラン「リヴァイアサン」 (Sub-Space Trimaran)": {
        "id": "trimaran",
        "base_mass": 650.0,
        "warp_eff": 1.60,
        "heat_cap": 11000.0,
        "desc": "重厚な三胴ハル。超加速モード突入時に左右の大型ワープ・ナセルがX字状に可変展開する。",
    },
    "【ジョーク】超時空・屋台ラーメン『銀河軒』 (Tachyon Noodle Stand)": {
        "id": "ramen_cart",
        "base_mass": 12.0,
        "warp_eff": 2.20,
        "heat_cap": 3500.0,
        "desc": "赤提灯と暖簾の裏にタキオン濃縮炉を積載。プラズマ豚骨スープの反作用で時空を突き破る謎の移動屋台。",
    },
}

POWER_CORES = {
    "零点エネルギー抽出炉 (Zero-Point ZPE Tap)": {
        "power_gw": 85000.0,
        "waste_heat_ratio": 0.08,
        "stability": 0.98,
        "glow_hex": 0x38BDF8,
    },
    "反物質対消滅コア (Antimatter Beam Core)": {
        "power_gw": 140000.0,
        "waste_heat_ratio": 0.22,
        "stability": 0.94,
        "glow_hex": 0xF43F5E,
    },
    "人工マイクロ・ブラックホール (Kerr Singularity)": {
        "power_gw": 290000.0,
        "waste_heat_ratio": 0.15,
        "stability": 0.88,
        "glow_hex": 0xA855F7,
    },
    "【ジョーク】回転する猫とバタートースト永久機関": {
        "power_gw": 999999.0,
        "waste_heat_ratio": 0.02,
        "stability": 0.99,
        "glow_hex": 0xFBBF24,
    },
}

DESTINATIONS = {
    "火星 オリンポス・テラフォーミング軌道都市": {
        "dist_au": 0.52,
        "dist_ly": 0.000008,
        "color_hex": 0xC2410C,
        "type": "mars",
        "desc": "赤く染まる地表とテラフォーミングドーム群。第1マスキャッチャーリングが待機。",
    },
    "木星 大赤斑上空・浮遊採掘ステーション": {
        "dist_au": 4.20,
        "dist_ly": 0.000066,
        "color_hex": 0xD97706,
        "type": "jupiter",
        "desc": "荒れ狂う大赤斑の真上。ガス採取用巨大アンカーリングへ突入。",
    },
    "土星リング 氷冠採掘ゲート「クロノス」": {
        "dist_au": 9.58,
        "dist_ly": 0.000151,
        "color_hex": 0xE2E8F0,
        "type": "saturn",
        "desc": "無数の氷塊が回る巨大環の隙間に鎮座する超大型減速ゲート。",
    },
    "ブラックホール「ガルガンチュア」事象の地平面スレスレ観光": {
        "dist_au": 18000.0,
        "dist_ly": 0.285,
        "color_hex": 0x1E1B4B,
        "type": "blackhole",
        "desc": "光さえ脱出不可能な極限重力場。時空の歪みをかすめて周回軌道へ入る決死のルート。",
    },
}

HULL_MATERIALS = {
    "自己修復液体金属 (Nanite Silver)": {
        "color": 0xF1F5F9,
        "roughness": 0.05,
        "metalness": 0.98,
        "structural_limit_g": 6500.0,
    },
    "ダマスカス量子合金 (Quantum Composite)": {
        "color": 0x1E293B,
        "roughness": 0.35,
        "metalness": 0.85,
        "structural_limit_g": 4800.0,
    },
    "縮退物質ブラックアーマー (Degenerate Armor)": {
        "color": 0x050505,
        "roughness": 0.85,
        "metalness": 0.20,
        "structural_limit_g": 9200.0,
    },
    "屋台用 天然ヒノキ木材＆赤提灯ビニール": {
        "color": 0xD97706,
        "roughness": 0.90,
        "metalness": 0.05,
        "structural_limit_g": 1200.0,
    },
}

# =========================================================================
# ⚙️ Streamlit UI タブ設計
# =========================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🛸 船体シャーシ & 外装",
    "⚡ 動力炉 & ワープドライブ",
    "🛡️ 慣性ダンパー & シールド",
    "🔥 展開放熱翼 & 冷却系",
    "🎯 目的地 & 航法ガイダンス",
])

with tab1:
  c1, c2 = st.columns(2)
  with c1:
    chassis_choice = st.selectbox(
        "ベースビークル (シャーシ)", list(CHASSIS_TYPES.keys())
    )
    material_choice = st.selectbox(
        "船体外装マテリアル", list(HULL_MATERIALS.keys())
    )
  with c2:
    st.info(f"**艦種解説:** {CHASSIS_TYPES[chassis_choice]['desc']}")
    hull_scale = st.slider("機体スケール倍率", 0.5, 2.5, 1.0, step=0.1)

with tab2:
  c1, c2 = st.columns(2)
  with c1:
    core_choice = st.selectbox("メイン動力炉", list(POWER_CORES.keys()))
    warp_factor = st.slider("ワープ曲率倍率 (Warp Factor)", 1.0, 9.9, 7.5, step=0.1)
  with c2:
    throttle_limit = st.slider("ドライブ出力リミッター (%)", 50, 150, 100, step=5)
    st.caption("※ 100%超過はコア不安定化と廃熱急上昇のリスクを伴います。")

with tab3:
  c1, c2 = st.columns(2)
  with c1:
    damper_efficiency = st.slider(
        "慣性ダンパー相殺率 (%)",
        99.000,
        99.999,
        99.985,
        step=0.001,
        format="%.3f%%",
    )
    st.caption("※ 0.01%の相殺不足でも乗員・船体に数十〜数百Gの致命的負荷がかかります。")
  with c2:
    deflector_power = st.slider(
        "デフレクターシールド出力 (GW)", 100, 2500, 1200, step=50
    )
    deflector_angle = st.slider("シールド迎角 (deg)", 10, 80, 45, step=5)

with tab4:
  c1, c2 = st.columns(2)
  with c1:
    radiator_wings = st.slider("展開式放熱フィン翼数", 2, 8, 4, step=2)
    radiator_area = st.slider(
        "放熱翼 展開面積 (m²)", 200.0, 5000.0, 1800.0, step=100.0
    )
  with c2:
    coolant_flow = st.slider(
        "超流動ヘリウム冷却材 循環レート (L/s)", 50, 800, 350, step=25
    )
    st.caption("※ 廃熱が許容量を超えると船体が自らの熱で融解メルトダウンします。")

with tab5:
  c1, c2 = st.columns(2)
  with c1:
    dest_choice = st.selectbox("航行目的地セレクター", list(DESTINATIONS.keys()))
    st.caption(f"**目的宙域環境:** {DESTINATIONS[dest_choice]['desc']}")
  with c2:
    flip_burn_ratio = st.slider(
        "反転減速（フリップ＆バーン）開始ポイント",
        0.50,
        0.95,
        0.75,
        step=0.01,
    )
    st.caption("※ 減速開始が遅すぎると目的地の惑星やゲートを光速で突き抜けます。")

# =========================================================================
# 💥 物理・時空シミュレーション計算
# =========================================================================
chosen_chassis = CHASSIS_TYPES[chassis_choice]
chosen_core = POWER_CORES[core_choice]
chosen_dest = DESTINATIONS[dest_choice]
chosen_mat = HULL_MATERIALS[material_choice]


def run_space_sim(preview_only=False):
  if preview_only:
    return [{
        "t": 0.0,
        "ship_time": 0.0,
        "earth_time": 0.0,
        "pos_ratio": 0.0,
        "v_c": 0.0,
        "raw_g": 0.0,
        "effective_g": 0.0,
        "heat_k": 300.0,
        "phase": "PAD_INSPECTION",
        "exploded": False,
        "rud_reason": None,
        "transform_morph": 0.0,
    }], None

  history = []
  fail_reason = None
  dt = 0.5
  total_steps = 140

  ship_mass = chosen_chassis["base_mass"] * hull_scale
  max_thrust_kn = (
      chosen_core["power_gw"]
      * (throttle_limit / 100.0)
      * chosen_chassis["warp_eff"]
      * 18.0
  )
  heat_current = 295.0

  uncompensated_ratio = (100.0 - damper_efficiency) / 100.0
  heat_dissipation_rate = (
      (radiator_area * 0.45 + coolant_flow * 2.2)
      * 0.08
      / (ship_mass * 0.05)
  )

  v_c = 0.0
  dist_progress = 0.0
  ship_elapsed_s = 0.0
  earth_elapsed_s = 0.0

  for step in range(total_steps):
    t = step * dt

    # フェーズ定義
    # 0~15: カタパルト射出加速
    # 15~85: 超時空ワープ巡航
    # 85~130: 反転減速＆リング突入
    # 130~: 到着キャッチ
    if t < 8.0:
      phase = "CATAPULT_LAUNCH"
      transform_morph = min(1.0, t / 8.0)
      raw_acc_g = (max_thrust_kn * 0.25) / (ship_mass * 9.8)
      v_c = min(0.15, (t / 8.0) * 0.15)
      dist_progress += (v_c * 0.002) * dt
    elif dist_progress < flip_burn_ratio:
      phase = "WARP_CRUISE"
      transform_morph = 1.0
      target_vc = min(0.992, 0.15 + (warp_factor / 10.0) * 0.84)
      v_c = min(target_vc, v_c + 0.08 * dt)
      raw_acc_g = (max_thrust_kn) / (ship_mass * 9.8)
      dist_progress += (v_c * 0.016) * dt
    else:
      phase = "DECEL_APPROACH"
      transform_morph = max(0.2, 1.0 - (dist_progress - flip_burn_ratio) * 2.5)
      raw_acc_g = (max_thrust_kn * 1.3) / (ship_mass * 9.8)
      v_c = max(0.005, v_c - 0.095 * dt)
      dist_progress += (v_c * 0.012) * dt

    effective_g = raw_acc_g * uncompensated_ratio

    # 特殊相対性理論：ローレンツ因子 gamma
    gamma = 1.0 / np.sqrt(max(0.001, 1.0 - (min(0.999, v_c) ** 2)))
    dt_ship = dt / gamma
    dt_earth = dt * gamma
    ship_elapsed_s += dt_ship
    earth_elapsed_s += dt_earth

    # 熱収支計算
    heat_in = (
        (chosen_core["power_gw"] * (throttle_limit / 100.0))
        * chosen_core["waste_heat_ratio"]
        * (0.45 + (v_c**1.5) * 1.2)
    ) / (ship_mass * 0.12)
    heat_current = max(
        290.0, heat_current + (heat_in - heat_dissipation_rate) * dt
    )

    # 💥 SF版 RUD（事故判定）
    rud = False

    # 1. 慣性ダンパー落ちアコーディオン圧壊
    if effective_g > chosen_mat["structural_limit_g"]:
      fail_reason = (
          f"【重力制御崩壊・アコーディオン圧壊】実効慣性G ({effective_g:.1f} G) が"
          f" {material_choice} の限界 ({chosen_mat['structural_limit_g']:.0f} G)"
          " を突破。船体が一瞬でペシャンコに潰れました。"
      )
      rud = True
    # 2. 廃熱パンク・メルトダウン
    elif heat_current > chosen_chassis["heat_cap"]:
      fail_reason = (
          f"【放熱限界・熱核メルトダウン】船内温度 ({heat_current:.0f} K) が"
          f" 許容限界 ({chosen_chassis['heat_cap']:.0f} K)"
          " を超過。ラジエーター能力不足により船体が蒸発しました。"
      )
      rud = True
    # 3. 宇宙塵衝突（デフレクター破壊）
    elif (
        v_c > 0.4
        and (deflector_power * np.sin(np.radians(deflector_angle)))
        < (v_c * 1800.0)
    ):
      fail_reason = (
          f"【宇宙塵・超音速カタストロフィ】光速の {v_c*100:.1f}% で微小デブリ群と衝突。"
          f" デフレクター出力 ({deflector_power} GW) が突破され船体が消滅しました。"
      )
      rud = True
    # 4. 特異点コア・ブラックホール暴走
    elif (
        core_choice == "人工マイクロ・ブラックホール (Kerr Singularity)"
        and throttle_limit > 125
        and t > 18.0
    ):
      fail_reason = (
          "【事象の地平面・自壊呑み込み】特異点磁気トラップが臨界突破。"
          " 宇宙船が自身の人工ブラックホールに内側から吸い込まれました。"
      )
      rud = True
    # 5. 反転遅れ・惑星直撃貫通
    elif dist_progress >= 1.05 and v_c > 0.15:
      fail_reason = (
          f"【オーバーシュート・惑星超光速激突】フリップ＆バーン開始比率"
          f" ({flip_burn_ratio:.2f})"
          " が遅すぎ、ブレーキが間に合わず目的地の地表に直撃しました。"
      )
      rud = True

    history.append({
        "t": float(t),
        "ship_time": float(ship_elapsed_s),
        "earth_time": float(earth_elapsed_s),
        "pos_ratio": float(min(1.0, dist_progress)),
        "v_c": float(v_c),
        "raw_g": float(raw_acc_g),
        "effective_g": float(effective_g),
        "heat_k": float(heat_current),
        "phase": "RUD" if rud else phase,
        "exploded": rud,
        "rud_reason": fail_reason,
        "transform_morph": float(transform_morph),
    })

    if rud:
      break
    if dist_progress >= 1.0 and v_c <= 0.05:
      # 到着成功
      for _ in range(15):
        history.append({
            "t": float(t + 1.0),
            "ship_time": float(ship_elapsed_s),
            "earth_time": float(earth_elapsed_s),
            "pos_ratio": 1.0,
            "v_c": 0.0,
            "raw_g": 0.0,
            "effective_g": 0.0,
            "heat_k": float(heat_current * 0.95),
            "phase": "ARRIVED",
            "exploded": False,
            "rud_reason": None,
            "transform_morph": 0.0,
        })
      break

  return history, fail_reason


# =========================================================================
# 🚀 実行トリガー & JSONペイロード生成
# =========================================================================
st.markdown("---")
c_run1, c_run2 = st.columns([3, 1])
with c_run1:
  warp_engage = st.button(
      "⚡ HYPER-DRIVE ENGAGE (ワープ跳躍シーケンス点火)",
      use_container_width=True,
      type="primary",
  )
with c_run2:
  st.caption("※ パラメータ変更時はプレビューモードで艦の3D形状を確認可能。")

sim_history, sim_error = run_space_sim(preview_only=(not warp_engage))

frontend_cfg = {
    "is_preview": not warp_engage,
    "chassis_id": chosen_chassis["id"],
    "hull_color": chosen_mat["color"],
    "roughness": chosen_mat["roughness"],
    "metalness": chosen_mat["metalness"],
    "core_glow": chosen_core["glow_hex"],
    "dest_type": chosen_dest["type"],
    "dest_color": chosen_dest["color_hex"],
    "radiator_wings": radiator_wings,
    "hull_scale": hull_scale,
}

sim_json = json.dumps(sim_history)
cfg_json = json.dumps(frontend_cfg)
fail_msg_safe = (sim_error or "").replace('"', '\\"').replace("'", "\\'")

# =========================================================================
# 📺 Three.js + Web Audio 一体型 HTML 描画テンプレート
# =========================================================================
html_code = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{box-sizing:border-box;}body,html{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:#000208;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#fff;user-select:none;}
#canvas-main{width:100%;height:100%;display:block;position:absolute;top:0;left:0;z-index:1;}
.hud-top{position:absolute;top:0;left:0;width:100%;min-height:44px;background:linear-gradient(180deg,rgba(5,10,25,0.96) 0%,rgba(5,10,25,0.85) 100%);border-bottom:1px solid rgba(56,189,248,0.3);display:flex;align-items:center;justify-content:space-between;padding:4px 16px;z-index:20;font-family:monospace;font-size:11px;}
.pip-box{position:absolute;top:54px;right:12px;width:380px;height:220px;border:2px solid #38bdf8;border-radius:6px;background:#020617;overflow:hidden;z-index:60;box-shadow:0 10px 40px rgba(0,0,0,0.95);}
#canvas-pip{width:100%;height:100%;display:block;}
.pip-label{position:absolute;top:6px;left:10px;background:rgba(15,23,42,0.9);padding:2px 8px;font-size:9px;font-weight:bold;color:#38bdf8;border-left:2px solid #38bdf8;}
.hud-bottom{position:absolute;bottom:0;left:0;width:100%;height:75px;background:rgba(2,6,23,0.95);border-top:1px solid rgba(255,255,255,0.15);padding:8px 24px;display:flex;align-items:center;justify-content:space-between;z-index:20;}
.telem-item{display:flex;flex-direction:column;}
.telem-lbl{font-size:9px;color:#94a3b8;letter-spacing:1px;}
.telem-val{font-size:clamp(14px,1.8vw,18px);font-weight:900;font-family:monospace;color:#f8fafc;}
.banner{display:none;position:absolute;top:150px;left:50%;transform:translateX(-50%);padding:22px 36px;border-radius:8px;z-index:80;text-align:center;}
.banner-rud{background:rgba(153,27,27,0.95);border:2px solid #ef4444;box-shadow:0 0 60px rgba(239,68,68,0.8);}
.banner-success{background:rgba(6,78,59,0.95);border:2px solid #10b981;box-shadow:0 0 60px rgba(16,185,129,0.8);}
</style></head>
<body>
<canvas id="canvas-main"></canvas>
<div class="pip-box" id="pip-container">
    <canvas id="canvas-pip"></canvas>
    <div class="pip-label" id="pip-status">CAM 02: DESTINATION GATE OBSERVATORY</div>
</div>
<div class="hud-top">
    <div>SHIP: <strong id="h-ship" style="color:#38bdf8;">HYPER-VESSEL</strong> | PHASE: <strong id="h-phase" style="color:#f59e0b;">INSPECTION</strong></div>
    <div>TEMP: <strong id="h-temp" style="color:#ef4444;">300 K</strong> | SHIP TIME: <strong id="h-stime">00:00.0</strong> | EARTH TIME: <strong id="h-etime">00:00.0</strong></div>
</div>
<div class="banner banner-rud" id="b-rud">
    <div style="font-size:18px;font-weight:900;color:#fff;">🚨 SPACETIME DISASTER / RUD OCCURRED 🚨</div>
    <div id="rud-text" style="font-size:12px;margin-top:8px;color:#fecaca;"></div>
</div>
<div class="banner banner-success" id="b-success">
    <div style="font-size:20px;font-weight:900;color:#6ee7b7;">🎉 DESTINATION REACHED & CAPTURED 🎉</div>
    <div style="font-size:12px;margin-top:6px;color:#ecfdf5;">GATE MAGNETIC DECELERATION LOCK SUCCESSFUL</div>
</div>
<div class="hud-bottom">
    <div class="telem-item"><div class="telem-lbl">WARP VELOCITY</div><div class="telem-val"><span id="t-vc">0.00</span> <span style="font-size:10px;color:#94a3b8;">c (Light Speed)</span></div></div>
    <div class="telem-item"><div class="telem-lbl">PROGRESS TO DESTINATION</div><div class="telem-val"><span id="t-dist">0.0</span> <span style="font-size:10px;color:#94a3b8;">%</span></div></div>
    <div class="telem-item"><div class="telem-lbl">INERTIAL ACCELERATION</div><div class="telem-val"><span id="t-g">0.0</span> <span style="font-size:10px;color:#94a3b8;">G (Compensated)</span></div></div>
    <div class="telem-item"><div class="telem-lbl">TIME DILATION FACTOR (γ)</div><div class="telem-val"><span id="t-gamma">1.00</span> <span style="font-size:10px;color:#94a3b8;">x</span></div></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
window.addEventListener('DOMContentLoaded',()=>{
try{
const data=__SIM_DATA__;const cfg=__SIM_CFG__;const failReason="__FAIL_MSG__";
const cMain=document.getElementById('canvas-main'),cPip=document.getElementById('canvas-pip');
const wMain=window.innerWidth,hMain=window.innerHeight;

// --- Three.js レンダラー構築 ---
const rMain=new THREE.WebGLRenderer({canvas:cMain,antialias:true});rMain.setSize(wMain,hMain);rMain.toneMapping=THREE.ACESFilmicToneMapping;
const rPip=new THREE.WebGLRenderer({canvas:cPip,antialias:true});rPip.setSize(380,220);
const scene=new THREE.Scene();

const camMain=new THREE.PerspectiveCamera(35,wMain/hMain,0.5,100000);
const camPip=new THREE.PerspectiveCamera(25,380/220,1.0,100000);

const lightSun=new THREE.DirectionalLight(0xffffff,3.5);lightSun.position.set(500,800,400);scene.add(lightSun);
scene.add(new THREE.AmbientLight(0x1e293b,1.5));
const coreGlowLight=new THREE.PointLight(cfg.core_glow,0.0,300);scene.add(coreGlowLight);

// --- Web Audio SF音響シンセシス ---
const AudioCtx=window.AudioContext||window.webkitAudioContext;let actx=null,warpOsc=null,subBass=null;
function initAudio(){
    if(!actx){
        actx=new AudioCtx();
        warpOsc=actx.createOscillator();warpOsc.type='sawtooth';
        const wFilter=actx.createBiquadFilter();wFilter.type='bandpass';wFilter.frequency.value=800;wFilter.Q.value=4.0;
        const wGain=actx.createGain();wGain.gain.value=0.0001;
        warpOsc.connect(wFilter);wFilter.connect(wGain);wGain.connect(actx.destination);warpOsc.start(0);

        const subOsc=actx.createOscillator();subOsc.type='sine';subOsc.frequency.value=38;
        subBass=actx.createGain();subBass.gain.value=0.0001;
        subOsc.connect(subBass);subBass.connect(actx.destination);subOsc.start(0);
    }
    if(actx.state==='suspended')actx.resume();
}
window.addEventListener('click',initAudio,{once:true});

// --- 星間空間・星々（ワープストレッチ表現） ---
const starGeo=new THREE.BufferGeometry(),starCount=4500;
const starPos=new Float32Array(starCount*3);
for(let i=0;i<starCount*3;i+=3){starPos[i]=(Math.random()-0.5)*12000;starPos[i+1]=(Math.random()-0.5)*12000;starPos[i+2]=(Math.random()-0.5)*18000;}
starGeo.setAttribute('position',new THREE.BufferAttribute(starPos,3));
const starMat=new THREE.PointsMaterial({color:0xffffff,size:2.5,transparent:true,opacity:0.85});
const starField=new THREE.Points(starGeo,starMat);scene.add(starField);

// --- 船体ビークルモデリング（基本図形によるプロシージャル構築） ---
const shipGroup=new THREE.Group();scene.add(shipGroup);
const hullMat=new THREE.MeshStandardMaterial({color:cfg.hull_color,roughness:cfg.roughness,metalness:cfg.metalness});
const coreMat=new THREE.MeshBasicMaterial({color:cfg.core_glow});
const radiatorMat=new THREE.MeshStandardMaterial({color:0x111111,emissive:0xff2200,emissiveIntensity:0.0});

let ring1=null,ring2=null,wings=[],trimaranNacelles=[],ramenBowl=null;

if(cfg.chassis_id==='ring_cruiser'){
    // ① ワープリング艦
    const hull=new THREE.Mesh(new THREE.ConeGeometry(3.5,24,16),hullMat);hull.rotation.x=Math.PI/2;shipGroup.add(hull);
    ring1=new THREE.Mesh(new THREE.TorusGeometry(8.5,0.45,16,64),coreMat);ring1.position.z=-2;shipGroup.add(ring1);
    ring2=new THREE.Mesh(new THREE.TorusGeometry(9.5,0.35,16,64),hullMat);ring2.position.z=-4;shipGroup.add(ring2);
}else if(cfg.chassis_id==='solar_valkyrie'){
    // ② ソーラー・ヴァルキリー
    const body=new THREE.Mesh(new THREE.CylinderGeometry(0.8,1.6,22,16),hullMat);body.rotation.x=Math.PI/2;shipGroup.add(body);
    for(let i=0;i<6;i++){
        const sail=new THREE.Mesh(new THREE.PlaneGeometry(16,32),new THREE.MeshStandardMaterial({color:0xfde047,metalness:0.95,roughness:0.1,side:THREE.DoubleSide}));
        sail.position.set(Math.cos(i/6*Math.PI*2)*3.0,Math.sin(i/6*Math.PI*2)*3.0,-6);
        sail.rotation.z=(i/6)*Math.PI*2;shipGroup.add(sail);wings.push(sail);
    }
}else if(cfg.chassis_id==='monolith'){
    // ③ 重力制御モノリス
    const topPyramid=new THREE.Mesh(new THREE.ConeGeometry(5,14,4),hullMat);topPyramid.position.z=7;topPyramid.rotation.x=Math.PI/2;shipGroup.add(topPyramid);
    const botPyramid=new THREE.Mesh(new THREE.ConeGeometry(5,14,4),hullMat);botPyramid.position.z=-7;botPyramid.rotation.x=-Math.PI/2;shipGroup.add(botPyramid);
    const centerCore=new THREE.Mesh(new THREE.SphereGeometry(3.2,32,32),new THREE.MeshBasicMaterial({color:0x000000}));shipGroup.add(centerCore);
}else if(cfg.chassis_id==='longinus'){
    // ④ ロンギヌス突撃艇
    const barrel=new THREE.Mesh(new THREE.CylinderGeometry(0.9,1.4,36,8),hullMat);barrel.rotation.x=Math.PI/2;shipGroup.add(barrel);
    for(let side of [-1,1]){
        const armor=new THREE.Mesh(new THREE.BoxGeometry(1.2,2.5,24),radiatorMat);armor.position.set(side*2.2,0,-4);shipGroup.add(armor);wings.push(armor);
    }
}else if(cfg.chassis_id==='trimaran'){
    // ⑤ トリマラン
    const centerHull=new THREE.Mesh(new THREE.BoxGeometry(4.5,2.5,22),hullMat);shipGroup.add(centerHull);
    for(let side of [-1,1]){
        const nacelle=new THREE.Mesh(new THREE.CylinderGeometry(1.4,1.8,18,12),hullMat);nacelle.rotation.x=Math.PI/2;
        nacelle.position.set(side*7.5,0,-2);shipGroup.add(nacelle);trimaranNacelles.push(nacelle);
    }
}else if(cfg.chassis_id==='ramen_cart'){
    // ⑥ 屋台ラーメン
    ramenBowl=new THREE.Mesh(new THREE.CylinderGeometry(3.5,2.0,3.2,16),new THREE.MeshStandardMaterial({color:0xd97706,roughness:0.8}));ramenBowl.position.y=1.5;shipGroup.add(ramenBowl);
    const noren=new THREE.Mesh(new THREE.BoxGeometry(5.2,2.8,4.2),hullMat);noren.position.y=4.5;shipGroup.add(noren);
    const lantern=new THREE.Mesh(new THREE.SphereGeometry(1.2,12,12),new THREE.MeshBasicMaterial({color:0xef4444}));lantern.position.set(2.8,4.0,2.2);shipGroup.add(lantern);
}

// 展開放熱翼
const radPanels=[];
for(let r=0;r<cfg.radiator_wings;r++){
    const ang=(r/cfg.radiator_wings)*Math.PI*2;
    const radP=new THREE.Mesh(new THREE.BoxGeometry(0.12,4.8,10.0),radiatorMat);
    radP.position.set(Math.cos(ang)*2.6,Math.sin(ang)*2.6,-8);radP.rotation.z=ang;shipGroup.add(radP);radPanels.push(radP);
}

// --- 目的地の惑星＆ゲート ---
const destGroup=new THREE.Group();destGroup.position.set(0,0,14000);scene.add(destGroup);
const planetMesh=new THREE.Mesh(new THREE.SphereGeometry(850,48,48),new THREE.MeshStandardMaterial({color:cfg.dest_color,roughness:0.8}));
destGroup.add(planetMesh);
if(cfg.dest_type==='saturn'){
    const ringMesh=new THREE.Mesh(new THREE.RingGeometry(1100,1800,64),new THREE.MeshStandardMaterial({color:0xa8a29e,side:THREE.DoubleSide}));
    ringMesh.rotation.x=Math.PI/2.4;destGroup.add(ringMesh);
}
// 減速キャッチャー・ゲート
const gateRing=new THREE.Mesh(new THREE.TorusGeometry(32,1.8,16,48),new THREE.MeshStandardMaterial({color:0x38bdf8,metalness:0.9,roughness:0.2}));
gateRing.position.set(0,0,-1200);destGroup.add(gateRing);

// --- アニメーションループ ---
const tStart=performance.now();
let isEnded=false;

function renderFrame(now){
    if(isEnded)return;requestAnimationFrame(renderFrame);
    const elapsed=(now-tStart)/1000.0;
    const curSimT=cfg.is_preview?0.0:elapsed*1.8;

    let idx=0;while(idx<data.length-1&&data[idx+1].t<=curSimT)idx++;
    const p=data[idx];

    // 機体変形・自転アクション
    if(ring1&&ring2){ring1.rotation.z+=0.04+p.v_c*0.25;ring2.rotation.z-=0.03+p.v_c*0.25;}
    if(cfg.chassis_id==='solar_valkyrie'){wings.forEach((w,i)=>{w.scale.set(p.transform_morph,p.transform_morph,1);});}
    if(cfg.chassis_id==='longinus'){wings.forEach((w,i)=>{w.position.x=(i===0?-1:1)*(2.2+p.transform_morph*1.5);});}
    if(cfg.chassis_id==='trimaran'){trimaranNacelles.forEach((n,i)=>{n.rotation.z=(i===0?1:-1)*p.transform_morph*0.35;});}
    if(ramenBowl){ramenBowl.rotation.y+=0.05;}

    // 放熱翼の赤熱
    const heatRatio=Math.min(2.5,Math.max(0.0,(p.heat_k-350.0)/1800.0));
    radiatorMat.emissiveIntensity=heatRatio;

    // ワープストレッチと機体進行
    const currentZ=p.pos_ratio*12800;
    shipGroup.position.set(0,0,currentZ);

    if(p.phase==="WARP_CRUISE"){
        shipGroup.scale.set(1.0,1.0,1.0+p.v_c*3.5);
        camMain.fov=THREE.MathUtils.lerp(camMain.fov,75.0,0.1);
        if(warpOsc&&actx){warpOsc.frequency.setTargetAtTime(400+p.v_c*1200,actx.currentTime,0.1);subBass.gain.setTargetAtTime(0.85,actx.currentTime,0.1);}
    }else{
        shipGroup.scale.set(1.0,1.0,1.0);
        camMain.fov=THREE.MathUtils.lerp(camMain.fov,35.0,0.08);
        if(subBass&&actx){subBass.gain.setTargetAtTime(0.0001,actx.currentTime,0.2);}
    }
    camMain.updateProjectionMatrix();

    // 💥 RUD 描画エフェクト
    if(p.exploded){
        if(document.getElementById('b-rud').style.display!=='block'){
            document.getElementById('b-rud').style.display='block';
            document.getElementById('rud-text').innerText=p.rud_reason||failReason;
        }
        if(p.rud_reason&&p.rud_reason.includes("アコーディオン")){
            shipGroup.scale.z=0.03;shipGroup.scale.x=2.5;shipGroup.scale.y=2.5;
        }else{
            shipGroup.scale.set(0.001,0.001,0.001);
        }
    }

    if(p.phase==="ARRIVED"&&document.getElementById('b-success').style.display!=='block'){
        document.getElementById('b-success').style.display='block';
    }

    // カメラワーク
    camMain.position.set(0,18+p.v_c*10,currentZ-55-p.v_c*30);
    camMain.lookAt(0,0,currentZ+30);

    // CAM 02（目的地ゲート待ち受けカメラ）
    camPip.position.set(0,40,12600);
    camPip.lookAt(shipGroup.position);
    rPip.render(scene,camPip);

    // メイン描画
    rMain.render(scene,camMain);

    // テレメトリHUD更新
    document.getElementById('h-phase').innerText=p.phase;
    document.getElementById('h-temp').innerText=`${Math.round(p.heat_k)} K`;
    document.getElementById('h-stime').innerText=`T+ ${p.ship_time.toFixed(1)}s`;
    document.getElementById('h-etime').innerText=`T+ ${p.earth_time.toFixed(1)}s`;
    document.getElementById('t-vc').innerText=p.v_c.toFixed(3);
    document.getElementById('t-dist').innerText=(p.pos_ratio*100.0).toFixed(1);
    document.getElementById('t-g').innerText=p.effective_g.toFixed(1);
    const gamma=1.0/Math.sqrt(Math.max(0.001,1.0-Math.min(0.999,p.v_c)**2));
    document.getElementById('t-gamma').innerText=gamma.toFixed(2);
}
requestAnimationFrame(renderFrame);

window.addEventListener('resize',()=>{
    const w=window.innerWidth,h=window.innerHeight;
    rMain.setSize(w,h);camMain.aspect=w/h;camMain.updateProjectionMatrix();
});
}catch(e){console.error(e);}
});
</script></body></html>"""

final_app_html = (
    html_code.replace("__SIM_DATA__", sim_json)
    .replace("__SIM_CFG__", cfg_json)
    .replace("__FAIL_MSG__", fail_msg_safe)
)

components.html(final_app_html, height=880)

if warp_engage:
  st.markdown("---")
  st.markdown("### 📋 航法ログ・タイムディレーション詳細")
  if sim_error:
    st.error(f"⚠️ **時空災害 (RUD) 発生**: {sim_error}")
  else:
    st.success(
        "🎉 **減速ゲート捕捉成功**: 目的宙域の軌道ステーションへの進入を確認。"
    )
