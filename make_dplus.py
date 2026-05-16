from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

# =========================================================
# 기본 설정
# =========================================================

TIMEZONE = "Asia/Seoul"

OUTPUT_DIR = Path(".")
REPORT_DIR = Path(".")
BASE_URL = "https://eofwaer.github.io/dday"

IMAGE_WIDTH = 800
IMAGE_HEIGHT = 400

# =========================================================
# 생성 옵션
# =========================================================

GENERATE_IMAGES = True
GENERATE_STATUS_REPORT = True
GENERATE_MILESTONE_REPORT = True
GENERATE_LINK_LIST = True

GENERATE_CATEGORIES = {"birth", "activity"}

# 특정 항목만 생성하고 싶으면 예: {"데뷔", "fromm"}
ONLY_TITLES = set()

# =========================================================
# 이미지 표시 옵션
# =========================================================

SHOW_TITLE = True
SHOW_CATEGORY = False
SHOW_DATE = False
SHOW_TODAY_DATE = False

USE_THOUSANDS_SEPARATOR = False

BORDER_WIDTH = 8
BACKGROUND_COLOR = "white"
TEXT_COLOR = "black"
BORDER_COLOR = "black"

# =========================================================
# 폰트 경로
# =========================================================

FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

# =========================================================
# D+ 데이터
# 해당일을 1일차로 계산
# =========================================================

items = [
    # 멤버 출생
    {"category": "birth", "title": "이새롬 출생", "date": date(1997, 1, 7), "filename": "birth_saerom.png"},
    {"category": "birth", "title": "송하영 출생", "date": date(1997, 9, 29), "filename": "birth_hayoung.png"},
    {"category": "birth", "title": "장규리 출생", "date": date(1997, 12, 27), "filename": "birth_gyuri.png"},
    {"category": "birth", "title": "박지원 출생", "date": date(1998, 3, 20), "filename": "birth_jiwon.png"},
    {"category": "birth", "title": "노지선 출생", "date": date(1998, 11, 23), "filename": "birth_jisun.png"},
    {"category": "birth", "title": "이서연 출생", "date": date(2000, 1, 22), "filename": "birth_seoyeon.png"},
    {"category": "birth", "title": "이채영 출생", "date": date(2000, 5, 14), "filename": "birth_chaeyoung.png"},
    {"category": "birth", "title": "이나경 출생", "date": date(2000, 6, 1), "filename": "birth_nagyung.png"},
    {"category": "birth", "title": "백지헌 출생", "date": date(2003, 4, 17), "filename": "birth_jiheon.png"},

    # 그룹 / 활동 / 곡
    {"category": "activity", "title": "결성일", "date": date(2017, 9, 27), "filename": "formed.png"},
    {"category": "activity", "title": "유리구두", "date": date(2017, 11, 30), "filename": "glass_shoes.png"},
    {"category": "activity", "title": "데뷔", "date": date(2018, 1, 24), "filename": "debut.png"},
    {"category": "activity", "title": "두근두근", "date": date(2018, 6, 5), "filename": "to_heart.png"},
    {"category": "activity", "title": "럽밤", "date": date(2018, 10, 10), "filename": "love_bomb.png"},
    {"category": "activity", "title": "펀", "date": date(2019, 6, 4), "filename": "fun.png"},
    {"category": "activity", "title": "필굿", "date": date(2020, 9, 16), "filename": "feel_good.png"},
    {"category": "activity", "title": "위고", "date": date(2021, 5, 17), "filename": "we_go.png"},
    {"category": "activity", "title": "톡앤톡", "date": date(2021, 9, 1), "filename": "talk_and_talk.png"},
    {"category": "activity", "title": "첫 1위", "date": date(2021, 9, 7), "filename": "first_win.png"},
    {"category": "activity", "title": "디엠", "date": date(2022, 1, 17), "filename": "dm.png"},
    {"category": "activity", "title": "팬미팅", "date": date(2022, 4, 22), "filename": "fanmeeting.png"},
    {"category": "activity", "title": "스디웨", "date": date(2022, 6, 27), "filename": "stay_this_way.png"},
    {"category": "activity", "title": "러브프롬", "date": date(2022, 9, 30), "filename": "love_from.png"},
    {"category": "activity", "title": "미나우", "date": date(2023, 6, 5), "filename": "menow.png"},
    {"category": "activity", "title": "프롬나우", "date": date(2024, 1, 27), "filename": "from_now.png"},
    {"category": "activity", "title": "슈퍼소닉", "date": date(2024, 8, 12), "filename": "supersonic.png"},
    {"category": "activity", "title": "프롬", "date": date(2024, 12, 23), "filename": "from.png"},
    {"category": "activity", "title": "fromm", "date": date(2025, 2, 24), "filename": "fromm.png"},
    {"category": "activity", "title": "라큐베", "date": date(2025, 6, 25), "filename": "lacube.png"},
    {"category": "activity", "title": "나우투머로우", "date": date(2025, 8, 8), "filename": "now_tomorrow.png"},
    {"category": "activity", "title": "하얀그리움", "date": date(2025, 12, 2), "filename": "white_longing.png"},
    {"category": "activity", "title": "나우투머로우 앵콘", "date": date(2026, 1, 30), "filename": "now_tomorrow_encore.png"},
    {"category": "activity", "title": "일본데뷔", "date": date(2026, 4, 1), "filename": "japan_debut.png"},
]

