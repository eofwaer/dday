from __future__ import annotations

import colorsys
import os
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# =========================================================
# 경로 / 설정
# =========================================================

ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT / "assets"
FONTS_DIR = ROOT / "fonts"
OUTPUT_DIR = ROOT  # png/txt를 저장할 위치

BONOBONO_PATH = ASSETS_DIR / "bonobono.png"

# 테스트용 날짜 지정 가능
# 예: TEST_TODAY = date(2026, 6, 4)
TEST_TODAY = None

# 이미지 크기
WIDTH = 300
HEIGHT = 150

# 일반판 설정
NORMAL_BG = (0, 0, 0)
NORMAL_BORDER = (255, 255, 255)
NORMAL_TEXT = (255, 255, 255)

# 특별판 설정
SPECIAL_BG = (0, 0, 0, 255)

# 일반판은 예전처럼 숫자만 보이게
SHOW_TITLE_ON_NORMAL = False

# n주년 당일엔 전부 특별판으로 만들지 여부
SPECIAL_ON_ANNIVERSARY = True

# 만약 특정 파일만 특별판으로 하고 싶으면 여기에 파일명만 넣고
# SPECIAL_ONLY_THESE = {"debut.png", "fun.png"}
# 처럼 사용하면 됨. None이면 전부 허용.
SPECIAL_ONLY_THESE = None

# =========================================================
# 데이터
# =========================================================

@dataclass
class DPlusItem:
    filename: str
    title: str
    event_date: date


def d(y: int, m: int, day: int) -> date:
    return date(y, m, day)


ITEMS: list[DPlusItem] = [
    # =========================
    # 멤버 생일
    # =========================
    DPlusItem("birth_saerom.png", "새롬", d(1997, 1, 7)),
    DPlusItem("birth_hayoung.png", "하영", d(1997, 9, 29)),
    DPlusItem("birth_gyuri.png", "규리", d(1997, 12, 27)),
    DPlusItem("birth_jiwon.png", "지원", d(1998, 3, 20)),
    DPlusItem("birth_jisun.png", "지선", d(1998, 11, 23)),
    DPlusItem("birth_seoyeon.png", "서연", d(2000, 1, 22)),
    DPlusItem("birth_chaeyoung.png", "채영", d(2000, 5, 14)),
    DPlusItem("birth_nagyung.png", "나경", d(2000, 6, 1)),
    DPlusItem("birth_jiheon.png", "지헌", d(2003, 4, 17)),

    # =========================
    # 팀 / 활동 기념일
    # =========================
    DPlusItem("formed.png", "결성", d(2017, 9, 27)),
    DPlusItem("glass_shoes.png", "유리구두", d(2017, 11, 30)),
    DPlusItem("debut.png", "데뷔", d(2018, 1, 24)),

    # 네 repo에서 to_heart.png를 두근두근용으로 쓰던 흐름 기준
    # 만약 파일명이 dkdk.png면 바꿔서 쓰면 됨
    DPlusItem("to_heart.png", "두근두근", d(2018, 6, 5)),

    DPlusItem("love_bomb.png", "LOVE BOMB", d(2018, 10, 10)),
    DPlusItem("fun.png", "FUN!", d(2019, 6, 4)),
    DPlusItem("feel_good.png", "Feel Good", d(2020, 9, 16)),
    DPlusItem("we_go.png", "WE GO", d(2021, 5, 17)),
    DPlusItem("talk_and_talk.png", "Talk & Talk", d(2021, 9, 1)),
    DPlusItem("first_win.png", "첫 1위", d(2021, 9, 7)),
    DPlusItem("dm.png", "DM", d(2022, 1, 17)),
    DPlusItem("fanmeeting.png", "팬미팅", d(2022, 3, 26)),
    DPlusItem("stay_this_way.png", "Stay This Way", d(2022, 6, 27)),
    DPlusItem("love_from.png", "Love From.", d(2023, 3, 15)),

    # 언마월 3주년을 원한 흐름 기준으로 menow.png를 2023-06-05로 둠
    DPlusItem("menow.png", "언마월", d(2023, 6, 5)),

    # 아래부터는 네 현재 repo 날짜와 다를 수 있으니
    # 필요하면 수정해서 쓰면 됨
    DPlusItem("from_now.png", "From Now.", d(2024, 1, 1)),
    DPlusItem("supersonic.png", "Supersonic", d(2024, 8, 12)),
    DPlusItem("from.png", "FROM", d(2025, 1, 1)),
    DPlusItem("fromm.png", "fromm", d(2025, 1, 1)),
    DPlusItem("lacube.png", "La Cube", d(2025, 1, 1)),
    DPlusItem("now_tomorrow.png", "Now, Tomorrow", d(2025, 1, 1)),
    DPlusItem("white_longing.png", "하얀 그리움", d(2025, 1, 1)),
    DPlusItem("now_tomorrow_encore.png", "Now, Tomorrow ENCORE", d(2025, 1, 1)),
    DPlusItem("japan_debut.png", "일본 데뷔", d(2025, 6, 1)),
]

