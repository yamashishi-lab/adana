import json
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hyper-Drive Architect: Apex VFX Cinema Edition",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("🛸 Hyper-Drive Architect: Apex VFX Cinema Edition")
st.caption(
    "※ 完全シネマティック改修版：画面スクロール完全透過 / レスポンシブHUD＆CAM02 / 高密度グリーブル・油圧メカ・PBRセルフシャドウ / UnrealBloom映画級発光 / 3D重力レンズ＆スターストレッチ"
)

# =========================================================================
# 🔬 機体・動力炉・目的地・環境データベース
# =========================================================================
VESSEL_DESIGNS = {
    "第6世代極超音速ウェイブライダー『ヴァルキリー SSTO』": {
        "id": "valkyrie",
        "style": "stealth_waverider",
        "catapult_mach": 15.5,
        "desc": "多面体ステルスノーズ、ダイバータレス超音速インテーク、エネルギー脈動コンジット、油圧リンク式12枚アイリス可変ノズルを備えた主力SSTO。軌道上で背面4分割ベイが開き、超伝導デュアル・アルクビエレリングがリフトアップする。",
    },
    "重工業・磁気慣性核融合クルーザー『プロメテウス』": {
        "id": "prometheus",
        "style": "magnetic_fusion",
        "catapult_mach": 12.2,
        "desc": "露出型トラスメインフレームに黄金のMLI断熱球形ヘリウム3タンク8基と極太クライオ冷却配管を懸架。船尾に大型磁気ピンチノズルとジャイロ・ソレノイドを備える深宇宙重巡航艇。",
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
        "metalness": 0.55,
        "roughness": 0.42,
        "plasma_hex": 0xD946EF,
    },
    "液体金属クローム・電磁ミラー装甲 (Mirror Electrum)": {
        "metalness": 0.98,
        "roughness": 0.10,
        "plasma_hex": 0x38BDF8,
    },
    "焼結タングステン・セラミック耐熱複合材 (Thermal Grey)": {
        "metalness": 0.72,
        "roughness": 0.28,
        "plasma_hex": 0x10B981,
    },
}

POWER_CORES = {
    "D-He3 超伝導マグネティック・パルス核融合炉": {
        "flame_hex": 0x38BDF8,
        "core_hex": 0xFFFFFF,
        "spark_hex": 0x7DD3FC,
        "aurora_hex": 0x0284C7,
    },
    "Kerr 人工特異点・ホーキング輻射抽出ドライブ": {
        "flame_hex": 0xA855F7,
        "core_hex": 0xFFFFFF,
        "spark_hex": 0xD8B4FE,
        "aurora_hex": 0x7E22CE,
    },
    "陽電子・反陽子消滅ガンマ線光子トーチ": {
        "flame_hex": 0xF43F5E,
        "core_hex": 0xFFFFFF,
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
        "sun_pos": [-1500, 800, -2500],
        "sun_color": 0x93C5FD,
        "sun_int": 2.2,
        "sky_zenith": "#02050E",
        "sky_horizon": "#0D254C",
        "glow_color": "#1E3A8A",
    },
    "相模湾 第1メガフロート射場 (夜明け・富士シルエット＆マジックアワー)": {
        "mode": "dawn",
        "angle_deg": 28.0,
        "sun_pos": [2200, 650, 2500],
        "sun_color": 0xFFAD60,
        "sun_int": 4.5,
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
    "🎥 シネマカメラ & 目的宙域",
])

with tab1:
  c1, c2 = st.columns(2)
  with c1:
    vessel_sel = st.selectbox("ベース艦種 (Chassis)", list(VESSEL_DESIGNS.keys()))
    vessel_cfg = VESSEL_DESIGNS[vessel_sel]
    armor_sel = st.selectbox("外装マテリアルPBR設定", list(ARMOR_SYSTEMS.keys()))
    armor_cfg = ARMOR_SYSTEMS[armor_sel]
    hull_color = st.color_picker("メイン装甲ベースカラー", "#1e293b")
    belly_color = st.color_picker("下部耐熱カーボンタイル配色", "#0b0f19")
  with c2:
    st.info(f"**構造設計:** {vessel_cfg['desc']}")
    wings_span = st.slider(
        "可変ジオメトリ主翼スパン (m)", 18.0, 42.0, 30.0, step=1.0
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
        "※ メガフロート基地ガントリクレーン・管制塔・サーチライト光柱、正面奥の富士山、発射台ウォーターデフレクターミストを描画。"
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
        "シネマカメラ画角プリセット (※画面タッチ/ドラッグは完全透過で縦スクロール可能)",
        [
            "シネマ・グランドワイド俯瞰 (黄金比：機体＋40m推進炎＋背後基地・富士山・地球を一望)",
            "ディープ・エクストラワイド (超広角：ワープ時空歪曲とオーロラトンネル全体を一望)",
            "チェイス・メカニカルフォーカス (主翼・油圧リンク・ラジエーター変形を高解像度観察)",
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
            "warp_lens": 0.0,
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
        "warp_lens": 0.0,
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
    w_lens = 0.0
    w_active = 0.0
    w_boom = 0.0
    rcs = 0.0
    tether = 0.0
    vib = 0.0
    yaw_deg = 0.0

    if t <= 3.5:
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
      if morph_prog > 0.65:
        w_lens = float(np.sin(((morph_prog - 0.65) / 0.35) * (np.pi / 2)))
      if morph_prog > 0.95:
        w_boom = 1.0
      rcs = 1.0 if morph_prog < 0.25 else 0.0
      vc = 0.008 + w_charge * 0.04
    elif progress < flip_timing:
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
      vib = 0.08
      progress += (vc * 0.026) * dt * 4.0
      if progress >= flip_timing - 0.02:
        w_boom = 1.0
    else:
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
      vib = 0.20 if eng_pwr > 0.5 else 0.03
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
        "warp_lens": float(w_lens),
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
            "warp_lens": 0.0,
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
      "※ 画面クリックでWeb Audioシンセ起動。画面上でのスワイプ・スクロールは完全に下層へ透過します。"
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
# 📺 Three.js ディレクターズカット描画エンジン (Apex Cinema Director's VFX)
# =========================================================================
html_code = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box;}
body,html{
  margin:0;padding:0;width:100%;height:100%;overflow:hidden;
  background:#010308;font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,Roboto,sans-serif;
  color:#f8fafc;user-select:none;
}

/* メインキャンバス：タッチ・スクロールを完全に背後へ透過 */
#webgl-canvas{
  width:100%;height:100%;display:block;position:absolute;top:0;left:0;
  z-index:1;pointer-events:none;touch-action:pan-y;
}

