import json
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import re
import plotly.graph_objects as go

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
        dcc.Dropdown(options=dropdown_opt, id="dropdown", placeholder="เลือกมหาวิทยาลัย"),
        dcc.Dropdown(
            options=course_opt, id="course_dropdown", placeholder="เลือกหลักสูตร"
        ),
        html.Div(id="selected_data"),
        dcc.Graph(id="bar_chart2"),
        dcc.Graph(id="bar_chart1"),
    ]
)


# Callback to update course dropdown based on university selection
@app.callback(Output("course_dropdown", "options"), [Input("dropdown", "value")])
def update_course_dropdown(selected_universities):
    if not selected_universities:
        return [{"label": opt, "value": opt} for opt in course_opt]

    filtered_courses = set()
    for entry in new_data:
        if entry["University"] in selected_universities:
            filtered_courses.add(entry["Course"])
    filtered_courses = list(filtered_courses)
    return [{"label": course, "value": course} for course in filtered_courses]


# Callback to update bar_chart1 based on dropdown and course_dropdown selections
@app.callback(
    Output("bar_chart1", "figure"),
    [Input("dropdown", "value"), Input("course_dropdown", "value")],
)
def update_bar_chart1(selected_universities, selected_courses):
    if not selected_universities or not selected_courses:
        return go.Figure(
            data=[go.Scatter(x=[0, 1], y=[0, 1], mode="text", text="No selected data")]
        )

    filtered_data = [
        entry
        for entry in new_data
        if entry["University"] in selected_universities
        and entry["Course"] in selected_courses
    ]

    fig = go.Figure()
    fig.update_layout(
        title="จำนวนการรับสมัครในแต่ละหลักสูตร (Bar Chart 1)",
        xaxis_title="รอบของการสมัคร TCAS",
        yaxis_title="จำนวนคนที่รับในแต่ละรอบ",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    for round_name in ["Tcas1", "Tcas2", "Tcas3", "Tcas4"]:
        round_data = [entry[round_name] for entry in filtered_data]
        fig.add_trace(
            go.Bar(
                x=[round_name],
                y=[sum(round_data)],
                name=round_name,
                marker=dict(
                    color=(
                        "blue"
                        if round_name == "Tcas1"
                        else (
                            "green"
                            if round_name == "Tcas2"
                            else "orange" if round_name == "Tcas3" else "red"
                        )
                    )
                ),
            )
        )

    return fig


# Callback to update bar_chart2 based on dropdown selection
@app.callback(Output("bar_chart2", "figure"), [Input("dropdown", "value")])
def update_bar_chart2(selected_university):
    if not selected_university:
        return go.Figure(
            data=[go.Scatter(x=[0, 1], y=[0, 1], mode="text", text="No selected data")]
        )

    # Filter data for the selected university
    filtered_data = [
        entry for entry in new_data if entry["University"] == selected_university
    ]

    # Aggregate TCAS rounds for each course
    course_totals = {}
    for entry in filtered_data:
        course = entry["Course"]
        if course in course_totals:
            course_totals[course]["Tcas1"] += entry["Tcas1"]
            course_totals[course]["Tcas2"] += entry["Tcas2"]
            course_totals[course]["Tcas3"] += entry["Tcas3"]
            course_totals[course]["Tcas4"] += entry["Tcas4"]
        else:
            course_totals[course] = {
                "Tcas1": entry["Tcas1"],
                "Tcas2": entry["Tcas2"],
                "Tcas3": entry["Tcas3"],
                "Tcas4": entry["Tcas4"],
            }

    # Prepare data for bar chart 2 (horizontal bar chart)
    courses = list(course_totals.keys())
    tcas_totals = [sum(course_totals[course].values()) for course in courses]

    fig = go.Figure()
    fig.update_layout(
        title=f"จำนวนการรับสมัครในทุกหลักสูตรของมหาวิทยาลัย {selected_university}",
        xaxis_title="จำนวนคนที่รับในทุกรอบ",
        yaxis_title="หลักสูตร",
        plot_bgcolor="rgba(0,0,0,0)",
        barmode="stack",  # Optional: Stack bars for better comparison
        yaxis={"categoryorder": "total ascending"},  # Order bars by total ascending
    )

    fig.add_trace(
        go.Bar(
            x=tcas_totals,
            y=courses,
            orientation="h",  # Horizontal orientation
            marker=dict(color="blue"),
            name="Total TCAS",
        )
    )

    return fig


# Callback to update selected_data display based on dropdown selections
@app.callback(
    Output("selected_data", "children"),
    [Input("dropdown", "value"), Input("course_dropdown", "value")],
)
def update_selected_data(selected_universities, selected_courses):
    if not selected_universities or not selected_courses:
        return "No selected data"

    filtered_data = [
        entry
        for entry in new_data
        if entry["University"] in selected_universities
        and entry["Course"] in selected_courses
    ]

    data_str = ""
    for entry in filtered_data:
        data_str += f"มหาวิทยาลัย: {entry['University']}, หลักสูตร: {entry['Course']}, ค่าใช้จ่าย: {entry['Cost']}"

    return html.Div(
        [html.H3("ข้อมูลที่เลือก", style={"color": "green"}), dcc.Markdown(data_str)]
    )


if __name__ == "__main__":
    app.run(debug=True)
