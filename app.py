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
    "※ 完全映画仕様ディレクターズカット：磁気ピンチ紡錘プラズマトーチ＆立体マッハ結晶 / 中空グラビティリング＆X字4ナセル恒星間艦 / "
    "360度耐Gロールケージ＆空間3Dホログラムブリッジ / ドーム貫通防止数理設計5種SFメガストラクチャー / 電磁アレスティング減速網"
)

# =========================================================================
# 🔬 機体・動力炉・目的地・環境データベース
# =========================================================================
VESSEL_DESIGNS = {
    "第6世代極超音速ウェイブライダー『ヴァルキリー SSTO』": {
        "id": "valkyrie",
        "style": "stealth_waverider",
        "catapult_mach": 15.5,
        "desc": "中空超伝導グラビティ・リング、非対称双胴レールガン・マンディブル、X字配置4基マグネティック・ナセル、8枚可変電磁ペタルを備えた主力SSTO。",
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
        "fog_density": 0.000045,
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
        "fog_density": 0.000035,
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
        wings_span = st.slider("X字マグネティック・ナセル展開スパン (m)", 18.0, 42.0, 30.0, step=1.0)
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
        st.caption("※ 200×200実測標高プロファイル富士山・宝永火口・雲海レイヤー・7オクターブFBM海面を描画。")
        cryo_steam = st.checkbox("極低温クライオ氷片＆プラズマスパーク高速通過粒子", value=True)
        mach_cone_vfx = st.checkbox("2層流体リボン音速ヴェイパー＆熱圏プラズマ衝撃波", value=True)

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        power_sel = st.selectbox("主推進エンジンコア", list(POWER_CORES.keys()))
        power_cfg = POWER_CORES[power_sel]
        shock_count = st.slider("推進炎 立体ショックダイヤモンド結晶数", 3, 7, 5)
    with c2:
        warp_factor = st.slider("アルクビエレ時空曲率 (Warp Factor)", 2.0, 9.9, 9.2, step=0.1)
        flip_timing = st.slider("フリップ＆バーン（180°反転減速）開始地点", 0.60, 0.85, 0.74, step=0.01)

with tab4:
    c1, c2 = st.columns(2)
    with c1:
        dest_sel = st.selectbox("目標宙域", list(DESTINATIONS.keys()))
        dest_cfg = DESTINATIONS[dest_sel]
        st.caption(f"**ゴール形式:** {'🛬 惑星滑走路着陸 (ILS Gate & 電磁アレスティング網)' if dest_cfg['goal_type'] == 'landing' else '🛰️ 恒星・特異点周回軌道投入 (Orbital Insertion)'}")
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
# 💥 タイムライン物理データ
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

    total_steps = 620
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
            if not is_orbit:
                if progress < 0.88:
                    phase = "GLIDESLOPE_FINAL_APPROACH"
                    p_in = (progress - 0.78) / 0.10
                    alt_km = float(2.5 * ((1.0 - p_in * 0.92) ** 2.0))
                    mach = float(max(0.85, 3.2 * (1.0 - p_in) + 0.85 * p_in))
                    runway_spd = float(mach * 340.0)
                    vc = 0.0
                    pitch_cur = -3.0
                    roll_deg = np.sin(p_in * np.pi * 3.0) * 2.5 * (1.0 - p_in)
                    gear_d = float(np.clip(p_in * 1.8, 0.0, 1.0))
                    speedbrake = 0.85
                    g_load = 1.8
                    eng_pwr = 0.18
                    nozzle = 0.35
                    wing_sw = 0.0
                    vib = 0.08
                    progress += 0.0055 * dt

                elif progress < 0.94:
                    phase = "FINAL_FLARE_HOLD"
                    p_fl = (progress - 0.88) / 0.06
                    alt_km = float(max(0.002, 0.18 * ((1.0 - p_fl) ** 2.2)))
                    mach = float(max(0.38, 0.85 * (1.0 - p_fl * 0.55)))
                    runway_spd = float(mach * 340.0)
                    pitch_cur = -3.0 * (1.0 - p_fl) + 6.5 * p_fl
                    roll_deg = 0.0
                    gear_d = 1.0
                    speedbrake = 1.0
                    g_load = 1.3
                    eng_pwr = 0.08
                    nozzle = 0.25
                    vib = 0.05
                    progress += 0.0050 * dt

                elif progress < 0.975:
                    phase = "MAIN_GEAR_TOUCHDOWN"
                    p_td = (progress - 0.94) / 0.035
                    alt_km = 0.0
                    mach = float(max(0.22, 0.38 * (1.0 - p_td * 0.42)))
                    runway_spd = float(mach * 340.0)
                    pitch_cur = float(max(0.0, 6.5 * (1.0 - p_td * 1.3)))
                    roll_deg = 0.0
                    gear_d = 1.0
                    speedbrake = 1.0
                    chute_d = float(np.clip(p_td * 2.8, 0.0, 1.0))
                    td_smoke = float(np.clip((1.0 - p_td) * 2.6, 0.0, 1.0))
                    g_load = 1.0 + float(np.sin(p_td * np.pi)) * 0.5
                    eng_pwr = 0.0
                    nozzle = 0.2
                    vib = 0.14 * (1.0 - p_td)
                    progress += 0.0045 * dt

                else:
                    phase = "ROLLOUT_REVERSE_THRUST"
                    p_ro = (progress - 0.975) / 0.025
                    alt_km = 0.0
                    mach = float(max(0.0, 0.22 * (1.0 - p_ro)))
                    runway_spd = float(max(0.0, 75.0 * ((1.0 - p_ro) ** 1.8)))
                    pitch_cur = 0.0
                    roll_deg = 0.0
                    gear_d = 1.0
                    speedbrake = 1.0
                    chute_d = 1.0
                    td_smoke = 0.0
                    g_load = 1.0
                    eng_pwr = 0.0
                    nozzle = 0.2
                    vib = 0.03 * (1.0 - p_ro)
                    progress = min(1.0, progress + 0.0040 * dt)
            else:
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
# 📺 Three.js 完全映画仕様・超魔改造フル統合版
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
.letterbox-top{position:absolute;top:0;left:0;width:100%;height:14px;background:#000;z-index:90;pointer-events:none;}
.letterbox-bottom{position:absolute;bottom:0;left:0;width:100%;height:14px;background:#000;z-index:90;pointer-events:none;}

.hud-header-container{
  position:absolute;top:14px;left:0;width:100%;
  display:flex;flex-direction:column;z-index:50;pointer-events:auto;
}
.hud-top-bar{
  background:linear-gradient(180deg,rgba(2,6,18,0.96) 0%,rgba(4,12,28,0.88) 100%);
  border-bottom:1px solid rgba(56,189,248,0.3);
  display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;
  padding:6px 18px;gap:8px;box-shadow:0 4px 25px rgba(0,0,0,0.85);
}
.hud-left{display:flex;flex-wrap:wrap;align-items:center;gap:12px;font-size:11px;}
.badge{background:rgba(14,165,233,0.18);border:1px solid #38bdf8;color:#38bdf8;padding:2px 8px;border-radius:3px;font-weight:800;}
.cam-btn-group{display:flex;align-items:center;gap:5px;}
.cam-btn{
  background:rgba(15,23,42,0.88);border:1px solid rgba(56,189,248,0.4);color:#38bdf8;
  font-size:9.5px;font-weight:800;padding:4px 9px;border-radius:3px;cursor:pointer;
  transition:all 0.2s;
}
.cam-btn:hover{background:rgba(56,189,248,0.3);color:#fff;}
.cam-btn.active{background:#0284c7;color:#fff;border-color:#38bdf8;}

#comms-strip{
  background:rgba(2,6,23,0.85);border-bottom:1px solid rgba(16,185,129,0.3);
  padding:4px 20px;font-size:10.5px;font-family:monospace;color:#6ee7b7;letter-spacing:1px;
  pointer-events:none;display:flex;align-items:center;gap:8px;
}

#countdown-overlay{
  position:absolute;top:40%;left:50%;transform:translate(-50%,-50%);
  font-family:monospace;font-size:68px;font-weight:900;letter-spacing:6px;
  color:#38bdf8;text-shadow:0 0 35px rgba(56,189,248,0.85);
  pointer-events:none;z-index:60;display:none;text-align:center;
}

.playback-controller{
  position:absolute;bottom:156px;left:20px;right:20px;
  display:flex;align-items:center;gap:12px;background:rgba(2,6,23,0.88);
  border:1px solid rgba(56,189,248,0.35);padding:6px 14px;border-radius:6px;
  z-index:50;pointer-events:auto;backdrop-filter:blur(6px);
}
.play-btn{background:#0284c7;border:none;color:#fff;font-size:11px;font-weight:800;padding:4px 10px;border-radius:4px;cursor:pointer;}
.play-btn:hover{background:#0369a1;}
.speed-btn{background:rgba(15,23,42,0.8);border:1px solid rgba(56,189,248,0.4);color:#38bdf8;font-size:10px;font-weight:700;padding:4px 8px;border-radius:4px;cursor:pointer;}
.speed-btn.active{background:#38bdf8;color:#020617;}
.scrub-slider{flex:1;-webkit-appearance:none;height:5px;border-radius:3px;background:rgba(56,189,248,0.25);outline:none;cursor:pointer;}
.scrub-slider::-webkit-slider-thumb{-webkit-appearance:none;width:14px;height:14px;border-radius:50%;background:#38bdf8;cursor:pointer;box-shadow:0 0 8px #38bdf8;}

.radar-panel{
  position:absolute;bottom:68px;left:0;width:100%;height:82px;
  background:rgba(2,6,20,0.94);border-top:1px solid rgba(56,189,248,0.45);border-bottom:1px solid rgba(56,189,248,0.2);
  display:flex;align-items:center;padding:0 20px;gap:14px;z-index:25;pointer-events:none;
}
.radar-tag{font-size:9.5px;color:#38bdf8;font-weight:900;white-space:nowrap;letter-spacing:1px;border-right:1px solid rgba(56,189,248,0.3);padding-right:12px;line-height:1.3;}
#radar-canvas{flex:1;height:70px;display:block;}

.hud-bottom{
  position:absolute;bottom:14px;left:0;width:100%;height:54px;
  background:linear-gradient(0deg,rgba(2,6,18,0.95) 0%,rgba(6,13,30,0.85) 100%);
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
// 1. レンダラー（対数深度バッファ有効）・大気圏スカイドーム・星空
// =========================================================================
const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    powerPreference: "high-performance",
    logarithmicDepthBuffer: true
});
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.5));
renderer.setSize(W, H);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.25;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

const scene = new THREE.Scene();
const baseFogColor = new THREE.Color(cfg.env.fog_color);
scene.fog = new THREE.FogExp2(baseFogColor, cfg.env.fog_density);

const cameraMain = new THREE.PerspectiveCamera(55, W / H, 0.5, 980000);

let baseCamPos = new THREE.Vector3(-36.0, 15.0, -96.0);
let baseTarget = new THREE.Vector3(0.0, 1.5, 4.0);

if (cfg.cam_preset.includes("エクストラ")) {
    baseCamPos.set(-54.0, 24.0, -138.0);
} else if (cfg.cam_preset.includes("チェイス")) {
    baseCamPos.set(-25.0, 10.5, -72.0);
}
cameraMain.position.copy(baseCamPos);
cameraMain.lookAt(baseTarget);

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
const atmoSkyGeo = new THREE.SphereGeometry(220000, 32, 16);
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
            float sunHalo = pow(max(0.0, dot(dir, uSunDir)), 14.0) * 0.45;
            sky += vec3(1.0, 0.78, 0.52) * sunHalo;
            sky = mix(sky, vec3(0.002, 0.005, 0.015), uSpaceFade);
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

// 全天球星空
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
spaceFieldGroup.add(createRealStarField(8000, 90000, 190000, 1.8, 0xdbeafe));
spaceFieldGroup.add(createRealStarField(5000, 80000, 170000, 2.2, 0x38bdf8));
spaceFieldGroup.add(createRealStarField(4000, 70000, 150000, 1.4, 0xfcd34d));

const sunLight = new THREE.DirectionalLight(cfg.env.sun_color, cfg.env.sun_int);
sunLight.position.set(cfg.env.sun_pos[0] * 0.15, cfg.env.sun_pos[1] * 0.15 + 40.0, cfg.env.sun_pos[2] * 0.15);
sunLight.castShadow = true;
scene.add(sunLight);
scene.add(new THREE.HemisphereLight(0x93c5fd, 0x0f172a, 1.7));

const WarpDistortionShader = {
    uniforms: { "tDiffuse": { value: null }, "uDistort": { value: 0.0 }, "uInvert": { value: 0.0 }, "uTime": { value: 0.0 }, "uFlare": { value: cfg.flare_int } },
    vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `
        uniform sampler2D tDiffuse; uniform float uDistort; uniform float uInvert; uniform float uTime; uniform float uFlare; varying vec2 vUv;
        void main() {
            vec2 center = vec2(0.5, 0.5); vec2 dir = vUv - center; float dist = length(dir);
            float ringDistort = sin(dist * 22.0 - uTime * 5.0) * exp(-dist * 3.2) * uDistort * 0.045;
            vec2 rUv = vUv + dir * (dist * uDistort * 0.08 + ringDistort);
            vec2 gUv = vUv;
            vec2 bUv = vUv - dir * (dist * uDistort * 0.08 + ringDistort);
            vec3 col = vec3(texture2D(tDiffuse, rUv).r, texture2D(tDiffuse, gUv).g, texture2D(tDiffuse, bUv).b);
            float streak = exp(-abs(vUv.y - 0.5) * 48.0) * uFlare * 0.12;
            col += vec3(0.2, 0.6, 1.0) * streak;
            if (uInvert > 0.01) col = mix(col, vec3(1.0) - col, uInvert);
            gl_FragColor = vec4(col * smoothstep(0.92, 0.25, dist), 1.0);
        }
    `
};

const composerMain = new THREE.EffectComposer(renderer);
composerMain.addPass(new THREE.RenderPass(scene, cameraMain));
composerMain.addPass(new THREE.UnrealBloomPass(new THREE.Vector2(W, H), 1.15, 0.42, 0.86));
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
    radarCanvas.width = radarCanvas.clientWidth * 2.0;
    radarCanvas.height = radarCanvas.clientHeight * 2.0;
}
window.addEventListener('resize', updateCameraAspect);
updateCameraAspect();

// =========================================================================
// 2. 音響合成（Brown Noise + WaveShaper + 42Hz SubBass）
// =========================================================================
let actx = null;
let rocketGain = null, rocketLpf = null, rocketReso = null;
let crackleGain = null, crackleShaper = null;
let subBassGain = null, subBassOsc = null;
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

function playBeep(freq, dur) {
    if (!actx) return;
    try {
        const osc = actx.createOscillator();
        const g = actx.createGain();
        osc.frequency.setValueAtTime(freq, actx.currentTime);
        g.gain.setValueAtTime(0.15, actx.currentTime);
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

function makeDistortionCurve(amount) {
    const k = typeof amount === 'number' ? amount : 50,
        n_samples = 44100,
        curve = new Float32Array(n_samples),
        deg = Math.PI / 180;
    for (let i = 0; i < n_samples; ++i) {
        let x = (i * 2) / n_samples - 1;
        curve[i] = ((3 + k) * x * 20 * deg) / (Math.PI + k * Math.abs(x));
    }
    return curve;
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

        const bufSize = actx.sampleRate * 2;
        const noiseBuf = actx.createBuffer(1, bufSize, actx.sampleRate);
        const output = noiseBuf.getChannelData(0);
        let lastOut = 0.0;
        for (let i = 0; i < bufSize; i++) {
            const white = Math.random() * 2 - 1;
            lastOut = (lastOut + (0.025 * white)) / 1.025;
            output[i] = lastOut * 3.5;
        }
        const brownNoiseSource = actx.createBufferSource();
        brownNoiseSource.buffer = noiseBuf;
        brownNoiseSource.loop = true;

        rocketLpf = actx.createBiquadFilter();
        rocketLpf.type = 'lowpass';
        rocketLpf.frequency.value = 180;

        rocketReso = actx.createBiquadFilter();
        rocketReso.type = 'bandpass';
        rocketReso.frequency.value = 90;
        rocketReso.Q.value = 3.5;

        rocketGain = actx.createGain();
        rocketGain.gain.value = 0.0001;

        brownNoiseSource.connect(rocketLpf);
        rocketLpf.connect(rocketGain);
        brownNoiseSource.connect(rocketReso);
        rocketReso.connect(rocketGain);
        rocketGain.connect(actx.destination);

        crackleShaper = actx.createWaveShaper();
        crackleShaper.curve = makeDistortionCurve(120);
        crackleShaper.oversample = '4x';
        crackleGain = actx.createGain();
        crackleGain.gain.value = 0.0001;

        rocketLpf.connect(crackleShaper);
        crackleShaper.connect(crackleGain);
        crackleGain.connect(actx.destination);

        brownNoiseSource.start(0);

        subBassOsc = actx.createOscillator();
        subBassOsc.type = 'sine';
        subBassOsc.frequency.value = 42;
        subBassGain = actx.createGain();
        subBassGain.gain.value = 0.0001;
        subBassOsc.connect(subBassGain);
        subBassGain.connect(actx.destination);
        subBassOsc.start(0);
    } catch(e){}
}
window.addEventListener('pointerdown', initAudioSystem, { once: false });

// =========================================================================
// 3. 高精細PBRテクスチャ＆黒体放射サーマルマテリアル
// =========================================================================
function makeMasterPbrTexture() {
    const c = document.createElement('canvas'); c.width = 1024; c.height = 1024;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#334155'; ctx.fillRect(0, 0, 1024, 1024);

    for (let x = 0; x < 1024; x += 64) {
        for (let y = 0; y < 1024; y += 32) {
            const v = 65 + Math.floor(Math.random() * 45);
            ctx.fillStyle = `rgb(${v},${v+4},${v+10})`;
            ctx.fillRect(x + 2, y + 2, 60, 28);
            ctx.fillStyle = '#090d16';
            ctx.fillRect(x + 6, y + 6, 2, 2); ctx.fillRect(x + 54, y + 6, 2, 2);
            ctx.fillRect(x + 6, y + 22, 2, 2); ctx.fillRect(x + 54, y + 22, 2, 2);
            if (Math.random() > 0.55) {
                ctx.fillStyle = 'rgba(15,23,42,0.4)'; ctx.fillRect(x + 2, y + 24, 60, 6);
            }
        }
    }
    ctx.strokeStyle = '#0f172a'; ctx.lineWidth = 2.5;
    for (let x = 0; x <= 1024; x += 64) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, 1024); ctx.stroke(); }
    for (let y = 0; y <= 1024; y += 32) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(1024, y); ctx.stroke(); }

    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.RepeatWrapping; tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(4, 4);
    return tex;
}
const masterHullTex = makeMasterPbrTexture();

const matHull = new THREE.MeshPhysicalMaterial({
    color: cfg.hull_color,
    metalness: cfg.metalness,
    roughness: cfg.roughness,
    bumpMap: masterHullTex,
    bumpScale: 0.06,
    clearcoat: 0.85,
    clearcoatRoughness: 0.15
});
const matBellyTile = new THREE.MeshStandardMaterial({
    color: cfg.belly_color,
    metalness: 0.35,
    roughness: 0.78,
    bumpMap: masterHullTex,
    bumpScale: 0.08,
    emissive: new THREE.Color(0xff3300),
    emissiveIntensity: 0.0
});
const matTitaniumFrame = new THREE.MeshStandardMaterial({ color: 0x64748b, metalness: 0.94, roughness: 0.18 });
const matDarkAlloy = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.92, roughness: 0.24 });
const matGoldMLI = new THREE.MeshStandardMaterial({ color: 0xf59e0b, metalness: 0.96, roughness: 0.18 });
const matCopperCoil = new THREE.MeshStandardMaterial({ color: 0xd97706, metalness: 0.95, roughness: 0.15 });
const matCanopy = new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, metalness: 0.92, roughness: 0.04, transparent: true, opacity: 0.32 });
const matCryoPipe = new THREE.MeshStandardMaterial({ color: 0xdbeafe, roughness: 0.55, metalness: 0.35 });
const matCoreVein = new THREE.MeshBasicMaterial({ color: cfg.flame_hex });
const matRadiatorGlow = new THREE.MeshStandardMaterial({
    color: 0x1e293b,
    metalness: 0.85,
    roughness: 0.3,
    emissive: new THREE.Color(0xff4500),
    emissiveIntensity: 0.0
});

// =========================================================================
// 4. 【魔改造2】ハリボテ戦闘機の廃止 ➔「超精密・多層ハードSF恒星間航行艦」への1からの再設計
// 中空グラビティリング ＋ 非対称双胴レールガン・マンディブル ＋ X字配置4基マグネティック・ナセル ＋ 120超Greeble装甲
// =========================================================================
const radAngle = THREE.MathUtils.degToRad(cfg.env.angle_deg);
const shipRoot = new THREE.Group();
scene.add(shipRoot);

const shipPitchGroup = new THREE.Group();
shipRoot.add(shipPitchGroup);

const shipMeshGroup = new THREE.Group();
shipPitchGroup.add(shipMeshGroup);

// コックピットカメラ視点アンカー
const cockpitCamAnchor = new THREE.Object3D();
cockpitCamAnchor.position.set(0, 1.45, 9.6);
cockpitCamAnchor.rotation.y = Math.PI;
shipMeshGroup.add(cockpitCamAnchor);

// --- 4-1. 中心構造：中空の超伝導グラビティ・リング（常時回転する二重粒子加速バレル） ---
const spineGroup = new THREE.Group();
shipMeshGroup.add(spineGroup);

// 前後2つの重厚トラス基部（中央は中空リングが貫通する）
const frontTrussCore = new THREE.Mesh(new THREE.BoxGeometry(1.7, 1.25, 11.5), matTitaniumFrame);
frontTrussCore.position.set(0, 0.0, 8.5);
spineGroup.add(frontTrussCore);

const rearTrussCore = new THREE.Mesh(new THREE.BoxGeometry(2.1, 1.45, 11.0), matTitaniumFrame);
rearTrussCore.position.set(0, 0.0, -9.5);
spineGroup.add(rearTrussCore);

// 左右メイン・構造ビーム（中空グラビティリングを両側から支持）
for (let s of [-1, 1]) {
    const sideBeam = new THREE.Mesh(new THREE.BoxGeometry(0.65, 1.05, 31.0), matDarkAlloy);
    sideBeam.position.set(s * 2.25, 0.0, -0.5);
    spineGroup.add(sideBeam);

    // 装甲の隙間から覗く発光プラズマ・エネルギーヴェイン
    const energyVein = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.13, 30.0, 12), matCoreVein);
    energyVein.rotation.x = Math.PI / 2;
    energyVein.position.set(s * 1.75, 0.35, -0.5);
    spineGroup.add(energyVein);

    // 黄金MLI（多層断熱材）極低温クライオタンク列（片側4基×2＝8基）
    for (let tk = 0; tk < 4; tk++) {
        const tank = new THREE.Mesh(new THREE.SphereGeometry(0.72, 16, 16), matGoldMLI);
        tank.scale.set(0.85, 0.85, 1.45);
        tank.position.set(s * 1.42, -0.45, 6.5 - tk * 4.2);
        spineGroup.add(tank);
    }

    // 立体カーブ高圧プラズマ導管パイプ束
    const pipePts = [
        new THREE.Vector3(s * 1.5, -0.35, 13.0),
        new THREE.Vector3(s * 2.6, -0.15, 4.5),
        new THREE.Vector3(s * 2.8, -0.25, -4.5),
        new THREE.Vector3(s * 1.2, -0.05, -14.8)
    ];
    spineGroup.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pipePts), 36, 0.13, 10, false), matCryoPipe));
}

