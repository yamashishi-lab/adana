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
    "※ 完全映画仕様ディレクターズカット：PMREM IBL / フォトリアルFBM地球＆都市夜景 / シーケンシャル誘導灯メガフロート / "
    "CAM 02機体＋天体追跡フレーミング / 2段軌道レーダーUI / 自動起動シンセ＆AIボイス / 超濃縮ワープシネマテンポ"
)

# =========================================================================
# 🔬 機体・動力炉・目的地・環境データベース
# =========================================================================
VESSEL_DESIGNS = {
    "第6世代極超音速ウェイブライダー『ヴァルキリー SSTO』": {
        "id": "valkyrie",
        "style": "stealth_waverider",
        "catapult_mach": 15.5,
        "desc": "多面体ステルスノーズ、ダイバータレス超音速インテーク、油圧ピストン連動ベイ、超伝導デュアル・アルクビエレリングを備えた主力SSTO。",
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
# 💥 タイムライン物理データ（虚無の待ち時間解消・テンポ最適化）
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
        elif alt_km < 75.0 and t < 8.2:
            phase = "STRATOSPHERE_CLIMB" if alt_km < 40.0 else "EXOSPHERE_INSERTION"
            sabot_p = min(1.0, sabot_p + 1.2 * dt)
            mach = min(42.0, mach + 5.5 * dt)
            speed_ms = mach * 340.0
            dist_m += speed_ms * dt * 0.85
            space_f = float(np.clip((alt_km - 10.0) / 65.0, 0.0, 1.0))
            pitch_boost = 6.0 if alt_km < 25.0 else 0.0
            pitch_cur = max(16.0, (base_pitch + pitch_boost) * (1.0 - space_f * 0.55))
            alt_km += (speed_ms * np.sin(np.radians(pitch_cur)) * dt) / 1000.0
            g_load = 6.8
            eng_pwr = 1.0
            nozzle = 1.0
            wing_sw = 1.0
            if 10.0 <= alt_km <= 70.0:
                plasma = float(np.sin(((alt_km - 10.0) / 60.0) * np.pi) ** 0.75)
            if alt_km >= 35.0 and aux_boosters:
                booster_p = min(1.0, booster_p + 0.9 * dt)
                if booster_p < 0.4:
                    rcs = 1.0
            vib = plasma * 0.45 + 0.12
        elif progress < 0.12:
            phase = "WARP_FIELD_COMPRESSION"
            alt_km = 95.0 + (progress / 0.12) * 205.0
            pitch_cur = max(0.0, 16.0 * (1.0 - progress / 0.12))
            eng_pwr = 0.65
            nozzle = 0.75
            g_load = 1.8
            wing_sw = 0.5
            progress += 0.038 * dt * 4.0
            morph_prog = float(np.clip(progress / 0.12, 0.0, 1.0))
            bay_o = float(np.clip(morph_prog * 2.5, 0.0, 1.0))
            ring_l = float(np.clip((morph_prog - 0.25) * 2.2, 0.0, 1.0))
            rad_d = float(np.clip((morph_prog - 0.45) * 2.0, 0.0, 1.0))
            if vessel_cfg["style"] == "massdriver_spear":
                fairing_p = min(1.0, fairing_p + 1.2 * dt)
            w_charge = float(np.clip((morph_prog - 0.20) / 0.80, 0.0, 1.0))
            if morph_prog > 0.55:
                w_lens = float(np.sin(((morph_prog - 0.55) / 0.45) * (np.pi / 2)))
            if morph_prog > 0.88:
                w_boom = 1.0
            rcs = 1.0 if morph_prog < 0.35 else 0.0
            vc = 0.05 + w_charge * 0.25
            vib = 0.15 + w_charge * 0.25
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
            target_vc = min(0.996, 0.50 + (warp_factor / 10.0) * 0.49)
            vc = min(target_vc, vc + 0.45 * dt)
            w_active = 1.0
            w_charge = 1.0
            g_load = 1.2
            vib = 0.08
            progress += (vc * 0.095) * dt * 4.0
            if progress >= flip_timing - 0.03:
                w_boom = 1.0
        else:
            phase = "DEBRIS_RETRO_BRAKING"
            alt_km = 99999.0
            rem = max(0.0001, 1.0 - progress)
            raw_flip = float(np.clip((progress - flip_timing) / 0.06, 0.0, 1.0))
            flip_prog = raw_flip * raw_flip * (3.0 - 2.0 * raw_flip)
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
    "dest_color": f"#{dest_cfg['color_hex']:06x}" if isinstance(dest_cfg["color_hex"], int) else str(dest_cfg["color_hex"]),
    "dest_band": f"#{dest_cfg['band_hex']:06x}" if isinstance(dest_cfg["band_hex"], int) else str(dest_cfg["band_hex"]),
    "cam_preset": cam_preset,
    "env": env_cfg,
}

# =========================================================================
# 📺 Three.js 完全映画仕様・極限細密＆ド迫力チェイス版 (Apex VFX Cinema Edition V4)
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
  z-index:1;pointer-events:none;touch-action:pan-y;
}
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

