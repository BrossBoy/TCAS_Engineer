import json

tcas_data = []
name = []
univer = []
detail = []
cost = []
tcas1 = []
tcas2 = []
tcas3 = []
tcas4 = []

file_path = "data/tcas_data.json"
with open("data/tcas_data.json", encoding="utf-8") as json_file:
    data = json.load(json_file)

for i in range(len(data)):
    tcas_data.append(data[f"eng{i}"])

for i in tcas_data:
    name.append(i["name"])
    univer.append(i["univer"])
    detail.append(i["detail"])

for j in detail:
    if "ค่าใช้จ่าย" in j:
        cost.append(j["ค่าใช้จ่าย"])
    else:
        cost.append("ไม่มีรายละเอียดค่าใช้จ่าย")
    tcas1.append(j["รอบ 1 Portfolio"])
    tcas2.append(j["รอบ 2 Quota"])
    tcas3.append(j["รอบ 3 Admission"])
    tcas4.append(j["รอบ 4 Direct Admission"])
