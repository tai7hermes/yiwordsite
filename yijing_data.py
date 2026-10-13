# YiWord Hexagram Data (H01-H64)
# Each hexagram: id, name_zh_hant, name_en, unicode, upper_trigram, lower_trigram
# Trigram codes: qian(☰), dui(☱), li(☲), zhen(☳), xun(☴), kan(☵), gen(☶), kun(☷)

HEXAGRAMS = [
    # (id, name_zh_hant, name_zh_hans, name_en, unicode, upper, lower, judgment_summary)
    ("H01", "乾", "乾", "Qian / The Creative", "䷀", "qian", "qian", "元亨利貞"),
    ("H02", "坤", "坤", "Kun / The Receptive", "䷁", "kun", "kun", "元亨，利牝馬之貞"),
    ("H03", "屯", "屯", "Zhun / Difficulty at the Beginning", "䷂", "kan", "zhen", "元亨利貞，勿用有攸往"),
    ("H04", "蒙", "蒙", "Meng / Youthful Folly", "䷃", "gen", "kan", "亨。匪我求童蒙，童蒙求我"),
    ("H05", "需", "需", "Xu / Waiting", "䷄", "kan", "qian", "有孚，光亨，貞吉"),
    ("H06", "訟", "讼", "Song / Conflict", "䷅", "qian", "kan", "有孚窒惕，中吉，終凶"),
    ("H07", "師", "师", "Shi / The Army", "䷆", "kun", "kan", "貞，丈人吉，無咎"),
    ("H08", "比", "比", "Bi / Holding Together", "䷇", "kan", "kun", "吉。原筮元永貞，無咎"),
    ("H09", "小畜", "小畜", "Xiao Xu / Small Taming", "䷈", "xun", "qian", "亨。密雲不雨"),
    ("H10", "履", "履", "Lü / Treading", "䷉", "qian", "dui", "履虎尾，不咥人，亨"),
    ("H11", "泰", "泰", "Tai / Peace", "䷊", "kun", "qian", "小往大來，吉，亨"),
    ("H12", "否", "否", "Pi / Standstill", "䷋", "qian", "kun", "否之匪人，不利君子貞"),
    ("H13", "同人", "同人", "Tong Ren / Fellowship", "䷌", "qian", "li", "同人于野，亨"),
    ("H14", "大有", "大有", "Da You / Great Possession", "䷍", "li", "qian", "元亨"),
    ("H15", "謙", "谦", "Qian / Modesty", "䷎", "kun", "gen", "亨，君子有終"),
    ("H16", "豫", "豫", "Yu / Enthusiasm", "䷏", "zhen", "kun", "利建侯行師"),
    ("H17", "隨", "随", "Sui / Following", "䷐", "dui", "zhen", "元亨利貞，無咎"),
    ("H18", "蠱", "蛊", "Gu / Work on the Decayed", "䷑", "gen", "xun", "元亨，利涉大川"),
    ("H19", "臨", "临", "Lin / Approach", "䷒", "kun", "dui", "元亨，利貞"),
    ("H20", "觀", "观", "Guan / Contemplation", "䷓", "xun", "kun", "盥而不薦，有孚顒若"),
    ("H21", "噬嗑", "噬嗑", "Shi He / Biting Through", "䷔", "li", "zhen", "亨。利用獄"),
    ("H22", "賁", "贲", "Bi / Grace", "䷕", "gen", "li", "亨。小利有攸往"),
    ("H23", "剝", "剥", "Bo / Splitting Apart", "䷖", "gen", "kun", "不利有攸往"),
    ("H24", "復", "复", "Fu / Return", "䷗", "kun", "zhen", "亨。出入無疾"),
    ("H25", "無妄", "无妄", "Wu Wang / Innocence", "䷘", "qian", "zhen", "元亨，利貞"),
    ("H26", "大畜", "大畜", "Da Xu / Great Taming", "䷙", "gen", "qian", "利貞。不家食吉"),
    ("H27", "頤", "颐", "Yi / Nourishment", "䷚", "gen", "zhen", "貞吉。觀頤，自求口實"),
    ("H28", "大過", "大过", "Da Guo / Great Exceeding", "䷛", "dui", "xun", "棟橈，利有攸往，亨"),
    ("H29", "坎", "坎", "Kan / The Abysmal", "䷜", "kan", "kan", "習坎，有孚，維心亨"),
    ("H30", "離", "离", "Li / The Clinging", "䷝", "li", "li", "利貞，亨。畜牝牛吉"),
    ("H31", "咸", "咸", "Xian / Influence", "䷞", "dui", "gen", "亨，利貞，取女吉"),
    ("H32", "恆", "恒", "Heng / Duration", "䷟", "zhen", "xun", "亨，無咎，利貞"),
    ("H33", "遯", "遁", "Dun / Retreat", "䷠", "qian", "gen", "亨，小利貞"),
    ("H34", "大壯", "大壮", "Da Zhuang / Great Power", "䷡", "zhen", "qian", "利貞"),
    ("H35", "晉", "晋", "Jin / Progress", "䷢", "li", "kun", "康侯用錫馬蕃庶，晝日三接"),
    ("H36", "明夷", "明夷", "Ming Yi / Darkening Light", "䷣", "kun", "li", "利艱貞"),
    ("H37", "家人", "家人", "Jia Ren / The Family", "䷤", "xun", "li", "利女貞"),
    ("H38", "睽", "睽", "Kui / Opposition", "䷥", "li", "dui", "小事吉"),
    ("H39", "蹇", "蹇", "Jian / Obstruction", "䷦", "kan", "gen", "利西南，不利東北"),
    ("H40", "解", "解", "Xie / Deliverance", "䷧", "zhen", "kan", "利西南，無所往"),
    ("H41", "損", "损", "Sun / Decrease", "䷨", "gen", "dui", "有孚，元吉，無咎"),
    ("H42", "益", "益", "Yi / Increase", "䷩", "xun", "zhen", "利有攸往，利涉大川"),
    ("H43", "夬", "夬", "Guai / Breakthrough", "䷪", "dui", "qian", "揚于王庭，孚號有厲"),
    ("H44", "姤", "姤", "Gou / Coming to Meet", "䷫", "qian", "xun", "女壯，勿用取女"),
    ("H45", "萃", "萃", "Cui / Gathering Together", "䷬", "dui", "kun", "亨。王假有廟"),
    ("H46", "升", "升", "Sheng / Pushing Upward", "䷭", "kun", "xun", "元亨，用見大人"),
    ("H47", "困", "困", "Kun / Oppression", "䷮", "dui", "kan", "亨，貞，大人吉"),
    ("H48", "井", "井", "Jing / The Well", "䷯", "kan", "xun", "改邑不改井，無喪無得"),
    ("H49", "革", "革", "Ge / Revolution", "䷰", "dui", "li", "巳日乃孚，元亨利貞"),
    ("H50", "鼎", "鼎", "Ding / The Caldron", "䷱", "li", "xun", "元吉，亨"),
    ("H51", "震", "震", "Zhen / The Arousing", "䷲", "zhen", "zhen", "亨。震來虩虩"),
    ("H52", "艮", "艮", "Gen / Keeping Still", "䷳", "gen", "gen", "艮其背，不獲其身"),
    ("H53", "漸", "渐", "Jian / Development", "䷴", "xun", "gen", "女歸吉，利貞"),
    ("H54", "歸妹", "归妹", "Gui Mei / Marrying Maiden", "䷵", "zhen", "dui", "征凶，無攸利"),
    ("H55", "豐", "丰", "Feng / Abundance", "䷶", "zhen", "li", "亨。王假之"),
    ("H56", "旅", "旅", "Lü / The Wanderer", "䷷", "li", "gen", "小亨，旅貞吉"),
    ("H57", "巽", "巽", "Xun / The Gentle", "䷸", "xun", "xun", "小亨，利有攸往"),
    ("H58", "兌", "兑", "Dui / The Joyous", "䷹", "dui", "dui", "亨，利貞"),
    ("H59", "渙", "涣", "Huan / Dispersion", "䷺", "xun", "kan", "亨。王假有廟"),
    ("H60", "節", "节", "Jie / Limitation", "䷻", "kan", "dui", "亨。苦節不可貞"),
    ("H61", "中孚", "中孚", "Zhong Fu / Inner Truth", "䷼", "xun", "dui", "豚魚吉，利涉大川"),
    ("H62", "小過", "小过", "Xiao Guo / Small Exceeding", "䷽", "zhen", "gen", "亨，利貞"),
    ("H63", "既濟", "既济", "Ji Ji / After Completion", "䷾", "kan", "li", "亨，利貞"),
    ("H64", "未濟", "未济", "Wei Ji / Before Completion", "䷿", "li", "kan", "亨。小狐汔濟"),
]