// 中央の常時回転・中空超伝導グラビティ・リング（二重粒子加速バレル）
const gravityHullRingGroup = new THREE.Group();
gravityHullRingGroup.position.set(0, 0.05, -0.8);
spineGroup.add(gravityHullRingGroup);

const gravityOuterBarrel = new THREE.Group();
const gravityInnerBarrel = new THREE.Group();
gravityHullRingGroup.add(gravityOuterBarrel);
gravityHullRingGroup.add(gravityInnerBarrel);

const mainGravityTorus = new THREE.Mesh(new THREE.TorusGeometry(3.4, 0.32, 14, 48), matTitaniumFrame);
gravityOuterBarrel.add(mainGravityTorus);
const innerGravityTorus = new THREE.Mesh(new THREE.TorusGeometry(2.75, 0.18, 12, 48), matCopperCoil);
gravityInnerBarrel.add(innerGravityTorus);

for (let seg = 0; seg < 12; seg++) {
    const a = (seg / 12) * Math.PI * 2;
    const node = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.55, 0.85), matDarkAlloy);
    node.position.set(Math.cos(a) * 3.4, Math.sin(a) * 3.4, 0);
    node.rotation.z = a;
    gravityOuterBarrel.add(node);

    const glowSlit = new THREE.Mesh(new THREE.BoxGeometry(0.22, 0.22, 0.92), matCoreVein);
    glowSlit.position.set(Math.cos(a) * 3.4, Math.sin(a) * 3.4, 0);
    glowSlit.rotation.z = a;
    gravityOuterBarrel.add(glowSlit);
}

// --- 4-2. 非対称・双胴レールガン・マンディブル（電磁加速顎） ---
for (let s of [-1, 1]) {
    const isLeft = (s === -1);
    const mandibleLen = isLeft ? 10.8 : 9.4; // 非対称ハードSFバランス
    const mandibleGroup = new THREE.Group();
    mandibleGroup.position.set(s * 1.48, -0.05, 11.8);
    shipMeshGroup.add(mandibleGroup);

    // 多面体分割アーマー外装
    const mShape = new THREE.Shape();
    mShape.moveTo(0, 0);
    mShape.lineTo(s * 1.35, -1.6);
    mShape.lineTo(s * 0.48, mandibleLen);
    mShape.lineTo(-s * 0.32, mandibleLen - 0.8);
    mShape.closePath();

    const mGeo = new THREE.ExtrudeGeometry(mShape, { depth: 0.58, bevelThickness: 0.16, bevelSize: 0.14 });
    const mMesh = new THREE.Mesh(mGeo, matHull);
    mMesh.rotation.x = Math.PI / 2;
    mMesh.position.y = 0.32;
    mMesh.castShadow = true;
    mandibleGroup.add(mMesh);

    // 露出電磁加速コイル列（6段の銅コイル＋プラズマ電極レール）
    const railElectrode = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.15, mandibleLen - 1.2), matCoreVein);
    railElectrode.position.set(-s * 0.24, 0.04, mandibleLen * 0.48);
    mandibleGroup.add(railElectrode);

    for (let rc = 0; rc < 6; rc++) {
        const coilBlock = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.42, 0.35), matCopperCoil);
        coilBlock.position.set(s * 0.12, 0.05, 1.5 + rc * 1.25);
        mandibleGroup.add(coilBlock);
    }

    // 非対称先端センサーブレード＆量子通信アンテナ
    const sensorTip = new THREE.Mesh(new THREE.ConeGeometry(0.15, isLeft ? 2.2 : 1.3, 6), matTitaniumFrame);
    sensorTip.rotation.x = Math.PI / 2;
    sensorTip.position.set(s * 0.08, 0.04, mandibleLen + 0.6);
    mandibleGroup.add(sensorTip);
}

// --- 4-3. 脱ハリボテ・超高密度Greebleマイクロ装甲パネル（InstancedMesh + 複合モジュール） ---
const armorShellGroup = new THREE.Group();
shipMeshGroup.add(armorShellGroup);

// コックピット・コマンドモジュール（多面体装甲ポッド）
const noseCore = new THREE.Mesh(new THREE.CylinderGeometry(0.78, 2.15, 9.2, 6), matHull);
noseCore.rotation.x = Math.PI / 2;
noseCore.rotation.z = Math.PI / 6;
noseCore.position.set(0, 0.42, 9.6);
armorShellGroup.add(noseCore);

// 段差のある分割マイクロ装甲タイル（InstancedMeshで120枚の立体パネルを生成）
const greebleCount = 120;
const greebleInst = new THREE.InstancedMesh(new THREE.BoxGeometry(0.95, 0.16, 1.65), matHull, greebleCount);
const dummyGreeble = new THREE.Object3D();
let gIdx = 0;
for (let s of [-1, 1]) {
    for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 20; col++) {
            if (gIdx >= greebleCount) break;
            const gz = 11.5 - col * 1.25;
            // 中央グラビティリング部分（z: -3.2 ~ 1.6）は避けてリングを露出させる
            if (gz > -3.2 && gz < 1.6 && row === 0) continue;
            const gx = s * (1.55 + row * 0.68);
            const gy = 0.58 - row * 0.22 + ((col + row) % 2) * 0.06;
            dummyGreeble.position.set(gx, gy, gz);
            dummyGreeble.rotation.set(0, s * 0.05, -s * (0.12 + row * 0.14));
            dummyGreeble.scale.set(0.85 + (col % 3) * 0.15, 1.0, 0.88);
            dummyGreeble.updateMatrix();
            greebleInst.setMatrixAt(gIdx++, dummyGreeble.matrix);
        }
    }
}
greebleInst.count = gIdx;
armorShellGroup.add(greebleInst);

// 発光冷却ルーバー（放熱スリット）＆油圧アクチュエータ・シリンダー群
for (let s of [-1, 1]) {
    for (let tIdx = 0; tIdx < 6; tIdx++) {
        const bellyPanel = new THREE.Mesh(new THREE.BoxGeometry(2.1, 0.24, 3.7), matBellyTile);
        bellyPanel.position.set(s * 1.45, -0.82, 8.0 - tIdx * 4.1);
        bellyPanel.rotation.z = s * 0.1;
        armorShellGroup.add(bellyPanel);
    }

    for (let lv = 0; lv < 5; lv++) {
        const lz = -4.2 - lv * 2.1;
        const louverBox = new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.28, 1.35), matDarkAlloy);
        louverBox.position.set(s * 3.15, 0.35, lz);
        armorShellGroup.add(louverBox);

        const louverGlow = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.08, 1.15), matRadiatorGlow);
        louverGlow.position.set(s * 3.15, 0.35, lz);
        armorShellGroup.add(louverGlow);

        // 油圧アクチュエータ・シリンダー
        const pistonRod = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 1.6, 8), matTitaniumFrame);
        pistonRod.rotation.z = s * 0.85;
        pistonRod.position.set(s * 2.75, 0.65, lz);
        armorShellGroup.add(pistonRod);
    }
}

// --- 4-4. 【魔改造2】X字配置された4基の独立可動マグネティック・スラスターナセル（翼の代替） ---
const halfSpan = cfg.wings_span * 0.5;
const wingPivots = [];
const elevonMeshes = [];
const navLights = [];
const strobeLights = [];

// X字4象限の配置角度（右上、右下、左上、左下）
const xConfigs = [
    { sx: -1, sy: 1, tilt: 0.34, zPos: -3.5, scale: 1.0 },
    { sx: 1,  sy: 1, tilt: -0.34, zPos: -3.5, scale: 1.0 },
    { sx: -1, sy: -1, tilt: -0.28, zPos: -6.8, scale: 0.78 },
    { sx: 1,  sy: -1, tilt: 0.28, zPos: -6.8, scale: 0.78 }
];

