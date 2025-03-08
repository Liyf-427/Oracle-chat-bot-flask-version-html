from datetime import datetime, timedelta

from testb import pred_b
from wt_est import est
import os
import re
#global variable
# Part A weather
# extract data
# pre-define location
def get_file_path_from_address():
    """
    从 static 文件夹中的 address.txt 中读取文件路径并返回。
    """
    # 设置文件路径
    file_path = "static/address.txt"

    # 检查文件是否存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ 文件 {file_path} 不存在，请检查文件路径。")

    # 读取文件中的路径
    with open(file_path, 'r') as file:
        address = file.readline().strip()  # 提取路径并去除多余空白
    return address

# 示例
file_path = get_file_path_from_address()
print(f"读取的文件路径: {file_path}")

locations = ["Beijing", "New York", "London", "Manchester"]

# data format matching（yyyy/mm/dd）
date_pattern = r"(\d{4})[./](\d{1,2})[./](\d{1,2})"  # 支持 yyyy.mm.dd 或 yyyy/mm/dd 格式

# the main function
def main(category,input_data):
    if category =='A':

        location,date=parse_weather_query(input_data)
        print(location,date)
        # 错误检查
        if not location:
            ans = (f"❌ Not found valid location，Please search the following location：{', '.join(locations)}")
            return ans
        if not date:
            ans = ("❌ Not found valid date，please use yyyy/mm/dd format（for example 2024/01/05）Or 'tomorrow', 'today', 'next Monday' 。")
            return ans
        temperature,humidity=est(location,date)
        ans = "At location",location,"finding weather at date:",date,"The temperature is :",temperature,"The humidity is :",humidity

    elif category =='B':
        date = extract_date(input_data)
        print(date)
        ans = pred_b(date)
        ans = "The air quality at date",date,"is:",ans
        return ans

    elif category =='C':
        numbers = [float(x) for x in input_data.split(',')]
        ans = min(numbers)

    return ans

def print_result(category,input,output):
    if category =='A':
        result = f"The weather to find is: {output}"
    elif category =='B':
        result = f"The air quality is: {output}"
    elif category =='C':
        result = f"The minimum in array is: {output}"
    return result


# Nature Language time process & match（into yyyy/mm/dd）
def extract_date(text):
    today = datetime.today()
    match = re.search(date_pattern, text)
    if match:
        return f"{match.group(1)}/{match.group(2).zfill(2)}/{match.group(3).zfill(2)}"
    text = re.sub(r"\s+", "", text.strip().lower())
    # process NL date
    if "tomorrow" in text.lower():
        return (today + timedelta(days=1)).strftime("%Y/%m/%d")
    if "today" in text.lower():
        return today.strftime("%Y/%m/%d")
    if "nextmonday" in text:
        days = 7 - today.weekday()
        return (today + timedelta(days=days)).strftime("%Y/%m/%d")
    if "nexttuesday" in text:
        days = 8 - today.weekday()
        return (today + timedelta(days=days)).strftime("%Y/%m/%d")
    if "nextwednesday" in text:
        days = 9- today.weekday()
        return (today + timedelta(days=days)).strftime("%Y/%m/%d")
    if "nextthursday" in text:
        days = 10 - today.weekday()
        return (today + timedelta(days=days)).strftime("%Y/%m/%d")
    if "nextfriday" in text:
        days = 11 - today.weekday()
        return (today + timedelta(days=days)).strftime("%Y/%m/%d")
    if "nextsaturday" in text:
        days = 12 - today.weekday()
        return (today + timedelta(days=days)).strftime("%Y/%m/%d")
    if "nextsunday" in text:
        days = 13 - today.weekday()
        return (today + timedelta(days=days)).strftime("%Y/%m/%d")

    if "thismonday" in text:
        days_until_monday = (0 - today.weekday()) % 7
        return (today + timedelta(days=days_until_monday)).strftime("%Y/%m/%d")
    if "thistuesday" in text:
        days_until_monday = (1 - today.weekday()) % 7
        return (today + timedelta(days=days_until_monday)).strftime("%Y/%m/%d")
    if "thiswednesday" in text:
        days_until_monday = (2 - today.weekday()) % 7
        return (today + timedelta(days=days_until_monday)).strftime("%Y/%m/%d")
    if "thisthursday" in text:
        days_until_monday = (3 - today.weekday()) % 7
        return (today + timedelta(days=days_until_monday)).strftime("%Y/%m/%d")
    if "thisfriday" in text:
        days_until_monday = (4 - today.weekday()) % 7
        return (today + timedelta(days=days_until_monday)).strftime("%Y/%m/%d")
    if "thissaturday" in text:
        days_until_monday = (5 - today.weekday()) % 7
        return (today + timedelta(days=days_until_monday)).strftime("%Y/%m/%d")
    if "thissunday" in text:
        days_until_monday = (6 - today.weekday()) % 7
        return (today + timedelta(days=days_until_monday)).strftime("%Y/%m/%d")

    return None  # not found

# location matcher
def extract_location(text):
    for loc in locations:
        if loc in text:
            return loc
    return None

# recognizer of nl-46/106 def
def parse_weather_query(query):
    location = extract_location(query)
    date = extract_date(query)
    return location, date

