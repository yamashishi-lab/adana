import json
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hyper-Drive Architect: Apex Cinematic 4K Master",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("🛸 Hyper-Drive Architect: Apex WaveRider (Master SF 4K Edition)")
st.caption(
    "※ 決定版：引きのワイドビュー・OrbitControls自由視点・CAM02フェーズ自動切替監視モニター・現代航空×深宇宙精密ハイブリッド造形・プラズマ噴射粒子＆ワープ衝撃波"
)

# =========================================================================
# 🔬 機体・動力炉・目的地・天候データベース
# =========================================================================
VESSEL_DESIGNS = {
    "極超音速ウェイブライダー『ヴァルキリー SSTO』": {
        "id": "waverider_valkyrie",
        "style": "stealth_waverider",
        "catapult_mach": 14.5,
        "desc": "チタン合金フレーム＋分割ステルス多面体。軌道上で背部装甲が観音開き展開し、超伝導デュアルワープリングがせり出す次世代機。",
    },
    "磁気慣性核融合クルーザー『プロメテウス』": {
        "id": "prometheus_cruiser",
        "style": "magnetic_fusion",
        "catapult_mach": 11.0,
        "desc": "船尾に巨大なオープンフレーム露出トラス、球形He3燃料タンク群、ソレノイド支柱を配置した重工業ディープスペース巡航艦。",
    },
    "電磁カタパルト迎撃槍『ロンギヌス・インターセプター』": {
        "id": "longinus_spear",
        "style": "massdriver_spear",
        "catapult_mach": 18.2,
        "desc": "空気抵抗極限の極細クサビ型。宇宙進出時に外装フェアリング4枚を四方へ爆砕パージし、黄金の深宇宙コアを露見させる突撃艇。",
    },
}

