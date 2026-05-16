from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

# =========================================================
# 기본 설정
# =========================================================
BASE_DATE = date(2026, 5, 17)   # 아래 base_count 값들이 이 날짜 기준
TIMEZONE = "Asia/Seoul"

OUTPUT_DIR = Path(".")          # 현재 폴더에 png 저장
REPORT_DIR = Path(".")          # txt 보고서 저장 위치
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

# 카테고리 필터
# "birth", "activity" 중에서 필요한 것만 남기면 됨
GENERATE_CATEGORIES = {"birth", "activity"}

# 특정 title만 뽑고 싶으면 여기에 넣기
# 예: ONLY_TITLES = {"데뷔", "결성일"}
ONLY_TITLES = set()

# =========================================================
# 이미지 표시 옵션
# =========================================================
SHOW_TITLE = True
SHOW_CATEGORY = False
SHOW_BASE_DATE = False
SHOW_TODAY_DATE = False

USE_THOUSANDS_SEPARATOR = False   # D+10,641처럼 쉼표 표시
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
# 데이터
# base_count = 2026-05-17 기준 값
# =========================================================
items = [
    # 멤버 출생
    {"category": "birth", "title": "이새롬 출생", "base_count": 10641, "filename": "birth_saerom.png"},
    {"category": "birth", "title": "송하영 출생", "base_count": 10376, "filename": "birth_hayoung.png"},
    {"category": "birth", "title": "장규리 출생", "base_count": 10287, "filename": "birth_gyuri.png"},
    {"category": "birth", "title": "박지원 출생", "base_count": 10204, "filename": "birth_jiwon.png"},
    {"category": "birth", "title": "노지선 출생", "base_count": 9956, "filename": "birth_jisun.png"},
    {"category": "birth", "title": "이서연 출생", "base_count": 9531, "filename": "birth_seoyeon.png"},
    {"category": "birth", "title": "이채영 출생", "base_count": 9418, "filename": "birth_chaeyoung.png"},
    {"category": "birth", "title": "이나경 출생", "base_count": 9400, "filename": "birth_nagyung.png"},
    {"category": "birth", "title": "백지헌 출생", "base_count": 8350, "filename": "birth_jiheon.png"},

    # 그룹 / 활동 / 곡
    {"category": "activity", "title": "결성일", "base_count": 3071, "filename": "formed.png"},
    {"category": "activity", "title": "유리구두", "base_count": 3009, "filename": "glass_shoes.png"},
    {"category": "activity", "title": "데뷔", "base_count": 2954, "filename": "debut.png"},
    {"category": "activity", "title": "두근두근", "base_count": 2822, "filename": "to_heart.png"},
    {"category": "activity", "title": "럽밤", "base_count": 2695, "filename": "love_bomb.png"},
    {"category": "activity", "title": "펀", "base_count": 2458, "filename": "fun.png"},
    {"category": "activity", "title": "필굿", "base_count": 1988, "filename": "feel_good.png"},
    {"category": "activity", "title": "위고", "base_count": 1745, "filename": "we_go.png"},
    {"category": "activity", "title": "톡앤톡", "base_count": 1638, "filename": "talk_and_talk.png"},
    {"category": "activity", "title": "첫 1위", "base_count": 1632, "filename": "first_win.png"},
    {"category": "activity", "title": "디엠", "base_count": 1500, "filename": "dm.png"},
    {"category": "activity", "title": "팬미팅", "base_count": 1405, "filename": "fanmeeting.png"},
    {"category": "activity", "title": "스디웨", "base_count": 1339, "filename": "stay_this_way.png"},
    {"category": "activity", "title": "러브프롬", "base_count": 1244, "filename": "love_from.png"},
    {"category": "activity", "title": "미나우", "base_count": 996, "filename": "menow.png"},
    {"category": "activity", "title": "프롬나우", "base_count": 760, "filename": "from_now.png"},
    {"category": "activity", "title": "슈퍼소닉", "base_count": 562, "filename": "supersonic.png"},
    {"category": "activity", "title": "프롬", "base_count": 429, "filename": "from.png"},
    {"category": "activity", "title": "fromm", "base_count": 366, "filename": "fromm.png"},
    {"category": "activity", "title": "라큐베", "base_count": 245, "filename": "lacube.png"},
    {"category": "activity", "title": "나우투머로우", "base_count": 201, "filename": "now_tomorrow.png"},
    {"category": "activity", "title": "하얀그리움", "base_count": 85, "filename": "white_longing.png"},
    {"category": "activity", "title": "나우투머로우 앵콘", "base_count": 26, "filename": "now_tomorrow_encore.png"},
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


def format_dplus(value: int) -> str:
    if USE_THOUSANDS_SEPARATOR:
        return f"D+{value:,}"
    return f"D+{value}"


def get_today() -> date:
    return datetime.now(ZoneInfo(TIMEZONE)).date()


def current_count(item: dict, today: date) -> int:
    delta_days = (today - BASE_DATE).days
    return item["base_count"] + delta_days


def get_start_date(item: dict) -> date:
    # 해당일을 1일차로 계산
    # base_count = (BASE_DATE - start_date).days + 1
    return BASE_DATE - timedelta(days=item["base_count"] - 1)


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

    # 테두리
    draw.rectangle(
        [(0, 0), (IMAGE_WIDTH - 1, IMAGE_HEIGHT - 1)],
        outline=BORDER_COLOR,
        width=BORDER_WIDTH
    )

    # 각 줄 준비
    lines = []

    if SHOW_CATEGORY:
        category_text = "출생" if item["category"] == "birth" else "활동"
        lines.append(("small", category_text))

    lines.append(("main", dplus_text))

    if SHOW_TITLE:
        lines.append(("title", title))

    if SHOW_BASE_DATE:
        lines.append(("meta", f"기준일: {BASE_DATE.isoformat()}"))

    if SHOW_TODAY_DATE:
        lines.append(("meta", f"오늘: {today.isoformat()}"))

    # 폰트 준비
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

    # 전체 높이 계산
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
# 현재 상태 보고서
# =========================================================
def write_status_report(items_to_use, today: date):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = REPORT_DIR / "dplus_status.txt"

    lines = []
    lines.append(f"[D+ 현재값] {today.isoformat()}")
    lines.append("")

    # 카테고리별 출력
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
# - 10000일 미만: 500일 단위
# - 10000일 이상: 1000일 단위
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
        start_date = get_start_date(item)

        # 이 해의 시작일/끝일에 해당하는 D+ 값
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

    print(f"기준일(BASE_DATE): {BASE_DATE}")
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
