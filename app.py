import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
import requests
import hashlib
import random
from datetime import datetime

st.set_page_config(
    page_title="公式・黒歴史二つ名認定院",
    page_icon="🎖️",
    layout="centered"
)

# --- 日本語フォントの自動取得（Streamlit Cloud環境対策） ---
FONT_PATH = "NotoSansJP-Bold.ttf"
if not os.path.exists(FONT_PATH):
    font_url = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/Japanese/NotoSansCJKjp-Bold.otf"
    try:
        r = requests.get(font_url, timeout=15)
        with open(FONT_PATH, "wb") as f:
            f.write(r.content)
    except Exception:
        FONT_PATH = None

# --- あだ名生成の語彙バンク ---
PREFIX_LIST = [
    "歩く", "前代未聞の", "救いようのない", "時空を歪める", "全米が呆れた",
    "背水の陣を敷く", "不可逆の", "神に見放されし", "国宝級の", "暴走機関車"
]
CORE_LIST = [
    "やらかし王", "自爆テロリスト", "免罪体質", "言い訳マイスター", "黒歴史量産機",
    "爆死職人", "逆転サヨナラ負け男", "フラグ回収神", "ドタキャン怪獣", "負債の錬金術師"
]
RANK_LIST = ["国宝級やらかし (SSS)", "特級過失 (SS)", "懲戒免職級 (S)", "赤恥レベル (A)"]

def generate_nickname_data(name, failure):
    # 名前と失敗から固有シードを生成（同じ入力には同じ結果）
    seed_str = f"{name}_{failure}"
    hash_obj = hashlib.sha256(seed_str.encode("utf-8"))
    hex_digest = hash_obj.hexdigest()
    rng = random.Random(int(hex_digest[:8], 16))

    nickname = f"“{rng.choice(PREFIX_LIST)}{rng.choice(CORE_LIST)}”"
    rank = rng.choice(RANK_LIST)
    serial_no = f"REG-{hex_digest[:4].upper()}-{hex_digest[4:8].upper()}-{hex_digest[8:12].upper()}"
    return nickname, rank, serial_no

