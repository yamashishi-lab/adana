import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import os
import requests
import hashlib
import random
import textwrap
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

# ==============================================================================
# 失敗内容（コンテキスト）解析 ＆ 超短縮・直感的二つ名エンジン
# ==============================================================================
CATEGORY_NICKNAMES = {
    "work_it": {
        "keywords": ["画面", "共有", "会議", "社内", "上司", "プレゼン", "メール", "誤送信", "誤爆", "Slack", "Teams", "チャット", "全社"],
        "prefixes": ["秒速の", "全画面の", "無警戒な", "痛恨の", "公開処刑の", "ノーガード", "突貫の"],
        "cores": ["誤爆王", "露出狂", "戦犯", "大惨事", "配信者", "自爆神", "テロリスト"]
    },
    "love": {
        "keywords": ["元カノ", "元彼", "告白", "LINE", "既読", "振られ", "浮気", "デート", "深夜", "好き", "未練", "復縁"],
        "prefixes": ["深夜の", "未練たらたら", "泥沼の", "一方通行の", "空回り", "自爆特攻の", "ゾンビ級"],
        "cores": ["未練鬼", "怪文書師", "自爆魔", "ピエロ", "撃沈王", "亡霊", "ストーカー"]
    },
    "alcohol": {
        "keywords": ["酒", "酔っ払", "飲み会", "泥酔", "記憶", "吐い", "終電", "二日酔い", "居酒屋", "テキーラ", "ビール"],
        "prefixes": ["泥酔の", "記憶喪失の", "ノーブレーキ", "暴走の", "制御不能の", "千鳥足の", "液体窒素級"],
        "cores": ["酒乱神", "撃沈艦", "粗相王", "迷惑鬼", "爆死職人", "大失態", "廃人"]
    },
    "money": {
        "keywords": ["金", "借金", "課金", "クレカ", "散財", "パチンコ", "競馬", "ギャンブル", "投資", "残高", "衝動買い"],
        "prefixes": ["無計画な", "秒速全損の", "自転車操業の", "ノーガード", "破滅型の", "底なしの"],
        "cores": ["散財神", "全ロス王", "負債魔人", "浪費鬼", "破綻者", "大赤字", "養分"]
    },
    "time_laziness": {
        "keywords": ["遅刻", "寝坊", "ドタキャン", "サボり", "すっぽかし", "二度寝", "バックレ"],
        "prefixes": ["時空歪める", "全自動の", "息を吐くように", "堂々たる", "常習犯の", "秒針無視の"],
        "cores": ["遅刻魔", "ドタキャン鬼", "脱走兵", "寝坊神", "サボり魔", "蒸発王"]
    },
    "blunder_mouth": {
        "keywords": ["失言", "口が滑", "暴露", "秘密", "悪口", "ポロリ", "自慢"],
        "prefixes": ["口先だけの", "余計な一言の", "ノーフィルター", "墓穴掘りの", "地雷踏み抜く"],
        "cores": ["失言王", "墓穴職人", "燃料係", "地雷神", "毒舌ピエロ", "スピーカー"]
    }
}

# 該当ジャンルがない場合の汎用ショート二つ名
GENERIC_PREFIXES = ["秒速の", "天然の", "無自覚な", "不可逆の", "世紀末の", "歩く", "自業自得の", "哀愁の", "問答無用の", "完全敗北の"]
GENERIC_CORES = ["地雷原", "自爆王", "大惨事", "黒歴史神", "戦犯", "ピエロ", "墓穴職人", "反面教師", "やらかし魔", "破滅フラグ"]