/* ★修正: 16:9比率の映画中継サブモニターワイプ枠（右上固定配置） */
.pip-window{
  position:absolute;top:70px;right:18px;
  width:360px;height:202px;
  border:2px solid rgba(56,189,248,0.85);border-radius:6px;
  background:rgba(2,6,23,0.35);
  backdrop-filter:contrast(1.25) saturate(0.85);
  box-shadow:0 12px 35px rgba(0,0,0,0.95);
  cursor:pointer;overflow:hidden;transition:all 0.25s ease;
  pointer-events:auto;z-index:40;
}
.pip-scan{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,0.25),rgba(0,0,0,0.25) 1px,transparent 1px,transparent 3px);pointer-events:none;z-index:42;}
.pip-header{position:absolute;top:6px;left:8px;right:8px;display:flex;justify-content:space-between;align-items:center;z-index:45;pointer-events:none;}
.pip-label{font-size:9px;font-weight:800;background:rgba(9,14,28,0.92);padding:2px 6px;border-left:2px solid #38bdf8;letter-spacing:1px;}
.pip-telemetry{font-size:8.5px;color:#38bdf8;font-family:monospace;background:rgba(9,14,28,0.85);padding:2px 5px;border-radius:2px;}
.pip-toggle{font-size:8px;color:#94a3b8;background:rgba(9,14,28,0.92);padding:2px 5px;cursor:pointer;}
.pip-rec{position:absolute;bottom:6px;right:8px;font-size:8.5px;color:#f43f5e;font-weight:900;display:flex;align-items:center;gap:4px;z-index:45;pointer-events:none;}
.rec-dot{width:5px;height:5px;border-radius:50%;background:#f43f5e;animation:pulse 1s infinite;}
@keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.15;}}

.radar-panel{
  position:absolute;bottom:70px;left:0;
  width:100%;height:78px;
  background:rgba(2,6,20,0.92);
  border-top:1px solid rgba(56,189,248,0.45);
  border-bottom:1px solid rgba(56,189,248,0.2);
  display:flex;align-items:center;padding:0 20px;gap:14px;
  z-index:25;pointer-events:none;box-shadow:0 -6px 25px rgba(0,0,0,0.75);
}
.radar-tag{font-size:9.5px;color:#38bdf8;font-weight:900;white-space:nowrap;letter-spacing:1px;border-right:1px solid rgba(56,189,248,0.3);padding-right:12px;}
#radar-canvas{flex:1;height:64px;display:block;}

.hud-bottom{
  position:absolute;bottom:14px;left:0;width:100%;height:56px;
  background:linear-gradient(0deg,rgba(2,6,18,0.94) 0%,rgba(6,13,30,0.82) 100%);
  border-top:1px solid rgba(148,163,184,0.2);
  display:grid;grid-template-columns:repeat(5,1fr);align-items:center;
  padding:0 20px;z-index:20;pointer-events:none;
}
.metric{display:flex;flex-direction:column;border-left:2px solid rgba(56,189,248,0.35);padding-left:10px;}
.metric-lbl{font-size:8.5px;color:#94a3b8;letter-spacing:1.1px;}
.metric-val{font-size:15px;font-weight:900;color:#f8fafc;margin-top:1px;}

#complete-banner{
  display:none;position:absolute;top:230px;left:50%;transform:translateX(-50%);
  background:rgba(6,78,59,0.95);border:2px solid #10b981;
  padding:16px 36px;border-radius:8px;text-align:center;z-index:70;
  box-shadow:0 0 60px rgba(16,185,129,0.7);pointer-events:none;
}

.cam-switcher{
  position:absolute;bottom:156px;right:20px;display:flex;gap:6px;z-index:50;pointer-events:auto;
}
.cam-btn{
  background:rgba(15,23,42,0.88);border:1px solid rgba(56,189,248,0.5);color:#38bdf8;
  font-size:10px;font-weight:800;padding:5px 10px;border-radius:4px;cursor:pointer;
  transition:all 0.2s;backdrop-filter:blur(4px);
}
.cam-btn:hover{background:rgba(56,189,248,0.3);color:#ffffff;}
.cam-btn.active{background:#0284c7;color:#ffffff;border-color:#38bdf8;box-shadow:0 0 10px rgba(56,189,248,0.8);}
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
</div>

<div id="pip-box" class="pip-window" title="クリックでサブモニター折りたたみ">
  <div class="pip-scan"></div>
  <div class="pip-header">
    <div id="pip-title" class="pip-label">CAM 02: ACTIVE TELEMETRY CHASE</div>
    <div id="pip-metric" class="pip-telemetry">EARTH RECESSION: 0 km/s | SCALE: LOW ORBIT</div>
    <div id="pip-btn" class="pip-toggle">[HIDE]</div>
  </div>
  <div class="pip-rec"><div class="rec-dot"></div>OPTICAL DUAL TRACKING LOCK</div>
</div>

<div class="cam-switcher">
  <button id="cam-btn-0" class="cam-btn active" onclick="switchCamMode(0)">AUTO DIRECTOR</button>
  <button id="cam-btn-1" class="cam-btn" onclick="switchCamMode(1)">MAIN CHASE</button>
  <button id="cam-btn-2" class="cam-btn" onclick="switchCamMode(2)">COCKPIT</button>
  <button id="cam-btn-3" class="cam-btn" onclick="switchCamMode(3)">WING-MOUNT</button>
  <button id="cam-btn-4" class="cam-btn" onclick="switchCamMode(4)">FLY-BY SPOT</button>
</div>

<div class="radar-panel">
  <div id="radar-label" class="radar-tag">TACTICAL RADAR<br><span style="color:#94a3b8;font-size:8px;">ORBITAL PROJECTION</span></div>
  <canvas id="radar-canvas"></canvas>
</div>

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
    pipBox.style.height = pipOpen ? '202px' : '26px';
    document.getElementById('pip-btn').innerText = pipOpen ? '[HIDE]' : '[SHOW]';
});

let activeCamMode = 0;
window.switchCamMode = function(mode) {
    activeCamMode = mode;
    for (let m = 0; m <= 4; m++) {
        const btn = document.getElementById(`cam-btn-${m}`);
        if (btn) {
            if (m === mode) btn.classList.add('active');
            else btn.classList.remove('active');
        }
    }
};

// =========================================================================
// 1. レンダラー構築＆PMREM IBL＆星雲パーティクル＆ポストプロセス
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
const cameraPip = new THREE.PerspectiveCamera(36, 16 / 9, 0.5, 950000);

// ★修正: 機体とバーナーを画面中央に美しく収める完璧なシネマチェイス座標
let baseCamPos = new THREE.Vector3(-18.0, 7.5, -46.0);
let baseTarget = new THREE.Vector3(0.0, 1.0, -2.0);

if (cfg.cam_preset.includes("エクストラ")) {
    baseCamPos.set(-36.0, 15.0, -78.0);
} else if (cfg.cam_preset.includes("チェイス")) {
    baseCamPos.set(-14.0, 5.0, -36.0);
}
cameraMain.position.copy(baseCamPos);
cameraMain.lookAt(baseTarget);

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
const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();
const rawSkyTex = makeSkyEnvTexture();
const envMapTexture = pmremGenerator.fromEquirectangular(rawSkyTex).texture;
scene.environment = envMapTexture;

const spaceFieldGroup = new THREE.Group();
scene.add(spaceFieldGroup);

function createStarField(count, radiusMin, radiusMax, size, baseColor) {
    const geo = new THREE.BufferGeometry();
    const pos = new Float32Array(count * 3);
    const col = new Float32Array(count * 3);
    const c = new THREE.Color(baseColor);

    for (let i = 0; i < count; i++) {
        const u = Math.random();
        const v = Math.random();
        const theta = u * 2.0 * Math.PI;
        const phi = Math.acos(2.0 * v - 1.0);
        const r = radiusMin + Math.random() * (radiusMax - radiusMin);

        pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
        pos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
        pos[i * 3 + 2] = r * Math.cos(phi);

        const variation = 0.7 + Math.random() * 0.6;
        col[i * 3] = c.r * variation;
        col[i * 3 + 1] = c.g * variation;
        col[i * 3 + 2] = c.b * variation;
    }
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
    const mat = new THREE.PointsMaterial({
        size: size,
        vertexColors: true,
        transparent: true,
        opacity: 0.9,
        sizeAttenuation: false
    });
    return new THREE.Points(geo, mat);
}

const deepStars = createStarField(4000, 250000, 600000, 1.8, 0xdbeafe);
const nebulaDust = createStarField(2500, 150000, 450000, 2.5, 0x38bdf8);
const milkyWayStars = createStarField(3000, 100000, 300000, 1.4, 0xf472b6);
spaceFieldGroup.add(deepStars);
spaceFieldGroup.add(nebulaDust);
spaceFieldGroup.add(milkyWayStars);

const sunLight = new THREE.DirectionalLight(cfg.env.sun_color, cfg.env.sun_int);
sunLight.position.set(cfg.env.sun_pos[0] * 0.15, cfg.env.sun_pos[1] * 0.15 + 40.0, cfg.env.sun_pos[2] * 0.15);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 10;
sunLight.shadow.camera.far = 800;
sunLight.shadow.camera.left = -90;
sunLight.shadow.camera.right = 90;
sunLight.shadow.camera.top = 90;
sunLight.shadow.camera.bottom = -90;
sunLight.shadow.bias = -0.0005;
scene.add(sunLight);

const rimLight = new THREE.DirectionalLight(0x93c5fd, 2.0);
rimLight.position.set(-60, 45, 60);
scene.add(rimLight);

const hemiLight = new THREE.HemisphereLight(0x93c5fd, 0x0f172a, 1.8);
scene.add(hemiLight);

const WarpDistortionShader = {
    uniforms: {
        "tDiffuse": { value: null },
        "uDistort": { value: 0.0 },
        "uTime": { value: 0.0 },
        "uDroplets": { value: 0.0 },
        "uGForce": { value: 0.0 }
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
        uniform float uDroplets;
        uniform float uGForce;
        varying vec2 vUv;

        float random(vec2 p) {
            return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
        }

        void main() {
            vec2 center = vec2(0.5, 0.5);
            vec2 uv = vUv;
            vec2 dir = uv - center;
            float dist = length(dir);

            float ringDistort = sin(dist * 18.0 - uTime * 4.0) * exp(-dist * 3.5) * uDistort * 0.05;
            vec2 rUv = uv + dir * (dist * uDistort * 0.09 + ringDistort);
            vec2 gUv = uv;
            vec2 bUv = uv - dir * (dist * uDistort * 0.09 + ringDistort);

            if (uDroplets > 0.01) {
                float drop = sin(uv.x * 65.0) * cos(uv.y * 65.0);
                if (drop > 0.88) {
                    vec2 dropOffset = vec2(cos(drop * 20.0), sin(drop * 20.0)) * 0.015 * uDroplets;
                    rUv += dropOffset; gUv += dropOffset; bUv += dropOffset;
                }
            }

            float r = texture2D(tDiffuse, rUv).r;
            float g = texture2D(tDiffuse, gUv).g;
            float b = texture2D(tDiffuse, bUv).b;
            vec3 col = vec3(r, g, b);

            float grain = (random(uv * 1000.0 + uTime) - 0.5) * 0.035;
            col += grain;

            float vig = smoothstep(0.85, 0.25, dist);
            col *= vig;

            if (uGForce > 3.0) {
                float gFactor = clamp((uGForce - 3.0) / 12.0, 0.0, 0.85);
                float tunnel = smoothstep(0.9 - gFactor * 0.45, 0.25, dist);
                col = mix(col, vec3(0.0), (1.0 - tunnel) * gFactor);
            }

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

const radarCanvas = document.getElementById('radar-canvas');
const rCtx = radarCanvas.getContext('2d');
const radarLabelEl = document.getElementById('radar-label');

function resizeRadarCanvas() {
    radarCanvas.width = radarCanvas.clientWidth * 1.5;
    radarCanvas.height = radarCanvas.clientHeight * 1.5;
}
resizeRadarCanvas();

window.addEventListener('resize', () => {
    W = window.innerWidth; H = window.innerHeight;
    renderer.setSize(W, H);
    composerMain.setSize(W, H);
    cameraMain.aspect = W / H;
    cameraMain.updateProjectionMatrix();
    resizeRadarCanvas();
});

// =========================================================================
// 2. 音声合成キュー制御・Web Audioシンセビープ＆ソニックブーム
// =========================================================================
let actx = null, rocketGain = null, rocketFilter = null, coilOsc = null, coilGain = null, warpOsc = null, warpGain = null, rcsGain = null;
let lastAnnouncedPhase = "";
let hasTriggeredBoom = false;

function playRadioBeep() {
    if (!actx) return;
    try {
        const o = actx.createOscillator();
        const g = actx.createGain();
        o.type = 'sine';
        o.frequency.setValueAtTime(880, actx.currentTime);
        o.frequency.setValueAtTime(1760, actx.currentTime + 0.04);
        g.gain.setValueAtTime(0.08, actx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.001, actx.currentTime + 0.12);
        o.connect(g);
        g.connect(actx.destination);
        o.start();
        o.stop(actx.currentTime + 0.13);
    } catch(e){}
}

function speakCallout(text) {
    playRadioBeep();
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        setTimeout(() => {
            const u = new SpeechSynthesisUtterance(text);
            u.rate = 1.05; u.pitch = 1.1; u.volume = 0.85;
            window.speechSynthesis.speak(u);
        }, 15);
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
    } catch(e){}
}

function playSonicBoomSound() {
    if (!actx) return;
    try {
        const osc = actx.createOscillator();
        const g = actx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(140, actx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(25, actx.currentTime + 0.6);
        g.gain.setValueAtTime(0.8, actx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.001, actx.currentTime + 0.7);
        osc.connect(g);
        g.connect(actx.destination);
        osc.start();
        osc.stop(actx.currentTime + 0.75);
    } catch(e){}
}

initAudioSystem();
window.addEventListener('pointerdown', () => { if (actx && actx.state === 'suspended') actx.resume(); }, { once: true });
window.addEventListener('keydown', () => { if (actx && actx.state === 'suspended') actx.resume(); }, { once: true });

// =========================================================================
// 3. プロシージャルテクスチャ＆PBRマテリアル
// =========================================================================
function makeAztecHullTexture() {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 1024;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#475569'; ctx.fillRect(0, 0, 1024, 1024);

    for (let x = 0; x < 1024; x += 64) {
        for (let y = 0; y < 1024; y += 32) {
            const v = 90 + Math.floor(Math.random() * 65);
            ctx.fillStyle = `rgb(${v},${v+3},${v+8})`;
            ctx.fillRect(x + 2, y + 2, 60, 28);

            ctx.fillStyle = '#0f172a';
            ctx.fillRect(x + 6, y + 6, 2, 2);
            ctx.fillRect(x + 54, y + 6, 2, 2);
            ctx.fillRect(x + 6, y + 22, 2, 2);
            ctx.fillRect(x + 54, y + 22, 2, 2);
        }
    }
    ctx.strokeStyle = '#1e293b'; ctx.lineWidth = 2.5;
    for (let x = 0; x <= 1024; x += 64) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 1024); ctx.stroke(); }
    for (let y = 0; y <= 1024; y += 32) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(1024, y); ctx.stroke(); }

    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(4, 4);
    return tex;
}
const hullPbrTex = makeAztecHullTexture();

function makeTileTexture() {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#0f172a'; ctx.fillRect(0, 0, 512, 512);
    ctx.strokeStyle = '#020617'; ctx.lineWidth = 3;
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

function makeRoughnessMap() {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#808080'; ctx.fillRect(0, 0, 512, 512);
    for (let i = 0; i < 200; i++) {
        const r = Math.floor(Math.random() * 180 + 50);
        ctx.fillStyle = `rgb(${r},${r},${r})`;
        ctx.fillRect(Math.random() * 512, Math.random() * 512, 32, 24);
    }
    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(4, 4);
    return tex;
}
const roughnessTex = makeRoughnessMap();

function makeHeatStainTexture() {
    const c = document.createElement('canvas'); c.width = 256; c.height = 256;
    const ctx = c.getContext('2d');
    const grad = ctx.createLinearGradient(0, 0, 0, 256);
    grad.addColorStop(0.0, '#38bdf8');
    grad.addColorStop(0.35, '#818cf8');
    grad.addColorStop(0.70, '#f59e0b');
    grad.addColorStop(1.0, '#78350f');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 256, 256);
    return new THREE.CanvasTexture(c);
}
const heatStainTex = makeHeatStainTexture();

const matHull = new THREE.MeshPhysicalMaterial({
    color: cfg.hull_color, metalness: cfg.metalness, roughness: cfg.roughness,
    bumpMap: hullPbrTex, bumpScale: 0.04, roughnessMap: roughnessTex,
    clearcoat: 0.9, clearcoatRoughness: 0.12, emissive: 0x000000, emissiveIntensity: 0.0
});
const matBellyTile = new THREE.MeshStandardMaterial({
    color: cfg.belly_color, metalness: 0.35, roughness: 0.75,
    bumpMap: tileTex, bumpScale: 0.06, roughnessMap: tileTex, emissive: 0x000000, emissiveIntensity: 0.0
});
const matTitaniumFrame = new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.92, roughness: 0.20 });
const matPistonRod = new THREE.MeshStandardMaterial({ color: 0xf8fafc, metalness: 0.98, roughness: 0.05 });
const matDarkAlloy = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.92, roughness: 0.22 });
const matGoldMLI = new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.96, roughness: 0.20, bumpMap: tileTex, bumpScale: 0.02 });
const matCopperCoil = new THREE.MeshStandardMaterial({ color: 0xd97706, metalness: 0.95, roughness: 0.15 });
const matCanopy = new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, metalness: 0.95, roughness: 0.03, transparent: true, opacity: 0.42, clearcoat: 1.0 });
const matRadiator = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.82, roughness: 0.28, emissive: 0xef4444, emissiveIntensity: 0.0 });
const matConcreteWet = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.45, metalness: 0.35, bumpMap: hullPbrTex, bumpScale: 0.06 });
const matCryoPipe = new THREE.MeshStandardMaterial({ color: 0xdbeafe, roughness: 0.65, metalness: 0.25 });
const matHeatStain = new THREE.MeshStandardMaterial({ map: heatStainTex, metalness: 0.85, roughness: 0.25 });

// =========================================================================
// 4. 極限細密スプラインロフト宇宙船・二重ノズル＆推力偏向＆パイピング
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
const sealPaddles = [];
const nozzlePistonLinks = [];
const radiatorPanels = [];
const hydraulicPistons = [];
const wingPivots = [];
const controlSurfaces = [];
const sabotClamps = [];
const fairingPanels = [];
const strobeLeds = [];
const rcsJets = [];
const laserBeams = [];

const innerSkeletonGroup = new THREE.Group();
shipMeshGroup.add(innerSkeletonGroup);

const spineCore = new THREE.Mesh(new THREE.BoxGeometry(2.2, 1.2, 28.0), matTitaniumFrame);
spineCore.castShadow = true;
innerSkeletonGroup.add(spineCore);

const mliCore = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 26.0, 16), matGoldMLI);
mliCore.rotation.x = Math.PI / 2;
innerSkeletonGroup.add(mliCore);

for (let s of [-1, 1]) {
    const pipePts = [
        new THREE.Vector3(s * 1.5, -0.4, 12.0),
        new THREE.Vector3(s * 2.2, -0.2, 4.0),
        new THREE.Vector3(s * 2.8, -0.3, -4.0),
        new THREE.Vector3(s * 1.9, 0.2, -12.0),
        new THREE.Vector3(s * 0.9, 0.0, -15.0)
    ];
    const pipeCurve = new THREE.CatmullRomCurve3(pipePts);
    const pipeGeo = new THREE.TubeGeometry(pipeCurve, 32, 0.16, 10, false);
    const pipeMesh = new THREE.Mesh(pipeGeo, matCryoPipe);
    pipeMesh.castShadow = true;
    innerSkeletonGroup.add(pipeMesh);

    for (let fIdx = 0; fIdx < 4; fIdx++) {
        const fZ = -10.0 + fIdx * 6.0;
        const flange = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.08, 12), matGoldMLI);
        flange.rotation.x = Math.PI / 2;
        flange.position.set(s * 2.2, -0.25, fZ);
        innerSkeletonGroup.add(flange);
    }
}

for (let bz = -12.0; bz <= 10.0; bz += 2.5) {
    const bulkhead = new THREE.Mesh(new THREE.TorusGeometry(2.1, 0.08, 6, 16), matTitaniumFrame);
    bulkhead.position.set(0, 0.1, bz);
    innerSkeletonGroup.add(bulkhead);
}

