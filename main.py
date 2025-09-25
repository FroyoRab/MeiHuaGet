import flet as ft
from meihua import MeiHuaCalc, DIZHI12
from bagua import GUA_MEAN


# 可选输入项
INPUT_METHOD = [
    {"key": "datetime", "text": "日期"},
    {"key": "random_number", "text": "数字"},
    {"key": "number_with_time", "text": "数字+时间"},
    {"key": "chinese_chars", "text": "字"},
    {"key": "upper_hexgram_with_time", "text": "上卦+时间"},
]


class InputSection(ft.Column):
    """负责收集排盘参数的输入区域。"""

    def __init__(self, page: ft.Page, state: dict, on_calculate):
        super().__init__(spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER, width=400)
        self.page = page
        self.state = state
        self.on_calculate = on_calculate

        self.select_date_show = ft.Text("", visible=True)
        self.select_time_show = ft.Text("")

        self.isgive_luan_date = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(label="输入公历", value=""),
                    ft.Radio(label="输入农历", value="lunar"),
                ],
                width=400,
            ),
            value="",
            on_change=lambda e: self.state.update({"islunardate": True if e.data == "lunar" else False}),
            visible=True,
        )

        self.lunar_date_input = self._build_date_input()
        self.random_numbers_input = self._build_random_number_input()
        self.number_time_input = self._build_number_with_time_input()
        self.time_type_container, self.time_input_24, self.time_input_dizhi = self._build_time_inputs()
        self.is_use_lunar_datetime = self._build_lunar_calculate_selector()
        self.input_method_dd = self._build_input_method_dropdown()
        self.calculate_btn = ft.ElevatedButton("排盘", on_click=self.on_calculate, width=400, height=50)

        self.controls = [
            ft.Text("梅花易数排盘工具", size=24, weight=ft.FontWeight.BOLD),
            self.input_method_dd,
            ft.Divider(),
            self.isgive_luan_date,
            self.lunar_date_input,
            self.random_numbers_input,
            self.number_time_input,
            self.time_type_container,
            self.is_use_lunar_datetime,
            ft.Divider(),
            self.calculate_btn,
        ]

        self._input_groups = {
            "datetime": [
                self.lunar_date_input,
                self.time_type_container,
                self.select_date_show,
                self.is_use_lunar_datetime,
                self.isgive_luan_date,
            ],
            "random_number": [self.random_numbers_input],
            "number_with_time": [self.number_time_input, self.time_type_container],
            "chinese_chars": [],
            "upper_hexgram_with_time": [],
        }
        self._time_groups = {"24": [self.time_input_24], "12": [self.time_input_dizhi]}

    def _build_input_method_dropdown(self) -> ft.Dropdown:
        return ft.Dropdown(
            label="选择输入方式",
            options=[ft.DropdownOption(**option) for option in INPUT_METHOD],
            on_change=self._update_visibility,
            value="datetime",
            width=400,
        )

    def _build_random_number_input(self) -> ft.Container:
        def number_input(event: ft.ControlEvent, index: int):
            self.state.update({f"number{index}": event.control.value})

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.TextField(label="输入第一个数", on_change=lambda e: number_input(e, 1)),
                    ft.TextField(label="输入第二个数", on_change=lambda e: number_input(e, 2)),
                    ft.TextField(label="可选输入，直接作为动爻", on_change=lambda e: number_input(e, 3)),
                ]
            ),
            visible=False,
            width=400,
        )

    def _build_date_input(self) -> ft.Row:
        def date_select(event: ft.ControlEvent):
            date_str = event.control.value.strftime("%Y-%m-%d")
            self.select_date_show.value = date_str
            self.state.update({"date": date_str})
            self.select_date_show.visible = True
            self.select_date_show.update()

        return ft.Row(
            [
                ft.ElevatedButton(
                    "选择日期",
                    icon=ft.Icons.CALENDAR_MONTH,
                    on_click=lambda _: self.page.open(ft.DatePicker(on_change=date_select)),
                ),
                self.select_date_show,
            ],
            width=400,
            visible=True,
        )

    def _build_time_inputs(self):
        time_type_radio = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value="24", label="24小时"),
                    ft.Radio(value="12", label="12地支"),
                ],
                col=6,
                width=400,
            ),
            on_change=self._update_visibility,
            value="24",
        )

        def time_select(event: ft.ControlEvent):
            self.select_time_show.value = event.data
            self.state.update({"time": event.data})
            self.select_time_show.visible = True
            self.select_time_show.update()

        time_input_24 = ft.Row(
            [
                ft.ElevatedButton(
                    "选择时间",
                    icon=ft.Icons.CALENDAR_MONTH,
                    on_click=lambda _: self.page.open(ft.TimePicker(on_change=time_select)),
                ),
                self.select_time_show,
            ],
            width=400,
            visible=True,
        )

        time_input_dizhi = ft.Dropdown(
            label="时辰",
            options=[ft.dropdown.Option(d) for d in DIZHI12],
            on_change=lambda e: self.state.update({"time": e.data}),
            visible=False,
            width=200,
        )

        time_type_container = ft.Column(
            [
                ft.Text("时间输入方式:"),
                time_type_radio,
                ft.Row([time_input_24, time_input_dizhi], col=4),
            ],
            visible=True,
            width=400,
        )

        return time_type_container, time_input_24, time_input_dizhi

    def _build_number_with_time_input(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.TextField(on_change=lambda e: self.state.update({"number1": e.control.value}), label="输入数字"),
                ]
            ),
            visible=False,
            width=400,
        )

    def _build_lunar_calculate_selector(self) -> ft.RadioGroup:
        return ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(label="使用农历日期计算", value="uselunar"),
                    ft.Radio(label="使用公历日期计算", value="notuselunar"),
                ],
                width=400,
            ),
            on_change=lambda e: self.state.update({"uselunar": True if e.data == "uselunar" else False}),
            visible=True,
            value="uselunar",
        )

    def _update_visibility(self, event: ft.ControlEvent):
        key = event.data
        for group in (self._input_groups, self._time_groups):
            if key in group:
                for controls in group.values():
                    for control in controls:
                        control.visible = False
                for control in group[key]:
                    control.visible = True
                self.state.clear()
                break
        self.page.update()


