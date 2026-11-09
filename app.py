import json
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hyper-Drive Architect: Apex WaveRider Pro - Hard SF Apex Edition",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("🛸 Hyper-Drive Architect: Apex WaveRider Pro (Hard SF Apex Edition)")
st.caption(
    "※ 4K級ハードSF：実機モジュール換装SSTO・ショックダイヤモンド・相対論的ドップラー星光・重力レンズワープ・電磁テザー捕獲完全版"
)

# =========================================================================
# 🔬 機体・動力炉・目的地・未来技術データベース
# =========================================================================
VESSEL_DESIGNS = {
    "極超音速ウェイブライダー『ヴァルキリー SSTO』": {
        "id": "waverider_valkyrie",
        "style": "stealth_waverider",
        "catapult_mach": 14.5,
        "desc": "チタン合金フレーム＋傾斜面ステルス多面体。軌道到達後に観音開き装甲が展開し、超伝導デュアルワープリングがせり出す次世代機。",
    },
    "磁気慣性核融合クルーザー『プロメテウス』": {
        "id": "prometheus_cruiser",
        "style": "magnetic_fusion",
        "catapult_mach": 11.0,
        "desc": "船尾に巨大なオープンフレーム露出トラス、球形He3燃料タンク、ソレノイド支柱を配置した重工業ディープスペース巡航艦。",
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
        "metalness": 0.25,
        "roughness": 0.85,
        "plasma_hex": 0xD946EF,  # 紫プラズマ
        "desc": "電波反射を抑える無光沢カーボンナノチューブ層。大気圏突破時のプラズマは高エネルギー紫色。",
    },
    "鏡面クローム電磁反射装甲 (Mirror Electrum Plate)": {
        "metalness": 0.98,
        "roughness": 0.12,
        "plasma_hex": 0x38BDF8,  # 青白プラズマ
        "desc": "超高圧鏡面加工合金。地上光や星光をシャープに反射し、青白いアブレーション光を纏う。",
    },
    "液体金属アブレーション装甲 (Liquid Metallic Ablative)": {
        "metalness": 0.70,
        "roughness": 0.38,
        "plasma_hex": 0x10B981,  # エメラルドプラズマ
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
    "夜明け (マジックアワー / 富士朝焼け)": {
        "sky_top": "#030712",
        "sky_mid": "#1e3a8a",
        "sky_bot": "#f97316",
        "sun_color": 0xFFD8A8,
        "sun_pos": [1500, 700, -800],
        "sun_int": 4.8,
        "fog_color": 0x1E293B,
        "fog_density": 0.000035,
    },
    "深夜 (ネオンサーチライト＆星彩)": {
        "sky_top": "#010206",
        "sky_mid": "#040b17",
        "sky_bot": "#0a192f",
        "sun_color": 0x64748B,
        "sun_pos": [-400, 2500, -1200],
        "sun_int": 1.2,
        "fog_color": 0x050C16,
        "fog_density": 0.000045,
    },
    "荒天・雷鳴成層圏突破 (Storm Thunder)": {
        "sky_top": "#050811",
        "sky_mid": "#0e1a2b",
        "sky_bot": "#1a2a40",
        "sun_color": 0x93C5FD,
        "sun_pos": [200, 1800, 300],
        "sun_int": 2.2,
        "fog_color": 0x111D30,
        "fog_density": 0.000065,
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
    "🛸 機体設計 & 航空宇宙マテリアル",
    "🛡️ 外装装甲 & 補助装備モジュール",
    "⚡ 地上射出 & 大気環境",
    "🌌 時空駆動炉 & ワープトポロジー",
    "🎯 目的地航路 & カメラワーク",
])

with tab1:
  col1, col2 = st.columns(2)
  with col1:
    vessel_sel = st.selectbox("ベース艦種 (Chassis)", list(VESSEL_DESIGNS.keys()))
    vessel_cfg = VESSEL_DESIGNS[vessel_sel]
    hull_primary = st.color_picker("メイン構造体プライマリ配色", "#1e293b")
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
    wireframe_facet = st.checkbox(
        "ステルス・ファセット（鋭角カット多面体強調）", value=True
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
    flip_ratio = st.slider(
        "反転逆噴射 (フリップ＆バーン) 開始位置比率",
        0.55,
        0.90,
        0.75,
        step=0.01,
    )
  with col2:
    cam_mode = st.radio(
        "カメラワーク・プリセット",
        [
            "シネマティック追尾 (手ブレ・動的FOV)",
            "フライバイ通過 (マッハ突破・ワープ突入臨場感)",
            "コックピット主観視点 (HUD密着)",
        ],
        index=0,
    )


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
        "purge_booster": 0.0,
        "purge_fairing": 0.0,
        "rcs_active": False,
        "warp_tunnel": 0.0,
        "plasma_alpha": 0.0,
        "space_ratio": 0.0,
        "progress": 0.0,
        "ship_time": 0.0,
        "earth_time": 0.0,
        "engine_active": False,
        "catapult_active": False,
        "laser_active": False,
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
        "purge_booster": 0.0,
        "purge_fairing": 0.0,
        "rcs_active": False,
        "warp_tunnel": 0.0,
        "plasma_alpha": 0.0,
        "space_ratio": 0.0,
        "progress": 0.0,
        "ship_time": 0.0,
        "earth_time": 0.0,
        "engine_active": False,
        "catapult_active": bool(t_cd >= -3.0),
        "laser_active": False,
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
  purge_b = 0.0
  purge_f = 0.0

  for step in range(total_sim_steps):
    t = float(step * dt)
    rcs_on = False
    laser_on = False

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
      warp_tun = 0.0
      space_r = float(np.clip((cur_alt - 15.0) / 75.0, 0.0, 1.0))
      pitch_deg = float(catapult_cfg["angle_deg"] * (1.0 - space_r * 0.7))
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
      warp_tun = 0.0
      space_r = 1.0
      cur_g = 1.0
      cur_vc = 0.03
      cur_progress += 0.005
      pitch_deg = 0.0
      rcs_on = True
    elif cur_progress < flip_ratio:
      phase = "WARP_CRUISE"
      eng_on = True
      target_vc = min(0.996, 0.20 + (warp_curvature / 10.0) * 0.79)
      cur_vc = min(target_vc, cur_vc + 0.12 * dt)
      cur_g = 1.8
      plasma = 0.0
      morph_ring = 1.0
      morph_wings = 1.0
      warp_tun = float(min(1.0, cur_vc * 1.2))
      space_r = 1.0
      cur_progress += (cur_vc * 0.018) * dt
      pitch_deg = 0.0
      laser_on = debris_laser
    else:
      phase = "DECEL_APPROACH"
      eng_on = True
      rem_dist = max(0.0001, 1.0 - cur_progress)
      cur_vc = max(0.008, min(cur_vc, rem_dist * 2.6))
      cur_g = 3.6
      plasma = 0.0
      morph_ring = max(0.2, cur_vc * 1.4)
      morph_wings = 1.0
      warp_tun = float(cur_vc)
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
        "purge_booster": float(purge_b),
        "purge_fairing": float(purge_f),
        "rcs_active": rcs_on,
        "warp_tunnel": float(warp_tun),
        "plasma_alpha": float(plasma),
        "space_ratio": float(space_r),
        "progress": float(min(1.0, cur_progress)),
        "ship_time": float(ship_t),
        "earth_time": float(earth_t),
        "engine_active": eng_on,
        "catapult_active": False,
        "laser_active": laser_on,
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
            "purge_booster": float(purge_b),
            "purge_fairing": float(purge_f),
            "rcs_active": False,
            "warp_tunnel": 0.0,
            "plasma_alpha": 0.0,
            "space_ratio": 1.0,
            "progress": 1.0,
            "ship_time": float(ship_t),
            "earth_time": float(earth_t),
            "engine_active": False,
            "catapult_active": False,
            "laser_active": False,
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
    "wireframe_facet": wireframe_facet,
    "shock_diamonds": shock_diamonds,
    "cam_mode": cam_mode,
    "catapult_angle": catapult_cfg["angle_deg"],
    "catapult_len": catapult_cfg["rail_len"],
    "env": env_cfg,
}

sim_json = json.dumps(sim_records)
cfg_json = json.dumps(client_config)

# =========================================================================
# 📺 Three.js + Web Audio 完全魔改造描画テンプレート
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
.crosshair{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);pointer-events:none;z-index:25;opacity:0.35;}
</style></head>
<body>
<canvas id="canvas-main"></canvas>
<div id="pip-box" class="pip-container" title="クリックでCAM 02の表示/非表示を切り替え">
    <canvas id="canvas-pip"></canvas>
    <div id="pip-tag" class="pip-tag">CAM 02: TRACKING SENSOR</div>
    <div id="pip-hint" class="pip-hint">[CLICK TO TOGGLE]</div>