# =========================================================
# 폰트
# =========================================================

FONT_CANDIDATES = [
    FONTS_DIR / "NanumGothicBold.ttf",
    FONTS_DIR / "NanumGothic.ttf",
    FONTS_DIR / "Pretendard-Bold.ttf",
    FONTS_DIR / "NotoSansCJKkr-Bold.otf",
    Path("/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf"),
    Path("/usr/share/fonts/truetype/nanum/NanumBarunGothicBold.ttf"),
    Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
]


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        if path.exists():
            try:
                return ImageFont.truetype(str(path), size=size)
            except Exception:
                pass
    return ImageFont.load_default()


FONT_NORMAL_NUMBER = load_font(56)
FONT_SPECIAL_TITLE = load_font(28)
FONT_SPECIAL_NUMBER = load_font(44)
FONT_CORNER = load_font(20)

# =========================================================
# 유틸
# =========================================================

def today_kst() -> date:
    if TEST_TODAY is not None:
        return TEST_TODAY
    return datetime.now().date()


def get_dplus(start_date: date, today: date) -> int:
    # 당일을 1일차로 계산
    return (today - start_date).days + 1


def get_anniversary_years(start_date: date, today: date) -> int:
    """
    정확히 n주년 '당일'이면 n 반환, 아니면 0
    """
    years = today.year - start_date.year

    if (today.month, today.day) < (start_date.month, start_date.day):
        years -= 1

    if years >= 1 and (today.month, today.day) == (start_date.month, start_date.day):
        return years

    return 0


def base_name(filename: str) -> str:
    return Path(filename).stem


def output_png_path(filename: str) -> Path:
    return OUTPUT_DIR / filename


def output_txt_path(filename: str) -> Path:
    return OUTPUT_DIR / f"{base_name(filename)}.txt"


def fit_text(draw: ImageDraw.ImageDraw, text: str, max_width: int, start_size: int) -> ImageFont.ImageFont:
    """
    긴 제목을 폭 안에 맞추기 위해 폰트 크기를 줄여가며 찾음
    """
    size = start_size
    while size >= 12:
        font = load_font(size)
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            return font
        size -= 1
    return load_font(12)


def center_text_x(draw: ImageDraw.ImageDraw, text: str, font, image_width: int) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    return (image_width - text_w) // 2


def rainbow_color(t: float) -> tuple[int, int, int]:
    r, g, b = colorsys.hsv_to_rgb(t, 1.0, 1.0)
    return (int(r * 255), int(g * 255), int(b * 255))


def draw_rainbow_border(draw: ImageDraw.ImageDraw, x1: int, y1: int, x2: int, y2: int, thickness: int = 4) -> None:
    width = x2 - x1
    height = y2 - y1

    # 위/아래
    for x in range(width + 1):
        t = x / max(1, width)
        color = rainbow_color(t)
        for k in range(thickness):
            draw.point((x1 + x, y1 + k), fill=color)
            draw.point((x1 + x, y2 - k), fill=color)

    # 좌/우
    for y in range(height + 1):
        t = y / max(1, height)
        color = rainbow_color(t)
        for k in range(thickness):
            draw.point((x1 + k, y1 + y), fill=color)
            draw.point((x2 - k, y1 + y), fill=color)


