from main import get_exam_page, simulate_login
from bs4 import BeautifulSoup


# 读取账号密码
def read_user_credentials():
    with open("user_credentials_cleaned.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    return lines


# 读取对应的账号密码
def get_user_credentials(lines):
    for i, line in enumerate(lines):
        if line.strip() == "------------":
            return lines[i - 2].strip(), lines[i - 1].strip()
    return None, None  # 如果没有找到分隔符，返回默认值


# 提取时间、考场、课程名称
def get_exam_time_and_place(exam_page):
    soup = BeautifulSoup(exam_page, "html.parser")
    table = soup.find("table", {"id": "dataList"})
    if not table:
        print("未找到考试信息表格")
        return []

    exam_info = []

    for row in table.find_all("tr")[1:]:  # 跳过表头
        columns = row.find_all("td")
        if len(columns) > 7:  # 确保行中有足够的列
            course_name = columns[4].get_text(strip=True)
            exam_time = columns[6].get_text(strip=True)
            exam_place = columns[7].get_text(strip=True)
            exam_info.append((course_name, exam_time, exam_place))

    return exam_info


if __name__ == "__main__":
    lines = read_user_credentials()
    i = 0
    while i < len(lines):
        try:
            username, password = get_user_credentials(lines[i : i + 3])
            if username and password:  # 确保用户名和密码都存在
                print(f"尝试登录 {username} {password}")
                # 模拟登录
                session, cookies = simulate_login(username, password)
                # 获取考试安排页面
                exam_page = get_exam_page(session, cookies)
                # 提取时间、考场、课程名称
                exam_info = get_exam_time_and_place(exam_page.text)
                if exam_info:
                    print(f"考试信息: {exam_info}")
                    # 将信息写入文件
                    with open("exam_info.txt", "a", encoding="utf-8") as f:
                        for course, time, place in exam_info:
                            f.write(
                                f"课程名称: {course}, 考试时间: {time}, 考场: {place}\n"
                            )
                else:
                    print(f"无法获取考试信息 {username} {password}")
            i += 3  # 跳过当前用户的三行
        except Exception as e:
            print(f"处理 {username} {password} 时发生错误: {e}")
            i += 3  # 确保即使出错也跳过当前用户的三行
