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
    "※ 完全映画仕様ディレクターズカット：PMREM IBL / 実写対数曲線富士山＆PBR海面 / 本格5面MFDコクピット同期 / "
    "多層シンセ音＆T-5カウントダウン / 惑星ILSグライドスロープ進入＆バイオドーム都市 / 恒星周回軌道分岐"
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
    "火星 オリンポス軌道テラフォーミング・コロニー": {
        "dist_label": "0.52 AU (78,000,000 km)",
        "goal_type": "landing",
        "type": "mars",
        "color_hex": 0xC2410C,
        "band_hex": 0x7C2D12,
    },
    "土星衛星タイタン メタン海洋メガフロート基地『クロノス』": {
        "dist_label": "9.58 AU (1,433,000,000 km)",
        "goal_type": "landing",
        "type": "saturn",
        "color_hex": 0xE2CCB2,
        "band_hex": 0xB89F80,
    },
    "赤色超巨星ベテルギウス ダイソン・スウォーム採掘軌道": {
        "dist_label": "642.5 光年 (6,078,000,000,000 km)",
        "goal_type": "orbit",
        "type": "star",
        "color_hex": 0xEF4444,
        "band_hex": 0xF97316,
    },
    "超大質量ブラックホール『ガルガンチュア』事象の地平線観測ステーション": {
        "dist_label": "10.00 億光年 (深宇宙特異点)",
        "goal_type": "orbit",
        "type": "blackhole",
        "color_hex": 0x0A0A0A,
        "band_hex": 0x38BDF8,
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
    "🎥 シネマカメラ & 目的宙域 & コクピット",
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
            "外装スクラムジェット補助ブースター×2 (高度55kmで分離パージ)", value=False
        )

with tab2:
    c1, c2 = st.columns(2)
    with c1:
        env_sel = st.selectbox("射場ロケーション＆時間帯", list(LAUNCH_ENVIRONMENTS.keys()))
        env_cfg = LAUNCH_ENVIRONMENTS[env_sel]
        coil_charge = st.slider("リニアカタパルト超伝導励磁出力 (%)", 80, 150, 125, step=5)
        weather_cond = st.selectbox("天候・大気コンディション", ["快晴 (Clear)", "夜間雷雨＆稲妻 (Thunderstorm)", "成層圏オーロラ (Aurora)"])
    with c2:
        st.caption("※ メガフロート人工島・防波堤・サーチライト光柱、実写風富士山稜線・湘南夜景、Gerstner波浪海面を描画。")
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
        dest_sel = st.selectbox("目標宙域", list(DESTINATIONS.keys()))
        dest_cfg = DESTINATIONS[dest_sel]
        st.caption(f"**ゴール形式:** {'🛬 惑星滑走路着陸 (ILS Approach & Touchdown)' if dest_cfg['goal_type'] == 'landing' else '🛰️ 恒星・特異点周回軌道投入 (Orbital Insertion)'}")
        st.caption(f"**航行距離:** {dest_cfg['dist_label']}")
        hud_theme = st.selectbox("コクピットHUDカラー", ["サイバーシアン (Cyan)", "ミリタリーグリーン (Green)", "クリムゾンアンバー (Amber)"])
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
        flare_int = st.slider("アナモルフィック・レンズフレア強度", 0.0, 2.0, 1.2, step=0.1)
        shake_scale = st.slider("カメラシェイク（Gフォース振動）強度 (%)", 0, 200, 100, step=10)
        voice_on = st.checkbox("AIフライトディレクター音声ガイド (Web Speech)", value=True)

