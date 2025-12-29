import csv
import sys


def clean_string(s: str) -> str:
    return s.strip()


OLD_COLUMNS = [
    "名前(姓)",
    "名前(名)",
    "敬称",
    "郵便番号(数字7桁)",
    "都道府県",
    "市区町村(最大23文字)",
    "番地・号(12文字)",
    "建物名(最大25文字)",
    "連名1(姓)",
    "連名1(名)",
    "連名1(敬称)",
    "連名2(姓)",
    "連名2(名)",
    "連名2(敬称)",
    "連名3(姓)",
    "連名3(名)",
    "連名3(敬称)",
    "連名4(姓)",
    "連名4(名)",
    "連名4(敬称)",
]

NEW_COLUMNS = [
    "last_name",
    "first_name",
    "title",
    "postal_code",
    "prefecture",
    "city",
    "address_line1",
    "address_line2",
    "last_name_2",
    "first_name_2",
    "title_2",
    "last_name_3",
    "first_name_3",
    "title_3",
    "last_name_4",
    "first_name_4",
    "title_4",
]


def generate_name(last_name, first_name, last_name_1, first_name_1):
    if last_name == "" and first_name == "":
        return None

    if last_name != last_name_1 and last_name != "":
        return f"{last_name}　{first_name}"
    else:
        place_holder_len = len(last_name_1) + len(first_name_1) - len(first_name)
        place_holder = "　" * place_holder_len
        return f"{place_holder}　{first_name}"


def replace_number(s: str) -> str:
    num_map = {
        "0": "〇",
        "1": "一",
        "2": "二",
        "3": "三",
        "4": "四",
        "5": "五",
        "6": "六",
        "7": "七",
        "8": "八",
        "9": "九",
    }
    for k, v in num_map.items():
        s = s.replace(k, v)
    return s


def get_col_index(name: str) -> int:
    return NEW_COLUMNS.index(name)


def i(name: str) -> int:
    return get_col_index(name)


def get(row, name: str) -> str:
    raw_text = row[i(name)]
    cleaned_text = clean_string(raw_text)
    return cleaned_text


def template(
    postal_code,
    full_address_1,
    full_address_2,
    title,
    last_name,
    first_name,
    other_names,
):
    tex = f"""
  {{{last_name}　{first_name}}}{{{title}}}
  {{{postal_code}}}
  {{{full_address_1}}}
  {{{full_address_2}}}
"""
    name_header = "\\addaddress"
    for name in other_names:
        if name is None or name == "":
            continue
        name_header += f"\n  [{name}]"
    tex = name_header + tex
    tex += "\n\\newpage\n"

    return tex


def process_row(row):
    # Process Address
    postal_code = get(row, "postal_code")
    prefecture = get(row, "prefecture")
    city = get(row, "city")
    address_line1 = get(row, "address_line1")
    address_line2 = get(row, "address_line2")

    full_address_1 = f"{prefecture}{city}{address_line1}"
    full_address_1 = replace_number(full_address_1)
    full_address_2 = address_line2
    full_address_2 = replace_number(full_address_2)

    # Process Name
    last_name_1 = get(row, "last_name")
    first_name_1 = get(row, "first_name")
    title = get(row, "title")

    last_name_2 = get(row, "last_name_2")
    first_name_2 = get(row, "first_name_2")
    full_name_2 = generate_name(last_name_2, first_name_2, last_name_1, first_name_1)

    last_name_3 = get(row, "last_name_3")
    first_name_3 = get(row, "first_name_3")
    full_name_3 = generate_name(last_name_3, first_name_3, last_name_1, first_name_1)

    last_name_4 = get(row, "last_name_4")
    first_name_4 = get(row, "first_name_4")
    full_name_4 = generate_name(last_name_4, first_name_4, last_name_1, first_name_1)

    other_names = [full_name_2, full_name_3, full_name_4]

    tex = template(
        postal_code,
        full_address_1,
        full_address_2,
        title,
        last_name_1,
        first_name_1,
        other_names,
    )
    return tex


def run(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            tex = process_row(row)
            print(tex)


if __name__ == "__main__":
    run(sys.argv[1])
