import json
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hyper-Drive Architect: Apex VFX Director's Cut",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("🛸 Hyper-Drive Architect: Apex VFX Director's Cut")
st.caption(
    "※ 完全改修版：ホイール干渉廃止ワイド視点 / 地球の超高速リセッション（後退・消失） / 相模湾メガフロート基地＆富士稜線 / 重力ブラックアウト収縮＆多層オーロラワープ / 氷塊デブリ減速"
)

# =========================================================================
# 🔬 機体・動力炉・目的地・環境データベース
# =========================================================================
VESSEL_DESIGNS = {
    "第6世代極超音速ウェイブライダー『ヴァルキリー SSTO』": {
        "id": "valkyrie",
        "style": "stealth_waverider",
        "catapult_mach": 15.5,
        "desc": "多面体ステルスノーズ、ダイバータレス超音速インテーク、エネルギー脈動コンジット、12枚花弁アイリス可変ノズルを備えた主力SSTO。軌道上で背面4分割ベイが開き、超伝導デュアル・アルクビエレリングがリフトアップする。",
    },
    "重工業・磁気慣性核融合クルーザー『プロメテウス』": {
        "id": "prometheus",
        "style": "magnetic_fusion",
        "catapult_mach": 12.2,
        "desc": "露出型メインボーンフレームに黄金のMLI断熱球形ヘリウム3タンク8基と極太クライオ冷却配管を懸架。船尾に大型磁気ピンチノズルとジャイロ・ソレノイドを備える深宇宙重巡航艇。",
    },
    "電磁カタパルト特化・軌道穿孔槍『ロンギヌス』": {
        "id": "longinus",
        "style": "massdriver_spear",
        "catapult_mach": 19.8,
        "desc": "先鋭化した極細ダイヤモンド断面クサビ型。高高度で外装アブレーション・フェアリング4枚を爆砕パージし、内部の超高密度反物質コアと多連装コイルを露出させる超高速迎撃実験機。",
    },
}

ARMOR_SYSTEMS = {
    "漆黒カーボンナノチューブ電波吸収装甲 (RAM Stealth)": {
        "metalness": 0.45,
        "roughness": 0.48,
        "plasma_hex": 0xD946EF,
    },
    "液体金属クローム・電磁ミラー装甲 (Mirror Electrum)": {
        "metalness": 0.96,
        "roughness": 0.12,
        "plasma_hex": 0x38BDF8,
    },
    "焼結タングステン・セラミック耐熱複合材 (Thermal Grey)": {
        "metalness": 0.68,
        "roughness": 0.32,
        "plasma_hex": 0x10B981,
    },
}

POWER_CORES = {
    "D-He3 超伝導マグネティック・パルス核融合炉": {
        "flame_hex": 0x38BDF8,
        "core_hex": 0xE0F2FE,
        "spark_hex": 0x7DD3FC,
        "aurora_hex": 0x0284C7,
    },
    "Kerr 人工特異点・ホーキング輻射抽出ドライブ": {
        "flame_hex": 0xA855F7,
        "core_hex": 0xF3E8FF,
        "spark_hex": 0xD8B4FE,
        "aurora_hex": 0x7E22CE,
    },
    "陽電子・反陽子消滅ガンマ線光子トーチ": {
        "flame_hex": 0xF43F5E,
        "core_hex": 0xFFE4E6,
        "spark_hex": 0xFDA4AF,
        "aurora_hex": 0xBE123C,
    },
}

DESTINATIONS = {
    "土星リング 氷冠スターゲート『クロノス』": {
        "dist_label": "9.58 AU (1,433,000,000 km)",
        "type": "saturn",
        "color_hex": 0xE2CCB2,
        "band_hex": 0xB89F80,
    },
    "木星 大赤斑上空・軌道エレベーターアンカー『ゼウス』": {
        "dist_label": "4.20 AU (628,000,000 km)",
        "type": "jupiter",
        "color_hex": 0xD97706,
        "band_hex": 0x92400E,
    },
    "火星 オリンポス軌道テラフォーミング・リング": {
        "dist_label": "0.52 AU (78,000,000 km)",
        "type": "mars",
        "color_hex": 0xC2410C,
        "band_hex": 0x7C2D12,
    },
}

LAUNCH_ENVIRONMENTS = {
    "相模湾 第1メガフロート射場 (深夜・ネオン誘導灯＆サーチライト照射)": {
        "mode": "night",
        "angle_deg": 28.0,
        "sun_pos": [-1500, 500, -2500],
        "sun_color": 0x60A5FA,
        "sun_int": 2.4,
        "sky_zenith": "#02050E",
        "sky_horizon": "#0D254C",
        "glow_color": "#1E3A8A",
    },
    "相模湾 第1メガフロート射場 (夜明け・富士シルエット＆マジックアワー)": {
        "mode": "dawn",
        "angle_deg": 28.0,
        "sun_pos": [2200, 450, 2500],
        "sun_color": 0xFFAD60,
        "sun_int": 5.0,
        "sky_zenith": "#040B1A",
        "sky_horizon": "#EA580C",
        "glow_color": "#F97316",
    },
}

# =========================================================================
# 🎛️ カスタマイズUI
# =========================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🛸 機体アーキテクチャ & 精密メカ設定",
    "🏗️ メガフロート基地 & 富士・大気環境",
    "⚡ 動力炉・重力収縮ワープ・物理挙動",
    "🎥 ワイドカメラ & 目的宙域",
])

with tab1:
  c1, c2 = st.columns(2)
  with c1:
    vessel_sel = st.selectbox("ベース艦種 (Chassis)", list(VESSEL_DESIGNS.keys()))
    vessel_cfg = VESSEL_DESIGNS[vessel_sel]
    armor_sel = st.selectbox("外装マテリアルPBR設定", list(ARMOR_SYSTEMS.keys()))
    armor_cfg = ARMOR_SYSTEMS[armor_sel]
    hull_color = st.color_picker("メイン装甲ベースカラー", "#1e293b")
    belly_color = st.color_picker("下部耐熱カーボンタイル配色", "#090d16")
  with c2:
    st.info(f"**構造設計:** {vessel_cfg['desc']}")
    wings_span = st.slider(
        "可変ジオメトリ主翼スパン (m)", 18.0, 40.0, 28.0, step=1.0
    )
    radiator_fins = st.slider("展開式 高温放熱ラジエーターパネル数", 2, 8, 4, step=2)
    aux_boosters = st.checkbox(
        "外装スクラムジェット補助ブースター×2 (高度55kmで分離パージ)",
        value=True,
    )

with tab2:
  c1, c2 = st.columns(2)
  with c1:
    env_sel = st.selectbox("射場ロケーション＆時間帯", list(LAUNCH_ENVIRONMENTS.keys()))
    env_cfg = LAUNCH_ENVIRONMENTS[env_sel]
    coil_charge = st.slider("リニアカタパルト超伝導励磁出力 (%)", 80, 150, 125, step=5)
  with c2:
    st.caption(
        "※ カタパルト両脇の照明クレーン塔・管制ビル・サーチライト光柱、正面奥の富士山と市街地夜景、高度雲海突破を描画します。"
    )
    cryo_steam = st.checkbox("極低温クライオ冷却ベント水蒸気＆発射アーク火花", value=True)
    mach_cone_vfx = st.checkbox("多重マッハコーン＆断熱圧縮プラズマトレイル", value=True)

with tab3:
  c1, c2 = st.columns(2)
  with c1:
    power_sel = st.selectbox("主推進エンジンコア", list(POWER_CORES.keys()))
    power_cfg = POWER_CORES[power_sel]
    shock_count = st.slider("推進炎 ショックダイヤモンド（マッハリング）段数", 3, 7, 5)
  with c2:
    warp_factor = st.slider("アルクビエレ時空曲率 (Warp Factor)", 2.0, 9.9, 9.2, step=0.1)
    flip_timing = st.slider(
        "フリップ＆バーン（180°反転減速）開始地点", 0.60, 0.85, 0.74, step=0.01
    )

with tab4:
  c1, c2 = st.columns(2)
  with c1:
    dest_sel = st.selectbox("目標スターゲート宙域", list(DESTINATIONS.keys()))
    dest_cfg = DESTINATIONS[dest_sel]
    st.caption(f"**航行距離:** {dest_cfg['dist_label']}")
  with c2:
    cam_preset = st.radio(
        "メインカメラ距離プリセット (※ホイールスクロール干渉なし / 左ドラッグで360°回転可能)",
        [
            "ロング・ワイド俯瞰 (推奨：機体全景＋推進炎＋基地・地球が広く見える)",
            "エクストラ・ワイド俯瞰 (超広角：周囲の空間・ワープトンネル全体を一望)",
            "ミディアム・チェイス (機体ディテール＆メカ変形をバランスよく観察)",
        ],
        index=0,
    )


