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
# 💥 タイムライン物理データ（機首前向き統一・エアブレーキ＆リアル滑走路着陸）
# =========================================================================
def build_timeline(preview_only=False):
    if preview_only:
        return [{
            "t": -5.0, "phase": "PAD_STANDBY", "dist_m": 0.0, "alt_km": 0.04,
            "mach": 0.0, "vc": 0.0, "g": 1.0, "temp_k": 288.0,
            "clamp_open": 0.0, "sabot_purge": 0.0, "booster_purge": 0.0, "fairing_purge": 0.0,
            "gear_deploy": 0.0, "speedbrake": 0.0, "chute_deploy": 0.0, "touchdown_smoke": 0.0,
            "wing_sweep": 0.0, "bay_open": 0.0, "ring_lift": 0.0, "rad_deploy": 0.0,
            "nozzle_open": 0.2, "engine_power": 0.0, "spark_arc": 0.0,
            "vapor_alpha": 0.0, "plasma_alpha": 0.0, "warp_charge": 0.0,
            "warp_lens": 0.0, "warp_active": 0.0, "warp_boom": 0.0,
            "rcs_burst": 0.0, "shield_hit": 0.0,
            "pitch_deg": float(env_cfg["angle_deg"]), "yaw_deg": 0.0, "roll_deg": 0.0,
            "vib": 0.0, "progress": 0.0, "ship_time": 0.0,
        }]

    dt = 0.25
    frames = []
    base_pitch = float(env_cfg["angle_deg"])
    exit_mach = float(vessel_cfg["catapult_mach"] * (coil_charge / 100.0))

    # 発射前待機
    for step in range(20):
        t = -5.0 + step * dt
        eng_pre = float(np.clip((t + 1.8) / 1.8, 0.0, 0.7))
        clamp = float(np.clip((t + 0.4) / 0.4, 0.0, 1.0))
        frames.append({
            "t": float(round(t, 2)),
            "phase": "CRYO_VENTING" if t < -3.0 else "LINEAR_COIL_CHARGE",
            "dist_m": 0.0, "alt_km": 0.04, "mach": 0.0, "vc": 0.0,
            "g": 1.0 + eng_pre * 0.9, "temp_k": 288.0 + eng_pre * 140.0,
            "clamp_open": clamp, "sabot_purge": 0.0, "booster_purge": 0.0, "fairing_purge": 0.0,
            "gear_deploy": 0.0, "speedbrake": 0.0, "chute_deploy": 0.0, "touchdown_smoke": 0.0,
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
    booster_p = 0.0
    fairing_p = 0.0
    gear_d = 0.0
    speedbrake = 0.0
    chute_d = 0.0
    td_smoke = 0.0
    bay_o = 0.0
    ring_l = 0.0
    rad_d = 0.0

    total_steps = 280
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

        if t <= 5.0:
            phase = "CATAPULT_RAIL_ACCEL"
            accel_ratio = t / 5.0
            mach = (accel_ratio**1.3) * exit_mach
            speed_ms = mach * 340.0
            dist_m += speed_ms * dt * 0.45
            alt_km = 0.04 + (dist_m * np.sin(rad_pitch)) / 1000.0
            g_load = 12.0 * (coil_charge / 100.0)
            eng_pwr = 1.0
            nozzle = 0.95
            spark_arc = 1.0
            wing_sw = float(np.clip((mach - 1.5) / 10.0, 0.0, 1.0))
            if 0.85 <= mach <= 2.4:
                vapor = float(1.0 - abs(mach - 1.6) / 0.8)
            vib = 0.28 + vapor * 0.35
            pitch_cur = base_pitch

        elif alt_km < 90.0 and t < 15.0:
            phase = "STRATOSPHERE_CLIMB" if alt_km < 45.0 else "EXOSPHERE_INSERTION"
            sabot_p = min(1.0, sabot_p + 1.0 * dt)
            mach = min(45.0, mach + 4.0 * dt)
            speed_ms = mach * 340.0
            dist_m += speed_ms * dt * 0.75
            space_f = float(np.clip((alt_km - 10.0) / 75.0, 0.0, 1.0))
            pitch_cur = max(14.0, base_pitch * (1.0 - space_f * 0.6))
            alt_km += (speed_ms * np.sin(np.radians(pitch_cur)) * dt) / 1000.0
            g_load = 5.8
            eng_pwr = 1.0
            nozzle = 1.0
            wing_sw = 1.0
            roll_deg = np.sin(t * 0.8) * 8.0
            if 12.0 <= alt_km <= 75.0:
                plasma = float(np.sin(((alt_km - 12.0) / 63.0) * np.pi) ** 0.75)
            if alt_km >= 50.0 and aux_boosters:
                booster_p = min(1.0, booster_p + 0.8 * dt)
                if booster_p < 0.5:
                    rcs = 1.0
            vib = plasma * 0.45 + 0.12

        elif progress < 0.16:
            phase = "WARP_FIELD_COMPRESSION"
            alt_km = 120.0 + (progress / 0.16) * 280.0
            pitch_cur = max(0.0, 14.0 * (1.0 - progress / 0.16))
            eng_pwr = 0.7
            nozzle = 0.8
            g_load = 1.8
            wing_sw = 0.4
            progress += 0.018 * dt
            morph_prog = float(np.clip(progress / 0.16, 0.0, 1.0))
            bay_o = float(np.clip(morph_prog * 2.2, 0.0, 1.0))
            ring_l = float(np.clip((morph_prog - 0.2) * 2.0, 0.0, 1.0))
            rad_d = float(np.clip((morph_prog - 0.4) * 1.8, 0.0, 1.0))
            if vessel_cfg["style"] == "massdriver_spear":
                fairing_p = min(1.0, fairing_p + 1.0 * dt)
            w_charge = float(np.clip((morph_prog - 0.15) / 0.85, 0.0, 1.0))
            if morph_prog > 0.5:
                w_lens = float(np.sin(((morph_prog - 0.5) / 0.5) * (np.pi / 2)))
            if morph_prog > 0.92:
                w_boom = 1.0
            rcs = 1.0 if (0.1 < morph_prog < 0.35) else 0.0
            vc = 0.05 + w_charge * 0.25
            vib = 0.12 + w_charge * 0.22

        elif progress < 0.70:
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
            vc = min(target_vc, vc + 0.15 * dt)
            w_active = 1.0
            w_charge = 1.0
            g_load = 1.2
            vib = 0.06
            progress += (0.018 + vc * 0.04) * dt
            roll_deg = np.sin(t * 0.3) * 4.0
            if progress >= 0.68:
                w_boom = 1.0

        elif progress < 0.82:
            phase = "DEBRIS_AERO_BRAKING"
            # 前向きのままエアブレーキと逆噴射ベクター、六角形シールドで迎撃
            alt_km = 99999.0
            pitch_cur = 8.0
            yaw_deg = 0.0
            roll_deg = np.sin(t * 1.2) * 6.0
            speedbrake = 1.0
            bay_o = 0.5
            ring_l = 0.2
            rad_d = 1.0
            wing_sw = 0.3
            eng_pwr = 0.35
            nozzle = 0.5
            vc = max(0.01, vc * 0.93)
            g_load = 4.2
            vib = 0.20
            progress += 0.02 * dt
            shield = float(np.sin(t * 8.0) ** 2) if 0.72 < progress < 0.78 else 0.0

        elif progress < 0.92:
            phase = "ATMOSPHERIC_ENTRY_GLIDESLOPE"
            # 惑星大気圏へ前向き高速突入・雲海突破
            descent_p = (progress - 0.82) / 0.10
            alt_km = float(np.clip(120.0 * (1.0 - descent_p), 1.5, 120.0))
            mach = float(max(1.5, 15.0 * (1.0 - descent_p)))
            vc = 0.0
            pitch_cur = 12.0 * (1.0 - descent_p) - 2.0 * descent_p
            roll_deg = np.sin(descent_p * np.pi * 3.0) * 10.0  # 気流乱れによる微小ロール
            plasma = float(np.sin(descent_p * np.pi) ** 1.2) if descent_p < 0.6 else 0.0
            vapor = float(np.sin(descent_p * np.pi) ** 1.5) if descent_p >= 0.5 else 0.0
            g_load = 4.0 * (1.0 - descent_p * 0.5)
            eng_pwr = 0.4
            nozzle = 0.6
            bay_o = 0.0
            ring_l = 0.0
            rad_d = 0.0
            wing_sw = 0.1
            speedbrake = 0.8
            vib = plasma * 0.5 + 0.15
            progress += 0.016 * dt

        elif progress < 0.97:
            phase = "FINAL_APPROACH_FLARE"
            # 高度1,500m〜0m、進入灯に乗り、機首を引き起こすフレア操作
            flare_p = (progress - 0.92) / 0.05
            alt_km = float(max(0.02, 1.5 * (1.0 - flare_p)))
            mach = float(max(0.35, 1.5 * (1.0 - flare_p)))
            vc = 0.0
            # フレア操作：接地寸前に機首を+6度持ち上げる
            pitch_cur = -3.0 * (1.0 - flare_p) + 6.0 * flare_p
            roll_deg = np.sin(flare_p * np.pi * 2.0) * 3.0  # 横風修正
            gear_d = float(np.clip(flare_p * 2.0, 0.0, 1.0))
            speedbrake = 1.0
            g_load = 1.4
            eng_pwr = 0.15
            nozzle = 0.3
            vib = 0.08
            progress += 0.012 * dt

        else:
            phase = "TOUCHDOWN_ROLLOUT_STOP"
            # メインギア接地！白煙吹き上がり、ドラッグシュート展開、滑走停止
            rollout_p = (progress - 0.97) / 0.03
            alt_km = 0.0
            mach = float(max(0.0, 0.35 * (1.0 - rollout_p)))
            vc = 0.0
            pitch_cur = max(0.0, 6.0 * (1.0 - rollout_p * 2.5))  # 前輪が徐々に接地
            roll_deg = 0.0
            gear_d = 1.0
            speedbrake = 1.0
            chute_d = float(np.clip(rollout_p * 3.0, 0.0, 1.0))  # シュート開傘
            td_smoke = float(np.clip((1.0 - rollout_p) * 2.0, 0.0, 1.0))  # タイヤ白煙
            g_load = 1.0 + float(np.sin(rollout_p * np.pi)) * 0.6
            eng_pwr = 0.0
            nozzle = 0.2
            vib = 0.18 * (1.0 - rollout_p)
            progress = min(1.0, progress + 0.009 * dt)

        gamma = 1.0 / np.sqrt(max(0.001, 1.0 - (min(0.999, vc) ** 2)))
        ship_time += dt / gamma
        temp_k = 288.0 + plasma * 1750.0 + (w_active * 600.0) + (eng_pwr * 220.0)

        frames.append({
            "t": float(round(t, 2)), "phase": phase, "dist_m": float(dist_m), "alt_km": float(alt_km),
            "mach": float(mach), "vc": float(vc), "g": float(g_load), "temp_k": float(temp_k),
            "clamp_open": 1.0, "sabot_purge": float(sabot_p), "booster_purge": float(booster_p),
            "fairing_purge": float(fairing_p), "gear_deploy": float(gear_d),
            "speedbrake": float(speedbrake), "chute_deploy": float(chute_d), "touchdown_smoke": float(td_smoke),
            "wing_sweep": float(wing_sw), "bay_open": float(bay_o), "ring_lift": float(ring_l), "rad_deploy": float(rad_d),
            "nozzle_open": float(nozzle), "engine_power": float(eng_pwr), "spark_arc": float(spark_arc),
            "vapor_alpha": float(vapor), "plasma_alpha": float(plasma), "warp_charge": float(w_charge),
            "warp_lens": float(w_lens), "warp_active": float(w_active), "warp_boom": float(w_boom),
            "rcs_burst": float(rcs), "shield_hit": float(shield),
            "pitch_deg": float(pitch_cur), "yaw_deg": float(yaw_deg), "roll_deg": float(roll_deg),
            "vib": float(vib), "progress": float(progress), "ship_time": float(ship_time),
        })

        if progress >= 1.0:
            for extra in range(20):
                frames.append({
                    "t": float(round(t + (extra + 1) * dt, 2)), "phase": "PLANETARY_RUNWAY_SECURED",
                    "dist_m": float(dist_m), "alt_km": 0.0, "mach": 0.0, "vc": 0.0, "g": 1.0,
                    "temp_k": 310.0, "clamp_open": 1.0, "sabot_purge": 1.0, "booster_purge": float(booster_p),
                    "fairing_purge": float(fairing_p), "gear_deploy": 1.0, "speedbrake": 1.0,
                    "chute_deploy": 1.0, "touchdown_smoke": 0.0, "wing_sweep": 0.0,
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
# 📺 Three.js 完全映画仕様・極限細密＆ド迫力チェイス版 (Apex VFX Cinema Edition V7)
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
  z-index:1;touch-action:none;
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

/* ILS（計器着陸装置）HUDオーバーレイ */
#ils-hud{
  position:absolute;top:48%;left:50%;transform:translate(-50%,-50%);
  width:320px;height:220px;border:1px dashed rgba(16,185,129,0.4);border-radius:6px;
  pointer-events:none;z-index:35;display:none;flex-direction:column;justify-content:space-between;
  padding:8px 12px;font-family:monospace;color:#10b981;font-size:11px;
}
.ils-cross{position:absolute;top:50%;left:50%;width:100px;height:100px;transform:translate(-50%,-50%);pointer-events:none;}
.ils-cross::before{content:'';position:absolute;top:50%;left:0;width:100%;height:1px;background:#10b981;}
.ils-cross::after{content:'';position:absolute;top:0;left:50%;width:1px;height:100%;background:#10b981;}

#cinematic-banner{
  position:absolute;top:38%;left:50%;transform:translate(-50%,-50%);
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  pointer-events:none;z-index:85;opacity:0;transition:opacity 0.6s ease;
  text-shadow:0 0 25px rgba(56,189,248,0.8);
}
.cine-stage{font-size:13px;letter-spacing:4px;color:#38bdf8;font-weight:800;margin-bottom:4px;}
.cine-title{font-size:28px;letter-spacing:6px;color:#ffffff;font-weight:900;text-transform:uppercase;}

#subtitle-box{
  position:absolute;bottom:170px;left:20px;
  background:rgba(2,6,23,0.88);border-left:3px solid #10b981;
  padding:6px 14px;border-radius:3px;font-size:11px;font-family:monospace;
  color:#6ee7b7;letter-spacing:1.2px;box-shadow:0 4px 15px rgba(0,0,0,0.8);
  pointer-events:none;z-index:50;transition:opacity 0.3s;
}

.pip-window{
  position:absolute;top:70px;right:18px;
  width:340px;height:190px;
  border:2px solid rgba(56,189,248,0.85);border-radius:6px;
  background:rgba(2,6,23,0.45);
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

.playback-controller{
  position:absolute;bottom:148px;left:20px;right:20px;
  display:flex;align-items:center;gap:12px;background:rgba(2,6,23,0.78);
  border:1px solid rgba(56,189,248,0.3);padding:6px 14px;border-radius:6px;
  z-index:50;pointer-events:auto;backdrop-filter:blur(6px);
}
.play-btn{
  background:#0284c7;border:none;color:#fff;font-size:11px;font-weight:800;
  padding:4px 10px;border-radius:4px;cursor:pointer;outline:none;
}
.play-btn:hover{background:#0369a1;}
.speed-btn{
  background:rgba(15,23,42,0.8);border:1px solid rgba(56,189,248,0.4);
  color:#38bdf8;font-size:10px;font-weight:700;padding:4px 8px;border-radius:4px;cursor:pointer;
}
.speed-btn.active{background:#38bdf8;color:#020617;}
.scrub-slider{
  flex:1;-webkit-appearance:none;height:5px;border-radius:3px;
  background:rgba(56,189,248,0.25);outline:none;cursor:pointer;
}
.scrub-slider::-webkit-slider-thumb{
  -webkit-appearance:none;width:14px;height:14px;border-radius:50%;
  background:#38bdf8;cursor:pointer;box-shadow:0 0 8px #38bdf8;
}

.radar-panel{
  position:absolute;bottom:68px;left:0;
  width:100%;height:76px;
  background:rgba(2,6,20,0.92);
  border-top:1px solid rgba(56,189,248,0.45);
  border-bottom:1px solid rgba(56,189,248,0.2);
  display:flex;align-items:center;padding:0 20px;gap:14px;
  z-index:25;pointer-events:none;box-shadow:0 -6px 25px rgba(0,0,0,0.75);
}
.radar-tag{font-size:9.5px;color:#38bdf8;font-weight:900;white-space:nowrap;letter-spacing:1px;border-right:1px solid rgba(56,189,248,0.3);padding-right:12px;}
#radar-canvas{flex:1;height:62px;display:block;}

.hud-bottom{
  position:absolute;bottom:14px;left:0;width:100%;height:54px;
  background:linear-gradient(0deg,rgba(2,6,18,0.94) 0%,rgba(6,13,30,0.82) 100%);
  border-top:1px solid rgba(148,163,184,0.2);
  display:grid;grid-template-columns:repeat(5,1fr);align-items:center;
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

.cam-switcher{
  position:absolute;top:70px;left:20px;display:flex;gap:6px;z-index:50;pointer-events:auto;
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

<div id="ils-hud">
  <div style="display:flex;justify-content:space-between;">
    <span>ILS RUNWAY 04L</span>
    <span>GLIDESLOPE: 3.0°</span>
  </div>
  <div class="ils-cross"></div>
  <div style="display:flex;justify-content:space-between;">
    <span id="ils-dist">DIST: 8.5 KM</span>
    <span id="ils-callout">LOCALIZER LOCKED</span>
  </div>
</div>

<div id="cinematic-banner">
  <div id="cine-stage" class="cine-stage">STAGE 01</div>
  <div id="cine-title" class="cine-title">CATAPULT LAUNCH</div>
</div>

<div id="subtitle-box">COMMS // READY FOR SYSTEM INITIALIZATION</div>

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
const pipBox = document.getElementById('pip-box');
let pipOpen = true;

pipBox.addEventListener('click', (e) => {
    e.stopPropagation();
    pipOpen = !pipOpen;
    pipBox.style.height = pipOpen ? '190px' : '26px';
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
// 1. レンダラー＆ポストプロセス＆引き構図カメラ
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

const cameraMain = new THREE.PerspectiveCamera(55, W / H, 0.5, 980000);
const cameraPip = new THREE.PerspectiveCamera(36, 16 / 9, 0.5, 980000);

let baseCamPos = new THREE.Vector3(-35.0, 16.0, -95.0);
let baseTarget = new THREE.Vector3(0.0, 1.5, -4.0);

if (cfg.cam_preset.includes("エクストラ")) {
    baseCamPos.set(-52.0, 24.0, -135.0);
} else if (cfg.cam_preset.includes("チェイス")) {
    baseCamPos.set(-26.0, 11.0, -75.0);
}
cameraMain.position.copy(baseCamPos);
cameraMain.lookAt(baseTarget);

const controls = new THREE.OrbitControls(cameraMain, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.enabled = false;

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
scene.environment = pmremGenerator.fromEquirectangular(makeSkyEnvTexture()).texture;

const spaceFieldGroup = new THREE.Group();
scene.add(spaceFieldGroup);

function createStarField(count, radiusMin, radiusMax, size, baseColor) {
    const geo = new THREE.BufferGeometry();
    const pos = new Float32Array(count * 3);
    const col = new Float32Array(count * 3);
    const c = new THREE.Color(baseColor);
    for (let i = 0; i < count; i++) {
        const u = Math.random(), v = Math.random();
        const theta = u * 2.0 * Math.PI;
        const phi = Math.acos(2.0 * v - 1.0);
        const r = radiusMin + Math.random() * (radiusMax - radiusMin);
        pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
        pos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
        pos[i * 3 + 2] = r * Math.cos(phi);
        const variation = 0.7 + Math.random() * 0.6;
        col[i * 3] = c.r * variation; col[i * 3 + 1] = c.g * variation; col[i * 3 + 2] = c.b * variation;
    }
    geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
    return new THREE.Points(geo, new THREE.PointsMaterial({ size: size, vertexColors: true, transparent: true, opacity: 0.9, sizeAttenuation: false }));
}
spaceFieldGroup.add(createStarField(4000, 250000, 600000, 1.8, 0xdbeafe));
spaceFieldGroup.add(createStarField(2500, 150000, 450000, 2.5, 0x38bdf8));
spaceFieldGroup.add(createStarField(3000, 100000, 300000, 1.4, 0xf472b6));

const sunLight = new THREE.DirectionalLight(cfg.env.sun_color, cfg.env.sun_int);
sunLight.position.set(cfg.env.sun_pos[0] * 0.15, cfg.env.sun_pos[1] * 0.15 + 40.0, cfg.env.sun_pos[2] * 0.15);
sunLight.castShadow = true;
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
        "uInvert": { value: 0.0 },
        "uTime": { value: 0.0 },
        "uGForce": { value: 0.0 }
    },
    vertexShader: `
        varying vec2 vUv;
        void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }
    `,
    fragmentShader: `
        uniform sampler2D tDiffuse;
        uniform float uDistort;
        uniform float uInvert;
        uniform float uTime;
        uniform float uGForce;
        varying vec2 vUv;
        void main() {
            vec2 center = vec2(0.5, 0.5);
            vec2 dir = vUv - center;
            float dist = length(dir);
            float ringDistort = sin(dist * 18.0 - uTime * 4.0) * exp(-dist * 3.5) * uDistort * 0.05;
            vec2 rUv = vUv + dir * (dist * uDistort * 0.09 + ringDistort);
            vec2 gUv = vUv;
            vec2 bUv = vUv - dir * (dist * uDistort * 0.09 + ringDistort);
            float r = texture2D(tDiffuse, rUv).r;
            float g = texture2D(tDiffuse, gUv).g;
            float b = texture2D(tDiffuse, bUv).b;
            vec3 col = vec3(r, g, b);
            if (uInvert > 0.01) {
                col = mix(col, vec3(1.0) - col, uInvert);
            }
            float vig = smoothstep(0.85, 0.25, dist);
            col *= vig;
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

function updateCameraAspect() {
    W = window.innerWidth; H = window.innerHeight;
    renderer.setSize(W, H);
    composerMain.setSize(W, H);
    cameraMain.aspect = W / H;
    cameraMain.fov = (W / H < 1.0) ? 68.0 : 55.0;
    cameraMain.updateProjectionMatrix();
    resizeRadarCanvas();
}
window.addEventListener('resize', updateCameraAspect);
updateCameraAspect();

// =========================================================================
// 2. 音声合成＆ILSコールアウト＆Web Audio
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

const subtitleEl = document.getElementById('subtitle-box');
const cineBannerEl = document.getElementById('cinematic-banner');
const cineStageEl = document.getElementById('cine-stage');
const cineTitleEl = document.getElementById('cine-title');
const ilsHudEl = document.getElementById('ils-hud');

function showCinematicBanner(stage, title) {
    cineStageEl.innerText = stage;
    cineTitleEl.innerText = title;
    cineBannerEl.style.opacity = '1.0';
    setTimeout(() => { cineBannerEl.style.opacity = '0.0'; }, 3200);
}

function speakCallout(text) {
    if (subtitleEl) {
        subtitleEl.innerText = `COMMS // "${text}"`;
        subtitleEl.style.opacity = '1.0';
    }
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        setTimeout(() => {
            const u = new SpeechSynthesisUtterance(text);
            u.lang = 'en-US';
            if (availableVoices.length === 0) availableVoices = window.speechSynthesis.getVoices();
            const enVoice = availableVoices.find(v => (v.lang === 'en-US' || v.lang === 'en_US') && (v.name.includes('Google') || v.name.includes('Natural') || v.name.includes('Zira') || v.name.includes('David')))
                         || availableVoices.find(v => v.lang.startsWith('en'));
            if (enVoice) u.voice = enVoice;
            u.rate = 1.0;
            u.pitch = 1.0;
            u.volume = 0.9;
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
// 3. 超高精細リベット・パネルライン・汚しPBRテクスチャ
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

            // リベット穴
            ctx.fillStyle = '#0f172a';
            ctx.fillRect(x + 6, y + 6, 2, 2);
            ctx.fillRect(x + 54, y + 6, 2, 2);
            ctx.fillRect(x + 6, y + 22, 2, 2);
            ctx.fillRect(x + 54, y + 22, 2, 2);

            // パネルスス汚し
            if (Math.random() > 0.6) {
                ctx.fillStyle = 'rgba(15,23,42,0.35)';
                ctx.fillRect(x + 2, y + 24, 60, 6);
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
const matCanopy = new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, metalness: 0.95, roughness: 0.03, transparent: true, opacity: 0.45 });
const matRadiator = new THREE.MeshStandardMaterial({ color: 0x1e293b, metalness: 0.82, roughness: 0.28 });
const matCryoPipe = new THREE.MeshStandardMaterial({ color: 0xdbeafe, roughness: 0.65, metalness: 0.25 });

// =========================================================================
// 4. 超精密宇宙船（24枚アイリスノズル・エアブレーキ・シュート・ギア・骨格）
// =========================================================================
const radAngle = THREE.MathUtils.degToRad(cfg.env.angle_deg);
const shipRoot = new THREE.Group();
shipRoot.rotation.x = -radAngle;
scene.add(shipRoot);

const shipPitchGroup = new THREE.Group();
shipRoot.add(shipPitchGroup);

const shipMeshGroup = new THREE.Group();
shipPitchGroup.add(shipMeshGroup);

// 内部骨格・極低温配管・He3タンク
const innerSkeletonGroup = new THREE.Group();
shipMeshGroup.add(innerSkeletonGroup);
innerSkeletonGroup.add(new THREE.Mesh(new THREE.BoxGeometry(2.2, 1.2, 28.0), matTitaniumFrame));

for (let s of [-1, 1]) {
    const pipePts = [new THREE.Vector3(s * 1.5, -0.4, 12.0), new THREE.Vector3(s * 2.2, -0.2, 4.0), new THREE.Vector3(s * 2.8, -0.3, -4.0), new THREE.Vector3(s * 0.9, 0.0, -15.0)];
    innerSkeletonGroup.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pipePts), 32, 0.16, 10, false), matCryoPipe));
}

// 艦種別造形分岐
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

// 可変ベイ扉＆油圧シリンダー
const bayDoors = [];
const hydraulicPistons = [];
for (let s of [-1, 1]) {
    const doorPivot = new THREE.Group();
    doorPivot.position.set(s * 2.4, 1.15, -2.5);
    shipMeshGroup.add(doorPivot);
    const dPanel = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.25, 12.0), matHull);
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
    hydraulicPistons.push({ cyl, rod, side: s });
}

// 主翼＆可動動翼（フラップ＆エルロン）
const halfSpan = cfg.wings_span * 0.5;
const wingPivots = [];
const elevonMeshes = [];
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

    // 可動エレボン
    const elMesh = new THREE.Mesh(new THREE.BoxGeometry(halfSpan * 0.45, 0.18, 1.6), matDarkAlloy);
    elMesh.position.set(s * (halfSpan * 0.55), 0, -8.6);
    pivot.add(elMesh);
    elevonMeshes.push({ mesh: elMesh, side: s });
}

// 背面スピードエアブレーキパネル
const speedbrakePivot = new THREE.Group();
speedbrakePivot.position.set(0, 1.35, -5.0);
shipMeshGroup.add(speedbrakePivot);
const speedbrakeMesh = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.18, 4.2), matTitaniumFrame);
speedbrakeMesh.position.set(0, 0, -2.1);
speedbrakePivot.add(speedbrakeMesh);

// 補助スクラムブースター×2
const boosterAssemblies = [];
for (let s of [-1, 1]) {
    const bGrp = new THREE.Group();
    bGrp.position.set(s * 4.6, -0.6, -2.0);
    const bPod = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.85, 14.0, 16), matDarkAlloy);
    bPod.rotation.x = Math.PI / 2;
    bGrp.add(bPod);
    const bNose = new THREE.Mesh(new THREE.ConeGeometry(0.7, 3.2, 16), matHull);
    bNose.rotation.x = Math.PI / 2;
    bNose.position.z = 8.6;
    bGrp.add(bNose);
    shipMeshGroup.add(bGrp);
    boosterAssemblies.push({ group: bGrp, side: s, baseX: s * 4.6 });
}

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

// 接地白煙エフェクト
const smokePuffGroup = new THREE.Group();
const smokePuffs = [];
const smokeGeo = new THREE.SphereGeometry(1.2, 8, 8);
const smokeMat = new THREE.MeshBasicMaterial({ color: 0xe2e8f0, transparent: true, opacity: 0.0 });
for (let sm = 0; sm < 8; sm++) {
    const p = new THREE.Mesh(smokeGeo, smokeMat);
    smokePuffGroup.add(p);
    smokePuffs.push(p);
}
shipMeshGroup.add(smokePuffGroup);

// 十字型ドラッグシュート（減速パラシュート）
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

for (let cLine = 0; cLine < 4; cLine++) {
    const ang = (cLine / 4) * Math.PI * 2;
    const lineGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0,0,0), new THREE.Vector3(Math.cos(ang)*4.5, Math.sin(ang)*4.5, -15.0)]);
    chuteGroup.add(new THREE.Line(lineGeo, new THREE.LineBasicMaterial({ color: 0xffffff })));
}

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

