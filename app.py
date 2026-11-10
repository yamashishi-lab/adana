import json
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Hyper-Drive Architect: Apex VFX Cinema Edition (Directors Cut Ultimate)",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("🛸 Hyper-Drive Architect: Apex VFX Ultimate Edition")
st.caption(
    "※ 完全映画仕様・極限改修版：CAM 02独立深度パイプライン / フォトリアルFBM地球＆動的自転 / "
    "二重反転アルクビエレ・リング＆重力波リップル / ワープ突入サウンドドロップ / フリーオービット＆シークバー完備"
)

# =========================================================================
# 🔬 機体・動力炉・目的地・環境データベース
# =========================================================================
VESSEL_DESIGNS = {
    "第6世代極超音速ウェイブライダー『ヴァルキリー SSTO』": {
        "id": "valkyrie",
        "style": "stealth_waverider",
        "catapult_mach": 15.5,
        "desc": "多面体ステルスノーズ、ダイバータレス超音速インテーク、油圧ピストン連動ベイ、二重反転アルクビエレリングを備えた主力SSTO。",
    },
    "重工業・磁気慣性核融合クルーザー『プロメテウス』": {
        "id": "prometheus",
        "style": "magnetic_fusion",
        "catapult_mach": 12.2,
        "desc": "露出トラスフレームに黄金MLI球形He3タンク8基、極太クライオ配管、大口径磁気ピンチノズルを備える深宇宙重巡航艇。",
    },
    "電磁カタパルト特化・軌道穿孔槍『ロンギヌス』": {
        "id": "longinus",
        "style": "massdriver_spear",
        "catapult_mach": 19.8,
        "desc": "クサビ型ダイヤモンド断面。高高度で外装フェアリング4枚を爆砕パージし、超高密度反物質コアを露出させる実験機。",
    },
}

