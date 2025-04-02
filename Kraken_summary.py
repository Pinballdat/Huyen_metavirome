import pandas as pd
import os

file = "/data18tb/datnguyen/Huyen_metavirome/13_Report.tabular"

content = pd.read_csv(file, sep="\t", names=["Percentage", "Number of fragments in clade", "Number of fragments in taxon", "Rank", "Tax ID", "Scientific name"])
Rank = ["U", "R", "D", "K", "P", "C", "O", "F", "G", "S"]
order = []
for index in content.index:
    if content.at[index, "Rank"] not in order:
        order.append(content.at[index, "Rank"])
#     if content.at[index, "Rank"] != "U":
#         content.at[index, content.at[index, "Rank"]] = content.at[index, "Scientific name"]
#         if content.at[index, "Rank"] not in order:
#             order.append(content.at[index, "Rank"])
sorted_order = sorted(order, key=lambda x: Rank.index(x[0]) if x[0] in Rank else len(Rank))
# print(sorted_order)
# print(list(content["Scientific name"]))
# for index in content:
#     if content.at[index, "Rank"] == "R1":
# new = content["Scientific name"].str.split(" +", n=-1, expand=True)
# print(new)


# Thêm các cột mới vào content theo sorted_order
for rank in sorted_order:
    content[rank] = ""

# Điền giá trị vào cột tương ứng với Rank
for index, row in content.iterrows():
    rank = row["Rank"]
    if rank in sorted_order:
        content.at[index, rank] = row["Scientific name"]
        
# Xử lý điền dữ liệu theo quy tắc phân cấp trong content
for row in range(1, len(content)):  # Bắt đầu từ dòng 1 (dòng 0 giữ nguyên)
    reset_index = None  # Đánh dấu vị trí cần xóa giá trị bên phải
    
    for col in sorted_order:  # Duyệt theo đúng thứ tự cấp bậc trong sorted_order
        if col in content.columns:
            if pd.notna(content.at[row, col]) and content.at[row, col] != "":  
                # Nếu có giá trị mới xuất hiện
                reset_index = sorted_order.index(col) + 1  
            elif pd.isna(content.at[row, col]) or content.at[row, col] == "":  
                # Nếu ô này rỗng nhưng cột trước có giá trị -> Kế thừa từ dòng trên
                prev_col = sorted_order[sorted_order.index(col) - 1] if sorted_order.index(col) > 0 else None
                if prev_col and pd.notna(content.at[row - 1, col]) and content.at[row - 1, col] != "":
                    content.at[row, col] = content.at[row - 1, col]
    
    # Nếu reset_index đã được đánh dấu, xóa tất cả giá trị bên phải nó
    if reset_index is not None:
        for col in sorted_order[reset_index:]:
            if col in content.columns:
                content.at[row, col] = ""
content = content.applymap(lambda x: x.lstrip() if isinstance(x, str) else x)
# print(list(content["S"]))

# Điền giá trị còn thiếu theo thứ tự từ trái sang phải
# content[sorted_order] = content[sorted_order].replace("", pd.NA).ffill(axis=1)
# print(content)
content.to_excel("13_Report.xlsx")