# =========================================================================
# 💥 高精度タイムライン物理データ生成
# =========================================================================
def build_timeline(preview_only=False):
  if preview_only:
    return [
        {
            "t": -5.0,
            "phase": "PAD_STANDBY",
            "dist_m": 0.0,
            "alt_km": 0.04,
            "mach": 0.0,
            "vc": 0.0,
            "g": 1.0,
            "temp_k": 288.0,
            "clamp_open": 0.0,
            "sabot_purge": 0.0,
            "booster_purge": 0.0,
            "fairing_purge": 0.0,
            "wing_sweep": 0.0,
            "bay_open": 0.0,
            "ring_lift": 0.0,
            "rad_deploy": 0.0,
            "nozzle_open": 0.2,
            "engine_power": 0.0,
            "spark_arc": 0.0,
            "vapor_alpha": 0.0,
            "plasma_alpha": 0.0,
            "warp_charge": 0.0,
            "warp_blackout": 0.0,
            "warp_active": 0.0,
            "warp_boom": 0.0,
            "rcs_burst": 0.0,
            "tether_lock": 0.0,
            "pitch_deg": env_cfg["angle_deg"],
            "yaw_deg": 0.0,
            "vib": 0.0,
            "progress": 0.0,
            "ship_time": 0.0,
        }
    ]

  dt = 0.25
  frames = []
  base_pitch = float(env_cfg["angle_deg"])
  exit_mach = vessel_cfg["catapult_mach"] * (coil_charge / 100.0)

  # 1. T-5.0s ~ T-0.0s : カウントダウン＆電磁励磁チャージ
  for step in range(20):
    t = -5.0 + step * dt
    eng_pre = float(np.clip((t + 1.8) / 1.8, 0.0, 0.7))
    clamp = float(np.clip((t + 0.4) / 0.4, 0.0, 1.0))
    frames.append({
        "t": t,
        "phase": "CRYO_VENTING" if t < -3.0 else "LINEAR_COIL_CHARGE",
        "dist_m": 0.0,
        "alt_km": 0.04,
        "mach": 0.0,
        "vc": 0.0,
        "g": 1.0 + eng_pre * 0.9,
        "temp_k": 288.0 + eng_pre * 140.0,
        "clamp_open": clamp,
        "sabot_purge": 0.0,
        "booster_purge": 0.0,
        "fairing_purge": 0.0,
        "wing_sweep": 0.0,
        "bay_open": 0.0,
        "ring_lift": 0.0,
        "rad_deploy": 0.0,
        "nozzle_open": 0.2 + eng_pre * 0.5,
        "engine_power": eng_pre,
        "spark_arc": float(np.clip((t + 2.5) / 2.5, 0.0, 0.6)),
        "vapor_alpha": 0.0,
        "plasma_alpha": 0.0,
        "warp_charge": 0.0,
        "warp_blackout": 0.0,
        "warp_active": 0.0,
        "warp_boom": 0.0,
        "rcs_burst": 0.0,
        "tether_lock": 0.0,
        "pitch_deg": base_pitch,
        "yaw_deg": 0.0,
        "vib": eng_pre * 0.12,
        "progress": 0.0,
        "ship_time": 0.0,
    })

  dist_m = 0.0
  alt_km = 0.04
  mach = 0.0
  vc = 0.0
  progress = 0.0
  ship_time = 0.0
  sabot_p = 0.0
  booster_p = 0.0
  fairing_p = 0.0
  bay_o = 0.0
  ring_l = 0.0
  rad_d = 0.0

  # 2. T+0.0s 以降のフライトシーケンス
  for step in range(280):
    t = step * dt
    rad_pitch = np.radians(base_pitch)
    vapor = 0.0
    plasma = 0.0
    spark_arc = 0.0
    w_charge = 0.0
    w_blackout = 0.0
    w_active = 0.0
    w_boom = 0.0
    rcs = 0.0
    tether = 0.0
    vib = 0.0
    yaw_deg = 0.0

    if t <= 3.5:
      # カタパルトレール電磁滑走 (火花アーク＆マッハ突破)
      phase = "CATAPULT_RAIL_ACCEL"
      accel_ratio = t / 3.5
      mach = (accel_ratio**1.25) * exit_mach
      speed_ms = mach * 340.0
      dist_m += speed_ms * dt * 0.50
      alt_km = 0.04 + (dist_m * np.sin(rad_pitch)) / 1000.0
      g_load = 15.0 * (coil_charge / 100.0)
      eng_pwr = 1.0
      nozzle = 0.95
      spark_arc = 1.0
      wing_sw = float(np.clip((mach - 1.5) / 10.0, 0.0, 1.0))
      if 0.85 <= mach <= 1.85:
        vapor = float(1.0 - abs(mach - 1.35) / 0.5)
      vib = 0.28 + vapor * 0.35
      pitch_cur = base_pitch
    elif alt_km < 130.0:
      # 極超音速クライム＆成層圏突破＆地球離脱加速
      phase = "STRATOSPHERE_CLIMB" if alt_km < 60.0 else "EXOSPHERE_INSERTION"
      sabot_p = min(1.0, sabot_p + 0.85 * dt)
      mach = min(35.0, mach + 2.4 * dt)
      speed_ms = mach * 340.0
      dist_m += speed_ms * dt * 0.65
      space_f = float(np.clip((alt_km - 10.0) / 110.0, 0.0, 1.0))
      pitch_cur = base_pitch * (1.0 - space_f * 0.88)
      alt_km += (speed_ms * np.sin(np.radians(max(4.5, pitch_cur))) * dt) / 1000.0
      g_load = 5.4
      eng_pwr = 1.0
      nozzle = 1.0
      wing_sw = 1.0
      if 14.0 <= alt_km <= 82.0:
        plasma = float(np.sin(((alt_km - 14.0) / 68.0) * np.pi) ** 0.75)
      if alt_km >= 55.0 and aux_boosters:
        booster_p = min(1.0, booster_p + 0.45 * dt)
        if booster_p < 0.4:
          rcs = 1.0
      vib = plasma * 0.45 + 0.08
    elif progress < 0.08:
      # 軌道到達・4段階メカ展開・重力レンズ収縮ブラックアウト（溜め）
      phase = "WARP_FIELD_COMPRESSION"
      alt_km = 155.0 + (progress / 0.08) * 120.0
      pitch_cur = 0.0
      eng_pwr = 0.15
      nozzle = 0.25
      g_load = 0.2
      wing_sw = 0.5
      progress += 0.0045 * dt * 4.0
      morph_prog = float(np.clip(progress / 0.08, 0.0, 1.0))
      bay_o = float(np.clip(morph_prog * 2.5, 0.0, 1.0))
      ring_l = float(np.clip((morph_prog - 0.25) * 2.2, 0.0, 1.0))
      rad_d = float(np.clip((morph_prog - 0.45) * 2.0, 0.0, 1.0))
      if vessel_cfg["style"] == "massdriver_spear":
        fairing_p = min(1.0, fairing_p + 0.5 * dt)
      w_charge = float(np.clip((morph_prog - 0.35) / 0.65, 0.0, 1.0))
      if morph_prog > 0.82:
        w_blackout = float(np.sin(((morph_prog - 0.82) / 0.18) * np.pi))
      if morph_prog > 0.94:
        w_boom = 1.0
      rcs = 1.0 if morph_prog < 0.25 else 0.0
      vc = 0.008 + w_charge * 0.04
    elif progress < flip_timing:
      # アルクビエレ超光速ワープ巡航（地球が一瞬で後方へ吹き飛び消失）
      phase = "ALCUBIERRE_HYPER_WARP"
      alt_km = 300.0 + (progress - 0.08) * 500000.0
      pitch_cur = 0.0
      bay_o = 1.0
      ring_l = 1.0
      rad_d = 1.0
      wing_sw = 1.0
      eng_pwr = 1.0
      nozzle = 1.0
      target_vc = min(0.996, 0.30 + (warp_factor / 10.0) * 0.69)
      vc = min(target_vc, vc + 0.20 * dt)
      w_active = 1.0
      w_charge = 1.0
      g_load = 1.1
      vib = 0.10
      progress += (vc * 0.026) * dt * 4.0
      if progress >= flip_timing - 0.02:
        w_boom = 1.0
    else:
      # ワープアウト＆氷塊デブリ帯での180度フリップ逆噴射＆電磁テザー着艦
      phase = "DEBRIS_RETRO_BRAKING"
      alt_km = 99999.0
      rem = max(0.0001, 1.0 - progress)
      flip_prog = float(np.clip((progress - flip_timing) / 0.05, 0.0, 1.0))
      yaw_deg = flip_prog * 180.0
      pitch_cur = 0.0
      rcs = 1.0 if flip_prog < 1.0 else 0.0
      if rem < 0.08:
        w_boom = max(0.0, 1.0 - (0.08 - rem) * 15.0)
      vc = max(0.004, min(vc, rem * 3.2))
      eng_pwr = 1.0 if flip_prog > 0.65 else 0.2
      nozzle = 1.0
      g_load = 5.2 if flip_prog > 0.65 else 2.2
      bay_o = 1.0
      ring_l = max(0.3, vc * 1.5)
      rad_d = 1.0
      wing_sw = 0.15
      vib = 0.22 if eng_pwr > 0.5 else 0.04
      if progress > 0.88:
        tether = float(np.clip((progress - 0.88) / 0.11, 0.0, 1.0))
      progress = min(1.0, progress + max(0.0025, vc * 0.022) * dt * 4.0)

    gamma = 1.0 / np.sqrt(max(0.001, 1.0 - (min(0.999, vc) ** 2)))
    ship_time += dt / gamma
    temp_k = (
        288.0
        + plasma * 1450.0
        + (w_active * 560.0)
        + (eng_pwr * 190.0)
    )

    frames.append({
        "t": float(t),
        "phase": phase,
        "dist_m": float(dist_m),
        "alt_km": float(alt_km),
        "mach": float(mach),
        "vc": float(vc),
        "g": float(g_load),
        "temp_k": float(temp_k),
        "clamp_open": 1.0,
        "sabot_purge": float(sabot_p),
        "booster_purge": float(booster_p),
        "fairing_purge": float(fairing_p),
        "wing_sweep": float(wing_sw),
        "bay_open": float(bay_o),
        "ring_lift": float(ring_l),
        "rad_deploy": float(rad_d),
        "nozzle_open": float(nozzle),
        "engine_power": float(eng_pwr),
        "spark_arc": float(spark_arc),
        "vapor_alpha": float(vapor),
        "plasma_alpha": float(plasma),
        "warp_charge": float(w_charge),
        "warp_blackout": float(w_blackout),
        "warp_active": float(w_active),
        "warp_boom": float(w_boom),
        "rcs_burst": float(rcs),
        "tether_lock": float(tether),
        "pitch_deg": float(pitch_cur),
        "yaw_deg": float(yaw_deg),
        "vib": float(vib),
        "progress": float(progress),
        "ship_time": float(ship_time),
    })

    if progress >= 0.998:
      for extra in range(20):
        frames.append({
            "t": float(t + (extra + 1) * dt),
            "phase": "STARGATE_DOCKING_LOCKED",
            "dist_m": float(dist_m),
            "alt_km": 99999.0,
            "mach": 0.0,
            "vc": 0.0,
            "g": 0.0,
            "temp_k": 330.0,
            "clamp_open": 1.0,
            "sabot_purge": 1.0,
            "booster_purge": float(booster_p),
            "fairing_purge": float(fairing_p),
            "wing_sweep": 0.0,
            "bay_open": 0.5,
            "ring_lift": 0.2,
            "rad_deploy": 1.0,
            "nozzle_open": 0.2,
            "engine_power": 0.0,
            "spark_arc": 0.0,
            "vapor_alpha": 0.0,
            "plasma_alpha": 0.0,
            "warp_charge": 0.0,
            "warp_blackout": 0.0,
            "warp_active": 0.0,
            "warp_boom": 0.0,
            "rcs_burst": 0.0,
            "tether_lock": 1.0,
            "pitch_deg": 0.0,
            "yaw_deg": 180.0,
            "vib": 0.0,
            "progress": 1.0,
            "ship_time": float(ship_time),
        })
      break

  return frames


# =========================================================================
# 🚀 起動ボタン＆JSONシリアライズ
# =========================================================================
st.markdown("---")
b_col1, b_col2 = st.columns([3, 1])
with b_col1:
  launch_trigger = st.button(
      "🔴 IGNITION & CATAPULT LAUNCH (超伝導励磁 ➔ マッハ射出 ➔ 時空収縮ワープ開始)",
      use_container_width=True,
      type="primary",
  )
with b_col2:
  st.caption(
      "※ 画面クリックでWeb Audio重低音シンセが起動。ホイールはページスクロール優先で引っかかりません。"
  )

timeline_data = build_timeline(preview_only=(not launch_trigger))

sim_config = {
    "is_preview": not launch_trigger,
    "style": vessel_cfg["style"],
    "hull_color": int(hull_color.lstrip("#"), 16),
    "belly_color": int(belly_color.lstrip("#"), 16),
    "metalness": armor_cfg["metalness"],
    "roughness": armor_cfg["roughness"],
    "plasma_hex": armor_cfg["plasma_hex"],
    "flame_hex": power_cfg["flame_hex"],
    "core_hex": power_cfg["core_hex"],
    "spark_hex": power_cfg["spark_hex"],
    "aurora_hex": power_cfg["aurora_hex"],
    "wings_span": wings_span,
    "radiator_fins": radiator_fins,
    "aux_boosters": aux_boosters,
    "cryo_steam": cryo_steam,
    "mach_cone_vfx": mach_cone_vfx,
    "shock_count": shock_count,
    "flip_timing": flip_timing,
    "dest_type": dest_cfg["type"],
    "dest_color": dest_cfg["color_hex"],
    "dest_band": dest_cfg["band_hex"],
    "cam_preset": cam_preset,
    "env": env_cfg,
}

