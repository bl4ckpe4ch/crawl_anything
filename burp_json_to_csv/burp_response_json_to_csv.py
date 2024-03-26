import json, os, csv, re

os.chdir(os.path.dirname(__file__))

# 设置要读取JSON文件的文件夹路径
dir_path = './detail_results/'
# 输入的json文件路径
json_file_path = './combined.json'
# 输入的csv文件路径
csv_file_path = './result.csv'

# 要提取的字段， 也可以所有字段都提取
FIELDS = ['id', 'jobName', 'industry', 'employmentProspects','jobDefinition','workContent','practiceRequirements','tips','caes','postSalary']
# FIELDS = '*'

# single_txt_to_single_json
def single_txt_to_single_json(dir_path):
    for filename in os.listdir(dir_path):
        # 拼接完整的文件路径
        if not filename.endswith("json"):
            file_path = os.path.join(dir_path, filename)
        else:
            continue
        assert file_path.endswith("json") == False, '不是txt文件，而是json文件'
        # 确认这是个文件而不是文件夹
        assert os.path.isfile(file_path) == True, '不是文件，而是文件夹'
        # 读取文件内容，去掉前6行的响应头
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()[6:]  # 读取除了前5行之外的所有内容
            # 构建新的文件名和路径,splitext()将文件名和扩展名分开
            new_file_path = os.path.join(dir_path, os.path.splitext(filename)[0] + '.json')
            # 将处理后的内容写入新文件
            with open(new_file_path, 'w', encoding='utf-8') as new_file:
                new_file.writelines(lines)
    print("single_txt_to_single_json已经完成")

# 合并每个文件的小json
def merge_json(dir_path):
    all_data = []
    # 查找所有JSON文件
    json_files = [os.path.join(dir_path, file) for file in os.listdir(dir_path) if file.endswith('.json')]
    print(f"一共有{len(json_files)}个json")
    # 合并这些json
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            all_data.append(data)
    # 将合并后的json写入文件
    with open('combined.json', 'w', encoding='utf-8') as combined_file:
        json.dump(all_data, combined_file, indent=4, ensure_ascii=False)
    assert os.path.exists("combined.json") == True, '合并后的json文件不存在'
    print("merge_json over，所有json已经合并完成")
    

# 读取JSON文件并提取数据
def extract_data_from_json(json_file):
    extracted_data = []
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    for i in range(len(data)):
        assert ('data' in list(data[i].keys())) == True, '我们想要的字段不在json中'
        data[i] = data[i].get('data')
    data = remove_newlines(data)
    if FIELDS == '*':
        print("extract_data_from_json已经完成")
        return data
    else:
        for entry in data:
            extracted_record = {field: entry.get(field, '') for field in FIELDS}
            extracted_data.append(extracted_record)
        print("extract_data_from_json已经完成")
        return extracted_data
    
def remove_newlines(obj):
    if isinstance(obj, str):
        return re.sub(r'\s+', ' ', obj)  # 替换换行符和多余空格为单个空格
    elif isinstance(obj, dict):
        return {k: remove_newlines(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [remove_newlines(elem) for elem in obj]
    else:
        return obj
    
# 保存数据到CSV文件
def save_data_to_csv(data, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS,delimiter='$',quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(data)

# 主程序
def main():
    single_txt_to_single_json(dir_path)
    merge_json(dir_path)
    data = extract_data_from_json(json_file_path)
    save_data_to_csv(data, csv_file_path)
    
if __name__ == "__main__":
    main()