const cockpitGroup = new THREE.Group();
cockpitGroup.position.set(0, 0.7, 7.5);
shipMeshGroup.add(cockpitGroup);

for (let s of [-0.4, 0.4]) {
    const seat = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.9, 0.6), matDarkAlloy);
    seat.position.set(s, 0, 0);
    cockpitGroup.add(seat);
    const pilotHead = new THREE.Mesh(new THREE.SphereGeometry(0.18, 12, 12), matDarkAlloy);
    pilotHead.position.set(s, 0.55, 0.05);
    cockpitGroup.add(pilotHead);
    const visor = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.08, 0.1), new THREE.MeshBasicMaterial({ color: 0x38bdf8 }));
    visor.position.set(s, 0.57, 0.18);
    cockpitGroup.add(visor);
}

const consoleHolo = new THREE.Mesh(
    new THREE.PlaneGeometry(1.2, 0.35),
    new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.85, side: THREE.DoubleSide })
);
consoleHolo.rotation.x = -0.5;
consoleHolo.position.set(0, 0.25, 1.2);
cockpitGroup.add(consoleHolo);

function createLoftedChassisGeometry() {
    const sections = [
        { z: 18.0, w: 0.1, hTop: 0.1, hBtm: 0.1, yOff: 0.0 },
        { z: 14.0, w: 1.8, hTop: 0.7, hBtm: 0.4, yOff: 0.1 },
        { z: 9.0,  w: 3.8, hTop: 1.3, hBtm: 0.8, yOff: 0.25 },
        { z: 4.0,  w: 4.8, hTop: 1.5, hBtm: 1.0, yOff: 0.2 },
        { z: -2.0, w: 5.4, hTop: 1.6, hBtm: 1.1, yOff: 0.1 },
        { z: -8.0, w: 5.2, hTop: 1.5, hBtm: 1.2, yOff: 0.0 },
        { z: -14.0,w: 4.2, hTop: 1.3, hBtm: 1.2, yOff: -0.1 }
    ];
    const radialSegs = 24;
    const zSegs = sections.length;
    const geo = new THREE.BufferGeometry();
    const pos = [];
    const uvs = [];
    const indices = [];

    for (let j = 0; j < zSegs; j++) {
        const sec = sections[j];
        for (let i = 0; i <= radialSegs; i++) {
            const theta = (i / radialSegs) * Math.PI * 2;
            const cosT = Math.cos(theta);
            const sinT = Math.sin(theta);
            const h = sinT >= 0 ? sec.hTop : sec.hBtm;
            const x = cosT * (sec.w * 0.5);
            const y = sec.yOff + sinT * h;
            const z = sec.z;
            pos.push(x, y, z);
            uvs.push(i / radialSegs, j / (zSegs - 1));
        }
    }

    for (let j = 0; j < zSegs - 1; j++) {
        for (let i = 0; i < radialSegs; i++) {
            const a = j * (radialSegs + 1) + i;
            const b = (j + 1) * (radialSegs + 1) + i;
            const c = (j + 1) * (radialSegs + 1) + (i + 1);
            const d = j * (radialSegs + 1) + (i + 1);
            indices.push(a, b, d);
            indices.push(b, c, d);
        }
    }

    geo.setIndex(indices);
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    geo.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
    geo.computeVertexNormals();
    return geo;
}

if (cfg.style === "stealth_waverider") {
    const loftChassisGeo = createLoftedChassisGeometry();
    const chassisMesh = new THREE.Mesh(loftChassisGeo, matHull);
    chassisMesh.castShadow = true; chassisMesh.receiveShadow = true;
    shipMeshGroup.add(chassisMesh);

    const bellyLoftMesh = new THREE.Mesh(loftChassisGeo, matBellyTile);
    bellyLoftMesh.scale.set(0.985, 0.98, 0.995);
    bellyLoftMesh.position.set(0, -0.06, 0);
    bellyLoftMesh.castShadow = true; bellyLoftMesh.receiveShadow = true;
    shipMeshGroup.add(bellyLoftMesh);

    for (let s of [-1, 1]) {
        const intakeDuct = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.2, 8.5), matDarkAlloy);
        intakeDuct.position.set(s * 2.8, -0.4, 0.0);
        intakeDuct.castShadow = true;
        shipMeshGroup.add(intakeDuct);

        const intakeOpening = new THREE.Mesh(new THREE.PlaneGeometry(1.4, 0.9), new THREE.MeshBasicMaterial({ color: 0x050b14, side: THREE.DoubleSide }));
        intakeOpening.position.set(s * 2.8, -0.4, 4.3);
        shipMeshGroup.add(intakeOpening);

        const vTail = new THREE.Mesh(new THREE.BoxGeometry(0.22, 4.8, 6.5), matHull);
        vTail.position.set(s * 3.8, 2.2, -10.8);
        vTail.rotation.z = -s * 0.32;
        vTail.castShadow = true;
        shipMeshGroup.add(vTail);

        const ruffler = new THREE.Mesh(new THREE.BoxGeometry(0.18, 3.8, 1.4), matDarkAlloy);
        ruffler.position.set(s * 4.4, 2.2, -13.5);
        ruffler.rotation.z = -s * 0.32;
        shipMeshGroup.add(ruffler);
        controlSurfaces.push({ mesh: ruffler, side: s, type: 'rudder' });

        const strobe = new THREE.Mesh(new THREE.SphereGeometry(0.14, 8, 8), new THREE.MeshBasicMaterial({ color: 0xffffff }));
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
        fairingPanels.push({ mesh: fPanel, baseX: fPanel.position.x, baseY: fPanel.position.y, ang: ang });
    }
}

const canopyGlass = new THREE.Mesh(new THREE.ConeGeometry(1.35, 7.5, 16), matCanopy);
canopyGlass.scale.set(1.0, 0.48, 1.6);
canopyGlass.rotation.x = Math.PI / 2;
canopyGlass.position.set(0, 0.95, 8.8);
canopyGlass.castShadow = true;
shipMeshGroup.add(canopyGlass);

const halfSpan = cfg.wings_span * 0.5;
const wingtipVortices = [];

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

    const elevonGeo = new THREE.BoxGeometry(halfSpan * 0.45, 0.18, 1.6);
    const elevonMesh = new THREE.Mesh(elevonGeo, matDarkAlloy);
    elevonMesh.position.set(s * (halfSpan * 0.55), 0, -8.6);
    pivot.add(elevonMesh);
    controlSurfaces.push({ mesh: elevonMesh, side: s, type: 'elevon' });

    for (let f = 1; f <= 3; f++) {
        const fairingPod = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.02, 2.2, 8), matTitaniumFrame);
        fairingPod.rotation.x = Math.PI / 2;
        fairingPod.position.set(s * (2.0 + f * (halfSpan - 4.5) / 3.0), -0.22, -6.5);
        pivot.add(fairingPod);
    }

    const tipLed = new THREE.Mesh(new THREE.SphereGeometry(0.16, 8, 8), new THREE.MeshBasicMaterial({ color: s > 0 ? 0x10b981 : 0xef4444 }));
    tipLed.position.set(s * (halfSpan - 3.4), 0, -5.5);
    pivot.add(tipLed);
    strobeLeds.push(tipLed);

    const vortexGeo = new THREE.CylinderGeometry(0.08, 0.85, 45.0, 8, 1, true);
    const vortexMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.0, side: THREE.DoubleSide, depthWrite: false });
    const vortexMesh = new THREE.Mesh(vortexGeo, vortexMat);
    vortexMesh.rotation.x = Math.PI / 2;
    vortexMesh.position.set(s * (halfSpan - 3.4), 0, -28.0);
    pivot.add(vortexMesh);
    wingtipVortices.push({ mesh: vortexMesh, mat: vortexMat });

    wingPivots.push({ group: pivot, side: s });
}

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

        const innerDoorFrame = new THREE.Mesh(new THREE.BoxGeometry(2.2, 0.12, 6.0), matDarkAlloy);
        innerDoorFrame.position.set(-s * 1.1, -0.1, 0);
        doorPivot.add(innerDoorFrame);

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

for (let s of [-1, 1]) {
    for (let z of [10.0, -10.0]) {
        const rcsBlock = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.4, 0.6), matTitaniumFrame);
        rcsBlock.position.set(s * 2.6, 0.2, z);
        shipMeshGroup.add(rcsBlock);

        const rcsMat = new THREE.MeshBasicMaterial({ color: 0xdbeafe, transparent: true, opacity: 0.0, depthWrite: false });
        const rcsCone = new THREE.Mesh(new THREE.ConeGeometry(0.35, 2.8, 8, 1, true), rcsMat);
        rcsCone.rotation.z = s * (Math.PI / 2);
        rcsCone.position.set(s * 3.1, 0.2, z);
        shipMeshGroup.add(rcsCone);
        rcsJets.push({ cone: rcsCone, mat: rcsMat });
    }
}

const warpRingAssembly = new THREE.Group();
warpRingAssembly.position.set(0, -0.8, -2.5);
shipMeshGroup.add(warpRingAssembly);

const ringPylon = new THREE.Mesh(new THREE.BoxGeometry(1.6, 3.8, 4.5), matTitaniumFrame);
ringPylon.position.set(0, -1.8, 0);
warpRingAssembly.add(ringPylon);

const rotorClockwise = new THREE.Group();
const rotorCounter = new THREE.Group();
warpRingAssembly.add(rotorClockwise);
warpRingAssembly.add(rotorCounter);

const segmentCount = 16;
const ringSegments = [];
for (let i = 0; i < segmentCount; i++) {
    const ang = (i / segmentCount) * Math.PI * 2;
    const segPivot = new THREE.Group();
    segPivot.rotation.z = ang;
    rotorClockwise.add(segPivot);

    const block = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.45, 1.8), matDarkAlloy);
    block.position.set(0, 6.2, 0);
    block.castShadow = true;
    segPivot.add(block);

    const coilCore = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.35, 1.4), new THREE.MeshBasicMaterial({ color: cfg.aurora_hex }));
    coilCore.position.set(0, 6.2, 0);
    segPivot.add(coilCore);

    ringSegments.push({ block, coilCore, baseR: 6.2 });
}

const counterTorus = new THREE.Mesh(new THREE.TorusGeometry(5.4, 0.18, 12, 48), matCopperCoil);
rotorCounter.add(counterTorus);

const rippleGeos = [];
for (let rp = 0; rp < 3; rp++) {
    const rip = new THREE.Mesh(
        new THREE.RingGeometry(4.5, 7.8, 32),
        new THREE.MeshBasicMaterial({ color: cfg.spark_hex, transparent: true, opacity: 0.0, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false })
    );
    rip.position.z = -rp * 3.5;
    warpRingAssembly.add(rip);
    rippleGeos.push(rip);
}

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

const accretionRing = new THREE.Mesh(
    new THREE.RingGeometry(5.4, 9.8, 48),
    new THREE.MeshBasicMaterial({ color: 0x38bdf8, side: THREE.DoubleSide, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending })
);
warpRingAssembly.add(accretionRing);

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

// エンジン＆推力偏向ジンバル根元
const nozzleGimbalRoot = new THREE.Group();
nozzleGimbalRoot.position.set(0, 0, -14.2);
shipMeshGroup.add(nozzleGimbalRoot);

const combustionThroat = new THREE.Mesh(
    new THREE.CylinderGeometry(1.8, 2.1, 1.8, 24, 1, true),
    new THREE.MeshBasicMaterial({ color: 0xffffff })
);
combustionThroat.rotation.x = Math.PI / 2;
combustionThroat.position.z = 1.0;
nozzleGimbalRoot.add(combustionThroat);

const heatShroud = new THREE.Mesh(new THREE.CylinderGeometry(2.7, 2.8, 2.4, 32, 1, true), matHeatStain);
heatShroud.rotation.x = Math.PI / 2;
heatShroud.position.z = -0.6;
nozzleGimbalRoot.add(heatShroud);

for (let inj = 1; inj <= 3; inj++) {
    const injRing = new THREE.Mesh(
        new THREE.TorusGeometry(inj * 0.65, 0.06, 8, 32),
        new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.95, roughness: 0.1, emissive: cfg.flame_hex, emissiveIntensity: 0.5 })
    );
    injRing.position.z = 0.6;
    nozzleGimbalRoot.add(injRing);
}