/* 親ラッパー：上部HUDとCAM02をFlex縦積みし、絶対にテキストと被らせない */
.top-ui-container{
  position:absolute;top:0;left:0;width:100%;display:flex;flex-direction:column;
  align-items:center;z-index:30;pointer-events:none;
}

.hud-top{
  width:100%;min-height:46px;
  background:linear-gradient(180deg,rgba(2,6,18,0.94) 0%,rgba(4,12,28,0.80) 100%);
  border-bottom:1px solid rgba(56,189,248,0.3);
  display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;
  padding:6px 18px;gap:8px;box-shadow:0 4px 25px rgba(0,0,0,0.85);
  pointer-events:none;
}
.hud-group{display:flex;align-items:center;flex-wrap:wrap;gap:12px;font-size:11px;letter-spacing:1px;}
.badge{background:rgba(14,165,233,0.18);border:1px solid #38bdf8;color:#38bdf8;padding:2px 8px;border-radius:3px;font-weight:800;}

/* CAM 02：メイン画面と同幅（余白左右12px）のウルトラワイド・デュアルスクリーン */
.pip-window{
  width:calc(100% - 24px);margin:4px 12px 0 12px;height:165px;
  border:2px solid rgba(56,189,248,0.85);border-radius:6px;
  background:rgba(2,6,20,0.65);box-shadow:0 12px 35px rgba(0,0,0,0.95);
  cursor:pointer;overflow:hidden;position:relative;transition:height 0.25s ease;
  pointer-events:auto;
}
.pip-scan{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,0.22),rgba(0,0,0,0.22) 1px,transparent 1px,transparent 3px);pointer-events:none;z-index:42;}
.pip-header{position:absolute;top:6px;left:10px;right:10px;display:flex;justify-content:space-between;align-items:center;z-index:45;pointer-events:none;}
.pip-label{font-size:9.5px;font-weight:800;background:rgba(9,14,28,0.92);padding:3px 8px;border-left:2px solid #38bdf8;letter-spacing:1px;}
.pip-telemetry{font-size:9px;color:#38bdf8;font-family:monospace;background:rgba(9,14,28,0.85);padding:2px 6px;border-radius:2px;}
.pip-toggle{font-size:8px;color:#94a3b8;background:rgba(9,14,28,0.92);padding:3px 6px;cursor:pointer;}
.pip-rec{position:absolute;bottom:6px;right:10px;font-size:9px;color:#f43f5e;font-weight:900;display:flex;align-items:center;gap:5px;z-index:45;pointer-events:none;}
.rec-dot{width:6px;height:6px;border-radius:50%;background:#f43f5e;animation:pulse 1s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.15;}}

.hud-bottom{
  position:absolute;bottom:0;left:0;width:100%;height:68px;
  background:linear-gradient(0deg,rgba(2,6,18,0.94) 0%,rgba(6,13,30,0.82) 100%);
  border-top:1px solid rgba(148,163,184,0.2);
  display:grid;grid-template-columns:repeat(5,1fr);align-items:center;
  padding:0 20px;z-index:20;pointer-events:none;
}
.metric{display:flex;flex-direction:column;border-left:2px solid rgba(56,189,248,0.35);padding-left:10px;}
.metric-lbl{font-size:9px;color:#94a3b8;letter-spacing:1.1px;}
.metric-val{font-size:16px;font-weight:900;color:#f8fafc;margin-top:2px;}

.audio-btn{
  position:absolute;bottom:76px;right:14px;
  background:rgba(8,15,30,0.88);border:1px solid #38bdf8;
  color:#38bdf8;font-size:10px;font-weight:800;padding:6px 14px;
  border-radius:20px;cursor:pointer;z-index:35;letter-spacing:1px;
  pointer-events:auto;
}
#complete-banner{
  display:none;position:absolute;top:220px;left:50%;transform:translateX(-50%);
  background:rgba(6,78,59,0.95);border:2px solid #10b981;
  padding:16px 32px;border-radius:8px;text-align:center;z-index:70;
  box-shadow:0 0 60px rgba(16,185,129,0.7);pointer-events:none;
}
</style>
</head>
<body>
<canvas id="webgl-canvas"></canvas>

<!-- 上部HUDとCAM02をFlex縦積み配置（被りを完全に排除） -->
<div class="top-ui-container">
  <div class="hud-top">
    <div class="hud-group">
      <span class="badge">CINEMA VFX DIRECTOR</span>
      <span>PHASE: <strong id="ui-phase" style="color:#fbbf24;">PAD_STANDBY</strong></span>
    </div>
    <div class="hud-group">
      <span>ALT: <strong id="ui-alt">0.04 km</strong></span>
      <span>VEL: <strong id="ui-spd" style="color:#38bdf8;">M 0.0</strong></span>
      <span>CLOCK: <strong id="ui-clock">T-05.0s</strong></span>
    </div>
  </div>

  <div id="pip-box" class="pip-window" title="クリックでサブモニター折りたたみ">
    <div class="pip-scan"></div>
    <div class="pip-header">
      <div id="pip-title" class="pip-label">CAM 02: ACTIVE TELEMETRY CHASE</div>
      <div id="pip-metric" class="pip-telemetry">EARTH RECESSION: 0 km/s | SCALE: LOW ORBIT</div>
      <div id="pip-btn" class="pip-toggle">[HIDE]</div>
    </div>
    <div class="pip-rec"><div class="rec-dot"></div>OPTICAL TRACKING LOCK</div>
  </div>
</div>

<button id="sound-btn" class="audio-btn">🔊 AUDIO ENGINE ON</button>

<div id="complete-banner">
  <div style="font-size:18px;font-weight:900;color:#6ee7b7;letter-spacing:1.5px;">STARGATE MAGNETIC ARREST COMPLETE</div>
  <div style="font-size:11px;color:#d1fae5;margin-top:4px;">ALL HYPER-DRIVE SUBSYSTEMS NOMINAL / DOCKING LOCKED</div>
</div>

<div class="hud-bottom">
  <div class="metric"><span class="metric-lbl">RELATIVISTIC VEL</span><span class="metric-val"><span id="ui-vc">0.000</span> <small style="font-size:10px;color:#64748b;">c</small></span></div>
  <div class="metric"><span class="metric-lbl">HULL THERMAL</span><span class="metric-val"><span id="ui-temp">288</span> <small style="font-size:10px;color:#64748b;">K</small></span></div>
  <div class="metric"><span class="metric-lbl">G-FORCE</span><span class="metric-val"><span id="ui-g">1.0</span> <small style="font-size:10px;color:#64748b;">G</small></span></div>
  <div class="metric"><span class="metric-lbl">LORENTZ (γ)</span><span class="metric-val"><span id="ui-gamma">1.00</span> <small style="font-size:10px;color:#64748b;">x</small></span></div>
  <div class="metric"><span class="metric-lbl">MISSION PROGRESS</span><span class="metric-val"><span id="ui-prog">0.0</span> <small style="font-size:10px;color:#64748b;">%</small></span></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/EffectComposer.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/RenderPass.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/ShaderPass.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/shaders/CopyShader.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/shaders/LuminosityHighPassShader.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/postprocessing/UnrealBloomPass.js"></script>

<script>
window.addEventListener('DOMContentLoaded', () => {
const frames = __TIMELINE_JSON__;
const cfg = __CONFIG_JSON__;

const canvas = document.getElementById('webgl-canvas');
let W = window.innerWidth, H = window.innerHeight;
const pipBox = document.getElementById('pip-box');
let pipOpen = true;

pipBox.addEventListener('click', (e) => {
    e.stopPropagation();
    pipOpen = !pipOpen;
    pipBox.style.height = pipOpen ? '165px' : '26px';
    document.getElementById('pip-btn').innerText = pipOpen ? '[HIDE]' : '[SHOW]';
});

// =========================================================================
// 1. レンダラー構築＆セルフシャドウ＆映画級発光ポストプロセス (UnrealBloom)
// =========================================================================
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: "high-performance" });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
renderer.setSize(W, H);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.35;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const scene = new THREE.Scene();

// カメラ（メイン ＆ CAM02）
const cameraMain = new THREE.PerspectiveCamera(46, W / H, 0.5, 650000);
const cameraPip = new THREE.PerspectiveCamera(40, (W - 24) / 165, 0.5, 650000);

let baseCamPos = new THREE.Vector3(-155, 62, -210);
let baseTarget = new THREE.Vector3(0, 2.0, -18.0);

if (cfg.cam_preset.includes("エクストラ")) {
    baseCamPos.set(-210, 85, -280);
} else if (cfg.cam_preset.includes("チェイス")) {
    baseCamPos.set(-98, 38, -135);
}
cameraMain.position.copy(baseCamPos);
cameraMain.lookAt(baseTarget);

// UnrealBloomPass：メイン画面とCAM02両方に映画級ブルームを適用
const renderSceneMain = new THREE.RenderPass(scene, cameraMain);
const bloomPass = new THREE.UnrealBloomPass(new THREE.Vector2(W, H), 1.15, 0.42, 0.82);
const composerMain = new THREE.EffectComposer(renderer);
composerMain.addPass(renderSceneMain);
composerMain.addPass(bloomPass);

const renderScenePip = new THREE.RenderPass(scene, cameraPip);
const composerPip = new THREE.EffectComposer(renderer);
composerPip.addPass(renderScenePip);
composerPip.addPass(bloomPass);

window.addEventListener('resize', () => {
    W = window.innerWidth; H = window.innerHeight;
    renderer.setSize(W, H);
    composerMain.setSize(W, H);
    composerPip.setSize(W, H);
    cameraMain.aspect = W / H;
    cameraMain.updateProjectionMatrix();
    cameraPip.aspect = (W - 24) / 165;
    cameraPip.updateProjectionMatrix();
});

// ライティング
const sunLight = new THREE.DirectionalLight(cfg.env.sun_color, cfg.env.sun_int);
sunLight.position.set(...cfg.env.sun_pos);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 10;
sunLight.shadow.camera.far = 4500;
sunLight.shadow.camera.left = -65;
sunLight.shadow.camera.right = 65;
sunLight.shadow.camera.top = 65;
sunLight.shadow.camera.bottom = -65;
sunLight.shadow.bias = -0.0005;
scene.add(sunLight);

const hemiLight = new THREE.HemisphereLight(0x93c5fd, 0x020617, 1.4);
scene.add(hemiLight);

const underRimLight = new THREE.PointLight(0x38bdf8, 3.2, 90);
underRimLight.position.set(0, -12, -8);
scene.add(underRimLight);

// =========================================================================
// 2. Web Audio シンセサイザー
// =========================================================================
let actx = null, rocketGain = null, coilOsc = null, coilGain = null, warpOsc = null, warpGain = null;
const soundBtn = document.getElementById('sound-btn');
soundBtn.addEventListener('click', () => {
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
    filter.frequency.value = 320;
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
    cFilter.frequency.value = 460;
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

    soundBtn.innerText = "🔊 AUDIO ENGAGED";
    soundBtn.style.borderColor = "#10b981";
    soundBtn.style.color = "#10b981";
});

// =========================================================================
// 3. プロシージャルPBR環境マップ＆ウェザリングテクスチャ
// =========================================================================
function makeSkyEnvTexture() {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 512;
    const ctx = c.getContext('2d');
    const g = ctx.createLinearGradient(0, 0, 0, 512);
    g.addColorStop(0, cfg.env.sky_zenith);
    g.addColorStop(0.48, cfg.env.sky_horizon);
    g.addColorStop(0.50, '#ffffff');
    g.addColorStop(0.53, '#1e293b');
    g.addColorStop(1, '#020617');
    ctx.fillStyle = g; ctx.fillRect(0, 0, 1024, 512);
    ctx.fillStyle = '#ffffff';
    ctx.beginPath(); ctx.arc(400, 180, 24, 0, Math.PI * 2); ctx.fill();
    const tex = new THREE.CanvasTexture(c);
    tex.mapping = THREE.EquirectangularReflectionMapping;
    return tex;
}
scene.environment = makeSkyEnvTexture();

function makeDetailedHullTexture() {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 1024;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#737373'; ctx.fillRect(0, 0, 1024, 1024);

    for (let x = 0; x < 1024; x += 64) {
        for (let y = 0; y < 1024; y += 32) {
            const v = 95 + Math.floor(Math.random() * 55);
            ctx.fillStyle = `rgb(${v},${v},${v})`;
            ctx.fillRect(x + 2, y + 2, 60, 28);
            ctx.fillStyle = '#262626';
            ctx.fillRect(x + 5, y + 5, 2, 2);
            ctx.fillRect(x + 56, y + 5, 2, 2);
            ctx.fillRect(x + 5, y + 24, 2, 2);
            ctx.fillRect(x + 56, y + 24, 2, 2);
        }
    }
    ctx.strokeStyle = '#171717'; ctx.lineWidth = 3;
    for (let x = 0; x <= 1024; x += 64) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 1024); ctx.stroke(); }
    for (let y = 0; y <= 1024; y += 32) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(1024, y); ctx.stroke(); }

    const grad = ctx.createLinearGradient(0, 1024, 0, 0);
    grad.addColorStop(0, 'rgba(15,23,42,0.45)');
    grad.addColorStop(0.5, 'rgba(0,0,0,0)');
    ctx.fillStyle = grad; ctx.fillRect(0, 0, 1024, 1024);

    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(4, 4);
    return tex;
}
const hullPbrTex = makeDetailedHullTexture();

function makeTileTexture() {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#111827'; ctx.fillRect(0, 0, 512, 512);
    ctx.strokeStyle = '#030712'; ctx.lineWidth = 3;
    for (let y = 0; y < 512; y += 16) {
        const off = (y / 16) % 2 === 0 ? 0 : 12;
        for (let x = -12; x < 512; x += 24) { ctx.strokeRect(x + off, y, 22, 14); }
    }
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(8, 8);
    return tex;
}
const tileTex = makeTileTexture();

// PBRマテリアル
const matHull = new THREE.MeshStandardMaterial({
    color: cfg.hull_color, metalness: cfg.metalness, roughness: cfg.roughness,
    bumpMap: hullPbrTex, bumpScale: 0.04, roughnessMap: hullPbrTex
});
const matBellyTile = new THREE.MeshStandardMaterial({
    color: cfg.belly_color, metalness: 0.25, roughness: 0.8,
    bumpMap: tileTex, bumpScale: 0.06
});
const matTitaniumFrame = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.92, roughness: 0.22 });
const matPistonRod = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.98, roughness: 0.08 });
const matDarkAlloy = new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.94, roughness: 0.18 });
const matGoldMLI = new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.96, roughness: 0.22, bumpMap: tileTex, bumpScale: 0.02 });
const matCopperCoil = new THREE.MeshStandardMaterial({ color: 0xd97706, metalness: 0.95, roughness: 0.15 });
const matCryoPipe = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.85, roughness: 0.12 });
const matCanopy = new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, metalness: 0.95, roughness: 0.03, transparent: true, opacity: 0.42, clearcoat: 1.0 });
const matConduitPulse = new THREE.MeshBasicMaterial({ color: cfg.flame_hex });
const matRadiator = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.82, roughness: 0.28, emissive: 0xef4444, emissiveIntensity: 0.0 });
const matNoseAblation = new THREE.MeshBasicMaterial({ color: 0xf97316, transparent: true, opacity: 0.0 });

