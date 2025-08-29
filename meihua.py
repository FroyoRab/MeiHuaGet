import bagua
from zhdate import ZhDate
from datetime import datetime

# 地支天干
DIZHI12 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
TIANGAN10 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]


class MeiHuaCalc():
    self_gua:bagua.Gua64 = None
    
    calc_type = -1
    # 0 - datetime
    # 1 - number
    # 2 - number and time
    # 3 - chinese char
    # 4 - upper hexgram and time
    
    # datetime
    time:int = -1
    year:int = -1
    month:int = -1
    day:int = -1
    
    # random number
    number:int = -1
    
    # chinese char
    ch_char:str = ""
    
    # upper hexgram index (从1计数)
    upper_index:int = -1
    
    def __init__(self,*args, **kwargs):
        arg_keys = kwargs.keys()
        if 'date' in arg_keys: 
            self.__datetime_init__(**kwargs)
            self.calc_type = 0
            
        if 'number' in arg_keys:
            self.__random_num_init__(**kwargs)
            self.calc_type = 1
            if 'time' in arg_keys:
                self.__time_init__(**kwargs)
                self.calc_type = 2
        
        if 'chinesechar' in arg_keys:
            self.__chinese_char_init__(**kwargs)
            self.calc_type = 3
        
        if 'upper_hexgram' in arg_keys:
            self.__upper_hexgram_init__(**kwargs)
            self.__time_init__(**kwargs)    
        
        
    @staticmethod
    def time2lunatime(hour:int)->str:
        index = (hour + 1) // 2
        return (index % 12) + 1
            
    def __datetime_init__(self,date,time,islunardate:bool=False,uselunar:bool=True):
        """_summary_

        Args:
            lunadate (str): "%Y-%m-%d"
            lunatime (str): 12:12 | 子丑寅卯辰巳午未申酉戌亥
        """
        self.__time_init__(time,islunardate,uselunar)
        if uselunar:
            lunar_date = None
            if islunardate :
                if type(date)==ZhDate:
                    lunar_date = date
                if type(date) == str and '-' in date:
                    year,mouth,day = date.split("-")
                    lunar_date = ZhDate(int(year),int(mouth),int(day))
            elif not islunardate and type(date) == str and '-' in date:
                year,month,day = date.split("-")
                lunar_date = ZhDate.from_datetime(datetime(int(year),int(month),int(day)))
            else:
                raise ValueError(f"给到的date不是合法数值(Zhdate or %Y-%m-%d),或逻辑错误。")

            self.day = lunar_date.lunar_day
            self.month = lunar_date.lunar_month
            self.year = (lunar_date.lunar_year - 1996 + 36) % 12
        else:
            if type(date)==str and '-' in date:
                self.day,self.month,self.year = date.split("-")
            else:ValueError(f"给到的date不是合法数值(%Y-%m-%d),或逻辑错误。")
        
    def __random_num_init__(self,num:str,useNumberValue:bool=True):
        if useNumberValue:
            if num.isalnum():
                self.number = int(num)
            else:
                raise ValueError("提供的数字非法")
        else:
            self.number = sum(list(num))
        
    def __time_init__(self,time:str,islunartime:bool,uselunar:bool):
        if uselunar:
            # 如果直接是地支就返回数值
            if islunartime:
                if time in DIZHI12:
                    self.time = DIZHI12.index(time)+1
                    return
                else: raise ValueError(f'给到的不是地支{time}')
            # 其他进行分割取小时
            if ":" in time :
                time = time.split(":")[0]
            if time.isalnum():
                hour = int(time)
            else: raise ValueError(f"给到的time不是合法数值{time}")                
            # 返回地支的数值
            self.time = MeiHuaCalc.time2lunatime(hour)
        else:
            # 不用地支则将所有数值相加
            if type(time)==str and ':' in time:
                self.time = sum([int(x) for x in time.split(':')])
            else: raise ValueError(f"给到的time不是合法数值{time}")
            
    def __chinese_char_init__(self,ch_char:str):
        self.ch_char = ch_char
        
    def __upper_hexgram_init__(self,upper_hexgram:str):
        self.upper_index = bagua.Gua.index(upper_hexgram)
        
    def calclator(self):
        if self.calc_type == -1:
            raise ValueError(f"计算方式未成功设置")
        calc_check_dict = [
            [self.time, self.day, self.month, self.year],   # 0 - datetime
            [self.number,],                               # 1 - number
            [self.number, self.time],                     # 2 - number and time
            [self.ch_char,],                              # 3 - chinese char
            [self.upper_index, self.time],                # 4 - upper hexgram and time
        ]
        
        # 确认依赖
        assert not [x for x in calc_check_dict[self.calc_type] if x == -1 or x == ""],'计算所需依赖为空'
        
        if self.calc_type == 0:
            date_sum = self.year + self.month + self.day
            upper = date_sum % 8 or 8
            lower = (date_sum + self.time) % 8 or 8
            changer = (date_sum + self.time) % 6 or 6
            self.self_gua = bagua.Gua64(upper,lower,changer)
            return self.self_gua