# =========================================================================
# 📺 Three.js ディレクターズカット描画エンジン
# =========================================================================
html_code = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box;}
body,html{margin:0;padding:0;width:100%;height:100%;overflow:hidden;background:#010308;font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,Roboto,monospace;color:#f8fafc;user-select:none;}
#webgl-canvas{width:100%;height:100%;display:block;position:absolute;top:0;left:0;z-index:1;}

.hud-top{position:absolute;top:0;left:0;width:100%;height:44px;background:linear-gradient(180deg,rgba(2,6,18,0.95) 0%,rgba(4,12,28,0.85) 100%);border-bottom:1px solid rgba(56,189,248,0.3);display:flex;align-items:center;justify-content:space-between;padding:0 18px;z-index:20;box-shadow:0 4px 25px rgba(0,0,0,0.8);}
.hud-group{display:flex;align-items:center;gap:14px;font-size:11px;letter-spacing:1px;}
.badge{background:rgba(14,165,233,0.18);border:1px solid #38bdf8;color:#38bdf8;padding:2px 8px;border-radius:3px;font-weight:800;}

.pip-window{position:absolute;top:52px;right:12px;width:350px;height:196px;border:2px solid rgba(56,189,248,0.9);border-radius:6px;z-index:40;background:rgba(2,6,20,0.4);box-shadow:0 15px 45px rgba(0,0,0,0.95);cursor:pointer;overflow:hidden;transition:height 0.25s ease;}
.pip-scan{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,0.22),rgba(0,0,0,0.22) 1px,transparent 1px,transparent 3px);pointer-events:none;z-index:42;}
.pip-header{position:absolute;top:6px;left:8px;right:8px;display:flex;justify-content:space-between;z-index:45;pointer-events:none;}
.pip-label{font-size:9px;font-weight:800;background:rgba(9,14,28,0.92);padding:3px 7px;border-left:2px solid #38bdf8;letter-spacing:1px;}
.pip-toggle{font-size:8px;color:#94a3b8;background:rgba(9,14,28,0.92);padding:3px 6px;}
.pip-rec{position:absolute;bottom:6px;right:8px;font-size:9px;color:#f43f5e;font-weight:900;display:flex;align-items:center;gap:5px;z-index:45;pointer-events:none;}
.rec-dot{width:6px;height:6px;border-radius:50%;background:#f43f5e;animation:pulse 1s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.15;}}

.hud-bottom{position:absolute;bottom:0;left:0;width:100%;height:72px;background:linear-gradient(0deg,rgba(2,6,18,0.96) 0%,rgba(6,13,30,0.88) 100%);border-top:1px solid rgba(148,163,184,0.2);display:grid;grid-template-columns:repeat(5,1fr);align-items:center;padding:0 24px;z-index:20;}
.metric{display:flex;flex-direction:column;border-left:2px solid rgba(56,189,248,0.35);padding-left:12px;}
.metric-lbl{font-size:9px;color:#94a3b8;letter-spacing:1.2px;}
.metric-val{font-size:18px;font-weight:900;color:#f8fafc;margin-top:2px;}

.ctrl-hint{position:absolute;bottom:80px;left:50%;transform:translateX(-50%);background:rgba(3,9,24,0.85);border:1px solid rgba(56,189,248,0.35);padding:4px 14px;border-radius:14px;font-size:10px;color:#7dd3fc;letter-spacing:1px;z-index:25;pointer-events:none;}
#complete-banner{display:none;position:absolute;top:130px;left:50%;transform:translateX(-50%);background:rgba(6,78,59,0.95);border:2px solid #10b981;padding:18px 36px;border-radius:8px;text-align:center;z-index:70;box-shadow:0 0 60px rgba(16,185,129,0.7);}
#warp-flash{position:absolute;inset:0;background:radial-gradient(circle,#ffffff 0%,#38bdf8 55%,transparent 100%);opacity:0;pointer-events:none;z-index:80;}
#blackout-lens{position:absolute;inset:0;background:radial-gradient(circle,#000000 0%,#000000 45%,rgba(56,189,248,0.6) 52%,transparent 70%);opacity:0;pointer-events:none;z-index:75;}
</style>
</head>
<body>
<canvas id="webgl-canvas"></canvas>
<div id="blackout-lens"></div>
<div id="warp-flash"></div>

<div class="hud-top">
  <div class="hud-group">
    <span class="badge">APEX VFX ENGINE</span>
    <span>PHASE: <strong id="ui-phase" style="color:#fbbf24;">PAD_STANDBY</strong></span>
  </div>
  <div class="hud-group">
    <span>EARTH DIST: <strong id="ui-alt">0.04 km</strong></span>
    <span>VELOCITY: <strong id="ui-spd" style="color:#38bdf8;">M 0.0</strong></span>
    <span>SHIP CLOCK: <strong id="ui-clock">T- 05.0s</strong></span>
  </div>
</div>

<div id="pip-box" class="pip-window" title="クリックでサブモニターを折りたたみ">
  <div class="pip-scan"></div>
  <div class="pip-header">
    <div id="pip-title" class="pip-label">CAM 02: RAIL SIDE TRACKER</div>
    <div id="pip-btn" class="pip-toggle">[HIDE]</div>
  </div>
  <div class="pip-rec"><div class="rec-dot"></div>LIVE TELEMETRY</div>
</div>

<div id="complete-banner">
  <div style="font-size:19px;font-weight:900;color:#6ee7b7;letter-spacing:1.5px;">STARGATE MAGNETIC ARREST COMPLETE</div>
  <div style="font-size:11px;color:#d1fae5;margin-top:4px;">ALL HYPER-DRIVE SUBSYSTEMS NOMINAL / DOCKING LOCK ENGAGED</div>
</div>

<div class="ctrl-hint">🖱️ 左ドラッグ: 360°アングル自由回転 （※ホイールズームはページスクロール優先のため無効化済み）</div>

<div class="hud-bottom">
  <div class="metric"><span class="metric-lbl">RELATIVISTIC SPEED</span><span class="metric-val"><span id="ui-vc">0.000</span> <small style="font-size:11px;color:#64748b;">c</small></span></div>
  <div class="metric"><span class="metric-lbl">HULL TEMPERATURE</span><span class="metric-val"><span id="ui-temp">288</span> <small style="font-size:11px;color:#64748b;">K</small></span></div>
  <div class="metric"><span class="metric-lbl">INERTIAL LOAD</span><span class="metric-val"><span id="ui-g">1.0</span> <small style="font-size:11px;color:#64748b;">G</small></span></div>
  <div class="metric"><span class="metric-lbl">LORENTZ FACTOR (γ)</span><span class="metric-val"><span id="ui-gamma">1.00</span> <small style="font-size:11px;color:#64748b;">x</small></span></div>
  <div class="metric"><span class="metric-lbl">ROUTE PROGRESS</span><span class="metric-val"><span id="ui-prog">0.0</span> <small style="font-size:11px;color:#64748b;">%</small></span></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
window.addEventListener('DOMContentLoaded', () => {
const frames = __TIMELINE_JSON__;
const cfg = __CONFIG_JSON__;

const canvas = document.getElementById('webgl-canvas');
let W = window.innerWidth, H = window.innerHeight;
const pipBox = document.getElementById('pip-box');
let pipOpen = true;

pipBox.addEventListener('click', () => {
    pipOpen = !pipOpen;
    pipBox.style.height = pipOpen ? '196px' : '28px';
    document.getElementById('pip-btn').innerText = pipOpen ? '[HIDE]' : '[SHOW]';
});

// =========================================================================
// 1. レンダラー＆カメラ構築（ホイールズーム完全無効化＋ワイド引き視点）
// =========================================================================
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: "high-performance" });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
renderer.setSize(W, H);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.4;

const scene = new THREE.Scene();
const cameraMain = new THREE.PerspectiveCamera(42, W / H, 0.5, 450000);
const cameraPip = new THREE.PerspectiveCamera(32, 350 / 196, 0.5, 450000);

const controls = new THREE.OrbitControls(cameraMain, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
// ★ホイールスクロール干渉を完全に防止
controls.enableZoom = false;
controls.enablePan = false;
controls.target.set(0, 1.0, -4.0);

if (cfg.cam_preset.includes("エクストラ")) {
    cameraMain.position.set(-125, 52, -165);
} else if (cfg.cam_preset.includes("ミディアム")) {
    cameraMain.position.set(-68, 28, -92);
} else {
    // ロング・ワイド俯瞰（機体＋40mの推進炎＋カタパルト基地＋背景富士山が一望できる黄金比）
    cameraMain.position.set(-96, 38, -132);
}
controls.update();

window.addEventListener('resize', () => {
    W = window.innerWidth; H = window.innerHeight;
    renderer.setSize(W, H);
    cameraMain.aspect = W / H;
    cameraMain.updateProjectionMatrix();
});

// ライティング
const sunLight = new THREE.DirectionalLight(cfg.env.sun_color, cfg.env.sun_int);
sunLight.position.set(...cfg.env.sun_pos);
scene.add(sunLight);

const hemiLight = new THREE.HemisphereLight(0xbae6fd, 0x0f172a, 1.5);
scene.add(hemiLight);

const underRimLight = new THREE.PointLight(0x38bdf8, 2.8, 60);
underRimLight.position.set(0, -10, -5);
scene.add(underRimLight);

// =========================================================================
// 2. Web Audio プロシージャル音響シンセサイザー
// =========================================================================
let actx = null, rocketGain = null, coilOsc = null, coilGain = null, warpOsc = null, warpGain = null;
function initAudio() {
    if (actx) return;
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    actx = new AudioCtx();

    const bufSize = actx.sampleRate * 2;
    const noiseBuf = actx.createBuffer(1, bufSize, actx.sampleRate);
    const output = noiseBuf.getChannelData(0);
    let lastOut = 0.0;
    for (let i = 0; i < bufSize; i++) {
        const white = Math.random() * 2 - 1;
        output[i] = (lastOut + (0.04 * white)) / 1.04;
        lastOut = output[i];
        output[i] *= 2.5;
    }
    const whiteNoise = actx.createBufferSource();
    whiteNoise.buffer = noiseBuf;
    whiteNoise.loop = true;
    const filter = actx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 340;
    rocketGain = actx.createGain();
    rocketGain.gain.value = 0.0001;
    whiteNoise.connect(filter);
    filter.connect(rocketGain);
    rocketGain.connect(actx.destination);
    whiteNoise.start(0);

    coilOsc = actx.createOscillator();
    coilOsc.type = 'sawtooth';
    coilOsc.frequency.value = 110;
    const cFilter = actx.createBiquadFilter();
    cFilter.type = 'bandpass';
    cFilter.frequency.value = 480;
    coilGain = actx.createGain();
    coilGain.gain.value = 0.0001;
    coilOsc.connect(cFilter);
    cFilter.connect(coilGain);
    coilGain.connect(actx.destination);
    coilOsc.start(0);

    warpOsc = actx.createOscillator();
    warpOsc.type = 'sine';
    warpOsc.frequency.value = 65;
    warpGain = actx.createGain();
    warpGain.gain.value = 0.0001;
    warpOsc.connect(warpGain);
    warpGain.connect(actx.destination);
    warpOsc.start(0);
}
window.addEventListener('pointerdown', initAudio, { once: true });

// =========================================================================
// 3. プロシージャルPBRテクスチャ生成
// =========================================================================
function makeSkyEnvTexture() {
    const c = document.createElement('canvas'); c.width = 512; c.height = 256;
    const ctx = c.getContext('2d');
    const g = ctx.createLinearGradient(0, 0, 0, 256);
    g.addColorStop(0, cfg.env.sky_zenith);
    g.addColorStop(0.48, cfg.env.sky_horizon);
    g.addColorStop(0.53, '#e0f2fe');
    g.addColorStop(1, '#020617');
    ctx.fillStyle = g; ctx.fillRect(0, 0, 512, 256);
    const tex = new THREE.CanvasTexture(c);
    tex.mapping = THREE.EquirectangularReflectionMapping;
    return tex;
}
scene.environment = makeSkyEnvTexture();

function makeSpacecraftHullTextures() {
    const cBump = document.createElement('canvas'); cBump.width = 1024; cBump.height = 1024;
    const ctx = cBump.getContext('2d');
    ctx.fillStyle = '#808080'; ctx.fillRect(0, 0, 1024, 1024);

    for (let x = 0; x < 1024; x += 64) {
        for (let y = 0; y < 1024; y += 32) {
            const v = 110 + Math.floor(Math.random() * 35);
            ctx.fillStyle = `rgb(${v},${v},${v})`;
            ctx.fillRect(x + 2, y + 2, 60, 28);
            ctx.fillStyle = '#383838';
            ctx.fillRect(x + 5, y + 5, 2, 2);
            ctx.fillRect(x + 56, y + 5, 2, 2);
            ctx.fillRect(x + 5, y + 24, 2, 2);
            ctx.fillRect(x + 56, y + 24, 2, 2);
        }
    }
    ctx.strokeStyle = '#181818'; ctx.lineWidth = 3;
    for (let x = 0; x <= 1024; x += 64) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 1024); ctx.stroke(); }
    for (let y = 0; y <= 1024; y += 32) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(1024, y); ctx.stroke(); }

    const tex = new THREE.CanvasTexture(cBump);
    tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(3, 3);
    return tex;
}
const hullBumpTex = makeSpacecraftHullTextures();

function makeHexCarbonTileTex() {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#18181b'; ctx.fillRect(0, 0, 512, 512);
    ctx.strokeStyle = '#09090b'; ctx.lineWidth = 3;
    for (let y = 0; y < 512; y += 16) {
        const off = (y / 16) % 2 === 0 ? 0 : 12;
        for (let x = -12; x < 512; x += 24) {
            ctx.strokeRect(x + off, y, 22, 14);
        }
    }
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(8, 8);
    return tex;
}
const tileBumpTex = makeHexCarbonTileTex();

function makeGlowSpriteTex(c1, c2) {
    const c = document.createElement('canvas'); c.width = 128; c.height = 128;
    const ctx = c.getContext('2d');
    const g = ctx.createRadialGradient(64, 64, 0, 64, 64, 64);
    g.addColorStop(0, '#ffffff');
    g.addColorStop(0.25, c1);
    g.addColorStop(0.6, c2);
    g.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, 128, 128);
    return new THREE.CanvasTexture(c);
}
const cyanFlareTex = makeGlowSpriteTex('rgba(56,189,248,0.95)', 'rgba(29,78,216,0.3)');
const coreFlareTex = makeGlowSpriteTex('rgba(244,63,94,0.95)', 'rgba(159,18,57,0.3)');

// マテリアル群
const matHull = new THREE.MeshStandardMaterial({
    color: cfg.hull_color, metalness: cfg.metalness, roughness: cfg.roughness,
    bumpMap: hullBumpTex, bumpScale: 0.035, roughnessMap: hullBumpTex
});
const matBellyTile = new THREE.MeshStandardMaterial({
    color: cfg.belly_color, metalness: 0.18, roughness: 0.78,
    bumpMap: tileBumpTex, bumpScale: 0.05
});
const matTitaniumFrame = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.88, roughness: 0.28 });
const matDarkAlloy = new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.92, roughness: 0.22 });
const matGoldMLI = new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.96, roughness: 0.25, bumpMap: tileBumpTex, bumpScale: 0.02 });
const matCopperCoil = new THREE.MeshStandardMaterial({ color: 0xd97706, metalness: 0.94, roughness: 0.2 });
const matCryoPipe = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.85, roughness: 0.15 });
const matCanopy = new THREE.MeshPhysicalMaterial({ color: 0xfbbf24, metalness: 0.85, roughness: 0.05, transparent: true, opacity: 0.88 });
const matSuperconductor = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
const matConduitPulse = new THREE.MeshBasicMaterial({ color: cfg.flame_hex });
const matRadiator = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.8, roughness: 0.3, emissive: 0xef4444, emissiveIntensity: 0.0 });