// =========================================================================
// 4. 宇宙船の超高密度モデリング（コックピット内装・配線・ストロボ等）
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
const strobeLeds = [];
const warpRingAssembly = new THREE.Group();
shipMeshGroup.add(warpRingAssembly);

// A. 内部チタンスパイン＆配線ハーネス
const spineCore = new THREE.Mesh(new THREE.BoxGeometry(2.6, 1.4, 30.0), matDarkAlloy);
spineCore.castShadow = true; spineCore.receiveShadow = true;
shipMeshGroup.add(spineCore);

// 露出配線ハーネス（黒と黄のケーブル束）
for (let side of [-1, 1]) {
    for (let c = 0; c < 3; c++) {
        const wire = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 26.0, 8), matDarkAlloy);
        wire.rotation.x = Math.PI / 2;
        wire.position.set(side * (1.3 + c * 0.12), -0.3 + c * 0.1, -1.0);
        shipMeshGroup.add(wire);
    }
}

// B. コックピット内部造形（キャノピー透過時に見えるシート＆ホログラム計器）
const cockpitGroup = new THREE.Group();
cockpitGroup.position.set(0, 0.7, 7.5);
shipMeshGroup.add(cockpitGroup);

for (let s of [-0.4, 0.4]) {
    const seat = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.9, 0.6), matDarkAlloy);
    seat.position.set(s, 0, 0);
    cockpitGroup.add(seat);
}
const consoleHolo = new THREE.Mesh(
    new THREE.PlaneGeometry(1.2, 0.35),
    new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.85, side: THREE.DoubleSide })
);
consoleHolo.rotation.x = -0.5;
consoleHolo.position.set(0, 0.25, 1.2);
cockpitGroup.add(consoleHolo);