xConfigs.forEach((xc, idx) => {
    const pivot = new THREE.Group();
    pivot.position.set(xc.sx * 2.8, xc.sy * 0.35, xc.zPos);
    pivot.rotation.z = xc.tilt;
    shipMeshGroup.add(pivot);

    const armLen = (halfSpan - 2.8) * xc.scale;

    // 構造パイロンアーム（トラス＋装甲）
    const pylonArm = new THREE.Mesh(new THREE.BoxGeometry(armLen, 0.32, 2.4), matHull);
    pylonArm.position.set(xc.sx * (armLen * 0.5), 0, -1.2);
    pivot.add(pylonArm);

    const pylonTruss = new THREE.Mesh(new THREE.BoxGeometry(armLen * 0.9, 0.42, 0.85), matTitaniumFrame);
    pylonTruss.position.set(xc.sx * (armLen * 0.5), 0, -0.2);
    pivot.add(pylonTruss);

    // 油圧リンクシリンダー
    const hydPiston = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.14, armLen * 0.55, 8), matCopperCoil);
    hydPiston.rotation.z = Math.PI / 2;
    hydPiston.position.set(xc.sx * (armLen * 0.35), -xc.sy * 0.32, -1.2);
    pivot.add(hydPiston);

    // 先端マグネティック・スラスターナセルポッド
    const nacelleGroup = new THREE.Group();
    nacelleGroup.position.set(xc.sx * armLen, 0, -1.5);
    pivot.add(nacelleGroup);

    const nacelleBody = new THREE.Mesh(new THREE.CylinderGeometry(0.68, 0.82, 6.8, 8), matDarkAlloy);
    nacelleBody.rotation.x = Math.PI / 2;
    nacelleGroup.add(nacelleBody);

    const nacelleCore = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 7.1, 12), matCoreVein);
    nacelleCore.rotation.x = Math.PI / 2;
    nacelleGroup.add(nacelleCore);

    // 可動制御フィン
    const elMesh = new THREE.Mesh(new THREE.BoxGeometry(armLen * 0.55, 0.14, 1.1), matDarkAlloy);
    elMesh.position.set(xc.sx * (armLen * 0.55), 0, -2.6);
    pivot.add(elMesh);
    elevonMeshes.push({ mesh: elMesh, side: xc.sx });

    // 上段ナセル先端にナビゲーションライト＆ストロボ配置
    if (xc.sy > 0) {
        const navCol = (xc.sx === -1) ? 0xef4444 : 0x10b981;
        const nLight = new THREE.Mesh(new THREE.SphereGeometry(0.22, 8, 8), new THREE.MeshBasicMaterial({ color: navCol }));
        nLight.position.set(0, 0.95, 2.2);
        nacelleGroup.add(nLight);
        navLights.push(nLight);

        const strLight = new THREE.Mesh(new THREE.SphereGeometry(0.25, 8, 8), new THREE.MeshBasicMaterial({ color: 0xffffff }));
        strLight.position.set(0, 1.05, -2.5);
        nacelleGroup.add(strLight);
        strobeLights.push(strLight);
    }

    wingPivots.push({ group: pivot, side: xc.sx, baseTilt: xc.tilt });
});

// --- 4-5. 可変ペイロードベイ＆3軸重力制御ジャイロ＋展開式クアッド放熱ラジエーター ---
const bayDoors = [];
for (let s of [-1, 1]) {
    const doorPivot = new THREE.Group();
    doorPivot.position.set(s * 2.1, 1.08, -7.2);
    shipMeshGroup.add(doorPivot);
    const dPanel = new THREE.Mesh(new THREE.BoxGeometry(2.05, 0.22, 7.5), matHull);
    dPanel.position.set(-s * 1.0, 0, 0);
    doorPivot.add(dPanel);
    bayDoors.push({ pivot: doorPivot, side: s });
}

const warpRingAssembly = new THREE.Group();
warpRingAssembly.position.set(0, 0.35, -7.2);
warpRingAssembly.scale.set(0.001, 0.001, 0.001);
shipMeshGroup.add(warpRingAssembly);

const rotorClockwise = new THREE.Group();
const rotorCounter = new THREE.Group();
const gyroGimbalInner = new THREE.Group();
warpRingAssembly.add(rotorClockwise);
warpRingAssembly.add(rotorCounter);
warpRingAssembly.add(gyroGimbalInner);

for (let i = 0; i < 20; i++) {
    const segPivot = new THREE.Group();
    segPivot.rotation.z = (i / 20) * Math.PI * 2;
    rotorClockwise.add(segPivot);
    const block = new THREE.Mesh(new THREE.BoxGeometry(1.05, 0.4, 1.5), matDarkAlloy);
    block.position.set(0, 5.8, 0);
    segPivot.add(block);
    const coilCore = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.3, 1.2), new THREE.MeshBasicMaterial({ color: cfg.aurora_hex }));
    coilCore.position.set(0, 5.8, 0);
    segPivot.add(coilCore);
}
rotorCounter.add(new THREE.Mesh(new THREE.TorusGeometry(5.0, 0.16, 12, 48), matCopperCoil));
gyroGimbalInner.add(new THREE.Mesh(new THREE.TorusGeometry(3.9, 0.14, 12, 48), matTitaniumFrame));

const radiatorPivots = [];
const radCount = Math.max(2, cfg.radiator_fins);
for (let r = 0; r < radCount; r++) {
    const side = (r % 2 === 0) ? -1 : 1;
    const zOffset = -5.5 - Math.floor(r / 2) * 2.6;
    const rPivot = new THREE.Group();
    rPivot.position.set(side * 2.4, 0.95, zOffset);
    const rFin = new THREE.Mesh(new THREE.BoxGeometry(4.8, 0.08, 1.3), matRadiatorGlow);
    rFin.position.set(side * 2.4, 0, 0);
    rPivot.add(rFin);
    rPivot.scale.set(0.001, 1, 1);
    shipMeshGroup.add(rPivot);
    radiatorPivots.push({ pivot: rPivot, side: side });
}

// 背面スピードエアブレーキ
const speedbrakePivot = new THREE.Group();
speedbrakePivot.position.set(0, 1.28, -9.8);
shipMeshGroup.add(speedbrakePivot);
const speedbrakeMesh = new THREE.Mesh(new THREE.BoxGeometry(2.5, 0.18, 3.8), matTitaniumFrame);
speedbrakeMesh.position.set(0, 0, -1.9);
speedbrakePivot.add(speedbrakeMesh);

// 3点式ヘビーデューティ・ランディングギア
const landingGears = [];
[{ x: 0, y: -0.5, z: 10.5 }, { x: -3.8, y: -0.6, z: -7.5 }, { x: 3.8, y: -0.6, z: -7.5 }].forEach((gp) => {
    const gPivot = new THREE.Group();
    gPivot.position.set(gp.x, gp.y, gp.z);
    const strut = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 2.6, 8), matTitaniumFrame);
    strut.position.y = -1.3;
    gPivot.add(strut);
    const footPad = new THREE.Mesh(new THREE.CylinderGeometry(0.48, 0.55, 0.22, 12), matDarkAlloy);
    footPad.position.y = -2.6;
    gPivot.add(footPad);
    gPivot.scale.set(0.001, 0.001, 0.001);
    shipMeshGroup.add(gPivot);
    landingGears.push(gPivot);
});

// 接地白煙パーティクル
const smokeCount = 30;
const smokePuffs = [];
const smokeGeo = new THREE.SphereGeometry(1.2, 8, 8);
const smokeMat = new THREE.MeshBasicMaterial({ color: 0xe2e8f0, transparent: true, opacity: 0.0 });
for (let sm = 0; sm < smokeCount; sm++) {
    const p = new THREE.Mesh(smokeGeo, smokeMat.clone());
    p.position.set((Math.random() - 0.5) * 4.5, -2.6, -6.0 - Math.random() * 45.0);
    p.scale.setScalar(1.0 + Math.random() * 2.5);
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

// --- 4-6. 【魔改造2】可変ベクター・8枚電磁ペタルノズル＋24枚アイリス ---
const nozzleGimbalRoot = new THREE.Group();
nozzleGimbalRoot.position.set(0, 0, -15.0);
shipMeshGroup.add(nozzleGimbalRoot);

const turbineCore = new THREE.Mesh(new THREE.SphereGeometry(1.75, 16, 16), new THREE.MeshBasicMaterial({ color: cfg.flame_hex }));
turbineCore.position.set(0, 0, 0.5);
nozzleGimbalRoot.add(turbineCore);

const irisPaddles = [];
for (let i = 0; i < 24; i++) {
    const ang = (i / 24) * Math.PI * 2;
    const pPivot = new THREE.Group();
    pPivot.position.set(Math.cos(ang) * 2.35, Math.sin(ang) * 2.35, -0.8);
    pPivot.rotation.z = ang;
    nozzleGimbalRoot.add(pPivot);
    const blade = new THREE.Mesh(new THREE.BoxGeometry(0.54, 0.09, 3.0), (i % 2 === 0) ? matTitaniumFrame : matDarkAlloy);
    blade.position.set(0, 0.05, -1.2);
    pPivot.add(blade);
    irisPaddles.push(pPivot);
}

// 外周8枚の可変ベクター・電磁シールドペタル＆油圧リンク
const emPetals = [];
for (let p = 0; p < 8; p++) {
    const ang = (p / 8) * Math.PI * 2 + Math.PI / 8;
    const petalPivot = new THREE.Group();
    petalPivot.position.set(Math.cos(ang) * 2.85, Math.sin(ang) * 2.85, -0.4);
    petalPivot.rotation.z = ang;
    nozzleGimbalRoot.add(petalPivot);

    const petalPlate = new THREE.Mesh(new THREE.BoxGeometry(1.35, 0.16, 4.4), matHull);
    petalPlate.position.set(0, 0.18, -1.9);
    petalPivot.add(petalPlate);

    const petalCoil = new THREE.Mesh(new THREE.BoxGeometry(0.45, 0.18, 3.8), matCoreVein);
    petalCoil.position.set(0, 0.08, -1.9);
    petalPivot.add(petalCoil);

    const petalLink = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2.2, 8), matTitaniumFrame);
    petalLink.rotation.x = Math.PI / 3;
    petalLink.position.set(0, 0.55, -0.8);
    petalPivot.add(petalLink);

    emPetals.push({ pivot: petalPivot, index: p });
}

// キャノピーガラス
const canopyGlass = new THREE.Mesh(new THREE.SphereGeometry(1.55, 24, 16, 0, Math.PI * 2, 0, Math.PI * 0.5), matCanopy);
canopyGlass.scale.set(0.95, 0.62, 2.75);
canopyGlass.position.set(0, 1.25, 9.8);
shipMeshGroup.add(canopyGlass);

// =========================================================================
// 【魔改造1】ラッパ型バーナーの完全廃止 ➔「磁気ピンチ・プラズマトーチ＆立体マッハディスク」
// =========================================================================
const plumeRoot = new THREE.Group();
plumeRoot.position.set(0, 0, -2.2);
plumeRoot.visible = false;
nozzleGimbalRoot.add(plumeRoot);

// 紡錘形（スピンドル）旋盤プロフィール生成関数（根元から膨らみ、磁気ピンチで鋭く収束）
function createSpindlePlumeGeometry(maxRadius, length) {
    const pts = [];
    const segs = 28;
    for (let i = 0; i <= segs; i++) {
        const t = i / segs; // 0: ノズル出口, 1: 炎の先端
        // ノズル直後(t=0.14)で膨張し、その後磁気ピンチで針のように鋭く収束する曲線
        const envelope = Math.sin(Math.pow(t, 0.52) * Math.PI) * Math.pow(1.0 - t, 0.65);
        const r = Math.max(0.01, maxRadius * envelope * 1.48);
        const y = t * length;
        pts.push(new THREE.Vector2(r, y));
    }
    const geo = new THREE.LatheGeometry(pts, 32);
    // LatheGeometryは+Y方向に伸びるため、-Z後方へ向くように回転
    geo.rotateX(-Math.PI / 2);
    return geo;
}

// 1-1. 内層：超高輝度ホワイトプラズマ・スピンドルコア
const innerSpindleGeo = createSpindlePlumeGeometry(1.15, 26.0);
const innerCoreMesh = new THREE.Mesh(
    innerSpindleGeo,
    new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.96, blending: THREE.AdditiveBlending, depthWrite: false })
);
plumeRoot.add(innerCoreMesh);

// 1-2. 中層：磁気ピンチ脈動プラズマ・スピンドルシース
const midSpindleGeo = createSpindlePlumeGeometry(2.25, 38.0);
const shockShaderMat = new THREE.ShaderMaterial({
    vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `
        varying vec2 vUv; uniform float uTime; uniform vec3 uColor; uniform float uWarp;
        void main() {
            float pulse = 0.65 + 0.35 * sin(vUv.y * 42.0 - uTime * 38.0);
            float pinch = sin(vUv.y * 3.14159);
            vec3 c = mix(uColor, vec3(0.35, 0.88, 1.0), uWarp);
            gl_FragColor = vec4(c, pulse * pinch * 0.85);
        }
    `,
    uniforms: { uTime: { value: 0.0 }, uColor: { value: new THREE.Color(cfg.flame_hex) }, uWarp: { value: 0.0 } },
    transparent: true, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false
});
const midSpindleMesh = new THREE.Mesh(midSpindleGeo, shockShaderMat);
plumeRoot.add(midSpindleMesh);

// 1-3. 外層：イオン化プラズマ・ハローコロナ（極細収束テール）
const outerSpindleGeo = createSpindlePlumeGeometry(3.15, 48.0);
const outerFlameMat = new THREE.ShaderMaterial({
    vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `
        varying vec2 vUv; uniform float uTime; uniform vec3 uColor;
        void main() {
            float filament = 0.55 + 0.45 * sin(vUv.x * 24.0 + vUv.y * 18.0 - uTime * 24.0);
            float fade = sin(vUv.y * 3.14159) * (1.0 - vUv.y);
            gl_FragColor = vec4(uColor, filament * fade * 0.48);
        }
    `,
    uniforms: { uTime: { value: 0.0 }, uColor: { value: new THREE.Color(cfg.spark_hex) } },
    transparent: true, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false
});
const outerFlameMesh = new THREE.Mesh(outerSpindleGeo, outerFlameMat);
plumeRoot.add(outerFlameMesh);

// 1-4. 独立した立体ショックダイヤモンド（マッハディスク結晶コーン群）
const shockDiamonds = [];
const diamondMat = new THREE.MeshBasicMaterial({
    color: 0xffffff,
    transparent: true,
    opacity: 0.92,
    blending: THREE.AdditiveBlending,
    depthWrite: false
});
const shockCrystalCount = Math.max(3, cfg.shock_count);
for (let sd = 0; sd < shockCrystalCount; sd++) {
    const dGroup = new THREE.Group();
    const scaleDecay = Math.pow(0.84, sd);
    const frontCone = new THREE.Mesh(new THREE.ConeGeometry(0.95 * scaleDecay, 1.8 * scaleDecay, 16), diamondMat);
    frontCone.rotation.x = Math.PI / 2;
    frontCone.position.z = 0.9 * scaleDecay;
    const backCone = new THREE.Mesh(new THREE.ConeGeometry(0.95 * scaleDecay, 2.4 * scaleDecay, 16), diamondMat);
    backCone.rotation.x = -Math.PI / 2;
    backCone.position.z = -1.2 * scaleDecay;
    dGroup.add(frontCone, backCone);
    dGroup.position.z = -3.8 - sd * 4.8;
    plumeRoot.add(dGroup);
    shockDiamonds.push({ group: dGroup, index: sd, baseScale: scaleDecay });
}

// 1-5. 磁気コンファインメント・プラズマリング（後方へ高速移動しながら収縮する8連発光トーラス）
const magneticRings = [];
const magRingMat = new THREE.MeshBasicMaterial({
    color: cfg.flame_hex,
    transparent: true,
    opacity: 0.78,
    blending: THREE.AdditiveBlending,
    depthWrite: false
});
for (let mr = 0; mr < 8; mr++) {
    const ringMesh = new THREE.Mesh(new THREE.TorusGeometry(2.35, 0.08, 8, 32), magRingMat);
    plumeRoot.add(ringMesh);
    magneticRings.push({ mesh: ringMesh, phaseOffset: mr / 8.0 });
}

// =========================================================================
// 【魔改造3】コクピット内装の超精密メカ化（360度SFブリッジ＆空間ホログラム計器）
// =========================================================================
const cockpitInteriorGroup = new THREE.Group();
cockpitCamAnchor.add(cockpitInteriorGroup);

const matCockpitCarbon = new THREE.MeshStandardMaterial({ color: 0x090d16, roughness: 0.42, metalness: 0.78 });
const matCockpitFrame = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.25, metalness: 0.92 });
const matSwitchRed = new THREE.MeshBasicMaterial({ color: 0xef4444 });
const matSwitchCyan = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
const matSwitchAmber = new THREE.MeshBasicMaterial({ color: 0xf59e0b });

// 3-1. 多角形トラス構造の耐Gロールケージ＆Gフォース連動油圧ダンパー
const rollCageGroup = new THREE.Group();
cockpitInteriorGroup.add(rollCageGroup);