</div>
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

// レンダラー設定 (ACESFilmic + PBRトーン)
const rendererMain=new THREE.WebGLRenderer({canvas:cMain,antialias:true,powerPreference:"high-performance"});
rendererMain.setPixelRatio(Math.min(window.devicePixelRatio,1.5));rendererMain.setSize(wMain,hMain);
rendererMain.toneMapping=THREE.ACESFilmicToneMapping;rendererMain.toneMappingExposure=1.35;

const rendererPip=new THREE.WebGLRenderer({canvas:cPip,antialias:true});
rendererPip.setPixelRatio(1.0);rendererPip.setSize(410,235);
rendererPip.toneMapping=THREE.ACESFilmicToneMapping;

const scene=new THREE.Scene();
scene.fog=new THREE.FogExp2(cfg.env.fog_color,cfg.env.fog_density);

// ★変数名バグを完全解消 (cameraMain / cameraPip で統一)
const cameraMain=new THREE.PerspectiveCamera(35,wMain/hMain,0.5,100000);
const cameraPip=new THREE.PerspectiveCamera(22,410/235,1.0,100000);

const sunLight=new THREE.DirectionalLight(cfg.env.sun_color,cfg.env.sun_int);
sunLight.position.set(cfg.env.sun_pos[0],cfg.env.sun_pos[1],cfg.env.sun_pos[2]);scene.add(sunLight);
scene.add(new THREE.AmbientLight(0x1e293b,1.5));

