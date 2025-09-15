import bagua
from zhdate import ZhDate
from datetime import datetime

# 地支天干
DIZHI12 = "子丑寅卯辰巳午未申酉戌亥"
TIANGAN10 = "甲乙丙丁戊己庚辛壬癸"


class MeiHuaCalc():
    self_gua:bagua.Gua64 = None
    calc_info:str = ""
    
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
    uselunar:bool
    
    # random number
    number1:int = -1
    number2:int = -1
    number3:int = -1
    
    # chinese char
    ch_char:str = ""
    
    # upper hexgram index (从1计数)
    upper_index:int = -1
    
    # tiyong
    
    
    def __init__(self,*args, **kwargs):
        arg_keys = kwargs.keys()
        if 'date' in arg_keys: 
            self.__datetime_init__(**kwargs)
            self.calc_type = 0
            
        if 'number1' in arg_keys:
            if 'number2' in arg_keys:
                self.__random_num_init__(**kwargs)
                self.calc_type = 1
            if 'time' in arg_keys:
                self.__number_time_init__(**kwargs)
                self.calc_type = 2
        
        if 'chinesechar' in arg_keys:
            self.__chinese_char_init__(**kwargs)
            self.calc_type = 3
        
        if 'upper_hexgram' in arg_keys:
            self.__upper_hexgram_init__(**kwargs)
            self.__number_time_init__(**kwargs)    
        
        
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
        self.__number_time_init__(time,islunardate,uselunar)
        self.uselunar = uselunar
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
                self.year,self.month,self.day = [int(x) for x in date.split("-")]
            else:ValueError(f"给到的date不是合法数值(%Y-%m-%d),或逻辑错误。")
        
    def __random_num_init__(self,number1:str,number2:str,number3:str=None,useNumberValue:bool=True):
        self.number1 = int(number1)
        self.number2 = int(number2)
        if number3.isalnum():
            self.number3 = int(number3)
        else: self.number3 = number3 # make none
            
        
    def __number_time_init__(self,number1:str,time:str):
        self.number1 = int(number1)
        if time in DIZHI12:
            self.time = DIZHI12.index(time)+1
            return
        # 其他进行分割取小时
        if ":" in time :
            time = time.split(":")[0]
        if time.isalnum():
            hour = int(time)
        else: raise ValueError(f"给到的time不是合法数值{time}")                
        self.time = MeiHuaCalc.time2lunatime(hour)
        # 返回地支的数值
            
    def __chinese_char_init__(self,ch_char:str):
        self.ch_char = ch_char
        
    def __upper_hexgram_init__(self,upper_hexgram:str):
        self.upper_index = bagua.Gua.index(upper_hexgram)
    
    @staticmethod
    def get_like(index:int=None,bin_str:str=None):
        like_dict = [
            "乾: 天、父、老人、官贵、头、骨、马、金宝、珠玉、水果、圆物、冠、镜、刚物、大赤色、水寒。",
            "兑：泽、少女、巫、舌、妾、肺、羊、毁折之物、带口之器、属金者、废缺之物、奴仆、婢。",
            "离：火、雉、日、目、电、霓霞、中女、甲胄、戈兵、文书、槁木、炉、兽、鳄龟蟹蚌、凡有壳之物、红赤紫色、花纹人、干燥物。",
            "震：雷、长男、足、发、龙、百虫、蹄、竹、萑苇、马鸣、馵足、的颡、稼、乐器之类、草木、青碧绿色、树、木核、柴、蛇。",
            "巽：风、长女、僧尼、鸡、股、百禽、百草、臼、香气、臭、绳、眼、羽毛、帆、扇、枝叶之类、仙道工匠、直物、工巧之器。",
            "坎：水、雨、雪、工、豕、中男、沟渎、弓轮、耳、血、月、盗、宫律、栋、丛棘、狐、蒺藜、桎梏、水族、鱼、盐、酒、醢、有核之物、黑色。",
            "艮：山、土、少男、童子、狗、手指、径路、门阙、果、蓏、阍寺、鼠、虎、狐、黔喙之属、木生之物、藤生之物、爪、鼻,黄色。",
            "坤：地、母、老妇、土、牛、金、布帛、文章、舆辇、方物、柄、黄色、瓦器、腹、裳、黑色、黍稷、书、米、谷。",
        ]
        index_like_dict = {}
        if bin_str:
            index_like_dict = {x['bin_str']:like_dict[index] for index,x in enumerate(bagua.EIGHT_TRIGRAMS)}
            return index_like_dict[bin_str]
        else: return like_dict[index]
    
    def calclator(self):
        if self.calc_type == -1:
            raise ValueError(f"计算方式未成功设置")
        calc_check_dict = [
            [self.time, self.day, self.month, self.year],   # 0 - datetime
            [self.number1,self.number2],       # 1 - number
            [self.number1, self.time],                     # 2 - number and time
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
            # self.self_gua = bagua.Gua64(upper,lower,changer)
            if self.uselunar:
                self.calc_info = f"{TIANGAN10[self.year-1]}年({self.year})，{DIZHI12[self.month-1]}月({self.month})，{self.day}日，{DIZHI12[self.time-1]}时({self.time})\n"
            else:
                self.calc_info = f"{self.year}年{self.month}月{self.day}日\n"
            self.calc_info += f"年月日和{date_sum}，{date_sum//8}X8 {(date_sum//8)*8}余{upper}，上卦为{bagua.EIGHT_TRIGRAMS[upper-1]['name']}\n"
            self.calc_info += f"年月日时和{date_sum+self.time}，{(date_sum+self.time)//8}X8 {((date_sum+self.time)//8)*8}余{lower}，下卦为{bagua.EIGHT_TRIGRAMS[lower-1]['name']}\n"
            self.calc_info += f"年月日时和{date_sum+self.time}，{(date_sum+self.time)//6}X6 {((date_sum+self.time)//6)*6}余{changer}"

        if self.calc_type == 1:
            upper = self.number1 % 8 or 8
            lower = self.number2 % 8 or 8
            self.calc_info = f"数{self.number1}为上卦，对8取余，{self.number1//8}X8 {(self.number1//8)*8}余{upper}\n"
            self.calc_info += f"数{self.number2}为下卦，对8取余，{self.number2//8}X8 {(self.number2//8)*8}余{lower}\n"
            
            if self.number3:
                changer = self.number3 % 6 or 6
                self.calc_info += f"数{self.number3}为变爻，对6取余，{self.number3//6}X6 {(self.number3//6)*6}余{changer}"
            else:
                changer = (upper + lower) % 6 or 6
                self.calc_info += f"数1+数2相加为{(upper + lower)}，对6取余，{(upper + lower)//6}X6 {((upper + lower)//6)*6}余{changer}"
            # self.calc_info += f"变爻为{['初','第二','第三','第四','第五','上'][changer-1]}爻"
            # self.self_gua = bagua.Gua64(upper,lower,changer)
        
        if self.calc_type == 2:
            upper = self.number1 % 8 or 8
            self.calc_info = f"数{self.number1}为上卦，对8取余，{self.number1//8}X8 {(self.number1//8)*8}余{upper}\n"
            
            lower = self.time % 8 or 8
            self.calc_info += f"{DIZHI12[self.time-1]}时({self.time})为上卦，对8取余，{self.number1//8}X8 {(self.number1//8)*8}余{upper}\n"
            
            changer = (self.number1 + self.time) % 6 or 6
            self.calc_info += f"数{self.number1}和{DIZHI12[self.time-1]}时({self.time})总数{(self.number1 + self.time)}，对86取余，{(self.number1 + self.time)//6}X6 {((self.number1 + self.time)//6)*6}余{changer}\n"
            
        self.calc_info += f"变爻为{['初','第二','第三','第四','第五','上'][changer-1]}爻"
            
        self.self_gua = bagua.Gua64(upper,lower,changer)
            
            
            


        # self.__check_element_kill()
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