// C. 艦種別外装
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
    noseMesh.castShadow = true; noseMesh.receiveShadow = true;
    shipMeshGroup.add(noseMesh);

    // 機首アブレーション（大気摩擦熱）グローコーン
    const noseGlow = new THREE.Mesh(new THREE.ConeGeometry(1.2, 4.0, 16), matNoseAblation);
    noseGlow.rotation.x = -Math.PI / 2;
    noseGlow.position.set(0, 0.1, 19.5);
    shipMeshGroup.add(noseGlow);

    const bellyMesh = new THREE.Mesh(noseGeo, matBellyTile);
    bellyMesh.scale.set(0.98, 0.45, 0.98);
    bellyMesh.position.set(0, -0.48, 3.5);
    bellyMesh.castShadow = true; bellyMesh.receiveShadow = true;
    shipMeshGroup.add(bellyMesh);

    for (let s of [-1, 1]) {
        const nacelle = new THREE.Mesh(new THREE.BoxGeometry(2.5, 1.9, 19.5), matHull);
        nacelle.position.set(s * 3.1, -0.15, -3.5);
        nacelle.castShadow = true; nacelle.receiveShadow = true;
        shipMeshGroup.add(nacelle);

        const vTail = new THREE.Mesh(new THREE.BoxGeometry(0.22, 4.8, 6.5), matHull);
        vTail.position.set(s * 3.8, 2.2, -10.8);
        vTail.rotation.z = -s * 0.32;
        vTail.castShadow = true;
        shipMeshGroup.add(vTail);

        // 垂直尾翼先端のストロボライト
        const strobe = new THREE.Mesh(new THREE.SphereGeometry(0.12, 8, 8), new THREE.MeshBasicMaterial({ color: 0xffffff }));
        strobe.position.set(s * 4.6, 4.2, -11.5);
        shipMeshGroup.add(strobe);
        strobeLeds.push(strobe);
    }
} else if (cfg.style === "magnetic_fusion") {
    const cmdPod = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 3.4, 13.0, 8), matHull);
    cmdPod.rotation.x = Math.PI / 2;
    cmdPod.scale.set(1.3, 0.75, 1.0);
    cmdPod.position.set(0, 0.2, 10.5);
    cmdPod.castShadow = true;
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
            sphereTank.castShadow = true;
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
        fPanel.castShadow = true;
        shipMeshGroup.add(fPanel);
        fairingPanels.push({ mesh: fPanel, baseX: fPanel.position.x, baseY: fPanel.position.y, vx: Math.cos(ang) * 22, vy: Math.sin(ang) * 22 });
    }
}