// --- Web Audio SF音響シンセシス ---
const AudioCtx=window.AudioContext||window.webkitAudioContext;let actx=null,oscWarp=null,gainWarp=null,subBass=null,catapultHum=null,rcsNoise=null,rcsGain=null;
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

        // RCSホワイトノイズ
        const bSize=actx.sampleRate*2;const b=actx.createBuffer(1,bSize,actx.sampleRate);const out=b.getChannelData(0);
        for(let i=0;i<bSize;i++)out[i]=(Math.random()*2-1)*0.4;
        const wNode=actx.createBufferSource();wNode.buffer=b;wNode.loop=true;
        const hpf=actx.createBiquadFilter();hpf.type='highpass';hpf.frequency.value=1200;
        rcsGain=actx.createGain();rcsGain.gain.value=0.0001;
        wNode.connect(hpf);hpf.connect(rcsGain);rcsGain.connect(actx.destination);wNode.start(0);
    }
    if(actx.state==='suspended')actx.resume();
}
window.addEventListener('click',initSFX,{once:true});

// --- PBR環境マップ＆先進リベット・コーションテクスチャ ---
function createEnvMap(){
    const cvs=document.createElement('canvas');cvs.width=512;cvs.height=256;const ctx=cvs.getContext('2d');
    const g=ctx.createLinearGradient(0,0,0,256);
    g.addColorStop(0,cfg.env.sky_top);g.addColorStop(0.4,cfg.env.sky_mid);g.addColorStop(0.7,cfg.env.sky_bot);g.addColorStop(1,'#020b18');
    ctx.fillStyle=g;ctx.fillRect(0,0,512,256);
    return new THREE.CanvasTexture(cvs);
}
const envMapTex=createEnvMap();envMapTex.mapping=THREE.EquirectangularReflectionMapping;scene.environment=envMapTex;

function createAdvancedArmorTex(){
    const cvs=document.createElement('canvas');cvs.width=1024;cvs.height=1024;const ctx=cvs.getContext('2d');
    ctx.fillStyle='#0f172a';ctx.fillRect(0,0,1024,1024);
    // パネルライン
    ctx.strokeStyle='#1e293b';ctx.lineWidth=2;
    for(let x=0;x<1024;x+=48){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,1024);ctx.stroke();}
    for(let y=0;y<1024;y+=48){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(1024,y);ctx.stroke();}
    // リベット
    ctx.fillStyle='#334155';
    for(let x=24;x<1024;x+=48){for(let y=24;y<1024;y+=48){ctx.fillRect(x-1,y-1,2,2);}}
    // コーションマーク＆スリット
    ctx.fillStyle='#f59e0b';
    ctx.fillRect(100,200,60,6);ctx.fillRect(400,600,60,6);ctx.fillRect(800,300,60,6);
    ctx.fillStyle='#ef4444';
    ctx.fillRect(110,208,40,4);ctx.fillRect(410,608,40,4);
    return new THREE.CanvasTexture(cvs);
}
const armorTex=createAdvancedArmorTex();armorTex.wrapS=THREE.RepeatWrapping;armorTex.wrapT=THREE.RepeatWrapping;armorTex.repeat.set(6,6);

// 先進マテリアル定義
const armorMat=new THREE.MeshStandardMaterial({
    color:cfg.hull_color,
    roughness:cfg.armor_roughness,
    metalness:cfg.armor_metalness,
    bumpMap:armorTex,
    bumpScale:0.03,
    flatShading:cfg.wireframe_facet
});
const carbonTileMat=new THREE.MeshStandardMaterial({color:cfg.tile_color,roughness:0.8,metalness:0.2,bumpMap:armorTex,bumpScale:0.04});
const goldFoilMat=new THREE.MeshStandardMaterial({color:0xd97706,roughness:0.35,metalness:0.95});
const pipeMat=new THREE.MeshStandardMaterial({color:0x94a3b8,roughness:0.25,metalness:0.95});
const canopyMat=new THREE.MeshPhysicalMaterial({color:0x38bdf8,roughness:0.08,metalness:0.92,transparent:true,opacity:0.85,transmission:0.7});
const coilGlowMat=new THREE.MeshBasicMaterial({color:0x38bdf8});
const plasmaMat=new THREE.MeshBasicMaterial({color:cfg.plasma_hex,transparent:true,opacity:0.0,blending:THREE.AdditiveBlending,side:THREE.DoubleSide});
const laserMat=new THREE.MeshBasicMaterial({color:0x38bdf8,blending:THREE.AdditiveBlending});

