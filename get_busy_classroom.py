import re
from datetime import datetime


def extract_classrooms(file_path):
    classrooms = {}
    seen_lines = set()  # 用于记录已经处理过的行
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            if line in seen_lines:
                print(f"重复行: {line.strip()}")  # 输出重复行
                continue
            seen_lines.add(line)
            match = re.search(
                r"课程名称: (.+?), 考试时间: (\d{4}-\d{2}-\d{2} \d{2}:\d{2})~(\d{2}:\d{2}), 考场: (\S+)",
                line,
            )
            if match:
                subject = match.group(1)
                start_time_str = match.group(2)
                end_time_str = f"{start_time_str[:11]}{match.group(3)}"
                classroom = match.group(4)
                start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M")
                end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M")
                classrooms[classroom] = (start_time, end_time, subject)
    return classrooms


def query_classrooms(classrooms, building_name, current_time):
    available_classrooms = []
    for classroom, (start_time, end_time, subject) in classrooms.items():
        if building_name in classroom and start_time <= current_time <= end_time:
            room_number = classroom.replace(building_name, "").strip()
            available_classrooms.append((room_number, subject))
    return available_classrooms


# 提取教室信息
file_path = "exam_info.txt"
classrooms = extract_classrooms(file_path)

# 查询某个楼的教室
building_name = "综合教学楼"  # 你可以根据需要更改
current_time = datetime.now()  # 获取当前时间
available_classrooms = query_classrooms(classrooms, building_name, current_time)

# 输出结果
if available_classrooms:
    room_numbers = ", ".join([room for room, _ in available_classrooms])
    print(f"在{building_name}的有考场教室：{room_numbers}")
else:
    print(f"在{building_name}没有考场教室。")
