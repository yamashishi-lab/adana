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
    "※ 完全映画仕様ディレクターズカット：PMREM IBL / 実写NASAテクスチャ地球＆宇宙 / 全天球リアル星空 / "
    "滑らか航空力学的アプローチ / 巨大コロニー＆無限滑走路 / 物理ベースシャドウ＆大気膨張プルーム"
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
        "metalness": 0.85,
        "roughness": 0.28,
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
        "color_hex": 0x3a3227,
        "band_hex": 0x241e17,
    },
    "木星 大赤斑上空・軌道エレベーターアンカー『ゼウス』": {
        "dist_label": "4.20 AU (628,000,000 km)",
        "type": "jupiter",
        "color_hex": 0x382110,
        "band_hex": 0x221309,
    },
    "火星 オリンポス軌道テラフォーミング・リング": {
        "dist_label": "0.52 AU (78,000,000 km)",
        "type": "mars",
        "color_hex": 0x3b1c10,
        "band_hex": 0x231008,
    },
}

LAUNCH_ENVIRONMENTS = {
    "相模湾 第1メガフロート射場 (深夜・大気光霧＆サーチライト照射)": {
        "mode": "night",
        "angle_deg": 12.0,
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
        "angle_deg": 12.0,
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
        hull_color = st.color_picker("メイン装甲ベースカラー", "#111827")
        belly_color = st.color_picker("下部耐熱カーボンタイル配色", "#030712")
    with c2:
        st.info(f"**構造設計:** {vessel_cfg['desc']}")
        wings_span = st.slider("可変ジオメトリ主翼スパン (m)", 18.0, 42.0, 30.0, step=1.0)
        radiator_fins = st.slider("展開式 高温放熱ラジエーターパネル数", 2, 8, 4, step=2)
        aux_boosters = st.checkbox(
            "外装スクラムジェット補助ブースター×2 (高度55kmで分離パージ)", value=False
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
# 💥 タイムライン物理データ
# =========================================================================
def build_timeline(preview_only=False):
    base_pitch = float(env_cfg["angle_deg"])
    if preview_only:
        return [{
            "t": -5.0, "phase": "PAD_STANDBY", "dist_m": 0.0, "alt_km": 0.04,
            "mach": 0.0, "vc": 0.0, "g": 1.0, "temp_k": 288.0,
            "clamp_open": 0.0, "sabot_purge": 0.0, "fairing_purge": 0.0,
            "gear_deploy": 0.0, "speedbrake": 0.0, "chute_deploy": 0.0, "runway_speed": 0.0, "touchdown_smoke": 0.0,
            "wing_sweep": 0.0, "bay_open": 0.0, "ring_lift": 0.0, "rad_deploy": 0.0,
            "nozzle_open": 0.2, "engine_power": 0.0, "spark_arc": 0.0,
            "vapor_alpha": 0.0, "plasma_alpha": 0.0, "warp_charge": 0.0,
            "warp_lens": 0.0, "warp_active": 0.0, "warp_boom": 0.0,
            "rcs_burst": 0.0, "shield_hit": 0.0,
            "pitch_deg": base_pitch, "yaw_deg": 0.0, "roll_deg": 0.0,
            "vib": 0.0, "progress": 0.0, "ship_time": 0.0,
        }]

    dt = 0.25
    frames = []
    exit_mach = float(vessel_cfg["catapult_mach"] * (coil_charge / 100.0))

    # T-5秒〜0秒: 発射前待機
    for step in range(20):
        t = -5.0 + step * dt
        eng_pre = float(np.clip((t + 1.8) / 1.8, 0.0, 0.7))
        clamp = float(np.clip((t + 0.4) / 0.4, 0.0, 1.0))
        frames.append({
            "t": float(round(t, 2)),
            "phase": "CRYO_VENTING" if t < -3.0 else "LINEAR_COIL_CHARGE",
            "dist_m": 0.0, "alt_km": 0.04, "mach": 0.0, "vc": 0.0,
            "g": 1.0 + eng_pre * 0.9, "temp_k": 288.0 + eng_pre * 140.0,
            "clamp_open": clamp, "sabot_purge": 0.0, "fairing_purge": 0.0,
            "gear_deploy": 0.0, "speedbrake": 0.0, "chute_deploy": 0.0, "runway_speed": 0.0, "touchdown_smoke": 0.0,
            "wing_sweep": 0.0, "bay_open": 0.0, "ring_lift": 0.0, "rad_deploy": 0.0,
            "nozzle_open": 0.2 + eng_pre * 0.5, "engine_power": eng_pre,
            "spark_arc": float(np.clip((t + 2.5) / 2.5, 0.0, 0.6)),
            "vapor_alpha": 0.0, "plasma_alpha": 0.0, "warp_charge": 0.0,
            "warp_lens": 0.0, "warp_active": 0.0, "warp_boom": 0.0,
            "rcs_burst": 0.0, "shield_hit": 0.0,
            "pitch_deg": base_pitch, "yaw_deg": 0.0, "roll_deg": 0.0,
            "vib": eng_pre * 0.12, "progress": 0.0, "ship_time": 0.0,
        })

    dist_m = 0.0
    alt_km = 0.04
    mach = 0.0
    vc = 0.0
    progress = 0.0
    ship_time = 0.0
    sabot_p = 0.0
    fairing_p = 0.0
    gear_d = 0.0
    speedbrake = 0.0
    chute_d = 0.0
    runway_spd = 0.0
    td_smoke = 0.0
    bay_o = 0.0
    ring_l = 0.0
    rad_d = 0.0

    total_steps = 440
    for step in range(total_steps):
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
        shield = 0.0
        vib = 0.0
        pitch_cur = base_pitch
        yaw_deg = 0.0
        roll_deg = 0.0

        if t <= 12.0:
            phase = "CATAPULT_RAIL_ACCEL"
            accel_ratio = t / 12.0
            mach = (accel_ratio**1.25) * exit_mach
            speed_ms = mach * 340.0
            dist_m += speed_ms * dt * 0.35
            alt_km = 0.04 + (dist_m * np.sin(rad_pitch)) / 1000.0
            g_load = 10.5 * (coil_charge / 100.0)
            eng_pwr = 1.0
            nozzle = 0.95
            spark_arc = 1.0
            wing_sw = float(np.clip((mach - 1.5) / 10.0, 0.0, 1.0))
            if 0.85 <= mach <= 2.4:
                vapor = float(1.0 - abs(mach - 1.6) / 0.8)
            vib = 0.28 + vapor * 0.35
            # レール上はレール角12度、末端で空気力学的にごくわずかな迎え角（+1.5度）のみ付加
            if t > 10.5:
                pitch_blend = (t - 10.5) / 1.5
                pitch_cur = base_pitch + 1.5 * (pitch_blend**1.5)
            else:
                pitch_cur = base_pitch

        elif alt_km < 95.0 and t < 28.0:
            phase = "STRATOSPHERE_CLIMB" if alt_km < 48.0 else "EXOSPHERE_INSERTION"
            sabot_p = min(1.0, sabot_p + 0.6 * dt)
            mach = min(45.0, mach + 2.2 * dt)
            speed_ms = mach * 340.0
            dist_m += speed_ms * dt * 0.55
            space_f = float(np.clip((alt_km - 10.0) / 85.0, 0.0, 1.0))
            # 空気抵抗を最小化する極超音速リフティング軌道（13.5度から宇宙で水平0度へ）
            pitch_cur = 13.5 * (1.0 - space_f * 0.8)
            alt_km += (speed_ms * np.sin(np.radians(pitch_cur)) * dt) / 1000.0
            g_load = 5.2
            eng_pwr = 1.0
            nozzle = 1.0
            wing_sw = 1.0
            roll_deg = np.sin(t * 0.6) * 4.0
            if 12.0 <= alt_km <= 80.0:
                plasma = float(np.sin(((alt_km - 12.0) / 68.0) * np.pi) ** 0.75)
            vib = plasma * 0.45 + 0.12

        elif progress < 0.16:
            phase = "WARP_FIELD_COMPRESSION"
            alt_km = 120.0 + (progress / 0.16) * 280.0
            pitch_cur = max(0.0, 4.0 * (1.0 - progress / 0.16))
            eng_pwr = 0.7
            nozzle = 0.8
            g_load = 1.8
            wing_sw = 0.4
            progress += 0.010 * dt
            morph_prog = float(np.clip(progress / 0.16, 0.0, 1.0))
            bay_o = float(np.clip(morph_prog * 2.2, 0.0, 1.0))
            ring_l = float(np.clip((morph_prog - 0.2) * 2.0, 0.0, 1.0))
            rad_d = float(np.clip((morph_prog - 0.4) * 1.8, 0.0, 1.0))
            if vessel_cfg["style"] == "massdriver_spear":
                fairing_p = min(1.0, fairing_p + 0.8 * dt)
            w_charge = float(np.clip((morph_prog - 0.15) / 0.85, 0.0, 1.0))
            if morph_prog > 0.5:
                w_lens = float(np.sin(((morph_prog - 0.5) / 0.5) * (np.pi / 2)))
            if morph_prog > 0.92:
                w_boom = 1.0
            rcs = 1.0 if (0.1 < morph_prog < 0.35) else 0.0
            vc = 0.05 + w_charge * 0.25
            vib = 0.12 + w_charge * 0.22

        elif progress < 0.68:
            phase = "ALCUBIERRE_HYPER_WARP"
            alt_km = 400.0 + (progress - 0.16) * 500000.0
            pitch_cur = 0.0
            bay_o = 1.0
            ring_l = 1.0
            rad_d = 1.0
            wing_sw = 1.0
            eng_pwr = 1.0
            nozzle = 1.0
            target_vc = min(0.996, 0.55 + (warp_factor / 10.0) * 0.44)
            vc = min(target_vc, vc + 0.08 * dt)
            w_active = 1.0
            w_charge = 1.0
            g_load = 1.2
            vib = 0.06
            progress += (0.010 + vc * 0.024) * dt
            roll_deg = np.sin(t * 0.25) * 2.5
            if progress >= 0.66:
                w_boom = 1.0

        elif progress < 0.80:
            phase = "DEBRIS_AERO_BRAKING"
            alt_km = 99999.0
            pitch_cur = 2.5
            yaw_deg = 0.0
            roll_deg = np.sin(t * 1.0) * 3.0
            speedbrake = 1.0
            bay_o = 0.5
            ring_l = 0.2
            rad_d = 1.0
            wing_sw = 0.3
            eng_pwr = 0.35
            nozzle = 0.5
            vc = max(0.01, vc * 0.94)
            g_load = 4.2
            vib = 0.20
            progress += 0.014 * dt
            shield = float(np.sin(t * 6.0) ** 2) if 0.72 < progress < 0.78 else 0.0

        elif progress < 0.92:
            phase = "ATMOSPHERIC_ENTRY_GLIDESLOPE"
            descent_p = (progress - 0.80) / 0.12
            # 航空機のような3度〜5度の緩やかな滑空パス（120kmから1.8kmへ滑らかにアプローチ）
            alt_km = float(np.clip(120.0 * (1.0 - (descent_p**1.3)), 1.8, 120.0))
            mach = float(max(1.8, 18.0 * (1.0 - descent_p)))
            vc = 0.0
            pitch_cur = -3.5 * (1.0 - descent_p)
            roll_deg = np.sin(descent_p * np.pi * 2.0) * 4.0
            plasma = float(np.sin(descent_p * np.pi) ** 1.2) if descent_p < 0.65 else 0.0
            vapor = float(np.sin(descent_p * np.pi) ** 1.5) if descent_p >= 0.55 else 0.0
            g_load = 3.5 * (1.0 - descent_p * 0.5)
            eng_pwr = 0.35
            nozzle = 0.5
            bay_o = 0.0
            ring_l = 0.0
            rad_d = 0.0
            wing_sw = 0.15
            speedbrake = 0.85
            runway_spd = float(280.0 * (1.0 - descent_p * 0.3))
            vib = plasma * 0.4 + 0.12
            progress += 0.011 * dt

        elif progress < 0.965:
            phase = "FINAL_APPROACH_FLARE"
            flare_p = (progress - 0.92) / 0.045
            alt_km = float(max(0.0, 1.8 * (1.0 - flare_p)))
            mach = float(max(0.32, 1.8 * (1.0 - flare_p)))
            vc = 0.0
            # 飛行機通りの自然なフレア引き起こし（-3度から+3.5度へ）
            pitch_cur = -3.0 * (1.0 - flare_p) + 3.5 * flare_p
            roll_deg = np.sin(flare_p * np.pi) * 1.5
            gear_d = float(np.clip(flare_p * 2.2, 0.0, 1.0))
            speedbrake = 1.0
            runway_spd = 195.0 * (1.0 - flare_p * 0.2)
            g_load = 1.3
            eng_pwr = 0.15
            nozzle = 0.3
            vib = 0.08
            progress += 0.008 * dt

        else:
            phase = "TOUCHDOWN_ROLLOUT_STOP"
            rollout_p = (progress - 0.965) / 0.035
            alt_km = 0.0
            mach = float(max(0.0, 0.32 * (1.0 - rollout_p)))
            vc = 0.0
            pitch_cur = max(0.0, 3.5 * (1.0 - rollout_p * 2.0))
            roll_deg = 0.0
            gear_d = 1.0
            speedbrake = 1.0
            chute_d = float(np.clip(rollout_p * 3.5, 0.0, 1.0))
            runway_spd = float(max(0.0, 155.0 * (1.0 - rollout_p)))
            td_smoke = float(np.clip((1.0 - rollout_p) * 2.0, 0.0, 1.0))
            g_load = 1.0 + float(np.sin(rollout_p * np.pi)) * 0.5
            eng_pwr = 0.0
            nozzle = 0.2
            vib = 0.15 * (1.0 - rollout_p)
            progress = min(1.0, progress + 0.006 * dt)

        gamma = 1.0 / np.sqrt(max(0.001, 1.0 - (min(0.999, vc) ** 2)))
        ship_time += dt / gamma
        temp_k = 288.0 + plasma * 1750.0 + (w_active * 600.0) + (eng_pwr * 220.0)

        frames.append({
            "t": float(round(t, 2)), "phase": phase, "dist_m": float(dist_m), "alt_km": float(alt_km),
            "mach": float(mach), "vc": float(vc), "g": float(g_load), "temp_k": float(temp_k),
            "clamp_open": 1.0, "sabot_purge": float(sabot_p),
            "fairing_purge": float(fairing_p), "gear_deploy": float(gear_d),
            "speedbrake": float(speedbrake), "chute_deploy": float(chute_d), "runway_speed": float(runway_spd), "touchdown_smoke": float(td_smoke),
            "wing_sweep": float(wing_sw), "bay_open": float(bay_o), "ring_lift": float(ring_l), "rad_deploy": float(rad_d),
            "nozzle_open": float(nozzle), "engine_power": float(eng_pwr), "spark_arc": float(spark_arc),
            "vapor_alpha": float(vapor), "plasma_alpha": float(plasma), "warp_charge": float(w_charge),
            "warp_lens": float(w_lens), "warp_active": float(w_active), "warp_boom": float(w_boom),
            "rcs_burst": float(rcs), "shield_hit": float(shield),
            "pitch_deg": float(pitch_cur), "yaw_deg": float(yaw_deg), "roll_deg": float(roll_deg),
            "vib": float(vib), "progress": float(progress), "ship_time": float(ship_time),
        })

        if progress >= 1.0:
            for extra in range(30):
                frames.append({
                    "t": float(round(t + (extra + 1) * dt, 2)), "phase": "PLANETARY_RUNWAY_SECURED",
                    "dist_m": float(dist_m), "alt_km": 0.0, "mach": 0.0, "vc": 0.0, "g": 1.0,
                    "temp_k": 310.0, "clamp_open": 1.0, "sabot_purge": 1.0,
                    "fairing_purge": float(fairing_p), "gear_deploy": 1.0, "speedbrake": 1.0,
                    "chute_deploy": 1.0, "runway_speed": 0.0, "touchdown_smoke": 0.0, "wing_sweep": 0.0,
                    "bay_open": 0.0, "ring_lift": 0.0, "rad_deploy": 1.0, "nozzle_open": 0.2,
                    "engine_power": 0.0, "spark_arc": 0.0, "vapor_alpha": 0.0, "plasma_alpha": 0.0,
                    "warp_charge": 0.0, "warp_lens": 0.0, "warp_active": 0.0, "warp_boom": 0.0,
                    "rcs_burst": 0.0, "shield_hit": 0.0,
                    "pitch_deg": 0.0, "yaw_deg": 0.0, "roll_deg": 0.0,
                    "vib": 0.0, "progress": 1.0, "ship_time": float(ship_time),
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
    "aux_boosters": False,
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
# 📺 Three.js 完全映画仕様・実写NASAアセット＆物理光学VFX版
# =========================================================================
html_code = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
*{box-sizing:border-box;}
body,html{
  margin:0;padding:0;width:100%;height:100%;overflow:hidden;
  background:#000205;font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,Roboto,sans-serif;
  color:#f8fafc;user-select:none;
}
#webgl-canvas{
  width:100%;height:100%;display:block;position:absolute;top:0;left:0;
  z-index:1;touch-action:none;
}
.letterbox-top{position:absolute;top:0;left:0;width:100%;height:14px;background:#000;z-index:90;pointer-events:none;}
.letterbox-bottom{position:absolute;bottom:0;left:0;width:100%;height:14px;background:#000;z-index:90;pointer-events:none;}

.hud-top-bar{
  position:absolute;top:14px;left:0;width:100%;
  background:linear-gradient(180deg,rgba(2,6,18,0.95) 0%,rgba(4,12,28,0.85) 100%);
  border-bottom:1px solid rgba(56,189,248,0.3);
  display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;
  padding:6px 18px;gap:8px;box-shadow:0 4px 25px rgba(0,0,0,0.85);
  z-index:50;pointer-events:auto;
}
.hud-left{display:flex;align-items:center;gap:12px;font-size:11px;}
.badge{background:rgba(14,165,233,0.18);border:1px solid #38bdf8;color:#38bdf8;padding:2px 8px;border-radius:3px;font-weight:800;}
.cam-btn-group{display:flex;align-items:center;gap:5px;}
.cam-btn{
  background:rgba(15,23,42,0.88);border:1px solid rgba(56,189,248,0.4);color:#38bdf8;
  font-size:9.5px;font-weight:800;padding:4px 8px;border-radius:3px;cursor:pointer;
  transition:all 0.2s;
}
.cam-btn:hover{background:rgba(56,189,248,0.3);color:#fff;}
.cam-btn.active{background:#0284c7;color:#fff;border-color:#38bdf8;}

#comms-strip{
  position:absolute;top:54px;left:0;width:100%;
  background:rgba(2,6,23,0.75);border-bottom:1px solid rgba(16,185,129,0.3);
  padding:3px 20px;font-size:10px;font-family:monospace;color:#6ee7b7;letter-spacing:1px;
  z-index:45;pointer-events:none;display:flex;align-items:center;gap:8px;
}

#ils-hud{
  position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
  width:280px;height:180px;border:1px dashed rgba(16,185,129,0.4);border-radius:6px;
  pointer-events:none;z-index:35;display:none;flex-direction:column;justify-content:space-between;
  padding:8px 12px;font-family:monospace;color:#10b981;font-size:10.5px;
}
.ils-cross{position:absolute;top:50%;left:50%;width:80px;height:80px;transform:translate(-50%,-50%);pointer-events:none;}
.ils-cross::before{content:'';position:absolute;top:50%;left:0;width:100%;height:1px;background:#10b981;}
.ils-cross::after{content:'';position:absolute;top:0;left:50%;width:1px;height:100%;background:#10b981;}

.playback-controller{
  position:absolute;bottom:148px;left:20px;right:20px;
  display:flex;align-items:center;gap:12px;background:rgba(2,6,23,0.78);
  border:1px solid rgba(56,189,248,0.3);padding:6px 14px;border-radius:6px;
  z-index:50;pointer-events:auto;backdrop-filter:blur(6px);
}
.play-btn{background:#0284c7;border:none;color:#fff;font-size:11px;font-weight:800;padding:4px 10px;border-radius:4px;cursor:pointer;}
.play-btn:hover{background:#0369a1;}
.speed-btn{background:rgba(15,23,42,0.8);border:1px solid rgba(56,189,248,0.4);color:#38bdf8;font-size:10px;font-weight:700;padding:4px 8px;border-radius:4px;cursor:pointer;}
.speed-btn.active{background:#38bdf8;color:#020617;}
.scrub-slider{flex:1;-webkit-appearance:none;height:5px;border-radius:3px;background:rgba(56,189,248,0.25);outline:none;cursor:pointer;}
.scrub-slider::-webkit-slider-thumb{-webkit-appearance:none;width:14px;height:14px;border-radius:50%;background:#38bdf8;cursor:pointer;box-shadow:0 0 8px #38bdf8;}

.radar-panel{
  position:absolute;bottom:68px;left:0;width:100%;height:76px;
  background:rgba(2,6,20,0.92);border-top:1px solid rgba(56,189,248,0.45);border-bottom:1px solid rgba(56,189,248,0.2);
  display:flex;align-items:center;padding:0 20px;gap:14px;z-index:25;pointer-events:none;
}
.radar-tag{font-size:9.5px;color:#38bdf8;font-weight:900;white-space:nowrap;letter-spacing:1px;border-right:1px solid rgba(56,189,248,0.3);padding-right:12px;}
#radar-canvas{flex:1;height:62px;display:block;}

.hud-bottom{
  position:absolute;bottom:14px;left:0;width:100%;height:54px;
  background:linear-gradient(0deg,rgba(2,6,18,0.94) 0%,rgba(6,13,30,0.82) 100%);
  border-top:1px solid rgba(148,163,184,0.2);display:grid;grid-template-columns:repeat(5,1fr);align-items:center;
  padding:0 20px;z-index:20;pointer-events:none;
}
.metric{display:flex;flex-direction:column;border-left:2px solid rgba(56,189,248,0.35);padding-left:10px;}
.metric-lbl{font-size:8.5px;color:#94a3b8;letter-spacing:1.1px;}
.metric-val{font-size:15px;font-weight:900;color:#f8fafc;margin-top:1px;}

#complete-banner{
  display:none;position:absolute;top:220px;left:50%;transform:translateX(-50%);
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

<div class="hud-top-bar">
  <div class="hud-left">
    <span class="badge">CINEMA VFX DIRECTOR</span>
    <span>PHASE: <strong id="ui-phase" style="color:#fbbf24;">PAD_STANDBY</strong></span>
    <span>ALT: <strong id="ui-alt">0.04 km</strong></span>
    <span>VEL: <strong id="ui-spd" style="color:#38bdf8;">M 0.0</strong></span>
    <span>CLOCK: <strong id="ui-clock">T-05.0s</strong></span>
  </div>
  <div class="cam-btn-group">
    <button id="cam-btn-0" class="cam-btn active" onclick="switchCamMode(0)">AUTO</button>
    <button id="cam-btn-1" class="cam-btn" onclick="switchCamMode(1)">CHASE</button>
    <button id="cam-btn-2" class="cam-btn" onclick="switchCamMode(2)">COCKPIT</button>
    <button id="cam-btn-3" class="cam-btn" onclick="switchCamMode(3)">WING</button>
    <button id="cam-btn-4" class="cam-btn" onclick="switchCamMode(4)">FLY-BY</button>
  </div>
</div>

<div id="comms-strip">
  <span style="color:#38bdf8;font-weight:800;">COMMS //</span>
  <span id="comms-text">SYSTEM CHECK OK. READY FOR INJECTION SEQUENCE.</span>
</div>

<div id="ils-hud">
  <div style="display:flex;justify-content:space-between;">
    <span>ILS RUNWAY 04L</span>
    <span>GS: 3.5° LOCKED</span>
  </div>
  <div class="ils-cross"></div>
  <div style="display:flex;justify-content:space-between;">
    <span id="ils-dist">ALT: 1,800 M</span>
    <span id="ils-callout">LOCALIZER NOMINAL</span>
  </div>
</div>

<div class="playback-controller">
  <button id="play-pause-btn" class="play-btn">PAUSE</button>
  <button id="speed-02" class="speed-btn">0.2x</button>
  <button id="speed-10" class="speed-btn active">1.0x</button>
  <button id="speed-20" class="speed-btn">2.0x</button>
  <input type="range" id="timeline-slider" class="scrub-slider" min="0" max="100" value="0" step="0.1">
</div>

<div class="radar-panel">
  <div id="radar-label" class="radar-tag">TACTICAL RADAR<br><span style="color:#94a3b8;font-size:8px;">ORBITAL PROJECTION</span></div>
  <canvas id="radar-canvas"></canvas>
</div>

<div id="complete-banner">
  <div style="font-size:18px;font-weight:900;color:#6ee7b7;letter-spacing:1.5px;">RUNWAY ARREST COMPLETE // TOUCHDOWN SECURED</div>
  <div style="font-size:11px;color:#d1fae5;margin-top:4px;">PARACHUTE JETTISONED / CHASSIS COOLED / MISSION SUCCESSFUL</div>
</div>

<div class="hud-bottom">
  <div class="metric"><span class="metric-lbl">RELATIVISTIC VEL</span><span class="metric-val"><span id="ui-vc">0.000</span> <small style="font-size:10px;color:#64748b;">c</small></span></div>
  <div class="metric"><span class="metric-lbl">HULL THERMAL</span><span class="metric-val"><span id="ui-temp">288</span> <small style="font-size:10px;color:#64748b;">K</small></span></div>
  <div class="metric"><span class="metric-lbl">G-FORCE</span><span class="metric-val"><span id="ui-g">1.0</span> <small style="font-size:10px;color:#64748b;">G</small></span></div>
  <div class="metric"><span class="metric-lbl">LORENTZ (γ)</span><span class="metric-val"><span id="ui-gamma">1.00</span> <small style="font-size:10px;color:#64748b;">x</small></span></div>
  <div class="metric"><span class="metric-lbl">MISSION PROGRESS</span><span class="metric-val"><span id="ui-prog">0.0</span> <small style="font-size:10px;color:#64748b;">%</small></span></div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
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
// 1. レンダラー＆PMREM IBL＆大気圏マルチストップ散乱空＆全天球リアル星空
// =========================================================================
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, powerPreference: "high-performance" });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
renderer.setSize(W, H);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const scene = new THREE.Scene();
const baseFogColor = new THREE.Color(cfg.env.fog_color);
scene.fog = new THREE.FogExp2(baseFogColor, cfg.env.fog_density);

// PMREM IBL 生成
const pmremGenerator = new THREE.PMREMGenerator(renderer);
pmremGenerator.compileEquirectangularShader();
const envScene = new THREE.Scene();
envScene.add(new THREE.HemisphereLight(0xdbeafe, 0x030712, 2.5));
const dirFill = new THREE.DirectionalLight(0xffeedd, 3.0);
dirFill.position.set(100, 150, 100);
envScene.add(dirFill);
const generatedEnvMap = pmremGenerator.fromScene(envScene).texture;
scene.environment = generatedEnvMap;

const cameraMain = new THREE.PerspectiveCamera(52, W / H, 0.5, 980000);

let baseCamPos = new THREE.Vector3(-32.0, 14.0, -85.0);
let baseTarget = new THREE.Vector3(0.0, 1.2, -4.0);

if (cfg.cam_preset.includes("エクストラ")) {
    baseCamPos.set(-48.0, 22.0, -125.0);
} else if (cfg.cam_preset.includes("チェイス")) {
    baseCamPos.set(-24.0, 9.5, -65.0);
}
cameraMain.position.copy(baseCamPos);
cameraMain.lookAt(baseTarget);

const controls = new THREE.OrbitControls(cameraMain, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.enabled = false;

// 大気散乱スカイドーム
const atmoSkyGeo = new THREE.SphereGeometry(180000, 32, 16);
const atmoSkyMat = new THREE.ShaderMaterial({
    vertexShader: `varying vec3 vWorldPos; void main() { vec4 wp = modelMatrix * vec4(position, 1.0); vWorldPos = wp.xyz; gl_Position = projectionMatrix * viewMatrix * wp; }`,
    fragmentShader: `
        varying vec3 vWorldPos;
        uniform vec3 uZenith; uniform vec3 uHorizon; uniform vec3 uSunDir; uniform float uSpaceFade;
        void main() {
            vec3 dir = normalize(vWorldPos);
            float h = clamp(dir.y, -0.2, 1.0);
            float curve = pow(max(0.0, h + 0.2) / 1.2, 0.45);
            vec3 midSky = mix(uHorizon, uZenith, 0.5) + vec3(0.03, 0.06, 0.12);
            vec3 sky = (curve < 0.5) ? mix(uHorizon, midSky, curve * 2.0) : mix(midSky, uZenith, (curve - 0.5) * 2.0);
            float sunHalo = pow(max(0.0, dot(dir, uSunDir)), 14.0) * 0.45;
            sky += vec3(1.0, 0.75, 0.45) * sunHalo;
            sky = mix(sky, vec3(0.001, 0.003, 0.008), uSpaceFade);
            gl_FragColor = vec4(sky, 1.0);
        }
    `,
    uniforms: {
        uZenith: { value: new THREE.Color(cfg.env.sky_zenith) },
        uHorizon: { value: new THREE.Color(cfg.env.sky_horizon) },
        uSunDir: { value: new THREE.Vector3().fromArray(cfg.env.sun_pos).normalize() },
        uSpaceFade: { value: 0.0 }
    },
    side: THREE.BackSide, depthWrite: false
});
const atmoSkyDome = new THREE.Mesh(atmoSkyGeo, atmoSkyMat);
scene.add(atmoSkyDome);

// 全天球リアル星空（fog: false でフォグ消滅を解消）
const spaceFieldGroup = new THREE.Group();
spaceFieldGroup.visible = false;
scene.add(spaceFieldGroup);

function createRealStarField(count, radiusMin, radiusMax, size, baseColor) {
    const geo = new THREE.BufferGeometry();
    const pos = new Float32Array(count * 3);
    const col = new Float32Array(count * 3);
    const c = new THREE.Color(baseColor);
    for (let i = 0; i < count; i++) {
        const u = Math.random(), v = Math.random();
        const theta = u * 2.0 * Math.PI, phi = Math.acos(2.0 * v - 1.0);
        const r = radiusMin + Math.random() * (radiusMax - radiusMin);
        pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
        pos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
        pos[i * 3 + 2] = r * Math.cos(phi);
        const lum = 0.5 + Math.random() * 0.5;
        col[i * 3] = c.r * lum; col[i * 3 + 1] = c.g * lum; col[i * 3 + 2] = c.b * lum;
    }
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
    return new THREE.Points(geo, new THREE.PointsMaterial({
        size: size, vertexColors: true, transparent: true, opacity: 0.95,
        sizeAttenuation: false, fog: false
    }));
}
spaceFieldGroup.add(createRealStarField(12000, 80000, 160000, 1.2, 0xdbeafe));
spaceFieldGroup.add(createRealStarField(7000, 70000, 140000, 1.8, 0x93c5fd));
spaceFieldGroup.add(createRealStarField(9000, 60000, 130000, 2.2, 0xfbcfe8));

// 太陽光（広角シャドウカメラ最適化）
const sunLight = new THREE.DirectionalLight(cfg.env.sun_color, cfg.env.sun_int);
sunLight.position.set(cfg.env.sun_pos[0] * 0.15, cfg.env.sun_pos[1] * 0.15 + 40.0, cfg.env.sun_pos[2] * 0.15);
sunLight.castShadow = true;
sunLight.shadow.mapSize.width = 2048;
sunLight.shadow.mapSize.height = 2048;
sunLight.shadow.camera.near = 0.5;
sunLight.shadow.camera.far = 1200;
sunLight.shadow.camera.left = -60;
sunLight.shadow.camera.right = 60;
sunLight.shadow.camera.top = 60;
sunLight.shadow.camera.bottom = -60;
scene.add(sunLight);
scene.add(new THREE.HemisphereLight(0x93c5fd, 0x030712, 1.4));

// ポストプロセス：フィルムグレイン＆色収差
const FilmCinemaShader = {
    uniforms: {
        "tDiffuse": { value: null },
        "uDistort": { value: 0.0 },
        "uInvert": { value: 0.0 },
        "uTime": { value: 0.0 }
    },
    vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `
        uniform sampler2D tDiffuse; uniform float uDistort; uniform float uInvert; uniform float uTime; varying vec2 vUv;
        void main() {
            vec2 center = vec2(0.5, 0.5); vec2 dir = vUv - center; float dist = length(dir);
            float ca = 0.0018 + uDistort * 0.04;
            vec2 rUv = vUv + dir * (ca + uDistort * 0.08);
            vec2 gUv = vUv;
            vec2 bUv = vUv - dir * (ca + uDistort * 0.08);
            vec3 col = vec3(texture2D(tDiffuse, rUv).r, texture2D(tDiffuse, gUv).g, texture2D(tDiffuse, bUv).b);
            if (uInvert > 0.01) col = mix(col, vec3(1.0) - col, uInvert);
            // フィルムグレインノイズ
            float grain = fract(sin(dot(vUv * (uTime * 0.1 + 1.0), vec2(12.9898, 78.233))) * 43758.5453) * 0.035;
            col += grain;
            gl_FragColor = vec4(col * smoothstep(0.95, 0.35, dist), 1.0);
        }
    `
};

const composerMain = new THREE.EffectComposer(renderer);
composerMain.addPass(new THREE.RenderPass(scene, cameraMain));
composerMain.addPass(new THREE.UnrealBloomPass(new THREE.Vector2(W, H), 0.85, 0.35, 0.85));
const filmPass = new THREE.ShaderPass(FilmCinemaShader);
composerMain.addPass(filmPass);

const radarCanvas = document.getElementById('radar-canvas');
const rCtx = radarCanvas.getContext('2d');
const radarLabelEl = document.getElementById('radar-label');

function updateCameraAspect() {
    W = window.innerWidth; H = window.innerHeight;
    renderer.setSize(W, H);
    composerMain.setSize(W, H);
    cameraMain.aspect = W / H;
    cameraMain.fov = (W / H < 1.0) ? 65.0 : 52.0;
    cameraMain.updateProjectionMatrix();
    radarCanvas.width = radarCanvas.clientWidth * 1.5;
    radarCanvas.height = radarCanvas.clientHeight * 1.5;
}
window.addEventListener('resize', updateCameraAspect);
updateCameraAspect();

// =========================================================================
// 2. 音声合成＆Web Audio
// =========================================================================
let actx = null, rocketGain = null, rocketFilter = null, coilGain = null, rcsGain = null;
let lastAnnouncedPhase = "";
let availableVoices = [];

function updateVoiceList() {
    if ('speechSynthesis' in window) availableVoices = window.speechSynthesis.getVoices();
}
if ('speechSynthesis' in window) {
    updateVoiceList();
    window.speechSynthesis.onvoiceschanged = updateVoiceList;
}

const commsTextEl = document.getElementById('comms-text');
const ilsHudEl = document.getElementById('ils-hud');

function speakCallout(text) {
    if (commsTextEl) commsTextEl.innerText = text;
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        setTimeout(() => {
            const u = new SpeechSynthesisUtterance(text);
            u.lang = 'en-US';
            if (availableVoices.length === 0) availableVoices = window.speechSynthesis.getVoices();
            const enVoice = availableVoices.find(v => (v.lang === 'en-US' || v.lang === 'en_US') && (v.name.includes('Google') || v.name.includes('Natural') || v.name.includes('Zira') || v.name.includes('David')))
                         || availableVoices.find(v => v.lang.startsWith('en'));
            if (enVoice) u.voice = enVoice;
            u.rate = 1.0; u.pitch = 1.0; u.volume = 0.9;
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

        rcsGain = actx.createGain();
        rcsGain.gain.value = 0.0001;
        whiteNoise.connect(rcsGain);
        rcsGain.connect(actx.destination);

        const coilOsc = actx.createOscillator();
        coilOsc.type = 'sawtooth';
        coilOsc.frequency.value = 110;
        coilGain = actx.createGain();
        coilGain.gain.value = 0.0001;
        coilOsc.connect(coilGain);
        coilGain.connect(actx.destination);
        coilOsc.start(0);
    } catch(e){}
}
window.addEventListener('pointerdown', () => { if (actx && actx.state === 'suspended') actx.resume(); }, { once: true });

// =========================================================================
// 3. 高密度実写PBRテクスチャ＆NASA実写アセットローダー
// =========================================================================
const texLoader = new THREE.TextureLoader();
texLoader.setCrossOrigin('anonymous');

const earthDayTex = texLoader.load('https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_atmos_2048.jpg');
const earthCloudsTex = texLoader.load('https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/earth_clouds_1024.png');
const moonCraterTex = texLoader.load('https://raw.githubusercontent.com/mrdoob/three.js/master/examples/textures/planets/moon_1024.jpg');

function makeMasterPbrTexture() {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 1024;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#2d3748'; ctx.fillRect(0, 0, 1024, 1024);

    for (let x = 0; x < 1024; x += 32) {
        for (let y = 0; y < 1024; y += 16) {
            const v = 35 + Math.floor(Math.random() * 25);
            ctx.fillStyle = `rgb(${v},${v+2},${v+5})`;
            ctx.fillRect(x + 1, y + 1, 30, 14);
            ctx.fillStyle = '#080c14';
            ctx.fillRect(x + 2, y + 2, 1.5, 1.5); ctx.fillRect(x + 28, y + 2, 1.5, 1.5);
        }
    }
    ctx.strokeStyle = '#0f172a'; ctx.lineWidth = 1.5;
    for (let x = 0; x <= 1024; x += 32) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 1024); ctx.stroke(); }
    for (let y = 0; y <= 1024; y += 16) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(1024, y); ctx.stroke(); }

    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(8, 8);
    return tex;
}
const masterHullTex = makeMasterPbrTexture();

const matHull = new THREE.MeshStandardMaterial({
    color: cfg.hull_color, metalness: cfg.metalness, roughness: cfg.roughness,
    bumpMap: masterHullTex, bumpScale: 0.035, envMapIntensity: 2.2
});
const matBellyTile = new THREE.MeshStandardMaterial({
    color: cfg.belly_color, metalness: 0.25, roughness: 0.85,
    bumpMap: masterHullTex, bumpScale: 0.05, envMapIntensity: 1.2
});
const matTitaniumFrame = new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.95, roughness: 0.18, envMapIntensity: 2.0 });
const matPistonRod = new THREE.MeshStandardMaterial({ color: 0xf8fafc, metalness: 0.98, roughness: 0.04 });
const matDarkAlloy = new THREE.MeshStandardMaterial({ color: 0x0f172a, metalness: 0.92, roughness: 0.25, envMapIntensity: 1.5 });
const matGoldMLI = new THREE.MeshStandardMaterial({ color: 0xd97706, metalness: 0.95, roughness: 0.25, envMapIntensity: 2.5 });
const matCopperCoil = new THREE.MeshStandardMaterial({ color: 0xb45309, metalness: 0.95, roughness: 0.18 });
// スモークゴールド・フラッシュマウントキャノピー
const matCanopy = new THREE.MeshPhysicalMaterial({
    color: 0x050811, metalness: 0.95, roughness: 0.02, transparent: true, opacity: 0.85,
    reflectivity: 0.95, clearcoat: 1.0, envMapIntensity: 3.0
});
const matCryoPipe = new THREE.MeshStandardMaterial({ color: 0xcfd8dc, roughness: 0.5, metalness: 0.35 });

// =========================================================================
// 4. 実写映画仕様ステルス・ウェッジ宇宙船（チャイン多面体構造）
// =========================================================================
const radAngle = THREE.MathUtils.degToRad(cfg.env.angle_deg);
const shipRoot = new THREE.Group();
scene.add(shipRoot);

const shipPitchGroup = new THREE.Group();
shipRoot.add(shipPitchGroup);

const shipMeshGroup = new THREE.Group();
shipPitchGroup.add(shipMeshGroup);

// 内部骨格・極低温配管
const innerSkeletonGroup = new THREE.Group();
shipMeshGroup.add(innerSkeletonGroup);
innerSkeletonGroup.add(new THREE.Mesh(new THREE.BoxGeometry(2.2, 1.0, 28.0), matTitaniumFrame));

for (let s of [-1, 1]) {
    const pipePts = [new THREE.Vector3(s * 1.5, -0.4, 12.0), new THREE.Vector3(s * 2.2, -0.2, 4.0), new THREE.Vector3(s * 2.8, -0.3, -4.0), new THREE.Vector3(s * 0.9, 0.0, -15.0)];
    innerSkeletonGroup.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pipePts), 32, 0.16, 10, false), matCryoPipe));
}

if (cfg.style === "magnetic_fusion") {
    for (let z of [-8.5, -3.5]) {
        for (let a = 0; a < 4; a++) {
            const ang = (a / 4) * Math.PI * 2 + Math.PI / 4;
            const tank = new THREE.Mesh(new THREE.SphereGeometry(1.65, 24, 24), matGoldMLI);
            tank.position.set(Math.cos(ang) * 3.2, Math.sin(ang) * 2.4, z);
            shipMeshGroup.add(tank);
        }
    }
}

// 可変ペイロードベイ扉
const bayDoors = [];
for (let s of [-1, 1]) {
    const doorPivot = new THREE.Group();
    doorPivot.position.set(s * 2.4, 1.15, -2.5);
    shipMeshGroup.add(doorPivot);
    const dPanel = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.22, 12.0), matHull);
    dPanel.position.set(-s * 1.1, 0, 0);
    doorPivot.add(dPanel);
    bayDoors.push({ pivot: doorPivot, side: s });

    const cyl = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.4, 8), matTitaniumFrame);
    const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 1.2, 8), matPistonRod);
    cyl.position.set(s * 1.2, 0.7, -2.5);
    cyl.rotation.z = s * 0.5;
    rod.position.set(0, 0.6, 0);
    cyl.add(rod);
    shipMeshGroup.add(cyl);
}

// シャープなチャイン・主翼
const halfSpan = cfg.wings_span * 0.5;
const wingPivots = [];
const elevonMeshes = [];
for (let s of [-1, 1]) {
    const pivot = new THREE.Group();
    pivot.position.set(s * 3.2, -0.05, 1.5);
    shipMeshGroup.add(pivot);

    const wShape = new THREE.Shape();
    wShape.moveTo(0, 5.0);
    wShape.lineTo(s * (halfSpan - 3.2), -3.0);
    wShape.lineTo(s * (halfSpan - 3.5), -7.0);
    wShape.lineTo(0, -10.5);
    wShape.closePath();

    const wMesh = new THREE.Mesh(new THREE.ExtrudeGeometry(wShape, { depth: 0.28, bevelThickness: 0.08, bevelSize: 0.25 }), matHull);
    wMesh.rotation.x = Math.PI / 2;
    wMesh.castShadow = true;
    pivot.add(wMesh);
    wingPivots.push({ group: pivot, side: s });

    const elMesh = new THREE.Mesh(new THREE.BoxGeometry(halfSpan * 0.45, 0.16, 1.5), matDarkAlloy);
    elMesh.position.set(s * (halfSpan * 0.55), 0, -8.4);
    pivot.add(elMesh);
    elevonMeshes.push({ mesh: elMesh, side: s });
}

// 背面スピードエアブレーキ
const speedbrakePivot = new THREE.Group();
speedbrakePivot.position.set(0, 1.25, -5.0);
shipMeshGroup.add(speedbrakePivot);
const speedbrakeMesh = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.16, 4.2), matTitaniumFrame);
speedbrakeMesh.position.set(0, 0, -2.1);
speedbrakePivot.add(speedbrakeMesh);