// ラジエーターフィン（排熱発光用）
const radiatorMat=new THREE.MeshStandardMaterial({color:0x1e293b,metalness:0.9,roughness:0.2,emissive:0x000000,emissiveIntensity:0.0});

// 地上・富士山・海・カタパルト
const groundGroup=new THREE.Group();scene.add(groundGroup);
const ocean=new THREE.Mesh(new THREE.PlaneGeometry(60000,60000),new THREE.MeshStandardMaterial({color:0x0c2d48,roughness:0.12,metalness:0.85}));
ocean.rotation.x=-Math.PI/2;groundGroup.add(ocean);

const mtn=new THREE.Mesh(new THREE.ConeGeometry(9200,3400,32),new THREE.MeshStandardMaterial({color:0x1e293b,roughness:0.9}));
mtn.position.set(12000,1700,-18000);groundGroup.add(mtn);
const snowCap=new THREE.Mesh(new THREE.ConeGeometry(3200,1200,32),new THREE.MeshStandardMaterial({color:0xffffff,roughness:0.5}));
snowCap.position.set(12000,2800,-18000);groundGroup.add(snowCap);

const railLen3D=cfg.catapult_len*150.0,catAngleRad=THREE.MathUtils.degToRad(cfg.catapult_angle);
const railGroup=new THREE.Group();groundGroup.add(railGroup);
const railSpine=new THREE.Mesh(new THREE.BoxGeometry(12,8,railLen3D),armorMat);
railSpine.position.set(0,railLen3D*0.5*Math.sin(catAngleRad)+2.0,railLen3D*0.5*Math.cos(catAngleRad));
railSpine.rotation.x=catAngleRad;railGroup.add(railSpine);

const catapultCoils=[];
for(let c=0;c<28;c++){
    const cMesh=new THREE.Mesh(new THREE.TorusGeometry(14,0.7,12,32),coilGlowMat);
    const zDist=(c/28)*railLen3D;
    cMesh.position.set(0,zDist*Math.sin(catAngleRad)+2.0,zDist*Math.cos(catAngleRad));
    cMesh.rotation.x=catAngleRad;railGroup.add(cMesh);catapultCoils.push(cMesh);
}

// 雲海
const cloudGroup=new THREE.Group();groundGroup.add(cloudGroup);
const cloudGeo=new THREE.PlaneGeometry(600,300);
for(let ci=0;ci<45;ci++){
    const cp=new THREE.Mesh(cloudGeo,new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0.32,depthWrite:false}));
    cp.rotation.x=-Math.PI/2;cp.position.set((Math.random()-0.5)*38000,1350,(Math.random()-0.5)*38000);
    cloudGroup.add(cp);
}

// --- 相対論的星々 (ドップラーシフト星光) ---
const starGeo=new THREE.BufferGeometry(),starCount=3500;
const starPos=new Float32Array(starCount*3);
const starColors=new Float32Array(starCount*3);
for(let i=0;i<starCount*3;i+=3){
    starPos[i]=(Math.random()-0.5)*18000;starPos[i+1]=(Math.random()-0.5)*18000;starPos[i+2]=(Math.random()-0.5)*32000;
    starColors[i]=1.0;starColors[i+1]=1.0;starColors[i+2]=1.0;
}
starGeo.setAttribute('position',new THREE.BufferAttribute(starPos,3));
starGeo.setAttribute('color',new THREE.BufferAttribute(starColors,3));
const starPoints=new THREE.Points(starGeo,new THREE.PointsMaterial({size:3.2,vertexColors:true,transparent:true,opacity:0.85}));
scene.add(starPoints);

// --- 先進宇宙船モジュール設計 (3船種固有ジオメトリ) ---
const vesselGroup=new THREE.Group();scene.add(vesselGroup);
const slidingDorsalDoors=[],warpRingGroup=new THREE.Group();
const radiatorMeshes=[],boosterMeshes=[],fairingMeshes=[];