[-0.72, 0.72].forEach(px => {
    // メインAピラー装甲フレーム
    const aPillar = new THREE.Mesh(new THREE.BoxGeometry(0.068, 1.18, 0.088), matCockpitFrame);
    aPillar.position.set(px, 0.22, -0.86);
    aPillar.rotation.set(-0.38, 0, (px > 0 ? -1 : 1) * 0.22);
    rollCageGroup.add(aPillar);

    // サブトラス補強バー（サイドウインドウ枠）
    const sideRollBar = new THREE.Mesh(new THREE.CylinderGeometry(0.022, 0.022, 1.25, 8), matTitaniumFrame);
    sideRollBar.position.set(px * 1.12, 0.38, -0.35);
    sideRollBar.rotation.set(Math.PI / 2.2, 0, (px > 0 ? -1 : 1) * 0.15);
    rollCageGroup.add(sideRollBar);

    // リベット列
    for (let rv = 0; rv < 6; rv++) {
        const rivet = new THREE.Mesh(new THREE.SphereGeometry(0.012, 6, 6), matTitaniumFrame);
        rivet.position.set(px * 0.96, -0.15 + rv * 0.14, -0.94 + rv * 0.055);
        rollCageGroup.add(rivet);
    }
});

// Gフォース連動・油圧ダンパーシリンダー（左右計器盤フレームを支持）
const cabinDampers = [];
[-0.48, 0.48].forEach(dx => {
    const damperOuter = new THREE.Mesh(new THREE.CylinderGeometry(0.026, 0.026, 0.28, 10), matDarkAlloy);
    damperOuter.position.set(dx, -0.18, -0.92);
    damperOuter.rotation.x = 0.45;
    cockpitInteriorGroup.add(damperOuter);

    const damperPiston = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.24, 10), matCopperCoil);
    damperPiston.position.set(dx, -0.14, -0.88);
    damperPiston.rotation.x = 0.45;
    cockpitInteriorGroup.add(damperPiston);
    cabinDampers.push(damperPiston);
});

// 天井からダッシュボードへ繋がる太い編み込み冷却ホースと光ファイバー束
for (let h = 0; h < 4; h++) {
    const side = (h < 2) ? -1 : 1;
    const offset = (h % 2) * 0.045;
    const hoseCurve = new THREE.CatmullRomCurve3([
        new THREE.Vector3(side * (0.28 + offset), 0.65, -0.45),
        new THREE.Vector3(side * (0.64 + offset), 0.35, -0.78),
        new THREE.Vector3(side * (0.68 + offset), -0.15, -0.88)
    ]);
    const hoseMat = (h % 2 === 0) ? matCryoPipe : new THREE.MeshBasicMaterial({ color: 0x38bdf8 });
    const hoseMesh = new THREE.Mesh(new THREE.TubeGeometry(hoseCurve, 20, h % 2 === 0 ? 0.018 : 0.008, 8, false), hoseMat);
    cockpitInteriorGroup.add(hoseMesh);
}

// 3-2. 湾曲メインダッシュボード＆物理量子ジャイロコア（中央奥で3軸回転）
const mainDash = new THREE.Mesh(new THREE.CylinderGeometry(1.06, 1.16, 0.46, 24, 1, false, Math.PI * 0.65, Math.PI * 0.7), matCockpitCarbon);
mainDash.position.set(0, -0.35, -0.35);
cockpitInteriorGroup.add(mainDash);

const glareHood = new THREE.Mesh(new THREE.BoxGeometry(1.68, 0.055, 0.66), matCockpitFrame);
glareHood.position.set(0, -0.13, -1.08);
glareHood.rotation.x = 0.08;
cockpitInteriorGroup.add(glareHood);

// ダッシュボード中央奥の物理量子ジャイロコア（金属リング＋発光特異点球）
const cabinGyroGroup = new THREE.Group();
cabinGyroGroup.position.set(0, -0.05, -1.05);
cockpitInteriorGroup.add(cabinGyroGroup);

const cabinGyroRingA = new THREE.Mesh(new THREE.TorusGeometry(0.065, 0.008, 8, 24), matTitaniumFrame);
const cabinGyroRingB = new THREE.Mesh(new THREE.TorusGeometry(0.048, 0.006, 8, 24), matCopperCoil);
const cabinGyroCore = new THREE.Mesh(new THREE.SphereGeometry(0.022, 12, 12), new THREE.MeshBasicMaterial({ color: cfg.flame_hex }));
cabinGyroGroup.add(cabinGyroRingA, cabinGyroRingB, cabinGyroCore);

// 3-3. 左右傾斜サイドコンソール（高低差スロットルクアドラント・冷却バルブ・密集スイッチ）
for (let s of [-1, 1]) {
    const sideConsole = new THREE.Mesh(new THREE.BoxGeometry(0.44, 0.28, 1.38), matCockpitCarbon);
    sideConsole.position.set(s * 0.66, -0.38, -0.58);
    sideConsole.rotation.z = -s * 0.22;
    cockpitInteriorGroup.add(sideConsole);

    // 立体物理スイッチ＆LEDボタン列（片側24個密集配置）
    for (let sw = 0; sw < 24; sw++) {
        const row = Math.floor(sw / 4);
        const col = sw % 4;
        const swMat = (sw % 5 === 0) ? matSwitchRed : ((sw % 2 === 0) ? matSwitchCyan : matSwitchAmber);
        const btnMesh = new THREE.Mesh(new THREE.BoxGeometry(0.032, 0.018, 0.042), swMat);
        btnMesh.position.set(
            s * (0.53 + col * 0.062),
            -0.23 + (col * 0.014),
            -0.28 - row * 0.125
        );
        btnMesh.rotation.z = -s * 0.22;
        cockpitInteriorGroup.add(btnMesh);
    }

    // 冷却圧力調整バルブハンドル
    const valveWheel = new THREE.Mesh(new THREE.TorusGeometry(0.035, 0.007, 8, 16), matSwitchRed);
    valveWheel.rotation.x = Math.PI / 2;
    valveWheel.position.set(s * 0.78, -0.21, -0.45);
    cockpitInteriorGroup.add(valveWheel);
}

// オーバーヘッド量子コンピュータ・スイッチパネル
const overheadPanel = new THREE.Mesh(new THREE.BoxGeometry(0.72, 0.08, 0.68), matCockpitCarbon);
overheadPanel.position.set(0, 0.68, -0.55);
overheadPanel.rotation.x = 0.35;
cockpitInteriorGroup.add(overheadPanel);

for (let oh = 0; oh < 10; oh++) {
    const ohLed = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.015, 0.025), oh % 3 === 0 ? matSwitchRed : (oh % 2 === 0 ? matSwitchCyan : matSwitchAmber));
    ohLed.position.set(-0.27 + oh * 0.06, 0.635, -0.55);
    ohLed.rotation.x = 0.35;
    cockpitInteriorGroup.add(ohLed);
}

const cockpitLight = new THREE.PointLight(0x38bdf8, 2.2, 4.0);
cockpitLight.position.set(0, 0.25, -0.55);
cockpitInteriorGroup.add(cockpitLight);

// HOTAS サイバー操縦桿＆デュアルスロットルクアドラント
const stickPivot = new THREE.Group();
stickPivot.position.set(0.36, -0.26, -0.68);
const flightStick = new THREE.Mesh(new THREE.CylinderGeometry(0.018, 0.026, 0.26, 10), matCockpitFrame);
flightStick.position.y = 0.13;
stickPivot.add(flightStick);
const stickGripHead = new THREE.Mesh(new THREE.BoxGeometry(0.045, 0.065, 0.055), matDarkAlloy);
stickGripHead.position.set(0, 0.25, -0.01);
stickPivot.add(stickGripHead);
cockpitInteriorGroup.add(stickPivot);

const throttlePivot = new THREE.Group();
throttlePivot.position.set(-0.36, -0.26, -0.68);
const throttleLeverL = new THREE.Mesh(new THREE.BoxGeometry(0.032, 0.16, 0.075), matDarkAlloy);
throttleLeverL.position.set(-0.02, 0.08, 0);
const throttleLeverR = new THREE.Mesh(new THREE.BoxGeometry(0.032, 0.16, 0.075), matTitaniumFrame);
throttleLeverR.position.set(0.02, 0.08, 0);
throttlePivot.add(throttleLeverL, throttleLeverR);
cockpitInteriorGroup.add(throttlePivot);

// 3-4. 多層空間ホログラム（3Dワイヤーフレーム地形スキャナー＋機体ダメージホログラム＋リングゲージ）
const holoProjectorGroup = new THREE.Group();
holoProjectorGroup.position.set(0, -0.01, -0.88);
cockpitInteriorGroup.add(holoProjectorGroup);

// 進行波ワイヤーフレーム地形スキャナー（シンセティック・ビジョン・グリッド）
const terrainScanGeo = new THREE.PlaneGeometry(0.28, 0.22, 14, 10);
terrainScanGeo.rotateX(-Math.PI / 2.3);
const terrainScanMesh = new THREE.Mesh(
    terrainScanGeo,
    new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true, transparent: true, opacity: 0.52 })
);
terrainScanMesh.position.set(0, -0.04, 0.04);
holoProjectorGroup.add(terrainScanMesh);

// 左側：立体リング状エンジンスプールゲージ
const holoSpoolRing = new THREE.Mesh(
    new THREE.RingGeometry(0.055, 0.075, 24),
    new THREE.MeshBasicMaterial({ color: 0x38bdf8, side: THREE.DoubleSide, transparent: true, opacity: 0.85 })
);
holoSpoolRing.position.set(-0.22, 0.03, 0.02);
holoProjectorGroup.add(holoSpoolRing);

// 右側：3D回転機体ダメージ・熱分布ホログラム
const holoShipMat = new THREE.MeshBasicMaterial({ color: 0x10b981, wireframe: true, transparent: true, opacity: 0.82 });
const holoShipCone = new THREE.Mesh(new THREE.ConeGeometry(0.045, 0.16, 6), holoShipMat);
holoShipCone.rotation.x = -Math.PI / 2;
holoShipCone.position.set(0.22, 0.03, 0.02);
holoProjectorGroup.add(holoShipCone);

// 3-5. 湾曲グラスコックピットMFD 3面ディスプレイ（2048 x 1024）
const mfdCanvas = document.createElement('canvas');
mfdCanvas.width = 2048; mfdCanvas.height = 1024;
const mfdCtx = mfdCanvas.getContext('2d');
const mfdTex = new THREE.CanvasTexture(mfdCanvas);
const mfdMat = new THREE.MeshBasicMaterial({ map: mfdTex });

// 湾曲シリンダー曲面スクリーン
const mfdCenterGeo = new THREE.CylinderGeometry(1.18, 1.18, 0.34, 24, 1, true, Math.PI * 0.86, Math.PI * 0.28);
mfdCenterGeo.scale(-1, 1, 1);
const mfdCenter = new THREE.Mesh(mfdCenterGeo, mfdMat);
mfdCenter.position.set(0, -0.31, 0.02);
cockpitInteriorGroup.add(mfdCenter);

const mfdLeft = new THREE.Mesh(new THREE.PlaneGeometry(0.44, 0.28), mfdMat);
mfdLeft.position.set(-0.56, -0.29, -1.02);
mfdLeft.rotation.set(-0.12, 0.44, 0);
cockpitInteriorGroup.add(mfdLeft);

const mfdRight = new THREE.Mesh(new THREE.PlaneGeometry(0.44, 0.28), mfdMat);
mfdRight.position.set(0.56, -0.29, -1.02);
mfdRight.rotation.set(-0.12, -0.44, 0);
cockpitInteriorGroup.add(mfdRight);

// フロントホログラフィック透過HUD
const hudCanvas = document.createElement('canvas');
hudCanvas.width = 1024; hudCanvas.height = 1024;
const hudCtx = hudCanvas.getContext('2d');
const hudTex = new THREE.CanvasTexture(hudCanvas);
const hudThemeColor = cfg.hud_theme.includes("Green") ? "#10b981" : (cfg.hud_theme.includes("Amber") ? "#f59e0b" : "#38bdf8");
const hudPlaneMat = new THREE.MeshBasicMaterial({ map: hudTex, transparent: true, opacity: 0.92, blending: THREE.AdditiveBlending });
const hudGlassPlane = new THREE.Mesh(new THREE.PlaneGeometry(0.95, 0.95), hudPlaneMat);
hudGlassPlane.position.set(0, 0.08, -0.96);
cockpitInteriorGroup.add(hudGlassPlane);

function updateCockpitDisplays(mach, altKm, gLoad, pitchDeg, rollDeg, engPwr, phase, tempK, nowSec, wAct) {
    mfdCtx.fillStyle = '#020617';
    mfdCtx.fillRect(0, 0, 2048, 1024);

    mfdCtx.strokeStyle = hudThemeColor;
    mfdCtx.lineWidth = 4;
    mfdCtx.strokeRect(16, 16, 2016, 992);
    mfdCtx.strokeRect(680, 16, 688, 992);

    // 左パネル：核融合炉タコメーター＆プラズマ波形オシロスコープ
    mfdCtx.save();
    mfdCtx.beginPath();
    mfdCtx.arc(340, 310, 145, 0.8 * Math.PI, 2.2 * Math.PI);
    mfdCtx.strokeStyle = 'rgba(56,189,248,0.22)';
    mfdCtx.lineWidth = 18;
    mfdCtx.stroke();

    mfdCtx.beginPath();
    mfdCtx.arc(340, 310, 145, 0.8 * Math.PI, (0.8 + engPwr * 1.4) * Math.PI);
    mfdCtx.strokeStyle = hudThemeColor;
    mfdCtx.lineWidth = 18;
    mfdCtx.stroke();
    mfdCtx.restore();

    mfdCtx.fillStyle = hudThemeColor;
    mfdCtx.font = 'bold 42px monospace';
    mfdCtx.fillText(`THRUST ${(engPwr * 100).toFixed(0)}%`, 210, 325);

    mfdCtx.strokeStyle = '#10b981';
    mfdCtx.lineWidth = 4;
    mfdCtx.beginPath();
    for (let wx = 80; wx <= 600; wx += 12) {
        const amp = (25 + engPwr * 65) * Math.sin(wx * 0.035 + nowSec * 12.0) * Math.cos(wx * 0.012 - nowSec * 5.0);
        const wy = 620 + amp;
        if (wx === 80) mfdCtx.moveTo(wx, wy);
        else mfdCtx.lineTo(wx, wy);
    }
    mfdCtx.stroke();

    mfdCtx.fillStyle = hudThemeColor;
    mfdCtx.font = 'bold 28px monospace';
    mfdCtx.fillText(`CORE: D-He3 MAGNETIC PINCH`, 80, 760);
    mfdCtx.fillText(`PLASMA TEMP: ${tempK.toFixed(0)} K`, 80, 810);
    mfdCtx.fillText(`MASS FLOW: ${(engPwr * 420).toFixed(0)} KG/S`, 80, 860);

    // 中央パネル：PFD 人工水平儀
    const cx = 1024, cy = 440;
    mfdCtx.save();
    mfdCtx.beginPath();
    mfdCtx.rect(700, 140, 648, 600);
    mfdCtx.clip();
    mfdCtx.translate(cx, cy);
    mfdCtx.rotate(-rollDeg * Math.PI / 180);
    const pOff = (pitchDeg / 90) * 320;

    mfdCtx.fillStyle = 'rgba(14,165,233,0.12)';
    mfdCtx.fillRect(-400, -500 - pOff, 800, 500);
    mfdCtx.fillStyle = 'rgba(180,83,9,0.16)';
    mfdCtx.fillRect(-400, -pOff, 800, 500);

    mfdCtx.strokeStyle = 'rgba(16,185,129,0.35)';
    mfdCtx.lineWidth = 2;
    for (let gy = -350; gy <= 350; gy += 50) {
        mfdCtx.beginPath();
        mfdCtx.moveTo(-260, gy - pOff); mfdCtx.lineTo(260, gy - pOff);
        mfdCtx.stroke();
    }

    mfdCtx.strokeStyle = hudThemeColor;
    mfdCtx.lineWidth = 6;
    mfdCtx.beginPath();
    mfdCtx.moveTo(-320, -pOff); mfdCtx.lineTo(320, -pOff);
    mfdCtx.stroke();
    mfdCtx.restore();

    mfdCtx.fillStyle = hudThemeColor;
    mfdCtx.font = 'bold 30px monospace';
    mfdCtx.fillText(`QUANTUM PFD // PITCH ${pitchDeg.toFixed(1)}°`, 760, 100);
    mfdCtx.fillText(`WARP METRIC: ${wAct > 0.1 ? 'ACTIVE' : 'STANDBY'}`, 760, 840);

    // 右パネル：テレメトリ＆熱シールド診断
    mfdCtx.fillStyle = hudThemeColor;
    mfdCtx.font = 'bold 38px monospace';
    mfdCtx.fillText(`MACH: ${mach.toFixed(1)}`, 1440, 140);
    mfdCtx.fillText(`ALT : ${altKm > 90000 ? 'ORBIT' : altKm.toFixed(2) + ' KM'}`, 1440, 200);
    mfdCtx.fillText(`LOAD: ${gLoad.toFixed(1)} G`, 1440, 260);
    mfdCtx.fillText(`STAT: ${phase.slice(0, 15)}`, 1440, 320);

    mfdCtx.fillStyle = 'rgba(56,189,248,0.2)';
    mfdCtx.fillRect(1440, 420, 480, 40);
    mfdCtx.fillStyle = (tempK > 1200) ? '#ef4444' : '#10b981';
    mfdCtx.fillRect(1440, 420, Math.min(480, (tempK / 2500) * 480), 40);
    mfdCtx.font = 'bold 26px monospace';
    mfdCtx.fillStyle = '#fff';
    mfdCtx.fillText(`THERMAL SHIELD: ${Math.min(100, (tempK / 2500) * 100).toFixed(0)}%`, 1455, 449);

    mfdTex.needsUpdate = true;

    // HUDホログラム描画
    hudCtx.clearRect(0, 0, 1024, 1024);
    hudCtx.strokeStyle = hudThemeColor;
    hudCtx.lineWidth = 4;

    hudCtx.beginPath();
    hudCtx.arc(512, 512, 36, 0, Math.PI * 2);
    hudCtx.moveTo(420, 512); hudCtx.lineTo(476, 512);
    hudCtx.moveTo(548, 512); hudCtx.lineTo(604, 512);
    hudCtx.moveTo(512, 476); hudCtx.lineTo(512, 435);
    hudCtx.stroke();

    for (let l = -2; l <= 2; l++) {
        if (l === 0) continue;
        const ly = 512 + l * 85;
        hudCtx.beginPath();
        hudCtx.moveTo(350, ly); hudCtx.lineTo(410, ly);
        hudCtx.moveTo(614, ly); hudCtx.lineTo(674, ly);
        hudCtx.stroke();
    }

    hudCtx.fillStyle = hudThemeColor;
    hudCtx.font = 'bold 34px monospace';
    hudCtx.fillText(`M ${mach.toFixed(1)}`, 200, 524);
    hudCtx.fillText(`${altKm > 90000 ? 'SPACE' : (altKm * 1000).toFixed(0) + 'M'}`, 710, 524);

    hudCtx.beginPath();
    hudCtx.moveTo(312, 220); hudCtx.lineTo(712, 220);
    hudCtx.stroke();
    hudCtx.font = 'bold 26px monospace';
    hudCtx.fillText(`QUANTUM NAV // VECTOR LOCK`, 335, 198);

    hudTex.needsUpdate = true;
}