for (let i = 0; i < 12; i++) {
    const ang = (i / 12) * Math.PI * 2;
    const petalPivot = new THREE.Group();
    petalPivot.position.set(Math.cos(ang) * 2.5, Math.sin(ang) * 2.5, -1.0);
    petalPivot.rotation.z = ang;
    nozzleGimbalRoot.add(petalPivot);

    const outerPetal = new THREE.Mesh(new THREE.BoxGeometry(1.1, 0.12, 3.2), matTitaniumFrame);
    outerPetal.position.set(0, 0.08, -1.4);
    outerPetal.castShadow = true;
    petalPivot.add(outerPetal);
    irisPaddles.push(petalPivot);

    const sealPivot = new THREE.Group();
    const sealAng = ang + Math.PI / 12;
    sealPivot.position.set(Math.cos(sealAng) * 2.35, Math.sin(sealAng) * 2.35, -1.0);
    sealPivot.rotation.z = sealAng;
    nozzleGimbalRoot.add(sealPivot);

    const innerSeal = new THREE.Mesh(new THREE.BoxGeometry(0.95, 0.08, 3.0), matDarkAlloy);
    innerSeal.position.set(0, 0.04, -1.3);
    sealPivot.add(innerSeal);
    sealPaddles.push(sealPivot);

    const linkCyl = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1.2, 6), matDarkAlloy);
    linkCyl.position.set(Math.cos(ang) * 2.8, Math.sin(ang) * 2.8, -0.6);
    linkCyl.rotation.x = Math.PI / 2;
    nozzleGimbalRoot.add(linkCyl);
    nozzlePistonLinks.push(linkCyl);
}

for (let s of [-1, 1]) {
    const sabot = new THREE.Mesh(new THREE.BoxGeometry(2.2, 1.1, 7.5), matDarkAlloy);
    sabot.position.set(s * 3.8, -1.4, -1.0);
    sabot.castShadow = true;
    shipMeshGroup.add(sabot);
    sabotClamps.push({ mesh: sabot, baseX: s * 3.8, side: s });
}

const sonicBoomDiscMat = new THREE.MeshBasicMaterial({
    color: 0xffffff, transparent: true, opacity: 0.0, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false
});
const sonicBoomDisc = new THREE.Mesh(new THREE.RingGeometry(0.5, 14.0, 32), sonicBoomDiscMat);
sonicBoomDisc.position.set(0, 0, 0);
shipMeshGroup.add(sonicBoomDisc);

const vaporShaderMat = new THREE.ShaderMaterial({
    vertexShader: `
        varying vec2 vUv;
        void main() {
            vUv = uv;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        uniform float uAlpha;
        uniform float uTime;
        varying vec2 vUv;
        void main() {
            float noise = sin(vUv.x * 25.0 + uTime * 35.0) * cos(vUv.y * 30.0 - uTime * 20.0);
            float rim = pow(vUv.y, 2.0);
            float tear = smoothstep(0.15, 0.85, vUv.y + noise * 0.18);
            gl_FragColor = vec4(1.0, 1.0, 1.0, uAlpha * rim * tear * 0.75);
        }
    `,
    uniforms: { uAlpha: { value: 0.0 }, uTime: { value: 0.0 } },
    transparent: true, depthWrite: false, side: THREE.DoubleSide
});
const vaporCone1 = new THREE.Mesh(new THREE.ConeGeometry(8.5, 4.2, 32, 1, true), vaporShaderMat);
vaporCone1.rotation.x = -Math.PI / 2;
vaporCone1.position.set(0, 0, 1.0);
shipMeshGroup.add(vaporCone1);

const vaporCone2 = new THREE.Mesh(new THREE.ConeGeometry(5.2, 2.8, 32, 1, true), vaporShaderMat);
vaporCone2.rotation.x = -Math.PI / 2;
vaporCone2.position.set(0, 0.4, 7.5);
shipMeshGroup.add(vaporCone2);

const plasmaBowMat = new THREE.MeshBasicMaterial({ color: cfg.plasma_hex, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending, depthWrite: false });
const plasmaBow = new THREE.Mesh(new THREE.SphereGeometry(4.8, 24, 24, 0, Math.PI * 2, 0, Math.PI * 0.5), plasmaBowMat);
plasmaBow.rotation.x = -Math.PI / 2;
plasmaBow.position.set(0, 0, 15.0);
shipMeshGroup.add(plasmaBow);

const leadingEdgeMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending });
for (let s of [-1, 1]) {
    const edgePts = [new THREE.Vector3(s * 0.2, 0.2, 16.0), new THREE.Vector3(s * 3.5, 0.0, 3.0), new THREE.Vector3(s * halfSpan, 0.0, -4.5)];
    const edgeCurve = new THREE.CatmullRomCurve3(edgePts);
    const edgeMesh = new THREE.Mesh(new THREE.TubeGeometry(edgeCurve, 20, 0.08, 6, false), leadingEdgeMat);
    shipMeshGroup.add(edgeMesh);
}

const sparkCount = 280;
const sparkGeo = new THREE.BufferGeometry();
const sparkPos = new Float32Array(sparkCount * 6);
for (let i = 0; i < sparkCount; i++) {
    const rx = (Math.random() - 0.5) * 6.0, ry = (Math.random() - 0.5) * 2.5, rz = Math.random() * 20.0;
    sparkPos[i * 6] = rx; sparkPos[i * 6 + 1] = ry; sparkPos[i * 6 + 2] = rz;
    sparkPos[i * 6 + 3] = rx; sparkPos[i * 6 + 4] = ry; sparkPos[i * 6 + 5] = rz - 6.0;
}
sparkGeo.setAttribute('position', new THREE.BufferAttribute(sparkPos, 3));
const sparkMat = new THREE.LineBasicMaterial({ color: 0xf59e0b, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending });
const sparkLines = new THREE.LineSegments(sparkGeo, sparkMat);
shipMeshGroup.add(sparkLines);

// 推進バーナー炎
const plumeRoot = new THREE.Group();
plumeRoot.position.set(0, 0, -2.3);
nozzleGimbalRoot.add(plumeRoot);

const plumeLight = new THREE.PointLight(cfg.flame_hex, 0.0, 160.0);
plumeLight.position.set(0, 0, -2.0);
plumeRoot.add(plumeLight);

const flareTexMat = new THREE.MeshBasicMaterial({
    color: cfg.flame_hex, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending, depthWrite: false
});
const anamorphicFlare = new THREE.Mesh(new THREE.PlaneGeometry(55.0, 1.2), flareTexMat);
anamorphicFlare.position.set(0, 0, -2.5);
plumeRoot.add(anamorphicFlare);

const flameShaderMat = new THREE.ShaderMaterial({
    vertexShader: `
        varying vec2 vUv;
        varying vec3 vNormal;
        void main() {
            vUv = uv;
            vNormal = normalize(normalMatrix * normal);
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        varying vec2 vUv;
        varying vec3 vNormal;
        uniform float uTime;
        uniform vec3 uColor;
        void main() {
            float noise = sin(vUv.y * 35.0 - uTime * 28.0) * cos(vUv.x * 20.0 + uTime * 15.0);
            float core = pow(1.0 - abs(vUv.x - 0.5) * 2.0, 3.0);
            float taper = pow(1.0 - vUv.y, 1.5);
            vec3 col = mix(uColor, vec3(1.0, 1.0, 1.0), core * 0.85);
            float alpha = (core + noise * 0.25) * taper * 0.88;
            gl_FragColor = vec4(col, clamp(alpha, 0.0, 1.0));
        }
    `,
    uniforms: {
        uTime: { value: 0.0 },
        uColor: { value: new THREE.Color(cfg.flame_hex) }
    },
    transparent: true,
    blending: THREE.AdditiveBlending,
    side: THREE.DoubleSide,
    depthWrite: false
});

const jetCylinder = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 4.8, 44.0, 32, 1, true), flameShaderMat);
jetCylinder.rotation.x = Math.PI / 2;
jetCylinder.position.z = -22.0;
plumeRoot.add(jetCylinder);

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

// 連射されるプラズマパルス渦輪
const pulseRings = [];
for (let pr = 0; pr < 6; pr++) {
    const pRing = new THREE.Mesh(
        new THREE.TorusGeometry(1.8, 0.22, 8, 24),
        new THREE.MeshBasicMaterial({ color: cfg.flame_hex, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending })
    );
    plumeRoot.add(pRing);
    pulseRings.push(pRing);
}

for (let s of [-1, 1]) {
    const lBeamMat = new THREE.LineBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending, linewidth: 2 });
    const lGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(s * 1.8, 0, 10.0), new THREE.Vector3(s * 4.0, 0, 90.0)]);
    const lLine = new THREE.Line(lGeo, lBeamMat);
    shipMeshGroup.add(lLine);
    laserBeams.push(lLine);
}

const debrisTargetGroup = new THREE.Group();
debrisTargetGroup.position.set(0, 0, 95.0);
debrisTargetGroup.visible = false;
shipMeshGroup.add(debrisTargetGroup);

const targetBoxMesh = new THREE.LineSegments(
    new THREE.EdgesGeometry(new THREE.BoxGeometry(4.2, 4.2, 0.1)),
    new THREE.LineBasicMaterial({ color: 0xf43f5e, linewidth: 2 })
);
debrisTargetGroup.add(targetBoxMesh);

function makeHoloHudTexture() {
    const c = document.createElement('canvas'); c.width = 512; c.height = 256;
    const ctx = c.getContext('2d');
    ctx.strokeStyle = '#38bdf8'; ctx.lineWidth = 4;
    ctx.strokeRect(10, 10, 492, 236);
    ctx.fillStyle = 'rgba(14,165,233,0.18)';
    ctx.fillRect(10, 10, 492, 236);
    ctx.font = 'bold 28px monospace';
    ctx.fillStyle = '#f8fafc';
    ctx.fillText('TARGET VECTOR LOCKED', 40, 60);
    ctx.font = 'bold 22px monospace';
    ctx.fillStyle = '#38bdf8';
    ctx.fillText('ALCUBIERRE RING: ARMED', 40, 110);
    ctx.fillText('FIELD: 9.85 TeV / FLUX NOMINAL', 40, 155);
    ctx.fillText('G-LOAD STABILIZER: 100%', 40, 200);
    return new THREE.CanvasTexture(c);
}
const holoHudMat = new THREE.SpriteMaterial({ map: makeHoloHudTexture(), transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending });
const holoHudSprite = new THREE.Sprite(holoHudMat);
holoHudSprite.scale.set(8.5, 4.25, 1.0);
holoHudSprite.position.set(0, 3.8, 8.0);
shipMeshGroup.add(holoHudSprite);

// =========================================================================
// ★魔改造: 常時稼働ハイスピード・スペースダスト＆近景光速ストリーク粒子群
// =========================================================================
const dustCount = 650;
const dustGeo = new THREE.BufferGeometry();
const dustPos = new Float32Array(dustCount * 6);
for (let i = 0; i < dustCount; i++) {
    const rx = (Math.random() - 0.5) * 45.0;
    const ry = (Math.random() - 0.5) * 30.0;
    const rz = (Math.random() - 0.5) * 220.0;
    dustPos[i * 6] = rx; dustPos[i * 6 + 1] = ry; dustPos[i * 6 + 2] = rz;
    dustPos[i * 6 + 3] = rx; dustPos[i * 6 + 4] = ry; dustPos[i * 6 + 5] = rz - 2.5;
}
dustGeo.setAttribute('position', new THREE.BufferAttribute(dustPos, 3));
const dustMat = new THREE.LineBasicMaterial({ color: 0x93c5fd, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending });
const ambientSpaceDust = new THREE.LineSegments(dustGeo, dustMat);
scene.add(ambientSpaceDust);

// ★魔改造: 連続通過する3Dホログラム空間誘導ゲート群
const waypointRingCount = 12;
const waypointRings = [];
for (let wr = 0; wr < waypointRingCount; wr++) {
    const ringShape = new THREE.RingGeometry(18.0, 19.5, 8);
    const ringMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.45, side: THREE.DoubleSide, blending: THREE.AdditiveBlending });
    const ringMesh = new THREE.Mesh(ringShape, ringMat);
    ringMesh.position.set(0, 0, wr * 75.0);
    scene.add(ringMesh);
    waypointRings.push(ringMesh);
}

// ★魔改造: ワープ時空曲率ワイヤーフレーム・グリッド
const warpGridMat = new THREE.ShaderMaterial({
    vertexShader: `
        varying vec2 vUv;
        varying vec3 vPos;
        void main() {
            vUv = uv;
            vPos = position;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        varying vec2 vUv;
        varying vec3 vPos;
        uniform float uTime;
        uniform float uAlpha;
        void main() {
            vec2 g = abs(fract(vUv * 35.0 - vec2(0.0, uTime * 4.0)) - 0.5);
            float line = 1.0 - smoothstep(0.01, 0.08, min(g.x, g.y));
            float distFade = smoothstep(120.0, 10.0, abs(vPos.z));
            gl_FragColor = vec4(0.22, 0.74, 0.98, line * distFade * uAlpha);
        }
    `,
    uniforms: { uTime: { value: 0.0 }, uAlpha: { value: 0.0 } },
    transparent: true, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false
});
const warpCurvatureGrid = new THREE.Mesh(new THREE.PlaneGeometry(90.0, 240.0, 32, 32), warpGridMat);
warpCurvatureGrid.rotation.x = Math.PI / 2;
warpCurvatureGrid.position.set(0, -6.5, 0);
scene.add(warpCurvatureGrid);