// 3点式ランディングギア
const landingGears = [];
[{ x: 0, y: -0.4, z: 9.0 }, { x: -3.5, y: -0.6, z: -6.0 }, { x: 3.5, y: -0.6, z: -6.0 }].forEach((gp) => {
    const gPivot = new THREE.Group();
    gPivot.position.set(gp.x, gp.y, gp.z);
    const strut = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 2.6, 8), matTitaniumFrame);
    strut.position.y = -1.3;
    gPivot.add(strut);
    const footPad = new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.5, 0.2, 12), matDarkAlloy);
    footPad.position.y = -2.6;
    gPivot.add(footPad);
    gPivot.scale.set(0.001, 0.001, 0.001);
    shipMeshGroup.add(gPivot);
    landingGears.push(gPivot);
});

// タイヤ白煙（左右ギア外側に逃がし機体を隠さない）
const smokePuffsLeft = [];
const smokePuffsRight = [];
const smokeGeo = new THREE.SphereGeometry(0.85, 8, 8);
const smokeMat = new THREE.MeshBasicMaterial({ color: 0xe2e8f0, transparent: true, opacity: 0.0 });
for (let sm = 0; sm < 6; sm++) {
    const pl = new THREE.Mesh(smokeGeo, smokeMat); shipMeshGroup.add(pl); smokePuffsLeft.push(pl);
    const pr = new THREE.Mesh(smokeGeo, smokeMat); shipMeshGroup.add(pr); smokePuffsRight.push(pr);
}

