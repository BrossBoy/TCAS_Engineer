import json
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import re

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

int_tcas1 = [
    int("".join(re.findall(r"\d+", s))) if re.findall(r"\d+", s) else 0 for s in tcas1
]
int_tcas2 = [
    int("".join(re.findall(r"\d+", s))) if re.findall(r"\d+", s) else 0 for s in tcas2
]
int_tcas3 = [
    int("".join(re.findall(r"\d+", s))) if re.findall(r"\d+", s) else 0 for s in tcas3
]
int_tcas4 = [
    int("".join(re.findall(r"\d+", s))) if re.findall(r"\d+", s) else 0 for s in tcas4
]
# print(int_tcas1)

new_data = []
for i, j, a, b, c, d, e in zip(
    univer, name, cost, int_tcas1, int_tcas2, int_tcas3, int_tcas4
):
    new_data.append(
        {
            "University": i,
            "Course": j,
            "Cost": a,
            "Tcas1": b,
            "Tcas2": c,
            "Tcas3": d,
            "Tcas4": e,
        }
    )
# print(new_data)

app = Dash(__name__)
dropdown_opt = list(set(univer))
course_opt = list(set(name))
app.layout = html.Div(
    [
        html.H1("TCAS Dashboard", style={"color": "Orange", "textAlign": "center"}),
        html.P("เลือกข้อมูลที่ต้องการ", style={"color": "blue"}),
        dcc.Dropdown(
            options=dropdown_opt, id="dropdown", placeholder="เลือกมหาวิทยาลัย"
        ),
        dcc.Dropdown(
            options=course_opt, id="course_dropdown", placeholder="เลือกหลักสูตร"
        ),
        dcc.Graph(id="bar_chart"),
    ]
)

# Define callback to update course dropdown based on university selection
@app.callback(
    Output("course_dropdown", "options"),
    [Input("dropdown", "value")]
)
def update_course_dropdown(selected_universities):
    if not selected_universities:
        return course_opt

    filtered_courses = set()
    for entry in new_data:
        if entry["University"] in selected_universities:
            filtered_courses.add(entry["Course"])
    filtered_courses = list(filtered_courses)
    return [{"label": course, "value": course} for course in filtered_courses]

# Define callback to update bar_chart based on dropdown and course_dropdown selections
@app.callback(
    Output("bar_chart", "figure"),
    [Input("dropdown", "value"),
     Input("course_dropdown", "value")]
)
def update_bar_chart(selected_universities, selected_courses):
    if not selected_universities or not selected_courses:
        return go.Figure()

    filtered_data = [entry for entry in new_data if entry["University"] in selected_universities and entry["Course"] in selected_courses]

    fig = go.Figure()
    fig.update_layout(
        title="จำนวนการรับสมัครในแต่ละหลักสูตร",
        xaxis_title="รอบของการสมัคร TCAS",
        yaxis_title="จำนวนคนที่รับในแต่ละรอบ",
        plot_bgcolor='rgba(0,0,0,0)'
    )

    for round_name in ["Tcas1", "Tcas2", "Tcas3", "Tcas4"]:
        round_data = [entry[round_name] for entry in filtered_data]
        fig.add_trace(go.Bar(
            x=[round_name],
            y=[sum(round_data)],
            name=round_name,
            marker=dict(color="blue" if round_name == "Tcas1" else \
                            "green" if round_name == "Tcas2" else \
                            "orange" if round_name == "Tcas3" else \
                            "red")
        ))

    return fig

if __name__ == "__main__":
    app.run(debug=True)