// =========================================================================
// 5. カタパルト＆誘導灯＆波浪海面
// =========================================================================
const catapultSlopeRoot = new THREE.Group();
catapultSlopeRoot.rotation.x = -radAngle;
scene.add(catapultSlopeRoot);

const railMover = new THREE.Group();
catapultSlopeRoot.add(railMover);

const arcLineGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0,0,0), new THREE.Vector3(0,0,0)]);
const arcLineMat = new THREE.LineBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.0, linewidth: 2 });
const arcLine = new THREE.Line(arcLineGeo, arcLineMat);
catapultSlopeRoot.add(arcLine);

const arcLight = new THREE.PointLight(0x38bdf8, 0.0, 80.0);
catapultSlopeRoot.add(arcLight);

const dummy = new THREE.Object3D();
const segCount = 220;
const archInst = new THREE.InstancedMesh(new THREE.TorusGeometry(9.5, 0.45, 10, 24, Math.PI), matTitaniumFrame, segCount);
archInst.castShadow = true;
for (let i = 0; i < segCount; i++) {
    dummy.position.set(0, -1.8, i * 16.0 - 40.0);
    dummy.updateMatrix();
    archInst.setMatrixAt(i, dummy.matrix);
}
railMover.add(archInst);

const seqLedInst = new THREE.InstancedMesh(new THREE.SphereGeometry(0.35, 8, 8), new THREE.MeshBasicMaterial({ color: 0x38bdf8 }), 220 * 2);
for (let i = 0; i < 220; i++) {
    dummy.position.set(-6.5, -1.2, i * 16.0 - 40.0);
    dummy.updateMatrix();
    seqLedInst.setMatrixAt(i * 2, dummy.matrix);
    dummy.position.set(6.5, -1.2, i * 16.0 - 40.0);
    dummy.updateMatrix();
    seqLedInst.setMatrixAt(i * 2 + 1, dummy.matrix);
}
railMover.add(seqLedInst);

const mainGirder = new THREE.Mesh(new THREE.BoxGeometry(14.5, 2.4, 3600), matDarkAlloy);
mainGirder.position.set(0, -3.2, 1750);
mainGirder.receiveShadow = true;
railMover.add(mainGirder);

const groundEnvMover = new THREE.Group();
scene.add(groundEnvMover);

const oceanShaderMat = new THREE.ShaderMaterial({
    vertexShader: `
        varying vec2 vUv;
        varying vec3 vWorldPos;
        varying vec3 vNormal;
        uniform float uTime;

        vec3 gerstnerWaveXZ(vec4 wave, vec3 p, inout vec3 tangent, inout vec3 binormal) {
            float steepness = wave.z;
            float wavelength = wave.w;
            float k = 2.0 * 3.14159 / wavelength;
            float c = sqrt(9.8 / k);
            vec2 d = normalize(wave.xy);
            float f = k * (dot(d, p.xz) - c * uTime * 0.45);
            float a = steepness / k;

            tangent += vec3(-d.x * d.x * (steepness * sin(f)), d.x * (steepness * cos(f)), -d.x * d.y * (steepness * sin(f)));
            binormal += vec3(-d.x * d.y * (steepness * sin(f)), d.y * (steepness * cos(f)), -d.y * d.y * (steepness * sin(f)));
            return vec3(d.x * (a * cos(f)), a * sin(f), d.y * (a * cos(f)));
        }

        void main() {
            vUv = uv * 350.0;
            vec3 p = position;
            vec3 tangent = vec3(1.0, 0.0, 0.0);
            vec3 binormal = vec3(0.0, 0.0, 1.0);

            p += gerstnerWaveXZ(vec4(1.0, 0.3, 0.22, 90.0), position, tangent, binormal);
            p += gerstnerWaveXZ(vec4(0.4, 0.9, 0.14, 45.0), position, tangent, binormal);
            p += gerstnerWaveXZ(vec4(-0.6, 0.7, 0.09, 22.0), position, tangent, binormal);

            vNormal = normalize(cross(binormal, tangent));
            vec4 worldP = modelMatrix * vec4(p, 1.0);
            vWorldPos = worldP.xyz;
            gl_Position = projectionMatrix * viewMatrix * worldP;
        }
    `,
    fragmentShader: `
        varying vec2 vUv;
        varying vec3 vWorldPos;
        varying vec3 vNormal;
        uniform vec3 uSunDir;
        uniform vec3 uSunColor;
        uniform float uTime;

        void main() {
            vec3 viewDir = normalize(cameraPosition - vWorldPos);
            float micro = sin(vUv.x * 2.5 + uTime * 2.0) * cos(vUv.y * 2.5 - uTime * 1.5) * 0.08;
            vec3 n = normalize(vNormal + vec3(micro, 0.0, micro));

            float fresnel = pow(1.0 - max(0.0, dot(n, viewDir)), 4.0);
            vec3 deepWater = vec3(0.015, 0.045, 0.095);
            vec3 skyReflect = vec3(0.35, 0.65, 0.98);

            vec3 halfVec = normalize(uSunDir + viewDir);
            float spec = pow(max(0.0, dot(n, halfVec)), 160.0) * 4.5;
            vec3 col = mix(deepWater, skyReflect, fresnel) + uSunColor * spec;
            gl_FragColor = vec4(col, 0.96);
        }
    `,
    uniforms: {
        uTime: { value: 0.0 },
        uSunDir: { value: new THREE.Vector3().fromArray(cfg.env.sun_pos).normalize() },
        uSunColor: { value: new THREE.Color(cfg.env.sun_color) }
    },
    transparent: true
});

const seaMesh = new THREE.Mesh(new THREE.PlaneGeometry(160000, 160000, 96, 96), oceanShaderMat);
seaMesh.rotation.x = -Math.PI / 2;
seaMesh.position.y = -45.0;
seaMesh.receiveShadow = true;
groundEnvMover.add(seaMesh);

const islandBase = new THREE.Mesh(new THREE.BoxGeometry(220, 28, 3800), matConcreteWet);
islandBase.position.set(0, -32, 1750);
islandBase.receiveShadow = true;
groundEnvMover.add(islandBase);

const craneGeo = new THREE.BoxGeometry(4.0, 95.0, 4.0);
const craneMat = new THREE.MeshStandardMaterial({ color: 0xef4444, metalness: 0.85, roughness: 0.25 });
for (let cr = 0; cr < 8; cr++) {
    const s = (cr % 2 === 0) ? 1 : -1;
    const cz = cr * 380.0 + 100.0;
    const cTower = new THREE.Mesh(craneGeo, craneMat);
    cTower.position.set(s * 75.0, 25.0, cz);
    cTower.castShadow = true;
    groundEnvMover.add(cTower);

    const cArm = new THREE.Mesh(new THREE.BoxGeometry(32.0, 3.5, 4.0), craneMat);
    cArm.position.set(s * 62.0, 72.0, cz);
    groundEnvMover.add(cArm);

    const warningBeacon = new THREE.Mesh(new THREE.SphereGeometry(1.2, 8, 8), new THREE.MeshBasicMaterial({ color: 0xff0000 }));
    warningBeacon.position.set(s * 75.0, 74.0, cz);
    groundEnvMover.add(warningBeacon);
    strobeLeds.push(warningBeacon);
}

const beamGeo = new THREE.CylinderGeometry(0.5, 32.0, 750, 16, 1, true);
const beamMat = new THREE.MeshBasicMaterial({
    color: cfg.env.sun_color, transparent: true, opacity: 0.16, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false
});
for (let b = 0; b < 10; b++) {
    const s = (b % 2 === 0) ? 1 : -1;
    const z = b * 320.0 - 200.0;
    const beam = new THREE.Mesh(beamGeo, beamMat);
    beam.position.set(s * 85.0, 320.0, z);
    beam.rotation.z = s * 0.28;
    beam.rotation.x = 0.15;
    groundEnvMover.add(beam);
}

const delugeGeo = new THREE.SphereGeometry(18.0, 12, 12);
const delugeMat = new THREE.MeshBasicMaterial({ color: 0xdbeafe, transparent: true, opacity: 0.0, depthWrite: false });
const delugePuffs = [];
for (let p = 0; p < 16; p++) {
    const puff = new THREE.Mesh(delugeGeo, delugeMat);
    puff.position.set((Math.random() - 0.5) * 60, -2.0, (Math.random() - 0.5) * 80 - 20);
    groundEnvMover.add(puff);
    delugePuffs.push(puff);
}

const fujiMount = new THREE.Mesh(
    new THREE.ConeGeometry(12500, 3776, 64),
    new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.85 })
);
fujiMount.position.set(4500, 1800, 14500);
groundEnvMover.add(fujiMount);

const cloudGroup = new THREE.Group();
groundEnvMover.add(cloudGroup);
for (let c = 0; c < 50; c++) {
    const cloud = new THREE.Mesh(
        new THREE.PlaneGeometry(3500, 1800),
        new THREE.MeshBasicMaterial({ color: 0xcbd5e1, transparent: true, opacity: 0.22, side: THREE.DoubleSide, depthWrite: false })
    );
    cloud.rotation.x = Math.PI / 2;
    cloud.position.set((Math.random() - 0.2) * 22000, 900 + (c % 4) * 450, (Math.random() - 0.2) * 22000);
    cloudGroup.add(cloud);
}

// =========================================================================
// 6. 滑らかな補間ノイズによるフォトリアルFBM地球＆都市夜景
// =========================================================================
const earthGroup = new THREE.Group();
scene.add(earthGroup);

const earthShaderMat = new THREE.ShaderMaterial({
    vertexShader: `
        varying vec3 vNormal;
        varying vec3 vWorldPos;
        void main() {
            vNormal = normalize(normalMatrix * normal);
            vec4 wp = modelMatrix * vec4(position, 1.0);
            vWorldPos = wp.xyz;
            gl_Position = projectionMatrix * viewMatrix * wp;
        }
    `,
    fragmentShader: `
        varying vec3 vNormal;
        varying vec3 vWorldPos;
        uniform vec3 uSunDir;

        float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123); }

        float smoothNoise(vec2 p) {
            vec2 i = floor(p);
            vec2 f = fract(p);
            vec2 u = f * f * (3.0 - 2.0 * f);
            return mix(mix(hash(i + vec2(0.0,0.0)), hash(i + vec2(1.0,0.0)), u.x),
                       mix(hash(i + vec2(0.0,1.0)), hash(i + vec2(1.0,1.0)), u.x), u.y);
        }

        float fbm(vec2 p) {
            float v = 0.0; float a = 0.5;
            for (int i = 0; i < 5; i++) {
                v += a * smoothNoise(p);
                p *= 2.0; a *= 0.5;
            }
            return v;
        }

        void main() {
            vec3 norm = normalize(vNormal);
            vec3 viewDir = normalize(cameraPosition - vWorldPos);
            float light = dot(norm, uSunDir);

            vec2 sphereUv = vec2(atan(norm.z, norm.x) * 0.159 + 0.5, asin(norm.y) * 0.318 + 0.5);
            float land = smoothstep(0.48, 0.54, fbm(sphereUv * 8.0));

            vec3 oceanCol = vec3(0.012, 0.045, 0.12);
            vec3 landCol = vec3(0.07, 0.13, 0.08);
            vec3 dayCol = mix(oceanCol, landCol, land);

            float clouds = smoothstep(0.45, 0.75, fbm(sphereUv * 16.0 + vec2(0.1, 0.0)));
            dayCol = mix(dayCol, vec3(0.92, 0.95, 1.0), clouds * 0.65);

            float cityLights = pow(smoothNoise(sphereUv * 32.0), 3.0) * land * 14.0;
            vec3 nightCol = vec3(1.0, 0.75, 0.3) * cityLights;

            float dayFactor = smoothstep(-0.15, 0.25, light);
            vec3 baseCol = mix(nightCol, dayCol * max(0.08, light), dayFactor);

            float rim = pow(1.0 - max(0.0, dot(norm, viewDir)), 3.0);
            vec3 atmoCol = vec3(0.25, 0.65, 1.0) * rim * 1.8;

            gl_FragColor = vec4(baseCol + atmoCol, 1.0);
        }
    `,
    uniforms: {
        uSunDir: { value: new THREE.Vector3().fromArray(cfg.env.sun_pos).normalize() }
    }
});

const earthSphere = new THREE.Mesh(new THREE.SphereGeometry(25000, 64, 64), earthShaderMat);
earthGroup.add(earthSphere);

const stationMarker = new THREE.Mesh(new THREE.TorusGeometry(32.0, 4.0, 12, 32), matTitaniumFrame);
stationMarker.position.set(40.0, -120.0, -450.0);
scene.add(stationMarker);

const moonMesh = new THREE.Mesh(new THREE.SphereGeometry(6800, 32, 32), new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.85 }));
scene.add(moonMesh);