# =========================================================================
# 💥 タイムライン物理データ（空力自然AoA・長尺ILS進入・軌道投入対応）
# =========================================================================
def build_timeline(preview_only=False):
    base_pitch = float(env_cfg["angle_deg"])
    is_orbit = (dest_cfg["goal_type"] == "orbit")

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
            "vib": 0.0, "progress": 0.0, "ship_time": 0.0, "goal_mode": dest_cfg["goal_type"]
        }]

    dt = 0.25
    frames = []
    exit_mach = float(vessel_cfg["catapult_mach"] * (coil_charge / 100.0))

    # T-5秒〜0秒: 発射前待機（T-1.8sまではエンジン完全停止、炎非表示）
    for step in range(20):
        t = -5.0 + step * dt
        eng_pre = float(np.clip((t + 1.8) / 1.8, 0.0, 0.7)) if t >= -1.8 else 0.0
        clamp = float(np.clip((t + 0.4) / 0.4, 0.0, 1.0))
        frames.append({
            "t": float(round(t, 2)),
            "phase": "CRYO_VENTING" if t < -3.0 else ("LINEAR_COIL_CHARGE" if t < -1.8 else "MAIN_ENGINE_IGNITION"),
            "dist_m": 0.0, "alt_km": 0.04, "mach": 0.0, "vc": 0.0,
            "g": 1.0 + eng_pre * 0.9, "temp_k": 288.0 + eng_pre * 140.0,
            "clamp_open": clamp, "sabot_purge": 0.0, "fairing_purge": 0.0,
            "gear_deploy": 0.0, "speedbrake": 0.0, "chute_deploy": 0.0, "runway_speed": 0.0, "touchdown_smoke": 0.0,
            "wing_sweep": 0.0, "bay_open": 0.0, "ring_lift": 0.0, "rad_deploy": 0.0,
            "nozzle_open": 0.2 + eng_pre * 0.5, "engine_power": eng_pre,
            "spark_arc": float(np.clip((t + 1.8) / 1.8, 0.0, 0.8)) if t >= -1.8 else 0.0,
            "vapor_alpha": 0.0, "plasma_alpha": 0.0, "warp_charge": 0.0,
            "warp_lens": 0.0, "warp_active": 0.0, "warp_boom": 0.0,
            "rcs_burst": 0.0, "shield_hit": 0.0,
            "pitch_deg": base_pitch, "yaw_deg": 0.0, "roll_deg": 0.0,
            "vib": eng_pre * 0.12, "progress": 0.0, "ship_time": 0.0, "goal_mode": dest_cfg["goal_type"]
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

    total_steps = 560
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
            # レール上ではレール角度そのまま、離脱直後に自然な+2.5度のシャープな迎え角に移行
            if t > 10.5:
                pitch_cur = base_pitch + 2.5 * ((t - 10.5) / 1.5)
            else:
                pitch_cur = base_pitch

        elif alt_km < 95.0 and t < 28.0:
            phase = "STRATOSPHERE_CLIMB" if alt_km < 48.0 else "EXOSPHERE_INSERTION"
            sabot_p = min(1.0, sabot_p + 0.6 * dt)
            mach = min(45.0, mach + 2.2 * dt)
            speed_ms = mach * 340.0
            dist_m += speed_ms * dt * 0.55
            space_f = float(np.clip((alt_km - 10.0) / 85.0, 0.0, 1.0))
            # 空力的にリアルなシャープな迎え角（+3.5度〜+1.5度）
            pitch_cur = 3.5 * (1.0 - space_f * 0.6)
            alt_km += (speed_ms * np.sin(np.radians(16.0)) * dt) / 1000.0
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
            pitch_cur = max(0.0, 2.0 * (1.0 - progress / 0.16))
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
            progress += (0.009 + vc * 0.020) * dt
            roll_deg = np.sin(t * 0.25) * 2.5
            if progress >= 0.66:
                w_boom = 1.0

        elif progress < 0.78:
            phase = "RETRO_BRAKING_TRANSITION"
            alt_km = 99999.0
            pitch_cur = 2.0
            yaw_deg = 0.0
            roll_deg = np.sin(t * 0.8) * 3.0
            speedbrake = 1.0
            bay_o = 0.5
            ring_l = 0.2
            rad_d = 1.0
            wing_sw = 0.3
            eng_pwr = 0.35
            nozzle = 0.5
            vc = max(0.01, vc * 0.92)
            g_load = 3.8
            vib = 0.18
            progress += 0.012 * dt
            shield = float(np.sin(t * 5.0) ** 2) if 0.70 < progress < 0.76 else 0.0

        else:
            # 分岐：着陸ゴール vs 恒星・特異点周回軌道投入ゴール
            if not is_orbit:
                # 🛬 惑星滑走路着陸（約40秒の重厚なILSグライドスロープ進入＆フレア接地）
                if progress < 0.86:
                    phase = "ATMOSPHERIC_ENTRY_DESCENT"
                    p_in = (progress - 0.78) / 0.08
                    alt_km = float(np.clip(120.0 * (1.0 - p_in * 0.85), 18.0, 120.0))
                    mach = float(max(4.0, 22.0 * (1.0 - p_in * 0.75)))
                    vc = 0.0
                    pitch_cur = 2.5 * (1.0 - p_in)
                    roll_deg = np.sin(p_in * np.pi * 3.0) * 5.0
                    plasma = float(np.sin(p_in * np.pi) ** 1.1)
                    g_load = 4.5 * (1.0 - p_in * 0.4)
                    eng_pwr = 0.3
                    nozzle = 0.5
                    bay_o = 0.0
                    ring_l = 0.0
                    rad_d = 0.0
                    wing_sw = 0.2
                    speedbrake = 0.7
                    vib = plasma * 0.45 + 0.12
                    progress += 0.0070 * dt

                elif progress < 0.92:
                    phase = "ILS_GLIDESLOPE_ALIGNMENT"
                    p_ils = (progress - 0.86) / 0.06
                    alt_km = float(np.clip(18.0 * (1.0 - p_ils) + 1.2 * p_ils, 1.2, 18.0))
                    mach = float(max(1.1, 4.0 * (1.0 - p_ils) + 1.1 * p_ils))
                    pitch_cur = -1.5  # 緩やかな3度グライドスロープ角
                    roll_deg = np.sin(p_ils * np.pi * 2.0) * 2.0
                    vapor = float(np.sin(p_ils * np.pi) ** 1.4)
                    g_load = 2.0
                    eng_pwr = 0.25
                    nozzle = 0.4
                    wing_sw = 0.0
                    speedbrake = 0.85
                    vib = 0.10
                    progress += 0.0055 * dt

                elif progress < 0.965:
                    phase = "FINAL_APPROACH_FLARE"
                    p_fl = (progress - 0.92) / 0.045
                    alt_km = float(max(0.0, 1.2 * (1.0 - p_fl)))
                    mach = float(max(0.32, 1.1 * (1.0 - p_fl * 0.75)))
                    pitch_cur = -1.5 * (1.0 - p_fl) + 4.5 * p_fl  # リアルな機首引き起こし（フレア）
                    roll_deg = 0.0
                    gear_d = float(np.clip(p_fl * 2.5, 0.0, 1.0))
                    speedbrake = 1.0
                    runway_spd = 145.0 * (1.0 - p_fl * 0.1)
                    g_load = 1.3
                    eng_pwr = 0.12
                    nozzle = 0.25
                    vib = 0.07
                    progress += 0.0050 * dt

                else:
                    phase = "TOUCHDOWN_ROLLOUT_STOP"
                    p_ro = (progress - 0.965) / 0.035
                    alt_km = 0.0
                    mach = float(max(0.0, 0.32 * (1.0 - p_ro)))
                    pitch_cur = max(0.0, 4.5 * (1.0 - p_ro * 2.0))
                    roll_deg = 0.0
                    gear_d = 1.0
                    speedbrake = 1.0
                    chute_d = float(np.clip(p_ro * 3.5, 0.0, 1.0))
                    runway_spd = float(max(0.0, 130.0 * (1.0 - p_ro)))
                    td_smoke = float(np.clip((1.0 - p_ro) * 2.2, 0.0, 1.0))
                    g_load = 1.0 + float(np.sin(p_ro * np.pi)) * 0.5
                    eng_pwr = 0.0
                    nozzle = 0.2
                    vib = 0.16 * (1.0 - p_ro)
                    progress = min(1.0, progress + 0.0040 * dt)
            else:
                # 🛰️ 恒星・特異点周回軌道投入
                if progress < 0.88:
                    phase = "LAGRANGE_INSERTION_BURN"
                    p_in = (progress - 0.78) / 0.10
                    alt_km = 99999.0
                    mach = 0.0
                    vc = max(0.001, 0.015 * (1.0 - p_in))
                    pitch_cur = 4.0 * np.sin(p_in * np.pi)
                    roll_deg = p_in * 12.0
                    eng_pwr = 0.85
                    nozzle = 0.9
                    bay_o = 0.0
                    ring_l = 0.0
                    rad_d = 1.0
                    wing_sw = 0.5
                    rcs = 0.6
                    g_load = 2.4
                    vib = 0.12
                    progress += 0.0065 * dt

                elif progress < 0.95:
                    phase = "DYSON_SWARM_APPROACH"
                    p_ap = (progress - 0.88) / 0.07
                    alt_km = 99999.0
                    mach = 0.0
                    vc = 0.001 * (1.0 - p_ap)
                    pitch_cur = 1.0
                    roll_deg = 3.0 * (1.0 - p_ap)
                    eng_pwr = 0.2
                    nozzle = 0.3
                    rad_d = 1.0
                    rcs = 0.4
                    g_load = 1.1
                    vib = 0.05
                    progress += 0.0055 * dt

                else:
                    phase = "STABLE_ORBIT_LOCKED"
                    alt_km = 99999.0
                    mach = 0.0
                    vc = 0.0
                    pitch_cur = 0.0
                    roll_deg = 0.0
                    eng_pwr = 0.0
                    nozzle = 0.2
                    rad_d = 1.0
                    rcs = 0.0
                    g_load = 1.0
                    vib = 0.01
                    progress = min(1.0, progress + 0.0045 * dt)

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
            "vib": float(vib), "progress": float(progress), "ship_time": float(ship_time), "goal_mode": dest_cfg["goal_type"]
        })

        if progress >= 1.0:
            terminal_phase = "PLANETARY_RUNWAY_SECURED" if not is_orbit else "ORBITAL_STATION_DOCKED"
            for extra in range(35):
                frames.append({
                    "t": float(round(t + (extra + 1) * dt, 2)), "phase": terminal_phase,
                    "dist_m": float(dist_m), "alt_km": 0.0 if not is_orbit else 99999.0,
                    "mach": 0.0, "vc": 0.0, "g": 1.0, "temp_k": 305.0, "clamp_open": 1.0, "sabot_purge": 1.0,
                    "fairing_purge": float(fairing_p), "gear_deploy": 1.0 if not is_orbit else 0.0,
                    "speedbrake": 1.0 if not is_orbit else 0.0, "chute_deploy": 1.0 if not is_orbit else 0.0,
                    "runway_speed": 0.0, "touchdown_smoke": 0.0, "wing_sweep": 0.0,
                    "bay_open": 0.0, "ring_lift": 0.0, "rad_deploy": 1.0, "nozzle_open": 0.2,
                    "engine_power": 0.0, "spark_arc": 0.0, "vapor_alpha": 0.0, "plasma_alpha": 0.0,
                    "warp_charge": 0.0, "warp_lens": 0.0, "warp_active": 0.0, "warp_boom": 0.0,
                    "rcs_burst": 0.0, "shield_hit": 0.0,
                    "pitch_deg": 0.0, "yaw_deg": 0.0, "roll_deg": 0.0,
                    "vib": 0.0, "progress": 1.0, "ship_time": float(ship_time), "goal_mode": dest_cfg["goal_type"]
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
    "goal_type": dest_cfg["goal_type"],
    "dest_color": f"#{dest_cfg['color_hex']:06x}" if isinstance(dest_cfg["color_hex"], int) else str(dest_cfg["color_hex"]),
    "dest_band": f"#{dest_cfg['band_hex']:06x}" if isinstance(dest_cfg["band_hex"], int) else str(dest_cfg["band_hex"]),
    "cam_preset": cam_preset,
    "env": env_cfg,
    "weather": weather_cond,
    "hud_theme": hud_theme,
    "flare_int": flare_int,
    "shake_scale": shake_scale / 100.0,
    "voice_on": voice_on,
}

# =========================================================================
# 📺 Three.js 完全映画仕様・全修正＆実写VFX統合版
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
  z-index:1;touch-action:pan-y;
}
.letterbox-top{position:absolute;top:0;left:0;width:100%;height:12px;background:#000;z-index:90;pointer-events:none;}
.letterbox-bottom{position:absolute;bottom:0;left:0;width:100%;height:12px;background:#000;z-index:90;pointer-events:none;}

/* 上部UI統合スタック */
.hud-header-container{
  position:absolute;top:12px;left:0;width:100%;
  display:flex;flex-direction:column;z-index:50;pointer-events:auto;
}
.hud-top-bar{
  background:linear-gradient(180deg,rgba(2,6,18,0.95) 0%,rgba(4,12,28,0.85) 100%);
  border-bottom:1px solid rgba(56,189,248,0.3);
  display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;
  padding:6px 18px;gap:8px;box-shadow:0 4px 25px rgba(0,0,0,0.85);
}
.hud-left{display:flex;flex-wrap:wrap;align-items:center;gap:12px;font-size:11px;}
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
  background:rgba(2,6,23,0.82);border-bottom:1px solid rgba(16,185,129,0.3);
  padding:4px 20px;font-size:10.5px;font-family:monospace;color:#6ee7b7;letter-spacing:1px;
  pointer-events:none;display:flex;align-items:center;gap:8px;
}

/* 映画仕様 T-5 カウントダウン HUD */
#countdown-overlay{
  position:absolute;top:40%;left:50%;transform:translate(-50%,-50%);
  font-family:monospace;font-size:68px;font-weight:900;letter-spacing:6px;
  color:#38bdf8;text-shadow:0 0 35px rgba(56,189,248,0.85);
  pointer-events:none;z-index:60;display:none;text-align:center;
}

