from pathlib import Path
from datetime import date
from PIL import Image, ImageDraw, ImageFont

# =====================
# 1. 행사 목록
# 날짜는 내가 임시로 채운 값
# =====================

events = [
    {"title": "상지대", "date": date(2026, 5, 14), "filename": "sangji.png"},
    {"title": "순천향대", "date": date(2026, 5, 15), "filename": "soonchunhyang.png"},
    {"title": "남서울대", "date": date(2026, 5, 16), "filename": "namseoul.png"},
    {"title": "성균관대", "date": date(2026, 5, 16), "filename": "skku.png"},
    {"title": "단국대 죽전캠", "date": date(2026, 5, 17), "filename": "dankook_jukjeon.png"},
    {"title": "홍익대 서울캠", "date": date(2026, 5, 17), "filename": "hongik_seoul.png"},
    {"title": "광운대", "date": date(2026, 5, 18), "filename": "kwangwoon.png"},
    {"title": "한밭대", "date": date(2026, 5, 19), "filename": "hanbat.png"},
    {"title": "카이스트", "date": date(2026, 5, 19), "filename": "kaist.png"},
    {"title": "한남대", "date": date(2026, 5, 19), "filename": "hannam.png"},
    {"title": "세종대", "date": date(2026, 5, 20), "filename": "sejong.png"},
    {"title": "상명대", "date": date(2026, 5, 20), "filename": "sangmyung.png"},
    {"title": "중앙대", "date": date(2026, 5, 21), "filename": "chungang.png"},
    {"title": "전남드래곤즈구장", "date": date(2026, 5, 24), "filename": "jeonnam_dragons.png"},
]

# =====================
# 2. 이미지 설정
# =====================

width, height = 500, 120
today = date.today()

# GitHub Actions(우분투)에서 쓸 폰트
noto_font = Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc")
dejavu_font = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")

if noto_font.exists():
    font_path = str(noto_font)
else:
    font_path = str(dejavu_font)

title_font = ImageFont.truetype(font_path, 24)
dday_font = ImageFont.truetype(font_path, 48)
date_font = ImageFont.truetype(font_path, 18)

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
        return "이미 지난 일정"

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

    title = event["title"]
    target_date = event["date"]
    date_text = target_date.strftime("%Y-%m-%d")
    dday_text = get_dday_text(target_date)

    center_text(draw, title, title_font, 10, "black")
    center_text(draw, dday_text, dday_font, 38, "red")
    center_text(draw, date_text, date_font, 92, "black")

    img.save(event["filename"])
    print(f'{event["filename"]} 생성 완료 -> {dday_text}')

print("모든 D-day 이미지 생성 완료")