const marsFlyby = new THREE.Mesh(new THREE.SphereGeometry(450, 32, 32), new THREE.MeshStandardMaterial({ color: 0xc2410c, roughness: 0.8 }));
marsFlyby.position.set(550, 120, 0);
marsFlyby.scale.setScalar(0.0001);
scene.add(marsFlyby);

const jupiterFlyby = new THREE.Mesh(new THREE.SphereGeometry(1800, 32, 32), new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.65 }));
jupiterFlyby.position.set(-2200, 350, 0);
jupiterFlyby.scale.setScalar(0.0001);
scene.add(jupiterFlyby);

// =========================================================================
// 7. ワープ演出（12本二重らせんオーロラ＆ドップラー・スターストレッチ）
// =========================================================================
const warpGroup = new THREE.Group();
warpGroup.scale.setScalar(0.0001);
scene.add(warpGroup);

const ribbonCount = 12;
const ribbonTubes = [];
for (let r = 0; r < ribbonCount; r++) {
    const rPts = [];
    const baseOffset = (r / ribbonCount) * Math.PI * 2;
    for (let z = -280; z <= 280; z += 12) {
        const ang = (z * 0.04) + baseOffset;
        const radius = 18.0 + Math.sin(z * 0.02) * 5.0;
        rPts.push(new THREE.Vector3(Math.cos(ang) * radius, Math.sin(ang) * radius, z));
    }
    const curve = new THREE.CatmullRomCurve3(rPts);
    const tubeGeo = new THREE.TubeGeometry(curve, 64, 0.55, 8, false);
    const tubeMat = new THREE.MeshBasicMaterial({
        color: (r % 2 === 0) ? cfg.aurora_hex : 0x38bdf8,
        transparent: true, opacity: 0.88, blending: THREE.AdditiveBlending
    });
    const tubeMesh = new THREE.Mesh(tubeGeo, tubeMat);
    warpGroup.add(tubeMesh);
    ribbonTubes.push(tubeMesh);
}

const starCount = 3500;
const starGeo = new THREE.BufferGeometry();
const starPos = new Float32Array(starCount * 6);
const starCol = new Float32Array(starCount * 6);
for (let i = 0; i < starCount; i++) {
    const ang = Math.random() * Math.PI * 2;
    const rad = 25.0 + Math.random() * 220.0;
    const z = (Math.random() - 0.5) * 600.0;
    const x = Math.cos(ang) * rad, y = Math.sin(ang) * rad;
    starPos[i * 6] = x; starPos[i * 6 + 1] = y; starPos[i * 6 + 2] = z;
    starPos[i * 6 + 3] = x; starPos[i * 6 + 4] = y; starPos[i * 6 + 5] = z + 1.0;

    starCol[i * 6] = 0.35; starCol[i * 6 + 1] = 0.85; starCol[i * 6 + 2] = 1.0;
    starCol[i * 6 + 3] = 0.95; starCol[i * 6 + 4] = 0.15; starCol[i * 6 + 5] = 0.45;
}
starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
starGeo.setAttribute('color', new THREE.BufferAttribute(starCol, 3));
const starLines = new THREE.LineSegments(starGeo, new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.92, blending: THREE.AdditiveBlending }));
warpGroup.add(starLines);

// =========================================================================
// 8. 目的星・スターゲート＆進入誘導回廊＆ハニカムエネルギー減速膜
// =========================================================================
const destWorld = new THREE.Group();
destWorld.visible = true;
scene.add(destWorld);

function makeGasGiantTexture() {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 512;
    const ctx = c.getContext('2d');
    const colStr = (typeof cfg.dest_color === 'number') ? `#${cfg.dest_color.toString(16).padStart(6, '0')}` : cfg.dest_color;
    const bandStr = (typeof cfg.dest_band === 'number') ? `#${cfg.dest_band.toString(16).padStart(6, '0')}` : cfg.dest_band;
    for (let y = 0; y < 512; y++) {
        const n = Math.sin(y * 0.08) * 0.5 + 0.5;
        ctx.fillStyle = n > 0.5 ? colStr : bandStr;
        ctx.fillRect(0, y, 1024, 1);
    }
    return new THREE.CanvasTexture(c);
}

const destPlanetMat = new THREE.MeshStandardMaterial({ map: makeGasGiantTexture(), roughness: 0.65 });
const destPlanet = new THREE.Mesh(new THREE.SphereGeometry(3200, 64, 64), destPlanetMat);
destPlanet.position.set(700, -450, 5200);
destWorld.add(destPlanet);

const atmosphereMat = new THREE.ShaderMaterial({
    vertexShader: `
        varying vec3 vNormal;
        void main() {
            vNormal = normalize(normalMatrix * normal);
            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }
    `,
    fragmentShader: `
        varying vec3 vNormal;
        void main() {
            float intensity = pow(0.65 - dot(vNormal, vec3(0, 0, 1.0)), 2.5);
            gl_FragColor = vec4(0.38, 0.75, 0.98, 1.0) * intensity;
        }
    `,
    blending: THREE.AdditiveBlending,
    side: THREE.BackSide,
    transparent: true
});
const atmosphereGlow = new THREE.Mesh(new THREE.SphereGeometry(3350, 48, 48), atmosphereMat);
atmosphereGlow.position.copy(destPlanet.position);
destWorld.add(atmosphereGlow);

const stargateGroup = new THREE.Group();
destWorld.add(stargateGroup);
const gateOuter = new THREE.Mesh(new THREE.TorusGeometry(65, 4.8, 20, 64), matTitaniumFrame);
gateOuter.castShadow = true;
stargateGroup.add(gateOuter);

const gateFieldMesh = new THREE.Mesh(
    new THREE.CircleGeometry(64.0, 32),
    new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.5, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false })
);
stargateGroup.add(gateFieldMesh);

const corridorGeo = new THREE.SphereGeometry(1.5, 8, 8);
const corridorMat = new THREE.MeshBasicMaterial({ color: 0xef4444 });
const corridorInst = new THREE.InstancedMesh(corridorGeo, corridorMat, 40);
for (let b = 0; b < 20; b++) {
    const bz = -b * 250.0 - 150.0;
    dummy.position.set(-45.0, 0, bz);
    dummy.updateMatrix();
    corridorInst.setMatrixAt(b * 2, dummy.matrix);
    dummy.position.set(45.0, 0, bz);
    dummy.updateMatrix();
    corridorInst.setMatrixAt(b * 2 + 1, dummy.matrix);
}
stargateGroup.add(corridorInst);

destWorld.position.set(0, 0, 800000.0);
destWorld.scale.setScalar(0.0001);

const tetherLines = [];
const tetherMat = new THREE.LineBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending, linewidth: 2 });
for (let k = 0; k < 6; k++) {
    const tGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, 0, 0)]);
    const tLine = new THREE.Line(tGeo, tetherMat);
    destWorld.add(tLine);
    tetherLines.push(tLine);
}

renderer.compile(scene, cameraMain);
renderer.compile(scene, cameraPip);

// =========================================================================
// 9. 2段スタッガー式・広角軌道レーダーマップ
// =========================================================================
function drawRadar(prog, vc, mach, altKm) {
    const rw = radarCanvas.width;
    const rh = radarCanvas.height;
    rCtx.clearRect(0, 0, rw, rh);

    const isSolar = (prog >= 0.12);
    radarLabelEl.innerHTML = isSolar
        ? `TACTICAL RADAR<br><span style="color:#10b981;font-size:8px;">INTERPLANETARY SCALE</span>`
        : `TACTICAL RADAR<br><span style="color:#38bdf8;font-size:8px;">LUNAR ESCAPE SCALE</span>`;

    const leftX = 75, rightX = rw - 85;
    const midY = rh / 2;

    rCtx.strokeStyle = 'rgba(56,189,248,0.3)';
    rCtx.lineWidth = 3;
    rCtx.beginPath();
    rCtx.moveTo(leftX, midY); rCtx.lineTo(rightX, midY);
    rCtx.stroke();

    rCtx.textAlign = "center";
    if (!isSolar) {
        const markers = [
            { x: leftX, lbl: "EARTH", sub: "0 km" },
            { x: leftX + (rightX - leftX) * 0.38, lbl: "LEO / GEO", sub: "36,000 km" },
            { x: rightX, lbl: "MOON", sub: "384,400 km" }
        ];
        markers.forEach(m => {
            rCtx.fillStyle = '#38bdf8';
            rCtx.beginPath(); rCtx.arc(m.x, midY, 4, 0, Math.PI * 2); rCtx.fill();
            rCtx.font = 'bold 10px monospace';
            rCtx.fillStyle = '#f8fafc';
            rCtx.fillText(m.lbl, m.x, midY - 14);
            rCtx.font = '8.5px monospace';
            rCtx.fillStyle = '#94a3b8';
            rCtx.fillText(m.sub, m.x, midY + 18);
        });

        const shipNorm = Math.min(1.0, altKm / 384400.0);
        const curX = leftX + shipNorm * (rightX - leftX);
        rCtx.fillStyle = '#f43f5e';
        rCtx.beginPath(); rCtx.arc(curX, midY, 6, 0, Math.PI * 2); rCtx.fill();
        rCtx.strokeStyle = '#ffffff'; rCtx.lineWidth = 2; rCtx.stroke();

        rCtx.font = 'bold 9px monospace';
        rCtx.fillStyle = '#f43f5e';
        rCtx.fillText(`VESSEL (M ${mach.toFixed(1)})`, curX, midY - 26);
    } else {
        const solarMarkers = [
            { pos: 0.12, lbl: "EARTH", sub: "1.0 AU" },
            { pos: 0.38, lbl: "MARS", sub: "1.5 AU" },
            { pos: 0.68, lbl: "JUPITER", sub: "5.2 AU" },
            { pos: 0.98, lbl: "SATURN GATE", sub: "9.5 AU" }
        ];
        solarMarkers.forEach((sm) => {
            const sx = leftX + ((sm.pos - 0.12) / 0.86) * (rightX - leftX);
            rCtx.fillStyle = '#94a3b8';
            rCtx.beginPath(); rCtx.arc(sx, midY, 4, 0, Math.PI * 2); rCtx.fill();
            rCtx.font = 'bold 10px monospace';
            rCtx.fillStyle = '#f8fafc';
            rCtx.fillText(sm.lbl, sx, midY - 14);
            rCtx.font = '8.5px monospace';
            rCtx.fillStyle = '#94a3b8';
            rCtx.fillText(sm.sub, sx, midY + 18);
        });

        const curX = leftX + ((prog - 0.12) / 0.86) * (rightX - leftX);
        rCtx.fillStyle = '#10b981';
        rCtx.beginPath(); rCtx.arc(curX, midY, 7, 0, Math.PI * 2); rCtx.fill();
        rCtx.strokeStyle = '#ffffff'; rCtx.lineWidth = 2; rCtx.stroke();

        rCtx.font = 'bold 9px monospace';
        rCtx.fillStyle = '#10b981';
        rCtx.fillText(`NOW: ${vc.toFixed(3)} c`, curX, midY - 26);
    }
}