// =========================================================================
// 5. 2層流体リボン・マッハコーン＆カタパルト電磁アーク＆カメラ横通過パーティクル
// =========================================================================
const machConeGeo = new THREE.ConeGeometry(10.5, 28.0, 40, 12, true);
const machConeMat = new THREE.ShaderMaterial({
    vertexShader: `
        varying vec2 vUv; varying vec3 vNormal; uniform float uTime;
        void main() {
            vUv = uv;
            vNormal = normalize(normalMatrix * normal);
            vec3 pos = position;
            float ripple = sin(uv.y * 28.0 - uTime * 22.0) * cos(uv.x * 18.0 + uTime * 14.0) * 0.35 * (1.0 - uv.y);
            pos.x += normal.x * ripple;
            pos.z += normal.z * ripple;
            gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
        }
    `,
    fragmentShader: `
        varying vec2 vUv; varying vec3 vNormal; uniform float uAlpha; uniform vec3 uBaseColor; uniform float uTime;
        void main() {
            float fresnel = pow(1.0 - abs(dot(vNormal, vec3(0.0, 0.0, 1.0))), 2.2);
            float streak = 0.65 + 0.35 * sin(vUv.x * 36.0 + vUv.y * 12.0 - uTime * 18.0);
            float taper = pow(vUv.y, 1.8) * smoothstep(0.0, 0.15, vUv.y);
            vec3 col = mix(vec3(1.0), uBaseColor, vUv.y);
            gl_FragColor = vec4(col, fresnel * taper * streak * uAlpha * 0.92);
        }
    `,
    uniforms: { uAlpha: { value: 0.0 }, uBaseColor: { value: new THREE.Color(cfg.plasma_hex) }, uTime: { value: 0.0 } },
    transparent: true, blending: THREE.AdditiveBlending, side: THREE.DoubleSide, depthWrite: false
});
const machConeMesh = new THREE.Mesh(machConeGeo, machConeMat);
machConeMesh.rotation.x = -Math.PI / 2;
machConeMesh.position.set(0, 0, 8.5);
shipMeshGroup.add(machConeMesh);

const outerShockCone = new THREE.Mesh(new THREE.ConeGeometry(13.5, 32.0, 32, 1, true), machConeMat);
outerShockCone.rotation.x = -Math.PI / 2;
outerShockCone.position.set(0, 0, 6.0);
shipMeshGroup.add(outerShockCone);

// カタパルト電磁アーク稲妻
const arcBolts = [];
const arcMat = new THREE.LineBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.0, blending: THREE.AdditiveBlending });
for (let ab = 0; ab < 6; ab++) {
    const pts = [];
    for (let k = 0; k < 10; k++) pts.push(new THREE.Vector3(0, -1.2, 10 - k * 2.2));
    const lineGeo = new THREE.BufferGeometry().setFromPoints(pts);
    const line = new THREE.Line(lineGeo, arcMat);
    shipMeshGroup.add(line);
    arcBolts.push(line);
}

// 【魔改造5】クライオ氷片＆プラズマ・スパークのカメラ横通過パーティクル（220個）
const flybyCount = 220;
const flybyGeo = new THREE.BufferGeometry();
const flybyPos = new Float32Array(flybyCount * 3);
const flybyCol = new Float32Array(flybyCount * 3);
for (let f = 0; f < flybyCount; f++) {
    flybyPos[f * 3] = (Math.random() - 0.5) * 75.0;
    flybyPos[f * 3 + 1] = (Math.random() - 0.5) * 45.0;
    flybyPos[f * 3 + 2] = (Math.random() - 0.5) * 180.0;
    const isIce = (f % 2 === 0);
    flybyCol[f * 3] = isIce ? 0.78 : 1.0;
    flybyCol[f * 3 + 1] = isIce ? 0.94 : 0.65;
    flybyCol[f * 3 + 2] = isIce ? 1.0 : 0.25;
}
flybyGeo.setAttribute('position', new THREE.BufferAttribute(flybyPos, 3));
flybyGeo.setAttribute('color', new THREE.BufferAttribute(flybyCol, 3));
const flybyMat = new THREE.PointsMaterial({
    size: 0.65,
    vertexColors: true,
    transparent: true,
    opacity: 0.0,
    blending: THREE.AdditiveBlending
});
const flybyParticles = new THREE.Points(flybyGeo, flybyMat);
scene.add(flybyParticles);

// =========================================================================
// 6. アルクビエレ・ワープバブル＆高次元ネビュラトンネル
// =========================================================================
const warpBubbleGeo = new THREE.SphereGeometry(24.0, 48, 32);
warpBubbleGeo.scale(1.05, 0.72, 1.45);
const warpBubbleMat = new THREE.ShaderMaterial({
    vertexShader: `
        varying vec3 vNormal; varying vec3 vLocalPos; varying vec3 vWorldPos;
        uniform float uTime; uniform float uIntensity;
        void main() {
            vLocalPos = position;
            vNormal = normalize(normalMatrix * normal);
            vec3 pos = position;
            float wave = sin(pos.z * 0.45 - uTime * 8.0) * 0.45 * uIntensity;
            pos += normal * wave;
            vec4 wp = modelMatrix * vec4(pos, 1.0);
            vWorldPos = wp.xyz;
            gl_Position = projectionMatrix * viewMatrix * wp;
        }
    `,
    fragmentShader: `
        varying vec3 vNormal; varying vec3 vLocalPos; varying vec3 vWorldPos;
        uniform float uTime; uniform float uIntensity; uniform vec3 uAuroraColor;
        void main() {
            vec3 viewDir = normalize(cameraPosition - vWorldPos);
            float fresnel = pow(1.0 - abs(dot(vNormal, viewDir)), 2.6);
            float zNorm = clamp(vLocalPos.z / 34.0, -1.0, 1.0);
            vec3 blueShift = vec3(0.35, 0.88, 1.0);
            vec3 redShift = vec3(0.95, 0.25, 0.65);
            vec3 shiftCol = mix(redShift, blueShift, zNorm * 0.5 + 0.5);
            float gridZ = abs(sin(vLocalPos.z * 0.8 - uTime * 14.0));
            float gridA = abs(sin(atan(vLocalPos.y, vLocalPos.x) * 12.0 + uTime * 3.0));
            float metricLines = smoothstep(0.92, 0.99, max(gridZ, gridA)) * 0.7;
            vec3 finalCol = mix(uAuroraColor, shiftCol, 0.7) + vec3(1.0) * metricLines * 0.5;
            float alpha = (fresnel * 0.85 + metricLines * 0.45) * uIntensity;
            gl_FragColor = vec4(finalCol, clamp(alpha, 0.0, 0.92));
        }
    `,
    uniforms: {
        uTime: { value: 0.0 },
        uIntensity: { value: 0.0 },
        uAuroraColor: { value: new THREE.Color(cfg.aurora_hex) }
    },
    transparent: true,
    blending: THREE.AdditiveBlending,
    side: THREE.DoubleSide,
    depthWrite: false
});
const warpBubbleMesh = new THREE.Mesh(warpBubbleGeo, warpBubbleMat);
warpBubbleMesh.position.set(0, 0, 1.0);
shipMeshGroup.add(warpBubbleMesh);

const warpGroup = new THREE.Group();
warpGroup.scale.setScalar(0.0001);
scene.add(warpGroup);

