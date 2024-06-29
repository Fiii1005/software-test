import random
import os

fish_types = ['Bluegill', 'Channel Catfish', 'Freshwater Drum', 'Gizzard Shad','River Carpsucker', 'Smallmouth Bass','Sauger']
length_ranges = ['0-3','3-6','6-9','9-12','12-15','15-18','18-21','21-24','24-27','27-30','30-33','33-36','36-39','39-42','42-45','45-48','48-51','51-54','54-57','57-60','60-63','63-66','66-69','69-72','72-75','75-78','78-81','81-84','84-87']
weight_ranges = ['0.00-0.04', '0.04-0.08', '0.08-0.11', '0.11-0.15', '0.15-0.19', '0.19-0.24', '0.24-0.30', '0.30-0.37', '0.37-0.44', '0.44-0.51', '0.51-0.58', '0.58-0.65', '0.65-0.72', '0.72-0.79', '0.79-0.86', '0.86-0.93', '0.93-1.00', '1.00-1.08', '1.08-1.15', '1.15-1.22', '1.22-1.29', '1.29-1.36', '1.36-1.43', '1.43-1.50', '1.50-1.57', '1.57-1.64', '1.64-1.71', '1.71-1.78', '1.78-1.85', '1.85-1.92', '1.92-2.00', '2.00-2.14', '2.14-2.29', '2.29-2.43', '2.43-2.57', '2.57-2.71', '2.71-2.86', '2.86-3.00', '3.00-3.22', '3.22-3.43', '3.43-3.64', '3.64-3.86', '3.86-4.07', '4.07-4.29', '4.29-4.50', '4.50-4.71', '4.71-4.93', '4.93-5.14', '5.14-5.36', '5.36-5.57', '5.57-5.79', '5.79-6.00', '6.00-6.43', '6.43-6.86', '6.86-7.00']

# 生成鱼群数据的函数
def generate_fish_data(year, month, day, unique_entries):
    fish_data = []
    num_records = random.randint(1, 10)  # Random number of records for each day

    for fishspecies in fish_types:
        for _ in range(num_records):
            species = fishspecies
            length_range = random.choice(length_ranges)
            weight_range = random.choice(weight_ranges)
            count = random.randint(1, 20)
            identifier = f"{year},{month},{day},{species},{length_range},{weight_range}"
            # 检查标识符是否已存在
            if identifier not in unique_entries:
                # 如果不存在，添加到集合和data中
                unique_entries.add(identifier)
                # 这里添加你的逻辑来实际添加到data中，例如：
                fish_data.append(f"{year},{month},{day},{species},{length_range},{weight_range},{count}")
                
    
    return fish_data

data=[]
unique_entries = set()

for year in range(2012,2023):
    for month in range(1,12):
        # 计算每月的天数
        days = 0
        if month in [1,3,5,7,8,10,12]:
            days = 31
        elif month in [4,6,9,11]:
            days = 30
        else:
            if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
                days = 29
            else:
                days = 28
        # 生成每天的数据
        for day in range(1,days+1):
            data.extend(generate_fish_data(year, month, day, unique_entries))
#写入文件
# 获取当前脚本文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
# 构建数据集文件的绝对路径
file_path = os.path.join(current_dir, 'dataset', 'fish_data.csv')
with open(file_path, 'w',encoding='utf-8') as f:
    f.write("年,月,日,鱼,范围（长度cm）,范围（重量kg）,数量\n")
    for line in data:
        f.write(f"{line}\n")

print("fish_data.csv数据写入完成")