// ドラッグシュート
const chuteGroup = new THREE.Group();
chuteGroup.position.set(0, 0.8, -16.5);
chuteGroup.scale.set(0.001, 0.001, 0.001);
shipMeshGroup.add(chuteGroup);

const chuteCanopy = new THREE.Mesh(
    new THREE.ConeGeometry(4.8, 6.0, 12, 1, true),
    new THREE.MeshStandardMaterial({ color: 0xd97706, side: THREE.DoubleSide, roughness: 0.6 })
);
chuteCanopy.rotation.x = -Math.PI / 2;
chuteCanopy.position.z = -18.0;
chuteGroup.add(chuteCanopy);

for (let cLine = 0; cLine < 4; cLine++) {
    const ang = (cLine / 4) * Math.PI * 2;
    const lineGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0,0,0), new THREE.Vector3(Math.cos(ang)*4.5, Math.sin(ang)*4.5, -15.0)]);
    chuteGroup.add(new THREE.Line(lineGeo, new THREE.LineBasicMaterial({ color: 0xffffff })));
}

// 24枚アイリスノズル
const nozzleGimbalRoot = new THREE.Group();
nozzleGimbalRoot.position.set(0, 0, -14.2);
shipMeshGroup.add(nozzleGimbalRoot);

const irisPaddles = [];
for (let i = 0; i < 24; i++) {
    const ang = (i / 24) * Math.PI * 2;
    const pPivot = new THREE.Group();
    pPivot.position.set(Math.cos(ang) * 2.3, Math.sin(ang) * 2.3, -1.0);
    pPivot.rotation.z = ang;
    nozzleGimbalRoot.add(pPivot);
    const blade = new THREE.Mesh(new THREE.BoxGeometry(0.52, 0.08, 3.2), (i % 2 === 0) ? matTitaniumFrame : matDarkAlloy);
    blade.position.set(0, 0.05, -1.4);
    pPivot.add(blade);
    irisPaddles.push(pPivot);
}