#ils-hud{
  position:absolute;top:48%;left:50%;transform:translate(-50%,-50%);
  width:320px;height:200px;border:1px dashed rgba(16,185,129,0.5);border-radius:6px;
  pointer-events:none;z-index:35;display:none;flex-direction:column;justify-content:space-between;
  padding:10px 14px;font-family:monospace;color:#10b981;font-size:11px;
  background:rgba(2,6,23,0.35);backdrop-filter:blur(2px);
}
.ils-cross{position:absolute;top:50%;left:50%;width:90px;height:90px;transform:translate(-50%,-50%);pointer-events:none;}
.ils-cross::before{content:'';position:absolute;top:50%;left:0;width:100%;height:1px;background:#10b981;}
.ils-cross::after{content:'';position:absolute;top:0;left:50%;width:1px;height:100%;background:#10b981;}

.playback-controller{
  position:absolute;bottom:148px;left:20px;right:20px;
  display:flex;align-items:center;gap:12px;background:rgba(2,6,23,0.85);
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
  position:absolute;bottom:12px;left:0;width:100%;height:54px;
  background:linear-gradient(0deg,rgba(2,6,18,0.94) 0%,rgba(6,13,30,0.82) 100%);
  border-top:1px solid rgba(148,163,184,0.2);display:grid;grid-template-columns:repeat(5,1fr);align-items:center;
  padding:0 20px;z-index:20;pointer-events:none;
}
.metric{display:flex;flex-direction:column;border-left:2px solid rgba(56,189,248,0.35);padding-left:10px;}
.metric-lbl{font-size:8.5px;color:#94a3b8;letter-spacing:1.1px;}
.metric-val{font-size:15px;font-weight:900;color:#f8fafc;margin-top:1px;}

#complete-banner{
  display:none;position:absolute;top:200px;left:50%;transform:translateX(-50%);
  background:rgba(6,78,59,0.95);border:2px solid #10b981;
  padding:18px 40px;border-radius:8px;text-align:center;z-index:70;
  box-shadow:0 0 60px rgba(16,185,129,0.7);pointer-events:none;
}
</style>
</head>
<body>
<div class="letterbox-top"></div>
<div class="letterbox-bottom"></div>
<canvas id="webgl-canvas"></canvas>

<div class="hud-header-container">
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
</div>

<div id="countdown-overlay">T-05</div>

<div id="ils-hud">
  <div style="display:flex;justify-content:space-between;">
    <span id="ils-title">ILS RUNWAY 04L</span>
    <span>GS: 3.0° LOCKED</span>
  </div>
  <div class="ils-cross"></div>
  <div style="display:flex;justify-content:space-between;">
    <span id="ils-dist">ALT: 1,500 M</span>
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
  <div id="banner-title" style="font-size:18px;font-weight:900;color:#6ee7b7;letter-spacing:1.5px;">RUNWAY ARREST COMPLETE // TOUCHDOWN SECURED</div>
  <div id="banner-sub" style="font-size:11px;color:#d1fae5;margin-top:4px;">PARACHUTE JETTISONED / CHASSIS COOLED / MISSION SUCCESSFUL</div>
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
// 1. レンダラー＆大気圏マルチストップ散乱空＆全天球星空
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

// ニアクリップを0.05に変更（至近距離のコックピット計器切断を根絶）
const cameraMain = new THREE.PerspectiveCamera(55, W / H, 0.05, 980000);

let baseCamPos = new THREE.Vector3(-35.0, 16.0, -95.0);
let baseTarget = new THREE.Vector3(0.0, 1.5, -4.0);

if (cfg.cam_preset.includes("エクストラ")) {
    baseCamPos.set(-52.0, 24.0, -135.0);
} else if (cfg.cam_preset.includes("チェイス")) {
    baseCamPos.set(-26.0, 11.0, -75.0);
}
cameraMain.position.copy(baseCamPos);
cameraMain.lookAt(baseTarget);

// スクロール改善: OrbitControlsのズームは通常オフ
const controls = new THREE.OrbitControls(cameraMain, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.enableZoom = false;
controls.enabled = false;

canvas.addEventListener('dblclick', () => {
    controls.enabled = !controls.enabled;
    controls.enableZoom = controls.enabled;
});

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
            vec3 midSky = mix(uHorizon, uZenith, 0.5) + vec3(0.04, 0.08, 0.15);
            vec3 sky = (curve < 0.5) ? mix(uHorizon, midSky, curve * 2.0) : mix(midSky, uZenith, (curve - 0.5) * 2.0);
            float sunHalo = pow(max(0.0, dot(dir, uSunDir)), 12.0) * 0.45;
            sky += vec3(1.0, 0.75, 0.45) * sunHalo;
            sky = mix(sky, vec3(0.003, 0.008, 0.02), uSpaceFade);
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

// 全天球星空（不自然な近景ゴミを排除し、15,000恒星と天の川バンドを配置）
const spaceFieldGroup = new THREE.Group();
spaceFieldGroup.visible = false;
scene.add(spaceFieldGroup);

function createRealStarField(count, rMin, rMax, size, baseHex) {
    const geo = new THREE.BufferGeometry();
    const pos = new Float32Array(count * 3);
    const col = new Float32Array(count * 3);
    const c = new THREE.Color(baseHex);
    for (let i = 0; i < count; i++) {
        const u = Math.random(), v = Math.random();
        const theta = u * 2.0 * Math.PI, phi = Math.acos(2.0 * v - 1.0);
        const r = rMin + Math.random() * (rMax - rMin);
        pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
        pos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
        pos[i * 3 + 2] = r * Math.cos(phi);
        const brightness = 0.7 + Math.random() * 0.6;
        col[i * 3] = c.r * brightness; col[i * 3 + 1] = c.g * brightness; col[i * 3 + 2] = c.b * brightness;
    }
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
    return new THREE.Points(geo, new THREE.PointsMaterial({ size: size, vertexColors: true, transparent: true, opacity: 0.95, sizeAttenuation: false }));
}
spaceFieldGroup.add(createRealStarField(8000, 75000, 160000, 1.8, 0xdbeafe));
spaceFieldGroup.add(createRealStarField(5000, 65000, 140000, 2.2, 0x38bdf8));
spaceFieldGroup.add(createRealStarField(4000, 55000, 120000, 1.4, 0xfcd34d));

const sunLight = new THREE.DirectionalLight(cfg.env.sun_color, cfg.env.sun_int);
sunLight.position.set(cfg.env.sun_pos[0] * 0.15, cfg.env.sun_pos[1] * 0.15 + 40.0, cfg.env.sun_pos[2] * 0.15);
sunLight.castShadow = true;
scene.add(sunLight);
scene.add(new THREE.HemisphereLight(0x93c5fd, 0x0f172a, 1.8));

const WarpDistortionShader = {
    uniforms: { "tDiffuse": { value: null }, "uDistort": { value: 0.0 }, "uInvert": { value: 0.0 }, "uTime": { value: 0.0 }, "uFlare": { value: cfg.flare_int } },
    vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `
        uniform sampler2D tDiffuse; uniform float uDistort; uniform float uInvert; uniform float uTime; uniform float uFlare; varying vec2 vUv;
        void main() {
            vec2 center = vec2(0.5, 0.5); vec2 dir = vUv - center; float dist = length(dir);
            float ringDistort = sin(dist * 18.0 - uTime * 4.0) * exp(-dist * 3.5) * uDistort * 0.05;
            vec2 rUv = vUv + dir * (dist * uDistort * 0.09 + ringDistort);
            vec2 gUv = vUv;
            vec2 bUv = vUv - dir * (dist * uDistort * 0.09 + ringDistort);
            vec3 col = vec3(texture2D(tDiffuse, rUv).r, texture2D(tDiffuse, gUv).g, texture2D(tDiffuse, bUv).b);
            
            float streak = exp(-abs(vUv.y - 0.5) * 45.0) * uFlare * 0.15;
            col += vec3(0.2, 0.6, 1.0) * streak;
            
            if (uInvert > 0.01) col = mix(col, vec3(1.0) - col, uInvert);
            gl_FragColor = vec4(col * smoothstep(0.88, 0.25, dist), 1.0);
        }
    `
};

const composerMain = new THREE.EffectComposer(renderer);
composerMain.addPass(new THREE.RenderPass(scene, cameraMain));
composerMain.addPass(new THREE.UnrealBloomPass(new THREE.Vector2(W, H), 1.35, 0.45, 0.80));
const warpPass = new THREE.ShaderPass(WarpDistortionShader);
composerMain.addPass(warpPass);

const radarCanvas = document.getElementById('radar-canvas');
const rCtx = radarCanvas.getContext('2d');
const radarLabelEl = document.getElementById('radar-label');

function updateCameraAspect() {
    W = window.innerWidth; H = window.innerHeight;
    renderer.setSize(W, H);
    composerMain.setSize(W, H);
    cameraMain.aspect = W / H;
    cameraMain.fov = (W / H < 1.0) ? 68.0 : 55.0;
    cameraMain.updateProjectionMatrix();
    radarCanvas.width = radarCanvas.clientWidth * 1.5;
    radarCanvas.height = radarCanvas.clientHeight * 1.5;
}
window.addEventListener('resize', updateCameraAspect);
updateCameraAspect();

// =========================================================================
// 2. 本格Web Audio多層シンセサイザー＆点火爆裂音＆音声ガイド
// =========================================================================
let actx = null, rocketGain = null, rocketFilter = null, subBassGain = null, spoolGain = null, spoolOsc = null;
let lastAnnouncedPhase = "";
let lastSpokenSec = -999;
let availableVoices = [];

function updateVoiceList() {
    if ('speechSynthesis' in window) availableVoices = window.speechSynthesis.getVoices();
}
if ('speechSynthesis' in window) {
    updateVoiceList();
    window.speechSynthesis.onvoiceschanged = updateVoiceList;
}

const commsTextEl = document.getElementById('comms-text');
const countdownEl = document.getElementById('countdown-overlay');
const ilsHudEl = document.getElementById('ils-hud');

function playBeep(freq, dur) {
    if (!actx) return;
    try {
        const osc = actx.createOscillator();
        const g = actx.createGain();
        osc.frequency.setValueAtTime(freq, actx.currentTime);
        g.gain.setValueAtTime(0.2, actx.currentTime);
        g.gain.exponentialRampToValueAtTime(0.001, actx.currentTime + dur);
        osc.connect(g);
        g.connect(actx.destination);
        osc.start();
        osc.stop(actx.currentTime + dur);
    } catch(e){}
}

function speakCallout(text) {
    if (commsTextEl) commsTextEl.innerText = text;
    if (!cfg.voice_on) return;
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        setTimeout(() => {
            const u = new SpeechSynthesisUtterance(text);
            u.lang = 'en-US';
            if (availableVoices.length === 0) availableVoices = window.speechSynthesis.getVoices();
            const enVoice = availableVoices.find(v => (v.lang === 'en-US' || v.lang === 'en_US') && (v.name.includes('Google') || v.name.includes('Natural') || v.name.includes('Zira') || v.name.includes('David')))
                         || availableVoices.find(v => v.lang.startsWith('en'));
            if (enVoice) u.voice = enVoice;
            u.rate = 1.05; u.pitch = 1.0; u.volume = 0.95;
            window.speechSynthesis.speak(u);
        }, 15);
    }
}

function initAudioSystem() {
    if (actx) {
        if (actx.state === 'suspended') actx.resume();
        return;
    }
    try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        actx = new AudioCtx();
        if (actx.state === 'suspended') actx.resume();

        // 1. メインロケット燃焼ノイズ
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
        rocketFilter.frequency.value = 350;
        rocketGain = actx.createGain();
        rocketGain.gain.value = 0.0001;
        whiteNoise.connect(rocketFilter);
        rocketFilter.connect(rocketGain);
        rocketGain.connect(actx.destination);
        whiteNoise.start(0);

        // 2. 55Hz 重低音サブベース
        const subOsc = actx.createOscillator();
        subOsc.type = 'sine';
        subOsc.frequency.value = 55;
        subBassGain = actx.createGain();
        subBassGain.gain.value = 0.0001;
        subOsc.connect(subBassGain);
        subBassGain.connect(actx.destination);
        subOsc.start(0);

        // 3. ターボポンプ高周波スプール音
        spoolOsc = actx.createOscillator();
        spoolOsc.type = 'sawtooth';
        spoolOsc.frequency.value = 240;
        spoolGain = actx.createGain();
        spoolGain.gain.value = 0.0001;
        spoolOsc.connect(spoolGain);
        spoolGain.connect(actx.destination);
        spoolOsc.start(0);
    } catch(e){}
}
window.addEventListener('pointerdown', initAudioSystem, { once: false });

// =========================================================================
// 3. 5層高精細PBRテクスチャ
// =========================================================================
function makeMasterPbrTexture() {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 1024;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#475569'; ctx.fillRect(0, 0, 1024, 1024);

    for (let x = 0; x < 1024; x += 64) {
        for (let y = 0; y < 1024; y += 32) {
            const v = 85 + Math.floor(Math.random() * 55);
            ctx.fillStyle = `rgb(${v},${v+3},${v+8})`;
            ctx.fillRect(x + 2, y + 2, 60, 28);
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(x + 6, y + 6, 2, 2); ctx.fillRect(x + 54, y + 6, 2, 2);
            ctx.fillRect(x + 6, y + 22, 2, 2); ctx.fillRect(x + 54, y + 22, 2, 2);
            if (Math.random() > 0.6) {
                ctx.fillStyle = 'rgba(15,23,42,0.35)'; ctx.fillRect(x + 2, y + 24, 60, 6);
            }
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
const masterHullTex = makeMasterPbrTexture();

const matHull = new THREE.MeshPhysicalMaterial({ color: cfg.hull_color, metalness: cfg.metalness, roughness: cfg.roughness, bumpMap: masterHullTex, bumpScale: 0.05, clearcoat: 0.8 });
const matBellyTile = new THREE.MeshStandardMaterial({ color: cfg.belly_color, metalness: 0.35, roughness: 0.75, bumpMap: masterHullTex, bumpScale: 0.06 });
const matTitaniumFrame = new THREE.MeshStandardMaterial({ color: 0x475569, metalness: 0.92, roughness: 0.20 });
const matPistonRod = new THREE.MeshStandardMaterial({ color: 0xf8fafc, metalness: 0.98, roughness: 0.05 });
const matDarkAlloy = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.92, roughness: 0.22 });
const matGoldMLI = new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.96, roughness: 0.20 });
const matCopperCoil = new THREE.MeshStandardMaterial({ color: 0xd97706, metalness: 0.95, roughness: 0.15 });
const matCanopy = new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, metalness: 0.95, roughness: 0.03, transparent: true, opacity: 0.35 });
const matCryoPipe = new THREE.MeshStandardMaterial({ color: 0xdbeafe, roughness: 0.65, metalness: 0.25 });