// 翼のExtrude化 (鋭角ステルス断面厚み)
function createSharpWing(span){
    const s=new THREE.Shape();s.moveTo(0,5);s.lineTo(span*0.5,-5);s.lineTo(span*0.48,-9);s.lineTo(0,-13);s.closePath();
    const g=new THREE.ExtrudeGeometry(s,{depth:0.45,bevelEnabled:true,bevelThickness:0.18,bevelSize:0.7,bevelSegments:2});
    const m=new THREE.Mesh(g,armorMat);m.rotation.x=Math.PI/2;m.position.y=-0.2;return m;
}

// 船種別分岐ビルド
if(cfg.style==="stealth_waverider"){
    // ヴァルキリー：多面体ファセットボディ＋前進カナード＋デルタ
    const bGeo=new THREE.CylinderGeometry(1.2,4.8,26,8);bGeo.scale(1.8,0.45,1.0);
    const body=new THREE.Mesh(bGeo,armorMat);body.rotation.x=Math.PI/2;vesselGroup.add(body);
    const heatBelly=new THREE.Mesh(bGeo,carbonTileMat);heatBelly.position.y=-0.15;heatBelly.scale.set(1.02,1.02,1.02);vesselGroup.add(heatBelly);
    vesselGroup.add(createSharpWing(cfg.wings_span));

    // カナード翼
    const canard=new THREE.Mesh(new THREE.BoxGeometry(cfg.wings_span*0.35,0.15,2.2),armorMat);canard.position.set(0,0.2,7.0);vesselGroup.add(canard);

    for(let side of [-1,1]){
        const vTail=new THREE.Mesh(new THREE.BoxGeometry(0.2,4.2,5.5),armorMat);vTail.position.set(side*3.2,2.0,-11.0);vTail.rotation.z=side*0.25;vesselGroup.add(vTail);
        const door=new THREE.Mesh(new THREE.BoxGeometry(3.6,0.35,12),armorMat);door.position.set(side*2.2,1.2,-2.0);vesselGroup.add(door);
        slidingDorsalDoors.push({mesh:door,side:side});
    }
}else if(cfg.style==="magnetic_fusion"){
    // プロメテウス：船尾オープンフレームトラス＋球形燃料タンク群＋太配管
    const frontCab=new THREE.Mesh(new THREE.ConeGeometry(3.2,14,8),armorMat);frontCab.rotation.x=Math.PI/2;frontCab.position.z=7;vesselGroup.add(frontCab);
    const midHull=new THREE.Mesh(new THREE.BoxGeometry(6,5,16),armorMat);vesselGroup.add(midHull);

    // むき出しオープンフレームトラス
    const trussGroup=new THREE.Group();trussGroup.position.set(0,0,-12);vesselGroup.add(trussGroup);
    const tFrame=new THREE.Mesh(new THREE.BoxGeometry(7,5.5,12),new THREE.MeshStandardMaterial({color:0x475569,wireframe:true}));trussGroup.add(tFrame);

    // 球形He3タンク4基
    for(let i=0;i<4;i++){
        const ang=(i/4)*Math.PI*2;
        const tank=new THREE.Mesh(new THREE.SphereGeometry(1.6,16,16),goldFoilMat);
        tank.position.set(Math.cos(ang)*2.4,Math.sin(ang)*1.8,-11);vesselGroup.add(tank);
    }
    vesselGroup.add(createSharpWing(cfg.wings_span*0.75));
}else{
    // ロンギヌス：超長クサビ＋爆砕パージフェアリング
    const coreSpike=new THREE.Mesh(new THREE.CylinderGeometry(0.6,2.2,34,6),goldFoilMat);coreSpike.rotation.x=Math.PI/2;vesselGroup.add(coreSpike);
    vesselGroup.add(createSharpWing(cfg.wings_span*0.5));

    // パージ用4面フェアリング
    for(let f=0;f<4;f++){
        const ang=(f/4)*Math.PI*2;
        const fairing=new THREE.Mesh(new THREE.BoxGeometry(2.0,0.3,16),armorMat);
        fairing.position.set(Math.cos(ang)*1.4,Math.sin(ang)*1.4,4);
        fairing.rotation.z=ang;vesselGroup.add(fairing);
        fairingMeshes.push({mesh:fairing,vx:Math.cos(ang)*14.0,vy:Math.sin(ang)*14.0});
    }
}

// コックピットキャノピー
const canopy=new THREE.Mesh(new THREE.ConeGeometry(1.3,6.5,16),canopyMat);canopy.scale.set(1.0,0.45,1.8);canopy.rotation.x=Math.PI/2;canopy.position.set(0,0.8,8.0);vesselGroup.add(canopy);

// 放熱ラジエーターフィン（UIで選択した枚数を展開配置）
for(let r=0;r<cfg.radiator_count;r++){
    const rad=new THREE.Mesh(new THREE.BoxGeometry(3.8,0.06,1.4),radiatorMat);
    rad.position.set(0,0.9,-4.0-(r*1.8));vesselGroup.add(rad);
    radiatorMeshes.push(rad);
}