// 実写ステルス多面体チャイン・ボディ造形
function createStealthChassisGeometry() {
    const sections = [
        { z: 18.0, w: 0.2, hTop: 0.1, hBtm: 0.1, yOff: 0.0 },
        { z: 14.0, w: 1.8, hTop: 0.65, hBtm: 0.35, yOff: 0.08 },
        { z: 9.0,  w: 3.8, hTop: 1.25, hBtm: 0.75, yOff: 0.2 },
        { z: 4.0,  w: 4.8, hTop: 1.45, hBtm: 0.95, yOff: 0.15 },
        { z: -2.0, w: 5.4, hTop: 1.55, hBtm: 1.05, yOff: 0.08 },
        { z: -8.0, w: 5.2, hTop: 1.45, hBtm: 1.15, yOff: 0.0 },
        { z: -14.0,w: 4.2, hTop: 1.25, hBtm: 1.15, yOff: -0.08 }
    ];
    const radialSegs = 24, zSegs = sections.length;
    const geo = new THREE.BufferGeometry(), pos = [], uvs = [], indices = [];
    for (let j = 0; j < zSegs; j++) {
        const sec = sections[j];
        for (let i = 0; i <= radialSegs; i++) {
            const theta = (i / radialSegs) * Math.PI * 2;
            const chineX = Math.sign(Math.cos(theta)) * Math.pow(Math.abs(Math.cos(theta)), 0.85);
            pos.push(chineX * (sec.w * 0.5), sec.yOff + Math.sin(theta) * (Math.sin(theta) >= 0 ? sec.hTop : sec.hBtm), sec.z);
            uvs.push(i / radialSegs, j / (zSegs - 1));
        }
    }
    for (let j = 0; j < zSegs - 1; j++) {
        for (let i = 0; i < radialSegs; i++) {
            indices.push(j * 25 + i, (j + 1) * 25 + i, j * 25 + (i + 1));
            indices.push((j + 1) * 25 + i, (j + 1) * 25 + (i + 1), j * 25 + (i + 1));
        }
    }
    geo.setIndex(indices);
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    geo.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
    geo.computeVertexNormals();
    return geo;
}
const loftGeo = createStealthChassisGeometry();
shipMeshGroup.add(new THREE.Mesh(loftGeo, matHull));
const bellyMesh = new THREE.Mesh(loftGeo, matBellyTile);
bellyMesh.scale.set(0.985, 0.98, 0.995);
bellyMesh.position.y = -0.05;
shipMeshGroup.add(bellyMesh);