// =========================================================================
// 4. 宇宙船の超高密度モデリング (原点固定 + エネルギー脈動コンジット)
// =========================================================================
const shipRoot = new THREE.Group();
scene.add(shipRoot);

const shipMeshGroup = new THREE.Group();
shipRoot.add(shipMeshGroup);

const bayDoors = [];
const irisPaddles = [];
const radiatorPanels = [];
const wingPivots = [];
const sabotClamps = [];
const boosterPods = [];
const fairingPanels = [];
const warpRingAssembly = new THREE.Group();
shipMeshGroup.add(warpRingAssembly);

// A. 内部チタン骨格スパイン＆脈動エネルギーコンジット配管
const spineCore = new THREE.Mesh(new THREE.BoxGeometry(2.6, 1.4, 29.0), matDarkAlloy);
shipMeshGroup.add(spineCore);

for (let side of [-1, 1]) {
    for (let h of [-0.4, 0.4]) {
        const cryoLine = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 27.0, 12), matCryoPipe);
        cryoLine.rotation.x = Math.PI / 2;
        cryoLine.position.set(side * 1.45, h, -1.0);
        shipMeshGroup.add(cryoLine);
    }
    // 装甲の隙間から青白く脈動するプラズマ・エネルギーコンジット
    const conduit = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.18, 25.0), matConduitPulse);
    conduit.position.set(side * 2.15, 0.35, -1.0);
    shipMeshGroup.add(conduit);

    for (let z = -9; z <= 5; z += 3.5) {
        const mliPack = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.9, 2.4), matGoldMLI);
        mliPack.position.set(side * 1.1, 0.55, z);
        shipMeshGroup.add(mliPack);
    }
}

// B. 3艦種別の外装モジュール造形
if (cfg.style === "stealth_waverider") {
    const noseShape = new THREE.Shape();
    noseShape.moveTo(0, 1.1);
    noseShape.lineTo(2.6, 0.15);
    noseShape.lineTo(2.1, -0.75);
    noseShape.lineTo(-2.1, -0.75);
    noseShape.lineTo(-2.6, 0.15);
    noseShape.closePath();

    const noseGeo = new THREE.ExtrudeGeometry(noseShape, { depth: 12.0, bevelEnabled: true, bevelThickness: 4.5, bevelSize: 0.9, bevelSegments: 4 });
    const noseMesh = new THREE.Mesh(noseGeo, matHull);
    noseMesh.position.set(0, 0, 3.5);
    shipMeshGroup.add(noseMesh);

    const pitot = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.08, 3.8, 8), matCryoPipe);
    pitot.rotation.x = Math.PI / 2;
    pitot.position.set(0, -0.1, 20.8);
    shipMeshGroup.add(pitot);

    const bellyMesh = new THREE.Mesh(noseGeo, matBellyTile);
    bellyMesh.scale.set(0.98, 0.45, 0.98);
    bellyMesh.position.set(0, -0.48, 3.5);
    shipMeshGroup.add(bellyMesh);

    for (let s of [-1, 1]) {
        const nacelle = new THREE.Mesh(new THREE.BoxGeometry(2.5, 1.9, 19.5), matHull);
        nacelle.position.set(s * 3.1, -0.15, -3.5);
        shipMeshGroup.add(nacelle);

        const intakeVoid = new THREE.Mesh(new THREE.BoxGeometry(2.1, 1.3, 1.2), new THREE.MeshBasicMaterial({ color: 0x020617 }));
        intakeVoid.position.set(s * 3.1, -0.2, 6.1);
        shipMeshGroup.add(intakeVoid);

        const splitterPlate = new THREE.Mesh(new THREE.BoxGeometry(0.08, 1.4, 2.8), matTitaniumFrame);
        splitterPlate.position.set(s * 3.1, -0.2, 6.5);
        shipMeshGroup.add(splitterPlate);

        const vTail = new THREE.Mesh(new THREE.BoxGeometry(0.22, 4.6, 6.2), matHull);
        vTail.position.set(s * 3.8, 2.1, -10.8);
        vTail.rotation.z = -s * 0.32;
        shipMeshGroup.add(vTail);
    }
} else if (cfg.style === "magnetic_fusion") {
    const cmdPod = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 3.4, 13.0, 8), matHull);
    cmdPod.rotation.x = Math.PI / 2;
    cmdPod.scale.set(1.3, 0.75, 1.0);
    cmdPod.position.set(0, 0.2, 10.5);
    shipMeshGroup.add(cmdPod);

    for (let z = -12; z <= 3; z += 3.0) {
        const ringFrame = new THREE.Mesh(new THREE.TorusGeometry(3.8, 0.18, 8, 8), matTitaniumFrame);
        ringFrame.position.set(0, 0, z);
        shipMeshGroup.add(ringFrame);
    }
    for (let z of [-8.5, -3.5]) {
        for (let a = 0; a < 4; a++) {
            const ang = (a / 4) * Math.PI * 2 + Math.PI / 4;
            const sphereTank = new THREE.Mesh(new THREE.SphereGeometry(1.65, 24, 24), matGoldMLI);
            sphereTank.position.set(Math.cos(ang) * 3.2, Math.sin(ang) * 2.4, z);
            shipMeshGroup.add(sphereTank);
        }
    }
} else {
    const innerCore = new THREE.Mesh(new THREE.ConeGeometry(2.1, 34.0, 6), matGoldMLI);
    innerCore.rotation.x = Math.PI / 2;
    innerCore.position.set(0, 0, 2.0);
    shipMeshGroup.add(innerCore);

    for (let i = 0; i < 4; i++) {
        const ang = (i / 4) * Math.PI * 2 + Math.PI / 4;
        const fPanel = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.35, 24.0), matHull);
        fPanel.position.set(Math.cos(ang) * 2.1, Math.sin(ang) * 2.1, 1.0);
        fPanel.rotation.z = ang + Math.PI / 2;
        shipMeshGroup.add(fPanel);
        fairingPanels.push({ mesh: fPanel, baseX: fPanel.position.x, baseY: fPanel.position.y, vx: Math.cos(ang) * 22, vy: Math.sin(ang) * 22 });
    }
}

