from pathlib import Path
from datetime import date
from PIL import Image, ImageDraw, ImageFont

# =====================
# 1. 행사 목록
# =====================

events = [
    {"title": "상지대", "date": date(2026, 5, 12), "filename": "sangji.png"},
    {"title": "순천향대", "date": date(2026, 5, 13), "filename": "soonchunhyang.png"},
    {"title": "남서울대", "date": date(2026, 5, 13), "filename": "namseoul.png"},
    {"title": "성균관대", "date": date(2026, 5, 14), "filename": "skku.png"},
    {"title": "단국대 죽전캠", "date": date(2026, 5, 14), "filename": "dankook_jukjeon.png"},
    {"title": "홍익대 서울캠", "date": date(2026, 5, 15), "filename": "hongik_seoul.png"},
    {"title": "광운대", "date": date(2026, 5, 15), "filename": "kwangwoon.png"},
    {"title": "한밭대", "date": date(2026, 5, 19), "filename": "hanbat.png"},
    {"title": "카이스트", "date": date(2026, 5, 19), "filename": "kaist.png"},
    {"title": "한남대", "date": date(2026, 5, 19), "filename": "hannam.png"},
    {"title": "세종대", "date": date(2026, 5, 20), "filename": "sejong.png"},
    {"title": "상명대", "date": date(2026, 5, 21), "filename": "sangmyung.png"},
    {"title": "전남드래곤즈구장", "date": date(2026, 5, 22), "filename": "jeonnam_dragons.png"},
    {"title": "하노이 케팝 워터 뮤직 페스티벌", "date": date(2026, 6, 6), "filename": "hanoi.png"},
]

# =====================
# 2. 이미지 설정
# =====================

width, height = 300, 120
today = date.today()

# GitHub Actions용 한글 폰트
noto_font = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc")
dejavu_font = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")

if noto_font.exists():
    font_path = str(noto_font)
else:
    font_path = str(dejavu_font)

dday_font = ImageFont.truetype(font_path, 58)
date_font = ImageFont.truetype(font_path, 24)

# =====================
# 3. 함수
# =====================

def get_dday_text(target_date):
    diff = (target_date - today).days

    if diff > 0:
        return f"D-{diff}"
    elif diff == 0:
        return "D-DAY"
    else:
        return "END"

def center_text(draw, text, font, y, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, y), text, font=font, fill=fill)

# =====================
# 4. 행사별 PNG 생성
# =====================

for event in events:
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    target_date = event["date"]
    dday_text = get_dday_text(target_date)
    date_text = target_date.strftime("%m.%d")

    center_text(draw, dday_text, dday_font, 18, "red")
    center_text(draw, date_text, date_font, 82, "black")

    img.save(event["filename"])
    print(f'{event["filename"]} 생성 완료 -> {dday_text} / {date_text}')

print("모든 D-day 이미지 생성 완료")