// =========================================================================
// 4. 超精密宇宙船 ＆ 本格3Dコックピット（パイロット頭部アンカー同期）
// =========================================================================
const radAngle = THREE.MathUtils.degToRad(cfg.env.angle_deg);
const shipRoot = new THREE.Group();
scene.add(shipRoot);

const shipPitchGroup = new THREE.Group();
shipRoot.add(shipPitchGroup);

const shipMeshGroup = new THREE.Group();
shipPitchGroup.add(shipMeshGroup);

// コックピットカメラ視点アンカー（機体ローカル座標系・パイロットの目線）
const cockpitCamAnchor = new THREE.Object3D();
cockpitCamAnchor.position.set(0, 1.05, 8.2);
shipMeshGroup.add(cockpitCamAnchor);

// 内部骨格・極低温配管
const innerSkeletonGroup = new THREE.Group();
shipMeshGroup.add(innerSkeletonGroup);
innerSkeletonGroup.add(new THREE.Mesh(new THREE.BoxGeometry(2.2, 1.2, 28.0), matTitaniumFrame));

for (let s of [-1, 1]) {
    const pipePts = [new THREE.Vector3(s * 1.5, -0.4, 12.0), new THREE.Vector3(s * 2.2, -0.2, 4.0), new THREE.Vector3(s * 2.8, -0.3, -4.0), new THREE.Vector3(s * 0.9, 0.0, -15.0)];
    innerSkeletonGroup.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pipePts), 32, 0.16, 10, false), matCryoPipe));
}

// 艦種別造形
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
    const dPanel = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.25, 12.0), matHull);
    dPanel.position.set(-s * 1.1, 0, 0);
    doorPivot.add(dPanel);
    bayDoors.push({ pivot: doorPivot, side: s });
}

// 主翼＆翼端ナビゲーションライト
const halfSpan = cfg.wings_span * 0.5;
const wingPivots = [];
const elevonMeshes = [];
const navLights = [];
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

    const wMesh = new THREE.Mesh(new THREE.ExtrudeGeometry(wShape, { depth: 0.32, bevelThickness: 0.12, bevelSize: 0.4 }), matHull);
    wMesh.rotation.x = Math.PI / 2;
    wMesh.castShadow = true;
    pivot.add(wMesh);
    wingPivots.push({ group: pivot, side: s });

    const elMesh = new THREE.Mesh(new THREE.BoxGeometry(halfSpan * 0.45, 0.18, 1.6), matDarkAlloy);
    elMesh.position.set(s * (halfSpan * 0.55), 0, -8.6);
    pivot.add(elMesh);
    elevonMeshes.push({ mesh: elMesh, side: s });

    // ナビライト（左翼：赤、右翼：緑）＋白色ストロボ
    const navCol = (s === -1) ? 0xef4444 : 0x10b981;
    const nLight = new THREE.Mesh(new THREE.SphereGeometry(0.2, 8, 8), new THREE.MeshBasicMaterial({ color: navCol }));
    nLight.position.set(s * (halfSpan - 3.4), 0, -5.5);
    pivot.add(nLight);
    navLights.push(nLight);
}

// 背面スピードエアブレーキ
const speedbrakePivot = new THREE.Group();
speedbrakePivot.position.set(0, 1.35, -5.0);
shipMeshGroup.add(speedbrakePivot);
const speedbrakeMesh = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.18, 4.2), matTitaniumFrame);
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

// タイヤ接地白煙
const smokePuffs = [];
const smokeGeo = new THREE.SphereGeometry(1.2, 8, 8);
const smokeMat = new THREE.MeshBasicMaterial({ color: 0xe2e8f0, transparent: true, opacity: 0.0 });
for (let sm = 0; sm < 8; sm++) {
    const p = new THREE.Mesh(smokeGeo, smokeMat);
    shipMeshGroup.add(p);
    smokePuffs.push(p);
}

// 十字型ドラッグシュート
const chuteGroup = new THREE.Group();
chuteGroup.position.set(0, 0.8, -16.5);
chuteGroup.scale.set(0.001, 0.001, 0.001);
shipMeshGroup.add(chuteGroup);

const chuteCanopy = new THREE.Mesh(
    new THREE.ConeGeometry(4.8, 6.0, 12, 1, true),
    new THREE.MeshStandardMaterial({ color: 0xf59e0b, side: THREE.DoubleSide, roughness: 0.7 })
);
chuteCanopy.rotation.x = -Math.PI / 2;
chuteCanopy.position.z = -18.0;
chuteGroup.add(chuteCanopy);

// 24枚二重アイリス可変ノズル
const nozzleGimbalRoot = new THREE.Group();
nozzleGimbalRoot.position.set(0, 0, -14.2);
shipMeshGroup.add(nozzleGimbalRoot);

const irisPaddles = [];
for (let i = 0; i < 24; i++) {
    const ang = (i / 24) * Math.PI * 2;
    const pPivot = new THREE.Group();
    pPivot.position.set(Math.cos(ang) * 2.4, Math.sin(ang) * 2.4, -1.0);
    pPivot.rotation.z = ang;
    nozzleGimbalRoot.add(pPivot);
    const blade = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.08, 3.2), (i % 2 === 0) ? matTitaniumFrame : matDarkAlloy);
    blade.position.set(0, 0.05, -1.4);
    pPivot.add(blade);
    irisPaddles.push(pPivot);
}