// アルクビエレ・ワープリング
const warpRingAssembly = new THREE.Group();
warpRingAssembly.position.set(0, -0.8, -2.5);
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

// 六角形シールド
const shieldMat = new THREE.ShaderMaterial({
    vertexShader: `varying vec3 vNormal; varying vec3 vWorldPos; void main() { vNormal = normalize(normalMatrix * normal); vec4 wp = modelMatrix * vec4(position, 1.0); vWorldPos = wp.xyz; gl_Position = projectionMatrix * viewMatrix * wp; }`,
    fragmentShader: `varying vec3 vNormal; varying vec3 vWorldPos; uniform float uAlpha; uniform float uTime; void main() { float hex = abs(sin(vWorldPos.x * 0.8) * cos(vWorldPos.y * 0.8) * sin(vWorldPos.z * 0.8)); float rim = pow(1.0 - abs(dot(vNormal, vec3(0,0,1))), 3.0); gl_FragColor = vec4(0.22, 0.74, 0.98, (rim + smoothstep(0.2, 0.8, hex) * 0.6) * uAlpha); }`,
    uniforms: { uAlpha: { value: 0.0 }, uTime: { value: 0.0 } },
    transparent: true, side: THREE.DoubleSide, blending: THREE.AdditiveBlending, depthWrite: false
});
const hexShieldMesh = new THREE.Mesh(new THREE.SphereGeometry(18.0, 32, 32), shieldMat);
shipMeshGroup.add(hexShieldMesh);