# ==============================================================================
# ブラックジョーク・皮肉 1,000通り生成エンジン（10 × 10 × 10）
# ==============================================================================
REASON_OPENINGS = [
    "貴殿がやらかした上記の大失態は、人類の愚かさの極致を鮮やかに体現しており、",
    "常人には到底真似できない絶妙なタイミングで自爆を遂げたその蛮勇は、まさに天災であり、",
    "冷静な思考を完全に放棄し、本能の赴くままに引き起こされた芸術的惨劇は、",
    "何一つ言い訳の余地が残されていない純度100％の自滅劇であり、",
    "世間が凍りつき、味方すら全員が静かに距離を置いたあの歴史的失態は、",
    "理性より先にちっぽけなプライドが木っ端微塵に粉砕されたあの刹那は、",
    "もし恥ずかしさで人間が核分裂を起こすなら、地球を3回消滅させていた規模であり、",
    "知能と危機管理能力の完全な欠如を、これ以上ない明快さで証明したその功績は、",
    "目撃した全員が『見なかったことにしてやろう』と憐れみの目を向けたあの惨状は、",
    "後悔と羞恥心で深夜にベッドの上で奇声を上げのたうち回るに相応しいあの凶行は、"
]

REASON_BODIES = [
    "関わったすべての人間に深い溜め息と、一生酒の肴にできる特大の失笑を提供しました。",
    "どれほど高い授業料を払っても決して取り返せない信頼と尊厳を、一瞬で消滅させました。",
    "歴史の教科書に『反面教師の最高傑作』としてフルネームで掲載すべきレベルに達しています。",
    "周囲を震撼させ、その場の空気を絶対零度まで急冷却する驚異的な破壊力を誇りました。",
    "『記憶を消す装置』が実用化された暁には、最初の被験者として真っ先に推薦されるべき偉業です。",
    "救いようのない哀愁と、誰の共感も得られない孤立無援の地獄を生み出しました。",
    "貴殿の人生のハイライトが『これ』で確定してしまったという残酷な現実を突きつけています。",
    "神ですら匙を投げてその場から立ち去るレベルの、非の打ち所がないパーフェクトな自爆でした。",
    "どれだけ美談に仕立て上げようとしても、下水のような悪臭を放つ恥辱のモニュメントです。",
    "関わった友人知人の連絡先から、貴殿の名前が静かに削除される決定打となりました。"
]

REASON_CLOSINGS = [
    "記憶から消したいと願う浅はかな祈りを即座に却下し、ここに終身二つ名として永遠に刻印します。",
    "その栄誉ある恥辱を讃え、墓場まで背負うべき呪いとして当院公式の永久ブラックリストに登録します。",
    "二度と元の平穏な日常には戻れない証として、この不名誉極まりない称号を謹んで贈呈いたします。",
    "貴殿がこの先どれほど徳を積もうとも帳消しにはならない汚点として、厳正に認定証を交付します。",
    "来世まで語り継がれるべき人類の汚点として、当院公認の烙印をその魂に深く刻み込みます。",
    "せめてもの慈悲として、この認定証を見るたびに己の愚かさを猛省することを義務付けます。",
    "死ぬ間際の走馬灯で真っ先に高画質再生されるよう、公式アーカイブに永久保存いたします。",
    "この称号が貴殿の余生に相応しい重荷となり続けることを、審査員一同心より確信しております。",
    "もはや失うものなど何一つない無敵のピエロとして、堂々と胸を張って泥道を歩んでください。",
    "この恥辱を忘れかけた頃に再び悪夢として蘇るよう、呪詛を込めてここに公認認定証を発行します。"
]

# 過失深刻度ランク（SSSは0.01%の天文学的確率）
RANKS_WEIGHTED = [
    ("【級外】微小な赤恥 (Rank D)", 45.0),
    ("【軽過失】日常的失態 (Rank C)", 30.0),
    ("【中過失】赤面トラウマ (Rank B)", 16.0),
    ("【重過失】人間関係亀裂 (Rank A)", 7.5),
    ("【特級過失】懲戒免職・絶縁級 (Rank S)", 1.4),
    ("【極刑過失】人生再起動推奨 (Rank SS)", 0.09),
    ("【世界遺産級・破滅】永久封印の呪物 (Rank SSS)", 0.01)
]