// C. キャノピー
const canopyGlass = new THREE.Mesh(new THREE.ConeGeometry(1.35, 7.5, 16), matCanopy);
canopyGlass.scale.set(1.0, 0.48, 1.6);
canopyGlass.rotation.x = Math.PI / 2;
canopyGlass.position.set(0, 0.95, 8.8);
shipMeshGroup.add(canopyGlass);

// D. 可変ジオメトリ主翼
const halfSpan = cfg.wings_span * 0.5;
for (let s of [-1, 1]) {
    const pivot = new THREE.Group();
    pivot.position.set(s * 3.2, -0.1, 1.5);
    shipMeshGroup.add(pivot);

    const wShape = new THREE.Shape();
    wShape.moveTo(0, 4.0);
    wShape.lineTo(s * (halfSpan - 3.2), -3.5);
    wShape.lineTo(s * (halfSpan - 3.6), -7.5);
    wShape.lineTo(0, -10.5);
    wShape.closePath();

    const wGeo = new THREE.ExtrudeGeometry(wShape, { depth: 0.32, bevelEnabled: true, bevelThickness: 0.12, bevelSize: 0.4, bevelSegments: 2 });
    const wMesh = new THREE.Mesh(wGeo, matHull);
    wMesh.rotation.x = Math.PI / 2;
    pivot.add(wMesh);

    const flap = new THREE.Mesh(new THREE.BoxGeometry(halfSpan * 0.55, 0.12, 1.2), matTitaniumFrame);
    flap.position.set(s * (halfSpan * 0.35), -0.15, -9.2);
    pivot.add(flap);

    wingPivots.push({ group: pivot, side: s });
}

// E. 背部4分割観音開きペイロードベイ
for (let s of [-1, 1]) {
    for (let zOff of [-6.0, 1.0]) {
        const doorPivot = new THREE.Group();
        doorPivot.position.set(s * 2.4, 1.15, zOff);
        shipMeshGroup.add(doorPivot);

        const doorPanel = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.25, 6.4), matHull);
        doorPanel.position.set(-s * 1.1, 0, 0);
        doorPivot.add(doorPanel);
        bayDoors.push({ pivot: doorPivot, side: s });
    }
}

// F. デュアル超伝導ワープリング
warpRingAssembly.position.set(0, -0.8, -2.5);
const ringPylon = new THREE.Mesh(new THREE.BoxGeometry(1.6, 3.8, 4.5), matTitaniumFrame);
ringPylon.position.set(0, -1.8, 0);
warpRingAssembly.add(ringPylon);

for (let c = -1.5; c <= 1.5; c += 1.0) {
    const cCoil = new THREE.Mesh(new THREE.TorusGeometry(1.2, 0.22, 12, 24), matCopperCoil);
    cCoil.rotation.y = Math.PI / 2;
    cCoil.position.set(c, -0.6, 0);
    warpRingAssembly.add(cCoil);
}

const outerWarpRing = new THREE.Mesh(new THREE.TorusGeometry(6.8, 0.42, 20, 64), matTitaniumFrame);
const innerWarpCoil = new THREE.Mesh(new THREE.TorusGeometry(6.1, 0.28, 16, 64), matSuperconductor);
warpRingAssembly.add(outerWarpRing);
warpRingAssembly.add(innerWarpCoil);

const warpCoreSprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: cyanFlareTex, blending: THREE.AdditiveBlending, transparent: true, opacity: 0.0 }));
warpCoreSprite.scale.set(28, 28, 1);
warpRingAssembly.add(warpCoreSprite);

// G. 展開式・高温赤熱ラジエーター
for (let r = 0; r < cfg.radiator_fins; r++) {
    const s = (r % 2 === 0) ? 1 : -1;
    const row = Math.floor(r / 2);
    const rPivot = new THREE.Group();
    rPivot.position.set(s * 2.2, 0.8, -3.5 - row * 2.8);
    shipMeshGroup.add(rPivot);

    const rBlade = new THREE.Mesh(new THREE.BoxGeometry(4.8, 0.08, 1.8), matRadiator);
    rBlade.position.set(s * 2.4, 0, 0);
    rPivot.add(rBlade);
    radiatorPanels.push({ pivot: rPivot, side: s });
}

// H. 12枚花弁アイリス可変ベクタード・ノズル
const nozzleRoot = new THREE.Group();
nozzleRoot.position.set(0, 0, -14.2);
shipMeshGroup.add(nozzleRoot);

const nozzleShroud = new THREE.Mesh(new THREE.CylinderGeometry(2.6, 2.9, 2.5, 24, 1, true), matDarkAlloy);
nozzleShroud.rotation.x = Math.PI / 2;
nozzleRoot.add(nozzleShroud);

for (let i = 0; i < 12; i++) {
    const ang = (i / 12) * Math.PI * 2;
    const petalPivot = new THREE.Group();
    petalPivot.position.set(Math.cos(ang) * 2.5, Math.sin(ang) * 2.5, -1.0);
    petalPivot.rotation.z = ang;
    nozzleRoot.add(petalPivot);

    const petal = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.22, 3.2), matTitaniumFrame);
    petal.position.set(0, 0, -1.4);
    petalPivot.add(petal);
    irisPaddles.push(petalPivot);
}

// I. 補助ブースター ＆ サボ台車
if (cfg.aux_boosters) {
    for (let s of [-1, 1]) {
        const bPod = new THREE.Group();
        bPod.position.set(s * 5.8, -0.65, -4.5);
        shipMeshGroup.add(bPod);

        const bBody = new THREE.Mesh(new THREE.CylinderGeometry(0.85, 1.05, 14.5, 20), matBellyTile);
        bBody.rotation.x = Math.PI / 2;
        bPod.add(bBody);

        const bCone = new THREE.Mesh(new THREE.ConeGeometry(0.85, 3.5, 20), matGoldMLI);
        bCone.rotation.x = Math.PI / 2;
        bCone.position.z = 9.0;
        bPod.add(bCone);

        boosterPods.push({ group: bPod, baseX: s * 5.8, side: s });
    }
}

for (let s of [-1, 1]) {
    const sabot = new THREE.Mesh(new THREE.BoxGeometry(2.2, 1.1, 7.5), matDarkAlloy);
    sabot.position.set(s * 3.8, -1.4, -1.0);
    shipMeshGroup.add(sabot);
    sabotClamps.push({ mesh: sabot, baseX: s * 3.8, side: s });
}

// J. 推進プラズマプルーム＆ショックダイヤモンド＆スパーク粒子
const plumeRoot = new THREE.Group();
plumeRoot.position.set(0, 0, -16.5);
shipMeshGroup.add(plumeRoot);

const innerCoreBeam = new THREE.Mesh(
    new THREE.CylinderGeometry(0.4, 1.9, 28.0, 20, 1, true),
    new THREE.MeshBasicMaterial({ color: cfg.core_hex, transparent: true, opacity: 0.95, blending: THREE.AdditiveBlending, side: THREE.DoubleSide })
);
innerCoreBeam.rotation.x = Math.PI / 2;
innerCoreBeam.position.z = -14.0;
plumeRoot.add(innerCoreBeam);

const outerPlasmaCone = new THREE.Mesh(
    new THREE.ConeGeometry(4.2, 42.0, 24, 1, true),
    new THREE.MeshBasicMaterial({ color: cfg.flame_hex, transparent: true, opacity: 0.65, blending: THREE.AdditiveBlending, side: THREE.DoubleSide })
);
outerPlasmaCone.rotation.x = Math.PI / 2;
outerPlasmaCone.position.z = -21.0;
plumeRoot.add(outerPlasmaCone);

const nozzleFlare = new THREE.Sprite(new THREE.SpriteMaterial({ map: coreFlareTex, blending: THREE.AdditiveBlending, transparent: true, opacity: 0.95 }));
nozzleFlare.scale.set(18, 18, 1);
plumeRoot.add(nozzleFlare);

const shockDisks = [];
for (let d = 0; d < cfg.shock_count; d++) {
    const disk = new THREE.Mesh(
        new THREE.RingGeometry(0.15, 2.1 - d * 0.24, 24),
        new THREE.MeshBasicMaterial({ color: cfg.spark_hex, transparent: true, opacity: 0.9, blending: THREE.AdditiveBlending, side: THREE.DoubleSide })
    );
    disk.position.set(0, 0, -3.5 - d * 4.6);
    plumeRoot.add(disk);
    shockDisks.push(disk);
}

const sparkCount = 260;
const sparkGeo = new THREE.BufferGeometry();
const sparkPos = new Float32Array(sparkCount * 3);
for (let i = 0; i < sparkCount; i++) {
    sparkPos[i * 3] = (Math.random() - 0.5) * 2.2;
    sparkPos[i * 3 + 1] = (Math.random() - 0.5) * 2.2;
    sparkPos[i * 3 + 2] = -Math.random() * 55.0;
}
sparkGeo.setAttribute('position', new THREE.BufferAttribute(sparkPos, 3));
const sparkSystem = new THREE.Points(sparkGeo, new THREE.PointsMaterial({ color: cfg.spark_hex, size: 1.8, blending: THREE.AdditiveBlending, transparent: true, opacity: 0.88 }));
plumeRoot.add(sparkSystem);

// K. 多重マッハコーン＆断熱圧縮プラズマトレイル＆RCSガス
const vaporGroup = new THREE.Group();
shipMeshGroup.add(vaporGroup);
const vaporCones = [];
for (let v of [{ z: 6.0, r: 7.5, l: 4.5 }, { z: -3.0, r: 14.0, l: 8.0 }]) {
    const vcMesh = new THREE.Mesh(
        new THREE.ConeGeometry(v.r, v.l, 32, 1, true),
        new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending, side: THREE.DoubleSide })
    );
    vcMesh.rotation.x = -Math.PI / 2;
    vcMesh.position.z = v.z;
    vaporGroup.add(vcMesh);
    vaporCones.push(vcMesh);
}

const plasmaEnvelope = new THREE.Mesh(
    new THREE.ConeGeometry(8.8, 44.0, 28, 1, true),
    new THREE.MeshBasicMaterial({ color: cfg.plasma_hex, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending, side: THREE.DoubleSide })
);
plasmaEnvelope.rotation.x = -Math.PI / 2;
plasmaEnvelope.position.z = 2.0;
shipMeshGroup.add(plasmaEnvelope);

const rcsJets = [];
for (let pos of [[2.2, 0.5, 11], [-2.2, 0.5, 11], [0, 1.6, 11], [3.5, 0.5, -11], [-3.5, 0.5, -11]]) {
    const rcsCone = new THREE.Mesh(
        new THREE.ConeGeometry(0.45, 3.2, 12),
        new THREE.MeshBasicMaterial({ color: 0xe0f2fe, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending })
    );
    rcsCone.position.set(...pos);
    rcsCone.rotation.z = pos[0] > 0 ? -Math.PI / 2 : (pos[0] < 0 ? Math.PI / 2 : 0);
    shipMeshGroup.add(rcsCone);
    rcsJets.push(rcsCone);
}

