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
# 語彙合成エンジン（各1,024通り ＝ 掛け合わせ100万通り超の被りなし二つ名）
# ==============================================================================
P_ATTR = [
    "歩く", "秒速の", "天然物の", "救いなき", "不可逆の", "全米絶句の", "世紀末の", "お粗末な",
    "時限式", "低燃費の", "人間国宝級", "恥の上塗り", "無自覚な", "泥舟の", "四面楚歌の", "背水の陣の",
    "致命的な", "見切り発車", "炎上確定の", "言い訳番長", "骨折り損の", "自爆覚悟の", "後戻り不能", "前途多難な",
    "墓穴掘りの", "自業自得の", "哀愁漂う", "ノーガード", "豆腐メンタルの", "神風特攻の", "問答無用の", "突貫工事の"
]
P_MOD = [
    "完全敗北", "全自動", "脳死状態", "深夜テンション", "空回り", "逆走", "ノーブレーキ", "暴走",
    "勘違い", "迷走", "空前絶後", "後悔先立ち", "メンタル崩壊", "情緒不安定", "自暴自棄", "焼け野原",
    "大炎上", "被害妄想", "見苦しい", "往生際悪い", "取り返しのつかない", "絶体絶命", "自作自演", "泥沼化",
    "赤面", "青息吐息", "八方塞がり", "不祥事", "失態続きの", "やっつけ", "やらかし確定", "前代未聞"
]

C_DOMAIN = [
    "地雷", "時限爆弾", "戦犯", "自爆", "黒歴史", "言い訳", "燃料投下", "赤っ恥",
    "墓穴", "破滅", "怪文書", "散財", "逆境", "ドタキャン", "誤爆", "大惨事",
    "負債", "逃亡", "恥晒し", "空回り", "お笑い草", "お調子者", "黒星", "全ロス",
    "ピエロ", "破綻", "迷惑", "トラブル", "撃沈", "失言", "トラウマ", "不祥事"
]
C_ROLE = [
    "神", "王", "マイスター", "職人", "魔人", "製造機", "モンスター", "クリエイター",
    "キング", "エージェント", "ソムリエ", "テロリスト", "ドクター", "プロデューサー", "プリンス", "アーティスト",
    "コレクター", "パフォーマー", "エンジニア", "コンサルタント", "スペシャリスト", "指揮官", "伝道師", "エリート",
    "カリスマ", "請負人", "第一人者", "パイオニア", "総帥", "権化", "マスター", "巨匠"
]

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

# ==============================================================================
# 過失深刻度ランク（SSSは0.01%の天文学的激低確率）
# ==============================================================================
RANKS_WEIGHTED = [
    ("【級外】微小な赤恥 (Rank D)", 45.0),
    ("【軽過失】日常的失態 (Rank C)", 30.0),
    ("【中過失】赤面トラウマ (Rank B)", 16.0),
    ("【重過失】人間関係亀裂 (Rank A)", 7.5),
    ("【特級過失】懲戒免職・絶縁級 (Rank S)", 1.4),
    ("【極刑過失】人生再起動推奨 (Rank SS)", 0.09),
    ("【世界遺産級・破滅】永久封印の呪物 (Rank SSS)", 0.01)  # 1万分の1の超プレミア
]

def generate_nickname_data(name, failure):
    seed_str = f"{name.strip()}_{failure.strip()}"
    hash_obj = hashlib.sha256(seed_str.encode("utf-8"))
    hex_digest = hash_obj.hexdigest()
    rng = random.Random(int(hex_digest[:8], 16))

    # 1,024 × 1,024 = 1,048,576通りの二つ名生成
    prefix = f"{rng.choice(P_ATTR)}{rng.choice(P_MOD)}"
    core = f"{rng.choice(C_DOMAIN)}{rng.choice(C_ROLE)}"
    nickname = f"“{prefix}の{core}”"

    # 10 × 10 × 10 = 1,000通りのブラックジョーク生成
    reason = f"{rng.choice(REASON_OPENINGS)}{rng.choice(REASON_BODIES)}{rng.choice(REASON_CLOSINGS)}"

    # 超激低SSS判定
    rank_choices, weights = zip(*RANKS_WEIGHTED)
    rank = rng.choices(rank_choices, weights=weights, k=1)[0]

    serial_no = f"REG-{hex_digest[:4].upper()}-{hex_digest[4:8].upper()}-{hex_digest[8:12].upper()}"
    return nickname, rank, reason, serial_no