// 外装使い捨てブースター×2
if(cfg.aux_booster){
    for(let bSide of [-1,1]){
        const bMesh=new THREE.Mesh(new THREE.CylinderGeometry(0.8,0.9,14,12),carbonTileMat);
        bMesh.position.set(bSide*(cfg.wings_span*0.35),-0.6,-5);bMesh.rotation.x=Math.PI/2;vesselGroup.add(bMesh);
        boosterMeshes.push({mesh:bMesh,side:bSide});
    }
}

// ワープリング (デュアル超伝導)
warpRingGroup.position.set(0,0.5,-2.0);vesselGroup.add(warpRingGroup);
const warpTorus1=new THREE.Mesh(new THREE.TorusGeometry(5.6,0.4,16,48),coilGlowMat);warpRingGroup.add(warpTorus1);
const warpTorus2=new THREE.Mesh(new THREE.TorusGeometry(6.4,0.3,16,48),armorMat);warpRingGroup.add(warpTorus2);

// アルクビエレ・重力レンズワープバブル
const warpBubble=new THREE.Mesh(
    new THREE.SphereGeometry(18,32,32),
    new THREE.MeshBasicMaterial({color:cfg.warp_halo_hex,wireframe:true,transparent:true,opacity:0.0,blending:THREE.AdditiveBlending})
);
vesselGroup.add(warpBubble);

// デブリ排除レーザー
const laserBeam=new THREE.Mesh(new THREE.CylinderGeometry(0.08,0.08,240,8),laserMat);
laserBeam.position.set(0,0,128);laserBeam.rotation.x=Math.PI/2;laserBeam.visible=false;vesselGroup.add(laserBeam);

// プラズマシェル
const plasmaShell=new THREE.Mesh(new THREE.ConeGeometry(7.8,38,16,1,true),plasmaMat);
plasmaShell.position.z=-4;plasmaShell.rotation.x=-Math.PI/2;vesselGroup.add(plasmaShell);

// RCSスラスター噴射煙（クアッド）
const rcsMeshes=[];
for(let s=0;s<4;s++){
    const ang=(s/4)*Math.PI*2;
    const rCone=new THREE.Mesh(new THREE.ConeGeometry(0.4,2.5,8),new THREE.MeshBasicMaterial({color:0xffffff,transparent:true,opacity:0.0}));
    rCone.position.set(Math.cos(ang)*2.6,Math.sin(ang)*1.2,6.0);rCone.rotation.z=ang+Math.PI/2;
    vesselGroup.add(rCone);rcsMeshes.push(rCone);
}

// 多層ショックダイヤモンド付き推進炎
const plumeGroup=new THREE.Group();plumeGroup.position.set(0,0,-15);vesselGroup.add(plumeGroup);
const coreTorch=new THREE.Mesh(new THREE.ConeGeometry(2.4,24,16,1,true),new THREE.MeshBasicMaterial({color:0xffffff,blending:THREE.AdditiveBlending}));
coreTorch.rotation.x=Math.PI/2;coreTorch.position.z=-12;plumeGroup.add(coreTorch);
const outerTorch=new THREE.Mesh(new THREE.ConeGeometry(3.8,32,16,1,true),new THREE.MeshBasicMaterial({color:cfg.flame_hex,transparent:true,opacity:0.8,blending:THREE.AdditiveBlending}));
outerTorch.rotation.x=Math.PI/2;outerTorch.position.z=-16;plumeGroup.add(outerTorch);

// ショックダイヤモンド円盤群
const shockDiamonds=[];
for(let d=0;d<cfg.shock_diamonds;d++){
    const dia=new THREE.Mesh(new THREE.RingGeometry(0.2,1.8-(d*0.25),16),new THREE.MeshBasicMaterial({color:cfg.spark_hex,side:THREE.DoubleSide,blending:THREE.AdditiveBlending}));
    dia.position.set(0,0,-4.0-(d*4.5));plumeGroup.add(dia);shockDiamonds.push(dia);
}

// 目的地惑星 ＆ 電磁テザー減速ゲート
const destGroup=new THREE.Group();destGroup.position.set(0,0,16500);scene.add(destGroup);
const planetMesh=new THREE.Mesh(new THREE.SphereGeometry(1200,48,48),new THREE.MeshStandardMaterial({color:cfg.dest_color,roughness:0.85}));
destGroup.add(planetMesh);
if(cfg.dest_type==='saturn'){
    const ringMesh=new THREE.Mesh(new THREE.RingGeometry(1400,2400,64),new THREE.MeshStandardMaterial({color:0xa8a29e,side:THREE.DoubleSide}));
    ringMesh.rotation.x=Math.PI/2.3;destGroup.add(ringMesh);
}
const catchGate=new THREE.Mesh(new THREE.TorusGeometry(48,3.2,16,48),new THREE.MeshStandardMaterial({color:0x38bdf8,metalness:0.95,roughness:0.2}));
catchGate.position.set(0,0,-1600);destGroup.add(catchGate);