// スペースブーム衝撃波リング
const boomRing = new THREE.Mesh(
    new THREE.RingGeometry(4.0, 9.0, 48),
    new THREE.MeshBasicMaterial({ color: 0x7dd3fc, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending, side: THREE.DoubleSide })
);
boomRing.rotation.x = Math.PI / 2;
shipRoot.add(boomRing);

// =========================================================================
// 5. メガフロート射場基地（照明クレーン・管制塔・サーチライト・正面奥の富士山・立体雲海）
// =========================================================================
const launchWorld = new THREE.Group();
scene.add(launchWorld);

const launchPitchGroup = new THREE.Group();
const radAngle = THREE.MathUtils.degToRad(cfg.env.angle_deg);
launchPitchGroup.rotation.x = -radAngle;
launchWorld.add(launchPitchGroup);

const segCount = 220;
const dummy = new THREE.Object3D();

const archGeo = new THREE.TorusGeometry(9.5, 0.45, 10, 24, Math.PI);
const archInst = new THREE.InstancedMesh(archGeo, matTitaniumFrame, segCount);
const coilLedGeo = new THREE.BoxGeometry(0.4, 2.2, 6.0);
const coilLedInst = new THREE.InstancedMesh(coilLedGeo, matSuperconductor, segCount * 2);

for (let i = 0; i < segCount; i++) {
    const zPos = i * 16.0 - 40.0;
    dummy.position.set(0, -1.8, zPos);
    dummy.rotation.set(0, 0, 0);
    dummy.updateMatrix();
    archInst.setMatrixAt(i, dummy.matrix);

    dummy.position.set(-6.8, -0.6, zPos);
    dummy.updateMatrix();
    coilLedInst.setMatrixAt(i * 2, dummy.matrix);

    dummy.position.set(6.8, -0.6, zPos);
    dummy.updateMatrix();
    coilLedInst.setMatrixAt(i * 2 + 1, dummy.matrix);
}
launchPitchGroup.add(archInst);
launchPitchGroup.add(coilLedInst);

// レール主桁
const mainGirder = new THREE.Mesh(new THREE.BoxGeometry(14.5, 2.4, 3600), matDarkAlloy);
mainGirder.position.set(0, -3.2, 1750);
launchPitchGroup.add(mainGirder);

// ★カタパルト両脇を高速で流れ去る「メガフロート基地のガントリクレーン塔＆赤色航空障害灯」
const towerCount = 44;
const towerInst = new THREE.InstancedMesh(new THREE.BoxGeometry(2.5, 36.0, 2.5), matTitaniumFrame, towerCount);
const beaconInst = new THREE.InstancedMesh(new THREE.SphereGeometry(0.8, 8, 8), new THREE.MeshBasicMaterial({ color: 0xef4444 }), towerCount);
for (let i = 0; i < towerCount; i++) {
    const side = (i % 2 === 0) ? 1 : -1;
    const zPos = Math.floor(i / 2) * 85.0 - 20.0;
    dummy.position.set(side * 24.0, 12.0, zPos);
    dummy.updateMatrix();
    towerInst.setMatrixAt(i, dummy.matrix);

    dummy.position.set(side * 24.0, 30.5, zPos);
    dummy.updateMatrix();
    beaconInst.setMatrixAt(i, dummy.matrix);
}
launchPitchGroup.add(towerInst);
launchPitchGroup.add(beaconInst);

// 発射台ホールドダウンクランプ
const padClamps = [];
for (let s of [-1, 1]) {
    const cArm = new THREE.Mesh(new THREE.BoxGeometry(1.4, 4.5, 3.0), matGoldMLI);
    cArm.position.set(s * 5.2, -0.5, -6.0);
    launchPitchGroup.add(cArm);
    padClamps.push({ mesh: cArm, side: s });
}

// クライオ冷却ベント蒸気
const steamCount = 350;
const steamGeo = new THREE.BufferGeometry();
const steamPos = new Float32Array(steamCount * 3);
for (let i = 0; i < steamCount; i++) {
    steamPos[i * 3] = (Math.random() - 0.5) * 14.0;
    steamPos[i * 3 + 1] = -2.0 + Math.random() * 3.0;
    steamPos[i * 3 + 2] = -20.0 + Math.random() * 260.0;
}
steamGeo.setAttribute('position', new THREE.BufferAttribute(steamPos, 3));
const steamPoints = new THREE.Points(steamGeo, new THREE.PointsMaterial({ color: 0xe2e8f0, size: 3.5, transparent: true, opacity: cfg.cryo_steam ? 0.38 : 0.0 }));
launchPitchGroup.add(steamPoints);

// B. 海面・防波堤・サーチライト光柱・正面奥の富士山・立体雲海
const groundEnvGroup = new THREE.Group();
launchWorld.add(groundEnvGroup);

const seaMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(160000, 160000),
    new THREE.MeshStandardMaterial({ color: 0x041226, metalness: 0.90, roughness: 0.14 })
);
seaMesh.rotation.x = -Math.PI / 2;
seaMesh.position.y = -45.0;
groundEnvGroup.add(seaMesh);

// メガフロート基地の防波堤＆発射管制ビル群＆サーチライト光柱
for (let b = 0; b < 16; b++) {
    const side = (b % 2 === 0) ? 1 : -1;
    const bldg = new THREE.Mesh(new THREE.BoxGeometry(28, 35 + (b % 3) * 18, 42), matDarkAlloy);
    bldg.position.set(side * (95 + (b % 3) * 35), -25, b * 160 - 100);
    groundEnvGroup.add(bldg);

    // サーチライトの光の柱（夜空を照らすボリュームライト）
    if (b % 2 === 0) {
        const beam = new THREE.Mesh(
            new THREE.ConeGeometry(28, 650, 16, 1, true),
            new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.12, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false })
        );
        beam.position.set(side * 110, 280, b * 160);
        beam.rotation.z = Math.PI + side * 0.12;
        groundEnvGroup.add(beam);
    }
}

// 相模湾沿岸の都市夜景ネットワーク (6000点・富士山の手前に広がる光の絨毯)
const cityGeo = new THREE.BufferGeometry();
const cityPos = new Float32Array(6000 * 3);
const cityCol = new Float32Array(6000 * 3);
for (let i = 0; i < 6000; i++) {
    cityPos[i * 3] = (Math.random() - 0.45) * 45000;
    cityPos[i * 3 + 1] = -42.0 + Math.random() * 12.0;
    cityPos[i * 3 + 2] = 2500 + Math.random() * 26000;
    const warm = Math.random() > 0.3;
    cityCol[i * 3] = warm ? 1.0 : 0.4;
    cityCol[i * 3 + 1] = warm ? 0.65 : 0.88;
    cityCol[i * 3 + 2] = warm ? 0.2 : 1.0;
}
cityGeo.setAttribute('position', new THREE.BufferAttribute(cityPos, 3));
cityGeo.setAttribute('color', new THREE.BufferAttribute(cityCol, 3));
groundEnvGroup.add(new THREE.Points(cityGeo, new THREE.PointsMaterial({ size: 6.5, vertexColors: true, transparent: true, opacity: 0.92 })));

// ★正面奥（カメラの視線延長線上）に堂々とそびえる富士山と雪化粧
const fujiGroup = new THREE.Group();
// カメラ (-96, 38, -132) から原点 (0,0,0) を見た延長線上 (X:+6500, Z:+16500) に配置
fujiGroup.position.set(6500, -45, 16500);
groundEnvGroup.add(fujiGroup);

const fujiPts = [];
for (let i = 0; i <= 24; i++) {
    const t = i / 24;
    fujiPts.push(new THREE.Vector2(Math.pow(1 - t, 2.1) * 14500 + 850, t * 3776));
}
const fujiMount = new THREE.Mesh(
    new THREE.LatheGeometry(fujiPts, 64),
    new THREE.MeshStandardMaterial({ color: 0x111c2d, roughness: 0.85, emissive: 0x081021, emissiveIntensity: 0.4 })
);
fujiGroup.add(fujiMount);

const snowPts = [];
for (let i = 15; i <= 24; i++) {
    const t = i / 24;
    snowPts.push(new THREE.Vector2(Math.pow(1 - t, 2.1) * 14500 + 855, t * 3776 + 2));
}
const fujiSnow = new THREE.Mesh(
    new THREE.LatheGeometry(snowPts, 64),
    new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.4, emissive: 0x38bdf8, emissiveIntensity: 0.15 })
);
fujiGroup.add(fujiSnow);

// 高度800m〜2200mの立体雲海レイヤー（射出直後に突き抜ける雲）
for (let c = 0; c < 65; c++) {
    const cloudPlane = new THREE.Mesh(
        new THREE.PlaneGeometry(1200, 700),
        new THREE.MeshBasicMaterial({ color: 0xcbd5e1, transparent: true, opacity: 0.18, side: THREE.DoubleSide, depthWrite: false })
    );
    cloudPlane.rotation.x = Math.PI / 2;
    cloudPlane.position.set((Math.random() - 0.5) * 18000, 650 + (c % 3) * 450, (Math.random() - 0.2) * 18000);
    groundEnvGroup.add(cloudPlane);
}

// =========================================================================
// 6. GLSLシェーダー球体地球（加速・ワープで斜め後方へ急速に遠ざかり消失する）
// =========================================================================
const earthGroup = new THREE.Group();
scene.add(earthGroup);

function makePlanetSurfaceTex() {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 512;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#061a38'; ctx.fillRect(0, 0, 1024, 512);
    ctx.fillStyle = '#112a22';
    for (let i = 0; i < 95; i++) {
        ctx.beginPath();
        ctx.arc(Math.random() * 1024, Math.random() * 512, 15 + Math.random() * 70, 0, Math.PI * 2);
        ctx.fill();
    }
    ctx.fillStyle = '#fbbf24';
    for (let i = 0; i < 450; i++) {
        ctx.fillRect(Math.random() * 1024, Math.random() * 512, 2.5, 2.5);
    }
    return new THREE.CanvasTexture(c);
}

const earthSphere = new THREE.Mesh(
    new THREE.SphereGeometry(25000, 64, 64),
    new THREE.MeshStandardMaterial({ map: makePlanetSurfaceTex(), roughness: 0.55, metalness: 0.25 })
);
earthGroup.add(earthSphere);

// GLSLレイリー散乱＋グリーンオーロラ（大気光）シェーダー
const atmosShaderMat = new THREE.ShaderMaterial({
    vertexShader: `
        varying vec3 vNormal;
        varying vec3 vViewPos;
        void main() {
            vNormal = normalize(normalMatrix * normal);
            vec4 mvPos = modelViewMatrix * vec4(position, 1.0);
            vViewPos = -mvPos.xyz;
            gl_Position = projectionMatrix * mvPos;
        }
    `,
    fragmentShader: `
        varying vec3 vNormal;
        varying vec3 vViewPos;
        void main() {
            vec3 viewDir = normalize(vViewPos);
            float fresnel = pow(1.0 - abs(dot(vNormal, viewDir)), 3.0);
            vec3 rayleigh = mix(vec3(0.05, 0.38, 0.98), vec3(0.2, 0.95, 0.75), pow(fresnel, 2.0));
            gl_FragColor = vec4(rayleigh, fresnel * 0.95);
        }
    `,
    transparent: true,
    blending: THREE.AdditiveBlending,
    side: THREE.BackSide,
    depthWrite: false
});
const earthAtmos = new THREE.Mesh(new THREE.SphereGeometry(25500, 64, 64), atmosShaderMat);
earthGroup.add(earthAtmos);