// フラッシュマウント・多面体キャノピー
const canopyGeo = new THREE.BufferGeometry();
const cVerts = new Float32Array([
    0, 1.45, 12.0,   -0.85, 0.95, 7.5,   0.85, 0.95, 7.5,
    0, 1.45, 12.0,    0.85, 0.95, 7.5,   0.0, 1.35, 6.0,
    0, 1.45, 12.0,    0.0, 1.35, 6.0,   -0.85, 0.95, 7.5
]);
canopyGeo.setAttribute('position', new THREE.BufferAttribute(cVerts, 3));
canopyGeo.computeVertexNormals();
const canopyGlass = new THREE.Mesh(canopyGeo, matCanopy);
shipMeshGroup.add(canopyGlass);

// アルクビエレ・ワープリング
const warpRingAssembly = new THREE.Group();
warpRingAssembly.position.set(0, 0.0, -2.5);
warpRingAssembly.scale.set(0.001, 0.001, 0.001);
shipMeshGroup.add(warpRingAssembly);

const rotorClockwise = new THREE.Group();
const rotorCounter = new THREE.Group();
warpRingAssembly.add(rotorClockwise);
warpRingAssembly.add(rotorCounter);

const ringSegments = [];
for (let i = 0; i < 16; i++) {
    const segPivot = new THREE.Group();
    segPivot.rotation.z = (i / 16) * Math.PI * 2;
    rotorClockwise.add(segPivot);
    const block = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.45, 1.8), matDarkAlloy);
    block.position.set(0, 6.2, 0);
    segPivot.add(block);
    const coilCore = new THREE.Mesh(new THREE.BoxGeometry(0.8, 0.35, 1.4), new THREE.MeshBasicMaterial({ color: cfg.aurora_hex }));
    coilCore.position.set(0, 6.2, 0);
    segPivot.add(coilCore);
    ringSegments.push({ block, coilCore, baseR: 6.2 });
}
rotorCounter.add(new THREE.Mesh(new THREE.TorusGeometry(5.4, 0.18, 12, 48), matCopperCoil));

// ベイパーコーン＆ボウショック
const vaporConeGeo = new THREE.ConeGeometry(7.5, 13.0, 32, 1, true);
const vaporConeMat = new THREE.MeshBasicMaterial({ color: 0xe0f2fe, transparent: true, opacity: 0.0, side: THREE.DoubleSide });
const vaporConeMesh = new THREE.Mesh(vaporConeGeo, vaporConeMat);
vaporConeMesh.rotation.x = -Math.PI / 2;
vaporConeMesh.position.set(0, 0, -1.0);
shipMeshGroup.add(vaporConeMesh);

const bowShockGeo = new THREE.SphereGeometry(3.8, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.5);
const bowShockMat = new THREE.MeshBasicMaterial({ color: 0xef4444, transparent: true, opacity: 0.0, side: THREE.DoubleSide, blending: THREE.AdditiveBlending });
const bowShockMesh = new THREE.Mesh(bowShockGeo, bowShockMat);
bowShockMesh.rotation.x = -Math.PI / 2;
bowShockMesh.position.set(0, 0, 16.5);
shipMeshGroup.add(bowShockMesh);

// 六角形シールド
const shieldMat = new THREE.ShaderMaterial({
    vertexShader: `varying vec3 vNormal; varying vec3 vWorldPos; void main() { vNormal = normalize(normalMatrix * normal); vec4 wp = modelMatrix * vec4(position, 1.0); vWorldPos = wp.xyz; gl_Position = projectionMatrix * viewMatrix * wp; }`,
    fragmentShader: `varying vec3 vNormal; varying vec3 vWorldPos; uniform float uAlpha; uniform float uTime; void main() { float hex = abs(sin(vWorldPos.x * 0.8) * cos(vWorldPos.y * 0.8) * sin(vWorldPos.z * 0.8)); float rim = pow(1.0 - abs(dot(vNormal, vec3(0,0,1))), 3.0); gl_FragColor = vec4(0.22, 0.74, 0.98, (rim + smoothstep(0.2, 0.8, hex) * 0.6) * uAlpha); }`,
    uniforms: { uAlpha: { value: 0.0 }, uTime: { value: 0.0 } },
    transparent: true, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false
});
const hexShieldMesh = new THREE.Mesh(new THREE.SphereGeometry(18.0, 32, 32), shieldMat);
shipMeshGroup.add(hexShieldMesh);

// 推進炎＆ショックダイヤモンド（大気圧膨張連動）
const plumeRoot = new THREE.Group();
plumeRoot.position.set(0, 0, -2.3);
nozzleGimbalRoot.add(plumeRoot);

const flameShaderMat = new THREE.ShaderMaterial({
    vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `varying vec2 vUv; uniform float uTime; uniform vec3 uColor; void main() { float noise = sin(vUv.y * 35.0 - uTime * 28.0) * cos(vUv.x * 20.0 + uTime * 15.0); float core = pow(1.0 - abs(vUv.x - 0.5) * 2.0, 3.0); float taper = pow(1.0 - vUv.y, 1.5); gl_FragColor = vec4(mix(uColor, vec3(1.0), core * 0.85), clamp((core + noise * 0.25) * taper * 0.9, 0.0, 1.0)); }`,
    uniforms: { uTime: { value: 0.0 }, uColor: { value: new THREE.Color(cfg.flame_hex) } },
    transparent: true, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false
});
const jetCylinder = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 4.8, 44.0, 32, 1, true), flameShaderMat);
jetCylinder.rotation.x = Math.PI / 2;
jetCylinder.position.z = -22.0;
plumeRoot.add(jetCylinder);

const shockBarrels = [];
for (let d = 0; d < cfg.shock_count; d++) {
    const sb = new THREE.Mesh(
        new THREE.SphereGeometry(1.5 - d * 0.16, 16, 16),
        new THREE.MeshBasicMaterial({ color: cfg.spark_hex, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending })
    );
    sb.scale.set(1.0, 1.0, 2.2);
    sb.position.set(0, 0, -3.5 - d * 5.4);
    plumeRoot.add(sb);
    shockBarrels.push(sb);
}

// =========================================================================
// 5. 3層パララックス・ワープトンネル＆近景スペースダスト
// =========================================================================
const warpGroup = new THREE.Group();
warpGroup.scale.setScalar(0.0001);
scene.add(warpGroup);

for (let r = 0; r < 12; r++) {
    const rPts = [];
    const baseOffset = (r / 12) * Math.PI * 2;
    for (let z = -280; z <= 280; z += 14) {
        rPts.push(new THREE.Vector3(Math.cos((z * 0.04) + baseOffset) * 22.0, Math.sin((z * 0.04) + baseOffset) * 22.0, z));
    }
    warpGroup.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(rPts), 64, 0.55, 8, false), new THREE.MeshBasicMaterial({ color: (r % 2 === 0) ? cfg.aurora_hex : 0x38bdf8, transparent: true, opacity: 0.88, blending: THREE.AdditiveBlending, fog: false })));
}

const starCount = 3500;
const starGeo = new THREE.BufferGeometry();
const starPos = new Float32Array(starCount * 6);
const starCol = new Float32Array(starCount * 6);
for (let i = 0; i < starCount; i++) {
    const ang = Math.random() * Math.PI * 2, rad = 25.0 + Math.random() * 220.0, z = (Math.random() - 0.5) * 600.0;
    starPos[i * 6] = Math.cos(ang) * rad; starPos[i * 6 + 1] = Math.sin(ang) * rad; starPos[i * 6 + 2] = z;
    starPos[i * 6 + 3] = starPos[i * 6]; starPos[i * 6 + 4] = starPos[i * 6 + 1]; starPos[i * 6 + 5] = z + 1.0;
    starCol[i * 6] = 0.35; starCol[i * 6 + 1] = 0.85; starCol[i * 6 + 2] = 1.0;
    starCol[i * 6 + 3] = 0.95; starCol[i * 6 + 4] = 0.15; starCol[i * 6 + 5] = 0.45;
}
starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
starGeo.setAttribute('color', new THREE.BufferAttribute(starCol, 3));
warpGroup.add(new THREE.LineSegments(starGeo, new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.92, blending: THREE.AdditiveBlending, fog: false })));

const dustCount = 800;
const dustGeo = new THREE.BufferGeometry();
const dustPos = new Float32Array(dustCount * 6);
for (let i = 0; i < dustCount; i++) {
    const rx = (Math.random() - 0.5) * 55.0, ry = (Math.random() - 0.5) * 35.0, rz = (Math.random() - 0.5) * 260.0;
    dustPos[i * 6] = rx; dustPos[i * 6 + 1] = ry; dustPos[i * 6 + 2] = rz;
    dustPos[i * 6 + 3] = rx; dustPos[i * 6 + 4] = ry; dustPos[i * 6 + 5] = rz - 3.0;
}
dustGeo.setAttribute('position', new THREE.BufferAttribute(dustPos, 3));
scene.add(new THREE.LineSegments(dustGeo, new THREE.LineBasicMaterial({ color: 0x93c5fd, transparent: true, opacity: 0.25, blending: THREE.AdditiveBlending, fog: false })));