// 推進炎
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

// =========================================================================
// 5. 3層パララックス・ワープトンネル＆ドップラースター＆スペースダスト
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

// 恒星ストリーク
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
const warpStars = new THREE.LineSegments(starGeo, new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.92, blending: THREE.AdditiveBlending }));
warpGroup.add(warpStars);

// 近景スペースダスト
const dustCount = 800;
const dustGeo = new THREE.BufferGeometry();
const dustPos = new Float32Array(dustCount * 6);
for (let i = 0; i < dustCount; i++) {
    const rx = (Math.random() - 0.5) * 55.0, ry = (Math.random() - 0.5) * 35.0, rz = (Math.random() - 0.5) * 260.0;
    dustPos[i * 6] = rx; dustPos[i * 6 + 1] = ry; dustPos[i * 6 + 2] = rz;
    dustPos[i * 6 + 3] = rx; dustPos[i * 6 + 4] = ry; dustPos[i * 6 + 5] = rz - 3.0;
}
dustGeo.setAttribute('position', new THREE.BufferAttribute(dustPos, 3));
scene.add(new THREE.LineSegments(dustGeo, new THREE.LineBasicMaterial({ color: 0x93c5fd, transparent: true, opacity: 0.85, blending: THREE.AdditiveBlending })));

// =========================================================================
// 6. 射場＆地球＆目標惑星・3.5km超長大滑走路・誘導灯システム
// =========================================================================
const catapultSlopeRoot = new THREE.Group();
catapultSlopeRoot.rotation.x = -radAngle;
scene.add(catapultSlopeRoot);
const railMover = new THREE.Group();
catapultSlopeRoot.add(railMover);
railMover.add(new THREE.Mesh(new THREE.BoxGeometry(14.5, 2.4, 3600), matDarkAlloy));