def draw_rainbow_text(img: Image.Image, text: str, font, x: int, y: int) -> None:
    """
    x, y는 텍스트의 좌상단
    """
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    mask = Image.new("L", (text_w, text_h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.text((0, 0), text, font=font, fill=255)

    grad = Image.new("RGBA", (text_w, text_h), (0, 0, 0, 0))
    grad_draw = ImageDraw.Draw(grad)

    for px in range(text_w):
        t = px / max(1, text_w - 1)
        color = rainbow_color(t)
        grad_draw.line((px, 0, px, text_h), fill=color + (255,))

    img.paste(grad, (x, y), mask)


def paste_bonobono(base_img: Image.Image, x: int, y: int, max_w: int = 70, max_h: int = 70) -> None:
    if not BONOBONO_PATH.exists():
        return

    try:
        bono = Image.open(BONOBONO_PATH).convert("RGBA")
        bono.thumbnail((max_w, max_h))
        base_img.paste(bono, (x, y), bono)
    except Exception:
        pass


def save_text_file(filename: str, display_text: str) -> None:
    txt_path = output_txt_path(filename)
    txt_path.write_text(display_text, encoding="utf-8")


# =========================================================
# 렌더링
# =========================================================

def render_normal_image(item: DPlusItem, display_text: str) -> None:
    img = Image.new("RGB", (WIDTH, HEIGHT), NORMAL_BG)
    draw = ImageDraw.Draw(img)

    # 바깥 흰 테두리
    draw.rectangle([0, 0, WIDTH - 1, HEIGHT - 1], outline=NORMAL_BORDER, width=3)

    if SHOW_TITLE_ON_NORMAL:
        title_font = fit_text(draw, item.title, max_width=WIDTH - 20, start_size=28)
        x = center_text_x(draw, item.title, title_font, WIDTH)
        draw.text((x, 18), item.title, font=title_font, fill=NORMAL_TEXT)

        number_font = fit_text(draw, display_text, max_width=WIDTH - 20, start_size=56)
        x = center_text_x(draw, display_text, number_font, WIDTH)
        draw.text((x, 64), display_text, font=number_font, fill=NORMAL_TEXT)
    else:
        # 숫자만 크게
        number_font = fit_text(draw, display_text, max_width=WIDTH - 20, start_size=60)
        bbox = draw.textbbox((0, 0), display_text, font=number_font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        x = (WIDTH - text_w) // 2
        y = (HEIGHT - text_h) // 2 - 4
        draw.text((x, y), display_text, font=number_font, fill=NORMAL_TEXT)

    out_path = output_png_path(item.filename)
    img.save(out_path)
    save_text_file(item.filename, display_text)


def render_special_image(item: DPlusItem, display_text: str, anniversary_years: int) -> None:
    img = Image.new("RGBA", (WIDTH, HEIGHT), SPECIAL_BG)
    draw = ImageDraw.Draw(img)

    # 무지개 테두리
    draw_rainbow_border(draw, 2, 2, WIDTH - 3, HEIGHT - 3, thickness=4)

    # 왼쪽 아래 보노보노
    paste_bonobono(img, 10, HEIGHT - 80, max_w=68, max_h=68)

    # 제목
    title_font = fit_text(draw, item.title, max_width=WIDTH - 20, start_size=28)
    title_bbox = draw.textbbox((0, 0), item.title, font=title_font)
    title_w = title_bbox[2] - title_bbox[0]
    title_x = (WIDTH - title_w) // 2
    title_y = 16
    draw_rainbow_text(img, item.title, title_font, title_x, title_y)

    # n주년 텍스트
    number_font = fit_text(draw, display_text, max_width=WIDTH - 36, start_size=46)
    num_bbox = draw.textbbox((0, 0), display_text, font=number_font)
    num_w = num_bbox[2] - num_bbox[0]
    num_x = (WIDTH - num_w) // 2 + 10  # 왼쪽 캐릭터 때문에 약간 우측으로
    num_y = 58
    draw_rainbow_text(img, display_text, number_font, num_x, num_y)

    # 구석에 n 표시(원하면)
    corner_text = str(anniversary_years)
    draw.text((WIDTH - 20, 10), corner_text, font=FONT_CORNER, fill=(255, 255, 255, 180), anchor="ra")

    out_path = output_png_path(item.filename)
    img.convert("RGB").save(out_path)
    save_text_file(item.filename, display_text)


# =========================================================
# 메인 로직
# =========================================================

def should_use_special(item: DPlusItem, anniversary_years: int) -> bool:
    if anniversary_years <= 0:
        return False

    if not SPECIAL_ON_ANNIVERSARY:
        return False

    if SPECIAL_ONLY_THESE is None:
        return True

    return item.filename in SPECIAL_ONLY_THESE


def make_one(item: DPlusItem, today: date) -> None:
    anniv_years = get_anniversary_years(item.event_date, today)

    if anniv_years > 0:
        display_text = f"{anniv_years}주년"
    else:
        dplus_value = get_dplus(item.event_date, today)
        display_text = f"D+{dplus_value}"

    if should_use_special(item, anniv_years):
        render_special_image(item, display_text, anniv_years)
        print(f"[SPECIAL] {item.filename:<24} -> {display_text}")
    else:
        render_normal_image(item, display_text)
        print(f"[NORMAL ] {item.filename:<24} -> {display_text}")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    today = today_kst()
    print(f"today = {today.isoformat()}")

    for item in ITEMS:
        make_one(item, today)

    print("done.")


if __name__ == "__main__":
    main()