ARMOR_MATERIALS = {
    "漆黒ステルス電波吸収材 (RAM / Carbon Stealth)": {
        "metalness": 0.35,
        "roughness": 0.65,
        "plasma_hex": 0xD946EF,
        "desc": "電波反射を抑える無光沢カーボンナノチューブ層。大気圏突破時のプラズマは高エネルギー紫色。",
    },
    "鏡面クローム電磁反射装甲 (Mirror Electrum Plate)": {
        "metalness": 0.96,
        "roughness": 0.14,
        "plasma_hex": 0x38BDF8,
        "desc": "超高圧鏡面加工合金。地上光や星光をシャープに反射し、青白いアブレーション光を纏う。",
    },
    "液体金属アブレーション装甲 (Liquid Metallic Ablative)": {
        "metalness": 0.75,
        "roughness": 0.30,
        "plasma_hex": 0x10B981,
        "desc": "再生循環アブレーション材。超高温気流下でエメラルドグリーンのイオン化皮膜を形成。",
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

WARP_TOPOLOGIES = {
    "アルクビエレ時空曲率バブル (Alcubierre Bubble)": {
        "type": "alcubierre",
        "halo_hex": 0x38BDF8,
        "desc": "前方の空間を収縮させ後方を膨張。チェレンコフ光の青白レンズバブルを形成。",
    },
    "アインシュタイン・ローゼン橋 (Wormhole Gate)": {
        "type": "wormhole",
        "halo_hex": 0xC084FC,
        "desc": "事象の地平面を穿孔。吸い込まれるような幾何学重力トンネルを突破。",
    },
    "量子スリップストリーム (Quantum Stream)": {
        "type": "slipstream",
        "halo_hex": 0x34D399,
        "desc": "超弦格子に沿って位相滑空。エメラルド色のアーク放電とともに巡航。",
    },
}

LAUNCH_ENVIRONMENTS = {
    "深夜 (ネオン夜景＆星彩サーチライト)": {
        "sky_top": "#010309",
        "sky_mid": "#040e24",
        "sky_bot": "#0a1f44",
        "sun_color": 0x64748B,
        "sun_pos": [-400, 2500, -1200],
        "sun_int": 1.4,
        "fog_color": 0x050C16,
        "fog_density": 0.000028,
    },
    "夜明け (マジックアワー / 富士朝焼け)": {
        "sky_top": "#030712",
        "sky_mid": "#1e3a8a",
        "sky_bot": "#f97316",
        "sun_color": 0xFFD8A8,
        "sun_pos": [1500, 700, -800],
        "sun_int": 4.8,
        "fog_color": 0x1E293B,
        "fog_density": 0.000022,
    },
    "荒天・雷鳴成層圏突破 (Storm Thunder)": {
        "sky_top": "#050811",
        "sky_mid": "#0e1a2b",
        "sky_bot": "#1a2a40",
        "sun_color": 0x93C5FD,
        "sun_pos": [200, 1800, 300],
        "sun_int": 2.2,
        "fog_color": 0x111D30,
        "fog_density": 0.000045,
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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🛸 機体設計 & メカ構造",
    "🛡️ 外装装甲 & 補助モジュール",
    "⚡ 地上射出 & 大気環境",
    "🌌 時空駆動炉 & ワープトポロジー",
    "🎯 目的地航路 & フリップ減速",
])

with tab1:
  col1, col2 = st.columns(2)
  with col1:
    vessel_sel = st.selectbox("ベース艦種 (Chassis)", list(VESSEL_DESIGNS.keys()))
    vessel_cfg = VESSEL_DESIGNS[vessel_sel]
    hull_primary = st.color_picker("チタン合金フレーム配色", "#1e293b")
    tile_color = st.color_picker("耐熱カーボン/MLI配色", "#0a0f1d")
  with col2:
    st.info(f"**艦種概要:** {vessel_cfg['desc']}")
    wings_span = st.slider(
        "可動デルタ翼 / カナード展開幅 (m)", 14.0, 42.0, 26.0, step=1.0
    )
    radiator_blades = st.slider("軌道展開 放熱ラジエーター枚数", 2, 8, 4, step=2)

with tab2:
  col1, col2 = st.columns(2)
  with col1:
    armor_sel = st.selectbox("先進外装装甲システム", list(ARMOR_MATERIALS.keys()))
    armor_cfg = ARMOR_MATERIALS[armor_sel]
    st.caption(f"※ {armor_cfg['desc']}")
  with col2:
    aux_booster = st.checkbox(
        "外装使い捨てラムジェット・ブースター×2 (高度60kmパージ)",
        value=True,
    )
    debris_laser = st.checkbox(
        "前方レーザー・デブリ排除システム (ワープ中照射)", value=True
    )

with tab3:
  col1, col2 = st.columns(2)
  with col1:
    catapult_sel = st.selectbox("地上電磁射出施設", list(LAUNCH_CATAPULTS.keys()))
    catapult_cfg = LAUNCH_CATAPULTS[catapult_sel]
    catapult_boost = st.slider("超伝導コイル電力チャージ率 (%)", 80, 160, 120, step=5)
  with col2:
    env_sel = st.selectbox("射出環境・天候プリセット", list(LAUNCH_ENVIRONMENTS.keys()))
    env_cfg = LAUNCH_ENVIRONMENTS[env_sel]
    launch_aoa = st.slider("大気圏突破 迎角 (AoA deg)", 1.0, 12.0, 4.5, step=0.5)

with tab4:
  col1, col2 = st.columns(2)
  with col1:
    power_sel = st.selectbox("主推進動力炉", list(POWER_CORES.keys()))
    power_cfg = POWER_CORES[power_sel]
    warp_sel = st.selectbox("ワープ空間トポロジー", list(WARP_TOPOLOGIES.keys()))
    warp_cfg = WARP_TOPOLOGIES[warp_sel]
    st.caption(f"※ {warp_cfg['desc']}")
  with col2:
    warp_curvature = st.slider("時空曲率倍率 (Warp Factor)", 1.0, 9.9, 8.8, step=0.1)
    shock_diamonds = st.slider("推進炎 ショックダイヤモンド段数", 2, 6, 4, step=1)
    damper_rate = st.slider(
        "慣性ダンパー相殺率 (%)",
        99.000,
        99.999,
        99.998,
        step=0.001,
        format="%.3f%%",
    )

with tab5:
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
    st.caption("※ 航法AIが最適な減速Gカーブを自動計算し、100%確実にゲート内へ停止着艦します。")


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
        "purge_sabot": 0.0,
        "purge_booster": 0.0,
        "purge_fairing": 0.0,
        "rcs_active": False,
        "warp_flash": 0.0,
        "warp_ring_wave": 0.0,
        "plasma_alpha": 0.0,
        "space_ratio": 0.0,
        "progress": 0.0,
        "ship_time": 0.0,
        "earth_time": 0.0,
        "engine_active": False,
        "catapult_active": False,
        "laser_active": False,
        "vapor_cone": 0.0,
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
        "purge_sabot": 0.0,
        "purge_booster": 0.0,
        "purge_fairing": 0.0,
        "rcs_active": False,
        "warp_flash": 0.0,
        "warp_ring_wave": 0.0,
        "plasma_alpha": 0.0,
        "space_ratio": 0.0,
        "progress": 0.0,
        "ship_time": 0.0,
        "earth_time": 0.0,
        "engine_active": False,
        "catapult_active": bool(t_cd >= -3.0),
        "laser_active": False,
        "vapor_cone": 0.0,
        "rx": 0.0,
        "ry": 1.2,
        "pitch_deg": float(catapult_cfg["angle_deg"]),
    })

  total_sim_steps = 160
  c_angle_rad = np.radians(catapult_cfg["angle_deg"])
  exit_m = catapult_cfg["exit_mach"] * (catapult_boost / 100.0)

  cur_alt = 0.05
  cur_downrange = 0.0
  cur_mach = 0.0
  cur_vc = 0.0
  cur_progress = 0.0
  purge_s = 0.0
  purge_b = 0.0
  purge_f = 0.0
  warp_fl = 0.0
  warp_wave = 0.0

  for step in range(total_sim_steps):
    t = float(step * dt)
    rcs_on = False
    laser_on = False
    vapor = 0.0
    warp_fl = max(0.0, warp_fl - 0.25 * dt)
    warp_wave = max(0.0, warp_wave - 0.3 * dt)

    if t <= 3.0:
      phase = "RAIL_ACCELERATION"
      cur_mach = (t / 3.0) * exit_m
      cur_alt = 0.05 + (t / 3.0) * 1.8 * np.sin(c_angle_rad)
      cur_downrange = (t / 3.0) * 1.8 * np.cos(c_angle_rad)
      cur_g = 12.5 * (catapult_boost / 100.0)
      plasma = 0.0
      morph_ring = 0.0
      morph_wings = 0.0
      space_r = 0.0
      eng_on = False
      pitch_deg = catapult_cfg["angle_deg"]
      if 0.9 <= cur_mach <= 1.4:
        vapor = 1.0 - abs(cur_mach - 1.15) / 0.25
    elif cur_alt < 120.0:
      phase = "HYPERSONIC_CLIMB"
      eng_on = True
      cur_mach = min(34.0, cur_mach + 1.9 * dt)
      climb_speed = cur_mach * 340.0
      cur_alt += (climb_speed * np.sin(c_angle_rad) * dt) / 1000.0
      cur_downrange += (climb_speed * np.cos(c_angle_rad) * dt) / 1000.0
      cur_g = 4.4
      if 15.0 <= cur_alt <= 75.0:
        plasma = float(np.sin(((cur_alt - 15.0) / 60.0) * np.pi) * 0.98)
      else:
        plasma = 0.0
      morph_ring = 0.0
      morph_wings = min(1.0, (cur_alt / 80.0))
      space_r = float(np.clip((cur_alt - 15.0) / 75.0, 0.0, 1.0))
      pitch_deg = float(catapult_cfg["angle_deg"] * (1.0 - space_r * 0.7))
      purge_s = min(1.0, purge_s + 0.5 * dt)
      if cur_alt >= 60.0 and aux_booster:
        purge_b = min(1.0, purge_b + 0.25 * dt)
    elif cur_progress < 0.06:
      phase = "ORBITAL_TRANSFORM"
      eng_on = False
      cur_alt = 145.0
      plasma = 0.0
      morph_ring = min(1.0, morph_ring + 0.14 * dt * 2.0)
      morph_wings = 1.0
      if vessel_cfg["style"] == "massdriver_spear":
        purge_f = min(1.0, purge_f + 0.2 * dt)
      space_r = 1.0
      cur_g = 1.0
      cur_vc = 0.03
      cur_progress += 0.005
      pitch_deg = 0.0
      rcs_on = True
      if cur_progress >= 0.055:
        warp_fl = 1.0
    elif cur_progress < flip_ratio:
      phase = "WARP_CRUISE"
      eng_on = True
      target_vc = min(0.996, 0.20 + (warp_curvature / 10.0) * 0.79)
      cur_vc = min(target_vc, cur_vc + 0.12 * dt)
      cur_g = 1.8
      plasma = 0.0
      morph_ring = 1.0
      morph_wings = 1.0
      space_r = 1.0
      cur_progress += (cur_vc * 0.018) * dt
      pitch_deg = 0.0
      laser_on = debris_laser
      if cur_progress >= flip_ratio - 0.015:
        warp_wave = 1.0
    else:
      phase = "DECEL_APPROACH"
      eng_on = True
      rem_dist = max(0.0001, 1.0 - cur_progress)
      cur_vc = max(0.008, min(cur_vc, rem_dist * 2.6))
      cur_g = 3.6
      plasma = 0.0
      morph_ring = max(0.2, cur_vc * 1.4)
      morph_wings = 1.0
      space_r = 1.0
      cur_progress = min(1.0, cur_progress + (cur_vc * 0.013) * dt)
      pitch_deg = 180.0
      rcs_on = bool(cur_progress < flip_ratio + 0.04)

    gamma = 1.0 / np.sqrt(max(0.001, 1.0 - (min(0.9995, cur_vc) ** 2)))
    ship_t += dt / gamma
    earth_t += dt * gamma
    temp_k = 293.0 + (cur_mach * 48.0 if cur_alt < 80 else cur_vc * 260.0)

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
        "purge_sabot": float(purge_s),
        "purge_booster": float(purge_b),
        "purge_fairing": float(purge_f),
        "rcs_active": rcs_on,
        "warp_flash": float(warp_fl),
        "warp_ring_wave": float(warp_wave),
        "plasma_alpha": float(plasma),
        "space_ratio": float(space_r),
        "progress": float(min(1.0, cur_progress)),
        "ship_time": float(ship_t),
        "earth_time": float(earth_t),
        "engine_active": eng_on,
        "catapult_active": False,
        "laser_active": laser_on,
        "vapor_cone": float(vapor),
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
            "purge_sabot": float(purge_s),
            "purge_booster": float(purge_b),
            "purge_fairing": float(purge_f),
            "rcs_active": False,
            "warp_flash": 0.0,
            "warp_ring_wave": 0.0,
            "plasma_alpha": 0.0,
            "space_ratio": 1.0,
            "progress": 1.0,
            "ship_time": float(ship_t),
            "earth_time": float(earth_t),
            "engine_active": False,
            "catapult_active": False,
            "laser_active": False,
            "vapor_cone": 0.0,
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
  st.caption("※ ハードSF仕様：安全リミッター内蔵。目的宙域の電磁テザーゲートへ100%停止着艦します。")

sim_records, _ = run_simulation(preview_only=(not launch_clicked))

client_config = {
    "is_preview": not launch_clicked,
    "vessel_id": vessel_cfg["id"],
    "style": vessel_cfg["style"],
    "hull_color": int(hull_primary.lstrip("#"), 16),
    "tile_color": int(tile_color.lstrip("#"), 16),
    "armor_metalness": armor_cfg["metalness"],
    "armor_roughness": armor_cfg["roughness"],
    "plasma_hex": armor_cfg["plasma_hex"],
    "flame_hex": power_cfg["flame_hex"],
    "outer_hex": power_cfg["outer_hex"],
    "spark_hex": power_cfg["spark_hex"],
    "warp_type": warp_cfg["type"],
    "warp_halo_hex": warp_cfg["halo_hex"],
    "dest_type": dest_cfg["type"],
    "dest_color": dest_cfg["color_hex"],
    "radiator_count": radiator_blades,
    "wings_span": wings_span,
    "aux_booster": aux_booster,
    "debris_laser": debris_laser,
    "shock_diamonds": shock_diamonds,
    "catapult_angle": catapult_cfg["angle_deg"],
    "catapult_len": catapult_cfg["rail_len"],
    "env": env_cfg,
}