const warpTunnelMat = new THREE.ShaderMaterial({
    vertexShader: `varying vec2 vUv; void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `
        varying vec2 vUv;
        uniform float uTime; uniform vec3 uColorA; uniform vec3 uColorB; uniform float uVc;
        float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
        float noise(vec2 p) {
            vec2 i = floor(p); vec2 f = fract(p); vec2 u = f * f * (3.0 - 2.0 * f);
            return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x), mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
        }
        float fbm(vec2 p) {
            float v = 0.0; float a = 0.5;
            for (int i = 0; i < 5; i++) { v += a * noise(p); p *= 2.05; a *= 0.5; }
            return v;
        }
        void main() {
            vec2 uv = vec2(vUv.x * 6.0, vUv.y * 8.0 - uTime * (2.5 + uVc * 4.0));
            float n1 = fbm(uv);
            float n2 = fbm(uv * 2.2 + vec2(n1 * 1.5, -uTime * 1.8));
            float lightning = pow(1.0 - abs(n2 - 0.5) * 2.0, 10.0) * 1.6;
            vec3 doppler = mix(vec3(0.9, 0.2, 0.5), vec3(0.25, 0.85, 1.0), vUv.y);
            vec3 nebula = mix(uColorA, uColorB, n1) * 0.75 + doppler * 0.45 + vec3(0.85, 0.95, 1.0) * lightning;
            float edgeFade = sin(vUv.y * 3.14159);
            gl_FragColor = vec4(nebula, clamp((n2 * 0.65 + lightning * 0.5) * edgeFade, 0.0, 0.88));
        }
    `,
    uniforms: {
        uTime: { value: 0.0 },
        uColorA: { value: new THREE.Color(cfg.aurora_hex) },
        uColorB: { value: new THREE.Color(cfg.flame_hex) },
        uVc: { value: 0.5 }
    },
    transparent: true,
    blending: THREE.AdditiveBlending,
    side: THREE.BackSide,
    depthWrite: false
});
const warpTunnelOuter = new THREE.Mesh(new THREE.CylinderGeometry(85.0, 85.0, 680.0, 48, 1, true), warpTunnelMat);
warpTunnelOuter.rotation.x = Math.PI / 2;
warpGroup.add(warpTunnelOuter);

const warpTunnelInner = new THREE.Mesh(new THREE.CylinderGeometry(42.0, 42.0, 640.0, 36, 1, true), warpTunnelMat);
warpTunnelInner.rotation.x = Math.PI / 2;
warpGroup.add(warpTunnelInner);

const starCount = 4000;
const starGeo = new THREE.BufferGeometry();
const starPos = new Float32Array(starCount * 6);
const starCol = new Float32Array(starCount * 6);
for (let i = 0; i < starCount; i++) {
    const ang = Math.random() * Math.PI * 2, rad = 28.0 + Math.random() * 210.0, z = (Math.random() - 0.5) * 640.0;
    starPos[i * 6] = Math.cos(ang) * rad; starPos[i * 6 + 1] = Math.sin(ang) * rad; starPos[i * 6 + 2] = z;
    starPos[i * 6 + 3] = starPos[i * 6]; starPos[i * 6 + 4] = starPos[i * 6 + 1]; starPos[i * 6 + 5] = z + 1.0;
    starCol[i * 6] = 0.55; starCol[i * 6 + 1] = 0.92; starCol[i * 6 + 2] = 1.0;
    starCol[i * 6 + 3] = 0.98; starCol[i * 6 + 4] = 0.22; starCol[i * 6 + 5] = 0.45;
}
starGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
starGeo.setAttribute('color', new THREE.BufferAttribute(starCol, 3));
warpGroup.add(new THREE.LineSegments(starGeo, new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.95, blending: THREE.AdditiveBlending })));

// =========================================================================
// 7. フォトリアル富士山（200×200実測ハイトマップ＋雪渓シェーダー＋雲海）＆海面
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

const oceanShaderMat = new THREE.ShaderMaterial({
    vertexShader: `
        varying vec2 vUv; varying vec3 vWorldPos;
        void main() {
            vUv = uv;
            vec4 wp = modelMatrix * vec4(position, 1.0);
            vWorldPos = wp.xyz;
            gl_Position = projectionMatrix * viewMatrix * wp;
        }
    `,
    fragmentShader: `
        varying vec2 vUv; varying vec3 vWorldPos;
        uniform vec3 uSunDir; uniform vec3 uSunColor; uniform float uTime; uniform float uOpacity;
        
        float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123); }
        float noise(vec2 p) {
            vec2 i = floor(p); vec2 f = fract(p); vec2 u = f * f * (3.0 - 2.0 * f);
            return mix(mix(hash(i + vec2(0.0,0.0)), hash(i + vec2(1.0,0.0)), u.x), mix(hash(i + vec2(0.0,1.0)), hash(i + vec2(1.0,1.0)), u.x), u.y);
        }
        float fbmWave(vec2 p) {
            float v = 0.0; float a = 0.5; vec2 shift = vec2(100.0);
            for (int i = 0; i < 7; i++) {
                v += a * noise(p + uTime * 0.15 * float(i + 1));
                p = p * 2.0 + shift;
                a *= 0.5;
            }
            return v;
        }
        void main() {
            vec2 waveUv = vWorldPos.xz * 0.0015;
            float hL = fbmWave(waveUv - vec2(0.004, 0.0));
            float hR = fbmWave(waveUv + vec2(0.004, 0.0));
            float hD = fbmWave(waveUv - vec2(0.0, 0.004));
            float hU = fbmWave(waveUv + vec2(0.0, 0.004));
            vec3 n = normalize(vec3(hL - hR, 0.12, hD - hU));
            
            vec3 viewDir = normalize(cameraPosition - vWorldPos);
            float fresnel = pow(1.0 - max(0.0, dot(n, viewDir)), 4.5);
            
            vec3 deepWater = vec3(0.012, 0.045, 0.095);
            vec3 sssWater = vec3(0.03, 0.22, 0.28);
            vec3 skyReflect = vec3(0.35, 0.65, 0.98);
            
            vec3 halfVec = normalize(uSunDir + viewDir);
            float spec = pow(max(0.0, dot(n, halfVec)), 280.0) * 8.0;
            float sss = pow(max(0.0, dot(viewDir, -uSunDir)), 2.0) * 0.45;
            
            vec3 finalSea = mix(mix(deepWater, sssWater, sss), skyReflect, fresnel) + uSunColor * spec;
            gl_FragColor = vec4(finalSea, uOpacity);
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
const seaMesh = new THREE.Mesh(new THREE.PlaneGeometry(320000, 320000), oceanShaderMat);
seaMesh.rotation.x = -Math.PI / 2;
seaMesh.position.y = -45.0;
groundEnvMover.add(seaMesh);

const islandBase = new THREE.Mesh(new THREE.BoxGeometry(220, 28, 3800), matDarkAlloy);
islandBase.position.set(0, -32, 1750);
islandBase.receiveShadow = true;
groundEnvMover.add(islandBase);

const fujiSize = 36000.0;
const fujiGeo = new THREE.PlaneGeometry(fujiSize, fujiSize, 200, 200);
fujiGeo.rotateX(-Math.PI / 2);

const fPos = fujiGeo.attributes.position;
const summitRadius = 720.0;
const maxHeight = 3776.0;

for (let i = 0; i < fPos.count; i++) {
    const x = fPos.getX(i);
    const z = fPos.getZ(i);
    const r = Math.sqrt(x * x + z * z);
    const theta = Math.atan2(z, x);

    const radialRidges =
        Math.sin(theta * 18.0 + r * 0.00045) * 0.032 +
        Math.cos(theta * 34.0 - r * 0.0008) * 0.018 +
        Math.sin(theta * 62.0 + r * 0.0015) * 0.009;

    const effectiveR = Math.max(0.0, r * (1.0 + radialRidges));
    let h = 0.0;

    if (effectiveR < summitRadius) {
        const rimRatio = effectiveR / summitRadius;
        const rimJagged = Math.sin(theta * 9.0) * 48.0 + Math.cos(theta * 17.0) * 26.0;
        const craterDepth = (1.0 - rimRatio * rimRatio) * 240.0;
        h = maxHeight - craterDepth + rimJagged * Math.pow(rimRatio, 1.5);
    } else {
        const d = (effectiveR - summitRadius) / 6800.0;
        h = maxHeight * Math.exp(-Math.pow(d, 1.48));
        const valleyCarve = (Math.sin(theta * 22.0) * 0.5 + Math.cos(theta * 41.0) * 0.35) * 95.0 * Math.exp(-d * 0.85) * Math.min(1.0, d * 2.5);
        h += valleyCarve;
    }

    const hoeiX = -2100.0, hoeiZ = -2600.0;
    const distHoei = Math.sqrt((x - hoeiX) * (x - hoeiX) + (z - hoeiZ) * (z - hoeiZ));
    if (distHoei < 1600.0) {
        const craterFactor = Math.cos((distHoei / 1600.0) * (Math.PI * 0.5));
        h -= craterFactor * craterFactor * 340.0;
    }
    const hoeiPeakX = -2650.0, hoeiPeakZ = -3250.0;
    const distPeak = Math.sqrt((x - hoeiPeakX) * (x - hoeiPeakX) + (z - hoeiPeakZ) * (z - hoeiPeakZ));
    if (distPeak < 1100.0) {
        h += Math.cos((distPeak / 1100.0) * (Math.PI * 0.5)) * 180.0;
    }

    fPos.setY(i, Math.max(-45.0, h - 42.0));
}
fujiGeo.computeVertexNormals();

const fujiShaderMat = new THREE.ShaderMaterial({
    vertexShader: `
        varying vec3 vWorldPos; varying vec3 vNormal; varying float vElev;
        void main() {
            vec4 wp = modelMatrix * vec4(position, 1.0);
            vWorldPos = wp.xyz;
            vNormal = normalize(mat3(modelMatrix) * normal);
            vElev = clamp((position.y + 42.0) / 3776.0, 0.0, 1.0);
            gl_Position = projectionMatrix * viewMatrix * wp;
        }
    `,
    fragmentShader: `
        varying vec3 vWorldPos; varying vec3 vNormal; varying float vElev;
        uniform vec3 uSunDir; uniform float uOpacity; uniform vec3 uHazeColor;

        float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
        float noise(vec2 p) {
            vec2 i = floor(p); vec2 f = fract(p); vec2 u = f * f * (3.0 - 2.0 * f);
            return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x), mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
        }
        float fbm(vec2 p) {
            float v = 0.0; float a = 0.5;
            for (int i = 0; i < 4; i++) { v += a * noise(p); p *= 2.1; a *= 0.5; }
            return v;
        }

        void main() {
            float dist = length(cameraPosition - vWorldPos);
            float nDetail = fbm(vWorldPos.xz * 0.0022);
            float slope = clamp(vNormal.y, 0.0, 1.0);
            float snowLine = 0.44 + (1.0 - slope) * 0.36 + (nDetail - 0.5) * 0.14;
            float snowMask = smoothstep(snowLine - 0.04, snowLine + 0.05, vElev);

            vec3 forestCol = vec3(0.03, 0.065, 0.045) * (0.8 + 0.4 * nDetail);
            vec3 basaltCol = vec3(0.09, 0.08, 0.085) * (0.75 + 0.5 * nDetail);
            vec3 snowCol = vec3(0.94, 0.97, 1.0);

            vec3 groundCol = mix(forestCol, basaltCol, smoothstep(0.18, 0.42, vElev));
            vec3 albedo = mix(groundCol, snowCol, snowMask);

            float diff = max(0.18, dot(vNormal, uSunDir));
            vec3 litCol = albedo * (diff * vec3(1.05, 0.98, 0.92) + vec3(0.08, 0.14, 0.24));

            float haze = clamp(pow(dist / 58000.0, 1.25), 0.0, 0.68);
            vec3 finalCol = mix(litCol, uHazeColor, haze);

            gl_FragColor = vec4(finalCol, uOpacity);
        }
    `,
    uniforms: {
        uSunDir: { value: new THREE.Vector3().fromArray(cfg.env.sun_pos).normalize() },
        uOpacity: { value: 1.0 },
        uHazeColor: { value: new THREE.Color(cfg.env.mode === "dawn" ? 0x7c2d12 : 0x1e3a5f) }
    },
    transparent: true
});
const fujiMount = new THREE.Mesh(fujiGeo, fujiShaderMat);
fujiMount.position.set(6200, 0, 23500);
fujiMount.frustumCulled = false;
groundEnvMover.add(fujiMount);

const seaOfCloudsMat = new THREE.ShaderMaterial({
    vertexShader: `varying vec2 vUv; varying vec3 vWorldPos; void main() { vUv = uv; vec4 wp = modelMatrix * vec4(position, 1.0); vWorldPos = wp.xyz; gl_Position = projectionMatrix * viewMatrix * wp; }`,
    fragmentShader: `
        varying vec2 vUv; varying vec3 vWorldPos; uniform float uTime; uniform float uOpacity;
        float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
        float noise(vec2 p) {
            vec2 i = floor(p); vec2 f = fract(p); vec2 u = f * f * (3.0 - 2.0 * f);
            return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x), mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
        }
        float fbm(vec2 p) { float v = 0.0; float a = 0.5; for (int i = 0; i < 4; i++) { v += a * noise(p); p *= 2.0; a *= 0.5; } return v; }
        void main() {
            float r = length(vUv - 0.5) * 2.0;
            float radialMask = smoothstep(1.0, 0.35, r);
            float n = fbm(vWorldPos.xz * 0.00035 + vec2(uTime * 0.015, 0.0));
            float cloudAlpha = smoothstep(0.42, 0.78, n) * radialMask * 0.65 * uOpacity;
            gl_FragColor = vec4(vec3(0.75, 0.85, 0.96), cloudAlpha);
        }
    `,
    uniforms: { uTime: { value: 0.0 }, uOpacity: { value: 1.0 } },
    transparent: true, depthWrite: false
});
const seaOfCloudsMesh = new THREE.Mesh(new THREE.PlaneGeometry(42000, 42000), seaOfCloudsMat);
seaOfCloudsMesh.rotation.x = -Math.PI / 2;
seaOfCloudsMesh.position.set(6200, 680, 23500);
groundEnvMover.add(seaOfCloudsMesh);

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

// 5オクターブFBM地球 ＆ 大気散乱リムヘイロー
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

const atmoHaloMat = new THREE.ShaderMaterial({
    vertexShader: `varying vec3 vNormal; varying vec3 vWorldPos; void main() { vNormal = normalize(normalMatrix * normal); vec4 wp = modelMatrix * vec4(position, 1.0); vWorldPos = wp.xyz; gl_Position = projectionMatrix * viewMatrix * wp; }`,
    fragmentShader: `
        varying vec3 vNormal; varying vec3 vWorldPos; uniform float uOpacity;
        void main() {
            vec3 viewDir = normalize(cameraPosition - vWorldPos);
            float rim = pow(1.0 - max(0.0, dot(vNormal, viewDir)), 4.0);
            vec3 atmoCyan = vec3(0.2, 0.7, 1.0);
            gl_FragColor = vec4(atmoCyan, rim * 1.2 * uOpacity);
        }
    `,
    uniforms: { uOpacity: { value: 1.0 } },
    transparent: true, blending: THREE.AdditiveBlending, side: THREE.BackSide, depthWrite: false
});
const atmoHaloMesh = new THREE.Mesh(new THREE.SphereGeometry(25450, 64, 64), atmoHaloMat);
earthGroup.add(atmoHaloMesh);

// =========================================================================
// 8. 【魔改造4 & 5】着陸都市の完全改修（ドーム貫通防止数理設計＋5種SF建築＋電磁アレスティング網）
// =========================================================================
const destWorld = new THREE.Group();
destWorld.visible = false;
scene.add(destWorld);

const planetTerrainMat = new THREE.MeshStandardMaterial({
    color: new THREE.Color(cfg.dest_color),
    roughness: 0.94,
    metalness: 0.08,
    polygonOffset: true,
    polygonOffsetFactor: 2,
    polygonOffsetUnits: 2
});
const planetTerrainMesh = new THREE.Mesh(new THREE.PlaneGeometry(350000, 350000), planetTerrainMat);
planetTerrainMesh.rotation.x = -Math.PI / 2;
planetTerrainMesh.position.y = -4.5;
destWorld.add(planetTerrainMesh);

const runwayScrollGroup = new THREE.Group();
destWorld.add(runwayScrollGroup);

const orbitGoalGroup = new THREE.Group();
destWorld.add(orbitGoalGroup);

function makeUnifiedRunwayTexture() {
    const c = document.createElement('canvas');
    c.width = 1024; c.height = 2048;
    const ctx = c.getContext('2d');

    ctx.fillStyle = '#111827';
    ctx.fillRect(0, 0, 1024, 2048);

    for (let i = 0; i < 18000; i++) {
        const rx = Math.random() * 1024;
        const ry = Math.random() * 2048;
        const shade = 14 + Math.floor(Math.random() * 18);
        ctx.fillStyle = `rgb(${shade},${shade+3},${shade+8})`;
        ctx.fillRect(rx, ry, 3, 3);
    }

    ctx.fillStyle = '#cbd5e1';
    ctx.fillRect(42, 0, 14, 2048);
    ctx.fillRect(968, 0, 14, 2048);

    ctx.fillStyle = '#e2e8f0';
    for (let y = 40; y < 2048; y += 128) {
        ctx.fillRect(504, y, 16, 72);
    }

    ctx.fillStyle = 'rgba(226, 232, 240, 0.85)';
    for (let b = 0; b < 4; b++) {
        ctx.fillRect(180 + b * 45, 220, 24, 160);
        ctx.fillRect(720 + b * 45, 220, 24, 160);
    }
    ctx.fillStyle = 'rgba(2, 6, 15, 0.55)';
    for (let sk = 0; sk < 14; sk++) {
        const sx = 390 + Math.random() * 244;
        ctx.fillRect(sx, 180 + Math.random() * 480, 6, 140 + Math.random() * 180);
    }

    const tex = new THREE.CanvasTexture(c);
    tex.wrapS = THREE.ClampToEdgeWrapping;
    tex.wrapT = THREE.RepeatWrapping;
    tex.repeat.set(1, 32);
    tex.anisotropy = 8;
    return tex;
}
const unifiedRunwayTex = makeUnifiedRunwayTexture();

const runwayLength = 40000.0;
const runwayMesh = new THREE.Mesh(
    new THREE.BoxGeometry(165.0, 0.8, runwayLength),
    new THREE.MeshStandardMaterial({
        map: unifiedRunwayTex,
        roughness: 0.72,
        metalness: 0.18,
        polygonOffset: true,
        polygonOffsetFactor: -2,
        polygonOffsetUnits: -2
    })
);
runwayMesh.position.set(0, -3.0, runwayLength * 0.5);
runwayMesh.receiveShadow = true;
runwayScrollGroup.add(runwayMesh);

// 非点滅ブルータリズムSF建築＆穏やかなスリット照明テクスチャ
function makeCalmArchitecturalTexture() {
    const c = document.createElement('canvas'); c.width = 512; c.height = 512;
    const ctx = c.getContext('2d');
    ctx.fillStyle = '#0f172a'; ctx.fillRect(0, 0, 512, 512);

    ctx.fillStyle = '#1e293b';
    for (let y = 0; y < 512; y += 64) {
        ctx.fillRect(0, y, 512, 22);
    }
    ctx.fillStyle = '#38bdf8';
    for (let y = 32; y < 512; y += 128) {
        ctx.fillRect(48, y, 160, 8);
        ctx.fillRect(304, y, 160, 8);
    }
    const t = new THREE.CanvasTexture(c);
    t.wrapS = THREE.RepeatWrapping; t.wrapT = THREE.RepeatWrapping;
    t.repeat.set(1, 3);
    t.minFilter = THREE.LinearMipmapLinearFilter;
    return t;
}
const calmBuildingTex = makeCalmArchitecturalTexture();

const matColonyBuilding = new THREE.MeshStandardMaterial({
    color: 0x1e293b,
    metalness: 0.65,
    roughness: 0.58,
    emissiveMap: calmBuildingTex,
    emissive: new THREE.Color(0x38bdf8),
    emissiveIntensity: 0.22
});
const matColonyAccent = new THREE.MeshStandardMaterial({
    color: 0x334155,
    metalness: 0.82,
    roughness: 0.35
});

// 【魔改造4】ドーム貫通を数学的に完全防止した5種のプロシージャルSF建築生成関数
function createProceduralSFBuilding(typeIdx, maxAllowedHeight, baseY) {
    const bGroup = new THREE.Group();
    const h = Math.max(45.0, maxAllowedHeight);

    if (typeIdx === 0) {
        // ① 階層ごとに角度が回転する「スパイラル・高層タワー」
        const tiers = 6;
        const tierH = h / tiers;
        for (let t = 0; t < tiers; t++) {
            const w = (48.0 - t * 3.5);
            const tierMesh = new THREE.Mesh(new THREE.BoxGeometry(w, tierH * 0.94, w), matColonyBuilding);
            tierMesh.position.y = baseY + tierH * (t + 0.5);
            tierMesh.rotation.y = t * 0.24;
            bGroup.add(tierMesh);
        }
    } else if (typeIdx === 1) {
        // ② 上部が広がった「ブルータリズム・アルコロジー複合体」
        const core = new THREE.Mesh(new THREE.CylinderGeometry(24.0, 34.0, h * 0.65, 8), matColonyAccent);
        core.position.y = baseY + h * 0.325;
        bGroup.add(core);

        const crown = new THREE.Mesh(new THREE.CylinderGeometry(48.0, 28.0, h * 0.35, 8), matColonyBuilding);
        crown.position.y = baseY + h * 0.825;
        bGroup.add(crown);
    } else if (typeIdx === 2) {
        // ③ 空中連絡ブリッジで繋がった「ツインタワー＆屋上通信アンテナ塔」
        const towerH = h * 0.85;
        [-24.0, 24.0].forEach(tx => {
            const tMesh = new THREE.Mesh(new THREE.BoxGeometry(26.0, towerH, 32.0), matColonyBuilding);
            tMesh.position.set(tx, baseY + towerH * 0.5, 0);
            bGroup.add(tMesh);
        });
        const skyBridge = new THREE.Mesh(new THREE.BoxGeometry(54.0, 12.0, 16.0), matColonyAccent);
        skyBridge.position.set(0, baseY + towerH * 0.65, 0);
        bGroup.add(skyBridge);

        const antenna = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 3.0, h * 0.15, 8), matTitaniumFrame);
        antenna.position.set(-24.0, baseY + towerH + h * 0.075, 0);
        bGroup.add(antenna);
    } else {
        // ④ 球体燃料タンクとトラスフレームが組まれた「テラフォーミング大気生成プラント」
        const baseDeck = new THREE.Mesh(new THREE.BoxGeometry(68.0, h * 0.25, 68.0), matColonyAccent);
        baseDeck.position.y = baseY + h * 0.125;
        bGroup.add(baseDeck);

        const sphereR = Math.min(28.0, h * 0.24);
        [-18.0, 18.0].forEach(sx => {
            const bioSphere = new THREE.Mesh(new THREE.SphereGeometry(sphereR, 16, 16), matColonyBuilding);
            bioSphere.position.set(sx, baseY + h * 0.25 + sphereR * 0.85, 0);
            bGroup.add(bioSphere);
        });

        const stack = new THREE.Mesh(new THREE.CylinderGeometry(7.0, 10.0, h * 0.75, 12), matTitaniumFrame);
        stack.position.set(0, baseY + h * 0.625, -18.0);
        bGroup.add(stack);
    }
    return bGroup;
}