# class MeiHuaState:
#     def __init__(self):
#         self.input_method = "lunar_date"
#         self.lunar_year = -1
#         self.lunar_month = -1
#         self.lunar_day = -1
#         self.time_period = -1
#         self.dizhi_time_input = False
#         self.random_numbers = -1
#         self.chinese_chars = ""
#         self.upper_trigram = -1
#         self.lower_trigram = -1
#         self.selected_time_period = -1
#         self.result = {}
#         self.show_result = False

#     def set_lunar(self, e):
#         value = e.control.value
#         try:
#             luna_date = ZhDate.from_datetime(datetime.strptime(value, '%Y-%m-%d'))
#             self.lunar_day = luna_date.lunar_day
#             self.lunar_month = luna_date.lunar_month
#             self.lunar_year = (luna_date.lunar_year - 1996 + 36) % 12
#         except:
#             pass

#     def set_input_method(self, e):
#         self.input_method = INPUT_METHOD[e.control.value]
#         self.show_result = False

#     def set_input_time_type(self, e):
#         self.dizhi_time_input = (e.control.value == "地支")

#     def set_time_period(self, e):
#         value = e.control.value
#         if ":" in value:
#             hour = int(value.split(":")[0]) % 24
#             index = (hour + 1) // 2
#             self.time_period = (index % 12) + 1
#         elif value in DIZHI12:
#             self.time_period = DIZHI12.index(value) + 1

#     def set_random_numbers(self, e):
#         try:
#             self.random_numbers = int(e.control.value)
#         except:
#             pass

#     def set_chinese_chars(self, e):
#         self.chinese_chars = e.control.value

#     def set_upper_trigram(self, e):
#         upper_name = e.control.value.split(":")[0]
#         self.upper_trigram = EIGHT_HEXGRAMS_VALUE[upper_name]

#     def calculate(self, e):
#         calc_func = {
#             'lunar_date': {
#                 'func': self.calculate_from_lunar_date,
#                 'check': [
#                     self.lunar_day,
#                     self.lunar_month,
#                     self.lunar_year
#                 ]
#             },
#             'random_numbers': {
#                 'func': self.calculate_from_random_numbers,
#                 'check': [
#                     self.random_numbers
#                 ]
#             },
#             'number_with_time': {
#                 'func': self.calculate_from_number_with_time,
#                 'check': [
#                     self.random_numbers,
#                     self.time_period
#                 ]
#             },
#             'chinese_chars': {
#                 'func': self.calculate_from_chinese_chars,
#                 'check': [
#                     self.chinese_chars
#                 ]
#             },
#             'upper_hexgram_with_time': {
#                 'func': self.calculate_from_upper_hexgram_with_time,
#                 'check': [
#                     self.upper_trigram,
#                     self.time_period
#                 ]
#             },
#         }
        
#         try:
#             calc_type = calc_func[self.input_method]
#             check_list = calc_type["check"]
#             if any(x == -1 or x == "" or x == 0 for x in check_list):
#                 raise ValueError('所需值为空')
#             else:
#                 calc_type['func']()
#         except Exception as ex:
#             self.result = {"error": f"计算错误: {str(ex)}"}
#             self.show_result = True

#     def calculate_from_lunar_date(self):
#         date_sum = self.lunar_year + self.lunar_month + self.lunar_day
#         upper_num = date_sum % 8 or 8
#         hour_num = self.time_period
#         time_sum = date_sum + hour_num
#         lower_num = time_sum % 8 or 8
#         moving_yao = time_sum % 6 or 6
#         self.generate_result(upper_num, lower_num, moving_yao)

#     def calculate_from_random_numbers(self):
#         numbers = re.findall(r'\d+', str(self.random_numbers))
#         if not numbers:
#             self.result = {"error": "请输入有效的数字"}
#             self.show_result = True
#             return
        
#         num1 = int(numbers[0]) if len(numbers) > 0 else 1
#         num2 = int(numbers[1]) if len(numbers) > 1 else 1
#         num3 = int(numbers[2]) if len(numbers) > 2 else 1
        