const groundEnvMover = new THREE.Group();
scene.add(groundEnvMover);
const seaMesh = new THREE.Mesh(new THREE.PlaneGeometry(160000, 160000), new THREE.MeshStandardMaterial({ color: 0x021124, roughness: 0.3 }));
seaMesh.rotation.x = -Math.PI / 2;
seaMesh.position.y = -45.0;
groundEnvMover.add(seaMesh);
const fujiMount = new THREE.Mesh(new THREE.ConeGeometry(12500, 3776, 64), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.85 }));
fujiMount.position.set(4500, 1800, 14500);
groundEnvMover.add(fujiMount);

const earthGroup = new THREE.Group();
scene.add(earthGroup);
earthGroup.add(new THREE.Mesh(new THREE.SphereGeometry(25000, 48, 48), new THREE.MeshStandardMaterial({ color: 0x1d4ed8, roughness: 0.6 })));

// 目標惑星＆3,500m舗装滑走路
const destWorld = new THREE.Group();
scene.add(destWorld);

const destPlanet = new THREE.Mesh(new THREE.SphereGeometry(3200, 64, 64), new THREE.MeshStandardMaterial({ color: new THREE.Color(cfg.dest_color), roughness: 0.7 }));
destPlanet.position.set(0, -3200, 0);
destWorld.add(destPlanet);