// =========================================================================
// 7. 多層プラズマオーロラ・ワープトンネル ＆ 氷塊デブリ帯 ＆ 目的宙域
// =========================================================================
const warpTunnelGroup = new THREE.Group();
warpTunnelGroup.visible = false;
scene.add(warpTunnelGroup);

// 外周を螺旋回転するプラズマ・オーロラチューブ
function makeAuroraTubeTex() {
    const c = document.createElement('canvas'); c.width = 256; c.height = 256;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#000000'; ctx.fillRect(0, 0, 256, 256);
    for (let i = 0; i < 18; i++) {
        const g = ctx.createLinearGradient(0, 0, 256, 256);
        g.addColorStop(0, 'rgba(0,0,0,0)');
        g.addColorStop(0.5, i % 2 === 0 ? 'rgba(56,189,248,0.45)' : 'rgba(168,85,247,0.45)');
        g.addColorStop(1, 'rgba(0,0,0,0)');
        ctx.fillStyle = g;
        ctx.fillRect(0, i * 14, 256, 8);
    }
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(2, 4);
    return tex;
}
const auroraTex = makeAuroraTubeTex();
const auroraCylinder = new THREE.Mesh(
    new THREE.CylinderGeometry(48, 48, 600, 32, 1, true),
    new THREE.MeshBasicMaterial({ map: auroraTex, transparent: true, opacity: 0.75, blending: THREE.AdditiveBlending, side: THREE.BackSide, depthWrite: false })
);
auroraCylinder.rotation.x = Math.PI / 2;
warpTunnelGroup.add(auroraCylinder);

// 相対論的ドップラー光線（前方青白 ➔ 後方赤紫）
const streakCount = 1000;
const streakGeo = new THREE.BufferGeometry();
const streakPositions = new Float32Array(streakCount * 6);
const streakColors = new Float32Array(streakCount * 6);
for (let i = 0; i < streakCount; i++) {
    const ang = Math.random() * Math.PI * 2;
    const rad = 14.0 + Math.random() * 80.0;
    const z = (Math.random() - 0.5) * 550.0;
    const len = 35.0 + Math.random() * 75.0;
    const x = Math.cos(ang) * rad, y = Math.sin(ang) * rad;
    streakPositions.set([x, y, z, x, y, z + len], i * 6);
    // 先端は青白（ブルーシフト）、後端はマゼンタ（レッドシフト）
    streakColors.set([0.9, 0.3, 0.8, 0.3, 0.9, 1.0], i * 6);
}
streakGeo.setAttribute('position', new THREE.BufferAttribute(streakPositions, 3));
streakGeo.setAttribute('color', new THREE.BufferAttribute(streakColors, 3));
const warpLines = new THREE.LineSegments(streakGeo, new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.95, blending: THREE.AdditiveBlending }));
warpTunnelGroup.add(warpLines);

// 背景恒星フィールド
const bgStarGeo = new THREE.BufferGeometry();
const bgStarPos = new Float32Array(3500 * 3);
for (let i = 0; i < 3500 * 3; i += 3) {
    const r = 60000 + Math.random() * 60000;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    bgStarPos[i] = r * Math.sin(phi) * Math.cos(theta);
    bgStarPos[i + 1] = r * Math.sin(phi) * Math.sin(theta);
    bgStarPos[i + 2] = r * Math.cos(phi);
}
bgStarGeo.setAttribute('position', new THREE.BufferAttribute(bgStarPos, 3));
scene.add(new THREE.Points(bgStarGeo, new THREE.PointsMaterial({ color: 0xffffff, size: 65, transparent: true, opacity: 0.85 })));

// 目的地惑星＆巨大スターゲート＆氷塊デブリフィールド
const destWorld = new THREE.Group();
destWorld.visible = false;
scene.add(destWorld);

function makeGasGiantTex() {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512;
    const ctx = c.getContext('2d');
    for (let y = 0; y < 512; y++) {
        const wave = Math.sin(y * 0.08) * 0.5 + 0.5;
        ctx.fillStyle = wave > 0.5 ? '#' + cfg.dest_color.toString(16).padStart(6, '0') : '#' + cfg.dest_band.toString(16).padStart(6, '0');
        ctx.fillRect(0, y, 512, 1);
    }
    return new THREE.CanvasTexture(c);
}

const destPlanet = new THREE.Mesh(
    new THREE.SphereGeometry(3200, 64, 64),
    new THREE.MeshStandardMaterial({ map: makeGasGiantTex(), roughness: 0.75 })
);
destPlanet.position.set(700, -450, 5200);
destWorld.add(destPlanet);

if (cfg.dest_type === "saturn") {
    const sRing = new THREE.Mesh(
        new THREE.RingGeometry(3800, 6800, 64),
        new THREE.MeshStandardMaterial({ color: 0xd6d3d1, side: THREE.DoubleSide, transparent: true, opacity: 0.85 })
    );
    sRing.position.copy(destPlanet.position);
    sRing.rotation.set(Math.PI / 2.2, 0.25, 0);
    destWorld.add(sRing);
}

// ★ワープアウト減速時に機体の横を高速で掠める「氷塊リング・スペースデブリ群」
const iceCount = 180;
const iceInst = new THREE.InstancedMesh(
    new THREE.DodecahedronGeometry(1.2, 0),
    new THREE.MeshStandardMaterial({ color: 0xe0f2fe, metalness: 0.9, roughness: 0.1 }),
    iceCount
);
const iceData = [];
for (let i = 0; i < iceCount; i++) {
    iceData.push({
        x: (Math.random() - 0.5) * 180,
        y: (Math.random() - 0.5) * 120,
        z: (Math.random() - 0.5) * 600,
        s: 0.4 + Math.random() * 1.8
    });
}
destWorld.add(iceInst);

const stargateGroup = new THREE.Group();
destWorld.add(stargateGroup);

const gateOuter = new THREE.Mesh(new THREE.TorusGeometry(65, 4.8, 20, 64), matTitaniumFrame);
const gateInner = new THREE.Mesh(new THREE.TorusGeometry(58, 1.4, 16, 64), matSuperconductor);
stargateGroup.add(gateOuter);
stargateGroup.add(gateInner);

const tetherBeams = [];
for (let i = 0; i < 4; i++) {
    const tGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
    const tLine = new THREE.Line(tGeo, new THREE.LineBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending }));
    scene.add(tLine);
    tetherBeams.push({ line: tLine, angle: (i / 4) * Math.PI * 2 });
}

// =========================================================================
// 8. 60fps アニメーションループ
// =========================================================================
const startTime = performance.now();
const flashEl = document.getElementById('warp-flash');
const blackoutEl = document.getElementById('blackout-lens');
const pipTitleEl = document.getElementById('pip-title');