// =========================================================================
// 10. 60fps アニメーションループ（ド迫力チェイス・天体機体100%捕捉CAM02）
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
    const tempK = L('temp_k');
    const gLoad = L('g');

    if (f0.phase !== lastAnnouncedPhase) {
        lastAnnouncedPhase = f0.phase;
        if (f0.phase === "CATAPULT_RAIL_ACCEL") speakCallout("Magnetic catapult engaged. Maximum acceleration.");
        else if (f0.phase === "EXOSPHERE_INSERTION") speakCallout("Leaving atmosphere. Orbital velocity achieved.");
        else if (f0.phase === "WARP_FIELD_COMPRESSION") speakCallout("Alcubierre drive spooling up. Warp field compression.");
        else if (f0.phase === "ALCUBIERRE_HYPER_WARP") speakCallout("Hyper warp engaged. Approaching light speed.");
        else if (f0.phase === "DEBRIS_RETRO_BRAKING") speakCallout("Flip and burn initiated. Laser defense online.");
        else if (f0.phase === "STARGATE_DOCKING_LOCKED") speakCallout("Stargate tether captured. Docking locked.");
    }

    const slowShake = Math.sin(now * 0.003) * Math.cos(now * 0.002) * 1.8;
    const fastShake = (Math.sin(now * 0.055) + Math.cos(now * 0.085)) * vib * 0.8;

    // ★修正: 加速時に機体がグンと前へ飛び出すラバーバンド・スプリングカメラ
    const engPwr = L('engine_power');
    const gLag = Math.min(26.0, gLoad * 1.6 + engPwr * 8.0);

    let effectiveCam = activeCamMode;
    if (activeCamMode === 0) {
        // ★修正: 映画的カット割り（上昇中・ワープ中も大迫力チェイスを維持）
        if (f0.phase.includes("STANDBY") || f0.phase.includes("CHARGE")) effectiveCam = 1;
        else if (f0.phase === "CATAPULT_RAIL_ACCEL") effectiveCam = (simTime < 1.6) ? 4 : 1;
        else if (f0.phase.includes("CLIMB") || f0.phase.includes("INSERTION")) effectiveCam = 1;
        else if (f0.phase === "WARP_FIELD_COMPRESSION") effectiveCam = 3;
        else if (f0.phase === "ALCUBIERRE_HYPER_WARP") effectiveCam = 1;
        else if (f0.phase === "DEBRIS_RETRO_BRAKING") effectiveCam = 4;
        else effectiveCam = 1;
    }

    const shipWorldPos = new THREE.Vector3();
    shipMeshGroup.getWorldPosition(shipWorldPos);

    if (effectiveCam === 1) { // メインチェイス（機体とバーナー炎が完璧に画面中央）
        const dynTargetZ = THREE.MathUtils.lerp(-2.0, -8.0, engPwr);
        cameraMain.position.x = baseCamPos.x + slowShake * 0.35;
        cameraMain.position.y = baseCamPos.y + slowShake * 0.25;
        cameraMain.position.z = baseCamPos.z - gLag + fastShake;
        cameraMain.lookAt(0.0, baseTarget.y, dynTargetZ);
    } else if (effectiveCam === 2) { // コックピット視点
        cameraMain.position.set(shipWorldPos.x, shipWorldPos.y + 1.25, shipWorldPos.z + 8.2);
        cameraMain.lookAt(shipWorldPos.x, shipWorldPos.y + 1.25, shipWorldPos.z + 140.0);
    } else if (effectiveCam === 3) { // 翼端マウント至近観察
        cameraMain.position.set(shipWorldPos.x - (halfSpan + 2.5), shipWorldPos.y + 1.2, shipWorldPos.z - 4.5);
        cameraMain.lookAt(shipWorldPos.x, shipWorldPos.y + 0.5, shipWorldPos.z);
    } else if (effectiveCam === 4) { // フライバイ定点追跡
        cameraMain.position.set(38.0, 18.0, 140.0 - (f0.phase === "DEBRIS_RETRO_BRAKING" ? 0 : distM * 0.02));
        cameraMain.lookAt(shipWorldPos);
    }

    railMover.position.set(0, 0, -distM);
    const groundY = -distM * Math.sin(radAngle);
    const groundZ = -distM * Math.cos(radAngle);
    groundEnvMover.position.set(0, groundY, groundZ);

    const isRailRunning = (altKm < 1.2 && f0.phase === "CATAPULT_RAIL_ACCEL");
    if (isRailRunning) {
        shipPitchGroup.rotation.set(0, 0, 0);
        shipMeshGroup.position.set(0, 0, 0);
    } else {
        const freePitch = -THREE.MathUtils.degToRad(pitchDeg) + radAngle;
        shipPitchGroup.rotation.set(freePitch, THREE.MathUtils.degToRad(yawDeg), 0);
        shipMeshGroup.position.set(
            Math.sin(now * 0.045) * vib * 0.35,
            Math.cos(now * 0.055) * vib * 0.35,
            Math.sin(now * 0.035) * vib * 0.35
        );
    }

    // ★魔改造: 推力偏向ノズルの首振り連動
    nozzleGimbalRoot.rotation.x = THREE.MathUtils.degToRad(pitchDeg > 5 ? -6.0 : 0.0);
    nozzleGimbalRoot.rotation.y = THREE.MathUtils.degToRad(Math.sin(now * 0.05) * 4.0 * (rcsBurst > 0.1 ? 2.0 : 0.5));

    cameraMain.fov = 46.0 + vc * 24.0 + (mach > 5 ? 4.0 : 0.0);
    cameraMain.updateProjectionMatrix();

    oceanShaderMat.uniforms.uTime.value = elapsed;
    flameShaderMat.uniforms.uTime.value = elapsed;
    vaporShaderMat.uniforms.uTime.value = elapsed;
    warpGridMat.uniforms.uTime.value = elapsed;
    warpGridMat.uniforms.uAlpha.value = THREE.MathUtils.lerp(0.0, 0.85, L('warp_charge'));

    // ★魔改造: 近景スペースダストの超高速スクロール
    const speedRatio = THREE.MathUtils.clamp((mach / 40.0) + (vc * 8.0), 0.08, 12.0);
    const dArr = dustGeo.attributes.position.array;
    for (let i = 0; i < dustCount; i++) {
        let z = dArr[i * 6 + 2] - speedRatio * 3.5;
        if (z < -110.0) z = 110.0;
        dArr[i * 6 + 2] = z;
        dArr[i * 6 + 5] = z - (2.5 + speedRatio * 4.5);
    }
    dustGeo.attributes.position.needsUpdate = true;

    // ★魔改造: 連続通過する3Dホログラム空間誘導ゲートの高速前進
    for (let wr = 0; wr < waypointRingCount; wr++) {
        const ring = waypointRings[wr];
        let rz = ring.position.z - speedRatio * 4.2;
        if (rz < -80.0) rz += waypointRingCount * 75.0;
        ring.position.z = rz;
        ring.material.opacity = (f0.phase.includes("WARP") || altKm > 50.0) ? 0.5 : 0.0;
    }

    const fogFade = THREE.MathUtils.clamp(1.0 - (altKm / 45.0), 0.0, 1.0);
    scene.fog.density = cfg.env.fog_density * fogFade;

    if (simTime < 3.0 && cfg.cryo_steam) {
        const dAlpha = (simTime > -1.8 && simTime < 1.5) ? 0.45 : (simTime < -1.8 ? 0.15 : 0.0);
        delugeMat.opacity = dAlpha;
        delugePuffs.forEach((puff, i) => {
            puff.scale.setScalar(1.0 + (simTime + 5.0) * 0.8 + Math.sin(elapsed * 2.0 + i) * 0.2);
            puff.position.y = -2.0 + (simTime + 5.0) * 1.2;
        });
    } else {
        delugeMat.opacity = 0.0;
    }

    if (mach >= 1.0 && mach <= 2.2) {
        const boomF = 1.0 - Math.abs(mach - 1.5) / 0.7;
        sonicBoomDiscMat.opacity = boomF * 0.85;
        sonicBoomDisc.scale.setScalar(1.0 + boomF * 3.2);
        sonicBoomDisc.position.z = -boomF * 12.0;
        if (!hasTriggeredBoom) {
            hasTriggeredBoom = true;
            playSonicBoomSound();
        }
    } else {
        sonicBoomDiscMat.opacity = 0.0;
    }

    const vAlpha = L('vapor_alpha');
    vaporShaderMat.uniforms.uAlpha.value = vAlpha * 0.75;
    wingtipVortices.forEach(v => { v.mat.opacity = vAlpha * 0.85; });

    const pAlpha = L('plasma_alpha');
    plasmaBowMat.opacity = pAlpha * 0.85;
    leadingEdgeMat.opacity = pAlpha * 0.95;
    sparkMat.opacity = pAlpha > 0.1 ? 0.85 : 0.0;

    if (tempK > 700.0) {
        const glowProg = Math.min(1.0, (tempK - 700.0) / 1200.0);
        const glowColor = new THREE.Color().lerpColors(new THREE.Color(0xd97706), new THREE.Color(0xf8fafc), glowProg * 0.7);
        matBellyTile.emissive.copy(glowColor);
        matBellyTile.emissiveIntensity = glowProg * 1.8;
        matHull.emissive.copy(glowColor);
        matHull.emissiveIntensity = glowProg * 0.8;
    } else {
        matBellyTile.emissiveIntensity = 0.0;
        matHull.emissiveIntensity = 0.0;
    }

    const sArc = L('spark_arc');
    if (sArc > 0.05 && f0.phase === "CATAPULT_RAIL_ACCEL") {
        arcLineMat.opacity = 0.95;
        arcLight.intensity = 3.5 + Math.random() * 4.0;
        const arcPos = arcLine.geometry.attributes.position;
        const jX = (Math.random() - 0.5) * 1.4, jY = (Math.random() - 0.5) * 1.4;
        arcPos.setXYZ(0, -3.8 + jX, -1.2 + jY, -distM + 2.0);
        arcPos.setXYZ(1, 3.8 - jX, -1.2 - jY, -distM - 4.0);
        arcPos.needsUpdate = true;
        arcLight.position.set(0, -1.0, -distM);
    } else {
        arcLineMat.opacity = 0.0;
        arcLight.intensity = 0.0;
    }

    warpPass.uniforms.uDistort.value = L('warp_boom') * 2.8 + L('warp_active') * 0.35;
    warpPass.uniforms.uTime.value = elapsed;
    warpPass.uniforms.uDroplets.value = (altKm < 8.0 && simTime > 0.0) ? 1.0 - (altKm / 8.0) : 0.0;
    warpPass.uniforms.uGForce.value = gLoad;

    const flashState = (Math.floor(now * 0.004) % 2 === 0);
    strobeLeds.forEach(led => { led.visible = flashState; });

    if (altKm < 110.0 && f0.phase !== "WARP_FIELD_COMPRESSION" && f0.phase !== "ALCUBIERRE_HYPER_WARP") {
        catapultSlopeRoot.visible = true;
        groundEnvMover.visible = true;
    } else {
        catapultSlopeRoot.visible = false;
        groundEnvMover.visible = false;
    }

    spaceFieldGroup.rotation.y = elapsed * 0.002;
    if (prog < 0.28) {
        earthGroup.visible = true;
        const warpRecede = Math.pow(Math.max(0, prog - 0.05) * 18.0, 3.0);
        earthGroup.position.set(0, -25050 - altKm * 120.0 - warpRecede * 35000.0, -4000 - distM * 0.6 - warpRecede * 95000.0);
        earthGroup.scale.setScalar(Math.max(0.001, 1.0 / (1.0 + warpRecede * 1.8)));

        moonMesh.visible = (altKm > 100.0);
        moonMesh.position.set(8000, 3500, -12000 - (prog / 0.12) * 80000.0);
        stationMarker.visible = (altKm > 80.0 && prog < 0.05);
        stationMarker.position.z = -150.0 - (altKm - 80.0) * 85.0;
    } else {
        earthGroup.visible = false;
        moonMesh.visible = false;
        stationMarker.visible = false;
    }

    if (prog >= 0.30 && prog <= 0.48) {
        marsFlyby.scale.setScalar(1.0);
        marsFlyby.position.z = 250.0 - ((prog - 0.30) / 0.18) * 600.0;
    } else {
        marsFlyby.scale.setScalar(0.0001);
    }
    if (prog >= 0.60 && prog <= 0.78) {
        jupiterFlyby.scale.setScalar(1.0);
        jupiterFlyby.position.z = 450.0 - ((prog - 0.60) / 0.18) * 1100.0;
    } else {
        jupiterFlyby.scale.setScalar(0.0001);
    }

    const sabotP = L('sabot_purge');
    if (sabotP > 0.01) {
        sabotClamps.forEach(sc => {
            sc.mesh.position.x = sc.baseX + sc.side * Math.pow(sabotP, 2.0) * 14.0;
            sc.mesh.position.y = -1.4 - Math.pow(sabotP, 2.0) * 8.0;
            sc.mesh.position.z = -1.0 - Math.pow(sabotP, 1.5) * 45.0;
            sc.mesh.rotation.set(sabotP * 8.0, sabotP * 6.0 * sc.side, 0);
        });
    }

    const fairingP = L('fairing_purge');
    if (fairingP > 0.01) {
        fairingPanels.forEach(fp => {
            const spread = Math.pow(fairingP, 2.0) * 35.0;
            fp.mesh.position.x = fp.baseX + Math.cos(fp.ang) * spread;
            fp.mesh.position.y = fp.baseY + Math.sin(fp.ang) * spread;
            fp.mesh.position.z = 1.0 - Math.pow(fairingP, 1.5) * 55.0;
            fp.mesh.rotation.x = fairingP * 6.0;
            fp.mesh.rotation.y = fairingP * 8.0;
        });
    }

    const bayVal = L('bay_open');
    wingPivots.forEach(wp => { wp.group.rotation.y = wp.side * L('wing_sweep') * 0.32; });
    bayDoors.forEach(bd => { bd.pivot.rotation.z = bd.side * bayVal * 1.35; });
    hydraulicPistons.forEach(hp => {
        hp.rod.position.y = 0.6 + bayVal * 0.45;
        hp.cyl.rotation.z = hp.side * (0.5 + bayVal * 0.35);
    });
    radiatorPanels.forEach(rp => { rp.pivot.rotation.z = rp.side * (1.0 - L('rad_deploy')) * 1.45; });

    controlSurfaces.forEach(cs => {
        if (cs.type === 'elevon') cs.mesh.rotation.x = Math.sin(now * 0.005) * 0.15 + (pitchDeg > 10 ? -0.25 : 0.05);
        if (cs.type === 'rudder') cs.mesh.rotation.y = Math.cos(now * 0.004) * 0.2;
    });

    const nozVal = L('nozzle_open');
    irisPaddles.forEach(ip => { ip.rotation.x = -0.35 + nozVal * 0.48; });
    sealPaddles.forEach(sp => { sp.rotation.x = -0.35 + nozVal * 0.48; });
    nozzlePistonLinks.forEach(nl => { nl.scale.set(1.0, 1.0, 0.6 + nozVal * 0.8); });

    const rcsBurst = L('rcs_burst');
    rcsJets.forEach(rj => { rj.mat.opacity = rcsBurst * 0.85; });

    const wCharge = L('warp_charge');
    warpRingAssembly.position.y = -0.8 + L('ring_lift') * 4.2;

    rotorClockwise.rotation.z += 0.04 + wCharge * 0.45;
    rotorCounter.rotation.z -= 0.05 + wCharge * 0.55;

    ringSegments.forEach(seg => {
        const slideDist = seg.baseR + wCharge * 1.4;
        seg.block.position.y = slideDist;
        seg.coilCore.position.y = slideDist;
        seg.coilCore.material.color.setHex(wCharge > 0.6 ? 0xffffff : cfg.aurora_hex);
    });

    rippleGeos.forEach((rip, rIdx) => {
        if (wCharge > 0.2) {
            rip.material.opacity = (wCharge * 0.8) * (1.0 - (elapsed * 2.0 + rIdx * 0.33) % 1.0);
            rip.scale.setScalar(1.0 + ((elapsed * 2.5 + rIdx * 0.33) % 1.0) * 1.8);
            rip.position.z = -(((elapsed * 18.0 + rIdx * 6.0) % 24.0));
        } else {
            rip.material.opacity = 0.0;
        }
    });

    gravLensMat.uniforms.uAlpha.value = L('warp_lens');
    accretionRing.material.opacity = L('warp_lens') * 0.95;
    accretionRing.rotation.z += 0.08;

    if (f0.phase === "DEBRIS_RETRO_BRAKING") {
        const fireState = (Math.sin(now * 0.06) > 0.3);
        laserBeams.forEach(lb => { lb.material.opacity = fireState ? 0.95 : 0.0; });
        debrisTargetGroup.visible = true;
        targetBoxMesh.rotation.z += 0.05;
        targetBoxMesh.material.color.setHex(fireState ? 0x10b981 : 0xf43f5e);
    } else {
        laserBeams.forEach(lb => { lb.material.opacity = 0.0; });
        debrisTargetGroup.visible = false;
    }

    plumeRoot.visible = engPwr > 0.02;
    if (plumeRoot.visible) {
        const pulse = 0.95 + Math.sin(now * 0.08) * 0.05;
        const atmoVacuumExpansion = THREE.MathUtils.clamp(altKm / 80.0, 0.0, 1.0);
        const plumeExpansion = THREE.MathUtils.lerp(1.0, 3.8, atmoVacuumExpansion);
        plumeRoot.scale.set(pulse * plumeExpansion, pulse * plumeExpansion, engPwr * (1.0 + vc * 1.5) * pulse);
        plumeLight.intensity = engPwr * 4.5;
        flareTexMat.opacity = engPwr * 0.85;
        shockBarrels.forEach((sb, idx) => {
            const bPulse = 1.0 + Math.sin(now * 0.12 + idx * 0.8) * 0.12;
            sb.scale.set(bPulse, bPulse, 2.2 * bPulse);
            sb.material.opacity = Math.max(0.1, 0.9 - atmoVacuumExpansion * 0.7);
        });

        // パルス渦輪の連続射出アニメーション
        pulseRings.forEach((pr, pIdx) => {
            const pProg = (elapsed * 3.5 + pIdx * 0.16) % 1.0;
            pr.position.z = -pProg * 38.0;
            pr.scale.setScalar(1.0 + pProg * 2.8);
            pr.material.opacity = (1.0 - pProg) * engPwr * 0.75;
        });
    } else {
        plumeLight.intensity = 0.0;
        flareTexMat.opacity = 0.0;
        pulseRings.forEach(pr => { pr.material.opacity = 0.0; });
    }

    const wAct = L('warp_active');
    warpGroup.scale.setScalar(wAct > 0.05 ? 1.0 : 0.0001);
    if (wAct > 0.05) {
        warpGroup.rotation.z += 0.035;
        ribbonTubes.forEach((tMesh, i) => {
            tMesh.material.opacity = (0.75 + Math.sin(elapsed * 4.0 + i) * 0.2) * wAct;
        });

        const sArr = starGeo.attributes.position.array;
        const stretchLen = 35.0 + vc * 180.0;
        for (let i = 0; i < starCount; i++) {
            let z = sArr[i * 6 + 2] - (18.0 + vc * 45.0);
            if (z < -300.0) z = 300.0;
            sArr[i * 6 + 2] = z;
            sArr[i * 6 + 5] = z + stretchLen;
        }
        starGeo.attributes.position.needsUpdate = true;
    }

    if (prog > 0.20) {
        const approachProg = THREE.MathUtils.clamp((prog - 0.20) / 0.80, 0.0, 1.0);
        const curDist = THREE.MathUtils.lerp(650000.0, 12.0, Math.pow(approachProg, 2.5));
        const curScale = THREE.MathUtils.lerp(0.002, 1.0, Math.pow(approachProg, 2.0));
        destWorld.position.set(0, 0, curDist);
        destWorld.scale.setScalar(curScale);
        gateFieldMesh.material.opacity = 0.35 + Math.sin(now * 0.008) * 0.25;
    } else {
        destWorld.position.set(0, 0, 800000.0);
        destWorld.scale.setScalar(0.0001);
    }

    const tLock = L('tether_lock');
    tetherMat.opacity = tLock * 0.85;
    if (tLock > 0.01) {
        for (let k = 0; k < 6; k++) {
            const ang = (k / 6) * Math.PI * 2;
            const gateP = new THREE.Vector3(Math.cos(ang) * 65.0, Math.sin(ang) * 65.0, 0);
            const shipAttach = new THREE.Vector3((k % 2 === 0 ? 3 : -3), 0, -5.0).applyMatrix4(shipMeshGroup.matrixWorld);
            const localShipP = destWorld.worldToLocal(shipAttach.clone());
            const posAttr = tetherLines[k].geometry.attributes.position;
            posAttr.setXYZ(0, gateP.x, gateP.y, gateP.z);
            posAttr.setXYZ(1, localShipP.x, localShipP.y, localShipP.z);
            posAttr.needsUpdate = true;
        }
    }

    let duckingFactor = 1.0;
    if (f0.phase === "WARP_FIELD_COMPRESSION" && prog > 0.09) {
        duckingFactor = Math.max(0.001, 1.0 - (prog - 0.09) / 0.03);
    }

    if (actx) {
        const inAtmo = (altKm < 95.0);
        rocketFilter.frequency.setTargetAtTime(inAtmo ? 340 : 55, actx.currentTime, 0.1);
        rocketGain.gain.setTargetAtTime(engPwr * (inAtmo ? 0.42 : 0.12) * duckingFactor, actx.currentTime, 0.08);
        rcsGain.gain.setTargetAtTime(rcsBurst * 0.18 * duckingFactor, actx.currentTime, 0.04);
        coilGain.gain.setTargetAtTime((f0.phase.includes("COIL") || f0.phase.includes("RAIL") ? 0.22 : 0.0001) * duckingFactor, actx.currentTime, 0.08);
        warpGain.gain.setTargetAtTime((wAct * 0.38 + L('warp_lens') * 0.25) * duckingFactor, actx.currentTime, 0.1);
        warpOsc.frequency.setTargetAtTime(60 + vc * 380, actx.currentTime, 0.1);
    }

    // =========================================================================
    // ★修正: CAM 02（天体と機体が100%同軸に並ぶツーショット望遠フレーミング）
    // =========================================================================
    const recessionKms = vc > 0.01 ? (vc * 299792).toFixed(0) : (mach * 0.34).toFixed(1);

    if (f0.phase.includes("STANDBY") || f0.phase.includes("CHARGE")) {
        pipTitleEl.innerText = "CAM 02: LAUNCH RAIL FLY-BY TRACKER";
        pipMetricEl.innerText = `RECESSION: 0 km/s | MACH: ${mach.toFixed(1)} | PAD LOCK`;
        cameraPip.position.set(28.0, 4.0, -14.0);
        cameraPip.lookAt(0, 1.0, 0);
    } else if (f0.phase === "CATAPULT_RAIL_ACCEL") {
        pipTitleEl.innerText = "CAM 02: CATAPULT SUPERSONIC FLY-BY";
        pipMetricEl.innerText = `RECESSION: ${recessionKms} km/s | MACH: ${mach.toFixed(1)} | RAIL EXIT`;
        cameraPip.position.set(22.0, 3.0, 35.0 - distM * 0.04);
        cameraPip.lookAt(0, 0, 0);
    } else if (f0.phase.includes("CLIMB") || f0.phase.includes("INSERTION")) {
        pipTitleEl.innerText = "CAM 02: ONBOARD WING-MOUNT & EARTH DEPARTURE";
        pipMetricEl.innerText = `EARTH RECESSION: ${recessionKms} km/s | ALT: ${altKm.toFixed(0)} km`;
        // 機体の斜め前方から機首と背後の巨大な地球を一直線に捉える構図
        cameraPip.position.set(8.5, 3.2, 18.0);
        cameraPip.lookAt(0, 0, -2000.0);
    } else if (f0.phase.includes("WARP")) {
        if (prog >= 0.30 && prog <= 0.48) {
            pipTitleEl.innerText = "CAM 02: MARS FLY-BY OPTICAL INTERCEPT";
            pipMetricEl.innerText = `VEL: ${vc.toFixed(3)} c | INTERCEPT TARGET: MARS`;
            // 火星 ➔ 宇宙船 ➔ カメラを一直線上に配置（自機越しに火星を捉える）
            cameraPip.position.set(-16.0, 5.0, -22.0);
            cameraPip.lookAt(marsFlyby.position.x * 0.1, marsFlyby.position.y * 0.1, marsFlyby.position.z * 0.5);
        } else if (prog >= 0.60 && prog <= 0.78) {
            pipTitleEl.innerText = "CAM 02: JUPITER GRAVITY PASS";
            pipMetricEl.innerText = `VEL: ${vc.toFixed(3)} c | INTERCEPT: GREAT RED SPOT`;
            cameraPip.position.set(18.0, 6.0, -22.0);
            cameraPip.lookAt(jupiterFlyby.position.x * 0.1, jupiterFlyby.position.y * 0.1, jupiterFlyby.position.z * 0.5);
        } else {
            pipTitleEl.innerText = "CAM 02: ALCUBIERRE WARP FIELD BOW SHOCK";
            pipMetricEl.innerText = `WARP: ${vc.toFixed(3)} c (${recessionKms} km/s) | LORENTZ: ${(1.0/Math.sqrt(Math.max(0.001,1.0-vc*vc))).toFixed(2)}x`;
            // 斜め前方からワープボウショックと激突する機首をクローズアップ
            cameraPip.position.set(-8.5, 3.5, 22.0);
            cameraPip.lookAt(0, 0, -5.0);
        }
    } else {
        pipTitleEl.innerText = "CAM 02: STARGATE APPROACH & ARREST LOCK";
        pipMetricEl.innerText = `APPROACH: ${recessionKms} km/s | TETHER CAPTURE READY`;
        // 機体の後方からスターゲートへ飛び込んでいく様子を一望
        cameraPip.position.set(0.0, 6.5, -28.0);
        cameraPip.lookAt(0, 0, 150.0);
    }

    drawRadar(prog, vc, mach, altKm);

    renderer.autoClear = true;
    renderer.setRenderTarget(null);
    renderer.setViewport(0, 0, W, H);
    renderer.setScissor(0, 0, W, H);
    renderer.setScissorTest(false);
    composerMain.render();

    if (pipOpen) {
        const rect = pipBox.getBoundingClientRect();
        renderer.setViewport(rect.left, H - rect.bottom, rect.width, rect.height);
        renderer.setScissor(rect.left, H - rect.bottom, rect.width, rect.height);
        renderer.setScissorTest(true);
        renderer.autoClear = false;
        renderer.clearDepth();
        renderer.render(scene, cameraPip);
    }

    document.getElementById('ui-phase').innerText = f0.phase;
    document.getElementById('ui-alt').innerText = altKm > 90000 ? "DEEP SPACE" : `${altKm.toFixed(1)} km`;
    document.getElementById('ui-spd').innerText = vc > 0.02 ? `${vc.toFixed(3)} c` : `M ${mach.toFixed(1)}`;
    const sTime = L('t');
    document.getElementById('ui-clock').innerText = sTime < 0 ? `T${sTime.toFixed(1)}s` : `T+${L('ship_time').toFixed(1)}s`;
    document.getElementById('ui-vc').innerText = vc.toFixed(3);
    document.getElementById('ui-temp').innerText = Math.round(L('temp_k'));
    document.getElementById('ui-g').innerText = gLoad.toFixed(1);
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