const cloudSea = new THREE.Mesh(new THREE.SphereGeometry(3240, 48, 48), new THREE.MeshStandardMaterial({ color: 0xffffff, transparent: true, opacity: 0.65 }));
cloudSea.position.copy(destPlanet.position);
destWorld.add(cloudSea);

// 3.5km滑走路本体
const runwayMesh = new THREE.Mesh(new THREE.BoxGeometry(60.0, 2.0, 3500.0), new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.85 }));
runwayMesh.position.set(0, -1.0, 0);
destWorld.add(runwayMesh);

// センターライン＆タッチダウンマーク
const centerLineMesh = new THREE.Mesh(new THREE.PlaneGeometry(2.0, 3400.0), new THREE.MeshBasicMaterial({ color: 0xffffff }));
centerLineMesh.rotation.x = -Math.PI / 2;
centerLineMesh.position.set(0, 0.05, 0);
destWorld.add(centerLineMesh);

// アプローチ進入誘導灯システム（1,500m手前から滑走路端まで）
const dummyLight = new THREE.Object3D();
const approachLightsInst = new THREE.InstancedMesh(new THREE.SphereGeometry(0.5, 8, 8), new THREE.MeshBasicMaterial({ color: 0x10b981 }), 120);
for (let al = 0; al < 60; al++) {
    const lz = -1750.0 - al * 25.0;
    dummyLight.position.set(-28.0, 0.5, lz); dummyLight.updateMatrix(); approachLightsInst.setMatrixAt(al * 2, dummyLight.matrix);
    dummyLight.position.set(28.0, 0.5, lz); dummyLight.updateMatrix(); approachLightsInst.setMatrixAt(al * 2 + 1, dummyLight.matrix);
}
destWorld.add(approachLightsInst);