def generate_nickname_data(name, failure):
    seed_str = f"{name.strip()}_{failure.strip()}"
    hash_obj = hashlib.sha256(seed_str.encode("utf-8"))
    hex_digest = hash_obj.hexdigest()
    rng = random.Random(int(hex_digest[:8], 16))

    # 失敗内容のキーワードマッチング
    matched_cat = None
    for cat_id, data in CATEGORY_NICKNAMES.items():
        if any(k in failure for k in data["keywords"]):
            matched_cat = data
            break

    if matched_cat:
        prefix = rng.choice(matched_cat["prefixes"])
        core = rng.choice(matched_cat["cores"])
    else:
        prefix = rng.choice(GENERIC_PREFIXES)
        core = rng.choice(GENERIC_CORES)

    # 短くシンプルに（例：「秒速の誤爆王」）
    nickname = f"“{prefix}{core}”"

    reason = f"{rng.choice(REASON_OPENINGS)}{rng.choice(REASON_BODIES)}{rng.choice(REASON_CLOSINGS)}"

    rank_choices, weights = zip(*RANKS_WEIGHTED)
    rank = rng.choices(rank_choices, weights=weights, k=1)[0]

    serial_no = f"REG-{hex_digest[:4].upper()}-{hex_digest[4:8].upper()}-{hex_digest[8:12].upper()}"
    return nickname, rank, reason, serial_no