sim_json = json.dumps(sim_records)
cfg_json = json.dumps(client_config)

# =========================================================================
# 📺 Three.js + Web Audio 完全魔改造・シネマティックマスター描画テンプレート
# =========================================================================
html_markup = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{box-sizing:border-box;}body,html{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:#000206;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:#fff;user-select:none;}
#canvas-viewport{width:100%;height:100%;display:block;position:absolute;top:0;left:0;z-index:1;}
.top-banner{position:absolute;top:0;left:0;width:100%;min-height:42px;background:linear-gradient(180deg,rgba(2,6,16,0.96) 0%,rgba(3,10,24,0.92) 100%);border-bottom:1px solid rgba(56,189,248,0.22);display:flex;align-items:center;justify-content:space-between;padding:4px 16px;z-index:20;flex-wrap:wrap;gap:6px 12px;box-shadow:0 4px 20px rgba(0,0,0,0.7);}
.banner-group{display:flex;align-items:center;gap:10px;flex-wrap:wrap;}
.pip-overlay{position:absolute;top:48px;right:10px;width:340px;height:190px;border:2px solid rgba(56,189,248,0.95);border-radius:6px;z-index:60;pointer-events:auto;cursor:pointer;background:rgba(2,6,23,0.35);box-shadow:0 12px 35px rgba(0,0,0,0.9);overflow:hidden;}
.pip-scanlines{position:absolute;top:0;left:0;width:100%;height:100%;background:repeating-linear-gradient(0deg,rgba(0,0,0,0.25),rgba(0,0,0,0.25) 1px,transparent 1px,transparent 3px);pointer-events:none;z-index:62;}
.pip-rec{position:absolute;bottom:6px;right:8px;font-size:9px;font-family:monospace;color:#ef4444;font-weight:900;display:flex;align-items:center;gap:4px;z-index:65;pointer-events:none;}
.pip-rec-dot{width:6px;height:6px;background:#ef4444;border-radius:50%;animation:blink-rec 1s infinite;}
@keyframes blink-rec{0%,100%{opacity:1;}50%{opacity:0.2;}}
.pip-tag{position:absolute;top:6px;left:8px;font-size:9px;font-weight:800;color:#fff;background:rgba(15,23,42,0.92);padding:2px 6px;border-radius:2px;letter-spacing:1px;font-family:monospace;pointer-events:none;border-left:2px solid #38bdf8;z-index:65;}
.pip-hint{position:absolute;top:6px;right:8px;font-size:8px;font-family:monospace;color:#94a3b8;background:rgba(15,23,42,0.92);padding:2px 5px;border-radius:2px;pointer-events:none;z-index:65;}
.hud-bottom{position:absolute;bottom:0;left:0;width:100%;height:75px;background:rgba(2,6,23,0.95);border-top:1px solid rgba(255,255,255,0.15);padding:8px 24px;display:flex;align-items:center;justify-content:space-between;z-index:20;}
.telem-box{display:flex;flex-direction:column;}
.telem-lbl{font-size:9px;color:#94a3b8;letter-spacing:1px;}
.telem-val{font-size:clamp(14px,1.8vw,18px);font-weight:900;font-family:monospace;color:#f8fafc;}
.banner{display:none;position:absolute;top:140px;left:50%;transform:translateX(-50%);padding:22px 36px;border-radius:8px;z-index:80;text-align:center;}
.banner-success{background:rgba(6,78,59,0.95);border:2px solid #10b981;box-shadow:0 0 60px rgba(16,185,129,0.8);}
.crosshair{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);pointer-events:none;z-index:25;opacity:0.25;}
#flash-overlay{position:absolute;top:0;left:0;width:100%;height:100%;background:#fff;z-index:90;pointer-events:none;opacity:0.0;}
.orbit-hint{position:absolute;bottom:85px;left:50%;transform:translateX(-50%);font-size:10px;font-family:monospace;color:#38bdf8;background:rgba(2,6,23,0.8);padding:4px 12px;border-radius:12px;border:1px solid rgba(56,189,248,0.3);pointer-events:none;z-index:30;letter-spacing:1px;}
</style></head>
<body>
<canvas id="canvas-viewport"></canvas>
<div id="flash-overlay"></div>
<div id="pip-click-box" class="pip-overlay" title="クリックでCAM 02の表示/非表示を切り替え">
    <div class="pip-scanlines"></div>
    <div id="pip-tag" class="pip-tag">CAM 02: GROUND TRACKER</div>
    <div id="pip-hint" class="pip-hint">[CLICK TO TOGGLE]</div>
    <div class="pip-rec"><div class="pip-rec-dot"></div>LIVE STREAM</div>
</div>
<div class="orbit-hint">🖱️ MOUSE DRAG: ROTATE | WHEEL: ZOOM (ORBIT CONTROL ACTIVE)</div>
<div class="top-banner" id="top-banner-bar">
    <div class="banner-group">
        <span style="color:#38bdf8;font-weight:800;font-size:11px;letter-spacing:1.5px;">APEX SSTO PRO</span>
        <span style="color:rgba(255,255,255,0.2);">|</span>
        <span style="color:#94a3b8;font-family:monospace;font-size:10px;">PHASE: <strong id="h-phase" style="color:#f59e0b;">STANDBY</strong></span>
    </div>
    <div class="banner-group" style="font-family:monospace;font-size:10px;">
        <span style="color:#94a3b8;">ALT: <strong id="h-alt" style="color:#f8fafc;">0.0 km</strong></span>
        <span style="color:#94a3b8;">SPEED: <strong id="h-speed" style="color:#38bdf8;">M 0.0</strong></span>
        <span style="color:#94a3b8;">SHIP TIME: <strong id="h-stime">00:00.0</strong></span>
    </div>
</div>
<div class="banner banner-success" id="b-success">
    <div style="font-size:20px;font-weight:900;color:#6ee7b7;">🎉 INTERPLANETARY WARP COMPLETE 🎉</div>
    <div style="font-size:12px;margin-top:6px;color:#ecfdf5;">DESTINATION MAGNETIC TETHER CAPTURE LOCKED</div>
</div>
<div class="hud-bottom">
    <div class="telem-box"><div class="telem-lbl">WARP VELOCITY</div><div class="telem-val"><span id="t-vc">0.00</span> <span style="font-size:10px;color:#94a3b8;">c</span></div></div>
    <div class="telem-box"><div class="telem-lbl">MISSION PROGRESS</div><div class="telem-val"><span id="t-dist">0.0</span> <span style="font-size:10px;color:#94a3b8;">%</span></div></div>
    <div class="telem-box"><div class="telem-lbl">CORE TEMP</div><div class="telem-val"><span id="t-temp">293</span> <span style="font-size:10px;color:#94a3b8;">K</span></div></div>
    <div class="telem-box"><div class="telem-lbl">LORENTZ (γ)</div><div class="telem-val"><span id="t-gamma">1.00</span> <span style="font-size:10px;color:#94a3b8;">x</span></div></div>
</div>

<svg class="crosshair" id="hud-crosshair" width="80" height="80" viewBox="0 0 80 80">
  <circle cx="40" cy="40" r="26" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="6,4"/>
  <line x1="40" y1="8" x2="40" y2="22" stroke="#38bdf8" stroke-width="1.5"/>
  <line x1="40" y1="58" x2="40" y2="72" stroke="#38bdf8" stroke-width="1.5"/>
  <line x1="8" y1="40" x2="22" y2="40" stroke="#38bdf8" stroke-width="1.5"/>
  <line x1="58" y1="40" x2="72" y2="40" stroke="#38bdf8" stroke-width="1.5"/>
</svg>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
window.addEventListener('DOMContentLoaded',()=>{
try{
const data=__SIM_DATA__;const cfg=__SIM_CFG__;
const canvas=document.getElementById('canvas-viewport');
let winW=window.innerWidth,winH=window.innerHeight;
const pipBox=document.getElementById('pip-click-box'),topBannerBar=document.getElementById('top-banner-bar');
const flashOverlay=document.getElementById('flash-overlay');
const pipTag=document.getElementById('pip-tag');
let pipVisible=true;

function updatePipPosition(){if(pipBox&&topBannerBar){const rect=topBannerBar.getBoundingClientRect();pipBox.style.top=Math.round(rect.bottom+4)+'px';}}
updatePipPosition();
window.addEventListener('resize',()=>{winW=window.innerWidth;winH=window.innerHeight;updatePipPosition();renderer.setSize(winW,winH);});

pipBox.addEventListener('click',()=>{
    pipVisible=!pipVisible;
    pipBox.style.border=pipVisible?'2px solid rgba(56,189,248,0.95)':'1px solid rgba(255,255,255,0.2)';
    pipBox.style.height=pipVisible?'190px':'28px';
    pipTag.style.display=pipVisible?'block':'none';
    document.getElementById('pip-hint').innerText=pipVisible?'[CLICK TO HIDE]':'[CLICK TO SHOW]';
});

// レンダラー
const renderer=new THREE.WebGLRenderer({canvas:canvas,antialias:true,powerPreference:"high-performance"});
renderer.setPixelRatio(Math.min(window.devicePixelRatio,1.5));
renderer.setSize(winW,winH);
renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.4;

const scene=new THREE.Scene();
scene.fog=new THREE.FogExp2(cfg.env.fog_color,cfg.env.fog_density);

// メインカメラ＆CAM02
const cameraMain=new THREE.PerspectiveCamera(38,winW/winH,0.5,150000);
const cameraPip=new THREE.PerspectiveCamera(28,340/190,1.0,150000);

// OrbitControls (自由回転＆ホイールズーム対応)
const controls=new THREE.OrbitControls(cameraMain,renderer.domElement);
controls.enableDamping=true;
controls.dampingFactor=0.08;
controls.minDistance=25.0;
controls.maxDistance=450.0;
controls.maxPolarAngle=Math.PI/2+0.1;

const sunLight=new THREE.DirectionalLight(cfg.env.sun_color,cfg.env.sun_int);
sunLight.position.set(cfg.env.sun_pos[0],cfg.env.sun_pos[1],cfg.env.sun_pos[2]);scene.add(sunLight);
scene.add(new THREE.AmbientLight(0x1e293b,1.8));

const rimLight=new THREE.DirectionalLight(0x38bdf8,2.2);rimLight.position.set(0,-10,0);scene.add(rimLight);

// Web Audio
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

        const sOsc=actx.createOscillator();sOsc.type='sine';sOsc.frequency.value=34;
        subBass=actx.createGain();subBass.gain.value=0.0001;
        sOsc.connect(subBass);subBass.connect(actx.destination);sOsc.start(0);
    }
    if(actx.state==='suspended')actx.resume();
}
window.addEventListener('click',initSFX,{once:true});

// テクスチャ
function createEnvMap(){
    const cvs=document.createElement('canvas');cvs.width=512;cvs.height=256;const ctx=cvs.getContext('2d');
    const g=ctx.createLinearGradient(0,0,0,256);
    g.addColorStop(0,cfg.env.sky_top);g.addColorStop(0.4,cfg.env.sky_mid);g.addColorStop(0.7,cfg.env.sky_bot);g.addColorStop(1,'#020b18');
    ctx.fillStyle=g;ctx.fillRect(0,0,512,256);
    return new THREE.CanvasTexture(cvs);
}
const envMapTex=createEnvMap();envMapTex.mapping=THREE.EquirectangularReflectionMapping;scene.environment=envMapTex;

function createGlowTexture(colorHex){
    const cvs=document.createElement('canvas');cvs.width=128;cvs.height=128;const ctx=cvs.getContext('2d');
    const g=ctx.createRadialGradient(64,64,0,64,64,64);
    g.addColorStop(0,colorHex);g.addColorStop(0.35,colorHex);g.addColorStop(1,'rgba(0,0,0,0)');
    ctx.fillStyle=g;ctx.fillRect(0,0,128,128);
    return new THREE.CanvasTexture(cvs);
}
const cyanGlowTex=createGlowTexture('rgba(56,189,248,0.9)');
const flameGlowTex=createGlowTexture('rgba(244,63,94,0.95)');

function createAdvancedArmorTex(){
    const cvs=document.createElement('canvas');cvs.width=1024;cvs.height=1024;const ctx=cvs.getContext('2d');
    ctx.fillStyle='#0f172a';ctx.fillRect(0,0,1024,1024);
    ctx.strokeStyle='#1e293b';ctx.lineWidth=2;
    for(let x=0;x<1024;x+=48){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,1024);ctx.stroke();}
    for(let y=0;y<1024;y+=48){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(1024,y);ctx.stroke();}
    ctx.fillStyle='#f59e0b';
    ctx.fillRect(100,200,60,6);ctx.fillRect(400,600,60,6);ctx.fillRect(800,300,60,6);
    return new THREE.CanvasTexture(cvs);
}
const armorTex=createAdvancedArmorTex();armorTex.wrapS=THREE.RepeatWrapping;armorTex.wrapT=THREE.RepeatWrapping;armorTex.repeat.set(6,6);

// マテリアル
const armorMat=new THREE.MeshStandardMaterial({
    color:cfg.hull_color,
    roughness:cfg.armor_roughness,
    metalness:cfg.armor_metalness,
    bumpMap:armorTex,
    bumpScale:0.02,
    flatShading:false
});
const carbonTileMat=new THREE.MeshStandardMaterial({color:cfg.tile_color,roughness:0.8,metalness:0.2,bumpMap:armorTex,bumpScale:0.03,flatShading:false});
const goldFoilMat=new THREE.MeshStandardMaterial({color:0xd97706,roughness:0.35,metalness:0.95});
const darkFrameMat=new THREE.MeshStandardMaterial({color:0x0f172a,metalness:0.9,roughness:0.3});
const copperMat=new THREE.MeshStandardMaterial({color:0xb45309,metalness:0.9,roughness:0.3});
const canopyMat=new THREE.MeshPhysicalMaterial({color:0x38bdf8,roughness:0.08,metalness:0.92,transparent:true,opacity:0.85,transmission:0.7});
const coilGlowMat=new THREE.MeshBasicMaterial({color:0x38bdf8});
const plasmaMat=new THREE.MeshBasicMaterial({color:cfg.plasma_hex,transparent:true,opacity:0.0,blending:THREE.AdditiveBlending,side:THREE.DoubleSide});
const laserMat=new THREE.MeshBasicMaterial({color:0x38bdf8,blending:THREE.AdditiveBlending});
const radiatorMat=new THREE.MeshStandardMaterial({color:0x1e293b,metalness:0.9,roughness:0.2,emissive:0x000000,emissiveIntensity:0.0});

// =========================================================================
// 🗻 地上・相模湾・富士山麓 ＆ 球体地球
// =========================================================================
const groundGroup=new THREE.Group();scene.add(groundGroup);
const ocean=new THREE.Mesh(new THREE.PlaneGeometry(80000,80000),new THREE.MeshStandardMaterial({color:0x081b2e,roughness:0.08,metalness:0.92}));
ocean.rotation.x=-Math.PI/2;groundGroup.add(ocean);

const cityLightsGeo=new THREE.BufferGeometry(),cityCount=4500;
const cityPos=new Float32Array(cityCount*3),cityCols=new Float32Array(cityCount*3);
for(let i=0;i<cityCount*3;i+=3){
    const dist=Math.random()*22000+2500;
    const ang=Math.random()*Math.PI*0.8-0.2;
    cityPos[i]=Math.cos(ang)*dist+6000;
    cityPos[i+1]=2.0+Math.random()*15.0;
    cityPos[i+2]=Math.sin(ang)*dist-12000;
    const isAmber=Math.random()>0.4;
    cityCols[i]=isAmber?1.0:0.4;cityCols[i+1]=isAmber?0.65:0.8;cityCols[i+2]=isAmber?0.2:1.0;
}
cityLightsGeo.setAttribute('position',new THREE.BufferAttribute(cityPos,3));
cityLightsGeo.setAttribute('color',new THREE.BufferAttribute(cityCols,3));
const cityPoints=new THREE.Points(cityLightsGeo,new THREE.PointsMaterial({size:3.5,vertexColors:true,transparent:true,opacity:0.85}));
groundGroup.add(cityPoints);

const fujiCurvePts=[];
for(let deg=0;deg<=20;deg++){
    const tNorm=deg/20.0;
    const y=tNorm*3776;
    const radius=Math.pow(1.0-tNorm,2.2)*14000+1200;
    fujiCurvePts.push(new THREE.Vector2(radius,y));
}
const fujiGeo=new THREE.LatheGeometry(fujiCurvePts,48);
const fujiMesh=new THREE.Mesh(fujiGeo,new THREE.MeshStandardMaterial({color:0x15202b,roughness:0.85}));
fujiMesh.position.set(13000,0,-18000);groundGroup.add(fujiMesh);

const snowPts=[];
for(let deg=14;deg<=20;deg++){
    const tNorm=deg/20.0;
    const y=tNorm*3776;
    const radius=Math.pow(1.0-tNorm,2.2)*14000+1200;
    snowPts.push(new THREE.Vector2(radius*1.002,y));
}
const snowMesh=new THREE.Mesh(new THREE.LatheGeometry(snowPts,48),new THREE.MeshStandardMaterial({color:0xffffff,roughness:0.4}));
snowMesh.position.set(13000,0,-18000);groundGroup.add(snowMesh);

// カタパルトレール＆トラス
const railLen3D=cfg.catapult_len*150.0,catAngleRad=THREE.MathUtils.degToRad(cfg.catapult_angle);
const railGroup=new THREE.Group();groundGroup.add(railGroup);
const railSpine=new THREE.Mesh(new THREE.BoxGeometry(10,6,railLen3D),armorMat);
railSpine.position.set(0,railLen3D*0.5*Math.sin(catAngleRad)+2.0,railLen3D*0.5*Math.cos(catAngleRad));
railSpine.rotation.x=catAngleRad;railGroup.add(railSpine);

for(let p=0;p<12;p++){
    const pz=(p/12)*railLen3D*Math.cos(catAngleRad);
    const py=(p/12)*railLen3D*Math.sin(catAngleRad);
    if(py>5.0){
        const pier=new THREE.Mesh(new THREE.CylinderGeometry(1.5,2.5,py,8),armorMat);
        pier.position.set(0,py*0.5,pz);railGroup.add(pier);
    }
}

const catapultCoils=[];
for(let c=0;c<26;c++){
    const cMesh=new THREE.Mesh(new THREE.TorusGeometry(14,0.65,16,36),coilGlowMat);
    const zDist=(c/26)*railLen3D;
    cMesh.position.set(0,zDist*Math.sin(catAngleRad)+2.0,zDist*Math.cos(catAngleRad));
    cMesh.rotation.x=catAngleRad;railGroup.add(cMesh);catapultCoils.push(cMesh);
}

const cloudGroup=new THREE.Group();groundGroup.add(cloudGroup);
const cloudGeo=new THREE.PlaneGeometry(700,350);
for(let ci=0;ci<40;ci++){
    const cp=new THREE.Mesh(cloudGeo,new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0.28,depthWrite:false}));
    cp.rotation.x=-Math.PI/2;cp.position.set((Math.random()-0.5)*40000,1350,(Math.random()-0.5)*40000);
    cloudGroup.add(cp);
}

// 球体地球＆リムグロー
const orbitalEarthGroup=new THREE.Group();scene.add(orbitalEarthGroup);
orbitalEarthGroup.position.set(0,-12500,2000);
const earthBody=new THREE.Mesh(new THREE.SphereGeometry(12000,64,64),new THREE.MeshStandardMaterial({color:0x0b2545,roughness:0.65,metalness:0.15}));
orbitalEarthGroup.add(earthBody);
const earthRim=new THREE.Mesh(new THREE.SphereGeometry(12120,64,64),new THREE.MeshBasicMaterial({color:0x38bdf8,transparent:true,opacity:0.42,side:THREE.BackSide,blending:THREE.AdditiveBlending}));
orbitalEarthGroup.add(earthRim);
orbitalEarthGroup.visible=false;

// =========================================================================
// 🚀 現代航空×深宇宙精密ハイブリッド造形宇宙船
// =========================================================================
const vesselGroup=new THREE.Group();scene.add(vesselGroup);
const slidingDorsalDoors=[],warpRingGroup=new THREE.Group();
const radiatorMeshes=[],boosterMeshes=[],fairingMeshes=[],sabotMeshes=[];

// 翼
function createSharpWing(span){
    const s=new THREE.Shape();s.moveTo(0,5);s.lineTo(span*0.5,-5);s.lineTo(span*0.48,-9);s.lineTo(0,-13);s.closePath();
    const g=new THREE.ExtrudeGeometry(s,{depth:0.45,bevelEnabled:true,bevelThickness:0.18,bevelSize:0.7,bevelSegments:3});
    const m=new THREE.Mesh(g,armorMat);m.rotation.x=Math.PI/2;m.position.y=-0.2;return m;
}

// 現代実在構造：くさび型ラムエアインテークダクト×2
for(let inSide of [-1,1]){
    const intakeBox=new THREE.Mesh(new THREE.BoxGeometry(2.4,1.8,7.5),armorMat);
    intakeBox.position.set(inSide*3.5,-0.6,2.0);intakeBox.rotation.y=inSide*0.08;vesselGroup.add(intakeBox);
    const intakeOpening=new THREE.Mesh(new THREE.BoxGeometry(2.0,1.2,1.0),darkFrameMat);
    intakeOpening.position.set(inSide*3.5,-0.6,5.8);vesselGroup.add(intakeOpening);
}

// 船種別造形
if(cfg.style==="stealth_waverider"){
    const bGeo=new THREE.CylinderGeometry(1.2,4.8,26,24);bGeo.scale(1.8,0.45,1.0);
    const body=new THREE.Mesh(bGeo,armorMat);body.rotation.x=Math.PI/2;vesselGroup.add(body);
    const heatBelly=new THREE.Mesh(bGeo,carbonTileMat);heatBelly.position.y=-0.12;heatBelly.scale.set(1.02,1.02,1.02);vesselGroup.add(heatBelly);
    vesselGroup.add(createSharpWing(cfg.wings_span));

    const canard=new THREE.Mesh(new THREE.BoxGeometry(cfg.wings_span*0.35,0.18,2.2),armorMat);canard.position.set(0,0.2,7.0);vesselGroup.add(canard);

    for(let side of [-1,1]){
        const vTail=new THREE.Mesh(new THREE.BoxGeometry(0.2,4.2,5.5),armorMat);vTail.position.set(side*3.2,2.0,-11.0);vTail.rotation.z=side*0.25;vesselGroup.add(vTail);
        const door=new THREE.Mesh(new THREE.BoxGeometry(3.6,0.35,12),armorMat);door.position.set(side*2.2,1.2,-2.0);vesselGroup.add(door);
        slidingDorsalDoors.push({mesh:door,side:side});
    }
}else if(cfg.style==="magnetic_fusion"){
    const frontCab=new THREE.Mesh(new THREE.ConeGeometry(3.2,14,24),armorMat);frontCab.rotation.x=Math.PI/2;frontCab.position.z=7;vesselGroup.add(frontCab);
    const midHull=new THREE.Mesh(new THREE.BoxGeometry(6,5,16),armorMat);vesselGroup.add(midHull);
    const trussGroup=new THREE.Group();trussGroup.position.set(0,0,-12);vesselGroup.add(trussGroup);
    const tFrame=new THREE.Mesh(new THREE.BoxGeometry(7,5.5,12),new THREE.MeshStandardMaterial({color:0x475569,wireframe:true}));trussGroup.add(tFrame);

    for(let i=0;i<4;i++){
        const ang=(i/4)*Math.PI*2;
        const tank=new THREE.Mesh(new THREE.SphereGeometry(1.6,24,24),goldFoilMat);
        tank.position.set(Math.cos(ang)*2.4,Math.sin(ang)*1.8,-11);vesselGroup.add(tank);
    }
    vesselGroup.add(createSharpWing(cfg.wings_span*0.75));
}else{
    const coreSpike=new THREE.Mesh(new THREE.CylinderGeometry(0.6,2.2,34,24),goldFoilMat);coreSpike.rotation.x=Math.PI/2;vesselGroup.add(coreSpike);
    vesselGroup.add(createSharpWing(cfg.wings_span*0.5));

    for(let f=0;f<4;f++){
        const ang=(f/4)*Math.PI*2;
        const fairing=new THREE.Mesh(new THREE.BoxGeometry(2.0,0.3,16),armorMat);
        fairing.position.set(Math.cos(ang)*1.4,Math.sin(ang)*1.4,4);
        fairing.rotation.z=ang;vesselGroup.add(fairing);
        fairingMeshes.push({mesh:fairing,vx:Math.cos(ang)*14.0,vy:Math.sin(ang)*14.0});
    }
}

// キャノピー
const canopy=new THREE.Mesh(new THREE.ConeGeometry(1.3,6.5,24),canopyMat);canopy.scale.set(1.0,0.45,1.8);canopy.rotation.x=Math.PI/2;canopy.position.set(0,0.8,8.0);vesselGroup.add(canopy);

// 可変推力偏向アイリスノズル花びらパドル×8
const nozzleGroup=new THREE.Group();nozzleGroup.position.set(0,0,-13.2);vesselGroup.add(nozzleGroup);
for(let p=0;p<8;p++){
    const ang=(p/8)*Math.PI*2;
    const paddle=new THREE.Mesh(new THREE.BoxGeometry(0.8,0.18,3.2),darkFrameMat);
    paddle.position.set(Math.cos(ang)*2.3,Math.sin(ang)*2.3,0);
    paddle.rotation.set(Math.sin(ang)*0.2,-Math.cos(ang)*0.2,ang);
    nozzleGroup.add(paddle);
}

// 超伝導ワープリング土台の銅製ソレノイドコイル＆極太配管
const solenoidBase=new THREE.Group();solenoidBase.position.set(0,0.8,-2.0);vesselGroup.add(solenoidBase);
for(let sc=0;sc<6;sc++){
    const solMesh=new THREE.Mesh(new THREE.TorusGeometry(1.8,0.25,12,24),copperMat);
    solMesh.position.set((sc-2.5)*0.8,0,0);solMesh.rotation.y=Math.PI/2;solenoidBase.add(solMesh);
}

// 放熱ラジエーターフィン
for(let r=0;r<cfg.radiator_count;r++){
    const rad=new THREE.Mesh(new THREE.BoxGeometry(3.8,0.06,1.4),radiatorMat);
    rad.position.set(0,0.9,-4.0-(r*1.8));vesselGroup.add(rad);radiatorMeshes.push(rad);
}

// ブースター
if(cfg.aux_booster){
    for(let bSide of [-1,1]){
        const bMesh=new THREE.Mesh(new THREE.CylinderGeometry(0.8,0.9,14,24),carbonTileMat);
        bMesh.position.set(bSide*(cfg.wings_span*0.35),-0.6,-5);bMesh.rotation.x=Math.PI/2;vesselGroup.add(bMesh);
        boosterMeshes.push({mesh:bMesh,side:bSide});
    }
}

// サボアーム
for(let sa of [-1,1]){
    const sabot=new THREE.Mesh(new THREE.BoxGeometry(1.8,0.8,6.0),darkFrameMat);
    sabot.position.set(sa*4.2,-1.2,0);vesselGroup.add(sabot);
    sabotMeshes.push({mesh:sabot,side:sa});
}

// ストロボ
const strobeLeft=new THREE.Mesh(new THREE.SphereGeometry(0.2,8,8),new THREE.MeshBasicMaterial({color:0xff0000}));
strobeLeft.position.set(-cfg.wings_span*0.48,-0.2,-8);vesselGroup.add(strobeLeft);
const strobeRight=new THREE.Mesh(new THREE.SphereGeometry(0.2,8,8),new THREE.MeshBasicMaterial({color:0x00ff00}));
strobeRight.position.set(cfg.wings_span*0.48,-0.2,-8);vesselGroup.add(strobeRight);

// デュアルワープリング
warpRingGroup.position.set(0,0.5,-2.0);vesselGroup.add(warpRingGroup);
const warpTorus1=new THREE.Mesh(new THREE.TorusGeometry(5.6,0.38,24,48),coilGlowMat);warpRingGroup.add(warpTorus1);
const warpTorus2=new THREE.Mesh(new THREE.TorusGeometry(6.4,0.28,24,48),armorMat);warpRingGroup.add(warpTorus2);

const ringGlowSprite=new THREE.Sprite(new THREE.SpriteMaterial({map:cyanGlowTex,blending:THREE.AdditiveBlending,transparent:true,opacity:0.0}));
ringGlowSprite.scale.set(22,22,1);warpRingGroup.add(ringGlowSprite);

// ワープアウト空間衝撃波リング
const warpWaveRing=new THREE.Mesh(
    new THREE.RingGeometry(2,4,48),
    new THREE.MeshBasicMaterial({color:0x38bdf8,side:THREE.DoubleSide,transparent:true,opacity:0.0,blending:THREE.AdditiveBlending})
);
warpWaveRing.rotation.x=Math.PI/2;vesselGroup.add(warpWaveRing);

// ヴェイパーコーン
const vaporCone=new THREE.Mesh(
    new THREE.ConeGeometry(10,5,32,1,true),
    new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0.0,side:THREE.DoubleSide})
);
vaporCone.rotation.x=-Math.PI/2;vaporCone.position.z=3.0;vesselGroup.add(vaporCone);

// レーザー＆プラズマ
const laserBeam=new THREE.Mesh(new THREE.CylinderGeometry(0.08,0.08,240,8),laserMat);
laserBeam.position.set(0,0,128);laserBeam.rotation.x=Math.PI/2;laserBeam.visible=false;vesselGroup.add(laserBeam);

const plasmaShell=new THREE.Mesh(new THREE.ConeGeometry(7.8,38,24,1,true),plasmaMat);
plasmaShell.position.z=-4;plasmaShell.rotation.x=-Math.PI/2;vesselGroup.add(plasmaShell);

const rcsMeshes=[];
for(let s=0;s<4;s++){
    const ang=(s/4)*Math.PI*2;
    const rCone=new THREE.Mesh(new THREE.ConeGeometry(0.4,2.5,8),new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0.0}));
    rCone.position.set(Math.cos(ang)*2.6,Math.sin(ang)*1.2,6.0);rCone.rotation.z=ang+Math.PI/2;
    vesselGroup.add(rCone);rcsMeshes.push(rCone);
}

// 推進炎＆ショックダイヤモンド
const plumeGroup=new THREE.Group();plumeGroup.position.set(0,0,-15);vesselGroup.add(plumeGroup);
const coreTorch=new THREE.Mesh(new THREE.ConeGeometry(2.4,24,24,1,true),new THREE.MeshBasicMaterial({color:0xffffff,blending:THREE.AdditiveBlending}));
coreTorch.rotation.x=Math.PI/2;coreTorch.position.z=-12;plumeGroup.add(coreTorch);

const outerTorch=new THREE.Mesh(new THREE.ConeGeometry(3.8,32,24,1,true),new THREE.MeshBasicMaterial({color:cfg.flame_hex,transparent:true,opacity:0.75,blending:THREE.AdditiveBlending}));
outerTorch.rotation.x=Math.PI/2;outerTorch.position.z=-16;plumeGroup.add(outerTorch);

const torchGlow=new THREE.Sprite(new THREE.SpriteMaterial({map:flameGlowTex,blending:THREE.AdditiveBlending,transparent:true,opacity:0.85}));
torchGlow.scale.set(16,16,1);torchGlow.position.set(0,0,-12);plumeGroup.add(torchGlow);

const shockDiamonds=[];
for(let d=0;d<cfg.shock_diamonds;d++){
    const dia=new THREE.Mesh(new THREE.RingGeometry(0.2,1.8-(d*0.25),24),new THREE.MeshBasicMaterial({color:cfg.spark_hex,side:THREE.DoubleSide,blending:THREE.AdditiveBlending}));
    dia.position.set(0,0,-4.0-(d*4.5));plumeGroup.add(dia);shockDiamonds.push(dia);
}

// アフターバーナー光るプラズマ噴射粒子システム (Spark Particles)
const sparkCount=150,sparkGeo=new THREE.BufferGeometry();
const sparkPos=new Float32Array(sparkCount*3);
for(let i=0;i<sparkCount*3;i+=3){
    sparkPos[i]=(Math.random()-0.5)*1.5;sparkPos[i+1]=(Math.random()-0.5)*1.5;sparkPos[i+2]=-14.0-Math.random()*45.0;
}
sparkGeo.setAttribute('position',new THREE.BufferAttribute(sparkPos,3));
const sparkParticles=new THREE.Points(sparkGeo,new THREE.PointsMaterial({color:cfg.spark_hex,size:1.8,blending:THREE.AdditiveBlending,transparent:true,opacity:0.8}));
vesselGroup.add(sparkParticles);

// =========================================================================
// 🌌 ハイパースペース・光速ワープトンネル ＆ 目的宙域
// =========================================================================
const warpTunnelGroup=new THREE.Group();scene.add(warpTunnelGroup);
const warpStreakCount=800,warpStreakGeo=new THREE.BufferGeometry();
const streakPos=new Float32Array(warpStreakCount*6);
for(let i=0;i<warpStreakCount;i++){
    const ang=Math.random()*Math.PI*2;
    const r=Math.random()*60+16;
    const z=(Math.random()-0.5)*400;
    const len=Math.random()*35+15;
    streakPos[i*6]=Math.cos(ang)*r;streakPos[i*6+1]=Math.sin(ang)*r;streakPos[i*6+2]=z;
    streakPos[i*6+3]=Math.cos(ang)*r;streakPos[i*6+4]=Math.sin(ang)*r;streakPos[i*6+5]=z+len;
}
warpStreakGeo.setAttribute('position',new THREE.BufferAttribute(streakPos,3));
const warpStreakLines=new THREE.LineSegments(warpStreakGeo,new THREE.LineBasicMaterial({color:cfg.warp_halo_hex,blending:THREE.AdditiveBlending,transparent:true,opacity:0.0}));
warpTunnelGroup.add(warpStreakLines);

const starGeo=new THREE.BufferGeometry(),starCount=3000;
const starPos=new Float32Array(starCount*3);
for(let i=0;i<starCount*3;i+=3){
    starPos[i]=(Math.random()-0.5)*20000;starPos[i+1]=(Math.random()-0.5)*20000;starPos[i+2]=(Math.random()-0.5)*32000;
}
starGeo.setAttribute('position',new THREE.BufferAttribute(starPos,3));
const starPoints=new THREE.Points(starGeo,new THREE.PointsMaterial({color:0xffffff,size:2.8,transparent:true,opacity:0.85}));
scene.add(starPoints);

const destGroup=new THREE.Group();destGroup.position.set(0,0,16500);scene.add(destGroup);
const planetMesh=new THREE.Mesh(new THREE.SphereGeometry(1200,48,48),new THREE.MeshStandardMaterial({color:cfg.dest_color,roughness:0.85}));
destGroup.add(planetMesh);
if(cfg.dest_type==='saturn'){
    const ringMesh=new THREE.Mesh(new THREE.RingGeometry(1400,2400,64),new THREE.MeshStandardMaterial({color:0xa8a29e,side:THREE.DoubleSide}));
    ringMesh.rotation.x=Math.PI/2.3;destGroup.add(ringMesh);
}
const catchGate=new THREE.Mesh(new THREE.TorusGeometry(48,3.2,24,48),new THREE.MeshStandardMaterial({color:0x38bdf8,metalness:0.95,roughness:0.2}));
catchGate.position.set(0,0,-1600);destGroup.add(catchGate);

const catchField=new THREE.Mesh(
    new THREE.CircleGeometry(47,32),
    new THREE.MeshBasicMaterial({color:0x38bdf8,transparent:true,opacity:0.0,blending:THREE.AdditiveBlending,side:THREE.DoubleSide})
);
catchField.position.set(0,0,-1600);destGroup.add(catchField);
destGroup.visible=false;

// =========================================================================
// 🎬 決定版アニメーションループ (Lerp補間・OrbitControls・CAM02自動切替)
// =========================================================================
const tStart=performance.now();let isEnded=false;

// カメラ初期配置（引きの美しいワイドビュー：x:-85, y:42, z:-135）
cameraMain.position.set(-85.0,42.0,-135.0);

function animate(now){
    if(isEnded)return;requestAnimationFrame(animate);
    const elapsed=(now-tStart)/1000.0;
    const simT=cfg.is_preview?-5.0:(-5.0+elapsed*1.8);

    let idx=0;while(idx<data.length-1&&data[idx+1].t<=simT)idx++;
    const p0=data[idx];
    const p1=data[Math.min(data.length-1,idx+1)];
    const timeDelta=p1.t-p0.t;
    const alpha=timeDelta>0.0001?Math.min(1.0,Math.max(0.0,(simT-p0.t)/timeDelta)):0.0;

    const lerpVal=(k)=>THREE.MathUtils.lerp(p0[k],p1[k],alpha);
    const curAlt=lerpVal('alt_km'),curMach=lerpVal('mach'),curVc=lerpVal('vc');
    const curRx=lerpVal('rx'),curRy=lerpVal('ry'),curPitch=lerpVal('pitch_deg');
    const curRing=lerpVal('morph_ring'),curPlasma=lerpVal('plasma_alpha');
    const curProg=lerpVal('progress'),curVapor=lerpVal('vapor_cone');
    const curSabot=lerpVal('purge_sabot'),curBooster=lerpVal('purge_booster'),curFairing=lerpVal('purge_fairing');
    const curFlash=lerpVal('warp_flash'),curWave=lerpVal('warp_ring_wave');

    if(flashOverlay){
        flashOverlay.style.opacity=curFlash>0.05?curFlash.toFixed(2):'0.0';
    }

    if(p0.phase==="RAIL_ACCELERATION"||p0.catapult_active){
        catapultCoils.forEach((cl,i)=>{
            const shift=(now*0.014+i*0.35)%Math.PI;
            cl.material.color.setRGB(0.2+Math.sin(shift)*0.8,0.7+Math.sin(shift)*0.3,1.0);
        });
        if(catapultHum&&actx)catapultHum.gain.setTargetAtTime(0.45,actx.currentTime,0.05);
    }else{
        if(catapultHum&&actx)catapultHum.gain.setTargetAtTime(0.0001,actx.currentTime,0.15);
    }

    slidingDorsalDoors.forEach(sd=>{sd.mesh.position.x=sd.side*(2.2+curRing*3.4);});
    warpRingGroup.position.y=0.5+curRing*3.8;
    warpTorus1.rotation.z+=0.04+curVc*0.3;warpTorus2.rotation.z-=0.03+curVc*0.3;
    ringGlowSprite.material.opacity=curRing*0.75;

    // ワープ衝撃波リング拡大
    if(curWave>0.05){
        warpWaveRing.material.opacity=curWave*0.9;
        const wScale=(1.0-curWave)*45.0+1.0;
        warpWaveRing.scale.set(wScale,wScale,wScale);
    }else{
        warpWaveRing.material.opacity=0.0;
    }

    const blink=Math.sin(now*0.01)>0.8?1.0:0.1;
    strobeLeft.material.color.setRGB(blink,0,0);
    strobeRight.material.color.setRGB(0,blink,0);

    const heatRatio=Math.min(1.0,Math.max(0.0,(lerpVal('temp_k')-300.0)/800.0));
    radiatorMat.emissive.setRGB(heatRatio*1.2,heatRatio*0.4,heatRatio*0.1);
    radiatorMat.emissiveIntensity=heatRatio*2.5;

    if(curSabot>0){
        sabotMeshes.forEach(sm=>{
            sm.mesh.position.x+=sm.side*curSabot*1.5;
            sm.mesh.position.y-=curSabot*1.2;
            sm.mesh.rotation.z+=sm.side*0.03;
        });
    }
    if(curBooster>0){
        boosterMeshes.forEach(bm=>{
            bm.mesh.position.x+=bm.side*curBooster*0.8;
            bm.mesh.position.y-=curBooster*0.6;
            bm.mesh.rotation.z+=bm.side*0.02;
        });
    }
    if(curFairing>0){
        fairingMeshes.forEach(fm=>{
            fm.mesh.position.x+=fm.vx*0.02*curFairing;
            fm.mesh.position.y+=fm.vy*0.02*curFairing;
            fm.mesh.position.z-=curFairing*0.5;
            fm.mesh.rotation.y+=0.05;
        });
    }

    rcsMeshes.forEach(rm=>{rm.material.opacity=p0.rcs_active?(0.5+Math.random()*0.4):0.0;});
    vaporCone.material.opacity=curVapor*0.85;
    laserBeam.visible=p0.laser_active;

    plasmaMat.opacity=curPlasma;
    plumeGroup.visible=p0.engine_active;
    sparkParticles.visible=p0.engine_active;
    if(p0.engine_active){
        const flicker=1.0+(Math.random()-0.5)*0.12;
        coreTorch.scale.set(flicker,flicker*(1.0+curVc*2.0),flicker);
        outerTorch.scale.set(flicker,flicker*(1.0+curVc*2.5),flicker);
        shockDiamonds.forEach((sd,i)=>{sd.scale.setScalar(1.0+Math.sin(now*0.02+i)*0.15);});

        // 噴射スパーク粒子の更新
        const sArr=sparkGeo.attributes.position.array;
        for(let i=0;i<sparkCount*3;i+=3){
            sArr[i+2]-=(1.8+curVc*4.0);
            if(sArr[i+2]<-55.0){
                sArr[i]=(Math.random()-0.5)*1.5;
                sArr[i+1]=(Math.random()-0.5)*1.5;
                sArr[i+2]=-14.0;
            }
        }
        sparkGeo.attributes.position.needsUpdate=true;
    }

    // 機体位置更新
    const prevZ=vesselGroup.position.z;
    if(p0.phase==="RAIL_ACCELERATION"||p0.phase==="HYPERSONIC_CLIMB"||p0.phase==="PRE_FLIGHT"){
        vesselGroup.position.set(curRx,curRy,lerpVal('downrange_km')*0.1);
        vesselGroup.rotation.set(-THREE.MathUtils.degToRad(curPitch),0,0);
        groundGroup.visible=true;
        orbitalEarthGroup.visible=(curAlt>=35.0);
    }else{
        const zProg=curProg*14200.0;
        vesselGroup.position.set(0,curRy,zProg);
        vesselGroup.rotation.set(-THREE.MathUtils.degToRad(curPitch),0,0);
        groundGroup.visible=(curAlt<450.0);
        orbitalEarthGroup.visible=true;
    }
    const deltaZ=vesselGroup.position.z-prevZ;

    // ワープトンネル
    if(p0.phase==="WARP_CRUISE"){
        warpTunnelGroup.visible=true;
        warpStreakLines.material.opacity=Math.min(0.95,curVc*1.3);
        warpTunnelGroup.position.copy(vesselGroup.position);
        warpStreakLines.position.z=(now*0.8*curVc)%80.0;
        destGroup.visible=false;
        if(oscWarp&&actx){
            oscWarp.frequency.setTargetAtTime(550+curVc*1300,actx.currentTime,0.1);
            gainWarp.gain.setTargetAtTime(0.75,actx.currentTime,0.1);
            subBass.gain.setTargetAtTime(0.85,actx.currentTime,0.1);
        }
    }else{
        warpTunnelGroup.visible=false;
        if(gainWarp&&actx){gainWarp.gain.setTargetAtTime(0.0001,actx.currentTime,0.2);subBass.gain.setTargetAtTime(0.0001,actx.currentTime,0.2);}
    }

    if(p0.phase==="DECEL_APPROACH"||p0.phase==="ARRIVED"){
        destGroup.visible=true;
        if(curProg>0.88){
            catchField.material.opacity=Math.min(0.85,(curProg-0.88)*7.0);
        }
    }

    if(p0.phase==="ARRIVED"&&document.getElementById('b-success').style.display!=='block'){
        document.getElementById('b-success').style.display='block';
        setTimeout(()=>{isEnded=true;},4500);
    }

    // ★メインカメラ：OrbitControlsターゲットを機体に自動追尾（自由操作可能）
    controls.target.set(vesselGroup.position.x,vesselGroup.position.y+2.0,vesselGroup.position.z);
    cameraMain.position.z+=deltaZ; // 機体の前進分カメラを連動移動
    controls.update();

    // ★CAM 02：フェーズ自動切替監視カメラ
    if(p0.phase==="PRE_FLIGHT"||p0.phase==="CATAPULT_CHARGE"||p0.phase==="RAIL_ACCELERATION"){
        pipTag.innerText="CAM 02: RAIL SIDE TRACKER";
        cameraPip.position.set(16.0,3.5,vesselGroup.position.z+25.0);
        cameraPip.lookAt(vesselGroup.position);
    }else if(p0.phase==="HYPERSONIC_CLIMB"){
        pipTag.innerText="CAM 02: AFT BOOSTER & EARTH CAM";
        cameraPip.position.set(vesselGroup.position.x+4.5,vesselGroup.position.y+0.8,vesselGroup.position.z+2.0);
        cameraPip.lookAt(vesselGroup.position.x+2.0,vesselGroup.position.y-2.0,vesselGroup.position.z-60.0);
    }else if(p0.phase==="ORBITAL_TRANSFORM"||p0.phase==="WARP_CRUISE"){
        pipTag.innerText="CAM 02: FORWARD HULL & RING MONITOR";
        cameraPip.position.set(vesselGroup.position.x+22.0,vesselGroup.position.y+12.0,vesselGroup.position.z+42.0);
        cameraPip.lookAt(vesselGroup.position.x,vesselGroup.position.y+1.0,vesselGroup.position.z);
    }else{
        pipTag.innerText="CAM 02: GATE APPROACH SENSOR";
        cameraPip.position.set(0,50,14600);
        cameraPip.lookAt(vesselGroup.position);
    }

    // 単一レンダラー画面分割描画
    renderer.setViewport(0,0,winW,winH);
    renderer.setScissor(0,0,winW,winH);
    renderer.setScissorTest(false);
    renderer.render(scene,cameraMain);

    if(pipVisible&&pipBox){
        const pipRect=pipBox.getBoundingClientRect();
        const pLeft=pipRect.left;
        const pBottom=winH-pipRect.bottom;
        const pW=pipRect.width;
        const pH=pipRect.height;

        renderer.setViewport(pLeft,pBottom,pW,pH);
        renderer.setScissor(pLeft,pBottom,pW,pH);
        renderer.setScissorTest(true);
        renderer.render(scene,cameraPip);
    }

    // HUD更新
    document.getElementById('h-phase').innerText=p0.phase;
    document.getElementById('h-alt').innerText=`${curAlt.toFixed(1)} km`;
    document.getElementById('h-speed').innerText=`M ${curMach.toFixed(1)}`;
    document.getElementById('h-stime').innerText=`T+ ${lerpVal('ship_time').toFixed(1)}s`;
    document.getElementById('t-vc').innerText=curVc.toFixed(3);
    document.getElementById('t-dist').innerText=(curProg*100.0).toFixed(1);
    document.getElementById('t-temp').innerText=Math.round(lerpVal('temp_k'));
    const gamma=1.0/Math.sqrt(Math.max(0.001,1.0-Math.min(0.9995,curVc)**2));
    document.getElementById('t-gamma').innerText=gamma.toFixed(2);
}
requestAnimationFrame(animate);
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
  st.success("🎉 **ミッション完全成功**: 海上メガカタパルト射出、サボ分離、球体地球軌道展開、光速ワープ閃光突入、目的宙域アレスティングゲート着艦シーケンスが完璧に完走しました。")