# =========================================================
# 공용 함수
# =========================================================

def load_font(size: int):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def fit_font(draw: ImageDraw.ImageDraw, text: str, max_width: int, start_size: int):
    size = start_size
    while size >= 10:
        font = load_font(size)
        bbox = draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        if width <= max_width:
            return font
        size -= 2
    return load_font(10)


def text_width_height(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_centered_text(draw, text, center_x, y, font, fill):
    w, _ = text_width_height(draw, text, font)
    x = center_x - w // 2
    draw.text((x, y), text, font=font, fill=fill)


def get_today() -> date:
    return datetime.now(ZoneInfo(TIMEZONE)).date()


def current_count(item: dict, today: date) -> int:
    # 해당일을 1일차로 계산
    return (today - item["date"]).days + 1


def format_dplus(value: int) -> str:
    if USE_THOUSANDS_SEPARATOR:
        return f"D+{value:,}"
    return f"D+{value}"


def filter_items(all_items):
    result = []
    for item in all_items:
        if item["category"] not in GENERATE_CATEGORIES:
            continue
        if ONLY_TITLES and item["title"] not in ONLY_TITLES:
            continue
        result.append(item)
    return result


# =========================================================
# 이미지 생성
# =========================================================

def make_image(item: dict, today: date):
    title = item["title"]
    filename = item["filename"]
    dplus_value = current_count(item, today)
    dplus_text = format_dplus(dplus_value)

    img = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)

    draw.rectangle(
        [(0, 0), (IMAGE_WIDTH - 1, IMAGE_HEIGHT - 1)],
        outline=BORDER_COLOR,
        width=BORDER_WIDTH
    )

    lines = []

    if SHOW_CATEGORY:
        category_text = "출생" if item["category"] == "birth" else "활동"
        lines.append(("small", category_text))

    lines.append(("main", dplus_text))

    if SHOW_TITLE:
        lines.append(("title", title))

    if SHOW_DATE:
        lines.append(("meta", f"시작일: {item['date'].isoformat()}"))

    if SHOW_TODAY_DATE:
        lines.append(("meta", f"오늘: {today.isoformat()}"))

    font_map = {}

    for line_type, text in lines:
        if line_type == "main":
            font_map[(line_type, text)] = fit_font(draw, text, IMAGE_WIDTH - 80, 180)
        elif line_type == "title":
            font_map[(line_type, text)] = fit_font(draw, text, IMAGE_WIDTH - 80, 42)
        elif line_type == "small":
            font_map[(line_type, text)] = fit_font(draw, text, IMAGE_WIDTH - 80, 28)
        else:
            font_map[(line_type, text)] = fit_font(draw, text, IMAGE_WIDTH - 80, 24)

    spacing_map = {
        "small": 10,
        "main": 18,
        "title": 10,
        "meta": 6,
    }

    total_height = 0
    line_heights = []

    for i, (line_type, text) in enumerate(lines):
        font = font_map[(line_type, text)]
        _, h = text_width_height(draw, text, font)
        line_heights.append(h)
        total_height += h
        if i < len(lines) - 1:
            total_height += spacing_map[line_type]

    y = (IMAGE_HEIGHT - total_height) // 2

    for i, (line_type, text) in enumerate(lines):
        font = font_map[(line_type, text)]
        _, h = text_width_height(draw, text, font)
        draw_centered_text(draw, text, IMAGE_WIDTH // 2, y, font, TEXT_COLOR)
        y += h
        if i < len(lines) - 1:
            y += spacing_map[line_type]

    output_path = OUTPUT_DIR / filename
    img.save(output_path)
    print(f"생성 완료: {output_path} / {dplus_text} / {title}")


# =========================================================
# 현재값 보고서
# =========================================================

def write_status_report(items_to_use, today: date):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORT_DIR / "dplus_status.txt"

    lines = []
    lines.append(f"[D+ 현재값] {today.isoformat()}")
    lines.append("")

    for category in ["birth", "activity"]:
        category_items = [x for x in items_to_use if x["category"] == category]
        if not category_items:
            continue

        category_name = "멤버 출생" if category == "birth" else "그룹/활동/곡"
        lines.append(f"## {category_name}")

        for item in category_items:
            value = current_count(item, today)
            lines.append(f"{item['title']} : D+{value}")

        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"상태 보고서 생성 완료: {output_path}")


