import flet as ft
import datetime
import re
from zhdate import ZhDate
from datetime import datetime
from meihua import MeiHuaCalc,DIZHI12
from bagua import BAGUA,GUA_MEAN
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
        on_change=lambda x : state.update({'time':x.data}),
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
        on_change= lambda x: state.update({'uselunar': (True if x.data == 'uselunar' else False)}),
        visible=True,
        value='uselunar'
    )
    
    NATURE_COLOR = {
        '金':ft.Colors.YELLOW_700,
        '木':ft.Colors.GREEN,
        '水':ft.Colors.BLUE,
        '火':ft.Colors.RED,
        '土':ft.Colors.BROWN
    }
    
    def select_gua(data:ft.ControlEvent):
        # show gua info on result_mean_container
        gua_bin_str,change_gua_index = data.control.key
        mean = GUA_MEAN[gua_bin_str]['mean']
        add_dict = {
            '原文':'origin',
            '卦辞白话文':'write_origin',
            '邵雍解':'shaoyong'
        }
        index_dict = {
            '卦辞':0,
            '爻辞':change_gua_index
        }
        
        column_element = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.START)
        
        for one_index in index_dict:
            # 大标题，区分卦辞爻辞
            column_element.controls.append(
                ft.Text(value=one_index,theme_style=ft.TextThemeStyle.TITLE_LARGE),
            )
            for one_add in add_dict:
                # 小标题，区分原文、译文、邵雍
                column_element.controls.append(
                    ft.Text(value=one_add,theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
                )
                try:
                    column_element.controls.append(
                        ft.Text(value=mean[index_dict[one_index]][add_dict[one_add]][0],theme_style=ft.TextThemeStyle.BODY_SMALL),
                    )
                except IndexError as e:
                    column_element.controls.append(
                        ft.Text(value="/",theme_style=ft.TextThemeStyle.BODY_SMALL),
                    )
                
        info = ft.Card(
            content=ft.Container(content=column_element)
        )
        result_mean_container.controls=[info,]
        result_mean_container.visible = True
        result_mean_container.update()
    
    def calculator(data,localvar):
        
        # RESULT_RELEATION_SIZE = 20
        # RESULT_LITTEL_TEXT_STYLE = ft.TextStyle(size=10)
        # RESULT_SYMBOL_STYLE = ft.TextStyle(size=50,height=0.72)
        # RESULT_TEXT_SIZE = 30
        result_releation_size = 10
        result_64gua_name_size = 30
        result_partname_size = 10
        result_partsymbol_size = 50
        result_partsymbol_height = 0.720
        
        meihuaobj = MeiHuaCalc(**state)
        res = meihuaobj.calclator()
        gua_obj_dict = {
            '本卦':res.self_gua,
            '互卦':res.hugua,
            '变卦':res.biangua
        }
        gua_name = ""
        part = {
            'upper':{},
            "lower":{}
        }
        
        res_list = []
        
        for one_gua in gua_obj_dict.keys():
            obj = gua_obj_dict[one_gua]
            gua_name = obj.name
            # 设置体用相互关系
            element_index,element_relation = res.check_element_kill(obj.upper.nature,obj.lower.nature,res.change_gua_index)
            for one_part_str in part.keys():
                one_part = getattr(obj,one_part_str)
                part[one_part_str]['symbol'] = one_part.symbol
                part[one_part_str]['color'] = NATURE_COLOR[one_part.nature]
                part[one_part_str]['name'] = f"{one_part.name}({one_part.attribute})"
            
            upper = part['upper']
            lower = part['lower']
            gua_symbol = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(spans=[
                            ft.TextSpan(spans=[ # 统一颜色
                            ft.TextSpan(text=upper['name'],style=ft.TextStyle(size=result_partname_size)),                                              # bengua_upper_name,
                            ft.TextSpan(text=upper['symbol'],style=ft.TextStyle(size=result_partsymbol_size,height=result_partsymbol_height)),      #bengua_upper
                            ],style=ft.TextStyle(color=upper['color'])),
                        ]),
                        ft.Text(spans=[
                            ft.TextSpan(spans=[ # 统一颜色故增加外包span
                            ft.TextSpan(text=lower['name'],style=ft.TextStyle(size=result_partname_size)),                                          #bengua_lower_name,
                            ft.TextSpan(text=lower['symbol'],style=ft.TextStyle(size=result_partsymbol_size,height=result_partsymbol_height)),      #bengua_lower
                            ],style=ft.TextStyle(color=lower['color'])),
                        ]),
                    ],spacing=0,expand=0
                )
            )
            gua_all = ft.Card(content=ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(value=f"{one_gua}:{gua_name}",size=result_64gua_name_size),
                            gua_symbol,
                            ft.Text(value=element_relation,size=result_releation_size)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    on_click = select_gua,
                    key=(obj.binary_str,res.change_gua_index)
                ),
                col={"xs": 12, "md": 8, "lg": 4},
            )
            
            res_list.append(gua_all)

        result_container.controls = [
            ft.Text(value=meihuaobj.calc_info),
            ft.ResponsiveRow(res_list,run_spacing={'xs':8},alignment=ft.MainAxisAlignment.SPACE_AROUND)
        ]
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
    result_container = ft.Column(
        horizontal_alignment=ft.MainAxisAlignment.CENTER
    ) 
    
    # 卦意显示区域
    result_mean_container = ft.Column(
        horizontal_alignment=ft.MainAxisAlignment.START
    )

    
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
            result_container,
            result_mean_container,
        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )
    page.update()
    
    # # 初始更新界面
    # update_input_visibility()

if __name__ == "__main__":
    ft.app(target=main)