// =========================================================================
// 6. 相模湾メガフロート射場＆Gerstner波浪海面＆実写NASA地球
// =========================================================================
const catapultSlopeRoot = new THREE.Group();
catapultSlopeRoot.rotation.x = -radAngle;
scene.add(catapultSlopeRoot);

const railMover = new THREE.Group();
catapultSlopeRoot.add(railMover);

// カタパルトレール主桁（z=0から前方にのみ伸ばし機体後方・視線を完全にクリア）
const mainGirder = new THREE.Mesh(new THREE.BoxGeometry(12.0, 1.5, 3600), matDarkAlloy);
mainGirder.position.set(0, -3.5, 1800);
mainGirder.receiveShadow = true;
railMover.add(mainGirder);

// カタパルトアーチ（機体より前方 z >= 25 のみに配置し見切れ解消）
const dummyArch = new THREE.Object3D();
const archInst = new THREE.InstancedMesh(new THREE.TorusGeometry(8.5, 0.35, 10, 24, Math.PI), matTitaniumFrame, 180);
for (let i = 0; i < 180; i++) {
    dummyArch.position.set(0, -2.6, i * 20.0 + 25.0); dummyArch.updateMatrix(); archInst.setMatrixAt(i, dummyArch.matrix);
}
railMover.add(archInst);

const groundEnvMover = new THREE.Group();
scene.add(groundEnvMover);

// Gerstner波浪海面
const oceanShaderMat = new THREE.ShaderMaterial({
    vertexShader: `
        varying vec2 vUv; varying vec3 vWorldPos; varying vec3 vNormal; uniform float uTime;
        vec3 gerstnerWaveXZ(vec4 wave, vec3 p, inout vec3 tangent, inout vec3 binormal) {
            float steepness = wave.z; float wavelength = wave.w;
            float k = 2.0 * 3.14159 / wavelength; float c = sqrt(9.8 / k);
            vec2 d = normalize(wave.xy); float f = k * (dot(d, p.xz) - c * uTime * 0.45); float a = steepness / k;
            tangent += vec3(-d.x * d.x * (steepness * sin(f)), d.x * (steepness * cos(f)), -d.x * d.y * (steepness * sin(f)));
            binormal += vec3(-d.x * d.y * (steepness * sin(f)), d.y * (steepness * cos(f)), -d.y * d.y * (steepness * sin(f)));
            return vec3(d.x * (a * cos(f)), a * sin(f), d.y * (a * cos(f)));
        }
        void main() {
            vUv = uv * 350.0; vec3 p = position; vec3 tangent = vec3(1.0, 0.0, 0.0); vec3 binormal = vec3(0.0, 0.0, 1.0);
            p += gerstnerWaveXZ(vec4(1.0, 0.3, 0.22, 90.0), position, tangent, binormal);
            p += gerstnerWaveXZ(vec4(0.4, 0.9, 0.14, 45.0), position, tangent, binormal);
            p += gerstnerWaveXZ(vec4(-0.6, 0.7, 0.09, 22.0), position, tangent, binormal);
            vNormal = normalize(cross(binormal, tangent));
            vec4 worldP = modelMatrix * vec4(p, 1.0); vWorldPos = worldP.xyz;
            gl_Position = projectionMatrix * viewMatrix * worldP;
        }
    `,
    fragmentShader: `
        varying vec2 vUv; varying vec3 vWorldPos; varying vec3 vNormal; uniform vec3 uSunDir; uniform vec3 uSunColor; uniform float uTime; uniform float uOpacity;
        void main() {
            vec3 viewDir = normalize(cameraPosition - vWorldPos);
            float micro = sin(vUv.x * 2.5 + uTime * 2.0) * cos(vUv.y * 2.5 - uTime * 1.5) * 0.08;
            vec3 n = normalize(vNormal + vec3(micro, 0.0, micro));
            float fresnel = pow(1.0 - max(0.0, dot(n, viewDir)), 4.0);
            vec3 deepWater = vec3(0.012, 0.038, 0.082); vec3 skyReflect = vec3(0.35, 0.65, 0.98);
            vec3 halfVec = normalize(uSunDir + viewDir); float spec = pow(max(0.0, dot(n, halfVec)), 160.0) * 4.5;
            gl_FragColor = vec4(mix(deepWater, skyReflect, fresnel) + uSunColor * spec, uOpacity);
        }
    `,
    uniforms: {
        uTime: { value: 0.0 },
        uSunDir: { value: new THREE.Vector3().fromArray(cfg.env.sun_pos).normalize() },
        uSunColor: { value: new THREE.Color(cfg.env.sun_color) },
        uOpacity: { value: 0.96 }
    },
    transparent: true
});
const seaMesh = new THREE.Mesh(new THREE.PlaneGeometry(350000, 350000, 96, 96), oceanShaderMat);
seaMesh.rotation.x = -Math.PI / 2;
seaMesh.position.y = -45.0;
groundEnvMover.add(seaMesh);

const islandBase = new THREE.Mesh(new THREE.BoxGeometry(220, 28, 3800), matDarkAlloy);
islandBase.position.set(0, -42, 1800);
islandBase.receiveShadow = true;
groundEnvMover.add(islandBase);

const craneMat = new THREE.MeshStandardMaterial({ color: 0xef4444, metalness: 0.85, roughness: 0.25 });
for (let cr = 0; cr < 8; cr++) {
    const s = (cr % 2 === 0) ? 1 : -1; const cz = cr * 380.0 + 150.0;
    const cTower = new THREE.Mesh(new THREE.BoxGeometry(4.0, 95.0, 4.0), craneMat);
    cTower.position.set(s * 75.0, 25.0, cz); groundEnvMover.add(cTower);
    const cArm = new THREE.Mesh(new THREE.BoxGeometry(32.0, 3.5, 4.0), craneMat);
    cArm.position.set(s * 62.0, 72.0, cz); groundEnvMover.add(cArm);
}

const fujiMount = new THREE.Mesh(new THREE.ConeGeometry(12500, 3776, 64), new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.85 }));
fujiMount.position.set(5500, 1800, 16500);
groundEnvMover.add(fujiMount);

const beamGeo = new THREE.CylinderGeometry(0.5, 32.0, 750, 16, 1, true);
const beamMat = new THREE.MeshBasicMaterial({ color: cfg.env.sun_color, transparent: true, opacity: 0.16, blending: THREE.AdditiveBlending, side: THREE.DoubleSide });
for (let b = 0; b < 8; b++) {
    const s = (b % 2 === 0) ? 1 : -1;
    const beam = new THREE.Mesh(beamGeo, beamMat);
    beam.position.set(s * 85.0, 320.0, b * 380.0);
    beam.rotation.z = s * 0.28;
    groundEnvMover.add(beam);
}

// 散水煙（ノズル後方にのみ小径球体を配置し機体見切れを完全解消）
const delugePuffs = [];
const delugeMat = new THREE.MeshBasicMaterial({ color: 0xdbeafe, transparent: true, opacity: 0.0 });
for (let p = 0; p < 8; p++) {
    const puff = new THREE.Mesh(new THREE.SphereGeometry(3.5, 12, 12), delugeMat);
    puff.position.set((Math.random() - 0.5) * 12.0, -4.5, -16.0 - p * 6.0);
    groundEnvMover.add(puff);
    delugePuffs.push(puff);
}

// 実写NASA Blue Marble テクスチャによる本物の地球
const earthGroup = new THREE.Group();
earthGroup.position.set(0, -60045, 15000);
scene.add(earthGroup);

const realEarthMesh = new THREE.Mesh(
    new THREE.SphereGeometry(60000, 64, 64),
    new THREE.MeshStandardMaterial({
        map: earthDayTex,
        roughness: 0.75,
        metalness: 0.1
    })
);
earthGroup.add(realEarthMesh);

const realCloudsMesh = new THREE.Mesh(
    new THREE.SphereGeometry(60250, 64, 64),
    new THREE.MeshStandardMaterial({
        map: earthCloudsTex,
        transparent: true,
        opacity: 0.75,
        blending: THREE.AdditiveBlending
    })
);
earthGroup.add(realCloudsMesh);