TRIGRAMS = {
    "qian": {"name": "乾", "symbol": "☰", "nature": "天", "unicode": "U+2630"},
    "dui":  {"name": "兌", "symbol": "☱", "nature": "澤", "unicode": "U+2631"},
    "li":   {"name": "離", "symbol": "☲", "nature": "火", "unicode": "U+2632"},
    "zhen": {"name": "震", "symbol": "☳", "nature": "雷", "unicode": "U+2633"},
    "xun":  {"name": "巽", "symbol": "☴", "nature": "風", "unicode": "U+2634"},
    "kan":  {"name": "坎", "symbol": "☵", "nature": "水", "unicode": "U+2635"},
    "gen":  {"name": "艮", "symbol": "☶", "nature": "山", "unicode": "U+2636"},
    "kun":  {"name": "坤", "symbol": "☷", "nature": "地", "unicode": "U+2637"},
}

# Wing (十翼) data
WINGS = [
    ("W01", "TUAN-U", "彖傳上", "彖传上", "Tuan Zhuan Shang", "解釋卦名、卦辭與全卦義理（上）"),
    ("W02", "TUAN-L", "彖傳下", "彖传下", "Tuan Zhuan Xia", "解釋卦名、卦辭與全卦義理（下）"),
    ("W03", "XIANG-U", "象傳上", "象传上", "Xiang Zhuan Shang", "以大象解釋全卦，以小象解釋各爻（上）"),
    ("W04", "XIANG-L", "象傳下", "象传下", "Xiang Zhuan Xia", "以大象解釋全卦，以小象解釋各爻（下）"),
    ("W05", "XICI-U", "繫辭傳上", "系辞传上", "Xi Ci Zhuan Shang", "討論陰陽、變化、象數與聖人之道（上）"),
    ("W06", "XICI-L", "繫辭傳下", "系辞传下", "Xi Ci Zhuan Xia", "討論陰陽、變化、象數與聖人之道（下）"),
    ("W07", "WENYAN", "文言傳", "文言传", "Wen Yan Zhuan", "集中闡釋乾坤兩卦的德性與實踐"),
    ("W08", "SHUOGUA", "說卦傳", "说卦传", "Shuo Gua Zhuan", "說明八卦的象徵、方位、自然及人事配屬"),
    ("W09", "XUGUA", "序卦傳", "序卦传", "Xu Gua Zhuan", "解釋六十四卦的排列次序"),
    ("W10", "ZAGUA", "雜卦傳", "杂卦传", "Za Gua Zhuan", "用對舉和簡語比較卦義"),
]

if __name__ == "__main__":
    print(f"Hexagrams: {len(HEXAGRAMS)}")
    print(f"Trigrams: {len(TRIGRAMS)}")
    print(f"Wings: {len(WINGS)}")
    print(f"Total content units (hexagrams): {len(HEXAGRAMS) * 7} (6 爻 + 1 卦辭 per hexagram)")
    print(f"Total with use lines: {len(HEXAGRAMS) * 7 + 2} (乾用九 + 坤用六)")
