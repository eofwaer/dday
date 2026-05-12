from PIL import Image, ImageDraw, ImageFont
from datetime import date

# 행사 정보
title = "중앙대 축제"
target_date = date(2026, 5, 21)
date_text = "2026-05-21"

# 오늘 날짜 기준 D-day 계산
today = date.today()
diff = (target_date - today).days

if diff > 0:
    dday_text = f"D-{diff}"
elif diff == 0:
    dday_text = "D-DAY"
else:
    dday_text = "이미 지난 일정"

# 이미지 설정
width, height = 500, 120
img = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(img)

# GitHub Actions용 폰트
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

title_font = ImageFont.truetype(font_path, 24)
dday_font = ImageFont.truetype(font_path, 48)
date_font = ImageFont.truetype(font_path, 18)

def center_text(text, font, y, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    draw.text((x, y), text, font=font, fill=fill)

center_text(title, title_font, 10, "black")
center_text(dday_text, dday_font, 38, "red")
center_text(date_text, date_font, 92, "black")

img.save("dday.png")

print("dday.png 생성 완료")
print("결과:", dday_text)