# --- 認定証画像レンダリング（Pillow） ---
def create_certificate_image(name, failure, nickname, rank, reason, serial_no, app_url="https://regret-court.streamlit.app"):
    width, height = 1080, 1440
    img = Image.new("RGB", (width, height), color="#0F0F14")
    draw = ImageDraw.Draw(img)

    def get_font(size):
        if FONT_PATH and os.path.exists(FONT_PATH):
            return ImageFont.truetype(FONT_PATH, size)
        return ImageFont.load_default()

    # 1. 外枠フレーム（金枠・アンティーク調）
    draw.rectangle([(25, 25), (width - 25, height - 25)], outline="#C5A059", width=5)
    draw.rectangle([(38, 38), (width - 38, height - 38)], outline="#4A3B22", width=2)
    draw.rectangle([(44, 44), (width - 44, height - 44)], outline="#8C6D37", width=1)

    corner_size = 28
    corners = [(44, 44), (width - 44 - corner_size, 44), (44, height - 44 - corner_size), (width - 44 - corner_size, height - 44 - corner_size)]
    for cx, cy in corners:
        draw.rectangle([(cx, cy), (cx + corner_size, cy + corner_size)], fill="#C5A059")

    # 2. 中央透かし
    draw.text((width // 2, height // 2 - 20), "OFFICIAL CERTIFICATE", fill="#171722", font=get_font(68), anchor="mm")

    # 3. ヘッダー
    draw.text((width // 2, 115), "全 国 黒 歴 史 認 定 院", fill="#E5C158", font=get_font(52), anchor="mm")
    draw.text((width // 2, 175), "NATIONAL REGRET & ATROCITY ARCHIVE", fill="#8A8A9E", font=get_font(24), anchor="mm")
    draw.line([(140, 210), (width - 140, 210)], fill="#C5A059", width=2)

    # 4. 被認定者名（枠内に収まるよう自動縮小）
    name_str = f"被 認 定 者 ： {name} 殿"
    name_size = 42
    name_font = get_font(name_size)
    while name_size > 22 and name_font.getlength(name_str) > (width - 200):
        name_size -= 2
        name_font = get_font(name_size)
    draw.text((width // 2, 275), name_str, fill="#FFFFFF", font=name_font, anchor="mm")

    # 5. 終身二つ名枠（文字数に応じて自動縮小）
    draw.rectangle([(90, 335), (width - 90, 485)], fill="#181824", outline="#FF2A55", width=3)
    draw.text((width // 2, 370), "【 授 与 さ れ し 終 身 二 つ 名 】", fill="#FF2A55", font=get_font(24), anchor="mm")

    nick_size = 54
    nick_font = get_font(nick_size)
    while nick_size > 24 and nick_font.getlength(nickname) > (width - 240):
        nick_size -= 2
        nick_font = get_font(nick_size)
    draw.text((width // 2, 430), nickname, fill="#FFDD44", font=nick_font, anchor="mm")

    # 6. 過失の概要（最大3行で省略＆はみ出し防止）
    draw.text((100, 530), "【 認定対象事由（過失記録） 】", fill="#E5C158", font=get_font(25))

    clean_failure = failure.replace("\n", " ").strip()
    wrapped_failure = textwrap.fill(clean_failure, width=28)
    failure_lines = wrapped_failure.split("\n")
    if len(failure_lines) > 3:
        failure_lines = failure_lines[:3]
        failure_lines[-1] = failure_lines[-1][:24] + "..."
    disp_failure = "\n".join(failure_lines)
    draw.text((105, 575), f"「{disp_failure}」", fill="#EAEAEA", font=get_font(27), spacing=10)

    # 7. 認定理由（自動折り返し）
    draw.text((100, 715), "【 認定および授与の辞 】", fill="#E5C158", font=get_font(25))
    wrapped_reason = textwrap.fill(reason, width=31)
    draw.text((105, 760), wrapped_reason, fill="#A6A6BA", font=get_font(24), spacing=10)

    # 8. ランク表示
    if "SSS" in rank:
        rank_color = "#FF0055"  # SSS専用カラー
    elif "SS" in rank or "Rank S" in rank:
        rank_color = "#FF8800"
    else:
        rank_color = "#00FFCC"

    draw.text((100, 995), f"過失深刻度ランク ： {rank}", fill=rank_color, font=get_font(27))
    draw.text((100, 1045), f"公 式 認 定 日   ： {datetime.now().strftime('%Y年%m月%d日')}", fill="#888899", font=get_font(22))

    # 9. 公式角印（重厚な二重朱印・中心配置）
    stamp_x, stamp_y = width - 275, 960
    stamp_w = 175

    draw.rectangle([(stamp_x, stamp_y), (stamp_x + stamp_w, stamp_y + stamp_w)], fill="#1E0D12", outline="#D92626", width=4)
    draw.rectangle([(stamp_x + 8, stamp_y + 8), (stamp_x + stamp_w - 8, stamp_y + stamp_w - 8)], outline="#D92626", width=1)

    for ox in [stamp_x + 16, stamp_x + stamp_w - 16]:
        for oy in [stamp_y + 16, stamp_y + stamp_w - 16]:
            draw.ellipse([(ox - 3, oy - 3), (ox + 3, oy + 3)], fill="#D92626")

    stamp_font = get_font(38)
    draw.text((stamp_x + 48, stamp_y + 48), "黒", fill="#E83030", font=stamp_font, anchor="mm")
    draw.text((stamp_x + 127, stamp_y + 48), "歴", fill="#E83030", font=stamp_font, anchor="mm")
    draw.text((stamp_x + 48, stamp_y + 127), "院", fill="#E83030", font=stamp_font, anchor="mm")
    draw.text((stamp_x + 127, stamp_y + 127), "印", fill="#E