const domeRadius = 560.0;
const domeMat = new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, roughness: 0.22, metalness: 0.1, transparent: true, opacity: 0.36 });
const baseYColony = -4.4;

for (let dm = 0; dm < 14; dm++) {
    const s = (dm % 2 === 0) ? -1 : 1;
    const dz = 2200.0 + dm * 2500.0;
    const cx = s * 1020.0;

    // バイオドーム本体
    const bioDome = new THREE.Mesh(new THREE.SphereGeometry(domeRadius, 36, 18, 0, Math.PI * 2, 0, Math.PI * 0.5), domeMat);
    bioDome.position.set(cx, baseYColony, dz);
    runwayScrollGroup.add(bioDome);

    // ドーム裾野の重厚な「多角形コロニー基礎隔壁リング」
    const collarRing = new THREE.Mesh(new THREE.TorusGeometry(domeRadius, 18.0, 10, 32), matColonyAccent);
    collarRing.rotation.x = Math.PI / 2;
    collarRing.position.set(cx, baseYColony + 8.0, dz);
    runwayScrollGroup.add(collarRing);

    // 次のドームと繋がる「地上チューブ回廊（ハイパーループ連絡管）」
    if (dm < 12) {
        const tubeCorridor = new THREE.Mesh(new THREE.CylinderGeometry(14.0, 14.0, 5000.0, 12), matColonyAccent);
        tubeCorridor.rotation.x = Math.PI / 2;
        tubeCorridor.position.set(cx, baseYColony + 14.0, dz + 2500.0);
        runwayScrollGroup.add(tubeCorridor);
    }

    // ドーム内部へ建物の配置（r < 0.78 R、最大高さ h_max <= 0.72 * sqrt(R^2 - r^2) を厳密遵守）
    for (let b = 0; b < 14; b++) {
        const ang = (b / 14) * Math.PI * 2 + dm * 0.5;
        const radDist = (0.18 + ((b * 37) % 100) / 100.0 * 0.58) * domeRadius; // 最大でも 0.76 * R
        const dx = Math.cos(ang) * radDist;
        const dzz = Math.sin(ang) * radDist;

        // ドーム天井高を厳密計算し、72%以下に制限して貫通を完全防止
        const domeCeilingAtPoint = Math.sqrt(Math.max(0.0, domeRadius * domeRadius - radDist * radDist));
        const safeMaxHeight = domeCeilingAtPoint * 0.72;
        const actualHeight = safeMaxHeight * (0.55 + ((b * 19) % 100) / 100.0 * 0.45);

        const buildingObj = createProceduralSFBuilding(b % 4, actualHeight, baseYColony);
        buildingObj.position.set(cx + dx, 0, dz + dzz);
        runwayScrollGroup.add(buildingObj);
    }
}

// ⑤ 滑走路の遥か奥（ドーム外）にそびえ立つ、高さ3,200m級の「軌道エレベーター基部メガストラクチャー」
const spaceElevatorGroup = new THREE.Group();
spaceElevatorGroup.position.set(0, baseYColony, 38500.0);
runwayScrollGroup.add(spaceElevatorGroup);

const seBasePyramid = new THREE.Mesh(new THREE.CylinderGeometry(180.0, 680.0, 520.0, 8), matColonyBuilding);
seBasePyramid.position.y = 260.0;
spaceElevatorGroup.add(seBasePyramid);

const seTetherTower = new THREE.Mesh(new THREE.CylinderGeometry(42.0, 95.0, 3400.0, 12), matTitaniumFrame);
seTetherTower.position.y = 1700.0;
spaceElevatorGroup.add(seTetherTower);

const seOrbitalRing = new THREE.Mesh(new THREE.TorusGeometry(320.0, 24.0, 12, 36), matColonyBuilding);
seOrbitalRing.rotation.x = Math.PI / 2;
seOrbitalRing.position.y = 1450.0;
spaceElevatorGroup.add(seOrbitalRing);

// 【魔改造5】滑走路両脇の「電磁アレスティング・パイロン＆減速エネルギー網」
const arrestingPylons = [];
const arrestingBeams = [];
const arrestingBeamMat = new THREE.MeshBasicMaterial({
    color: 0x10b981,
    transparent: true,
    opacity: 0.0,
    blending: THREE.AdditiveBlending
});

for (let ap = 0; ap < 28; ap++) {
    const pz = 800.0 + ap * 1200.0;
    for (let side of [-1, 1]) {
        const pylon = new THREE.Mesh(new THREE.BoxGeometry(4.5, 22.0, 6.0), matTitaniumFrame);
        pylon.position.set(side * 96.0, 6.5, pz);
        pylon.rotation.z = side * 0.25;
        runwayScrollGroup.add(pylon);
        arrestingPylons.push(pylon);
    }
    // 左右パイロン間を結ぶ減速エネルギーフィールド・レーザーグリッド
    const beamMesh = new THREE.Mesh(new THREE.PlaneGeometry(184.0, 12.0), arrestingBeamMat);
    beamMesh.position.set(0, 6.0, pz);
    runwayScrollGroup.add(beamMesh);
    arrestingBeams.push(beamMesh);
}

// 距離減衰シェーダー付き誘導灯
const guideLightMat = new THREE.ShaderMaterial({
    vertexShader: `
        varying float vDist;
        void main() {
            vec4 wp = modelMatrix * instanceMatrix * vec4(position, 1.0);
            vDist = length(cameraPosition - wp.xyz);
            gl_Position = projectionMatrix * viewMatrix * wp;
        }
    `,
    fragmentShader: `
        varying float vDist;
        void main() {
            float fade = smoothstep(8500.0, 600.0, vDist);
            gl_FragColor = vec4(0.06, 0.72, 0.50, fade * 0.85);
        }
    `,
    transparent: true
});
const dummyLight = new THREE.Object3D();
const approachLightsInst = new THREE.InstancedMesh(new THREE.BoxGeometry(1.4, 0.5, 2.2), guideLightMat, 240);
for (let al = 0; al < 120; al++) {
    const lz = al * 300.0;
    dummyLight.position.set(-84.0, -2.4, lz); dummyLight.updateMatrix(); approachLightsInst.setMatrixAt(al * 2, dummyLight.matrix);
    dummyLight.position.set(84.0, -2.4, lz); dummyLight.updateMatrix(); approachLightsInst.setMatrixAt(al * 2 + 1, dummyLight.matrix);
}
runwayScrollGroup.add(approachLightsInst);

// 空中進入経路のホログラフィックILSスカイ・ゲート
const ilsGateMat = new THREE.MeshBasicMaterial({
    color: 0x38bdf8,
    transparent: true,
    opacity: 0.42,
    blending: THREE.AdditiveBlending
});
for (let g = 0; g < 10; g++) {
    const gz = 1800.0 + g * 1800.0;
    const gy = 35.0 + g * 85.0;
    const gateGroup = new THREE.Group();
    gateGroup.position.set(0, gy, gz);

    const wGate = 75.0 + g * 8.0;
    const hGate = 38.0 + g * 4.0;
    const barThick = 1.4;

    const topBar = new THREE.Mesh(new THREE.BoxGeometry(wGate, barThick, barThick), ilsGateMat);
    topBar.position.y = hGate * 0.5;
    const btmBar = new THREE.Mesh(new THREE.BoxGeometry(wGate, barThick, barThick), ilsGateMat);
    btmBar.position.y = -hGate * 0.5;
    const leftBar = new THREE.Mesh(new THREE.BoxGeometry(barThick, hGate, barThick), ilsGateMat);
    leftBar.position.x = -wGate * 0.5;
    const rightBar = new THREE.Mesh(new THREE.BoxGeometry(barThick, hGate, barThick), ilsGateMat);
    rightBar.position.x = wGate * 0.5;

    gateGroup.add(topBar, btmBar, leftBar, rightBar);
    runwayScrollGroup.add(gateGroup);
}

// 恒星周回軌道用：ダイソン・スウォーム＆恒星コロナシェーダー＋採掘レーザー
const dysonStation = new THREE.Mesh(new THREE.TorusGeometry(130.0, 9.0, 16, 64), matTitaniumFrame);
dysonStation.position.set(0, 0, 140.0);
orbitGoalGroup.add(dysonStation);

const starCoronaMat = new THREE.ShaderMaterial({
    vertexShader: `varying vec3 vNormal; varying vec3 vLocal; void main() { vLocal = position; vNormal = normalize(normalMatrix * normal); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }`,
    fragmentShader: `
        varying vec3 vNormal; varying vec3 vLocal; uniform float uTime; uniform vec3 uBaseCol;
        void main() {
            float pulse = 0.85 + 0.15 * sin(vLocal.x * 0.015 + uTime * 3.0) * cos(vLocal.y * 0.015 - uTime * 2.5);
            vec3 core = mix(uBaseCol, vec3(1.0, 0.85, 0.45), pulse * 0.65);
            gl_FragColor = vec4(core, 1.0);
        }
    `,
    uniforms: { uTime: { value: 0.0 }, uBaseCol: { value: new THREE.Color(cfg.dest_color) } }
});
const starCore = new THREE.Mesh(new THREE.SphereGeometry(3200, 64, 64), starCoronaMat);
starCore.position.set(0, 0, 8200);
orbitGoalGroup.add(starCore);

const miningBeam = new THREE.Mesh(
    new THREE.CylinderGeometry(3.5, 14.0, 8000, 16, 1, true),
    new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.45, blending: THREE.AdditiveBlending })
);
miningBeam.rotation.x = Math.PI / 2;
miningBeam.position.set(0, 0, 4100);
orbitGoalGroup.add(miningBeam);

// =========================================================================
// 9. 再生コントローラー
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
// 10. 軌道レーダー
// =========================================================================
function drawRadar(prog, vc, mach, altKm, phase) {
    const rw = radarCanvas.width, rh = radarCanvas.height;
    rCtx.clearRect(0, 0, rw, rh);

    const isSolar = (prog >= 0.16 && prog < 0.78);
    radarLabelEl.innerHTML = isSolar ? `TACTICAL RADAR<br><span style="color:#10b981;font-size:8px;">INTERPLANETARY SCALE</span>` : `TACTICAL RADAR<br><span style="color:#38bdf8;font-size:8px;">APPROACH & VECTOR</span>`;

    const leftX = 90, rightX = rw - 90, midY = rh / 2;

    rCtx.strokeStyle = 'rgba(56,189,248,0.35)';
    rCtx.lineWidth = 3;
    rCtx.beginPath();
    rCtx.moveTo(leftX, midY);
    rCtx.lineTo(rightX, midY);
    rCtx.stroke();

    rCtx.textAlign = "center";
    rCtx.textBaseline = "middle";

    if (!isSolar) {
        const destLabel = cfg.goal_type === "orbit" ? "ORBIT STATION" : "RUNWAY 04L";
        [
            { x: leftX, lbl: "EARTH PAD" },
            { x: leftX + (rightX - leftX) * 0.5, lbl: "TRANSIT" },
            { x: rightX, lbl: destLabel }
        ].forEach(m => {
            rCtx.fillStyle = '#38bdf8';
            rCtx.beginPath();
            rCtx.arc(m.x, midY, 6, 0, Math.PI * 2);
            rCtx.fill();

            rCtx.font = 'bold 18px monospace';
            rCtx.fillStyle = '#f8fafc';
            rCtx.fillText(m.lbl, m.x, midY - 24);
        });

        const curX = leftX + THREE.MathUtils.clamp(prog, 0.0, 1.0) * (rightX - leftX);
        rCtx.fillStyle = '#f43f5e';
        rCtx.beginPath();
        rCtx.arc(curX, midY, 9, 0, Math.PI * 2);
        rCtx.fill();

        rCtx.font = 'bold 17px monospace';
        rCtx.fillStyle = '#fbbf24';
        rCtx.fillText(`${(prog * 100).toFixed(1)}% [${phase.slice(0, 14)}]`, curX, midY + 24);
    } else {
        const curX = leftX + ((prog - 0.16) / 0.62) * (rightX - leftX);
        rCtx.fillStyle = '#10b981';
        rCtx.beginPath();
        rCtx.arc(curX, midY, 10, 0, Math.PI * 2);
        rCtx.fill();

        rCtx.font = 'bold 18px monospace';
        rCtx.fillStyle = '#6ee7b7';
        rCtx.fillText(`WARP TRANSIT // ${(prog * 100).toFixed(1)}%`, curX, midY + 24);
    }
}

// =========================================================================
// 11. 60fps アニメーションループ
// =========================================================================
const cameraIdealPos = new THREE.Vector3();
const cameraLookTarget = new THREE.Vector3();
const shipWorldPos = new THREE.Vector3();
const anchorWorldPos = new THREE.Vector3();
const anchorWorldQuat = new THREE.Quaternion();
let runwayAccumZ = 0.0;
let prevProg = 0.0;
const completeBannerEl = document.getElementById('complete-banner');