function animate(now) {
    requestAnimationFrame(animate);

    const elapsed = (now - startTime) / 1000.0;
    const simTime = cfg.is_preview ? -5.0 : (-5.0 + elapsed * 1.65);

    let idx = 0;
    while (idx < frames.length - 1 && frames[idx + 1].t <= simTime) idx++;
    const f0 = frames[idx];
    const f1 = frames[Math.min(frames.length - 1, idx + 1)];
    const dt = f1.t - f0.t;
    const alpha = dt > 0.0001 ? THREE.MathUtils.clamp((simTime - f0.t) / dt, 0.0, 1.0) : 0.0;
    const L = (k) => THREE.MathUtils.lerp(f0[k], f1[k], alpha);

    const distM = L('dist_m');
    const altKm = L('alt_km');
    const mach = L('mach');
    const vc = L('vc');
    const pitchDeg = L('pitch_deg');
    const yawDeg = L('yaw_deg');
    const vib = L('vib');
    const prog = L('progress');

    // 1. 機体姿勢＆滑らかな周期関数バイブレーション（チラつかない重厚なG表現）
    shipMeshGroup.rotation.set(
        -THREE.MathUtils.degToRad(pitchDeg),
        THREE.MathUtils.degToRad(yawDeg),
        0
    );
    shipMeshGroup.position.set(
        Math.sin(now * 0.045) * vib * 0.4,
        Math.cos(now * 0.055) * vib * 0.4,
        Math.sin(now * 0.035) * vib * 0.4
    );

    // エネルギーコンジット脈動発光
    const pulseWave = 0.5 + 0.5 * Math.sin(now * 0.012);
    matConduitPulse.color.setHex(cfg.flame_hex).multiplyScalar(0.6 + pulseWave * 0.8);

    // 2. カタパルト＆地上ワールドの高速後退
    if (altKm < 110.0 && f0.phase !== "WARP_FIELD_COMPRESSION" && f0.phase !== "ALCUBIERRE_HYPER_WARP") {
        launchWorld.visible = true;
        launchPitchGroup.position.set(0, 0, -distM);
        groundEnvGroup.position.set(
            0,
            -altKm * 1000.0 + 40.0,
            -distM * Math.cos(radAngle)
        );
        padClamps.forEach(pc => {
            pc.mesh.rotation.z = -pc.side * L('clamp_open') * 0.85;
        });
        if (cfg.cryo_steam) {
            const sp = steamGeo.attributes.position.array;
            for (let i = 0; i < steamCount * 3; i += 3) {
                sp[i + 1] += 0.08;
                sp[i + 2] -= (0.4 + mach * 0.8);
                if (sp[i + 1] > 3.5 || sp[i + 2] < -40.0) {
                    sp[i + 1] = -2.0;
                    sp[i + 2] = -10.0 + Math.random() * 180.0;
                }
            }
            steamGeo.attributes.position.needsUpdate = true;
        }
    } else {
        launchWorld.visible = false;
    }

    // ★3. 球体地球の超高速リセッション（大気圏脱出で斜め後方へ離れ、ワープで一気に縮小・消失！）
    if (prog < 0.25) {
        earthGroup.visible = true;
        // ワープ進行度に応じて3乗で後方・下方へ猛スピードで遠ざかる
        const warpRecede = Math.pow(Math.max(0, prog - 0.05) * 18.0, 3.0);
        const recedeY = -25050 - altKm * 120.0 - warpRecede * 35000.0;
        const recedeZ = -4000 - distM * 0.6 - warpRecede * 95000.0;
        earthGroup.position.set(0, recedeY, recedeZ);
        // 遠ざかると同時にスケールも縮小して宇宙の彼方の点へ消える
        const eScale = Math.max(0.001, 1.0 / (1.0 + warpRecede * 1.8));
        earthGroup.scale.setScalar(eScale);
        earthSphere.rotation.y = elapsed * 0.015;
    } else {
        earthGroup.visible = false;
    }

    // 4. メカニカル変形ギミック
    const sweep = L('wing_sweep');
    wingPivots.forEach(wp => { wp.group.rotation.y = wp.side * sweep * 0.32; });

    const bayOpen = L('bay_open');
    bayDoors.forEach(bd => { bd.pivot.rotation.z = bd.side * bayOpen * 1.35; });

    const ringLift = L('ring_lift');
    warpRingAssembly.position.y = -0.8 + ringLift * 4.2;
    const ringSpin = 0.02 + L('warp_charge') * 0.38 + vc * 0.45;
    innerWarpCoil.rotation.z += ringSpin;
    outerWarpRing.rotation.z -= ringSpin * 0.5;
    warpCoreSprite.material.opacity = L('warp_charge') * 0.9;

    const radDep = L('rad_deploy');
    radiatorPanels.forEach(rp => { rp.pivot.rotation.z = rp.side * (1.0 - radDep) * 1.45; });
    const heatNorm = THREE.MathUtils.clamp((L('temp_k') - 320.0) / 1100.0, 0.0, 1.0);
    matRadiator.emissiveIntensity = heatNorm * 2.8;

    const nozOpen = L('nozzle_open');
    irisPaddles.forEach(ip => {
        ip.rotation.x = -0.35 + nozOpen * 0.48 + Math.sin(now * 0.05) * 0.02 * L('engine_power');
    });

    // パージギミック
    const sPurge = L('sabot_purge');
    sabotClamps.forEach(sc => {
        sc.mesh.visible = sPurge < 0.98;
        sc.mesh.position.set(sc.baseX + sc.side * sPurge * 28.0, -1.4 - sPurge * 22.0, -1.0 - sPurge * 65.0);
        sc.mesh.rotation.z = sc.side * sPurge * 3.5;
    });

    const bPurge = L('booster_purge');
    boosterPods.forEach(bp => {
        bp.group.visible = bPurge < 0.98;
        bp.group.position.set(bp.baseX + bp.side * bPurge * 32.0, -0.65 - bPurge * 18.0, -4.5 - bPurge * 85.0);
        bp.group.rotation.y = bp.side * bPurge * 1.2;
    });

    const fPurge = L('fairing_purge');
    fairingPanels.forEach(fp => {
        fp.mesh.visible = fPurge < 0.98;
        fp.mesh.position.set(fp.baseX + fp.vx * fPurge, fp.baseY + fp.vy * fPurge, 1.0 - fPurge * 50.0);
    });

    // 5. エンジン推進炎＆高速スパーク
    const engPwr = L('engine_power');
    plumeRoot.visible = engPwr > 0.02;
    if (plumeRoot.visible) {
        const pulse = 0.94 + Math.sin(now * 0.08) * 0.08;
        plumeRoot.scale.set(pulse, pulse, engPwr * (1.0 + vc * 1.5) * pulse);
        const sArr = sparkGeo.attributes.position.array;
        for (let i = 0; i < sparkCount * 3; i += 3) {
            sArr[i + 2] -= (3.2 + engPwr * 4.8);
            if (sArr[i + 2] < -55.0) {
                sArr[i] = (Math.random() - 0.5) * 2.0;
                sArr[i + 1] = (Math.random() - 0.5) * 2.0;
                sArr[i + 2] = -1.0;
            }
        }
        sparkGeo.attributes.position.needsUpdate = true;
    }

    // 6. マッハコーン・プラズマ・RCS
    const vAlpha = cfg.mach_cone_vfx ? L('vapor_alpha') : 0.0;
    vaporCones.forEach(vcMesh => { vcMesh.material.opacity = vAlpha * 0.78; });
    plasmaEnvelope.material.opacity = cfg.mach_cone_vfx ? L('plasma_alpha') * 0.85 : 0.0;

    const rcsVal = L('rcs_burst');
    rcsJets.forEach(rj => { rj.material.opacity = rcsVal * (0.45 + Math.sin(now * 0.09) * 0.35); });

    // ★7. ワープ重力ブラックアウト収縮 ➔ チェレンコフ爆縮ジャンプ ➔ 多層オーロラワープトンネル
    const wBlack = L('warp_blackout');
    blackoutEl.style.opacity = wBlack * 0.92;
    const wBoom = L('warp_boom');
    flashEl.style.opacity = wBoom * 0.9;

    const wAct = L('warp_active');
    warpTunnelGroup.visible = wAct > 0.05;
    if (warpTunnelGroup.visible) {
        auroraTex.offset.y -= 0.035 * (1.0 + vc);
        auroraCylinder.rotation.z += 0.012;
        const posArr = streakGeo.attributes.position.array;
        const stepZ = 22.0 + vc * 48.0;
        for (let i = 0; i < streakCount; i++) {
            posArr[i * 6 + 2] -= stepZ;
            posArr[i * 6 + 5] -= stepZ;
            if (posArr[i * 6 + 5] < -275.0) {
                const len = posArr[i * 6 + 5] - posArr[i * 6 + 2];
                posArr[i * 6 + 2] = 275.0;
                posArr[i * 6 + 5] = 275.0 + len;
            }
        }
        streakGeo.attributes.position.needsUpdate = true;
        warpTunnelGroup.rotation.z += 0.018;
    }

    boomRing.material.opacity = wBoom * 0.95;
    boomRing.scale.setScalar(1.0 + (1.0 - wBoom) * 42.0);

    // ★8. 目的地スターゲート接近＆氷塊デブリ高速すれ違い＆電磁テザー捕捉
    if (prog >= cfg.flip_timing || f0.phase === "DEBRIS_RETRO_BRAKING" || f0.phase === "STARGATE_DOCKING_LOCKED") {
        destWorld.visible = true;
        const approachRatio = THREE.MathUtils.clamp((1.0 - prog) / (1.0 - cfg.flip_timing), 0.0, 1.0);
        stargateGroup.position.set(0, 0, 12.0 + Math.pow(approachRatio, 1.75) * 3200.0);
        gateInner.rotation.z += 0.035;

        // 氷塊デブリが減速に合わせて機体横を後方へ流れる
        const iceSpeed = vc * 95.0;
        for (let i = 0; i < iceCount; i++) {
            const id = iceData[i];
            id.z -= iceSpeed;
            if (id.z < -250) id.z = 350;
            dummy.position.set(id.x, id.y, id.z);
            dummy.rotation.set(elapsed + i, elapsed * 0.5, i);
            dummy.scale.setScalar(id.s);
            dummy.updateMatrix();
            iceInst.setMatrixAt(i, dummy.matrix);
        }
        iceInst.instanceMatrix.needsUpdate = true;
    } else {
        destWorld.visible = false;
    }

    const tLock = L('tether_lock');
    tetherBeams.forEach(tb => {
        tb.line.material.opacity = tLock * 0.92;
        if (tLock > 0.01) {
            const gZ = stargateGroup.position.z;
            const gx = Math.cos(tb.angle + elapsed * 2.2) * 58.0;
            const gy = Math.sin(tb.angle + elapsed * 2.2) * 58.0;
            tb.line.geometry.setFromPoints([
                new THREE.Vector3(gx, gy, gZ),
                new THREE.Vector3(Math.sin(now * 0.05) * 0.8, Math.cos(now * 0.05) * 0.8, 0)
            ]);
        }
    });

    // 9. Web Audio 変調
    if (actx) {
        rocketGain.gain.setTargetAtTime(engPwr * 0.45, actx.currentTime, 0.08);
        coilGain.gain.setTargetAtTime(f0.phase === "CATAPULT_RAIL_ACCEL" || f0.phase === "LINEAR_COIL_CHARGE" ? 0.25 : 0.0001, actx.currentTime, 0.08);
        coilOsc.frequency.setTargetAtTime(110 + mach * 28, actx.currentTime, 0.08);
        warpGain.gain.setTargetAtTime((L('warp_charge') * 0.35 + wAct * 0.42), actx.currentTime, 0.1);
        warpOsc.frequency.setTargetAtTime(60 + L('warp_charge') * 240 + vc * 390, actx.currentTime, 0.1);
    }

    // 10. CAM 02（フェーズ連動マルチアングル監視カメラ）
    if (f0.phase.includes("VENTING") || f0.phase.includes("CHARGE") || f0.phase === "CATAPULT_RAIL_ACCEL") {
        pipTitleEl.innerText = "CAM 02: RAIL SIDE & MT.FUJI TRACKER";
        cameraPip.position.set(18.0, 2.5, -24.0);
        cameraPip.lookAt(0, 1.0, 40.0);
    } else if (f0.phase.includes("CLIMB") || f0.phase.includes("INSERTION")) {
        pipTitleEl.innerText = "CAM 02: AFT EARTH RECESSION CAM";
        cameraPip.position.set(6.5, 2.2, 8.0);
        cameraPip.lookAt(0, -4.0, -60.0);
    } else if (f0.phase === "WARP_FIELD_COMPRESSION" || f0.phase === "ALCUBIERRE_HYPER_WARP") {
        pipTitleEl.innerText = "CAM 02: DORSAL WARP CORE MONITOR";
        cameraPip.position.set(18.0, 10.5, 25.0);
        cameraPip.lookAt(0, 1.8, -2.5);
    } else {
        pipTitleEl.innerText = "CAM 02: STARGATE ARREST TOWER";
        cameraPip.position.set(45.0, 20.0, stargateGroup.position.z - 38.0);
        cameraPip.lookAt(0, 0, 0);
    }

    controls.update();

    // 11. シングルレンダラー分割描画
    renderer.setViewport(0, 0, W, H);
    renderer.setScissor(0, 0, W, H);
    renderer.setScissorTest(false);
    renderer.render(scene, cameraMain);

    if (pipOpen) {
        const rect = pipBox.getBoundingClientRect();
        const pL = rect.left;
        const pB = H - rect.bottom;
        renderer.setViewport(pL, pB, rect.width, rect.height);
        renderer.setScissor(pL, pB, rect.width, rect.height);
        renderer.setScissorTest(true);
        renderer.render(scene, cameraPip);
    }

    // 12. HUDテレメトリ更新
    document.getElementById('ui-phase').innerText = f0.phase;
    document.getElementById('ui-alt').innerText = altKm > 90000 ? "DEEP SPACE" : `${altKm.toFixed(1)} km`;
    document.getElementById('ui-spd').innerText = vc > 0.02 ? `${vc.toFixed(3)} c` : `M ${mach.toFixed(1)}`;
    const sTime = L('t');
    document.getElementById('ui-clock').innerText = sTime < 0 ? `T${sTime.toFixed(1)}s` : `T+${L('ship_time').toFixed(1)}s`;
    document.getElementById('ui-vc').innerText = vc.toFixed(3);
    document.getElementById('ui-temp').innerText = Math.round(L('temp_k'));
    document.getElementById('ui-g').innerText = L('g').toFixed(1);
    const gamma = 1.0 / Math.sqrt(Math.max(0.001, 1.0 - Math.min(0.999, vc) ** 2));
    document.getElementById('ui-gamma').innerText = gamma.toFixed(2);
    document.getElementById('ui-prog').innerText = (prog * 100).toFixed(1);

    if (f0.phase === "STARGATE_DOCKING_LOCKED") {
        document.getElementById('complete-banner').style.display = 'block';
    }
}
requestAnimationFrame(animate);
});
</script>
</body>
</html>
"""

final_output = (
    html_code.replace("__TIMELINE_JSON__", json.dumps(timeline_data)).replace(
        "__CONFIG_JSON__", json.dumps(sim_config)
    )
)

components.html(final_output, height=860)