// ロフト機体本体
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
    const radialSegs = 24, zSegs = sections.length;
    const geo = new THREE.BufferGeometry(), pos = [], uvs = [], indices = [];
    for (let j = 0; j < zSegs; j++) {
        const sec = sections[j];
        for (let i = 0; i <= radialSegs; i++) {
            const theta = (i / radialSegs) * Math.PI * 2;
            pos.push(Math.cos(theta) * (sec.w * 0.5), sec.yOff + Math.sin(theta) * (Math.sin(theta) >= 0 ? sec.hTop : sec.hBtm), sec.z);
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
const loftGeo = createLoftedChassisGeometry();
shipMeshGroup.add(new THREE.Mesh(loftGeo, matHull));
const bellyMesh = new THREE.Mesh(loftGeo, matBellyTile);
bellyMesh.scale.set(0.985, 0.98, 0.995);
bellyMesh.position.y = -0.06;
shipMeshGroup.add(bellyMesh);

const canopyGlass = new THREE.Mesh(new THREE.ConeGeometry(1.35, 7.5, 16), matCanopy);
canopyGlass.scale.set(1.0, 0.48, 1.6);
canopyGlass.rotation.x = Math.PI / 2;
canopyGlass.position.set(0, 0.95, 8.8);
shipMeshGroup.add(canopyGlass);

// =========================================================================
// 🔬 本格5面グラスコックピット＆ホログラムHUD（パイロット目線）
// =========================================================================
const cockpitInteriorGroup = new THREE.Group();
cockpitInteriorGroup.position.set(0, 0.75, 8.5);
cockpitInteriorGroup.visible = false;
shipMeshGroup.add(cockpitInteriorGroup);

const canopyPillarMat = new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.2, metalness: 0.9 });
const frontArch = new THREE.Mesh(new THREE.TorusGeometry(0.92, 0.05, 8, 24, Math.PI), canopyPillarMat);
frontArch.position.set(0, 0.32, 0.3);
cockpitInteriorGroup.add(frontArch);

const dashBoard = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.38, 0.9), canopyPillarMat);
dashBoard.position.set(0, -0.12, 0.55);
dashBoard.rotation.x = 0.28;
cockpitInteriorGroup.add(dashBoard);

// 操縦桿＆スロットル
const stickPivot = new THREE.Group();
stickPivot.position.set(0.35, -0.02, 0.15);
const flightStick = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.025, 0.28, 8), matTitaniumFrame);
flightStick.position.y = 0.14;
stickPivot.add(flightStick);
cockpitInteriorGroup.add(stickPivot);

const throttlePivot = new THREE.Group();
throttlePivot.position.set(-0.38, -0.02, 0.15);
const throttleLever = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.14, 0.06), matDarkAlloy);
throttleLever.position.y = 0.07;
throttlePivot.add(throttleLever);
cockpitInteriorGroup.add(throttlePivot);

// 5面動的マルチファンクションディスプレイ (MFD)
const mfdCanvas = document.createElement('canvas');
mfdCanvas.width = 1024; mfdCanvas.height = 512;
const mfdCtx = mfdCanvas.getContext('2d');
const mfdTex = new THREE.CanvasTexture(mfdCanvas);
const mfdMat = new THREE.MeshBasicMaterial({ map: mfdTex });

const mfdCenter = new THREE.Mesh(new THREE.PlaneGeometry(0.46, 0.28), mfdMat);
mfdCenter.position.set(0, 0.05, 0.75);
mfdCenter.rotation.x = -0.32;
cockpitInteriorGroup.add(mfdCenter);

const mfdLeftMid = new THREE.Mesh(new THREE.PlaneGeometry(0.38, 0.25), mfdMat);
mfdLeftMid.position.set(-0.50, 0.04, 0.68);
mfdLeftMid.rotation.set(-0.32, 0.35, 0);
cockpitInteriorGroup.add(mfdLeftMid);

const mfdRightMid = new THREE.Mesh(new THREE.PlaneGeometry(0.38, 0.25), mfdMat);
mfdRightMid.position.set(0.50, 0.04, 0.68);
mfdRightMid.rotation.set(-0.32, -0.35, 0);
cockpitInteriorGroup.add(mfdRightMid);

// フロントホログラムHUD
const hudCanvas = document.createElement('canvas');
hudCanvas.width = 512; hudCanvas.height = 512;
const hudCtx = hudCanvas.getContext('2d');
const hudTex = new THREE.CanvasTexture(hudCanvas);
const hudThemeColor = cfg.hud_theme.includes("Green") ? "#10b981" : (cfg.hud_theme.includes("Amber") ? "#f59e0b" : "#38bdf8");
const hudPlaneMat = new THREE.MeshBasicMaterial({ map: hudTex, transparent: true, opacity: 0.90, blending: THREE.AdditiveBlending });
const hudGlassPlane = new THREE.Mesh(new THREE.PlaneGeometry(0.95, 0.95), hudPlaneMat);
hudGlassPlane.position.set(0, 0.32, 1.18);
hudGlassPlane.rotation.x = -0.15;
cockpitInteriorGroup.add(hudGlassPlane);

function updateCockpitDisplays(mach, altKm, gLoad, pitchDeg, rollDeg, engPwr, phase) {
    mfdCtx.fillStyle = '#020617';
    mfdCtx.fillRect(0, 0, 1024, 512);
    mfdCtx.strokeStyle = hudThemeColor;
    mfdCtx.lineWidth = 3;
    mfdCtx.strokeRect(8, 8, 1008, 496);

    // PFD 人工水平儀
    const cx = 512, cy = 256;
    mfdCtx.save();
    mfdCtx.translate(cx, cy);
    mfdCtx.rotate(-rollDeg * Math.PI / 180);
    const pOff = (pitchDeg / 90) * 160;
    mfdCtx.strokeStyle = hudThemeColor;
    mfdCtx.lineWidth = 3;
    mfdCtx.beginPath();
    mfdCtx.moveTo(-160, -pOff); mfdCtx.lineTo(160, -pOff);
    mfdCtx.stroke();
    mfdCtx.restore();

    mfdCtx.fillStyle = hudThemeColor;
    mfdCtx.font = 'bold 36px monospace';
    mfdCtx.fillText(`VEL: M ${mach.toFixed(1)}`, 40, 70);
    mfdCtx.fillText(`ALT: ${altKm.toFixed(1)} KM`, 40, 130);
    mfdCtx.fillText(`ENG: ${Math.round(engPwr*100)}%`, 40, 190);

    mfdCtx.fillText(`G-LOAD: ${gLoad.toFixed(1)} G`, 680, 70);
    mfdCtx.fillText(`MODE: ${phase.slice(0, 12)}`, 680, 130);
    mfdCtx.fillText(`STATUS: NOMINAL`, 680, 190);
    mfdTex.needsUpdate = true;

    // HUDホログラム描画
    hudCtx.clearRect(0, 0, 512, 512);
    hudCtx.strokeStyle = hudThemeColor;
    hudCtx.lineWidth = 2.5;
    hudCtx.beginPath();
    hudCtx.arc(256, 256, 50, 0, Math.PI * 2);
    hudCtx.moveTo(256, 170); hudCtx.lineTo(256, 342);
    hudCtx.moveTo(170, 256); hudCtx.lineTo(342, 256);
    hudCtx.stroke();

    hudCtx.fillStyle = hudThemeColor;
    hudCtx.font = 'bold 24px monospace';
    hudCtx.fillText(`M ${mach.toFixed(1)}`, 110, 264);
    hudCtx.fillText(`${Math.round(altKm * 1000)}M`, 350, 264);
    hudTex.needsUpdate = true;
}

// アルクビエレ・ワープリング
const warpRingAssembly = new THREE.Group();
warpRingAssembly.position.set(0, 0.0, -2.5);
warpRingAssembly.scale.set(0.001, 0.001, 0.001);
shipMeshGroup.add(warpRingAssembly);

const rotorClockwise = new THREE.Group();
const rotorCounter = new THREE.Group();
warpRingAssembly.add(rotorClockwise);
warpRingAssembly.add(rotorCounter);

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
}
rotorCounter.add(new THREE.Mesh(new THREE.TorusGeometry(5.4, 0.18, 12, 48), matCopperCoil));