class ResultSection(ft.Column):
    """负责展示排盘结果。"""

    NATURE_COLOR = {
        "金": ft.Colors.YELLOW_700,
        "木": ft.Colors.GREEN,
        "水": ft.Colors.BLUE,
        "火": ft.Colors.RED,
        "土": ft.Colors.BROWN,
    }

    def __init__(self):
        self.result_container = ft.Column(horizontal_alignment=ft.MainAxisAlignment.CENTER)
        self.result_mean_container = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.START)
        super().__init__(
            controls=[self.result_container, self.result_mean_container],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def show_results(self, meihuaobj, result):
        result_releation_size = 10
        result_64gua_name_size = 30
        result_partname_size = 10
        result_partsymbol_size = 50
        result_partsymbol_height = 0.720

        gua_obj_dict = {"本卦": result.self_gua, "互卦": result.hugua, "变卦": result.biangua}
        part_template = {"upper": {}, "lower": {}}
        res_list = []

        for gua_label, obj in gua_obj_dict.items():
            part = {name: dict(values) for name, values in part_template.items()}
            element_index, element_relation = result.check_element_kill(
                obj.upper.nature, obj.lower.nature, result.change_gua_index
            )

            for part_name in part.keys():
                part_obj = getattr(obj, part_name)
                part[part_name]["symbol"] = part_obj.symbol
                part[part_name]["color"] = self.NATURE_COLOR[part_obj.nature]
                part[part_name]["name"] = f"{part_obj.name}({part_obj.attribute})"
                part[part_name]["decline_direction"] = f"{part_obj.decline},{part_obj.direction}"

            upper = part["upper"]
            lower = part["lower"]
            gua_symbol = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            spans=[
                                ft.TextSpan(
                                    spans=[
                                        ft.TextSpan(text=upper["name"], style=ft.TextStyle(size=result_partname_size)),
                                        ft.TextSpan(
                                            text=upper["symbol"],
                                            style=ft.TextStyle(size=result_partsymbol_size, height=result_partsymbol_height),
                                        ),
                                        ft.TextSpan(
                                            text=upper["decline_direction"], style=ft.TextStyle(size=result_partname_size)
                                        ),
                                    ],
                                    style=ft.TextStyle(color=upper["color"]),
                                ),
                            ]
                        ),
                        ft.Text(
                            spans=[
                                ft.TextSpan(
                                    spans=[
                                        ft.TextSpan(text=lower["name"], style=ft.TextStyle(size=result_partname_size)),
                                        ft.TextSpan(
                                            text=lower["symbol"],
                                            style=ft.TextStyle(size=result_partsymbol_size, height=result_partsymbol_height),
                                        ),
                                        ft.TextSpan(
                                            text=lower["decline_direction"], style=ft.TextStyle(size=result_partname_size)
                                        ),
                                    ],
                                    style=ft.TextStyle(color=lower["color"]),
                                ),
                            ]
                        ),
                    ],
                    spacing=0,
                    expand=0,
                )
            )
            gua_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(value=f"{gua_label}:{obj.name}", size=result_64gua_name_size),
                            gua_symbol,
                            ft.Text(value=element_relation, size=result_releation_size),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    on_click=self.show_gua_detail,
                    key=(obj.binary_str, result.change_gua_index),
                ),
                col={"xs": 12, "md": 8, "lg": 4},
            )
            res_list.append(gua_card)

        self.result_container.controls = [
            ft.Text(value=meihuaobj.calc_info),
            ft.ResponsiveRow(res_list, run_spacing={"xs": 8}, alignment=ft.MainAxisAlignment.SPACE_AROUND),
        ]
        self.result_container.visible = True
        self.result_container.update()

        self.result_mean_container.controls = []
        self.result_mean_container.visible = False
        self.result_mean_container.update()

    def show_gua_detail(self, event: ft.ControlEvent):
        gua_bin_str, change_gua_index = event.control.key
        mean = GUA_MEAN[gua_bin_str]["mean"]

        add_dict = {"原文": "origin", "卦辞白话文": "write_origin", "邵雍解": "shaoyong", "梅花易一姐注": "yijie"}
        index_dict = {"卦辞": 0, "爻辞": change_gua_index}

        column_element = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.START)
        for title, index in index_dict.items():
            column_element.controls.append(ft.Text(value=title, theme_style=ft.TextThemeStyle.TITLE_LARGE))
            for sub_title, key in add_dict.items():
                column_element.controls.append(ft.Text(value=sub_title, theme_style=ft.TextThemeStyle.TITLE_MEDIUM))
                try:
                    column_element.controls.append(
                        ft.Text(value=mean[index][key][0], theme_style=ft.TextThemeStyle.BODY_SMALL)
                    )
                except LookupError:
                    column_element.controls.pop()
            column_element.controls.append(
                ft.ExpansionTile(
                    title=ft.Text(f"{title}更多"),
                    controls=[
                        ft.Text(value=mean[index]["all"], theme_style=ft.TextThemeStyle.LABEL_SMALL),
                    ],
                    expanded_cross_axis_alignment=ft.CrossAxisAlignment.START,
                )
            )

        like = ft.Card(
            content=ft.Text(
                value=(
                    f"{MeiHuaCalc.get_like(bin_str=gua_bin_str[:3][::-1])}\n"
                    f"{MeiHuaCalc.get_like(bin_str=gua_bin_str[3:][::-1])}"
                ),
                theme_style=ft.TextThemeStyle.BODY_MEDIUM,
            )
        )
        info = ft.Card(content=ft.Container(content=column_element))

        self.result_mean_container.controls = [like, info]
        self.result_mean_container.visible = True
        self.result_mean_container.update()


class MeiHuaApp:
    """整体页面的封装，负责协调输入与结果区域。"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.state: dict = {}

        self.page.title = "排个好的"
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.adaptive = True

        self.result_section = ResultSection()
        self.input_section = InputSection(self.page, self.state, self.calculate)

        self.page.add(self.input_section)
        self.page.add(self.result_section)
        self.page.update()

    def calculate(self, _):
        meihuaobj = MeiHuaCalc(**self.state)
        result = meihuaobj.calclator()
        self.result_section.show_results(meihuaobj, result)


async def main(page: ft.Page):
    MeiHuaApp(page)
    page.update()


if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="assets",
        view=ft.AppView.WEB_BROWSER,
        port=65510,
    )