# --- 認定証画像レンダリング（Pillow） ---
def create_certificate_image(name, failure, nickname, rank, serial_no, app_url="https://regret-court.streamlit.app"):
    width, height = 1080, 1350  # SNS（X/Instagram）に最適な縦長高解像度
    img = Image.new("RGB", (width, height), color="#121218")
    draw = ImageDraw.Draw(img)

    # 1. 豪華な二重フレーム（金枠）
    draw.rectangle([(30, 30), (width - 30, height - 30)], outline="#D4AF37", width=6)
    draw.rectangle([(45, 45), (width - 45, height - 45)], outline="#554411", width=2)

    # フォントロード（フォント取得失敗時はデフォルト）
    def get_font(size):
        if FONT_PATH and os.path.exists(FONT_PATH):
            return ImageFont.truetype(FONT_PATH, size)
        return ImageFont.load_default()

    font_title = get_font(54)
    font_sub = get_font(26)
    font_name = get_font(44)
    font_nick = get_font(58)
    font_body = get_font(30)
    font_meta = get_font(22)

    # 2. パクリ防止：中央透かし文字（ウォーターマーク）
    draw.text((width // 2, height // 2 - 50), "OFFICIAL CERTIFICATE", fill="#1a1a26", font=get_font(72), anchor="mm")

    # 3. ヘッダー
    draw.text((width // 2, 120), "全 国 黒 歴 史 認 定 院", fill="#D4AF37", font=font_title, anchor="mm")
    draw.text((width // 2, 180), "OFFICIAL REGRET ALIAS REGISTRATION", fill="#888899", font=font_sub, anchor="mm")
    draw.line([(150, 220), (width - 150, 220)], fill="#D4AF37", width=2)

    # 4. 対象者・認定二つ名
    draw.text((width // 2, 300), f"被 認 定 者 ： {name} 殿", fill="#FFFFFF", font=font_name, anchor="mm")
    
    draw.rectangle([(100, 370), (width - 100, 520)], fill="#1E1E2A", outline="#FF3366", width=3)
    draw.text((width // 2, 410), "【 授 与 さ れ し 終 身 二 つ 名 】", fill="#FF3366", font=font_sub, anchor="mm")
    draw.text((width // 2, 465), nickname, fill="#FFDD44", font=font_nick, anchor="mm")

    # 5. 犯した過ち（本文）
    draw.text((120, 580), "【 認定根拠となる過去の過失 】", fill="#D4AF37", font=font_sub)
    
    # 複数行の折り返し表示
    failure_disp = f"「{failure}」"
    if len(failure_disp) > 26:
        failure_disp = failure_disp[:26] + "\n" + failure_disp[26:50] + ("..." if len(failure) > 48 else "")
    draw.text((120, 630), failure_disp, fill="#E0E0E0", font=font_body, spacing=12)

    reason_text = (
        "貴殿が過去に犯した上記の大失態は、人類の愚かさを極限まで体現し、\n"
        "周囲に深い戦慄と特大の失笑をもたらしました。\n"
        "その栄誉ある恥辱を永遠に称え、当院公認の二つ名としてここに刻みます。"
    )
    draw.text((120, 770), reason_text, fill="#AAAAAA", font=font_body, spacing=12)

    # 6. スペック・ランク
    draw.text((120, 960), f"過失深刻度ランク ： {rank}", fill="#00FFCC", font=font_body)
    draw.text((120, 1010), f"認 定 日 時      ： {datetime.now().strftime('%Y年%m月%d日')}", fill="#888899", font=font_meta)

    # 7. パクリ防止：公認朱印（デジタル角印）
    stamp_x, stamp_y = width - 260, height - 360
    draw.rectangle([(stamp_x, stamp_y), (stamp_x + 150, stamp_y + 150)], outline="#DD2222", width=5)
    draw.text((stamp_x + 75, stamp_y + 45), "公式\n認証", fill="#DD2222", font=get_font(42), anchor="mm", spacing=6)

    # 8. パクリ防止：改ざん防止シリアルナンバー＆帰還URL
    draw.line([(100, height - 140), (width - 100, height - 140)], fill="#444455", width=1)
    draw.text((120, height - 105), f"SERIAL NO: {serial_no} (VERIFIED)", fill="#FFCC00", font=font_meta)
    draw.text((width - 120, height - 105), f"ISSUED BY: {app_url}", fill="#888899", font=font_meta, anchor="ra")

    return img

# --- UIフロントエンド ---
st.title("🎖️ 公式・黒歴史二つ名認定院")
st.caption("消し去りたい過去のやらかしを、SNSで一生背負う『公認二つ名』に昇華します。")

with st.form("cert_form"):
    user_name = st.text_input("あなたの名前（またはハンドルネーム）", value="たけし")
    user_failure = st.text_area(
        "過去にやらかした最大の失敗・黒歴史", 
        placeholder="例: 全社員の前で行うプレゼンで画面共有したまま怪しい検索履歴を晒した\n例: 酔っ払って元カノ全員に深夜3時に「元気？」と一斉送信した"
    )
    submitted = st.form_submit_button("🔥 公式認定証を発行する", type="primary", use_container_width=True)

if submitted:
    if not user_failure.strip():
        st.error("やらかした失敗を入力してください。")
    else:
        nickname, rank, serial_no = generate_nickname_data(user_name, user_failure)
        
        with st.spinner("公認印を押印し、偽造防止コードを生成中..."):
            cert_img = create_certificate_image(user_name, user_failure, nickname, rank, serial_no)
            
            # 画像をバイトストリームに変換
            buf = io.BytesIO()
            cert_img.save(buf, format="PNG", quality=95)
            byte_im = buf.getvalue()

        st.success("✅ 厳正なる審査の結果、不名誉な二つ名が認定されました！")
        
        # 画面に画像表示
        st.image(byte_im, caption="公式発行・偽造防止暗号化済み認定証", use_container_width=True)

        # ダウンロードボタン
        st.download_button(
            label="📥 認定証画像を保存してSNSに晒す (PNG)",
            data=byte_im,
            file_name=f"certificate_{serial_no}.png",
            mime="image/png",
            use_container_width=True
        )

        # Xシェア用リンク
        share_text = f"【悲報】過去のやらかしにより、公式二つ名が決定しました。\n\n私の二つ名：{nickname}\n深刻度：{rank}\n証拠シリアル：{serial_no}\n\n#黒歴史二つ名認定院"
        x_url = f"https://twitter.com/intent/tweet?text={requests.utils.quote(share_text)}"
        st.markdown(f'''
        <a href="{x_url}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #000; color: #fff; text-align: center; padding: 12px; border-radius: 8px; font-weight: bold; border: 1px solid #333; margin-top: 10px;">
                𝕏 (Twitter) でこの不名誉を告発する
            </div>
        </a>
        ''', unsafe_allow_html=True)