ARMOR_SYSTEMS = {
    "漆黒カーボンナノチューブ電波吸収装甲 (RAM Stealth)": {
        "metalness": 0.65,
        "roughness": 0.38,
        "plasma_hex": 0xD946EF,
    },
    "液体金属クローム・電磁ミラー装甲 (Mirror Electrum)": {
        "metalness": 0.98,
        "roughness": 0.08,
        "plasma_hex": 0x38BDF8,
    },
    "焼結タングステン・セラミック耐熱複合材 (Thermal Grey)": {
        "metalness": 0.75,
        "roughness": 0.25,
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
    "相模湾 第1メガフロート射場 (深夜・大気光霧＆サーチライト照射)": {
        "mode": "night",
        "angle_deg": 28.0,
        "sun_pos": [-180, 110, -260],
        "sun_color": 0x93C5FD,
        "sun_int": 2.8,
        "sky_zenith": "#02050E",
        "sky_horizon": "#07172F",
        "fog_color": "#07172F",
        "fog_density": 0.00006,
    },
    "相模湾 第1メガフロート射場 (夜明け・富士シルエット＆マジックアワー)": {
        "mode": "dawn",
        "angle_deg": 28.0,
        "sun_pos": [200, 90, 220],
        "sun_color": 0xFFAD60,
        "sun_int": 4.8,
        "sky_zenith": "#040B1A",
        "sky_horizon": "#9A3412",
        "fog_color": "#431407",
        "fog_density": 0.000045,
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
    wings_span = st.slider("可変ジオメトリ主翼スパン (m)", 18.0, 42.0, 30.0, step=1.0)
    radiator_fins = st.slider("展開式 高温放熱ラジエーターパネル数", 2, 8, 4, step=2)
    aux_boosters = st.checkbox(
        "外装スクラムジェット補助ブースター×2 (高度55kmで分離パージ)", value=True
    )

with tab2:
  c1, c2 = st.columns(2)
  with c1:
    env_sel = st.selectbox("射場ロケーション＆時間帯", list(LAUNCH_ENVIRONMENTS.keys()))
    env_cfg = LAUNCH_ENVIRONMENTS[env_sel]
    coil_charge = st.slider("リニアカタパルト超伝導励磁出力 (%)", 80, 150, 125, step=5)
  with c2:
    st.caption("※ メガフロート人工島・防波堤・サーチライト光柱、富士山稜線、Gerstner波浪海面を描画。")
    cryo_steam = st.checkbox("極低温クライオ水蒸気＆散水デリュージ煙", value=True)
    mach_cone_vfx = st.checkbox("音速ヴェイパー＆熱圏プラズマボウショック", value=True)

with tab3:
  c1, c2 = st.columns(2)
  with c1:
    power_sel = st.selectbox("主推進エンジンコア", list(POWER_CORES.keys()))
    power_cfg = POWER_CORES[power_sel]
    shock_count = st.slider("推進炎 ショックダイヤモンド（マッハリング）段数", 3, 7, 5)
  with c2:
    warp_factor = st.slider("アルクビエレ時空曲率 (Warp Factor)", 2.0, 9.9, 9.2, step=0.1)
    flip_timing = st.slider("フリップ＆バーン（180°反転減速）開始地点", 0.60, 0.85, 0.74, step=0.01)

with tab4:
  c1, c2 = st.columns(2)
  with c1:
    dest_sel = st.selectbox("目標スターゲート宙域", list(DESTINATIONS.keys()))
    dest_cfg = DESTINATIONS[dest_sel]
    st.caption(f"**航行距離:** {dest_cfg['dist_label']}")
  with c2:
    cam_preset = st.radio(
        "シネマカメラ画角プリセット",
        [
            "シネマ・グランド煽り追従 (機体・富士・地球・大気圏の弧をダイナミックに一望)",
            "ディープ・エクストラワイド (超広角：ワープ時空歪曲とオーロラトンネル全体を一望)",
            "チェイス・メカニカルフォーカス (主翼・油圧リンク・ラジエーター変形を高解像度観察)",
        ],
        index=0,
    )

# =========================================================================
# 💥 タイムライン物理データ生成
# =========================================================================
def build_timeline(preview_only=False):
  if preview_only:
    return [{
        "t": -5.0, "phase": "PAD_STANDBY", "dist_m": 0.0, "alt_km": 0.04,
        "mach": 0.0, "vc": 0.0, "g": 1.0, "temp_k": 288.0,
        "clamp_open": 0.0, "sabot_purge": 0.0, "booster_purge": 0.0, "fairing_purge": 0.0,
        "wing_sweep": 0.0, "bay_open": 0.0, "ring_lift": 0.0, "rad_deploy": 0.0,
        "nozzle_open": 0.2, "engine_power": 0.0, "spark_arc": 0.0,
        "vapor_alpha": 0.0, "plasma_alpha": 0.0, "warp_charge": 0.0,
        "warp_lens": 0.0, "warp_active": 0.0, "warp_boom": 0.0,
        "rcs_burst": 0.0, "tether_lock": 0.0, "pitch_deg": env_cfg["angle_deg"],
        "yaw_deg": 0.0, "vib": 0.0, "progress": 0.0, "ship_time": 0.0,
    }]

  dt = 0.25
  frames = []
  base_pitch = float(env_cfg["angle_deg"])
  exit_mach = vessel_cfg["catapult_mach"] * (coil_charge / 100.0)

  for step in range(20):
    t = -5.0 + step * dt
    eng_pre = float(np.clip((t + 1.8) / 1.8, 0.0, 0.7))
    clamp = float(np.clip((t + 0.4) / 0.4, 0.0, 1.0))
    frames.append({
        "t": t,
        "phase": "CRYO_VENTING" if t < -3.0 else "LINEAR_COIL_CHARGE",
        "dist_m": 0.0, "alt_km": 0.04, "mach": 0.0, "vc": 0.0,
        "g": 1.0 + eng_pre * 0.9, "temp_k": 288.0 + eng_pre * 140.0,
        "clamp_open": clamp, "sabot_purge": 0.0, "booster_purge": 0.0, "fairing_purge": 0.0,
        "wing_sweep": 0.0, "bay_open": 0.0, "ring_lift": 0.0, "rad_deploy": 0.0,
        "nozzle_open": 0.2 + eng_pre * 0.5, "engine_power": eng_pre,
        "spark_arc": float(np.clip((t + 2.5) / 2.5, 0.0, 0.6)),
        "vapor_alpha": 0.0, "plasma_alpha": 0.0, "warp_charge": 0.0,
        "warp_lens": 0.0, "warp_active": 0.0, "warp_boom": 0.0,
        "rcs_burst": 0.0, "tether_lock": 0.0, "pitch_deg": base_pitch,
        "yaw_deg": 0.0, "vib": eng_pre * 0.12, "progress": 0.0, "ship_time": 0.0,
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

  for step in range(240):
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

    if t <= 3.2:
      phase = "CATAPULT_RAIL_ACCEL"
      accel_ratio = t / 3.2
      mach = (accel_ratio**1.25) * exit_mach
      speed_ms = mach * 340.0
      dist_m += speed_ms * dt * 0.50
      alt_km = 0.04 + (dist_m * np.sin(rad_pitch)) / 1000.0
      g_load = 15.0 * (coil_charge / 100.0)
      eng_pwr = 1.0
      nozzle = 0.95
      spark_arc = 1.0
      wing_sw = float(np.clip((mach - 1.5) / 10.0, 0.0, 1.0))
      if 0.85 <= mach <= 2.2:
        vapor = float(1.0 - abs(mach - 1.5) / 0.7)
      vib = 0.28 + vapor * 0.35
      pitch_cur = base_pitch
    elif alt_km < 130.0:
      phase = "STRATOSPHERE_CLIMB" if alt_km < 60.0 else "EXOSPHERE_INSERTION"
      sabot_p = min(1.0, sabot_p + 1.2 * dt)
      mach = min(35.0, mach + 3.8 * dt)
      speed_ms = mach * 340.0
      dist_m += speed_ms * dt * 0.75
      space_f = float(np.clip((alt_km - 10.0) / 110.0, 0.0, 1.0))
      pitch_boost = 5.0 if alt_km < 25.0 else 0.0
      pitch_cur = (base_pitch + pitch_boost) * (1.0 - space_f * 0.88)
      alt_km += (speed_ms * np.sin(np.radians(max(4.5, pitch_cur))) * dt) / 1000.0
      g_load = 5.4
      eng_pwr = 1.0
      nozzle = 1.0
      wing_sw = 1.0
      if 12.0 <= alt_km <= 85.0:
        plasma = float(np.sin(((alt_km - 12.0) / 73.0) * np.pi) ** 0.75)
      if alt_km >= 50.0 and aux_boosters:
        booster_p = min(1.0, booster_p + 0.65 * dt)
        if booster_p < 0.4:
          rcs = 1.0
      vib = plasma * 0.45 + 0.08
    elif progress < 0.12:
      phase = "WARP_FIELD_COMPRESSION"
      alt_km = 160.0 + (progress / 0.12) * 140.0
      pitch_cur = 0.0
      eng_pwr = 0.2
      nozzle = 0.25
      g_load = 0.2
      wing_sw = 0.5
      progress += 0.018 * dt * 4.0
      morph_prog = float(np.clip(progress / 0.12, 0.0, 1.0))
      bay_o = float(np.clip(morph_prog * 2.5, 0.0, 1.0))
      ring_l = float(np.clip((morph_prog - 0.25) * 2.2, 0.0, 1.0))
      rad_d = float(np.clip((morph_prog - 0.45) * 2.0, 0.0, 1.0))
      if vessel_cfg["style"] == "massdriver_spear":
        fairing_p = min(1.0, fairing_p + 0.8 * dt)
      w_charge = float(np.clip((morph_prog - 0.35) / 0.65, 0.0, 1.0))
      if morph_prog > 0.65:
        w_lens = float(np.sin(((morph_prog - 0.65) / 0.35) * (np.pi / 2)))
      if morph_prog > 0.95:
        w_boom = 1.0
      rcs = 1.0 if morph_prog < 0.25 else 0.0
      vc = 0.02 + w_charge * 0.12
    elif progress < flip_timing:
      phase = "ALCUBIERRE_HYPER_WARP"
      alt_km = 300.0 + (progress - 0.12) * 500000.0
      pitch_cur = 0.0
      bay_o = 1.0
      ring_l = 1.0
      rad_d = 1.0
      wing_sw = 1.0
      eng_pwr = 1.0
      nozzle = 1.0
      target_vc = min(0.996, 0.40 + (warp_factor / 10.0) * 0.59)
      vc = min(target_vc, vc + 0.35 * dt)
      w_active = 1.0
      w_charge = 1.0
      g_load = 1.1
      vib = 0.08
      progress += (vc * 0.075) * dt * 4.0
      if progress >= flip_timing - 0.03:
        w_boom = 1.0
    else:
      phase = "DEBRIS_RETRO_BRAKING"
      alt_km = 99999.0
      rem = max(0.0001, 1.0 - progress)
      flip_prog = float(np.clip((progress - flip_timing) / 0.06, 0.0, 1.0))
      yaw_deg = flip_prog * 180.0
      pitch_cur = 0.0
      rcs = 1.0 if (flip_prog < 0.25 or (0.75 < flip_prog < 1.0)) else 0.0
      if rem < 0.08:
        w_boom = max(0.0, 1.0 - (0.08 - rem) * 15.0)
      vc = max(0.004, min(vc, rem * 4.2))
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
      progress = min(1.0, progress + max(0.004, vc * 0.065) * dt * 4.0)

    gamma = 1.0 / np.sqrt(max(0.001, 1.0 - (min(0.999, vc) ** 2)))
    ship_time += dt / gamma
    temp_k = 288.0 + plasma * 1650.0 + (w_active * 620.0) + (eng_pwr * 240.0)

    frames.append({
        "t": float(t), "phase": phase, "dist_m": float(dist_m), "alt_km": float(alt_km),
        "mach": float(mach), "vc": float(vc), "g": float(g_load), "temp_k": float(temp_k),
        "clamp_open": 1.0, "sabot_purge": float(sabot_p), "booster_purge": float(booster_p),
        "fairing_purge": float(fairing_p), "wing_sweep": float(wing_sw), "bay_open": float(bay_o),
        "ring_lift": float(ring_l), "rad_deploy": float(rad_d), "nozzle_open": float(nozzle),
        "engine_power": float(eng_pwr), "spark_arc": float(spark_arc), "vapor_alpha": float(vapor),
        "plasma_alpha": float(plasma), "warp_charge": float(w_charge), "warp_lens": float(w_lens),
        "warp_active": float(w_active), "warp_boom": float(w_boom), "rcs_burst": float(rcs),
        "tether_lock": float(tether), "pitch_deg": float(pitch_cur), "yaw_deg": float(yaw_deg),
        "vib": float(vib), "progress": float(progress), "ship_time": float(ship_time),
    })

    if progress >= 0.998:
      for extra in range(16):
        frames.append({
            "t": float(t + (extra + 1) * dt), "phase": "STARGATE_DOCKING_LOCKED",
            "dist_m": float(dist_m), "alt_km": 99999.0, "mach": 0.0, "vc": 0.0, "g": 0.0,
            "temp_k": 330.0, "clamp_open": 1.0, "sabot_purge": 1.0, "booster_purge": float(booster_p),
            "fairing_purge": float(fairing_p), "wing_sweep": 0.0, "bay_open": 0.5, "ring_lift": 0.2,
            "rad_deploy": 1.0, "nozzle_open": 0.2, "engine_power": 0.0, "spark_arc": 0.0,
            "vapor_alpha": 0.0, "plasma_alpha": 0.0, "warp_charge": 0.0, "warp_lens": 0.0,
            "warp_active": 0.0, "warp_boom": 0.0, "rcs_burst": 0.0, "tether_lock": 1.0,
            "pitch_deg": 0.0, "yaw_deg": 180.0, "vib": 0.0, "progress": 1.0, "ship_time": float(ship_time),
        })
      break

  return frames

# =========================================================================
# 🚀 起動ボタン＆シリアライズ
# =========================================================================
st.markdown("---")
launch_trigger = st.button(
    "🔴 IGNITION & CATAPULT LAUNCH (超伝導励磁 ➔ マッハ射出 ➔ 時空収縮ワープ開始)",
    use_container_width=True,
    type="primary",
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
# 📺 Three.js 完全版 (Directors Cut Ultimate Edition)
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
#webgl-canvas{
  width:100%;height:100%;display:block;position:absolute;top:0;left:0;
  z-index:1;cursor:grab;touch-action:none;
}
#webgl-canvas:active{cursor:grabbing;}
.letterbox-top{position:absolute;top:0;left:0;width:100%;height:14px;background:#000;z-index:90;pointer-events:none;}
.letterbox-bottom{position:absolute;bottom:0;left:0;width:100%;height:14px;background:#000;z-index:90;pointer-events:none;}

.top-ui-container{
  position:absolute;top:14px;left:0;width:100%;display:flex;flex-direction:column;
  align-items:center;z-index:30;pointer-events:none;
}
.hud-top{
  width:100%;min-height:44px;
  background:linear-gradient(180deg,rgba(2,6,18,0.94) 0%,rgba(4,12,28,0.80) 100%);
  border-bottom:1px solid rgba(56,189,248,0.3);
  display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;
  padding:5px 18px;gap:8px;box-shadow:0 4px 25px rgba(0,0,0,0.85);
  pointer-events:none;
}
.hud-group{display:flex;align-items:center;flex-wrap:wrap;gap:12px;font-size:11px;letter-spacing:1px;}
.badge{background:rgba(14,165,233,0.18);border:1px solid #38bdf8;color:#38bdf8;padding:2px 8px;border-radius:3px;font-weight:800;}

/* ★修正: CAM 02 PIPウィンドウ（背景透過＋独立枠） */
.pip-window{
  width:calc(100% - 24px);margin:4px 12px 0 12px;height:175px;
  border:2px solid rgba(56,189,248,0.85);border-radius:6px;
  background:transparent !important;
  box-shadow:0 12px 35px rgba(0,0,0,0.85);
  cursor:pointer;overflow:hidden;position:relative;transition:height 0.25s ease;
  pointer-events:auto;
}
.pip-scan{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,0.18),rgba(0,0,0,0.18) 1px,transparent 1px,transparent 3px);pointer-events:none;z-index:42;}
.pip-header{position:absolute;top:6px;left:10px;right:10px;display:flex;justify-content:space-between;align-items:center;z-index:45;pointer-events:none;}
.pip-label{font-size:9.5px;font-weight:800;background:rgba(9,14,28,0.88);padding:3px 8px;border-left:2px solid #38bdf8;letter-spacing:1px;}
.pip-telemetry{font-size:9px;color:#38bdf8;font-family:monospace;background:rgba(9,14,28,0.85);padding:2px 6px;border-radius:2px;}
.pip-toggle{font-size:8px;color:#94a3b8;background:rgba(9,14,28,0.88);padding:3px 6px;cursor:pointer;}
.pip-rec{position:absolute;bottom:6px;right:10px;font-size:9px;color:#f43f5e;font-weight:900;display:flex;align-items:center;gap:5px;z-index:45;pointer-events:none;}
.rec-dot{width:6px;height:6px;border-radius:50%;background:#f43f5e;animation:pulse 1s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.15;}}

/* ★魔改造: タイムライン・スクラブ＆シネマコントロールバー */
.scrub-bar-container{
  position:absolute;bottom:128px;left:50%;transform:translateX(-50%);
  width:min(90%, 820px);background:rgba(2,6,20,0.88);border:1px solid rgba(56,189,248,0.4);
  border-radius:20px;padding:4px 16px;display:flex;align-items:center;gap:12px;z-index:35;
  box-shadow:0 6px 20px rgba(0,0,0,0.7);
}
.scrub-btn{background:rgba(14,165,233,0.2);border:1px solid #38bdf8;color:#38bdf8;font-size:10px;font-weight:bold;padding:2px 8px;border-radius:4px;cursor:pointer;}
.scrub-btn:hover{background:#38bdf8;color:#000;}
.scrub-slider{flex:1;accent-color:#38bdf8;cursor:pointer;}

.radar-panel{
  position:absolute;bottom:68px;left:0;
  width:100%;height:58px;
  background:rgba(2,6,20,0.92);
  border-top:1px solid rgba(56,189,248,0.45);
  border-bottom:1px solid rgba(56,189,248,0.2);
  display:flex;align-items:center;padding:0 20px;gap:14px;
  z-index:25;pointer-events:none;
}
.radar-tag{font-size:9px;color:#38bdf8;font-weight:900;white-space:nowrap;letter-spacing:1px;border-right:1px solid rgba(56,189,248,0.3);padding-right:10px;}
#radar-canvas{flex:1;height:50px;display:block;}

.hud-bottom{
  position:absolute;bottom:14px;left:0;width:100%;height:54px;
  background:linear-gradient(0deg,rgba(2,6,18,0.94) 0%,rgba(6,13,30,0.82) 100%);
  border-top:1px solid rgba(148,163,184,0.2);
  display:grid;grid-template-columns:repeat(5,1fr);align-items:center;
  padding:0 20px;z-index:20;pointer-events:none;
}
.metric{display:flex;flex-direction:column;border-left:2px solid rgba(56,189,248,0.35);padding-left:10px;}
.metric-lbl{font-size:8px;color:#94a3b8;letter-spacing:1px;}
.metric-val{font-size:14px;font-weight:900;color:#f8fafc;}

#complete-banner{
  display:none;position:absolute;top:230px;left:50%;transform:translateX(-50%);
  background:rgba(6,78,59,0.95);border:2px solid #10b981;
  padding:16px 36px;border-radius:8px;text-align:center;z-index:70;
  box-shadow:0 0 60px rgba(16,185,129,0.7);pointer-events:none;
}
</style>
</head>
<body>
<div class="letterbox-top"></div>
<div class="letterbox-bottom"></div>
<canvas id="webgl-canvas"></canvas>

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
      <div id="pip-metric" class="pip-telemetry">TARGET LOCK: ACQUIRING...</div>
      <div id="pip-btn" class="pip-toggle">[HIDE]</div>
    </div>
    <div class="pip-rec"><div class="rec-dot"></div>OPTICAL DUAL TRACKING LOCK</div>
  </div>
</div>

<div class="scrub-bar-container">
  <button id="btn-play" class="scrub-btn">PAUSE</button>
  <button id="btn-speed" class="scrub-btn">1.0x</button>
  <input type="range" id="time-scrub" class="scrub-slider" min="0" max="1000" value="0">
  <span id="scrub-val" style="font-size:10px;font-family:monospace;color:#38bdf8;width:45px;">0%</span>
</div>

<div class="radar-panel">
  <div id="radar-label" class="radar-tag">TACTICAL RADAR<br><span style="color:#94a3b8;font-size:7.5px;">ORBITAL PROJECTION</span></div>
  <canvas id="radar-canvas"></canvas>
</div>

<div id="complete-banner">
  <div style="font-size:18px;font-weight:900;color:#6ee7b7;letter-spacing:1.5px;">STARGATE MAGNETIC ARREST COMPLETE</div>
  <div style="font-size:11px;color:#d1fae5;margin-top:4px;">ALL HYPER-DRIVE SUBSYSTEMS NOMINAL / DOCKING LOCKED</div>
</div>

<div class="hud-bottom">
  <div class="metric"><span class="metric-lbl">RELATIVISTIC VEL</span><span class="metric-val"><span id="ui-vc">0.000</span> <small style="font-size:9px;color:#64748b;">c</small></span></div>
  <div class="metric"><span class="metric-lbl">HULL THERMAL</span><span class="metric-val"><span id="ui-temp">288</span> <small style="font-size:9px;color:#64748b;">K</small></span></div>
  <div class="metric"><span class="metric-lbl">G-FORCE</span><span class="metric-val"><span id="ui-g">1.0</span> <small style="font-size:9px;color:#64748b;">G</small></span></div>
  <div class="metric"><span class="metric-lbl">LORENTZ (γ)</span><span class="metric-val"><span id="ui-gamma">1.00</span> <small style="font-size:9px;color:#64748b;">x</small></span></div>
  <div class="metric"><span class="metric-lbl">MISSION PROGRESS</span><span class="metric-val"><span id="ui-prog">0.0</span> <small style="font-size:9px;color:#64748b;">%</small></span></div>
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
    pipBox.style.height = pipOpen ? '175px' : '26px';
    document.getElementById('pip-btn').innerText = pipOpen ? '[HIDE]' : '[SHOW]';
});

// =========================================================================
// 1. レンダラー構築＆PMREM IBL＆修正天球＆ポストプロセス
// =========================================================================
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: "high-performance" });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
renderer.setSize(W, H);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.35;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const scene = new THREE.Scene();
const baseFogColor = new THREE.Color(cfg.env.fog_color);
scene.fog = new THREE.FogExp2(baseFogColor, cfg.env.fog_density);

const cameraMain = new THREE.PerspectiveCamera(46, W / H, 0.5, 950000);
const cameraPip = new THREE.PerspectiveCamera(42, (W - 24) / 175, 0.5, 950000);

let baseCamPos = new THREE.Vector3(-65, 22, -115);
let baseTarget = new THREE.Vector3(0, 6.0, 50.0);
if (cfg.cam_preset.includes("エクストラ")) baseCamPos.set(-110, 35, -160);
else if (cfg.cam_preset.includes("チェイス")) baseCamPos.set(-42, 14, -75);
cameraMain.position.copy(baseCamPos);
cameraMain.lookAt(baseTarget);

// ★魔改造: マウスドラッグによる360度フリーオービット旋回
let isOrbiting = false, orbitTheta = 0, orbitPhi = 0, prevMouseX = 0, prevMouseY = 0;
canvas.addEventListener('pointerdown', (e) => {
    isOrbiting = true;
    prevMouseX = e.clientX; prevMouseY = e.clientY;
});
window.addEventListener('pointermove', (e) => {
    if (!isOrbiting) return;
    const dx = e.clientX - prevMouseX;
    const dy = e.clientY - prevMouseY;
    orbitTheta -= dx * 0.005;
    orbitPhi = Math.max(-1.2, Math.min(1.2, orbitPhi - dy * 0.005));
    prevMouseX = e.clientX; prevMouseY = e.clientY;
});
window.addEventListener('pointerup', () => { isOrbiting = false; });

// PMREM Generator
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
    const tex = new THREE.CanvasTexture(c);
    tex.mapping = THREE.EquirectangularReflectionMapping;
    return tex;
}
const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();
const rawSkyTex = makeSkyEnvTexture();
const envMapTexture = pmremGenerator.fromEquirectangular(rawSkyTex).texture;
scene.environment = envMapTexture;

// ★修正: バグ・モアレの出ない3Dパーティクル深宇宙星雲（天球）
const starPointsCount = 4500;
const starPointGeo = new THREE.BufferGeometry();
const starPointPos = new Float32Array(starPointsCount * 3);
const starPointCol = new Float32Array(starPointsCount * 3);
for (let i = 0; i < starPointsCount; i++) {
    const u = Math.random(), v = Math.random();
    const theta = u * 2.0 * Math.PI, phi = Math.acos(2.0 * v - 1.0);
    const r = 250000.0;
    starPointPos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
    starPointPos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
    starPointPos[i * 3 + 2] = r * Math.cos(phi);
    const colMix = Math.random();
    starPointCol[i * 3] = 0.5 + colMix * 0.5;
    starPointCol[i * 3 + 1] = 0.7 + colMix * 0.3;
    starPointCol[i * 3 + 2] = 1.0;
}
starPointGeo.setAttribute('position', new THREE.BufferAttribute(starPointPos, 3));
starPointGeo.setAttribute('color', new THREE.BufferAttribute(starPointCol, 3));
const starDomePoints = new THREE.Points(
    starPointGeo,
    new THREE.PointsMaterial({ size: 280.0, vertexColors: true, transparent: true, opacity: 0.9, depthWrite: false })
);
scene.add(starDomePoints);

const sunLight = new THREE.DirectionalLight(cfg.env.sun_color, cfg.env.sun_int);
sunLight.position.set(cfg.env.sun_pos[0] * 0.15, cfg.env.sun_pos[1] * 0.15 + 40.0, cfg.env.sun_pos[2] * 0.15);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048; sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 10; sunLight.shadow.camera.far = 800;
sunLight.shadow.camera.left = -90; sunLight.shadow.camera.right = 90;
sunLight.shadow.camera.top = 90; sunLight.shadow.camera.bottom = -90;
scene.add(sunLight);

const rimLight = new THREE.DirectionalLight(0x93c5fd, 2.0);
rimLight.position.set(-60, 45, 60);
scene.add(rimLight);

const hemiLight = new THREE.HemisphereLight(0x93c5fd, 0x0f172a, 1.8);
scene.add(hemiLight);

// ★魔改造: 重力レンズ＋色収差＋フィルムグレイン＆周辺減光
const WarpDistortionShader = {
    uniforms: {
        "tDiffuse": { value: null },
        "uDistort": { value: 0.0 },
        "uTime": { value: 0.0 },
        "uFlash": { value: 0.0 }
    },
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform sampler2D tDiffuse;
        uniform float uDistort;
        uniform float uTime;
        uniform float uFlash;
        varying vec2 vUv;

        float random(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }

        void main() {
            vec2 center = vec2(0.5, 0.5);
            vec2 dir = vUv - center;
            float dist = length(dir);

            float ringDistort = sin(dist * 18.0 - uTime * 6.0) * exp(-dist * 3.5) * uDistort * 0.08;
            vec2 rUv = vUv + dir * (dist * uDistort * 0.12 + ringDistort);
            vec2 gUv = vUv;
            vec2 bUv = vUv - dir * (dist * uDistort * 0.12 + ringDistort);

            float r = texture2D(tDiffuse, rUv).r;
            float g = texture2D(tDiffuse, gUv).g;
            float b = texture2D(tDiffuse, bUv).b;
            vec3 col = vec3(r, g, b);

            float grain = (random(vUv * 800.0 + uTime) - 0.5) * 0.035;
            col += grain;

            float vig = smoothstep(0.85, 0.25, dist);
            col *= vig;
            col = mix(col, vec3(1.0, 1.0, 1.0), uFlash);

            gl_FragColor = vec4(col, 1.0);
        }
    `
};

const renderSceneMain = new THREE.RenderPass(scene, cameraMain);
const bloomPass = new THREE.UnrealBloomPass(new THREE.Vector2(W, H), 1.35, 0.45, 0.80);
const warpPass = new THREE.ShaderPass(WarpDistortionShader);

const composerMain = new THREE.EffectComposer(renderer);
composerMain.addPass(renderSceneMain);
composerMain.addPass(bloomPass);
composerMain.addPass(warpPass);

window.addEventListener('resize', () => {
    W = window.innerWidth; H = window.innerHeight;
    renderer.setSize(W, H);
    composerMain.setSize(W, H);
    cameraMain.aspect = W / H;
    cameraMain.updateProjectionMatrix();
    cameraPip.aspect = (W - 24) / 175;
    cameraPip.updateProjectionMatrix();
});

// =========================================================================
// 2. 音響システム＆AI音声コールアウト（★魔改造: サウンドドロップ機能）
// =========================================================================
let actx = null, rocketGain = null, rocketFilter = null, coilGain = null, warpOsc = null, warpGain = null, rcsGain = null;
let lastAnnouncedPhase = "";
let isAudioMutedForWarp = false;

function speakCallout(text) {
    if ('speechSynthesis' in window) {
        const u = new SpeechSynthesisUtterance(text);
        u.rate = 1.05; u.pitch = 1.1; u.volume = 0.85;
        window.speechSynthesis.speak(u);
    }
}

function initAudioSystem() {
    if (actx) return;
    try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        actx = new AudioCtx();
        if (actx.state === 'suspended') actx.resume();

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
        rocketFilter = actx.createBiquadFilter();
        rocketFilter.type = 'lowpass';
        rocketFilter.frequency.value = 340;
        rocketGain = actx.createGain();
        rocketGain.gain.value = 0.0001;
        whiteNoise.connect(rocketFilter);
        rocketFilter.connect(rocketGain);
        rocketGain.connect(actx.destination);
        whiteNoise.start(0);

        const rcsFilter = actx.createBiquadFilter();
        rcsFilter.type = 'highpass';
        rcsFilter.frequency.value = 1200;
        rcsGain = actx.createGain();
        rcsGain.gain.value = 0.0001;
        whiteNoise.connect(rcsFilter);
        rcsFilter.connect(rcsGain);
        rcsGain.connect(actx.destination);

        const coilOsc = actx.createOscillator();
        coilOsc.type = 'sawtooth'; coilOsc.frequency.value = 110;
        const cFilter = actx.createBiquadFilter();
        cFilter.type = 'bandpass'; cFilter.frequency.value = 460;
        coilGain = actx.createGain();
        coilGain.gain.value = 0.0001;
        coilOsc.connect(cFilter); cFilter.connect(coilGain);
        coilGain.connect(actx.destination);
        coilOsc.start(0);

        warpOsc = actx.createOscillator();
        warpOsc.type = 'sine'; warpOsc.frequency.value = 65;
        warpGain = actx.createGain();
        warpGain.gain.value = 0.0001;
        warpOsc.connect(warpGain); warpGain.connect(actx.destination);
        warpOsc.start(0);
    } catch(e){}
}
initAudioSystem();
window.addEventListener('pointerdown', () => { if (actx && actx.state === 'suspended') actx.resume(); }, { once: true });

// =========================================================================
// 3. プロシージャルPBRマテリアル＆ディテールテクスチャ
// =========================================================================
function makeDetailedHullTexture() {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 1024;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#64748b'; ctx.fillRect(0, 0, 1024, 1024);
    for (let x = 0; x < 1024; x += 64) {
        for (let y = 0; y < 1024; y += 32) {
            const v = 110 + Math.floor(Math.random() * 45);
            ctx.fillStyle = `rgb(${v},${v},${v})`;
            ctx.fillRect(x + 2, y + 2, 60, 28);
            ctx.fillStyle = '#1e293b';
            ctx.fillRect(x + 5, y + 5, 2, 2);
            ctx.fillRect(x + 56, y + 5, 2, 2);
        }
    }
    ctx.strokeStyle = '#0f172a'; ctx.lineWidth = 3;
    for (let x = 0; x <= 1024; x += 64) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 1024); ctx.stroke(); }
    for (let y = 0; y <= 1024; y += 32) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(1024, y); ctx.stroke(); }
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(4, 4);
    return tex;
}
const hullPbrTex = makeDetailedHullTexture();

const matHull = new THREE.MeshPhysicalMaterial({
    color: cfg.hull_color, metalness: cfg.metalness, roughness: cfg.roughness,
    bumpMap: hullPbrTex, bumpScale: 0.04, roughnessMap: hullPbrTex,
    clearcoat: 0.9, clearcoatRoughness: 0.12
});
const matBellyTile = new THREE.MeshStandardMaterial({ color: cfg.belly_color, metalness: 0.35, roughness: 0.75 });
const matTitaniumFrame = new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.92, roughness: 0.20 });
const matPistonRod = new THREE.MeshStandardMaterial({ color: 0xf8fafc, metalness: 0.98, roughness: 0.05 });
const matDarkAlloy = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.92, roughness: 0.22 });
const matGoldMLI = new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.96, roughness: 0.20 });
const matCopperCoil = new THREE.MeshStandardMaterial({ color: 0xd97706, metalness: 0.95, roughness: 0.15 });
const matCanopy = new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, metalness: 0.95, roughness: 0.03, transparent: true, opacity: 0.42, clearcoat: 1.0 });
const matRadiator = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.82, roughness: 0.28, emissive: 0xef4444, emissiveIntensity: 0.0 });
const matConcreteWet = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.45, metalness: 0.35 });

// =========================================================================
// 4. 宇宙船・超精密メカ造形＆★二重反転アルクビエレ・リング
// =========================================================================
const radAngle = THREE.MathUtils.degToRad(cfg.env.angle_deg);
const shipRoot = new THREE.Group();
shipRoot.rotation.x = -radAngle;
scene.add(shipRoot);

const shipPitchGroup = new THREE.Group();
shipRoot.add(shipPitchGroup);

const shipMeshGroup = new THREE.Group();
shipPitchGroup.add(shipMeshGroup);

const bayDoors = [];
const irisPaddles = [];
const radiatorPanels = [];
const hydraulicPistons = [];
const wingPivots = [];
const sabotClamps = [];
const fairingPanels = [];
const strobeLeds = [];
const rcsJets = [];
const purgableBoosters = [];

// 機体コア
const spineCore = new THREE.Mesh(new THREE.BoxGeometry(2.6, 1.4, 30.0), matDarkAlloy);
spineCore.castShadow = true;
shipMeshGroup.add(spineCore);

// ★ディテールUP: パネルライン・スジボリエッジの強調
const spineEdges = new THREE.LineSegments(new THREE.EdgesGeometry(spineCore.geometry, 25), new THREE.LineBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.3 }));
spineCore.add(spineEdges);

// コックピット
const cockpitGroup = new THREE.Group();
cockpitGroup.position.set(0, 0.7, 7.5);
shipMeshGroup.add(cockpitGroup);
for (let s of [-0.4, 0.4]) {
    const seat = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.9, 0.6), matDarkAlloy);
    seat.position.set(s, 0, 0);
    cockpitGroup.add(seat);
}
const canopyGlass = new THREE.Mesh(new THREE.ConeGeometry(1.35, 7.5, 16), matCanopy);
canopyGlass.scale.set(1.0, 0.48, 1.6);
canopyGlass.rotation.x = Math.PI / 2;
canopyGlass.position.set(0, 0.95, 8.8);
shipMeshGroup.add(canopyGlass);

// ステルスノーズ＆ナセル
if (cfg.style === "stealth_waverider") {
    const noseShape = new THREE.Shape();
    noseShape.moveTo(0, 1.1); noseShape.lineTo(2.6, 0.15); noseShape.lineTo(2.1, -0.75);
    noseShape.lineTo(-2.1, -0.75); noseShape.lineTo(-2.6, 0.15); noseShape.closePath();
    const noseGeo = new THREE.ExtrudeGeometry(noseShape, { depth: 12.0, bevelEnabled: true, bevelThickness: 4.5, bevelSize: 0.9, bevelSegments: 4 });
    const noseMesh = new THREE.Mesh(noseGeo, matHull);
    noseMesh.position.set(0, 0, 3.5);
    noseMesh.castShadow = true;
    shipMeshGroup.add(noseMesh);

    const noseEdges = new THREE.LineSegments(new THREE.EdgesGeometry(noseGeo, 30), new THREE.LineBasicMaterial({ color: 0x64748b, transparent: true, opacity: 0.45 }));
    noseMesh.add(noseEdges);

    for (let s of [-1, 1]) {
        const nacelle = new THREE.Mesh(new THREE.BoxGeometry(2.5, 1.9, 19.5), matHull);
        nacelle.position.set(s * 3.1, -0.15, -3.5);
        nacelle.castShadow = true;
        shipMeshGroup.add(nacelle);

        const vTail = new THREE.Mesh(new THREE.BoxGeometry(0.22, 4.8, 6.5), matHull);
        vTail.position.set(s * 3.8, 2.2, -10.8);
        vTail.rotation.z = -s * 0.32;
        shipMeshGroup.add(vTail);
    }
} else if (cfg.style === "magnetic_fusion") {
    const cmdPod = new THREE.Mesh(new THREE.CylinderGeometry(1.4, 3.4, 13.0, 8), matHull);
    cmdPod.rotation.x = Math.PI / 2;
    cmdPod.scale.set(1.3, 0.75, 1.0);
    cmdPod.position.set(0, 0.2, 10.5);
    shipMeshGroup.add(cmdPod);

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
        fairingPanels.push({ mesh: fPanel, baseX: fPanel.position.x, baseY: fPanel.position.y, ang: ang });
    }
}

// ★魔改造: 分離パージする外装補助ブースター×2
if (cfg.aux_boosters) {
    for (let s of [-1, 1]) {
        const boosterGroup = new THREE.Group();
        boosterGroup.position.set(s * 5.4, -0.6, -2.0);
        const bBody = new THREE.Mesh(new THREE.CylinderGeometry(0.85, 0.85, 16.0, 16), matTitaniumFrame);
        bBody.rotation.x = Math.PI / 2;
        boosterGroup.add(bBody);
        const bNose = new THREE.Mesh(new THREE.ConeGeometry(0.85, 3.2, 16), matDarkAlloy);
        bNose.rotation.x = -Math.PI / 2;
        bNose.position.z = 9.6;
        boosterGroup.add(bNose);
        shipMeshGroup.add(boosterGroup);
        purgableBoosters.push({ group: boosterGroup, side: s, basePos: boosterGroup.position.clone() });
    }
}

// 主翼
const halfSpan = cfg.wings_span * 0.5;
for (let s of [-1, 1]) {
    const pivot = new THREE.Group();
    pivot.position.set(s * 3.2, -0.1, 1.5);
    shipMeshGroup.add(pivot);

    const wShape = new THREE.Shape();
    wShape.moveTo(0, 4.0); wShape.lineTo(s * (halfSpan - 3.2), -3.5);
    wShape.lineTo(s * (halfSpan - 3.6), -7.5); wShape.lineTo(0, -10.5); wShape.closePath();
    const wGeo = new THREE.ExtrudeGeometry(wShape, { depth: 0.32, bevelEnabled: true, bevelThickness: 0.12, bevelSize: 0.4, bevelSegments: 2 });
    const wMesh = new THREE.Mesh(wGeo, matHull);
    wMesh.rotation.x = Math.PI / 2;
    pivot.add(wMesh);

    const wEdges = new THREE.LineSegments(new THREE.EdgesGeometry(wGeo, 25), new THREE.LineBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.35 }));
    wMesh.add(wEdges);
    wingPivots.push({ group: pivot, side: s });
}

// ベイドア＆油圧ピストン
for (let s of [-1, 1]) {
    for (let zOff of [-6.0, 1.0]) {
        const doorPivot = new THREE.Group();
        doorPivot.position.set(s * 2.4, 1.15, zOff);
        shipMeshGroup.add(doorPivot);
        const doorPanel = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.25, 6.4), matHull);
        doorPanel.position.set(-s * 1.1, 0, 0);
        doorPivot.add(doorPanel);
        bayDoors.push({ pivot: doorPivot, side: s });

        const cyl = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.4, 8), matTitaniumFrame);
        const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 1.2, 8), matPistonRod);
        cyl.position.set(s * 1.2, 0.7, zOff);
        cyl.rotation.z = s * 0.5;
        rod.position.set(0, 0.6, 0);
        cyl.add(rod);
        shipMeshGroup.add(cyl);
        hydraulicPistons.push({ cyl, rod, side: s });
    }
}

// ★魔改造: 二重反転アルクビエレ・リング＆超伝導セグメント磁石
const warpRingAssembly = new THREE.Group();
warpRingAssembly.position.set(0, -0.8, -2.5);
shipMeshGroup.add(warpRingAssembly);

const outerWarpRing = new THREE.Group();
const innerWarpRing = new THREE.Group();
warpRingAssembly.add(outerWarpRing);
warpRingAssembly.add(innerWarpRing);

const outerTorus = new THREE.Mesh(new THREE.TorusGeometry(6.8, 0.35, 16, 64), matTitaniumFrame);
outerWarpRing.add(outerTorus);
const innerTorus = new THREE.Mesh(new THREE.TorusGeometry(5.6, 0.28, 16, 64), matCopperCoil);
innerWarpRing.add(innerTorus);

// コイル・セグメント磁石ブロック群
const coilBlockGeo = new THREE.BoxGeometry(0.8, 0.5, 0.9);
for (let c = 0; c < 24; c++) {
    const ang = (c / 24) * Math.PI * 2;
    const cBlock = new THREE.Mesh(coilBlockGeo, matCopperCoil);
    cBlock.position.set(Math.cos(ang) * 6.8, Math.sin(ang) * 6.8, 0);
    cBlock.rotation.z = ang;
    outerWarpRing.add(cBlock);
}
for (let c = 0; c < 18; c++) {
    const ang = (c / 18) * Math.PI * 2;
    const cBlock = new THREE.Mesh(coilBlockGeo, matTitaniumFrame);
    cBlock.position.set(Math.cos(ang) * 5.6, Math.sin(ang) * 5.6, 0);
    cBlock.rotation.z = ang;
    innerWarpRing.add(cBlock);
}

// ★魔改造: 重力波リップル（空間パルス放出リング）
const rippleRings = [];
const rippleGeo = new THREE.RingGeometry(5.5, 6.2, 48);
const rippleMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.0, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false });
for (let rp = 0; rp < 5; rp++) {
    const rMesh = new THREE.Mesh(rippleGeo, rippleMat.clone());
    warpRingAssembly.add(rMesh);
    rippleRings.push({ mesh: rMesh, offset: rp * 0.2 });
}

// ★魔改造: リング中心へのプラズマアーク放電（稲妻）
const arcLineGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]);
const arcLineMat = new THREE.LineBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.0, linewidth: 2, blending: THREE.AdditiveBlending });
const warpArcs = [];
for (let a = 0; a < 6; a++) {
    const aLine = new THREE.Line(arcLineGeo.clone(), arcLineMat.clone());
    warpRingAssembly.add(aLine);
    warpArcs.push({ line: aLine, ang: (a / 6) * Math.PI * 2 });
}

// 推進ノズル＆ショックダイヤモンド
const nozzleRoot = new THREE.Group();
nozzleRoot.position.set(0, 0, -14.2);
shipMeshGroup.add(nozzleRoot);
for (let i = 0; i < 12; i++) {
    const ang = (i / 12) * Math.PI * 2;
    const petalPivot = new THREE.Group();
    petalPivot.position.set(Math.cos(ang) * 2.5, Math.sin(ang) * 2.5, -1.0);
    petalPivot.rotation.z = ang;
    nozzleRoot.add(petalPivot);
    const outerPetal = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.12, 3.2), matTitaniumFrame);
    outerPetal.position.set(0, 0.08, -1.4);
    petalPivot.add(outerPetal);
    irisPaddles.push(petalPivot);
}

const plumeRoot = new THREE.Group();
plumeRoot.position.set(0, 0, -16.5);
shipMeshGroup.add(plumeRoot);
const plumeLight = new THREE.PointLight(cfg.flame_hex, 0.0, 160.0);
plumeRoot.add(plumeLight);

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

// =========================================================================
// 5. カタパルト＆Gerstner波浪海面＆富士山
// =========================================================================
const catapultSlopeRoot = new THREE.Group();
catapultSlopeRoot.rotation.x = -radAngle;
scene.add(catapultSlopeRoot);
const railMover = new THREE.Group();
catapultSlopeRoot.add(railMover);

const dummy = new THREE.Object3D();
const archInst = new THREE.InstancedMesh(new THREE.TorusGeometry(9.5, 0.45, 10, 24, Math.PI), matTitaniumFrame, 220);
for (let i = 0; i < 220; i++) {
    dummy.position.set(0, -1.8, i * 16.0 - 40.0);
    dummy.updateMatrix();
    archInst.setMatrixAt(i, dummy.matrix);
}
railMover.add(archInst);

const groundEnvMover = new THREE.Group();
scene.add(groundEnvMover);

const fujiMount = new THREE.Mesh(new THREE.ConeGeometry(12500, 3776, 64), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.85 }));
fujiMount.position.set(4500, 1800, 14500);
groundEnvMover.add(fujiMount);

// =========================================================================
// 6. ★修正: フォトリアルFBM地球＆動的自転（モアレ解消版）
// =========================================================================
const earthGroup = new THREE.Group();
scene.add(earthGroup);

const earthShaderMat = new THREE.ShaderMaterial({
    vertexShader: `
        varying vec3 vNormal;
        varying vec3 vWorldPos;
        varying vec2 vUv;
        void main() {
            vUv = uv;
            vNormal = normalize(normalMatrix * normal);
            vec4 wp = modelMatrix * vec4(position, 1.0);
            vWorldPos = wp.xyz;
            gl_Position = projectionMatrix * viewMatrix * wp;
        }
    `,
    fragmentShader: `
        varying vec3 vNormal;
        varying vec3 vWorldPos;
        varying vec2 vUv;
        uniform vec3 uSunDir;
        uniform float uTime;

        // 滑らかなValue Noise
        float hash(vec2 p) { return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
        float noise(vec2 p) {
            vec2 i = floor(p); vec2 f = fract(p);
            f = f * f * (3.0 - 2.0 * f);
            return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), f.x),
                       mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), f.x), f.y);
        }
        float fbm(vec2 p) {
            float v = 0.0; float a = 0.5;
            for(int i = 0; i < 4; i++) {
                v += a * noise(p);
                p *= 2.0; a *= 0.5;
            }
            return v;
        }

        void main() {
            vec3 norm = normalize(vNormal);
            vec3 viewDir = normalize(cameraPosition - vWorldPos);
            float light = dot(norm, uSunDir);

            vec2 uvScroll = vec2(vUv.x + uTime * 0.0008, vUv.y);
            float land = smoothstep(0.48, 0.55, fbm(uvScroll * 12.0));

            vec3 ocean = vec3(0.015, 0.065, 0.16);
            vec3 continent = vec3(0.08, 0.14, 0.09);
            vec3 dayCol = mix(ocean, continent, land);

            // 夜間都市光
            float city = pow(fbm(uvScroll * 28.0), 3.0) * land * 14.0;
            vec3 nightCol = vec3(1.0, 0.72, 0.25) * city;

            float dayFactor = smoothstep(-0.1, 0.2, light);
            vec3 baseCol = mix(nightCol, dayCol * max(0.08, light), dayFactor);

            // 大気レイリーグロー
            float rim = pow(1.0 - max(0.0, dot(norm, viewDir)), 3.0);
            vec3 atmoCol = vec3(0.25, 0.65, 1.0) * rim * 1.6;

            gl_FragColor = vec4(baseCol + atmoCol, 1.0);
        }
    `,
    uniforms: {
        uSunDir: { value: new THREE.Vector3().fromArray(cfg.env.sun_pos).normalize() },
        uTime: { value: 0.0 }
    }
});
const earthSphere = new THREE.Mesh(new THREE.SphereGeometry(25000, 64, 64), earthShaderMat);
earthGroup.add(earthSphere);

// =========================================================================
// 7. ワープオーロラ＆目的スターゲート
// =========================================================================
const warpGroup = new THREE.Group();
warpGroup.visible = false;
scene.add(warpGroup);

const destWorld = new THREE.Group();
destWorld.position.set(0, 0, 800000.0);
destWorld.scale.setScalar(0.0001);
scene.add(destWorld);

const destPlanet = new THREE.Mesh(
    new THREE.SphereGeometry(3200, 48, 48),
    new THREE.MeshStandardMaterial({ color: cfg.dest_color, roughness: 0.65 })
);
destPlanet.position.set(700, -450, 5200);
destWorld.add(destPlanet);

const stargateOuter = new THREE.Mesh(new THREE.TorusGeometry(65, 4.8, 20, 64), matTitaniumFrame);
destWorld.add(stargateOuter);

// =========================================================================
// 8. 軌道レーダーマップ描画
// =========================================================================
const radarCanvas = document.getElementById('radar-canvas');
const rCtx = radarCanvas.getContext('2d');
const radarLabelEl = document.getElementById('radar-label');

function drawRadar(prog, vc, mach, altKm) {
    const rw = radarCanvas.width = radarCanvas.clientWidth * 1.5;
    const rh = radarCanvas.height = radarCanvas.clientHeight * 1.5;
    rCtx.clearRect(0, 0, rw, rh);
    const isSolar = (prog >= 0.12);
    radarLabelEl.innerHTML = isSolar
        ? `TACTICAL RADAR<br><span style="color:#10b981;font-size:7.5px;">SOLAR ESCAPE</span>`
        : `TACTICAL RADAR<br><span style="color:#38bdf8;font-size:7.5px;">LUNAR ORBIT</span>`;

    const leftX = 65, rightX = rw - 75, midY = rh / 2;
    rCtx.strokeStyle = 'rgba(56,189,248,0.3)';
    rCtx.lineWidth = 2;
    rCtx.beginPath(); rCtx.moveTo(leftX, midY); rCtx.lineTo(rightX, midY); rCtx.stroke();

    const curX = leftX + (isSolar ? ((prog - 0.12) / 0.86) : Math.min(1.0, altKm / 384400.0)) * (rightX - leftX);
    rCtx.fillStyle = '#f43f5e';
    rCtx.beginPath(); rCtx.arc(curX, midY, 5, 0, Math.PI * 2); rCtx.fill();
}

// =========================================================================
// 9. タイムライン再生・シーク制御＆60fpsアニメーションループ
// =========================================================================
let isPlaying = true;
let playSpeed = 1.0;
let userSimTime = -5.0;
let lastFrameTime = performance.now();

const btnPlay = document.getElementById('btn-play');
const btnSpeed = document.getElementById('btn-speed');
const scrubSlider = document.getElementById('time-scrub');
const scrubVal = document.getElementById('scrub-val');

btnPlay.addEventListener('click', () => {
    isPlaying = !isPlaying;
    btnPlay.innerText = isPlaying ? "PAUSE" : "PLAY";
});

btnSpeed.addEventListener('click', () => {
    playSpeed = playSpeed === 1.0 ? 0.2 : (playSpeed === 0.2 ? 2.5 : 1.0);
    btnSpeed.innerText = `${playSpeed.toFixed(1)}x`;
});

scrubSlider.addEventListener('input', (e) => {
    const norm = parseFloat(e.target.value) / 1000.0;
    const totalDuration = frames[frames.length - 1].t - frames[0].t;
    userSimTime = frames[0].t + norm * totalDuration;
});

function animate(now) {
    requestAnimationFrame(animate);
    const dtReal = (now - lastFrameTime) / 1000.0;
    lastFrameTime = now;

    if (!cfg.is_preview && isPlaying) {
        userSimTime += dtReal * 1.65 * playSpeed;
        const maxT = frames[frames.length - 1].t;
        if (userSimTime > maxT) userSimTime = maxT;
        const totalDuration = frames[frames.length - 1].t - frames[0].t;
        const curNorm = Math.min(1.0, Math.max(0.0, (userSimTime - frames[0].t) / totalDuration));
        scrubSlider.value = curNorm * 1000;
        scrubVal.innerText = `${(curNorm * 100).toFixed(0)}%`;
    }

    let idx = 0;
    while (idx < frames.length - 1 && frames[idx + 1].t <= userSimTime) idx++;
    const f0 = frames[idx];
    const f1 = frames[Math.min(frames.length - 1, idx + 1)];
    const dt = f1.t - f0.t;
    const alpha = dt > 0.0001 ? THREE.MathUtils.clamp((userSimTime - f0.t) / dt, 0.0, 1.0) : 0.0;
    const L = (k) => THREE.MathUtils.lerp(f0[k], f1[k], alpha);

    const distM = L('dist_m'), altKm = L('alt_km'), mach = L('mach'), vc = L('vc');
    const pitchDeg = L('pitch_deg'), yawDeg = L('yaw_deg'), vib = L('vib'), prog = L('progress');

    // ★魔改造: ワープ突入時の無音化＆フラッシュ判定
    const isWarpThreshold = (f0.phase === "WARP_FIELD_COMPRESSION" && prog > 0.10);
    warpPass.uniforms.uFlash.value = THREE.MathUtils.lerp(warpPass.uniforms.uFlash.value, L('warp_boom'), 0.15);

    // AI音声コールアウト
    if (f0.phase !== lastAnnouncedPhase) {
        lastAnnouncedPhase = f0.phase;
        if (f0.phase === "CATAPULT_RAIL_ACCEL") speakCallout("Magnetic catapult engaged.");
        else if (f0.phase === "EXOSPHERE_INSERTION") speakCallout("Exosphere insertion achieved.");
        else if (f0.phase === "WARP_FIELD_COMPRESSION") speakCallout("Alcubierre drive compression.");
        else if (f0.phase === "ALCUBIERRE_HYPER_WARP") speakCallout("Hyper warp engaged.");
        else if (f0.phase === "STARGATE_DOCKING_LOCKED") speakCallout("Docking locked.");
    }

    // カメラ位置・オービット補間
    const targetCam = baseCamPos.clone();
    targetCam.applyAxisAngle(new THREE.Vector3(0, 1, 0), orbitTheta);
    targetCam.y += orbitPhi * 30.0;
    cameraMain.position.lerp(targetCam, 0.08);
    cameraMain.lookAt(0, 2.0, 0);

    // 地上＆レール移動
    railMover.position.set(0, 0, -distM);
    groundEnvMover.position.set(0, -distM * Math.sin(radAngle), -distM * Math.cos(radAngle));

    const freePitch = -THREE.MathUtils.degToRad(pitchDeg) + radAngle;
    shipPitchGroup.rotation.set(freePitch, THREE.MathUtils.degToRad(yawDeg), 0);
    shipMeshGroup.position.set(
        Math.sin(now * 0.045) * vib * 0.35,
        Math.cos(now * 0.055) * vib * 0.35,
        Math.sin(now * 0.035) * vib * 0.35
    );

    // ★二重反転アルクビエレ・リングの回転＆パルス演出
    outerWarpRing.rotation.z += 0.04 + L('warp_charge') * 0.25;
    innerWarpRing.rotation.z -= 0.05 + L('warp_charge') * 0.35;
    warpRingAssembly.position.y = -0.8 + L('ring_lift') * 4.2;

    const wAct = L('warp_active');
    rippleRings.forEach(rp => {
        const rProg = (now * 0.002 + rp.offset) % 1.0;
        rp.mesh.position.z = -rProg * 35.0;
        rp.mesh.scale.setScalar(1.0 + rProg * 3.5);
        rp.mesh.material.opacity = (1.0 - rProg) * wAct * 0.85;
    });

    // 補助ブースター分離物理挙動
    const bPurge = L('booster_purge');
    purgableBoosters.forEach(b => {
        if (bPurge > 0.01) {
            b.group.position.x = b.basePos.x + b.side * bPurge * 35.0;
            b.group.position.y = b.basePos.y - bPurge * 22.0;
            b.group.position.z = b.basePos.z - bPurge * 55.0;
            b.group.rotation.x += 0.08;
            b.group.rotation.z += b.side * 0.05;
        } else {
            b.group.position.copy(b.basePos);
            b.group.rotation.set(0, 0, 0);
        }
    });

    // シェーダー更新
    earthShaderMat.uniforms.uTime.value = now * 0.001;
    warpPass.uniforms.uDistort.value = L('warp_boom') * 2.5 + wAct * 0.4;
    warpPass.uniforms.uTime.value = now * 0.001;

    // 地球の位置
    if (prog < 0.28) {
        earthGroup.visible = true;
        const warpRecede = Math.pow(Math.max(0, prog - 0.05) * 18.0, 3.0);
        earthGroup.position.set(0, -25050 - altKm * 120.0 - warpRecede * 35000.0, -4000 - distM * 0.6 - warpRecede * 95000.0);
    } else {
        earthGroup.visible = false;
    }

    // 音響制御（無音化対応）
    if (actx) {
        const muteFactor = isWarpThreshold ? 0.0001 : 1.0;
        rocketGain.gain.setTargetAtTime(L('engine_power') * 0.35 * muteFactor, actx.currentTime, 0.08);
        warpGain.gain.setTargetAtTime((wAct * 0.4 + L('warp_lens') * 0.25) * muteFactor, actx.currentTime, 0.1);
    }

    // =========================================================================
    // ★修正: CAM 02（PIP）独立レンダリング＆追従ロジック
    // =========================================================================
    const shipWorldPos = new THREE.Vector3();
    shipMeshGroup.getWorldPosition(shipWorldPos);

    if (f0.phase.includes("STANDBY") || f0.phase.includes("CHARGE")) {
        cameraPip.position.set(shipWorldPos.x + 18.0, shipWorldPos.y + 3.0, shipWorldPos.z - 25.0);
        cameraPip.lookAt(shipWorldPos);
        document.getElementById('pip-title').innerText = "CAM 02: LAUNCH PAD TELEMETRY";
        document.getElementById('pip-metric').innerText = `STATUS: MAGNETIZED / COIL 125%`;
    } else if (f0.phase === "CATAPULT_RAIL_ACCEL") {
        cameraPip.position.set(shipWorldPos.x - 22.0, shipWorldPos.y + 6.0, shipWorldPos.z - 35.0);
        cameraPip.lookAt(shipWorldPos);
        document.getElementById('pip-title').innerText = "CAM 02: RAIL ACCELERATION CHASE";
        document.getElementById('pip-metric').innerText = `MACH: ${mach.toFixed(1)} / G-LOAD: ${L('g').toFixed(1)}G`;
    } else if (f0.phase.includes("WARP")) {
        cameraPip.position.set(shipWorldPos.x + 32.0, shipWorldPos.y + 12.0, shipWorldPos.z - 45.0);
        cameraPip.lookAt(shipWorldPos);
        document.getElementById('pip-title').innerText = "CAM 02: WARP FIELD RECESSION";
        document.getElementById('pip-metric').innerText = `VEL: ${vc.toFixed(3)} c / LORENTZ: ${(1.0/Math.sqrt(Math.max(0.001,1.0-vc*vc))).toFixed(2)}x`;
    } else {
        cameraPip.position.set(shipWorldPos.x + 25.0, shipWorldPos.y + 8.0, shipWorldPos.z + 30.0);
        cameraPip.lookAt(shipWorldPos);
        document.getElementById('pip-title').innerText = "CAM 02: STARGATE APPROACH";
        document.getElementById('pip-metric').innerText = `VECTOR: ALIGNED / CAPTURE READY`;
    }

    drawRadar(prog, vc, mach, altKm);

    // メインビュー描画
    renderer.setRenderTarget(null);
    renderer.setViewport(0, 0, W, H);
    renderer.setScissorTest(false);
    composerMain.render();

    // ★修正: PIPビューを深度クリアして確実に上書き合成
    if (pipOpen) {
        const rect = pipBox.getBoundingClientRect();
        renderer.setViewport(rect.left, H - rect.bottom, rect.width, rect.height);
        renderer.setScissor(rect.left, H - rect.bottom, rect.width, rect.height);
        renderer.setScissorTest(true);
        renderer.clearDepth();
        renderer.render(scene, cameraPip);
    }

    // UI更新
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

components.html(final_output, height=940)