// D. キャノピー
const canopyGlass = new THREE.Mesh(new THREE.ConeGeometry(1.35, 7.5, 16), matCanopy);
canopyGlass.scale.set(1.0, 0.48, 1.6);
canopyGlass.rotation.x = Math.PI / 2;
canopyGlass.position.set(0, 0.95, 8.8);
canopyGlass.castShadow = true;
shipMeshGroup.add(canopyGlass);

// E. 可変主翼＆翼端ナビゲーションストロボ（赤・緑）
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
    wMesh.castShadow = true; wMesh.receiveShadow = true;
    pivot.add(wMesh);

    // 翼端ストロボ（右舷緑、左舷赤）
    const tipLed = new THREE.Mesh(new THREE.SphereGeometry(0.16, 8, 8), new THREE.MeshBasicMaterial({ color: s > 0 ? 0x10b981 : 0xef4444 }));
    tipLed.position.set(s * (halfSpan - 3.4), 0, -5.5);
    pivot.add(tipLed);
    strobeLeds.push(tipLed);

    wingPivots.push({ group: pivot, side: s });
}

// F. ペイロードベイ
for (let s of [-1, 1]) {
    for (let zOff of [-6.0, 1.0]) {
        const doorPivot = new THREE.Group();
        doorPivot.position.set(s * 2.4, 1.15, zOff);
        shipMeshGroup.add(doorPivot);

        const doorPanel = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.25, 6.4), matHull);
        doorPanel.position.set(-s * 1.1, 0, 0);
        doorPanel.castShadow = true;
        doorPivot.add(doorPanel);
        bayDoors.push({ pivot: doorPivot, side: s });
    }
}

// G. ワープリング＆3D重力レンズ
warpRingAssembly.position.set(0, -0.8, -2.5);
const ringPylon = new THREE.Mesh(new THREE.BoxGeometry(1.6, 3.8, 4.5), matTitaniumFrame);
ringPylon.position.set(0, -1.8, 0);
warpRingAssembly.add(ringPylon);

const outerWarpRing = new THREE.Mesh(new THREE.TorusGeometry(6.8, 0.42, 20, 64), matTitaniumFrame);
const innerWarpCoil = new THREE.Mesh(new THREE.TorusGeometry(6.1, 0.28, 16, 64), matCopperCoil);
outerWarpRing.castShadow = true;
warpRingAssembly.add(outerWarpRing);
warpRingAssembly.add(innerWarpCoil);