// 実写風マッハコーン放物線衝撃波
const machConeGeo = new THREE.ConeGeometry(9.0, 24.0, 32, 1, true);
const machConeMat = new THREE.ShaderMaterial({
    vertexShader: `varying vec2 vUv; varying vec3 vNormal; void main() { vUv = uv; vNormal = normalize(normalMatrix * normal); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `
        varying vec2 vUv; varying vec3 vNormal; uniform float uAlpha; uniform vec3 uBaseColor;
        void main() {
            float fresnel = pow(1.0 - abs(dot(vNormal, vec3(0.0, 0.0, 1.0))), 2.5);
            float taper = pow(vUv.y, 2.0);
            vec3 col = mix(vec3(1.0), uBaseColor, vUv.y);
            gl_FragColor = vec4(col, fresnel * taper * uAlpha * 0.9);
        }
    `,
    uniforms: { uAlpha: { value: 0.0 }, uBaseColor: { value: new THREE.Color(cfg.plasma_hex) } },
    transparent: true, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false
});
const machConeMesh = new THREE.Mesh(machConeGeo, machConeMat);
machConeMesh.rotation.x = -Math.PI / 2;
machConeMesh.position.set(0, 0, 7.0);
shipMeshGroup.add(machConeMesh);

// 3層構造・推進炎（初期完全非表示）
const plumeRoot = new THREE.Group();
plumeRoot.position.set(0, 0, -2.3);
plumeRoot.visible = false;
nozzleGimbalRoot.add(plumeRoot);

const innerCoreMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 1.2, 28.0, 16, 1, true), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.95, blending: THREE.AdditiveBlending }));
innerCoreMesh.rotation.x = Math.PI / 2;
innerCoreMesh.position.z = -14.0;
plumeRoot.add(innerCoreMesh);

const shockShaderMat = new THREE.ShaderMaterial({
    vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `
        varying vec2 vUv; uniform float uTime; uniform vec3 uColor; uniform float uWarp;
        void main() {
            float rings = sin(vUv.y * 55.0 - uTime * 35.0);
            float diamond = abs(rings) * pow(1.0 - abs(vUv.x - 0.5) * 2.0, 2.0);
            float taper = pow(1.0 - vUv.y, 1.2);
            vec3 c = mix(uColor, vec3(0.3, 0.8, 1.0), uWarp);
            gl_FragColor = vec4(c, diamond * taper);
        }
    `,
    uniforms: { uTime: { value: 0.0 }, uColor: { value: new THREE.Color(cfg.flame_hex) }, uWarp: { value: 0.0 } },
    transparent: true, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false
});
const shockCylinder = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 4.2, 42.0, 32, 1, true), shockShaderMat);
shockCylinder.rotation.x = Math.PI / 2;
shockCylinder.position.z = -21.0;
plumeRoot.add(shockCylinder);

const outerFlameMat = new THREE.ShaderMaterial({
    vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `
        varying vec2 vUv; uniform float uTime; uniform vec3 uColor;
        void main() {
            float noise = sin(vUv.y * 22.0 - uTime * 20.0) * cos(vUv.x * 14.0 + uTime * 12.0);
            float edge = pow(1.0 - vUv.y, 2.0) * (0.6 + noise * 0.4);
            gl_FragColor = vec4(uColor, edge * 0.55);
        }
    `,
    uniforms: { uTime: { value: 0.0 }, uColor: { value: new THREE.Color(cfg.spark_hex) } },
    transparent: true, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false
});
const outerFlameMesh = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 6.5, 48.0, 32, 1, true), outerFlameMat);
outerFlameMesh.rotation.x = Math.PI / 2;
outerFlameMesh.position.z = -24.0;
plumeRoot.add(outerFlameMesh);

// =========================================================================
// 5. 3層パララックス・ワープトンネル
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
    warpGroup.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(rPts), 64, 0.55, 8, false), new THREE.MeshBasicMaterial({ color: (r % 2 === 0) ? cfg.aurora_hex : 0x38bdf8, transparent: true, opacity: 0.88, blending: THREE.AdditiveBlending })));
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
warpGroup.add(new THREE.LineSegments(starGeo, new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.92, blending: THREE.AdditiveBlending })));

// =========================================================================
// 6. 実写風富士山・PBR海面・相模湾メガフロート
// =========================================================================
const catapultSlopeRoot = new THREE.Group();
catapultSlopeRoot.rotation.x = -radAngle;
scene.add(catapultSlopeRoot);

const railMover = new THREE.Group();
catapultSlopeRoot.add(railMover);

const mainGirder = new THREE.Mesh(new THREE.BoxGeometry(14.5, 2.4, 3600), matDarkAlloy);
mainGirder.position.set(0, -4.8, 1750);
mainGirder.receiveShadow = true;
railMover.add(mainGirder);

const dummyArch = new THREE.Object3D();
const archInst = new THREE.InstancedMesh(new THREE.TorusGeometry(9.5, 0.45, 10, 24, Math.PI), matTitaniumFrame, 220);
for (let i = 0; i < 220; i++) {
    dummyArch.position.set(0, -3.2, i * 16.0 - 40.0); dummyArch.updateMatrix(); archInst.setMatrixAt(i, dummyArch.matrix);
}
railMover.add(archInst);

const groundEnvMover = new THREE.Group();
scene.add(groundEnvMover);

// Gerstner + PBR海面
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
            vec3 deepWater = vec3(0.015, 0.045, 0.095); vec3 skyReflect = vec3(0.35, 0.65, 0.98);
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
const seaMesh = new THREE.Mesh(new THREE.PlaneGeometry(280000, 280000, 96, 96), oceanShaderMat);
seaMesh.rotation.x = -Math.PI / 2;
seaMesh.position.y = -45.0;
groundEnvMover.add(seaMesh);

const islandBase = new THREE.Mesh(new THREE.BoxGeometry(220, 28, 3800), matDarkAlloy);
islandBase.position.set(0, -32, 1750);
islandBase.receiveShadow = true;
groundEnvMover.add(islandBase);

// 実写対数曲線・富士山（正規化修正・宝永火口・雪渓シェーダー）
const fujiShaderMat = new THREE.ShaderMaterial({
    vertexShader: `
        varying vec3 vWorldPos; varying vec3 vNormal;
        void main() {
            vNormal = normalize(normalMatrix * normal);
            vec3 p = position;
            // ConeGeometryのY範囲（-1888〜+1888）を0.0〜1.0に正確に正規化
            float h = clamp((p.y + 1888.0) / 3776.0, 0.0, 1.0);
            float flare = pow(1.0 - h, 1.65) * 1.5;
            p.xz *= (1.0 + flare);
            if (p.x > 300.0 && p.x < 1400.0 && h > 0.45 && h < 0.68) {
                p.z -= 280.0 * sin((h - 0.45) / 0.23 * 3.1415);
            }
            vec4 wp = modelMatrix * vec4(p, 1.0);
            vWorldPos = wp.xyz;
            gl_Position = projectionMatrix * viewMatrix * wp;
        }
    `,
    fragmentShader: `
        varying vec3 vWorldPos; varying vec3 vNormal; uniform vec3 uSunDir;
        void main() {
            float alt = vWorldPos.y;
            float snow = smoothstep(2200.0, 3100.0, alt + sin(vWorldPos.x * 0.01) * 160.0);
            vec3 rockCol = vec3(0.09, 0.10, 0.13);
            vec3 snowCol = vec3(0.94, 0.96, 1.0);
            vec3 col = mix(rockCol, snowCol, snow);
            float diff = max(0.18, dot(vNormal, uSunDir));
            gl_FragColor = vec4(col * diff, 1.0);
        }
    `,
    uniforms: { uSunDir: { value: new THREE.Vector3().fromArray(cfg.env.sun_pos).normalize() } }
});
const fujiMount = new THREE.Mesh(new THREE.ConeGeometry(14000, 3776, 64, 32), fujiShaderMat);
fujiMount.position.set(4500, 1888, 14500);
groundEnvMover.add(fujiMount);

// 湘南海岸都市光
const cityCount = 4500;
const cityGeo = new THREE.BufferGeometry();
const cityPos = new Float32Array(cityCount * 3);
const cityCol = new Float32Array(cityCount * 3);
for (let i = 0; i < cityCount; i++) {
    cityPos[i * 3] = (Math.random() - 0.5) * 24000 + 4000;
    cityPos[i * 3 + 1] = 5.0 + Math.random() * 30.0;
    cityPos[i * 3 + 2] = 3000 + Math.random() * 16000;
    const isAmber = Math.random() > 0.4;
    cityCol[i * 3] = isAmber ? 1.0 : 0.4;
    cityCol[i * 3 + 1] = isAmber ? 0.65 : 0.8;
    cityCol[i * 3 + 2] = isAmber ? 0.2 : 1.0;
}
cityGeo.setAttribute('position', new THREE.BufferAttribute(cityPos, 3));
cityGeo.setAttribute('color', new THREE.BufferAttribute(cityCol, 3));
const cityPoints = new THREE.Points(cityGeo, new THREE.PointsMaterial({ size: 3.5, vertexColors: true, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending }));
groundEnvMover.add(cityPoints);

// 5オクターブFBM地球
const earthShaderMat = new THREE.ShaderMaterial({
    vertexShader: `varying vec3 vNormal; varying vec3 vWorldPos; void main() { vNormal = normalize(normalMatrix * normal); vec4 wp = modelMatrix * vec4(position, 1.0); vWorldPos = wp.xyz; gl_Position = projectionMatrix * viewMatrix * wp; }`,
    fragmentShader: `
        varying vec3 vNormal; varying vec3 vWorldPos; uniform vec3 uSunDir; uniform float uOpacity;
        float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123); }
        float smoothNoise(vec2 p) {
            vec2 i = floor(p); vec2 f = fract(p); vec2 u = f * f * (3.0 - 2.0 * f);
            return mix(mix(hash(i + vec2(0.0,0.0)), hash(i + vec2(1.0,0.0)), u.x), mix(hash(i + vec2(0.0,1.0)), hash(i + vec2(1.0,1.0)), u.x), u.y);
        }
        float fbm(vec2 p) { float v = 0.0; float a = 0.5; for (int i = 0; i < 5; i++) { v += a * smoothNoise(p); p *= 2.0; a *= 0.5; } return v; }
        void main() {
            vec3 norm = normalize(vNormal); vec3 viewDir = normalize(cameraPosition - vWorldPos); float light = dot(norm, uSunDir);
            vec2 sphereUv = vec2(atan(norm.z, norm.x) * 0.159 + 0.5, asin(norm.y) * 0.318 + 0.5);
            float land = smoothstep(0.48, 0.54, fbm(sphereUv * 8.0));
            vec3 oceanCol = vec3(0.012, 0.045, 0.12); vec3 landCol = vec3(0.07, 0.13, 0.08);
            vec3 dayCol = mix(oceanCol, landCol, land);
            float clouds = smoothstep(0.45, 0.75, fbm(sphereUv * 16.0 + vec2(0.1, 0.0)));
            dayCol = mix(dayCol, vec3(0.92, 0.95, 1.0), clouds * 0.65);
            float cityLights = pow(smoothNoise(sphereUv * 32.0), 3.0) * land * 14.0;
            vec3 nightCol = vec3(1.0, 0.75, 0.3) * cityLights;
            vec3 baseCol = mix(nightCol, dayCol * max(0.08, light), smoothstep(-0.15, 0.25, light));
            float rim = pow(1.0 - max(0.0, dot(norm, viewDir)), 3.0);
            gl_FragColor = vec4(baseCol + vec3(0.25, 0.65, 1.0) * rim * 1.8, uOpacity);
        }
    `,
    uniforms: { uSunDir: { value: new THREE.Vector3().fromArray(cfg.env.sun_pos).normalize() }, uOpacity: { value: 1.0 } },
    transparent: true
});
const earthGroup = new THREE.Group();
earthGroup.visible = false;
scene.add(earthGroup);
earthGroup.add(new THREE.Mesh(new THREE.SphereGeometry(25000, 64, 64), earthShaderMat));

// =========================================================================
// 7. 目的地：惑星着陸バイオドーム都市 vs 恒星・ブラックホール周回軌道
// =========================================================================
const destWorld = new THREE.Group();
destWorld.visible = false;
scene.add(destWorld);

const runwayScrollGroup = new THREE.Group();
destWorld.add(runwayScrollGroup);

const orbitGoalGroup = new THREE.Group();
destWorld.add(orbitGoalGroup);

// 惑星用：幅150m・長さ5000mの滑走路＆巨大バイオドーム都市
const runwayMesh = new THREE.Mesh(new THREE.BoxGeometry(150.0, 0.4, 5000.0), new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.85 }));
runwayMesh.position.set(0, -3.0, 0);
runwayMesh.receiveShadow = true;
runwayScrollGroup.add(runwayMesh);

const centerLineMesh = new THREE.Mesh(new THREE.PlaneGeometry(3.0, 4800.0), new THREE.MeshBasicMaterial({ color: 0xffffff }));
centerLineMesh.rotation.x = -Math.PI / 2;
centerLineMesh.position.set(0, -2.75, 0);
runwayScrollGroup.add(centerLineMesh);

const domeMat = new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, roughness: 0.1, transmission: 0.75, transparent: true, opacity: 0.65 });
for (let dm = 0; dm < 4; dm++) {
    const s = (dm % 2 === 0) ? -1 : 1;
    const dz = -1600.0 + dm * 1000.0;
    const bioDome = new THREE.Mesh(new THREE.SphereGeometry(450.0, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.5), domeMat);
    bioDome.position.set(s * 750.0, -3.0, dz);
    runwayScrollGroup.add(bioDome);

    for (let b = 0; b < 18; b++) {
        const bh = 150.0 + Math.random() * 450.0;
        const bMesh = new THREE.Mesh(new THREE.BoxGeometry(45.0, bh, 45.0), matTitaniumFrame);
        bMesh.position.set(s * 750.0 + (Math.random() - 0.5) * 400.0, bh * 0.5 - 3.0, dz + (Math.random() - 0.5) * 400.0);
        runwayScrollGroup.add(bMesh);
    }
}

for (let hg = 0; hg < 14; hg++) {
    const gateZ = -2200.0 + hg * 320.0;
    const hgMesh = new THREE.Mesh(new THREE.RingGeometry(45.0, 48.0, 4), new THREE.MeshBasicMaterial({ color: 0x10b981, transparent: true, opacity: 0.7, side: THREE.DoubleSide }));
    hgMesh.position.set(0, 25.0, gateZ);
    runwayScrollGroup.add(hgMesh);
}

const dummyLight = new THREE.Object3D();
const approachLightsInst = new THREE.InstancedMesh(new THREE.SphereGeometry(0.8, 8, 8), new THREE.MeshBasicMaterial({ color: 0x10b981 }), 160);
for (let al = 0; al < 80; al++) {
    const lz = -2500.0 - al * 30.0;
    dummyLight.position.set(-70.0, -2.6, lz); dummyLight.updateMatrix(); approachLightsInst.setMatrixAt(al * 2, dummyLight.matrix);
    dummyLight.position.set(70.0, -2.6, lz); dummyLight.updateMatrix(); approachLightsInst.setMatrixAt(al * 2 + 1, dummyLight.matrix);
}
runwayScrollGroup.add(approachLightsInst);

const rabbitStrobeMesh = new THREE.Mesh(new THREE.SphereGeometry(2.0, 12, 12), new THREE.MeshBasicMaterial({ color: 0xffffff, blending: THREE.AdditiveBlending }));
rabbitStrobeMesh.position.set(0, -2.0, -2500.0);
runwayScrollGroup.add(rabbitStrobeMesh);

// 恒星周回軌道用：ダイソン・スウォーム＆恒星
const dysonStation = new THREE.Mesh(new THREE.TorusGeometry(120.0, 8.0, 16, 64), matTitaniumFrame);
dysonStation.position.set(0, 0, 120.0);
orbitGoalGroup.add(dysonStation);

const starCore = new THREE.Mesh(new THREE.SphereGeometry(3200, 64, 64), new THREE.MeshBasicMaterial({ color: new THREE.Color(cfg.dest_color) }));
starCore.position.set(0, 0, 8000);
orbitGoalGroup.add(starCore);

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
    initAudioSystem();
    isPlaying = !isPlaying;
    playPauseBtn.innerText = isPlaying ? "PAUSE" : "PLAY";
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
    const isSolar = (prog >= 0.16 && prog < 0.78);
    radarLabelEl.innerHTML = isSolar ? `TACTICAL RADAR<br><span style="color:#10b981;font-size:8px;">INTERPLANETARY SCALE</span>` : `TACTICAL RADAR<br><span style="color:#38bdf8;font-size:8px;">APPROACH & VECTOR</span>`;
    const leftX = 75, rightX = rw - 85, midY = rh / 2;
    rCtx.strokeStyle = 'rgba(56,189,248,0.3)'; rCtx.lineWidth = 3;
    rCtx.beginPath(); rCtx.moveTo(leftX, midY); rCtx.lineTo(rightX, midY); rCtx.stroke();
    rCtx.textAlign = "center";
    if (!isSolar) {
        const destLabel = cfg.goal_type === "orbit" ? "ORBIT STATION" : "RUNWAY 04L";
        [{ x: leftX, lbl: "EARTH" }, { x: leftX + (rightX - leftX) * 0.5, lbl: "ORBIT" }, { x: rightX, lbl: destLabel }].forEach(m => {
            rCtx.fillStyle = '#38bdf8'; rCtx.beginPath(); rCtx.arc(m.x, midY, 4, 0, Math.PI * 2); rCtx.fill();
            rCtx.font = 'bold 10px monospace'; rCtx.fillStyle = '#f8fafc'; rCtx.fillText(m.lbl, m.x, midY - 14);
        });
        const curX = leftX + THREE.MathUtils.clamp(prog, 0.0, 1.0) * (rightX - leftX);
        rCtx.fillStyle = '#f43f5e'; rCtx.beginPath(); rCtx.arc(curX, midY, 6, 0, Math.PI * 2); rCtx.fill();
    } else {
        const curX = leftX + ((prog - 0.16) / 0.62) * (rightX - leftX);
        rCtx.fillStyle = '#10b981'; rCtx.beginPath(); rCtx.arc(curX, midY, 7, 0, Math.PI * 2); rCtx.fill();
    }
}

// =========================================================================
// 10. 60fps アニメーションループ（完全同期・実写VFX）
// =========================================================================
const cameraIdealPos = new THREE.Vector3();
const cameraLookTarget = new THREE.Vector3();
const shipWorldPos = new THREE.Vector3();
const anchorWorldPos = new THREE.Vector3();
const anchorWorldQuat = new THREE.Quaternion();
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
    const vib = L('vib') * cfg.shake_scale, prog = L('progress'), tempK = L('temp_k'), gLoad = L('g');
    const engPwr = L('engine_power'), pAlpha = L('plasma_alpha');
    const wCharge = L('warp_charge'), wAct = L('warp_active'), wBoom = L('warp_boom');
    const gearD = L('gear_deploy'), speedbrake = L('speedbrake'), ringL = L('ring_lift'), bayO = L('bay_open');
    const chuteD = L('chute_deploy'), runwaySpd = L('runway_speed'), tdSmoke = L('touchdown_smoke');
    const vaporA = L('vapor_alpha');

    // T-5カウントダウン演出
    if (currentTime < 0.0) {
        countdownEl.style.display = 'block';
        const secLeft = Math.ceil(-currentTime);
        countdownEl.innerText = `T-0${secLeft}`;
        if (secLeft !== lastSpokenSec) {
            lastSpokenSec = secLeft;
            playBeep(880, 0.12);
            speakCallout(`${secLeft}`);
        }
    } else if (currentTime <= 1.5) {
        countdownEl.style.display = 'block';
        countdownEl.innerText = `IGNITION`;
        if (lastSpokenSec !== 0) {
            lastSpokenSec = 0;
            playBeep(1760, 0.35);
            speakCallout("Ignition. Liftoff.");
        }
    } else {
        countdownEl.style.display = 'none';
    }

    // コールアウト音声
    if (f0.phase !== lastAnnouncedPhase && currentTime > 1.5) {
        lastAnnouncedPhase = f0.phase;
        if (f0.phase === "CATAPULT_RAIL_ACCEL") speakCallout("Catapult engaged. Full boost.");
        else if (f0.phase === "STRATOSPHERE_CLIMB") speakCallout("Max Q nominal. Clearing stratosphere.");
        else if (f0.phase === "WARP_FIELD_COMPRESSION") speakCallout("Spooling warp field.");
        else if (f0.phase === "ALCUBIERRE_HYPER_WARP") speakCallout("Hyper warp engaged.");
        else if (f0.phase === "RETRO_BRAKING_TRANSITION") speakCallout("Warp disengaged. Braking burn.");
        else if (f0.phase === "ILS_GLIDESLOPE_ALIGNMENT") speakCallout("ILS glideslope intercepted. Gear down.");
        else if (f0.phase === "FINAL_APPROACH_FLARE") speakCallout("Minimums. Flare.");
        else if (f0.phase === "TOUCHDOWN_ROLLOUT_STOP") speakCallout("Touchdown! Chute out.");
        else if (f0.phase === "PLANETARY_RUNWAY_SECURED") speakCallout("Outpost runway secured. Welcome.");
        else if (f0.phase === "ORBITAL_STATION_DOCKED") speakCallout("Dyson station rendezvous complete.");
    }

    if (cfg.goal_type === "landing" && (f0.phase.includes("APPROACH") || f0.phase.includes("FLARE") || f0.phase.includes("GLIDESLOPE"))) {
        ilsHudEl.style.display = 'flex';
        document.getElementById('ils-dist').innerText = `ALT: ${(altKm * 1000).toFixed(0)} M`;
    } else {
        ilsHudEl.style.display = 'none';
    }

    // スカイドーム制御
    const spaceFade = THREE.MathUtils.clamp((altKm - 15.0) / 65.0, 0.0, 1.0);
    atmoSkyMat.uniforms.uSpaceFade.value = spaceFade;
    spaceFieldGroup.visible = (spaceFade > 0.05);

    // 機体姿勢（空力的に自然なピッチ角）
    shipPitchGroup.rotation.set(-THREE.MathUtils.degToRad(pitchDeg), THREE.MathUtils.degToRad(yawDeg), THREE.MathUtils.degToRad(rollDeg));

    // サスペンション接地バウンド
    let suspensionBounce = 0.0;
    if (f0.phase === "TOUCHDOWN_ROLLOUT_STOP") {
        const bouncePhase = ((currentTime - f0.t) / (dtFrame || 1.0)) * 5.0;
        suspensionBounce = Math.sin(bouncePhase * Math.PI) * Math.exp(-bouncePhase * 0.8) * 0.18;
    }
    shipMeshGroup.position.set(
        Math.sin(now * 0.003) * 0.25,
        Math.cos(now * 0.004) * 0.18 - suspensionBounce,
        Math.sin(now * 0.002) * 0.35
    );

    shipMeshGroup.getWorldPosition(shipWorldPos);

    // ダイナミックFOV
    let targetFov = 55.0;
    if (f0.phase === "CATAPULT_RAIL_ACCEL" || f0.phase === "ALCUBIERRE_HYPER_WARP") {
        targetFov = 55.0 + (gLoad / 10.0) * 22.0;
    } else if (f0.phase === "TOUCHDOWN_ROLLOUT_STOP") {
        targetFov = 48.0;
    }
    cameraMain.fov = THREE.MathUtils.lerp(cameraMain.fov, targetFov, 0.08);
    cameraMain.updateProjectionMatrix();

    // コックピットカメラ切替（目線アンカーと完全同期）
    cockpitInteriorGroup.visible = (activeCamMode === 2);
    if (activeCamMode === 2) {
        updateCockpitDisplays(mach, altKm, gLoad, pitchDeg, rollDeg, engPwr, f0.phase);
        stickPivot.rotation.x = -pitchDeg * 0.015;
        stickPivot.rotation.z = -rollDeg * 0.015;
        throttlePivot.rotation.x = engPwr * 0.45;

        // アンカーからワールド座標と回転を抽出してカメラへコピー
        cockpitCamAnchor.getWorldPosition(anchorWorldPos);
        cockpitCamAnchor.getWorldQuaternion(anchorWorldQuat);
        cameraMain.position.copy(anchorWorldPos);
        cameraMain.quaternion.copy(anchorWorldQuat);
    } else {
        if (!controls.enabled) {
            if (activeCamMode === 0 || activeCamMode === 1) {
                const camZLag = (gLoad > 3.0) ? (gLoad - 3.0) * 1.5 : 0.0;
                cameraIdealPos.set(shipWorldPos.x + baseCamPos.x, shipWorldPos.y + baseCamPos.y, shipWorldPos.z + baseCamPos.z - (engPwr * 8.0) - camZLag);
                cameraLookTarget.set(shipWorldPos.x, shipWorldPos.y + baseTarget.y, shipWorldPos.z + baseTarget.z);
                cameraMain.position.lerp(cameraIdealPos, 0.05);
                cameraMain.lookAt(cameraLookTarget);
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
    }

    // 地球メガフロート＆海面表示
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

    // 地球球体
    if (altKm >= 20.0 && prog < 0.30) {
        earthGroup.visible = true;
        const earthFade = THREE.MathUtils.clamp((altKm - 20.0) / 25.0, 0.0, 1.0);
        earthShaderMat.uniforms.uOpacity.value = earthFade;
        const warpRecede = Math.pow(Math.max(0, prog - 0.05) * 18.0, 3.0);
        earthGroup.position.set(0, -25050 - altKm * 120.0 - warpRecede * 35000.0, -4000 - distM * 0.6 - warpRecede * 95000.0);
    } else {
        earthGroup.visible = false;
    }

    // 実写風マッハコーン放物線衝撃波
    if (cfg.mach_cone_vfx && (vaporA > 0.05 || pAlpha > 0.05)) {
        machConeMat.uniforms.uAlpha.value = Math.max(vaporA, pAlpha);
        machConeMesh.scale.set(1.0 + mach * 0.03, 1.0 + mach * 0.03, 1.0);
    } else {
        machConeMat.uniforms.uAlpha.value = 0.0;
    }

    // 推進炎制御（発射前は完全非表示・点火でゼロから伸長）
    if (currentTime >= -1.8 && engPwr > 0.01) {
        plumeRoot.visible = true;
        const flameLength = Math.max(0.05, Math.pow(engPwr, 1.4));
        plumeRoot.scale.set(engPwr, engPwr, flameLength);
        shockShaderMat.uniforms.uTime.value = now * 0.001;
        shockShaderMat.uniforms.uWarp.value = wAct;
        outerFlameMat.uniforms.uTime.value = now * 0.001;
    } else {
        plumeRoot.visible = false;
    }

    // アルクビエレ・ワープリング
    if (ringL > 0.01) {
        warpRingAssembly.scale.setScalar(ringL);
        warpRingAssembly.position.y = THREE.MathUtils.lerp(0.0, -0.8, ringL);
        rotorClockwise.rotation.z += 0.03 * ringL;
        rotorCounter.rotation.z -= 0.03 * ringL;
    } else {
        warpRingAssembly.scale.set(0.001, 0.001, 0.001);
    }

    // ペイロードベイ開閉
    bayDoors.forEach(bd => { bd.pivot.rotation.z = -bd.side * bayO * 1.5; });

    // 可動翼＆スピードブレーキ
    speedbrakePivot.rotation.x = speedbrake * 0.75;
    elevonMeshes.forEach(em => { em.mesh.rotation.x = Math.sin(now * 0.005) * 0.15 + THREE.MathUtils.degToRad(-pitchDeg * 0.3); });
    irisPaddles.forEach(ip => { ip.rotation.x = -0.35 + L('nozzle_open') * 0.48; });

    // ランディングギア
    landingGears.forEach(lg => { lg.scale.setScalar(Math.max(0.001, gearD)); });

    // 接地白煙
    if (tdSmoke > 0.05) {
        smokeMat.opacity = tdSmoke * 0.85;
        smokePuffs.forEach(p => {
            p.position.set((Math.random() - 0.5) * 3.5, -2.6, -6.0 - Math.random() * 8.0);
            p.scale.setScalar(1.0 + Math.random() * 2.0);
        });
    } else {
        smokeMat.opacity = 0.0;
    }

    // ドラッグシュート開傘
    if (chuteD > 0.01) {
        chuteGroup.scale.setScalar(chuteD);
        chuteCanopy.rotation.z += 0.02;
    } else {
        chuteGroup.scale.setScalar(0.001);
    }

    // 目的地描画
    if (prog > 0.76) {
        destWorld.visible = true;
        if (cfg.goal_type === "landing") {
            runwayScrollGroup.visible = true;
            orbitGoalGroup.visible = false;
            destWorld.position.y = -altKm * 1000.0;

            const rabbitStep = Math.floor((now * 0.025) % 80);
            rabbitStrobeMesh.position.z = -2500.0 - (79 - rabbitStep) * 30.0;

            if (runwaySpd > 0.1 && isPlaying) {
                runwayAccumZ += runwaySpd * delta;
                runwayScrollGroup.position.z = -(runwayAccumZ % 4800.0);
            }
        } else {
            runwayScrollGroup.visible = false;
            orbitGoalGroup.visible = true;
            dysonStation.rotation.y += 0.005;
        }
    } else {
        destWorld.visible = false;
    }

    // ワープトンネル流動
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

    // ワープPass
    let duckingFactor = 1.0;
    if (f0.phase === "WARP_FIELD_COMPRESSION" && prog > 0.14) {
        warpPass.uniforms.uInvert.value = 1.0;
        duckingFactor = 0.001;
    } else {
        warpPass.uniforms.uInvert.value = 0.0;
    }
    warpPass.uniforms.uDistort.value = wBoom * 2.8 + wAct * 0.35;
    warpPass.uniforms.uTime.value = now * 0.001;

    // 音声多層シンセ音量・周波数制御
    if (actx) {
        rocketGain.gain.setTargetAtTime(engPwr * 0.38 * duckingFactor, actx.currentTime, 0.05);
        subBassGain.gain.setTargetAtTime(engPwr * 0.28 * duckingFactor, actx.currentTime, 0.05);
        spoolGain.gain.setTargetAtTime(engPwr * 0.15 * duckingFactor, actx.currentTime, 0.05);
        if (spoolOsc) {
            spoolOsc.frequency.setTargetAtTime(240 + engPwr * 800, actx.currentTime, 0.05);
        }
    }

    drawRadar(prog, vc, mach, altKm);

    renderer.setViewport(0, 0, W, H);
    composerMain.render();

    // UIテキスト更新
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

    // 終了バナー
    if (f0.phase === "PLANETARY_RUNWAY_SECURED" || f0.phase === "ORBITAL_STATION_DOCKED") {
        completeBannerEl.style.display = 'block';
        if (f0.phase === "ORBITAL_STATION_DOCKED") {
            document.getElementById('banner-title').innerText = "ORBITAL INSERTION COMPLETE // STATION DOCKED";
            document.getElementById('banner-sub').innerText = "DYSON HUB RENDEZVOUS / STABLE LAGRANGE ORBIT SECURED";
        }
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