function animate(now) {
    requestAnimationFrame(animate);

    const delta = (now - lastTimestamp) / 1000.0;
    const nowSec = now * 0.001;
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
    const radD = L('rad_deploy'), wingSw = L('wing_sweep'), sparkArc = L('spark_arc');
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
        else if (f0.phase === "GLIDESLOPE_FINAL_APPROACH") speakCallout("Glideslope locked. ILS gates active.");
        else if (f0.phase === "FINAL_FLARE_HOLD") speakCallout("Minimums. Flare.");
        else if (f0.phase === "MAIN_GEAR_TOUCHDOWN") speakCallout("Touchdown! Arresting field active.");
        else if (f0.phase === "ROLLOUT_REVERSE_THRUST") speakCallout("Reverse thrust. Chute deployed.");
        else if (f0.phase === "PLANETARY_RUNWAY_SECURED") speakCallout("Runway secured. Welcome to colony.");
        else if (f0.phase === "ORBITAL_STATION_DOCKED") speakCallout("Dyson station rendezvous complete.");
    }

    // スカイドーム制御
    const spaceFade = THREE.MathUtils.clamp((altKm - 15.0) / 65.0, 0.0, 1.0);
    atmoSkyMat.uniforms.uSpaceFade.value = spaceFade;
    spaceFieldGroup.visible = (spaceFade > 0.05);

    // 機体姿勢
    shipPitchGroup.rotation.set(-THREE.MathUtils.degToRad(pitchDeg), THREE.MathUtils.degToRad(yawDeg), THREE.MathUtils.degToRad(rollDeg));

    let suspensionBounce = 0.0;
    if (f0.phase === "MAIN_GEAR_TOUCHDOWN") {
        const bouncePhase = ((currentTime - f0.t) / (dtFrame || 1.0)) * 5.0;
        suspensionBounce = Math.sin(bouncePhase * Math.PI) * Math.exp(-bouncePhase * 0.8) * 0.18;
    }
    shipMeshGroup.position.set(
        Math.sin(now * 0.003) * 0.22 + (Math.random() - 0.5) * vib,
        Math.cos(now * 0.004) * 0.16 - suspensionBounce + (Math.random() - 0.5) * vib,
        Math.sin(now * 0.002) * 0.30
    );

    shipMeshGroup.getWorldPosition(shipWorldPos);

    // 中空超伝導グラビティ・リング常時回転
    const spinBoost = 1.0 + engPwr * 2.5 + wAct * 6.0;
    gravityOuterBarrel.rotation.z += 0.018 * spinBoost;
    gravityInnerBarrel.rotation.z -= 0.028 * spinBoost;

    // アンチコリジョン・ストロボ点滅
    const strobeFlash = (Math.sin(now * 0.005) > 0.88) ? 1.0 : 0.0;
    strobeLights.forEach(sl => { sl.visible = (strobeFlash > 0.5); });

    // 黒体放射サーマルグロー＆ラジエーター加熱制御
    const heatFactor = THREE.MathUtils.clamp((tempK - 850.0) / 1400.0, 0.0, 1.0);
    matBellyTile.emissiveIntensity = heatFactor * 1.45;
    matRadiatorGlow.emissiveIntensity = heatFactor * 1.25;

    radiatorPivots.forEach(rp => {
        rp.pivot.scale.set(Math.max(0.001, radD), 1, 1);
        rp.pivot.rotation.z = rp.side * radD * 0.25;
    });

    // X字マグネティック・ナセル角度連動
    wingPivots.forEach(wp => {
        wp.group.rotation.y = wp.side * wingSw * 0.32;
        wp.group.rotation.z = wp.baseTilt + wp.side * wingSw * 0.08;
    });

    // 8枚可変ベクター・電磁ペタルノズル稼働
    emPetals.forEach(ep => {
        const wave = Math.sin(nowSec * 6.0 + ep.index) * 0.04 * engPwr;
        ep.pivot.rotation.x = -0.25 + engPwr * 0.32 + wave;
    });

    // ダイナミックFOV＆ニアクリップ切替
    let targetFov = 55.0;
    if (f0.phase === "CATAPULT_RAIL_ACCEL" || f0.phase === "ALCUBIERRE_HYPER_WARP") {
        targetFov = 55.0 + (gLoad / 10.0) * 20.0;
    } else if (f0.phase.includes("TOUCHDOWN") || f0.phase.includes("ROLLOUT")) {
        targetFov = 48.0;
    }
    cameraMain.fov = THREE.MathUtils.lerp(cameraMain.fov, targetFov, 0.08);
    cameraMain.near = (activeCamMode === 2) ? 0.08 : 0.5;
    cameraMain.updateProjectionMatrix();

    // 【魔改造3】コクピットカメラ切替＆3Dホログラム・油圧ダンパー稼働
    cockpitInteriorGroup.visible = (activeCamMode === 2);
    if (activeCamMode === 2) {
        spineGroup.visible = false;
        canopyGlass.visible = false;

        // 物理量子ジャイロコア3軸回転
        cabinGyroRingA.rotation.x = nowSec * 1.8;
        cabinGyroRingB.rotation.y = nowSec * 2.4;

        // Gフォース連動油圧ダンパー伸縮
        const damperOffset = Math.sin(nowSec * 18.0) * vib * 0.04 + (gLoad - 1.0) * 0.003;
        cabinDampers.forEach(dp => { dp.position.y = -0.14 - damperOffset; });

        // 進行波ワイヤーフレーム地形スキャナーアニメーション
        const tScanAttr = terrainScanGeo.attributes.position;
        for (let ti = 0; ti < tScanAttr.count; ti++) {
            const tx = tScanAttr.getX(ti);
            const ty = tScanAttr.getY(ti);
            const tzWave = Math.sin(tx * 28.0 + nowSec * 4.0) * Math.cos(ty * 28.0 - nowSec * 6.0) * 0.015;
            tScanAttr.setZ(ti, tzWave);
        }
        tScanAttr.needsUpdate = true;

        holoSpoolRing.rotation.z = -nowSec * (1.0 + engPwr * 5.0);
        holoShipCone.rotation.z = -THREE.MathUtils.degToRad(rollDeg);
        holoShipCone.rotation.x = -Math.PI / 2 - THREE.MathUtils.degToRad(pitchDeg);
        holoShipMat.color.setHex(tempK > 1200 ? 0xf43f5e : (gLoad > 5.0 ? 0xf59e0b : 0x10b981));

        updateCockpitDisplays(mach, altKm, gLoad, pitchDeg, rollDeg, engPwr, f0.phase, tempK, nowSec, wAct);
        stickPivot.rotation.x = -pitchDeg * 0.015;
        stickPivot.rotation.z = -rollDeg * 0.015;
        throttlePivot.rotation.x = engPwr * 0.45;

        cockpitCamAnchor.getWorldPosition(anchorWorldPos);
        cockpitCamAnchor.getWorldQuaternion(anchorWorldQuat);
        cameraMain.position.copy(anchorWorldPos);
        cameraMain.quaternion.copy(anchorWorldQuat);
    } else {
        spineGroup.visible = true;
        canopyGlass.visible = true;

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

    // 【魔改造5】クライオ氷片＆プラズマ・スパークのカメラ横通過パーティクル更新
    if (cfg.cryo_steam && (mach > 0.2 || engPwr > 0.2)) {
        flybyMat.opacity = Math.min(0.85, (mach / 8.0) + engPwr * 0.35);
        const fbArr = flybyGeo.attributes.position.array;
        const flySpeed = (25.0 + mach * 18.0) * delta;
        for (let f = 0; f < flybyCount; f++) {
            fbArr[f * 3 + 2] -= flySpeed;
            if (fbArr[f * 3 + 2] < shipWorldPos.z - 95.0) {
                fbArr[f * 3] = shipWorldPos.x + (Math.random() - 0.5) * 70.0;
                fbArr[f * 3 + 1] = shipWorldPos.y + (Math.random() - 0.5) * 40.0;
                fbArr[f * 3 + 2] = shipWorldPos.z + 65.0 + Math.random() * 40.0;
            }
        }
        flybyGeo.attributes.position.needsUpdate = true;
    } else {
        flybyMat.opacity = 0.0;
    }

    // 地球メガフロート・海面・富士山・雲海制御
    if (prog === 0.0 && altKm < 110.0) {
        catapultSlopeRoot.visible = true;
        groundEnvMover.visible = true;
        railMover.position.set(0, 0, -distM);
        const actualAltM = altKm * 1000.0 - 40.0;
        groundEnvMover.position.set(0, -actualAltM, -distM * 0.7);

        oceanShaderMat.uniforms.uTime.value = nowSec;
        seaOfCloudsMat.uniforms.uTime.value = nowSec;
        const groundFade = THREE.MathUtils.clamp(1.0 - (altKm - 30.0) / 40.0, 0.0, 1.0);
        oceanShaderMat.uniforms.uOpacity.value = 0.96 * groundFade;
        fujiShaderMat.uniforms.uOpacity.value = groundFade;
        seaOfCloudsMat.uniforms.uOpacity.value = groundFade;
    } else {
        catapultSlopeRoot.visible = false;
        groundEnvMover.visible = false;
    }

    // 地球球体＆大気散乱リム
    if (altKm >= 20.0 && prog < 0.30) {
        earthGroup.visible = true;
        const earthFade = THREE.MathUtils.clamp((altKm - 20.0) / 25.0, 0.0, 1.0);
        earthShaderMat.uniforms.uOpacity.value = earthFade;
        atmoHaloMat.uniforms.uOpacity.value = earthFade;
        const warpRecede = Math.pow(Math.max(0, prog - 0.05) * 18.0, 3.0);
        earthGroup.position.set(0, -25050 - altKm * 120.0 - warpRecede * 35000.0, -4000 - distM * 0.6 - warpRecede * 95000.0);
    } else {
        earthGroup.visible = false;
    }

    // カタパルト電磁アーク放電
    if (sparkArc > 0.1 && f0.phase === "CATAPULT_RAIL_ACCEL") {
        arcMat.opacity = sparkArc * (0.4 + Math.random() * 0.6);
        arcBolts.forEach((bolt, bIdx) => {
            bolt.visible = true;
            const arr = bolt.geometry.attributes.position.array;
            const side = (bIdx % 2 === 0) ? -1 : 1;
            for (let k = 0; k < 10; k++) {
                arr[k * 3] = side * (1.2 + Math.random() * 2.4);
                arr[k * 3 + 1] = -0.8 - Math.random() * 1.8;
                arr[k * 3 + 2] = 12.0 - k * 2.6 + (Math.random() - 0.5) * 1.2;
            }
            bolt.geometry.attributes.position.needsUpdate = true;
        });
    } else {
        arcBolts.forEach(bolt => { bolt.visible = false; });
    }

    // 2層流体リボン・マッハコーン放物線衝撃波
    if (cfg.mach_cone_vfx && (vaporA > 0.05 || pAlpha > 0.05)) {
        machConeMat.uniforms.uAlpha.value = Math.max(vaporA, pAlpha);
        machConeMat.uniforms.uTime.value = nowSec;
        machConeMesh.scale.set(1.0 + mach * 0.03, 1.0 + mach * 0.03, 1.0);
        outerShockCone.scale.set(1.05 + mach * 0.035, 1.05 + mach * 0.035, 1.05);
    } else {
        machConeMat.uniforms.uAlpha.value = 0.0;
    }

    // 【魔改造1】磁気ピンチ紡錘プラズマトーチ＆立体ショックダイヤモンド＆磁気リング制御
    if (currentTime >= -1.8 && engPwr > 0.01) {
        plumeRoot.visible = true;
        const flameLength = Math.max(0.08, Math.pow(engPwr, 1.35));
        plumeRoot.scale.set(engPwr, engPwr, flameLength);
        shockShaderMat.uniforms.uTime.value = nowSec;
        shockShaderMat.uniforms.uWarp.value = wAct;
        outerFlameMat.uniforms.uTime.value = nowSec;

        // 立体ショックダイヤモンド結晶の脈動と間隔調整
        shockDiamonds.forEach(sd => {
            const vibScale = sd.baseScale * (0.88 + 0.24 * Math.sin(nowSec * 36.0 - sd.index * 1.5));
            sd.group.scale.set(vibScale, vibScale, vibScale * (0.8 + engPwr * 0.5));
            sd.group.position.z = -3.4 - sd.index * (3.6 + engPwr * 1.6);
        });

        // 磁気コンファインメント・プラズマリングの後方収縮フロー
        magneticRings.forEach(mr => {
            const cycle = (nowSec * 2.6 + mr.phaseOffset) % 1.0; // 0 -> 1
            mr.mesh.position.z = -1.5 - cycle * 34.0;
            const pinchRadius = Math.max(0.05, (1.0 - Math.pow(cycle, 0.85)) * 1.15);
            mr.mesh.scale.set(pinchRadius, pinchRadius, 1.0);
        });
    } else {
        plumeRoot.visible = false;
    }

    // 3軸重力制御ジャイロ＆ワープリング
    if (ringL > 0.01) {
        warpRingAssembly.scale.setScalar(ringL);
        warpRingAssembly.position.y = THREE.MathUtils.lerp(0.35, 1.5, ringL);
        rotorClockwise.rotation.z += 0.035 * ringL;
        rotorCounter.rotation.z -= 0.04 * ringL;
        gyroGimbalInner.rotation.x += 0.045 * ringL;
        gyroGimbalInner.rotation.y += 0.03 * ringL;
    } else {
        warpRingAssembly.scale.set(0.001, 0.001, 0.001);
    }

    bayDoors.forEach(bd => { bd.pivot.rotation.z = -bd.side * bayO * 1.5; });
    speedbrakePivot.rotation.x = speedbrake * 0.75;
    elevonMeshes.forEach(em => { em.mesh.rotation.x = Math.sin(now * 0.005) * 0.15 + THREE.MathUtils.degToRad(-pitchDeg * 0.3); });
    irisPaddles.forEach(ip => { ip.rotation.x = -0.35 + L('nozzle_open') * 0.48; });
    landingGears.forEach(lg => { lg.scale.setScalar(Math.max(0.001, gearD)); });

    // タイヤ接地白煙の後方流去
    if (tdSmoke > 0.05) {
        smokePuffs.forEach(p => {
            p.material.opacity = tdSmoke * 0.85;
            p.position.z -= (runwaySpd > 10.0 ? runwaySpd : 50.0) * delta * 0.85;
            if (p.position.z < -65.0) {
                p.position.set((Math.random() - 0.5) * 4.5, -2.6, -6.0 - Math.random() * 3.0);
            }
        });
    } else {
        smokePuffs.forEach(p => { p.material.opacity = 0.0; });
    }

    if (chuteD > 0.01) {
        chuteGroup.scale.setScalar(chuteD);
        chuteCanopy.rotation.z += 0.02;
    } else {
        chuteGroup.scale.setScalar(0.001);
    }

    // 目的地滑走路・都市・電磁アレスティング網制御
    if (prog > 0.78) {
        destWorld.visible = true;
        if (cfg.goal_type === "landing") {
            runwayScrollGroup.visible = true;
            orbitGoalGroup.visible = false;
            destWorld.position.y = -altKm * 1000.0;

            if (prevProg <= 0.78) {
                runwayAccumZ = 0.0;
            }
            if (runwaySpd > 0.01 && isPlaying) {
                runwayAccumZ += runwaySpd * delta;
                runwayScrollGroup.position.z = -runwayAccumZ;
            }

            // タッチダウン〜減速中の電磁アレスティング・エネルギー網展開
            if (f0.phase === "MAIN_GEAR_TOUCHDOWN" || f0.phase === "ROLLOUT_REVERSE_THRUST") {
                arrestingBeamMat.opacity = 0.35 + 0.25 * Math.sin(nowSec * 14.0);
            } else {
                arrestingBeamMat.opacity = 0.0;
            }
        } else {
            runwayScrollGroup.visible = false;
            orbitGoalGroup.visible = true;
            dysonStation.rotation.y += 0.005;
            starCoronaMat.uniforms.uTime.value = nowSec;
        }
    } else {
        destWorld.visible = false;
    }
    prevProg = prog;

    // アルクビエレ・ワープバブル＆高次元ボリュメトリックトンネル流動
    const bubbleIntensity = Math.max(wCharge * 0.65, wAct);
    warpBubbleMesh.visible = (bubbleIntensity > 0.02);
    warpBubbleMat.uniforms.uTime.value = nowSec;
    warpBubbleMat.uniforms.uIntensity.value = bubbleIntensity;

    warpGroup.scale.setScalar(wAct > 0.05 ? 1.0 : 0.0001);
    if (wAct > 0.05) {
        warpTunnelMat.uniforms.uTime.value = nowSec;
        warpTunnelMat.uniforms.uVc.value = vc;
        warpGroup.rotation.z += 0.025;
        const sArr = starGeo.attributes.position.array;
        const stretchLen = 55.0 + vc * 240.0;
        for (let i = 0; i < starCount; i++) {
            let z = sArr[i * 6 + 2] - (28.0 + vc * 72.0);
            if (z < -320.0) z = 320.0;
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
    warpPass.uniforms.uTime.value = nowSec;

    // 音響シンセ制御
    if (actx) {
        const pwr = engPwr * duckingFactor;
        rocketGain.gain.setTargetAtTime(pwr * 0.45, actx.currentTime, 0.05);
        if (rocketLpf) {
            rocketLpf.frequency.setTargetAtTime(180 + pwr * 420, actx.currentTime, 0.05);
        }

        const crackleAmount = Math.max(0.0, (pwr - 0.78) / 0.22);
        crackleGain.gain.setTargetAtTime(crackleAmount * 0.35, actx.currentTime, 0.04);

        const subBassLevel = (pwr > 0.6 || wAct > 0.5) ? (pwr * 0.35) : 0.0001;
        subBassGain.gain.setTargetAtTime(subBassLevel, actx.currentTime, 0.05);
    }

    drawRadar(prog, vc, mach, altKm, f0.phase);

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