#         upper_num = num1 % 8 or 8
#         lower_num = num2 % 8 or 8
#         moving_yao = num3 % 6 or 6
        
#         self.generate_result(upper_num, lower_num, moving_yao)

#     def calculate_from_number_with_time(self):
#         numbers = re.findall(r'\d+', str(self.random_numbers))
#         if not numbers:
#             self.result = {"error": "请输入有效的数字"}
#             self.show_result = True
#             return
        
#         num = int(numbers[0])
#         upper_num = (num // 10) % 8 or 8
#         lower_num = (num % 10) % 8 or 8
#         moving_yao = (num + self.time_period) % 6 or 6
#         self.generate_result(upper_num, lower_num, moving_yao)

#     def calculate_from_chinese_chars(self):
#         if not self.chinese_chars:
#             self.result = {"error": "请输入中文字符"}
#             self.show_result = True
#             return
        
#         stroke_count = 0
#         for char in self.chinese_chars:
#             stroke_count += ord(char) % 10 + 1
        
#         upper_num = stroke_count % 8 or 8
#         lower_num = (stroke_count + len(self.chinese_chars)) % 8 or 8
#         moving_yao = (stroke_count + len(self.chinese_chars)) % 6 or 6
        
#         self.generate_result(upper_num, lower_num, moving_yao)

#     def calculate_from_upper_hexgram_with_time(self):
#         upper_num = self.upper_trigram
#         lower_num = self.lower_trigram
#         moving_yao = (upper_num + lower_num + self.time_period) % 6 or 6
#         self.generate_result(upper_num, lower_num, moving_yao)

#     def generate_result(self, upper_num, lower_num, moving_yao):
#         upper_trigram = EIGHT_TRIGRAMS[upper_num]
#         lower_trigram = EIGHT_TRIGRAMS[lower_num]
        
#         trigram_bin = hexgrams2bin(upper_num, lower_num)
#         mutual_upper_num = bin2hexgram(trigram_bin[1:4])
#         mutual_lower_num = bin2hexgram(trigram_bin[2:5])
#         mutual_upper_trigram = mutual_upper_num['value']
#         mutual_lower_trigram = mutual_lower_num['value']
        
#         change_trigram_bin = list(trigram_bin)
#         change_trigram_bin[6-moving_yao] = '0' if trigram_bin[6-moving_yao]=='1' else '1'
#         change_trigram_bin = "".join(change_trigram_bin)
        
#         change_upper_trigram = bin2hexgram(change_trigram_bin[0:3])['value']
#         change_lower_trigram = bin2hexgram(change_trigram_bin[3:6])['value']
        
#         body_trigram = lower_trigram if moving_yao <= 3 else upper_trigram
#         use_trigram = upper_trigram if moving_yao <= 3 else lower_trigram
        
#         five_element_kill = '金木土水火'
#         body_element = five_element_kill.index(body_trigram["nature"]) 
#         use_element = five_element_kill.index(use_trigram["nature"]) 
        
#         value = body_element - use_element
#         if value < 0:
#             value = value + 5
        
#         element_relation_dict = {
#             0: '体用相和',
#             1: '用克体',
#             2: '体生用',
#             3: '用生体',
#             4: '体克用',
#         }
#         element_relation = element_relation_dict[value]
        
#         self.result = {
#             "original_hexagram": {
#                 "upper": upper_trigram,
#                 "lower": lower_trigram,
#                 "name": f"{upper_trigram['name']}为{upper_trigram['attribute']} {lower_trigram['name']}为{lower_trigram['attribute']}",
#                 "full_name": f"{upper_trigram['attribute']}{lower_trigram['attribute']}"
#             },
#             "mutual_hexagram": {
#                 "upper": mutual_upper_trigram,
#                 "lower": mutual_lower_trigram,
#                 "name": f"{mutual_upper_trigram['name']}为{mutual_upper_trigram['attribute']} {mutual_lower_trigram['name']}为{mutual_lower_trigram['attribute']}"
#             },
#             "changed_hexagram": {
#                 "upper": change_upper_trigram,
#                 "lower": change_lower_trigram,
#                 "name": f"{change_upper_trigram['name']}为{change_upper_trigram['attribute']} {change_lower_trigram['name']}为{change_lower_trigram['attribute']}"
#             },
#             "moving_yao": moving_yao,
#             "body_use": {
#                 "body": body_trigram,
#                 "use": use_trigram,
#                 "relation": element_relation
#             }
#         }
#         self.show_result = True