// 宇宙空間用大気リムグロー
const atmoGlowMesh = new THREE.Mesh(
    new THREE.SphereGeometry(60800, 64, 64),
    new THREE.ShaderMaterial({
        vertexShader: `varying vec3 vNormal; void main() { vNormal = normalize(normalMatrix * normal); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
        fragmentShader: `varying vec3 vNormal; void main() { float intensity = pow(0.7 - dot(vNormal, vec3(0, 0, 1.0)), 2.5); gl_FragColor = vec4(0.28, 0.65, 1.0, 1.0) * intensity; }`,
        side: THREE.BackSide, blending: THREE.AdditiveBlending, transparent: true
    })
);
earthGroup.add(atmoGlowMesh);

// =========================================================================
// 7. 実写クレーター地表・巨大未来都市コロニー・16km無限滑走路
// =========================================================================
const destWorld = new THREE.Group();
destWorld.visible = false;
scene.add(destWorld);

// 目標惑星本体（実写真・非発光低反射PBR）
const destPlanet = new THREE.Mesh(
    new THREE.SphereGeometry(4500, 64, 64),
    new THREE.MeshStandardMaterial({
        map: moonCraterTex,
        color: new THREE.Color(cfg.dest_color),
        roughness: 0.9,
        metalness: 0.1
    })
);
destPlanet.position.set(0, -4500, 0);
destWorld.add(destPlanet);

if (cfg.dest_type === "saturn") {
    const ringGeo = new THREE.RingGeometry(5200, 8500, 64);
    const ringMat = new THREE.MeshStandardMaterial({ color: new THREE.Color(cfg.dest_band), side: THREE.DoubleSide, transparent: true, opacity: 0.75 });
    const planetRing = new THREE.Mesh(ringGeo, ringMat);
    planetRing.rotation.x = Math.PI / 2.3;
    planetRing.position.copy(destPlanet.position);
    destWorld.add(planetRing);
}

// 実写クレーターバンプ付き山岳地形（滑走路周辺 |tx| < 1400 は完全フラット）
const terrainGeo = new THREE.PlaneGeometry(90000, 90000, 64, 64);
const terrainPos = terrainGeo.attributes.position.array;
for (let i = 0; i < terrainPos.length; i += 3) {
    const tx = terrainPos[i], ty = terrainPos[i+1];
    const rawElevation = Math.sin(tx * 0.001) * Math.cos(ty * 0.001) * 320.0 + Math.sin(tx * 0.003) * 70.0;
    const flatFactor = THREE.MathUtils.clamp((Math.abs(tx) - 400.0) / 1000.0, 0.0, 1.0);
    terrainPos[i+2] = rawElevation * flatFactor;
}
terrainGeo.computeVertexNormals();
const terrainMesh = new THREE.Mesh(terrainGeo, new THREE.MeshStandardMaterial({
    map: moonCraterTex,
    color: new THREE.Color(cfg.dest_band),
    roughness: 0.95,
    metalness: 0.1
}));
terrainMesh.rotation.x = -Math.PI / 2;
terrainMesh.position.y = -3.2;
destWorld.add(terrainMesh);

// 16,000m 無限滑走路＆未来都市コロニー
const runwayScrollGroup = new THREE.Group();
destWorld.add(runwayScrollGroup);

const runwayMesh = new THREE.Mesh(new THREE.BoxGeometry(70.0, 0.4, 16000.0), new THREE.MeshStandardMaterial({ color: 0x111827, roughness: 0.85 }));
runwayMesh.position.set(0, -3.0, 6000.0);
runwayMesh.receiveShadow = true;
runwayScrollGroup.add(runwayMesh);

const centerLineMesh = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 15800.0), new THREE.MeshBasicMaterial({ color: 0xf8fafc }));
centerLineMesh.rotation.x = -Math.PI / 2;
centerLineMesh.position.set(0, -2.78, 6000.0);
runwayScrollGroup.add(centerLineMesh);

// 滑走路両脇の未来都市コロニー＆発光管制塔（滑走路上には絶対出ない |x| > 120m）
const colonyTowerMat = new THREE.MeshStandardMaterial({ color: 0x334155, metalness: 0.85, roughness: 0.25 });
for (let b = 0; b < 24; b++) {
    const s = (b % 2 === 0) ? -1 : 1;
    const bz = -1800.0 + b * 550.0;
    const bHeight = 80.0 + (b % 4) * 45.0;
    const tower = new THREE.Mesh(new THREE.BoxGeometry(35.0, bHeight, 45.0), colonyTowerMat);
    tower.position.set(s * 150.0, bHeight * 0.5 - 3.0, bz);
    runwayScrollGroup.add(tower);

    // 窓明かりエミッシブライン
    const windowStrip = new THREE.Mesh(new THREE.BoxGeometry(35.4, 1.5, 45.4), new THREE.MeshBasicMaterial({ color: 0x38bdf8 }));
    windowStrip.position.set(s * 150.0, bHeight * 0.7 - 3.0, bz);
    runwayScrollGroup.add(windowStrip);
}

// 誘導灯＆ラビットライト
const dummyLight = new THREE.Object3D();
const approachLightsInst = new THREE.InstancedMesh(new THREE.SphereGeometry(0.65, 8, 8), new THREE.MeshBasicMaterial({ color: 0x10b981 }), 160);
for (let al = 0; al < 80; al++) {
    const lz = -2200.0 - al * 30.0;
    dummyLight.position.set(-32.0, -2.6, lz); dummyLight.updateMatrix(); approachLightsInst.setMatrixAt(al * 2, dummyLight.matrix);
    dummyLight.position.set(32.0, -2.6, lz); dummyLight.updateMatrix(); approachLightsInst.setMatrixAt(al * 2 + 1, dummyLight.matrix);
}
runwayScrollGroup.add(approachLightsInst);

const rabbitStrobeMesh = new THREE.Mesh(new THREE.SphereGeometry(1.6, 12, 12), new THREE.MeshBasicMaterial({ color: 0xffffff, blending: THREE.AdditiveBlending }));
rabbitStrobeMesh.position.set(0, -2.2, -2200.0);
runwayScrollGroup.add(rabbitStrobeMesh);

// =========================================================================
// 8. 再生コントローラー
// =========================================================================
let isPlaying = true;
let playbackSpeed = 1.0;
let currentTime = -5.0;
let lastTimestamp = performance.now();

const playPauseBtn = document.getElementById('play-pause-btn');
const speed02Btn = document.getElementById('speed-02');
const speed10Btn = document.getElementById('speed-10');
const speed20Btn = document.getElementById('speed-20');
const timelineSlider = document.getElementById('timeline-slider');

playPauseBtn.addEventListener('click', () => {
    isPlaying = !isPlaying;
    playPauseBtn.innerText = isPlaying ? "PAUSE" : "PLAY";
    controls.enabled = !isPlaying;
});

function setSpeed(speed, btn) {
    playbackSpeed = speed;
    [speed02Btn, speed10Btn, speed20Btn].forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
}
speed02Btn.addEventListener('click', () => setSpeed(0.2, speed02Btn));
speed10Btn.addEventListener('click', () => setSpeed(1.0, speed10Btn));
speed20Btn.addEventListener('click', () => setSpeed(2.0, speed20Btn));

timelineSlider.addEventListener('input', (e) => {
    currentTime = -5.0 + (parseFloat(e.target.value) / 100.0) * (frames[frames.length - 1].t - (-5.0));
});

// =========================================================================
// 9. 軌道レーダー
// =========================================================================
function drawRadar(prog, vc, mach, altKm) {
    const rw = radarCanvas.width, rh = radarCanvas.height;
    rCtx.clearRect(0, 0, rw, rh);
    const isSolar = (prog >= 0.16 && prog < 0.80);
    radarLabelEl.innerHTML = isSolar ? `TACTICAL RADAR<br><span style="color:#10b981;font-size:8px;">INTERPLANETARY SCALE</span>` : `TACTICAL RADAR<br><span style="color:#38bdf8;font-size:8px;">RUNWAY ILS APPROACH</span>`;
    const leftX = 75, rightX = rw - 85, midY = rh / 2;
    rCtx.strokeStyle = 'rgba(56,189,248,0.3)'; rCtx.lineWidth = 3;
    rCtx.beginPath(); rCtx.moveTo(leftX, midY); rCtx.lineTo(rightX, midY); rCtx.stroke();
    rCtx.textAlign = "center";
    if (!isSolar) {
        [{ x: leftX, lbl: "EARTH" }, { x: leftX + (rightX - leftX) * 0.5, lbl: "ORBIT" }, { x: rightX, lbl: "RUNWAY 04L" }].forEach(m => {
            rCtx.fillStyle = '#38bdf8'; rCtx.beginPath(); rCtx.arc(m.x, midY, 4, 0, Math.PI * 2); rCtx.fill();
            rCtx.font = 'bold 10px monospace'; rCtx.fillStyle = '#f8fafc'; rCtx.fillText(m.lbl, m.x, midY - 14);
        });
        const curX = leftX + THREE.MathUtils.clamp(prog, 0.0, 1.0) * (rightX - leftX);
        rCtx.fillStyle = '#f43f5e'; rCtx.beginPath(); rCtx.arc(curX, midY, 6, 0, Math.PI * 2); rCtx.fill();
    } else {
        const curX = leftX + ((prog - 0.16) / 0.64) * (rightX - leftX);
        rCtx.fillStyle = '#10b981'; rCtx.beginPath(); rCtx.arc(curX, midY, 7, 0, Math.PI * 2); rCtx.fill();
    }
}

// =========================================================================
// 10. 60fps アニメーションループ（全修正＆物理光学シネマ制御）
// =========================================================================
const cameraIdealPos = new THREE.Vector3();
const cameraLookTarget = new THREE.Vector3();
const shipWorldPos = new THREE.Vector3();
let announcedAltitudes = {};
let runwayAccumZ = 0.0;
const completeBannerEl = document.getElementById('complete-banner');

function animate(now) {
    requestAnimationFrame(animate);

    const delta = (now - lastTimestamp) / 1000.0;
    lastTimestamp = now;

    if (isPlaying && !cfg.is_preview) {
        currentTime += delta * playbackSpeed;
        const maxT = frames[frames.length - 1].t;
        if (currentTime > maxT) currentTime = maxT;
        timelineSlider.value = ((currentTime - (-5.0)) / (maxT - (-5.0))) * 100.0;
    }

    let idx = 0;
    while (idx < frames.length - 1 && frames[idx + 1].t <= currentTime) idx++;
    const f0 = frames[idx];
    const f1 = frames[Math.min(frames.length - 1, idx + 1)];
    const dtFrame = f1.t - f0.t;
    const alpha = dtFrame > 0.0001 ? THREE.MathUtils.clamp((currentTime - f0.t) / dtFrame, 0.0, 1.0) : 0.0;
    const L = (k) => THREE.MathUtils.lerp(f0[k], f1[k], alpha);

    const distM = L('dist_m'), altKm = L('alt_km'), mach = L('mach'), vc = L('vc');
    const pitchDeg = L('pitch_deg'), yawDeg = L('yaw_deg'), rollDeg = L('roll_deg');
    const vib = L('vib'), prog = L('progress'), tempK = L('temp_k'), gLoad = L('g');
    const engPwr = L('engine_power'), rcsBurst = L('rcs_burst'), pAlpha = L('plasma_alpha');
    const wCharge = L('warp_charge'), wAct = L('warp_active'), wBoom = L('warp_boom');
    const gearD = L('gear_deploy'), speedbrake = L('speedbrake'), ringL = L('ring_lift'), bayO = L('bay_open');
    const chuteD = L('chute_deploy'), runwaySpd = L('runway_speed'), tdSmoke = L('touchdown_smoke');
    const vaporA = L('vapor_alpha');

    // 音声コールアウト
    if (f0.phase !== lastAnnouncedPhase) {
        lastAnnouncedPhase = f0.phase;
        if (f0.phase === "CATAPULT_RAIL_ACCEL") speakCallout("Magnetic catapult engaged. Maximum acceleration.");
        else if (f0.phase === "STRATOSPHERE_CLIMB") speakCallout("Approaching Max Q. Clearing upper stratosphere.");
        else if (f0.phase === "WARP_FIELD_COMPRESSION") speakCallout("Spooling warp coils. Spacetime compression active.");
        else if (f0.phase === "ALCUBIERRE_HYPER_WARP") speakCallout("Hyper warp engaged. Approaching light speed.");
        else if (f0.phase === "DEBRIS_AERO_BRAKING") speakCallout("Warp disengaged. Forward airbrakes and shields online.");
        else if (f0.phase === "ATMOSPHERIC_ENTRY_GLIDESLOPE") speakCallout("Entering destination atmosphere. Intercepting ILS glideslope.");
        else if (f0.phase === "FINAL_APPROACH_FLARE") speakCallout("Minimums. Runway in sight. Flare.");
        else if (f0.phase === "TOUCHDOWN_ROLLOUT_STOP") speakCallout("Touchdown! Drag chute deployed. Reversing thrust.");
        else if (f0.phase === "PLANETARY_RUNWAY_SECURED") speakCallout("All systems secure. Welcome to the outpost.");
    }

    // ILS高度カウントダウン
    if (f0.phase.includes("APPROACH") || f0.phase.includes("FLARE")) {
        ilsHudEl.style.display = 'flex';
        document.getElementById('ils-dist').innerText = `ALT: ${(altKm * 1000).toFixed(0)} M`;
        const altM = altKm * 1000;
        [500, 200, 100, 50, 30].forEach(a => {
            if (altM <= a && !announcedAltitudes[a]) {
                announcedAltitudes[a] = true;
                speakCallout(`${a}`);
            }
        });
    } else {
        ilsHudEl.style.display = 'none';
        announcedAltitudes = {};
    }

    // 宇宙空間でフォグ消滅
    const spaceFade = THREE.MathUtils.clamp((altKm - 15.0) / 65.0, 0.0, 1.0);
    atmoSkyMat.uniforms.uSpaceFade.value = spaceFade;
    spaceFieldGroup.visible = (spaceFade > 0.05);
    scene.fog.density = cfg.env.fog_density * (1.0 - spaceFade);

    // 実写地球の自転＆雲アニメーション
    realEarthMesh.rotation.y = now * 0.00008;
    realCloudsMesh.rotation.y = now * 0.00012;

    // 航空力学ピッチ姿勢制御
    shipPitchGroup.rotation.set(-THREE.MathUtils.degToRad(pitchDeg), THREE.MathUtils.degToRad(yawDeg), THREE.MathUtils.degToRad(rollDeg));

    // 高周波空力カメラシェイク
    const aeroShake = (mach > 0.5 && altKm < 60.0) ? (Math.sin(now * 0.045) * 0.08 + Math.cos(now * 0.078) * 0.05) * vib : 0.0;
    let suspensionBounce = 0.0;
    if (f0.phase === "TOUCHDOWN_ROLLOUT_STOP") {
        const bouncePhase = ((currentTime - f0.t) / (dtFrame || 1.0)) * 5.0;
        suspensionBounce = Math.sin(bouncePhase * Math.PI) * Math.exp(-bouncePhase * 0.8) * 0.16;
    }
    shipMeshGroup.position.set(
        Math.sin(now * 0.003) * 0.18 + aeroShake,
        Math.cos(now * 0.004) * 0.12 - suspensionBounce,
        Math.sin(now * 0.002) * 0.25
    );

    shipMeshGroup.getWorldPosition(shipWorldPos);

    // 大気圧連動プルーム膨張
    const atmoPressureRatio = THREE.MathUtils.clamp(1.0 - (altKm / 75.0), 0.15, 1.0);
    jetCylinder.scale.set(1.0 + (1.0 - atmoPressureRatio) * 1.8, 1.0 + (1.0 - atmoPressureRatio) * 1.8, 1.0);

    // ダイナミックFOV
    let targetFov = 52.0;
    if (f0.phase === "CATAPULT_RAIL_ACCEL" || f0.phase === "ALCUBIERRE_HYPER_WARP") {
        targetFov = 52.0 + (gLoad / 10.0) * 20.0;
    } else if (f0.phase === "DEBRIS_AERO_BRAKING" || f0.phase === "TOUCHDOWN_ROLLOUT_STOP") {
        targetFov = 46.0;
    }
    cameraMain.fov = THREE.MathUtils.lerp(cameraMain.fov, targetFov, 0.08);
    cameraMain.updateProjectionMatrix();

    // カメラ位置追従制御（着陸滑走時は機体が見えなくならないよう斜め前方に回り込み）
    if (!controls.enabled) {
        if (activeCamMode === 0) {
            if (f0.phase.includes("SECURED") || (f0.phase.includes("STOP") && runwaySpd < 40.0)) {
                // 着陸成功シネマティック・パンニング
                cameraIdealPos.set(shipWorldPos.x - 24.0, shipWorldPos.y + 4.5, shipWorldPos.z + 18.0);
                cameraLookTarget.set(shipWorldPos.x, shipWorldPos.y + 1.2, shipWorldPos.z - 2.0);
            } else {
                cameraIdealPos.set(shipWorldPos.x + baseCamPos.x, shipWorldPos.y + baseCamPos.y, shipWorldPos.z + baseCamPos.z - (engPwr * 8.0));
                cameraLookTarget.set(shipWorldPos.x, shipWorldPos.y + baseTarget.y, shipWorldPos.z + baseTarget.z);
            }
            cameraMain.position.lerp(cameraIdealPos, 0.05);
            cameraMain.lookAt(cameraLookTarget);
        } else if (activeCamMode === 1) {
            cameraIdealPos.set(shipWorldPos.x + baseCamPos.x, shipWorldPos.y + baseCamPos.y, shipWorldPos.z + baseCamPos.z - (engPwr * 8.0));
            cameraLookTarget.set(shipWorldPos.x, shipWorldPos.y + baseTarget.y, shipWorldPos.z + baseTarget.z);
            cameraMain.position.lerp(cameraIdealPos, 0.05);
            cameraMain.lookAt(cameraLookTarget);
        } else if (activeCamMode === 2) {
            cameraMain.position.set(shipWorldPos.x, shipWorldPos.y + 1.2, shipWorldPos.z + 8.0);
            cameraMain.lookAt(shipWorldPos.x, shipWorldPos.y + 1.2, shipWorldPos.z + 100.0);
        } else if (activeCamMode === 3) {
            cameraMain.position.set(shipWorldPos.x - halfSpan - 4.0, shipWorldPos.y + 2.0, shipWorldPos.z - 6.0);
            cameraMain.lookAt(shipWorldPos);
        } else if (activeCamMode === 4) {
            cameraMain.position.set(45.0, 22.0, shipWorldPos.z + 60.0);
            cameraMain.lookAt(shipWorldPos);
        }
    } else {
        controls.update();
    }

    // 地球メガフロート・海面連動
    if (prog === 0.0 && altKm < 110.0) {
        catapultSlopeRoot.visible = true;
        groundEnvMover.visible = true;
        railMover.position.set(0, 0, -distM);
        const actualAltM = altKm * 1000.0 - 40.0;
        groundEnvMover.position.set(0, -actualAltM, -distM * 0.7);
        oceanShaderMat.uniforms.uTime.value = now * 0.001;
        const seaFade = THREE.MathUtils.clamp(1.0 - (altKm - 15.0) / 30.0, 0.0, 1.0);
        oceanShaderMat.uniforms.uOpacity.value = 0.96 * seaFade;
    } else {
        catapultSlopeRoot.visible = false;
        groundEnvMover.visible = false;
    }

    // 実写地球の遠ざかり
    if (altKm >= 20.0 && prog < 0.35) {
        earthGroup.visible = true;
        const warpRecede = Math.pow(Math.max(0, prog - 0.05) * 18.0, 3.0);
        earthGroup.position.set(0, -60045 - altKm * 1000.0 - warpRecede * 35000.0, 15000 - distM * 0.6 - warpRecede * 95000.0);
    } else {
        earthGroup.visible = false;
    }

    // 散水煙
    if (prog === 0.0 && altKm < 4.0 && cfg.cryo_steam) {
        delugeMat.opacity = THREE.MathUtils.clamp(1.0 - (altKm / 3.5), 0.0, 0.35);
    } else {
        delugeMat.opacity = 0.0;
    }

    // ワープリング格納
    if (ringL > 0.01) {
        warpRingAssembly.scale.setScalar(ringL);
        warpRingAssembly.position.y = THREE.MathUtils.lerp(0.0, -0.8, ringL);
        rotorClockwise.rotation.z += 0.03 * ringL;
        rotorCounter.rotation.z -= 0.03 * ringL;
    } else {
        warpRingAssembly.scale.set(0.001, 0.001, 0.001);
    }

    bayDoors.forEach(bd => {
        bd.pivot.rotation.z = -bd.side * bayO * 1.5;
    });

    // ベイパーコーン＆ボウショック
    if (cfg.mach_cone_vfx) {
        if (vaporA > 0.05) {
            vaporConeMat.opacity = vaporA * 0.65;
            vaporConeMesh.scale.set(1.0 + vaporA * 0.5, 1.0 + vaporA * 0.5, 1.0);
        } else {
            vaporConeMat.opacity = 0.0;
        }

        if (pAlpha > 0.05) {
            bowShockMat.opacity = pAlpha * 0.75;
            bowShockMesh.scale.set(1.0 + (1.0 - pAlpha) * 0.4, 1.0 + (1.0 - pAlpha) * 0.4, 1.0 + pAlpha * 0.5);
        } else {
            bowShockMat.opacity = 0.0;
        }
    }

    speedbrakePivot.rotation.x = speedbrake * 0.75;
    elevonMeshes.forEach(em => { em.mesh.rotation.x = Math.sin(now * 0.005) * 0.12 + THREE.MathUtils.degToRad(-pitchDeg * 0.25); });
    irisPaddles.forEach(ip => { ip.rotation.x = -0.35 + L('nozzle_open') * 0.48; });

    landingGears.forEach(lg => { lg.scale.setScalar(Math.max(0.001, gearD)); });

    // 左右白煙
    if (tdSmoke > 0.05) {
        smokeMat.opacity = tdSmoke * 0.45;
        smokePuffsLeft.forEach(p => { p.position.set(-4.5 - Math.random() * 2.0, -2.6, -6.0 - Math.random() * 6.0); });
        smokePuffsRight.forEach(p => { p.position.set(4.5 + Math.random() * 2.0, -2.6, -6.0 - Math.random() * 6.0); });
    } else {
        smokeMat.opacity = 0.0;
    }

    if (chuteD > 0.01) {
        chuteGroup.scale.setScalar(chuteD);
        chuteCanopy.rotation.z += 0.02;
    } else {
        chuteGroup.scale.setScalar(0.001);
    }

    // 目標惑星・緩やかな進入アプローチ＆無限滑走路スクロール
    if (prog > 0.75) {
        destWorld.visible = true;
        const targetAltM = altKm * 1000.0;
        destWorld.position.y = -targetAltM;

        atmoSkyMat.uniforms.uHorizon.value.set(cfg.dest_band);
        atmoSkyMat.uniforms.uZenith.value.set(cfg.dest_color);
        atmoSkyMat.uniforms.uSpaceFade.value = THREE.MathUtils.clamp((altKm - 1.8) / 90.0, 0.0, 1.0);

        const rabbitStep = Math.floor((now * 0.025) % 80);
        rabbitStrobeMesh.position.z = -2200.0 - (79 - rabbitStep) * 30.0;

        // 飛行機通りの連続進入前進スクロール
        if (runwaySpd > 0.1 && isPlaying) {
            runwayAccumZ += runwaySpd * delta;
            runwayScrollGroup.position.z = -(runwayAccumZ % 15000.0);
        }
    } else {
        destWorld.visible = false;
        atmoSkyMat.uniforms.uHorizon.value.set(cfg.env.sky_horizon);
        atmoSkyMat.uniforms.uZenith.value.set(cfg.env.sky_zenith);
    }

    // ワープ高速流動
    warpGroup.scale.setScalar(wAct > 0.05 ? 1.0 : 0.0001);
    if (wAct > 0.05) {
        warpGroup.rotation.z += 0.04;
        const sArr = starGeo.attributes.position.array;
        const stretchLen = 45.0 + vc * 220.0;
        for (let i = 0; i < starCount; i++) {
            let z = sArr[i * 6 + 2] - (25.0 + vc * 65.0);
            if (z < -300.0) z = 300.0;
            sArr[i * 6 + 2] = z; sArr[i * 6 + 5] = z + stretchLen;
        }
        starGeo.attributes.position.needsUpdate = true;
    }

    const speedRatio = THREE.MathUtils.clamp((mach / 30.0) + (vc * 8.0), 0.1, 14.0);
    const dArr = dustGeo.attributes.position.array;
    for (let i = 0; i < dustCount; i++) {
        let z = dArr[i * 6 + 2] - speedRatio * 4.0;
        if (z < -130.0) z = 130.0;
        dArr[i * 6 + 2] = z; dArr[i * 6 + 5] = z - (3.0 + speedRatio * 5.0);
    }
    dustGeo.attributes.position.needsUpdate = true;

    // ポストプロセス更新
    let duckingFactor = 1.0;
    if (f0.phase === "WARP_FIELD_COMPRESSION" && prog > 0.14) {
        filmPass.uniforms.uInvert.value = 1.0;
        duckingFactor = 0.001;
    } else {
        filmPass.uniforms.uInvert.value = 0.0;
    }
    filmPass.uniforms.uDistort.value = wBoom * 2.8 + wAct * 0.35;
    filmPass.uniforms.uTime.value = now * 0.001;

    if (actx) {
        rocketGain.gain.setTargetAtTime(engPwr * 0.35 * duckingFactor, actx.currentTime, 0.05);
        rcsGain.gain.setTargetAtTime(rcsBurst * 0.15 * duckingFactor, actx.currentTime, 0.05);
    }

    drawRadar(prog, vc, mach, altKm);

    renderer.setViewport(0, 0, W, H);
    composerMain.render();

    document.getElementById('ui-phase').innerText = f0.phase;
    document.getElementById('ui-alt').innerText = altKm > 90000 ? "DEEP SPACE" : `${altKm.toFixed(1)} km`;
    document.getElementById('ui-spd').innerText = vc > 0.02 ? `${vc.toFixed(3)} c` : `M ${mach.toFixed(1)}`;
    const sTime = L('t');
    document.getElementById('ui-clock').innerText = sTime < 0 ? `T${sTime.toFixed(1)}s` : `T+${L('ship_time').toFixed(1)}s`;
    document.getElementById('ui-vc').innerText = vc.toFixed(3);
    document.getElementById('ui-temp').innerText = Math.round(tempK);
    document.getElementById('ui-g').innerText = gLoad.toFixed(1);
    const gamma = 1.0 / Math.sqrt(Math.max(0.001, 1.0 - Math.min(0.999, vc) ** 2));
    document.getElementById('ui-gamma').innerText = gamma.toFixed(2);
    document.getElementById('ui-prog').innerText = (prog * 100).toFixed(1);

    if (f0.phase === "PLANETARY_RUNWAY_SECURED" && runwaySpd < 1.0) {
        completeBannerEl.style.display = 'block';
    } else {
        completeBannerEl.style.display = 'none';
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