# --- 認定証画像レンダリング（賞状・金彩フレーム・本格印章） ---
def create_certificate_image(name, failure, nickname, rank, reason, serial_no, app_url="https://regret-court.streamlit.app"):
    width, height = 1080, 1440
    img = Image.new("RGB", (width, height), color="#0D0D12")
    draw = ImageDraw.Draw(img)

    def get_font(size):
        if FONT_PATH and os.path.exists(FONT_PATH):
            return ImageFont.truetype(FONT_PATH, size)
        return ImageFont.load_default()

    # 1. 賞状・金彩多重フレーム（Gold Leaf Certificate Style）
    draw.rectangle([(25, 25), (width - 25, height - 25)], outline="#D4AF37", width=4)
    draw.rectangle([(35, 35), (width - 35, height - 35)], outline="#5A4A1C", width=1)
    draw.rectangle([(42, 42), (width - 42, height - 42)], outline="#E8C864", width=2)
    draw.rectangle([(50, 50), (width - 50, height - 50)], outline="#3A3014", width=1)

    # 伝統的な賞状風コーナーオーナメント
    cs = 45
    corners = [
        (50, 50, 1, 1),
        (width - 50, 50, -1, 1),
        (50, height - 50, 1, -1),
        (width - 50, height - 50, -1, -1)
    ]
    for cx, cy, dx, dy in corners:
        # コーナー幾何学ライン
        draw.line([(cx, cy), (cx + dx * cs, cy)], fill="#E8C864", width=3)
        draw.line([(cx, cy), (cx, cy + dy * cs)], fill="#E8C864", width=3)
        draw.line([(cx + dx * 10, cy + dy * 10), (cx + dx * cs, cy + dy * 10)], fill="#AA8828", width=1)
        draw.line([(cx + dx * 10, cy + dy * 10), (cx + dx * 10, cy + dy * cs)], fill="#AA8828", width=1)
        draw.rectangle([(cx + dx * 14 - 3, cy + dy * 14 - 3), (cx + dx * 14 + 3, cy + dy * 14 + 3)], fill="#D4AF37")

    # 2. 中央透かし（クラシカル・ウォーターマーク）
    draw.text((width // 2, height // 2 - 20), "CERTIFICATE OF DISHONOR", fill="#14141E", font=get_font(56), anchor="mm")

    # 3. ヘッダー（格調高い賞状タイトル）
    draw.text((width // 2, 105), "認　定　証", fill="#F5D77F", font=get_font(58), anchor="mm")
    draw.text((width // 2, 155), "CERTIFICATE OF OFFICIAL REGRET ALIAS", fill="#9A8C6A", font=get_font(20), anchor="mm")
    
    # 飾り仕切り線
    draw.line([(220, 185), (width - 220, 185)], fill="#D4AF37", width=2)
    draw.polygon([(width // 2 - 6, 185 - 5), (width // 2 + 6, 185 - 5), (width // 2, 185 + 5)], fill="#D4AF37")

    # 4. 被認定者（受賞者表記）
    name_str = f"{name}　殿"
    name_size = 46
    name_font = get_font(name_size)
    while name_size > 24 and name_font.getlength(name_str) > (width - 220):
        name_size -= 2
        name_font = get_font(name_size)
    draw.text((120, 245), name_str, fill="#FFFFFF", font=name_font)

    # 5. 終身二つ名枠（短くインパクトのある黄金プレート）
    draw.rectangle([(100, 315), (width - 100, 475)], fill="#15141E", outline="#C43C3C", width=2)
    draw.rectangle([(106, 321), (width - 106, 469)], outline="#7A2222", width=1)
    draw.text((width // 2, 350), "―　授 与 さ れ し 終 身 二 つ 名　―", fill="#E55555", font=get_font(22), anchor="mm")

    nick_size = 56
    nick_font = get_font(nick_size)
    while nick_size > 26 and nick_font.getlength(nickname) > (width - 260):
        nick_size -= 2
        nick_font = get_font(nick_size)
    draw.text((width // 2, 415), nickname, fill="#FFDF00", font=nick_font, anchor="mm")

    # 6. 過失記録事由（本文冒頭）
    draw.text((110, 525), "【 認定対象事由（過失記録） 】", fill="#D4AF37", font=get_font(24))

    clean_failure = failure.replace("\n", " ").strip()
    wrapped_failure = textwrap.fill(clean_failure, width=28)
    failure_lines = wrapped_failure.split("\n")
    if len(failure_lines) > 3:
        failure_lines = failure_lines[:3]
        failure_lines[-1] = failure_lines[-1][:24] + "..."
    disp_failure = "\n".join(failure_lines)
    draw.text((115, 570), f"「{disp_failure}」", fill="#EAEAEA", font=get_font(26), spacing=10)

    # 7. 認定および授与の辞（賞状本文）
    draw.text((110, 710), "【 認定の辞 】", fill="#D4AF37", font=get_font(24))
    wrapped_reason = textwrap.fill(reason, width=31)
    draw.text((115, 755), wrapped_reason, fill="#B0B0C0", font=get_font(24), spacing=11)

    # 8. ランク表記
    if "SSS" in rank:
        rank_color = "#FF0055"
    elif "SS" in rank or "Rank S" in rank:
        rank_color = "#FF9900"
    else:
        rank_color = "#00E5AA"

    draw.text((110, 995), f"過失深刻度ランク ： {rank}", fill=rank_color, font=get_font(26))
    draw.text((110, 1045), f"認 定 機 関      ： 全国黒歴史認定院 審査第一局", fill="#888899", font=get_font(22))
    draw.text((110, 1085), f"公 式 発 行 日   ： {datetime.now().strftime('%Y年%m月%d日')}", fill="#888899", font=get_font(22))

    # 9. 本格公式角印（三重枠・朱肉滲み風・重厚デザイン）
    stamp_x, stamp_y = width - 290, 965
    stamp_size = 180

    # 印章の外枠（重厚な三重線）
    draw.rectangle([(stamp_x, stamp_y), (stamp_x + stamp_size, stamp_y + stamp_size)], fill="#1C0A0E", outline="#C92020", width=5)
    draw.rectangle([(stamp_x + 7, stamp_y + 7), (stamp_x + stamp_size - 7, stamp_y + stamp_size - 7)], outline="#8A1414", width=1)
    draw.rectangle([(stamp_x + 12, stamp_y + 12), (stamp_x + stamp_size - 12, stamp_y + stamp_size - 12)], outline="#C92020", width=2)

    # 四隅のコーナーリベット
    for rx, ry in [
        (stamp_x + 22, stamp_y + 22),
        (stamp_x + stamp_size - 22, stamp_y + 22),
        (stamp_x + 22, stamp_y + stamp_size - 22),
        (stamp_x + stamp_size - 22, stamp_y + stamp_size - 22)
    ]:
        draw.ellipse([(rx - 3, ry - 3), (rx + 3, ry + 3)], fill="#C92020")

    # 伝統的な篆書体風配置（右上:黒、右下:歴、左上:院、左下:印）
    # ※印章の伝統的配置ルールに準拠
    stamp_font = get_font(38)
    draw.text((stamp_x + 128, stamp_y + 54), "黒", fill="#E62E2E", font=stamp_font, anchor="mm")
    draw.text((stamp_x + 128, stamp_y + 128), "歴", fill="#E62E2E", font=stamp_font, anchor="mm")
    draw.text((stamp_x + 54, stamp_y + 54), "院", fill="#E62E2E", font=stamp_font, anchor="mm")
    draw.text((stamp_x + 54, stamp_y + 128), "印", fill="#E62E2E", font=stamp_font, anchor="mm")

    # 10. フッター
    draw.line([(80, height - 110), (width - 80, height - 110)], fill="#3B3528", width=1)
    draw.text((90, height - 75), f"REGISTRATION NO: {serial_no}", fill="#D4AF37", font=get_font(21))
    draw.text((width - 90, height - 75), f"ARCHIVE: {app_url}", fill="#777785", font=get_font(20), anchor="ra")

    return img

# --- Streamlit フロントエンド ---
st.title("🎖️ 公式・黒歴史二つ名認定院")
st.caption("消し去りたい過去の過失を、厳格な審査を経て一生背負う『公認二つ名』へと昇華します。")

with st.form("cert_form"):
    user_name = st.text_input("あなたの名前（またはハンドルネーム）", value="たけし")
    user_failure = st.text_area(
        "過去にやらかした最大の失敗・黒歴史", 
        placeholder="例: 全社員の前で行うプレゼンで画面共有したまま怪しい検索履歴を晒した\n例: 酔っ払って元カノ全員に深夜3時に「元気？」と一斉送信した"
    )
    submitted = st.form_submit_button("🔥 厳正なる審査を受け認定証を発行する", type="primary", use_container_width=True)

if submitted:
    if not user_failure.strip():
        st.error("やらかした失敗を入力してください。")
    else:
        nickname, rank, reason, serial_no = generate_nickname_data(user_name, user_failure)

        with st.spinner("過失内容を精査し、公認朱印を押印中..."):
            cert_img = create_certificate_image(user_name, user_failure, nickname, rank, reason, serial_no)

            buf = io.BytesIO()
            cert_img.save(buf, format="PNG", quality=95)
            byte_im = buf.getvalue()

        if "SSS" in rank:
            st.balloons()
            st.error("⚠️【警告】0.01%の天文学的確率で『世界遺産級・破滅 (Rank SSS)』を引き当ててしまいました。")
        else:
            st.success("✅ 厳正なる審査の結果、不名誉な終身二つ名が認定されました！")

        st.image(byte_im, caption="公式発行・金彩偽造防止暗号化済み認定証", use_container_width=True)

        st.download_button(
            label="📥 認定証画像を保存してSNSに晒す (PNG)",
            data=byte_im,
            file_name=f"certificate_{serial_no}.png",
            mime="image/png",
            use_container_width=True
        )

        share_text = f"【悲報】過去のやらかしにより、公式二つ名が決定しました。\n\n二つ名：{nickname}\n深刻度：{rank}\n証拠シリアル：{serial_no}\n\n#黒歴史二つ名認定院"
        x_url = f"https://twitter.com/intent/tweet?text={requests.utils.quote(share_text)}"
        st.markdown(f'''
        <a href="{x_url}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #000; color: #fff; text-align: center; padding: 12px; border-radius: 8px; font-weight: bold; border: 1px solid #333; margin-top: 10px;">
                𝕏 (Twitter) でこの不名誉を告発する
            </div>
        </a>
        ''', unsafe_allow_html=True)