// 電磁テザー光線（青白いアーク線3本）
const tetherGroup=new THREE.Group();destGroup.add(tetherGroup);
const tetherLines=[];
for(let t=0;t<3;t++){
    const tGeo=new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0,0,-1600),new THREE.Vector3(0,0,-1600)]);
    const tLine=new THREE.Line(tGeo,new THREE.LineBasicMaterial({color:0x38bdf8,linewidth:2}));
    tetherGroup.add(tLine);tetherLines.push(tLine);
}

// --- アニメーションループ ---
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
            const shift=(now*0.014+i*0.35)%Math.PI;
            cl.material.color.setRGB(0.2+Math.sin(shift)*0.8,0.7+Math.sin(shift)*0.3,1.0);
        });
        if(catapultHum&&actx)catapultHum.gain.setTargetAtTime(0.45,actx.currentTime,0.05);
    }else{
        if(catapultHum&&actx)catapultHum.gain.setTargetAtTime(0.0001,actx.currentTime,0.15);
    }

    // メカ変形 & ラジエーター排熱発光
    slidingDorsalDoors.forEach(sd=>{sd.mesh.position.x=sd.side*(2.2+p.morph_ring*3.4);});
    warpRingGroup.position.y=0.5+p.morph_ring*3.8;
    warpTorus1.rotation.z+=0.04+p.vc*0.3;warpTorus2.rotation.z-=0.03+p.vc*0.3;

    // ラジエーター温度連動 (赤熱〜白熱発光)
    const heatRatio=Math.min(1.0,Math.max(0.0,(p.temp_k-300.0)/800.0));
    radiatorMat.emissive.setRGB(heatRatio*1.2,heatRatio*0.4,heatRatio*0.1);
    radiatorMat.emissiveIntensity=heatRatio*2.5;

    // ブースターパージ
    if(p.purge_booster>0){
        boosterMeshes.forEach(bm=>{
            bm.mesh.position.x+=bm.side*p.purge_booster*0.8;
            bm.mesh.position.y-=p.purge_booster*0.6;
            bm.mesh.rotation.z+=bm.side*0.02;
        });
    }
    // フェアリング爆砕パージ
    if(p.purge_fairing>0){
        fairingMeshes.forEach(fm=>{
            fm.mesh.position.x+=fm.vx*0.02*p.purge_fairing;
            fm.mesh.position.y+=fm.vy*0.02*p.purge_fairing;
            fm.mesh.position.z-=p.purge_fairing*0.5;
            fm.mesh.rotation.y+=0.05;
        });
    }

    // RCS噴射
    rcsMeshes.forEach(rm=>{rm.material.opacity=p.rcs_active?(0.5+Math.random()*0.4):0.0;});
    if(rcsGain&&actx)rcsGain.gain.setTargetAtTime(p.rcs_active?0.3:0.0001,actx.currentTime,0.05);

    // デブリ排除レーザー
    laserBeam.visible=p.laser_active;
    if(p.laser_active){laserBeam.scale.y=1.0+Math.random()*0.2;}

    // プラズマ＆エンジン炎
    plasmaMat.opacity=p.plasma_alpha;
    plumeGroup.visible=p.engine_active;
    if(p.engine_active){
        const flicker=1.0+(Math.random()-0.5)*0.15;
        coreTorch.scale.set(flicker,flicker*(1.0+p.vc*2.0),flicker);
        outerTorch.scale.set(flicker,flicker*(1.0+p.vc*2.5),flicker);
        shockDiamonds.forEach((sd,i)=>{sd.scale.setScalar(1.0+Math.sin(now*0.02+i)*0.15);});
    }

    // 位置更新
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

    // ドップラー星光＆アルクビエレ・重力レンズ
    if(p.phase==="WARP_CRUISE"){
        warpBubble.material.opacity=p.vc*0.75;
        warpBubble.rotation.z+=0.02;warpBubble.rotation.y+=0.01;
        // 星々のドップラー色偏移（前方は青白くブルーシフト、星光ストレッチ）
        const colors=starGeo.attributes.color.array;
        for(let i=0;i<starCount*3;i+=3){
            colors[i]=Math.max(0.2,1.0-p.vc*0.8);      // R抑制
            colors[i+1]=Math.min(1.0,0.8+p.vc*0.2);   // G
            colors[i+2]=1.0;                           // B最大化 (超高エネルギー青白)
        }
        starGeo.attributes.color.needsUpdate=true;
        if(oscWarp&&actx){
            oscWarp.frequency.setTargetAtTime(550+p.vc*1300,actx.currentTime,0.1);
            gainWarp.gain.setTargetAtTime(0.75,actx.currentTime,0.1);
            subBass.gain.setTargetAtTime(0.85,actx.currentTime,0.1);
        }
    }else{
        warpBubble.material.opacity=0.0;
        if(gainWarp&&actx){gainWarp.gain.setTargetAtTime(0.0001,actx.currentTime,0.2);subBass.gain.setTargetAtTime(0.0001,actx.currentTime,0.2);}
    }

    // 電磁テザー捕獲アーク光線 (DECEL & ARRIVED)
    if(p.phase==="DECEL_APPROACH"&&p.progress>0.92){
        tetherGroup.visible=true;
        const vPosLocal=tetherGroup.worldToLocal(vesselGroup.position.clone());
        tetherLines.forEach((tl,idx)=>{
            const offsetAng=(idx/3)*Math.PI*2+now*0.01;
            const ringPos=new THREE.Vector3(Math.cos(offsetAng)*48,Math.sin(offsetAng)*48,-1600);
            const jitter=new THREE.Vector3((Math.random()-0.5)*2,(Math.random()-0.5)*2,(Math.random()-0.5)*2);
            tl.geometry.setFromPoints([ringPos,vPosLocal.clone().add(jitter)]);
        });
    }else{
        tetherGroup.visible=false;
    }

    if(p.phase==="ARRIVED"&&document.getElementById('b-success').style.display!=='block'){
        document.getElementById('b-success').style.display='block';
        setTimeout(()=>{isEnded=true;},4500);
    }

    // ★カメラワーク・プリセット分岐 (cameraMain で統一)
    if(cfg.cam_mode==="フライバイ通過 (マッハ突破・ワープ突入臨場感)"){
        cameraMain.fov=50;
        if(p.phase==="RAIL_ACCELERATION"){
            cameraMain.position.set(24.0,18.0,vesselGroup.position.z+40.0);
        }else if(p.phase==="WARP_CRUISE"){
            cameraMain.position.set(-30.0,8.0,vesselGroup.position.z+80.0);
        }else{
            cameraMain.position.set(40.0,20.0,vesselGroup.position.z-60.0);
        }
        cameraMain.lookAt(vesselGroup.position);
    }else if(cfg.cam_mode==="コックピット主観視点 (HUD密着)"){
        cameraMain.fov=75;
        cameraMain.position.set(vesselGroup.position.x,vesselGroup.position.y+1.2,vesselGroup.position.z+6.5);
        cameraMain.rotation.set(-THREE.MathUtils.degToRad(p.pitch_deg),0,0);
    }else{
        // シネマティック追尾 (手ブレ + 動的FOV)
        const shake=(p.mach>1.0&&p.mach<5.0)?(Math.random()-0.5)*0.35:0.0;
        cameraMain.fov=THREE.MathUtils.lerp(cameraMain.fov,(p.phase==="WARP_CRUISE"?85.0:36.0),0.08);
        cameraMain.position.set(vesselGroup.position.x-36.0+shake,vesselGroup.position.y+19.0+shake,vesselGroup.position.z-68.0);
        cameraMain.lookAt(vesselGroup.position.x,vesselGroup.position.y+1.0,vesselGroup.position.z+28.0);
    }
    cameraMain.updateProjectionMatrix();

    // PiPカメラ (CAM 02)
    if(p.phase==="WARP_CRUISE"||p.phase==="DECEL_APPROACH"||p.phase==="ARRIVED"){
        cameraPip.position.set(0,60,14600);cameraPip.lookAt(vesselGroup.position);
    }else{
        cameraPip.position.set(160.0,40.0,240.0);cameraPip.lookAt(vesselGroup.position);
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
    document.getElementById('t-temp').innerText=Math.round(p.temp_k);
    const gamma=1.0/Math.sqrt(Math.max(0.001,1.0-Math.min(0.9995,p.vc)**2));
    document.getElementById('t-gamma').innerText=gamma.toFixed(2);
}
requestAnimationFrame(animate);

window.addEventListener('resize',()=>{
    updatePipPosition();resizePipRenderer();
    const w=window.innerWidth,h=window.innerHeight;
    rendererMain.setSize(w,h);cameraMain.aspect=w/h;cameraMain.updateProjectionMatrix();
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
  st.success("🎉 **ミッション完全成功**: 海上メガカタパルト射出、ラムジェットブースターパージ、軌道上モジュール展開、相対論的ワープ巡航、電磁テザーゲート捕獲シーケンスが設計通り完璧に完走しました。")
