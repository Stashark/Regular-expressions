from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# TODO 1: выполните пункты 1-3 ДЗ
fix_contacts = []

for row in contacts_list:
    all_names = " ".join(row[:3]).split()

    if len(all_names) > 0:
        lastname = all_names[0]
    else:
        lastname = ""

    if len(all_names) > 1:
        firstname = all_names[1]
    else:
        firstname = ""

    if len(all_names) > 2:
        surname = all_names[2]
    else:
        surname = ""

    fix_contacts.append([lastname, firstname, surname] + row[3:])

def is_phone(phone):
    # Если поле пустое — возвращаем как есть, ничего не делаем
    if not phone:
        return phone

    ext_match = re.search(r'доб\.?\s*(\d+)', phone)

    if ext_match:
        ext = ext_match.group(1)
        phone = phone[:ext_match.start()]
    else:
        ext = ""

    phone = re.sub(r'[()]', '', phone)

    phone_pattern = r"(\+7|8)?\s*?(\(?\d{3}\)?)[-\s]?(\d{3})[-\s]?(\d{2})[-\s]?(\d{2})\s*?"

    replacement_pattern = r"+7(\2)\3-\4-\5"

    cleaned_phone = re.sub(phone_pattern, replacement_pattern, phone)

    if ext:
        cleaned_phone = cleaned_phone.strip() + " доб." + ext

    return cleaned_phone

for row in fix_contacts:
    if row[0] != "lastname":
        row[5] = is_phone(row[5])

merged = {}

for row in fix_contacts:
    if row[0] == "lastname":
        header = row
        continue

    key = (row[0], row[1])

    if key not in merged:
        merged[key] = row
    else:
        existing = merged[key]
        for i in range(len(existing)):
            if existing[i] == "" and row[i] != "":
                existing[i] = row[i]

result = [header] + list(merged.values())

pprint(result)


# TODO 2: сохраните получившиеся данные в другой файл
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result)