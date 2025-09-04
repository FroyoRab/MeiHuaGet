import copy
import json

# 八卦定义
EIGHT_TRIGRAMS = [
    {"index":1, "name": "乾", "symbol": "☰", "nature": "金", "direction": "西北", "attribute": "天", "bin_str": '111'},
    {"index":2, "name": "兑", "symbol": "☱", "nature": "金", "direction": "西", "attribute": "泽", "bin_str": '110'},
    {"index":3, "name": "离", "symbol": "☲", "nature": "火", "direction": "南", "attribute": "火", "bin_str": '101'},
    {"index":4, "name": "震", "symbol": "☳", "nature": "木", "direction": "东", "attribute": "雷", "bin_str": '100'},
    {"index":5, "name": "巽", "symbol": "☴", "nature": "木", "direction": "东南", "attribute": "风", "bin_str": '011'},
    {"index":6, "name": "坎", "symbol": "☵", "nature": "水", "direction": "北", "attribute": "水", "bin_str": '010'},
    {"index":7, "name": "艮", "symbol": "☶", "nature": "土", "direction": "东北", "attribute": "山", "bin_str": '001'},
    {"index":8, "name": "坤", "symbol": "☷", "nature": "土", "direction": "西南", "attribute": "地", "bin_str": '000'},
]

ALL64GUA = {
    "000000":{"name":"坤为地","symbol":"䷁"},
    "000001":{"name":"地雷复","symbol":"䷗"},
    "000010":{"name":"地水师","symbol":"䷆"},
    "000011":{"name":"地泽临","symbol":"䷒"},
    "000100":{"name":"地山谦","symbol":"䷎"},
    "000101":{"name":"地火明夷","symbol":"䷣"},
    "000110":{"name":"地风升","symbol":"䷭"},
    "000111":{"name":"地天泰","symbol":"䷊"},
    "001000":{"name":"雷地豫","symbol":"䷏"},
    "001001":{"name":"震为雷","symbol":"䷲"},
    "001010":{"name":"雷水解","symbol":"䷧"},
    "001011":{"name":"雷泽归妹","symbol":"䷵"},
    "001100":{"name":"雷山小过","symbol":"䷽"},
    "001101":{"name":"雷火丰","symbol":"䷶"},
    "001110":{"name":"雷风恒","symbol":"䷟"},
    "001111":{"name":"雷天大壮","symbol":"䷡"},
    "010000":{"name":"水地比","symbol":"䷇"},
    "010001":{"name":"水雷屯","symbol":"䷂"},
    "010010":{"name":"坎为水","symbol":"䷜"},
    "010011":{"name":"水泽节","symbol":"䷻"},
    "010100":{"name":"水山蹇","symbol":"䷦"},
    "010101":{"name":"水火既济","symbol":"䷾"},
    "010110":{"name":"水风井","symbol":"䷯"},
    "010111":{"name":"水天需","symbol":"䷄"},
    "011000":{"name":"泽地萃","symbol":"䷬"},
    "011001":{"name":"泽雷随","symbol":"䷐"},
    "011010":{"name":"泽水困","symbol":"䷮"},
    "011011":{"name":"兑为泽","symbol":"䷹"},
    "011100":{"name":"泽山咸","symbol":"䷞"},
    "011101":{"name":"泽火革","symbol":"䷰"},
    "011110":{"name":"泽风大过","symbol":"䷛"},
    "011111":{"name":"泽天夬","symbol":"䷪"},
    "100000":{"name":"山地剥","symbol":"䷖"},
    "100001":{"name":"山雷颐","symbol":"䷚"},
    "100010":{"name":"山水蒙","symbol":"䷃"},
    "100011":{"name":"山泽损","symbol":"䷨"},
    "100100":{"name":"艮为山","symbol":"䷳"},
    "100101":{"name":"山火贲","symbol":"䷕"},
    "100110":{"name":"山风蛊","symbol":"䷑"},
    "100111":{"name":"山天大蓄","symbol":"䷙"},
    "101000":{"name":"火地晋","symbol":"䷢"},
    "101001":{"name":"火雷噬嗑","symbol":"䷔"},
    "101010":{"name":"火水未济","symbol":"䷿"},
    "101011":{"name":"火泽睽","symbol":"䷥"},
    "101100":{"name":"火山旅","symbol":"䷷"},
    "101101":{"name":"离为火","symbol":"䷝"},
    "101110":{"name":"火风鼎","symbol":"䷱"},
    "101111":{"name":"火天大有","symbol":"䷍"},
    "110000":{"name":"风地观","symbol":"䷓"},
    "110001":{"name":"风雷益","symbol":"䷩"},
    "110010":{"name":"风水涣","symbol":"䷺"},
    "110011":{"name":"风泽中孚","symbol":"䷼"},
    "110100":{"name":"风山渐","symbol":"䷴"},
    "110101":{"name":"风火家人","symbol":"䷤"},
    "110110":{"name":"巽为风","symbol":"䷸"},
    "110111":{"name":"风天小蓄","symbol":"䷈"},
    "111000":{"name":"天地否","symbol":"䷋"},
    "111001":{"name":"天雷无妄","symbol":"䷘"},
    "111010":{"name":"天水讼","symbol":"䷅"},
    "111011":{"name":"天泽履","symbol":"䷉"},
    "111100":{"name":"天山遁","symbol":"䷠"},
    "111101":{"name":"天火同人","symbol":"䷌"},
    "111110":{"name":"天风姤","symbol":"䷫"},
    "111111":{"name":"乾为天","symbol":"䷀"}
}