const gravLensMat = new THREE.ShaderMaterial({
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
        uniform float uAlpha;
        void main() {
            vec3 v = normalize(vViewPos);
            float fres = pow(1.0 - abs(dot(vNormal, v)), 3.5);
            vec3 col = mix(vec3(0.01, 0.05, 0.15), vec3(0.22, 0.75, 0.98), fres);
            gl_FragColor = vec4(col, fres * uAlpha * 0.95);
        }
    `,
    uniforms: { uAlpha: { value: 0.0 } },
    transparent: true,
    blending: THREE.AdditiveBlending,
    side: THREE.DoubleSide,
    depthWrite: false
});
const gravLensSphere = new THREE.Mesh(new THREE.SphereGeometry(5.2, 32, 32), gravLensMat);
warpRingAssembly.add(gravLensSphere);

// H. ラジエーター
for (let r = 0; r < cfg.radiator_fins; r++) {
    const s = (r % 2 === 0) ? 1 : -1;
    const row = Math.floor(r / 2);
    const rPivot = new THREE.Group();
    rPivot.position.set(s * 2.2, 0.8, -3.5 - row * 2.8);
    shipMeshGroup.add(rPivot);

    const rBlade = new THREE.Mesh(new THREE.BoxGeometry(4.8, 0.08, 1.8), matRadiator);
    rBlade.position.set(s * 2.4, 0, 0);
    rBlade.castShadow = true;
    rPivot.add(rBlade);
    radiatorPanels.push({ pivot: rPivot, side: s });
}

// I. バーナー超精密化（2重反転ペタル・再生冷却パイプ・タービン・バレルショック）
const nozzleRoot = new THREE.Group();
nozzleRoot.position.set(0, 0, -14.2);
shipMeshGroup.add(nozzleRoot);

// 燃焼室スロートと回転タービン
const turbineDisc = new THREE.Mesh(
    new THREE.RingGeometry(0.2, 2.2, 24),
    new THREE.MeshStandardMaterial({ color: 0xd97706, metalness: 0.95, roughness: 0.1, emissive: cfg.flame_hex, emissiveIntensity: 0.6 })
);
turbineDisc.position.z = 0.5;
nozzleRoot.add(turbineDisc);

// 再生冷却配管リング
const cryoManifold = new THREE.Mesh(new THREE.TorusGeometry(2.7, 0.14, 12, 32), matCryoPipe);
cryoManifold.position.z = -0.3;
nozzleRoot.add(cryoManifold);

for (let i = 0; i < 12; i++) {
    const ang = (i / 12) * Math.PI * 2;
    const petalPivot = new THREE.Group();
    petalPivot.position.set(Math.cos(ang) * 2.5, Math.sin(ang) * 2.5, -1.0);
    petalPivot.rotation.z = ang;
    nozzleRoot.add(petalPivot);

    // 外装チタンペタル
    const outerPetal = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.12, 3.2), matTitaniumFrame);
    outerPetal.position.set(0, 0.08, -1.4);
    outerPetal.castShadow = true;
    petalPivot.add(outerPetal);

    // 内側セラミック耐熱ライナー
    const innerLiner = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.08, 3.0), matBellyTile);
    innerLiner.position.set(0, -0.04, -1.4);
    petalPivot.add(innerLiner);

    // 背面U字冷却パイプ
    const uPipe = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 2.8, 6), matPistonRod);
    uPipe.rotation.x = Math.PI / 2;
    uPipe.position.set(0, 0.16, -1.4);
    petalPivot.add(uPipe);

    irisPaddles.push(petalPivot);
}

// サボ＆ブースター
if (cfg.aux_boosters) {
    for (let s of [-1, 1]) {
        const bPod = new THREE.Group();
        bPod.position.set(s * 5.8, -0.65, -4.5);
        shipMeshGroup.add(bPod);

        const bBody = new THREE.Mesh(new THREE.CylinderGeometry(0.85, 1.05, 14.5, 20), matBellyTile);
        bBody.rotation.x = Math.PI / 2;
        bBody.castShadow = true;
        bPod.add(bBody);

        boosterPods.push({ group: bPod, baseX: s * 5.8, side: s });
    }
}
for (let s of [-1, 1]) {
    const sabot = new THREE.Mesh(new THREE.BoxGeometry(2.2, 1.1, 7.5), matDarkAlloy);
    sabot.position.set(s * 3.8, -1.4, -1.0);
    sabot.castShadow = true;
    shipMeshGroup.add(sabot);
    sabotClamps.push({ mesh: sabot, baseX: s * 3.8, side: s });
}

// J. プラズマ噴射炎＆立体バレルショックダイヤモンド
const plumeRoot = new THREE.Group();
plumeRoot.position.set(0, 0, -16.5);
shipMeshGroup.add(plumeRoot);

const innerCoreBeam = new THREE.Mesh(
    new THREE.CylinderGeometry(0.45, 2.4, 34.0, 24, 1, true),
    new THREE.MeshBasicMaterial({ color: cfg.core_hex, transparent: true, opacity: 0.95, blending: THREE.AdditiveBlending, side: THREE.DoubleSide })
);
innerCoreBeam.rotation.x = Math.PI / 2;
innerCoreBeam.position.z = -17.0;
plumeRoot.add(innerCoreBeam);

const outerPlasmaCone = new THREE.Mesh(
    new THREE.ConeGeometry(5.2, 48.0, 28, 1, true),
    new THREE.MeshBasicMaterial({ color: cfg.flame_hex, transparent: true, opacity: 0.68, blending: THREE.AdditiveBlending, side: THREE.DoubleSide })
);
outerPlasmaCone.rotation.x = Math.PI / 2;
outerPlasmaCone.position.z = -24.0;
plumeRoot.add(outerPlasmaCone);

// 立体バレルショック（樽型ショックダイヤモンド）
const shockBarrels = [];
for (let d = 0; d < cfg.shock_count; d++) {
    const barrel = new THREE.Mesh(
        new THREE.SphereGeometry(1.6 - d * 0.18, 16, 16),
        new THREE.MeshBasicMaterial({ color: cfg.spark_hex, transparent: true, opacity: 0.88, blending: THREE.AdditiveBlending })
    );
    barrel.scale.set(1.0, 1.0, 2.2);
    barrel.position.set(0, 0, -3.5 - d * 5.4);
    plumeRoot.add(barrel);
    shockBarrels.push(barrel);
}

// アブレーション火花粒子（成層圏突破時の溶融火花）
const ablatCount = 180;
const ablatGeo = new THREE.BufferGeometry();
const ablatPos = new Float32Array(ablatCount * 3);
for (let i = 0; i < ablatCount; i++) {
    ablatPos[i * 3] = (Math.random() - 0.5) * 6.0;
    ablatPos[i * 3 + 1] = (Math.random() - 0.5) * 3.0;
    ablatPos[i * 3 + 2] = -Math.random() * 45.0;
}
ablatGeo.setAttribute('position', new THREE.BufferAttribute(ablatPos, 3));
const ablatSystem = new THREE.Points(ablatGeo, new THREE.PointsMaterial({ color: 0xf97316, size: 2.2, blending: THREE.AdditiveBlending, transparent: true, opacity: 0.0 }));
shipMeshGroup.add(ablatSystem);

// =========================================================================
// 5. 基地・海面・雲海・富士山
// =========================================================================
const launchWorld = new THREE.Group();
scene.add(launchWorld);

const launchPitchGroup = new THREE.Group();
const radAngle = THREE.MathUtils.degToRad(cfg.env.angle_deg);
launchPitchGroup.rotation.x = -radAngle;
launchWorld.add(launchPitchGroup);

const dummy = new THREE.Object3D();
const segCount = 200;
const archInst = new THREE.InstancedMesh(new THREE.TorusGeometry(9.5, 0.45, 10, 24, Math.PI), matTitaniumFrame, segCount);
archInst.castShadow = true;
for (let i = 0; i < segCount; i++) {
    dummy.position.set(0, -1.8, i * 16.0 - 40.0);
    dummy.updateMatrix();
    archInst.setMatrixAt(i, dummy.matrix);
}
launchPitchGroup.add(archInst);

const mainGirder = new THREE.Mesh(new THREE.BoxGeometry(14.5, 2.4, 3400), matDarkAlloy);
mainGirder.position.set(0, -3.2, 1650);
mainGirder.receiveShadow = true;
launchPitchGroup.add(mainGirder);

const towerCount = 36;
const towerInst = new THREE.InstancedMesh(new THREE.BoxGeometry(2.5, 36.0, 2.5), matTitaniumFrame, towerCount);
towerInst.castShadow = true;
for (let i = 0; i < towerCount; i++) {
    const side = (i % 2 === 0) ? 1 : -1;
    dummy.position.set(side * 25.0, 12.0, Math.floor(i / 2) * 95.0 - 20.0);
    dummy.updateMatrix();
    towerInst.setMatrixAt(i, dummy.matrix);
}
launchPitchGroup.add(towerInst);

const groundEnvGroup = new THREE.Group();
launchWorld.add(groundEnvGroup);

const seaMesh = new THREE.Mesh(
    new THREE.PlaneGeometry(160000, 160000),
    new THREE.MeshStandardMaterial({ color: 0x030d1c, metalness: 0.92, roughness: 0.12 })
);
seaMesh.rotation.x = -Math.PI / 2;
seaMesh.position.y = -45.0;
groundEnvGroup.add(seaMesh);

const fujiGroup = new THREE.Group();
fujiGroup.position.set(6500, -45, 16500);
groundEnvGroup.add(fujiGroup);
const fujiPts = [];
for (let i = 0; i <= 24; i++) {
    const t = i / 24;
    fujiPts.push(new THREE.Vector2(Math.pow(1 - t, 2.1) * 14500 + 850, t * 3776));
}
const fujiMount = new THREE.Mesh(new THREE.LatheGeometry(fujiPts, 64), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.85 }));
fujiGroup.add(fujiMount);

const cityGeo = new THREE.BufferGeometry();
const cityPos = new Float32Array(5000 * 3);
const cityCol = new Float32Array(5000 * 3);
for (let i = 0; i < 5000; i++) {
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

// =========================================================================
// 6. 地球・軌道ステーション・月（超高速追い越しスケールマーカー）
// =========================================================================
const earthGroup = new THREE.Group();
scene.add(earthGroup);

function makePlanetSurfaceTex() {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 512;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#061a38'; ctx.fillRect(0, 0, 1024, 512);
    ctx.fillStyle = '#112a22';
    for (let i = 0; i < 90; i++) {
        ctx.beginPath();
        ctx.arc(Math.random() * 1024, Math.random() * 512, 20 + Math.random() * 70, 0, Math.PI * 2);
        ctx.fill();
    }
    return new THREE.CanvasTexture(c);
}
const earthSphere = new THREE.Mesh(new THREE.SphereGeometry(25000, 64, 64), new THREE.MeshStandardMaterial({ map: makePlanetSurfaceTex(), roughness: 0.55 }));
earthGroup.add(earthSphere);

// 低軌道宇宙ステーション（通過スケールマーカー）
const stationMarker = new THREE.Mesh(new THREE.TorusGeometry(32.0, 4.0, 12, 32), matTitaniumFrame);
stationMarker.position.set(40.0, -120.0, -450.0);
scene.add(stationMarker);

// 月（38万kmのスケールマーカー：ワープ直前に超高速で後方へすっ飛ぶ）
const moonMesh = new THREE.Mesh(new THREE.SphereGeometry(6800, 32, 32), new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.85 }));
scene.add(moonMesh);

// =========================================================================
// 7. ワープ演出（スターストレッチ＆螺旋プラズマリボン）
// =========================================================================
const warpGroup = new THREE.Group();
warpGroup.visible = false;
scene.add(warpGroup);

const ribbonCount = 6;
for (let r = 0; r < ribbonCount; r++) {
    const rPts = [];
    for (let z = -250; z <= 250; z += 10) {
        const ang = (z * 0.05) + (r / ribbonCount) * Math.PI * 2;
        rPts.push(new THREE.Vector3(Math.cos(ang) * 22.0, Math.sin(ang) * 22.0, z));
    }
    const rGeo = new THREE.BufferGeometry().setFromPoints(rPts);
    warpGroup.add(new THREE.Line(rGeo, new THREE.LineBasicMaterial({ color: cfg.aurora_hex, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending })));
}

const starCount = 3000;
const starGeo = new THREE.BufferGeometry();
const starPos = new Float32Array(starCount * 6);
for (let i = 0; i < starCount; i++) {
    const ang = Math.random() * Math.PI * 2;
    const rad = 25.0 + Math.random() * 180.0;
    const z = (Math.random() - 0.5) * 600.0;
    const x = Math.cos(ang) * rad, y = Math.sin(ang) * rad;
    starPos[i * 6] = x; starPos[i * 6 + 1] = y; starPos[i * 6 + 2] = z;
    starPos[i * 6 + 3] = x; starPos[i * 6 + 4] = y; starPos[i * 6 + 5] = z + 1.0;
}
starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
const starLines = new THREE.LineSegments(starGeo, new THREE.LineBasicMaterial({ color: 0x7dd3fc, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending }));
warpGroup.add(starLines);

const destWorld = new THREE.Group();
destWorld.visible = false;
scene.add(destWorld);

const destPlanet = new THREE.Mesh(new THREE.SphereGeometry(3200, 64, 64), new THREE.MeshStandardMaterial({ color: cfg.dest_color, roughness: 0.75 }));
destPlanet.position.set(700, -450, 5200);
destWorld.add(destPlanet);

const stargateGroup = new THREE.Group();
destWorld.add(stargateGroup);
const gateOuter = new THREE.Mesh(new THREE.TorusGeometry(65, 4.8, 20, 64), matTitaniumFrame);
gateOuter.castShadow = true;
stargateGroup.add(gateOuter);

// =========================================================================
// 8. 60fps アニメーションループ（CAM 02アクティブカメラワーク）
// =========================================================================
const startTime = performance.now();
const pipTitleEl = document.getElementById('pip-title');
const pipMetricEl = document.getElementById('pip-metric');

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

    // 機体姿勢＆慣性ラグ
    const lagZ = -Math.min(18.0, L('g') * 1.2);
    shipMeshGroup.position.set(
        Math.sin(now * 0.045) * vib * 0.35,
        Math.cos(now * 0.055) * vib * 0.35,
        lagZ + Math.sin(now * 0.035) * vib * 0.35
    );
    shipMeshGroup.rotation.set(-THREE.MathUtils.degToRad(pitchDeg), THREE.MathUtils.degToRad(yawDeg), 0);

    // ダイナミックFOV
    cameraMain.fov = 46.0 + vc * 24.0 + (mach > 5 ? 4.0 : 0.0);
    cameraMain.updateProjectionMatrix();

    // ストロボ点滅
    const flashState = (Math.floor(now * 0.004) % 2 === 0);
    strobeLeds.forEach(led => { led.visible = flashState; });

    // アブレーション熱（マッハ15突破時）
    const ablatIntensity = THREE.MathUtils.clamp((mach - 8.0) / 16.0, 0.0, 1.0);
    matNoseAblation.opacity = ablatIntensity * 0.85;
    ablatSystem.material.opacity = ablatIntensity * 0.9;
    if (ablatIntensity > 0.05) {
        const ap = ablatGeo.attributes.position.array;
        for (let i = 0; i < ablatCount * 3; i += 3) {
            ap[i + 2] -= 4.2;
            if (ap[i + 2] < -45.0) {
                ap[i] = (Math.random() - 0.5) * 5.0;
                ap[i + 1] = (Math.random() - 0.5) * 2.5;
                ap[i + 2] = 16.0;
            }
        }
        ablatGeo.attributes.position.needsUpdate = true;
    }

    // 地上界
    if (altKm < 110.0 && f0.phase !== "WARP_FIELD_COMPRESSION" && f0.phase !== "ALCUBIERRE_HYPER_WARP") {
        launchWorld.visible = true;
        launchPitchGroup.position.set(0, 0, -distM);
        groundEnvGroup.position.set(0, -altKm * 1000.0 + 40.0, -distM * Math.cos(radAngle));
    } else {
        launchWorld.visible = false;
    }

    // 地球・月・軌道ステーションの超高速後退（スケールマーカー）
    if (prog < 0.28) {
        earthGroup.visible = true;
        const warpRecede = Math.pow(Math.max(0, prog - 0.05) * 18.0, 3.0);
        earthGroup.position.set(0, -25050 - altKm * 120.0 - warpRecede * 35000.0, -4000 - distM * 0.6 - warpRecede * 95000.0);
        earthGroup.scale.setScalar(Math.max(0.001, 1.0 / (1.0 + warpRecede * 1.8)));

        // 月（38万km）の通過
        moonMesh.visible = (altKm > 100.0);
        const moonZ = -12000 - (prog / 0.12) * 80000.0;
        moonMesh.position.set(8000, 3500, moonZ);

        // 軌道ステーションのすれ違い
        stationMarker.visible = (altKm > 80.0 && prog < 0.05);
        stationMarker.position.z = -150.0 - (altKm - 80.0) * 85.0;
    } else {
        earthGroup.visible = false;
        moonMesh.visible = false;
        stationMarker.visible = false;
    }

    // メカギミック展開
    wingPivots.forEach(wp => { wp.group.rotation.y = wp.side * L('wing_sweep') * 0.32; });
    bayDoors.forEach(bd => { bd.pivot.rotation.z = bd.side * L('bay_open') * 1.35; });
    radiatorPanels.forEach(rp => { rp.pivot.rotation.z = rp.side * (1.0 - L('rad_deploy')) * 1.45; });
    irisPaddles.forEach(ip => { ip.rotation.x = -0.35 + L('nozzle_open') * 0.48; });

    warpRingAssembly.position.y = -0.8 + L('ring_lift') * 4.2;
    innerWarpCoil.rotation.z += 0.02 + L('warp_charge') * 0.35;
    gravLensMat.uniforms.uAlpha.value = L('warp_lens');

    // バーナー推進炎＆バレルショック脈動
    const engPwr = L('engine_power');
    plumeRoot.visible = engPwr > 0.02;
    turbineDisc.rotation.z += 0.25 * (1.0 + engPwr * 2.0);
    if (plumeRoot.visible) {
        const pulse = 0.95 + Math.sin(now * 0.08) * 0.05;
        plumeRoot.scale.set(pulse, pulse, engPwr * (1.0 + vc * 1.5) * pulse);
        shockBarrels.forEach((sb, idx) => {
            const bPulse = 1.0 + Math.sin(now * 0.12 + idx * 0.8) * 0.12;
            sb.scale.set(bPulse, bPulse, 2.2 * bPulse);
        });
    }

    // ワープ（スターストレッチ）
    const wAct = L('warp_active');
    warpGroup.visible = wAct > 0.05;
    if (warpGroup.visible) {
        warpGroup.rotation.z += 0.025;
        const sArr = starGeo.attributes.position.array;
        const stretchLen = 35.0 + vc * 140.0;
        for (let i = 0; i < starCount; i++) {
            let z = sArr[i * 6 + 2] - (18.0 + vc * 42.0);
            if (z < -300.0) z = 300.0;
            sArr[i * 6 + 2] = z;
            sArr[i * 6 + 5] = z + stretchLen;
        }
        starGeo.attributes.position.needsUpdate = true;
    }

    // 目的地
    if (prog >= cfg.flip_timing) {
        destWorld.visible = true;
        const approachRatio = THREE.MathUtils.clamp((1.0 - prog) / (1.0 - cfg.flip_timing), 0.0, 1.0);
        stargateGroup.position.set(0, 0, 12.0 + Math.pow(approachRatio, 1.75) * 3200.0);
    } else {
        destWorld.visible = false;
    }

    // Web Audio
    if (actx) {
        rocketGain.gain.setTargetAtTime(engPwr * 0.42, actx.currentTime, 0.08);
        coilGain.gain.setTargetAtTime(f0.phase.includes("COIL") || f0.phase.includes("RAIL") ? 0.22 : 0.0001, actx.currentTime, 0.08);
        warpGain.gain.setTargetAtTime(wAct * 0.38 + L('warp_lens') * 0.25, actx.currentTime, 0.1);
        warpOsc.frequency.setTargetAtTime(60 + vc * 380, actx.currentTime, 0.1);
    }

    // ★CAM 02 アクティブ・カメラワーク＆速度スケール演出
    const recessionKms = vc > 0.01 ? (vc * 299792).toFixed(0) : (mach * 0.34).toFixed(1);
    if (f0.phase.includes("STANDBY") || f0.phase.includes("CHARGE")) {
        pipTitleEl.innerText = "CAM 02: LAUNCH RAIL FLY-BY TRACKER";
        pipMetricEl.innerText = `RECESSION: 0 km/s | MACH: ${mach.toFixed(1)} | PAD LOCK`;
        cameraPip.position.set(32.0, 4.0, -18.0);
        cameraPip.lookAt(0, 1.0, 20.0);
    } else if (f0.phase === "CATAPULT_RAIL_ACCEL") {
        // 機体を横切る超高速フライバイ（カメラが首を振る）
        pipTitleEl.innerText = "CAM 02: CATAPULT SUPERSONIC FLY-BY";
        pipMetricEl.innerText = `RECESSION: ${recessionKms} km/s | MACH: ${mach.toFixed(1)} | RAIL EXIT`;
        cameraPip.position.set(24.0, 2.5, 45.0 - distM * 0.05);
        cameraPip.lookAt(shipMeshGroup.position);
    } else if (f0.phase.includes("CLIMB") || f0.phase.includes("INSERTION")) {
        // 前方から地球を見下ろすアングル（地球・月が後方へ吹き飛ぶ）
        pipTitleEl.innerText = "CAM 02: ORBITAL DEPARTURE & EARTH RECESSION";
        pipMetricEl.innerText = `EARTH RECESSION: ${recessionKms} km/s | ALT: ${altKm.toFixed(0)} km | MOON APPROACH`;
        cameraPip.position.set(0, 18.0, 48.0);
        cameraPip.lookAt(earthGroup.position.x, earthGroup.position.y * 0.2, earthGroup.position.z);
    } else if (f0.phase.includes("WARP")) {
        // ワープ突入時の置き去り追従（カメラが引っ張られる）
        pipTitleEl.innerText = "CAM 02: ALCUBIERRE WARP FIELD BOW SHOCK";
        pipMetricEl.innerText = `WARP SPEED: ${vc.toFixed(3)} c (${recessionKms} km/s) | LORENTZ: ${(1.0/Math.sqrt(Math.max(0.001,1.0-vc*vc))).toFixed(2)}x`;
        const lagCamZ = -80.0 + (1.0 - L('warp_lens')) * 55.0;
        cameraPip.position.set(22.0, 15.0, lagCamZ);
        cameraPip.lookAt(0, 1.0, 0);
    } else {
        pipTitleEl.innerText = "CAM 02: STARGATE APPROACH & ARREST LOCK";
        pipMetricEl.innerText = `APPROACH: ${recessionKms} km/s | TETHER CAPTURE READY`;
        cameraPip.position.set(50.0, 25.0, stargateGroup.position.z - 50.0);
        cameraPip.lookAt(0, 0, 0);
    }

    // レンダリング（メイン画面）
    renderer.setViewport(0, 0, W, H);
    renderer.setScissor(0, 0, W, H);
    renderer.setScissorTest(false);
    composerMain.render();

    // レンダリング（CAM 02：ブルーム適用ウルトラワイド描画）
    if (pipOpen) {
        const rect = pipBox.getBoundingClientRect();
        renderer.setViewport(rect.left, H - rect.bottom, rect.width, rect.height);
        renderer.setScissor(rect.left, H - rect.bottom, rect.width, rect.height);
        renderer.setScissorTest(true);
        composerPip.render();
    }

    // HUDテキスト更新
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
