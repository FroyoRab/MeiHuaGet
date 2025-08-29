import flet as ft
import datetime
import re
from zhdate import ZhDate
from datetime import datetime
from meihua import MeiHuaCalc,DIZHI12
from bagua import BAGUA
import functools

# 可选输入项
INPUT_METHOD = [
    {"key":"datetime","text":"日期"},
    {"key":"random_number","text":"数字"},
    {"key":"number_with_time","text":"数字+时间"},
    {"key":"chinese_chars","text":"字"},
    {"key":"upper_hexgram_with_time","text":"上卦+时间"},
]

def main(page: ft.Page):
    page.title = "梅花易数排盘"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.adaptive = True
    state = {}
    
    def input_select(select:ft.ControlEvent):
        select_input_dict = {
            'datetime':[lunar_date_input,time_type_container,select_date_show,is_use_lunar_datetime,isgive_luan_date],
        }
        select_time_type = {
            '24':[time_input_24,],
            '12':[time_input_dizhi,]
        }
        dicts = [select_input_dict,select_time_type]
        
        use_dict = [x for x in dicts if select.data in x][0] = [x for x in dicts if select.data in x][0]
        if select.data in use_dict:
            for one in use_dict.keys():
                if one == select.data:
                    for one_element in use_dict[one]:
                        one_element.visible = True
                else:
                    for one_element in use_dict[one]:
                        one_element.visible = False
        page.update()
        
    # 输入控件
    input_method_dd = ft.Dropdown(
        label="选择输入方式",
        options=[ft.DropdownOption(**k) for k in INPUT_METHOD],
        on_change=input_select,
        value='datetime',
        width=400
    )
    
    def date_select(date:ft.ControlEvent):
        date_str = date.control.value.strftime("%Y-%m-%d")
        select_date_show.value = date_str
        state.update({"date":date_str})
        select_date_show.visible = True
        select_date_show.update()
    
    select_date_show = ft.Text(
        '',visible=True
    )
    
    isgive_luan_date = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(label='输入公历',value=''),
            ft.Radio(label="输入农历",value='lunar'),
        ],width=400),
        value='',
        on_change=lambda x:state.update({'islunardate':True if x=='lunar' else False}),
        visible=True
    )
    
    lunar_date_input = ft.Row(
        [
            ft.ElevatedButton(
                "选择日期",
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda e: page.open(
                    ft.DatePicker(
                        # first_date=datetime.now(),
                        # last_date=datetime.datetime(year=2025, month=10, day=1),
                        on_change=date_select,
                        # on_dismiss=handle_dismissal,
                    )
                ),
            ),
            select_date_show,
        ],
        width=400,
        visible=True
    )
    
    time_type_radio = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="24", label="24小时"),
            ft.Radio(value="12", label="12地支"),
        ],col=6,width=400),
        on_change=input_select,
        value="24"
    )
    
    select_time_show = ft.Text("")
    
    def time_select(time):
        select_time_show.value = time.data
        state.update({"time":time.data})
        select_time_show.visible = True
        select_time_show.update()
    
    time_input_24 = ft.Row(
        [
            ft.ElevatedButton(
                "选择时间",
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda e: page.open(
                    ft.TimePicker(
                        # first_date=datetime.now(),
                        # last_date=datetime.datetime(year=2025, month=10, day=1),
                        on_change=time_select,
                        # on_dismiss=handle_dismissal,
                    )
                ),
            ),
            select_time_show,
        ],
        width=400,
        visible=True
    )
    
    time_input_dizhi = ft.Dropdown(
        label="时辰",
        options=[ft.dropdown.Option(d) for d in DIZHI12],
        on_change=lambda x : state.update({'time':x}),
        visible=False,
        width=200
    )
    
    is_use_lunar_datetime = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(
                label='使用农历日期计算',
                value='uselunar',                
            ),
            ft.Radio(
                label='使用公历日期计算',
                value='notuselunar'
            )
        ],width=400),
        on_change= lambda x: state.update({'uselunar':True if x == 'uselunar' else False}),
        visible=True,
        value='uselunar'
    )
    
    # random_numbers_input = ft.TextField(
    #     label="输入任意数字",
    #     on_change=state.set_random_numbers,
    #     visible=False,
    #     width=400
    # )
    
    # chinese_chars_input = ft.TextField(
    #     label="输入中文字符串",
    #     on_change=state.set_chinese_chars,
    #     visible=False,
    #     width=400
    # )
    
    # upper_trigram_dd = ft.Dropdown(
    #     label="上卦",
    #     options=[ft.dropdown.Option(f"{v.name}:{v.symbol}") for v in BAGUA],
    #     on_change=state.set_upper_trigram,
    #     visible=False,
    #     width=200
    # )
    
    RESULT_LITTEL_TEXT_SIZE = 10
    RESULT_TEXT_SIZE = 50
    RESULT_SYMBOL_SIZE = 400
    RESULT_SYMBOL_HIGHT = 300
    RESULT_TEXT_HIGHT = 50
    # 结果显示部分
    # 本卦
    bengua_text = ft.TextSpan(style=ft.TextStyle(size=RESULT_TEXT_SIZE))
    bengua_upper = ft.TextSpan(style=ft.TextStyle(size=RESULT_SYMBOL_SIZE))
    bengua_upper_name = ft.TextSpan(style=ft.TextStyle(size=RESULT_LITTEL_TEXT_SIZE))
    bengua_lower = ft.TextSpan(style=ft.TextStyle(size=RESULT_SYMBOL_SIZE))
    bengua_lower_name = ft.TextSpan(style=ft.TextStyle(size=RESULT_LITTEL_TEXT_SIZE))
    
    # bengua_upper = ft.Text(size=RESULT_SYMBOL_SIZE)
    # bengua_upper_name = ft.Text(size=RESULT_LITTEL_TEXT_SIZE)
    # bengua_lower = ft.Text(size=RESULT_SYMBOL_SIZE)
    # bengua_lower_name = ft.Text(size=RESULT_LITTEL_TEXT_SIZE)
    # bengua_symbol = ft.Text(size=RESULT_SYMBOL_SIZE)
    
    # 互卦
    hugua_text = ft.Text(size=RESULT_TEXT_SIZE)
    hugua_upper = ft.Text(size=RESULT_SYMBOL_SIZE)
    hugua_upper_name = ft.Text(size=RESULT_LITTEL_TEXT_SIZE)
    hugua_lower = ft.Text(size=RESULT_SYMBOL_SIZE)
    hugua_lower_name = ft.Text(size=RESULT_LITTEL_TEXT_SIZE)
    # hugua_symbol = ft.Text(size=RESULT_SYMBOL_SIZE)
    
    # 变卦
    biangua_text = ft.Text(size=RESULT_TEXT_SIZE)
    biangua_upper = ft.Text(size=RESULT_SYMBOL_SIZE)
    biangua_upper_name = ft.Text(size=RESULT_LITTEL_TEXT_SIZE)
    biangua_lower = ft.Text(size=RESULT_SYMBOL_SIZE)
    biangua_lower_name = ft.Text(size=RESULT_LITTEL_TEXT_SIZE)
    # biangua_symbol = ft.Text(size=RESULT_SYMBOL_SIZE)
    
    def calculator(data,localvar):
        meihuaobj = MeiHuaCalc(**state)
        res = meihuaobj.calclator()
        gua_obj_dict = {
            'bengua':res.self_gua,
            'hugua':res.hugua,
            'biangua':res.biangua
        }
        for one_gua in gua_obj_dict.keys():
            obj = gua_obj_dict[one_gua]
            # 设置64卦名
            setattr(localvar[f"{one_gua}_text"],'value',getattr(obj,'name'))
            # obj_upper = getattr(obj,'upper')
            # obj_lower = getattr(obj,'lower')
            for one_part_str in ['upper','lower']:
                one_part = getattr(obj,one_part_str)
                # 设置8卦符号
                setattr(localvar[f"{one_gua}_{one_part_str}"],"value",getattr(one_part,'symbol'))
                # 设置8卦名称(属性)
                setattr(
                    localvar[f"{one_gua}_{one_part_str}_name"],"value",
                    f"{getattr(one_part,'name')}({getattr(one_part,'attribute')})"
                )
        
        
        result_container.value = str(res)
        result_container.visible = True
        result_container.update()
        
    local_vars = locals()
    calculate_btn = ft.ElevatedButton(
        "排盘",
        on_click=lambda x:calculator(x,local_vars),
        width=400,
        height=50
    )
    
    # 结果显示区域
    result_container = ft.Row([
        ft.Card(
            content=ft.Text(
                spans=[
                    ft.TextSpan(spans=[bengua_text,]),
                    ft.TextSpan(spans=[
                            bengua_upper_name,
                            bengua_upper
                        ]),
                    ft.TextSpan(spans=[
                        bengua_lower_name,
                        bengua_lower    
                    ]),
                ],
                disabled=False
            ),margin=0
        ),
        ft.Card(
            content=ft.Column(
                [
                    hugua_text,
                    ft.Row([
                        hugua_upper_name,
                        hugua_upper
                    ],height=RESULT_SYMBOL_HIGHT,spacing=0),
                    ft.Row([
                        hugua_lower_name,
                        hugua_lower
                    ],height=RESULT_SYMBOL_HIGHT,spacing=0)
                ],
                width=400,
                spacing=0,
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),margin=0
        ),
        ft.Card(
            content=ft.Column(
                [
                    biangua_text,
                    ft.Row([
                        biangua_upper_name,
                        biangua_upper
                    ],height=RESULT_SYMBOL_HIGHT),
                    ft.Row([
                        biangua_lower_name,
                        biangua_lower
                    ],height=RESULT_SYMBOL_HIGHT)
                ],
                width=400,
                spacing=0,
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),margin=0
        )
    ],width=1200)
    
    
    # def on_calculate(e):
    #     state.calculate(e)
    #     if state.show_result:
    #         # 清空之前的结果
    #         result_container.controls.clear()
            
    #         # 添加新结果
    #         result_container.controls.append(
    #             ft.Text("排盘结果", size=24, weight=ft.FontWeight.BOLD)
    #         )
            
    #         # 本卦显示
    #         result_container.controls.append(
    #             render_hexagram_display(
    #                 state.result["original_hexagram"],
    #                 f"本卦 (第{state.result['moving_yao']}爻动)"
    #             )
    #         )
            
    #         # 互卦显示
    #         result_container.controls.append(
    #             render_hexagram_display(
    #                 state.result["mutual_hexagram"],
    #                 "互卦"
    #             )
    #         )
            
    #         # 变卦显示
    #         result_container.controls.append(
    #             render_hexagram_display(
    #                 state.result["changed_hexagram"],
    #                 "变卦"
    #             )
    #         )
            
    #         # 体用关系
    #         result_container.controls.append(
    #             ft.Container(
    #                 content=ft.Column([
    #                     ft.Text("体用关系", size=20, weight=ft.FontWeight.BOLD),
    #                     ft.Row([
    #                         ft.Column([
    #                             ft.Text("体卦", weight=ft.FontWeight.BOLD),
    #                             ft.Text(state.result["body_use"]["body"]["name"]),
    #                             ft.Text(f"({state.result['body_use']['body']['attribute']})"),
    #                         ], spacing=5),
    #                         ft.Column([
    #                             ft.Text("用卦", weight=ft.FontWeight.BOLD),
    #                             ft.Text(state.result["body_use"]["use"]["name"]),
    #                             ft.Text(f"({state.result['body_use']['use']['attribute']})"),
    #                         ], spacing=5),
    #                     ], spacing=20),
    #                     ft.Text(
    #                         f"关系: {state.result['body_use']['relation']}",
    #                         weight=ft.FontWeight.BOLD,
    #                         color=ft.colors.GREEN if "生" in state.result["body_use"]["relation"] or "和" in state.result["body_use"]["relation"] else ft.colors.RED
    #                     )
    #                 ], spacing=10),
    #                 padding=15,
    #                 border=ft.border.all(1, "#eaeaea"),
    #                 border_radius=10,
    #                 width=page.width - 40
    #             )
    #         )
            
    #         result_container.visible = True
    #     else:
    #         result_container.visible = False
        
    #     page.update()
    
    # calculate_btn.on_click = state.calclator()
    
    # 时间类型选择容器
    time_type_container = ft.Column([
        ft.Text("时间输入方式:"),
        time_type_radio,
        ft.Row([time_input_24, time_input_dizhi],col=4)
    ], visible=True,width=400)
    
    # 主界面布局
    page.add(
        ft.Column([
            ft.Text("梅花易数排盘工具", size=24, weight=ft.FontWeight.BOLD),
            isgive_luan_date,
            input_method_dd,
            lunar_date_input,
            # random_numbers_input,
            # chinese_chars_input,
            # ft.Row([upper_trigram_dd], visible=False),
            time_type_container,
            is_use_lunar_datetime,
            calculate_btn,
            result_container
        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    page.update()
    
    # # 初始更新界面
    # update_input_visibility()

if __name__ == "__main__":
    ft.app(target=main)