# =========================================================
# 올해 milestone 보고서
# 규칙:
# 10000일 미만: 500일 단위
# 10000일 이상: 1000일 단위
# =========================================================

def is_valid_milestone(n: int) -> bool:
    if n < 1:
        return False
    if n < 10000:
        return n % 500 == 0
    return n % 1000 == 0


def write_milestone_report(items_to_use, report_year: int):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORT_DIR / f"dplus_milestones_{report_year}.txt"

    year_start = date(report_year, 1, 1)
    year_end = date(report_year, 12, 31)

    milestone_rows = []

    for item in items_to_use:
        start_date = item["date"]

        count_at_year_start = (year_start - start_date).days + 1
        count_at_year_end = (year_end - start_date).days + 1

        if count_at_year_end < 1:
            continue

        lower = max(1, count_at_year_start)
        upper = max(1, count_at_year_end)

        for n in range(lower, upper + 1):
            if not is_valid_milestone(n):
                continue

            milestone_date = start_date + timedelta(days=n - 1)

            if year_start <= milestone_date <= year_end:
                milestone_rows.append((milestone_date, item["title"], n))

    milestone_rows.sort(key=lambda x: (x[0], x[1], x[2]))

    lines = []
    lines.append(f"[{report_year}년 milestone 일정]")
    lines.append("규칙: 500일 단위 / 10000일 이후는 1000일 단위")
    lines.append("")

    if not milestone_rows:
        lines.append("해당 연도 milestone 없음")
    else:
        for milestone_date, title, n in milestone_rows:
            lines.append(f"{milestone_date.isoformat()} - {title} {n}일")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"milestone 보고서 생성 완료: {output_path}")


# =========================================================
# 링크 목록
# =========================================================

def write_link_list(items_to_use):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORT_DIR / "dplus_links.txt"

    lines = []
    lines.append("[D+ 이미지 링크 목록]")
    lines.append("")

    for item in items_to_use:
        lines.append(f"{item['title']} : {BASE_URL}/{item['filename']}")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"링크 목록 생성 완료: {output_path}")


# =========================================================
# 메인
# =========================================================

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    today = get_today()
    items_to_use = filter_items(items)

    print(f"오늘(today): {today}")
    print(f"사용 항목 수: {len(items_to_use)}")

    if GENERATE_IMAGES:
        for item in items_to_use:
            make_image(item, today)

    if GENERATE_STATUS_REPORT:
        write_status_report(items_to_use, today)

    if GENERATE_MILESTONE_REPORT:
        write_milestone_report(items_to_use, today.year)

    if GENERATE_LINK_LIST:
        write_link_list(items_to_use)


if __name__ == "__main__":
    main()