GUA_MEAN = {}

# 64卦卦义
# from zhouyi.cc
with open('64gua_mean_.json','r',encoding='utf8') as files:
    GUA_MEAN = json.loads(files.read())
        
# with open('./64gua_mean_.json','w',encoding='utf-8') as files: 
#     files.write(json.dumps(ALL64GUA_DATA,indent=4,ensure_ascii=False))

# [{x:f"\u4DC{index}".encode('utf-8')} for index,x in enumerate(ALL64GUA.keys())]


class Gua():
    index = -1
    name = ""
    symbol = ""
    nature = ""
    direction = ""
    bin_str = ""
    attribute = ""
    # class _calc():
    #     bagua_bin = ""
    #     calc_index = -1
    # calc_info = _calc()
    
    def __init__(self,*args, **kwargs):
        for one_arg in kwargs.keys():
            self.__setattr__(one_arg,kwargs[one_arg])
        # self.calc_info.bagua_bin = self.bin_str
        # self.calc_info.calc_index = 8-self.index
            
    @staticmethod
    def bin2hexgram(binstr) -> int:
        index = 8 - int(binstr[::-1], 2)
        return index
    
    def index(upper_name:str) ->int:
        return [x['name'] for x in EIGHT_TRIGRAMS.values()].index(upper_name)+1
    
    def change_index(self,index:int) -> str:
        """_summary_
        Returns:
            str: changed binary str
        """
        # [::-1]翻转因为index变卦从下往上数,	所以是从右往左数
        bin_list = list(self.bin_str)[::-1]
        bin_list[index-1] = '1' if bin_list[index-1]=='0' else "0"
        return "".join(bin_list[::-1])
        
        
        
BAGUA = [Gua(**x) for x in EIGHT_TRIGRAMS]

class _Gua64():
    upper:Gua
    lower:Gua
    binary_str:str = ""
    name:str = ""
    symbol:str = ""
    
    def __init__(self,upper:Gua,lower:Gua):
        # global GUA64_ALL
        # nonlocal G
        self.upper = upper
        self.lower = lower
        self.binary_str = self.__get_bin_str()
        self.name = ALL64GUA[self.binary_str]['name']
        self.symbol = ALL64GUA[self.binary_str]['symbol']
        
    def __get_bin_str(self):
        return f"{self.lower.bin_str}{self.upper.bin_str}"[::-1]
        
    def __str__(self):
        return f"{self.name}\t{self.symbol}"
    

class Gua64():
    # binary_str = ""
    self_gua = _Gua64
    hugua:_Gua64
    biangua:_Gua64
    change_gua_index:int
    # element_relation_index:int
    # element_relation:str
    
    def __init__(self,upper_index,lower_index,change_index):
        self.self_gua = _Gua64(
            BAGUA[upper_index-1],
            BAGUA[lower_index-1]
        )
        self.__get_hu_gua()
        if change_index:
            self.set_change_gua(change_index)
            # self.__check_element_kill()
    
    def set_change_gua(self,change_index):
        change_gua = None
        if change_index > 3: change_gua = "upper"
        else: change_gua = 'lower'
        self.change_gua_index  = change_index
        
        change_gua_obj = getattr(self.self_gua,change_gua)
        change_gua_bin = change_gua_obj.change_index(change_index if change_gua=='lower' else change_index-3 )
        if change_gua=='upper':
            self.biangua = _Gua64(
                BAGUA[Gua.bin2hexgram(change_gua_bin)-1],
                Gua(**self.self_gua.lower.__dict__)
            )
        else:
            self.biangua = _Gua64(
                Gua(**self.self_gua.upper.__dict__),
                BAGUA[Gua.bin2hexgram(change_gua_bin)-1],
            )
        # self.__check_element_kill()

    @staticmethod
    def check_element_kill(upper_nature:str,lower_nature:str,change_yao_index:int):
        use_nature,body_nature = (lower_nature,upper_nature) if change_yao_index <= 3 else (upper_nature,lower_nature)
        # body_nature = upper_nature if change_yao_index <= 3 else lower_nature
        
        five_element_kill = '金木土水火'
        body_element = five_element_kill.index(body_nature) 
        use_element = five_element_kill.index(use_nature)
        
        value = body_element - use_element
        if value < 0:
            value = value + 5
        
        element_relation_dict = {
            0: '体用相和',
            1: '用克体',
            2: '体生用',
            3: '用生体',
            4: '体克用',
        }
        res_str = f"变爻在{change_yao_index}，"+\
            ("上{}下{}，" if change_yao_index<=3 else "下{}上{}，").format('体',"用")+\
            "体为{}用为{}".format(five_element_kill[body_element],five_element_kill[use_element])+\
            element_relation_dict[value]
            
        return value,res_str
            
    def __get_hu_gua(self):
        hu_upper = self.self_gua.binary_str[1:4]
        hu_lower = self.self_gua.binary_str[2:5]
        self.hugua = _Gua64(
            BAGUA[Gua.bin2hexgram(hu_upper)-1],
            BAGUA[Gua.bin2hexgram(hu_lower)-1]
        )

    def __str__(self):
        return f"本卦:{self.self_gua}\n互卦:{self.hugua}\n变卦:{self.biangua}"