destWorld.position.set(0, 0, 800000.0);
destWorld.scale.setScalar(0.0001);

// =========================================================================
// 7. 再生制御＆シークバー
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
// 8. 軌道レーダー描画
// =========================================================================
function drawRadar(prog, vc, mach, altKm) {
    const rw = radarCanvas.width, rh = radarCanvas.height;
    rCtx.clearRect(0, 0, rw, rh);
    const isSolar = (prog >= 0.16 && prog < 0.82);
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
        const curX = leftX + ((prog - 0.16) / 0.66) * (rightX - leftX);
        rCtx.fillStyle = '#10b981'; rCtx.beginPath(); rCtx.arc(curX, midY, 7, 0, Math.PI * 2); rCtx.fill();
    }
}

// =========================================================================
// 9. 60fps アニメーションループ（3層高速ワープ流動＆リアル滑走路着陸）
// =========================================================================
const cameraIdealPos = new THREE.Vector3();
const cameraLookTarget = new THREE.Vector3();
const shipWorldPos = new THREE.Vector3();
let announcedAltitudes = {};

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
    const boosterP = L('booster_purge'), gearD = L('gear_deploy'), speedbrake = L('speedbrake');
    const chuteD = L('chute_deploy'), tdSmoke = L('touchdown_smoke'), shieldHit = L('shield_hit');

    // フェーズ移行＆大型テロップ
    if (f0.phase !== lastAnnouncedPhase) {
        lastAnnouncedPhase = f0.phase;
        if (f0.phase === "CATAPULT_RAIL_ACCEL") {
            showCinematicBanner("STAGE 01", "SUPERSONIC CATAPULT LAUNCH");
            speakCallout("Magnetic catapult engaged. Maximum acceleration.");
        } else if (f0.phase === "STRATOSPHERE_CLIMB") {
            showCinematicBanner("STAGE 02", "ATMOSPHERIC ESCAPE & ASCENT");
            speakCallout("Approaching Max Q. Clearing upper stratosphere.");
        } else if (f0.phase === "WARP_FIELD_COMPRESSION") {
            showCinematicBanner("STAGE 03", "ALCUBIERRE WARP FIELD CHARGE");
            speakCallout("Spooling warp coils. Spacetime compression active.");
        } else if (f0.phase === "ALCUBIERRE_HYPER_WARP") {
            showCinematicBanner("STAGE 04", "SUPERLUMINAL HYPER-DRIVE");
            speakCallout("Hyper warp engaged. Approaching light speed.");
        } else if (f0.phase === "DEBRIS_AERO_BRAKING") {
            showCinematicBanner("STAGE 05", "FORWARD AERO-BRAKE & SHIELD DEFENSE");
            speakCallout("Warp disengaged. Forward airbrakes and shields online.");
        } else if (f0.phase === "ATMOSPHERIC_ENTRY_GLIDESLOPE") {
            showCinematicBanner("STAGE 06", "ATMOSPHERIC ENTRY & CLOUD PIERCE");
            speakCallout("Entering destination atmosphere. Intercepting ILS glideslope.");
        } else if (f0.phase === "FINAL_APPROACH_FLARE") {
            showCinematicBanner("STAGE 07", "FINAL RUNWAY 04L FLARE");
            speakCallout("Minimums. Runway in sight. Flare.");
        } else if (f0.phase === "TOUCHDOWN_ROLLOUT_STOP") {
            showCinematicBanner("STAGE 08", "TOUCHDOWN & DRAG CHUTE ARREST");
            speakCallout("Touchdown! Drag chute deployed. Reversing thrust.");
        }
    }

    // ILS高度カウントダウン音声読み上げ
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

    // 機体姿勢（機首前向き統一、ピッチ・ロールのみでダイナミック旋回）
    const isRailRunning = (altKm < 1.2 && f0.phase === "CATAPULT_RAIL_ACCEL");
    if (isRailRunning) {
        shipPitchGroup.rotation.set(0, 0, 0);
        shipMeshGroup.position.set(0, 0, 0);
    } else {
        shipPitchGroup.rotation.set(-THREE.MathUtils.degToRad(pitchDeg) + radAngle, THREE.MathUtils.degToRad(yawDeg), THREE.MathUtils.degToRad(rollDeg));
        shipMeshGroup.position.set(Math.sin(now * 0.003) * 0.35, Math.cos(now * 0.004) * 0.25, Math.sin(now * 0.002) * 0.5);
    }

    shipMeshGroup.getWorldPosition(shipWorldPos);

    // バネ追従カメラ
    if (!controls.enabled) {
        if (activeCamMode === 0 || activeCamMode === 1) {
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

    // カタパルト＆射場移動
    railMover.position.set(0, 0, -distM);
    groundEnvMover.position.set(0, -distM * Math.sin(radAngle), -distM * Math.cos(radAngle));

    // ブースター分離
    if (boosterP > 0.01) {
        boosterAssemblies.forEach(ba => {
            ba.group.position.x = ba.baseX + ba.side * Math.pow(boosterP, 2.0) * 22.0;
            ba.group.position.y = -0.6 - Math.pow(boosterP, 2.0) * 12.0;
            ba.group.position.z = -2.0 - Math.pow(boosterP, 1.8) * 35.0;
        });
    }

    // 可動動翼＆スピードブレーキ
    speedbrakePivot.rotation.x = speedbrake * 0.75;
    elevonMeshes.forEach(em => { em.mesh.rotation.x = Math.sin(now * 0.005) * 0.15 + THREE.MathUtils.degToRad(-pitchDeg * 0.3); });
    irisPaddles.forEach((ip, idx) => { ip.rotation.x = -0.35 + L('nozzle_open') * 0.48; });

    // ランディングギア
    landingGears.forEach(lg => { lg.scale.setScalar(Math.max(0.001, gearD)); });

    // タイヤ接地白煙
    if (tdSmoke > 0.05) {
        smokeMat.opacity = tdSmoke * 0.85;
        smokePuffs.forEach((p, idx) => {
            p.position.set((Math.random() - 0.5) * 3.5, -2.6, -6.0 - Math.random() * 8.0);
            p.scale.setScalar(1.0 + Math.random() * 2.0);
        });
    } else {
        smokeMat.opacity = 0.0;
    }

    // 十字型ドラッグシュート開傘
    if (chuteD > 0.01) {
        chuteGroup.scale.setScalar(chuteD);
        chuteCanopy.rotation.z += 0.02;
    } else {
        chuteGroup.scale.setScalar(0.001);
    }

    // 3層パララックス・ワープ高速流動
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

    // 近景スペースダスト流動
    const speedRatio = THREE.MathUtils.clamp((mach / 30.0) + (vc * 8.0), 0.1, 14.0);
    const dArr = dustGeo.attributes.position.array;
    for (let i = 0; i < dustCount; i++) {
        let z = dArr[i * 6 + 2] - speedRatio * 4.0;
        if (z < -130.0) z = 130.0;
        dArr[i * 6 + 2] = z; dArr[i * 6 + 5] = z - (3.0 + speedRatio * 5.0);
    }
    dustGeo.attributes.position.needsUpdate = true;

    // ワープ時空歪曲＆バレットタイム光彩反転
    let duckingFactor = 1.0;
    if (f0.phase === "WARP_FIELD_COMPRESSION" && prog > 0.14) {
        warpPass.uniforms.uInvert.value = 1.0;
        duckingFactor = 0.001;
    } else {
        warpPass.uniforms.uInvert.value = 0.0;
    }
    warpPass.uniforms.uDistort.value = wBoom * 2.8 + wAct * 0.35;
    warpPass.uniforms.uTime.value = now * 0.001;

    // 目標惑星・滑走路への接近
    if (prog > 0.35) {
        const approachProg = THREE.MathUtils.clamp((prog - 0.35) / 0.65, 0.0, 1.0);
        destWorld.position.set(0, THREE.MathUtils.lerp(-1800, 0, Math.pow(approachProg, 2.0)), THREE.MathUtils.lerp(650000.0, 0.0, Math.pow(approachProg, 2.5)));
        destWorld.scale.setScalar(THREE.MathUtils.lerp(0.002, 1.0, Math.pow(approachProg, 2.0)));
    } else {
        destWorld.position.set(0, 0, 800000.0);
        destWorld.scale.setScalar(0.0001);
    }

    // 音声
    if (actx) {
        rocketGain.gain.setTargetAtTime(engPwr * 0.35 * duckingFactor, actx.currentTime, 0.05);
        rcsGain.gain.setTargetAtTime(rcsBurst * 0.15 * duckingFactor, actx.currentTime, 0.05);
    }

    cameraPip.position.set(shipWorldPos.x - 22.0, shipWorldPos.y + 12.0, shipWorldPos.z - 35.0);
    cameraPip.lookAt(shipWorldPos);

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
        renderer.setScissorTest(false);
        renderer.setViewport(0, 0, W, H);
    }

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

    if (f0.phase.includes("SECURED") || f0.phase.includes("STOP")) {
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
