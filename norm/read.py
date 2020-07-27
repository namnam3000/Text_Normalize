import re
from num2words import num2words
import string

def unit2words(input_str, output_str):
    # Units of information
    # input_str = input_str.replace('KB ', ' <MEASURE>KB</MEASURE> ')
    # input_str = input_str.replace('MB ', ' <MEASURE>MB</MEASURE> ')
    input_str = input_str.replace('GB ', ' <MEASURE>GB</MEASURE> ')
    input_str = input_str.replace('Gb ', ' <MEASURE>Gb</MEASURE> ')
    # input_str = input_str.replace('TB ', ' <MEASURE>TB</MEASURE> ')

    # 2G, 3G, etc
    input_str = input_str.replace(' 2G ', ' <MEASURE>2G</MEASURE> ')
    input_str = input_str.replace(' 3G ', ' <MEASURE>3G</MEASURE> ')
    input_str = input_str.replace(' 4G ', ' <MEASURE>4G</MEASURE> ')
    input_str = input_str.replace(' 5G ', ' <MEASURE>5G</MEASURE> ')

    # Units of frequency
    input_str = input_str.replace('GHz', ' <MEASURE>GHz</MEASURE> ')
    input_str = input_str.replace('MHz', ' <MEASURE>MHz</MEASURE> ')

    # Units of data-rate
    input_str = input_str.replace('Mbps', ' <MEASURE>Mbps</MEASURE> ')
    input_str = input_str.replace('Mb/s', ' <MEASURE>Mb/s</MEASURE> ')

    # Units of currency
    input_str = input_str.replace("đồng/", " <MEASURE>đồng/</MEASURE> ")
    input_str = input_str.replace("USD/", " <MEASURE>USD/</MEASURE> ")
    input_str = input_str.replace('đ ', ' <MEASURE>đ</MEASURE> ')
    input_str = input_str.replace('$', ' <MEASURE>$</MEASURE> ')
    input_str = input_str.replace('USD', ' <MEASURE>USD</MEASURE> ')
    input_str = input_str.replace('VNĐ', ' <MEASURE>VNĐ</MEASURE> ')
    input_str = input_str.replace('vnđ', ' <MEASURE>vnđ</MEASURE> ')
    input_str = input_str.replace('vnd', ' <MEASURE>vnd</MEASURE> ')
    input_str = input_str.replace('VND', ' <MEASURE>VND</MEASURE> ')

    # Units of area
    input_str = input_str.replace('km2', ' <MEASURE>km2</MEASURE> ')
    input_str = input_str.replace('cm2', ' <MEASURE>cm2</MEASURE> ')
    input_str = input_str.replace('mm2', ' <MEASURE>mm2</MEASURE> ')
    input_str = input_str.replace('m2', ' <MEASURE>m2</MEASURE> ')
    input_str = input_str.replace(' ha ', ' <MEASURE>ha</MEASURE> ')

    # Units of length
    # input_str = input_str.replace(' km ', ' <MEASURE>km</MEASURE> ')
    # input_str = input_str.replace(' cm ', ' <MEASURE>cm</MEASURE> ')
    input_str = input_str.replace(' mm ', ' <MEASURE>mm</MEASURE> ')
    # input_str = input_str.replace(' nm ', ' <MEASURE>nm</MEASURE> ')
    input_str = input_str.replace('inch ', ' <MEASURE>inch</MEASURE> ')

    # Unit update
    input_str = input_str.replace('grams ', ' <MEASURE>grams</MEASURE> ')
    # input_str = input_str.replace('ms ', ' <MEASURE>ms</MEASURE> ')
    input_str = input_str.replace('mmol ', ' <MEASURE>mmol</MEASURE> ')
    input_str = input_str.replace('gr ', ' <MEASURE>gr</MEASURE> ')
    
    input_str = input_str.replace('hr ', ' <MEASURE>hr</MEASURE> ')
    input_str = input_str.replace('mmhg ', ' <MEASURE>mmhg</MEASURE> ')


    # Units of volume
    input_str = input_str.replace('ml ', ' <MEASURE>ml</MEASURE> ')
    input_str = input_str.replace('cm3 ', ' <MEASURE>cm3</MEASURE> ')
    # input_str = input_str.replace('cc ', ' <MEASURE>cc</MEASURE> ')
    input_str = input_str.replace('m3 ', ' <MEASURE>m3</MEASURE> ')

    # Units of weight
    input_str = input_str.replace('/kg', ' <MEASURE>/kg</MEASURE> ')
    input_str = input_str.replace('kg/', ' <MEASURE>kg/</MEASURE> ')
    # input_str = input_str.replace('kg ', ' <MEASURE>kg</MEASURE> ')
    # input_str = input_str.replace(' gram ', ' <MEASURE>gram</MEASURE> ')
    input_str = input_str.replace(' mg ', ' <MEASURE>mg</MEASURE> ')

    # Units of temperature
    input_str = input_str.replace("oC ", " <MEASURE>oC</MEASURE> ")
    input_str = input_str.replace("ºC ", " <MEASURE>ºC</MEASURE> ")
    input_str = input_str.replace("ºF ", " <MEASURE>ºF</MEASURE> ")

    # Picture element
    input_str = input_str.replace('MP ', ' <MEASURE>MP</MEASURE> ')

    # Units of speed
    input_str = input_str.replace("bpm", " <MEASURE>bpm</MEASURE> ")
    input_str = input_str.replace("nm/s", " <MEASURE>nm/s</MEASURE> ")
    input_str = input_str.replace("µm/s", " <MEASURE>µm/s</MEASURE> ")
    input_str = input_str.replace("mm/s", " <MEASURE>mm/s</MEASURE> ")
    input_str = input_str.replace("cm/s", " <MEASURE>cm/s</MEASURE> ")
    input_str = input_str.replace("dm/s", " <MEASURE>dm/s</MEASURE> ")
    input_str = input_str.replace("dam/s", " <MEASURE>dam/s</MEASURE> ")
    input_str = input_str.replace("hm/s", " <MEASURE>hm/s</MEASURE> ")
    input_str = input_str.replace("km/s", " <MEASURE>km/s</MEASURE> ")
    input_str = input_str.replace("m/s", " <MEASURE>m/s</MEASURE> ")
    input_str = input_str.replace("nm/giây", " <MEASURE>nm/giây</MEASURE> ")
    input_str = input_str.replace("µm/giây", " <MEASURE>µm/giây</MEASURE> ")
    input_str = input_str.replace("mm/giây", " <MEASURE>mm/giây</MEASURE> ")
    input_str = input_str.replace("cm/giây", " <MEASURE>cm/giây</MEASURE> ")
    input_str = input_str.replace("dm/giây", " <MEASURE>dm/giây</MEASURE> ")
    input_str = input_str.replace("dam/giây", " <MEASURE>dam/giây</MEASURE> ")
    input_str = input_str.replace("hm/giây", " <MEASURE>hm/giây</MEASURE> ")
    input_str = input_str.replace("km/giây", " <MEASURE>km/giây</MEASURE> ")
    input_str = input_str.replace("dặm/giây", " <MEASURE>dặm/giây</MEASURE> ")
    input_str = input_str.replace("m/giây", " <MEASURE>m/giây</MEASURE> ")
    input_str = input_str.replace("nm/h", " <MEASURE>nm/h</MEASURE> ")
    input_str = input_str.replace("µm/h", " <MEASURE>µm/h</MEASURE> ")
    input_str = input_str.replace("mm/h", " <MEASURE>mm/h</MEASURE> ")
    input_str = input_str.replace("cm/h", " <MEASURE>cm/h</MEASURE> ")
    input_str = input_str.replace("dm/h", " <MEASURE>dm/h</MEASURE> ")
    input_str = input_str.replace("dam/h", " <MEASURE>dam/h</MEASURE> ")
    input_str = input_str.replace("hm/h", " <MEASURE>hm/h</MEASURE> ")
    input_str = input_str.replace("km/h", " <MEASURE>km/h</MEASURE> ")
    input_str = input_str.replace("kmh", " <MEASURE>kmh</MEASURE> ")
    input_str = input_str.replace("m/h", " <MEASURE>m/h</MEASURE> ")
    input_str = input_str.replace("nm/giờ", " <MEASURE>nm/giờ</MEASURE> ")
    input_str = input_str.replace("µm/giờ", " <MEASURE>µm/giờ</MEASURE> ")
    input_str = input_str.replace("mm/giờ", " <MEASURE>mm/giờ</MEASURE> ")
    input_str = input_str.replace("cm/giờ", " <MEASURE>cm/giờ</MEASURE> ")
    input_str = input_str.replace("dm/giờ", " <MEASURE>dm/giờ</MEASURE> ")
    input_str = input_str.replace("dam/giờ", " <MEASURE>dam/giờ</MEASURE> ")
    input_str = input_str.replace("hm/giờ", " <MEASURE>hm/giờ</MEASURE> ")
    input_str = input_str.replace("km/giờ", " <MEASURE>km/giờ</MEASURE> ")
    input_str = input_str.replace("m/giờ", " <MEASURE>m/giờ</MEASURE> ")

    # Others
    input_str = input_str.replace("/giây", " <MEASURE>/giây</MEASURE> ")
    input_str = input_str.replace("/tấn", " <MEASURE>/tấn</MEASURE> ")
    input_str = input_str.replace("/thùng", " <MEASURE>/thùng</MEASURE> ")
    input_str = input_str.replace("/căn", " <MEASURE>/căn</MEASURE> ")
    input_str = input_str.replace("/cái", " <MEASURE>/cái</MEASURE> ")
    input_str = input_str.replace("/con", " <MEASURE>/con</MEASURE> ")
    input_str = input_str.replace("/năm", " <MEASURE>/năm</MEASURE> ")
    input_str = input_str.replace("/tháng", " <MEASURE>/tháng</MEASURE> ")
    input_str = input_str.replace("/ngày", " <MEASURE>/ngày</MEASURE> ")
    input_str = input_str.replace("/giờ", " <MEASURE>/giờ</MEASURE> ")
    input_str = input_str.replace("/phút", " <MEASURE>/phút</MEASURE> ")
    input_str = input_str.replace("/người", " <MEASURE>/người</MEASURE> ")
    input_str = input_str.replace("đ/CP", " <MEASURE>đ/CP</MEASURE> ")
    input_str = input_str.replace("đ/lít", " <MEASURE>đ/lít</MEASURE> ")
    input_str = input_str.replace("đ/lượt", " <MEASURE>đ/lượt</MEASURE> ")
    input_str = input_str.replace("người/", " <MEASURE>người/</MEASURE> ")
    input_str = input_str.replace("giờ/", " <MEASURE>giờ/</MEASURE> ")
    input_str = input_str.replace('%', ' <MEASURE>%</MEASURE> ')
    input_str = input_str.replace('mAh ', ' <MEASURE>mAh</MEASURE> ')
    input_str = input_str.replace(" lít/", " <MEASURE>lít/</MEASURE> ")
    input_str = input_str.replace("./", "")
    input_str = input_str.replace("Nm", " <MEASURE>Nm</MEASURE> ")
    input_str = input_str.replace("º", " <MEASURE>º</MEASURE> ")
    input_str = input_str.replace("vòng 1/", " <MEASURE>vòng 1/</MEASURE> ")
    input_str = input_str.replace("mmol/l", " <MEASURE>mmol/l</MEASURE> ")
    input_str = input_str.replace("mg/", " <MEASURE>mg/</MEASURE> ")
    input_str = input_str.replace("triệu/", " <MEASURE>triệu/</MEASURE> ")
    input_str = input_str.replace("g/km", " <MEASURE>g/km</MEASURE> ")
    input_str = input_str.replace("ounce", " <MEASURE>ounce</MEASURE> ")
    input_str = input_str.replace("m3/s", " <MEASURE>m3/s</MEASURE> ")

    # Units of information
    # output_str = output_str.replace('KB ', ' <MEASURE>ki lô bai</MEASURE> ')
    output_str = output_str.replace('Mb ', ' <MEASURE>mê ga bai</MEASURE> ')
    output_str = output_str.replace('GB ', ' <MEASURE>ghi</MEASURE> ')
    output_str = output_str.replace('Gb ', ' <MEASURE>ghi</MEASURE> ')
    # output_str = output_str.replace('TB ', ' <MEASURE>tê ra bai</MEASURE> ')
    
    # 2G, 3G, etc
    output_str = output_str.replace(' 2G ', ' <MEASURE>hai gờ</MEASURE> ')
    output_str = output_str.replace(' 3G ', ' <MEASURE>ba gờ</MEASURE> ')
    output_str = output_str.replace(' 4G ', ' <MEASURE>bốn gờ</MEASURE> ')
    output_str = output_str.replace(' 5G ', ' <MEASURE>năm gờ</MEASURE> ')
    
    # Units of frequency
    output_str = output_str.replace('GHz', ' <MEASURE>ghi ga héc</MEASURE> ')
    output_str = output_str.replace('MHz', ' <MEASURE>mê ga héc</MEASURE> ')

    # Units of data-rate
    output_str = output_str.replace('Mbps', ' <MEASURE>mê ga bít trên giây</MEASURE> ')
    output_str = output_str.replace('Mb/s', ' <MEASURE>mê ga bít trên giây</MEASURE> ')
    
    # Units of currency
    output_str = output_str.replace("đồng/", " <MEASURE>đồng trên</MEASURE> ")
    output_str = output_str.replace("USD/", " <MEASURE>u ét đê trên</MEASURE> ")
    output_str = output_str.replace('đ ', ' <MEASURE>đồng</MEASURE> ')
    output_str = output_str.replace('$', ' <MEASURE>đô la</MEASURE> ')
    output_str = output_str.replace('USD', ' <MEASURE>u ét đê</MEASURE> ')
    output_str = output_str.replace('VNĐ', ' <MEASURE>đồng</MEASURE> ')
    output_str = output_str.replace('vnđ', ' <MEASURE>đồng</MEASURE> ')
    output_str = output_str.replace('vnd', ' <MEASURE>đồng</MEASURE> ')
    output_str = output_str.replace('VND', ' <MEASURE>đồng</MEASURE> ')

    # Units of area
    output_str = output_str.replace('km2', ' <MEASURE>ki lô mét vuông</MEASURE> ')
    output_str = output_str.replace('cm2', ' <MEASURE>xen ti mét vuông</MEASURE> ')
    output_str = output_str.replace('mm2', ' <MEASURE>mi li mét vuông</MEASURE> ')
    output_str = output_str.replace('m2', ' <MEASURE>mét vuông</MEASURE> ')
    output_str = output_str.replace(' ha ', ' <MEASURE>héc ta</MEASURE> ')
    
    # Units of length
    # output_str = output_str.replace(' km ', ' <MEASURE>ki lô mét</MEASURE> ')
    # output_str = output_str.replace(' cm ', ' <MEASURE>xen ti mét</MEASURE> ')
    output_str = output_str.replace(' mm ', ' <MEASURE>mi li mét</MEASURE> ')
    # output_str = output_str.replace(' nm ', ' <MEASURE>na nô mét</MEASURE> ')
    output_str = output_str.replace('inch ', ' <MEASURE>inh</MEASURE> ')
    
    # Units of volume
    output_str = output_str.replace('ml ', ' <MEASURE>mi li lít</MEASURE> ')
    output_str = output_str.replace('cm3 ', ' <MEASURE>xen ti mét khối</MEASURE> ')
    # output_str = output_str.replace('cc ', ' <MEASURE>xen ti mét khối</MEASURE> ')
    output_str = output_str.replace('m3 ', ' <MEASURE>mét khối</MEASURE> ')

    # Units of weight
    output_str = output_str.replace('/kg', ' <MEASURE>trên một ki lô gam</MEASURE> ')
    output_str = output_str.replace('kg/', ' <MEASURE>ki lô gam trên</MEASURE> ')
    # output_str = output_str.replace('kg ', ' <MEASURE>ki lô gam</MEASURE> ')
    output_str = output_str.replace(' gram ', ' <MEASURE>gờ ram</MEASURE> ')
    output_str = output_str.replace(' mg ', ' <MEASURE>mi li gam</MEASURE> ')

    # Unit update

    # output_str = output_str.replace('ms ', ' <MEASURE>mi li giây</MEASURE> ')
    output_str = output_str.replace('mmol ', ' <MEASURE>mi li mon</MEASURE> ')
    output_str = output_str.replace('gr ', ' <MEASURE>gờ ram</MEASURE> ')
    output_str = output_str.replace('grams ', ' <MEASURE>gờ ram</MEASURE> ')
    # output_str = output_str.replace('hr ', ' <MEASURE>giờ</MEASURE> ')
    output_str = output_str.replace('mmhg ', ' <MEASURE>mi li mét thủy ngân</MEASURE> ')

    # Units of temperature
    output_str = output_str.replace("oC ", " <MEASURE>độ xê</MEASURE> ")
    output_str = output_str.replace("ºC ", " <MEASURE>độ xê</MEASURE> ")
    output_str = output_str.replace("ºF ", " <MEASURE>độ ép</MEASURE> ")
    
    # Picture element
    output_str = output_str.replace('MP ', ' <MEASURE>mê ga píc xeo</MEASURE> ')
    
    # Units of speed
    output_str = output_str.replace("bpm", " <MEASURE>nhịp trên phút</MEASURE> ")
    output_str = output_str.replace("nm/s", " <MEASURE>na nô mét trên giây</MEASURE> ")
    output_str = output_str.replace("µm/s", " <MEASURE>mi cờ rô mét trên giây</MEASURE> ")
    output_str = output_str.replace("mm/s", " <MEASURE>mi li mét trên giây</MEASURE> ")
    output_str = output_str.replace("cm/s", " <MEASURE>xen ti mét trên giây</MEASURE> ")
    output_str = output_str.replace("dm/s", " <MEASURE>đề xi mét trên giây</MEASURE> ")
    output_str = output_str.replace("dam/s", " <MEASURE>đề ca mét trên giây</MEASURE> ")
    output_str = output_str.replace("hm/s", " <MEASURE>héc tô mét trên giây</MEASURE> ")
    output_str = output_str.replace("km/s", " <MEASURE>ki lô mét trên giây</MEASURE> ")
    output_str = output_str.replace("m/s", " <MEASURE>mét trên giây</MEASURE> ")
    output_str = output_str.replace("nm/giây", " <MEASURE>na nô mét trên giây</MEASURE> ")
    output_str = output_str.replace("µm/giây", " <MEASURE>mi cờ rô mét trên giây</MEASURE> ")
    output_str = output_str.replace("mm/giây", " <MEASURE>mi li mét trên giây</MEASURE> ")
    output_str = output_str.replace("cm/giây", " <MEASURE>xen ti mét trên giây</MEASURE> ")
    output_str = output_str.replace("dm/giây", " <MEASURE>đề xi mét trên giây</MEASURE> ")
    output_str = output_str.replace("dam/giây", " <MEASURE>đề ca mét trên giây</MEASURE> ")
    output_str = output_str.replace("hm/giây", " <MEASURE>héc tô mét trên giây</MEASURE> ")
    output_str = output_str.replace("km/giây", " <MEASURE>ki lô mét trên giây</MEASURE> ")
    output_str = output_str.replace("dặm/giây", " <MEASURE>dặm trên giây</MEASURE> ")
    output_str = output_str.replace("m/giây", " <MEASURE>mét trên giây</MEASURE> ")
    output_str = output_str.replace("nm/h", " <MEASURE>na nô mét trên giờ</MEASURE> ")
    output_str = output_str.replace("µm/h", " <MEASURE>mi cờ rô mét trên giờ</MEASURE> ")
    output_str = output_str.replace("mm/h", " <MEASURE>mi li mét trên giờ</MEASURE> ")
    output_str = output_str.replace("cm/h", " <MEASURE>xen ti mét trên giờ</MEASURE> ")
    output_str = output_str.replace("dm/h", " <MEASURE>đề xi mét trên giờ</MEASURE> ")
    output_str = output_str.replace("dam/h", " <MEASURE>đề ca mét trên giờ</MEASURE> ")
    output_str = output_str.replace("hm/h", " <MEASURE>héc tô mét trên giờ</MEASURE> ")
    output_str = output_str.replace("km/h", " <MEASURE>ki lô mét trên giờ</MEASURE> ")
    output_str = output_str.replace("kmh", " <MEASURE>ki lô mét trên giờ</MEASURE> ")
    output_str = output_str.replace("m/h", " <MEASURE>mét trên giờ</MEASURE> ")
    output_str = output_str.replace("nm/giờ", " <MEASURE>na nô mét trên giờ</MEASURE> ")
    output_str = output_str.replace("µm/giờ", " <MEASURE>mi cờ rô mét trên giờ</MEASURE> ")
    output_str = output_str.replace("mm/giờ", " <MEASURE>mi li mét trên giờ</MEASURE> ")
    output_str = output_str.replace("cm/giờ", " <MEASURE>xen ti mét trên giờ</MEASURE> ")
    output_str = output_str.replace("dm/giờ", " <MEASURE>đề xi mét trên giờ</MEASURE> ")
    output_str = output_str.replace("dam/giờ", " <MEASURE>đề ca mét trên giờ</MEASURE> ")
    output_str = output_str.replace("hm/giờ", " <MEASURE>héc tô mét trên giờ</MEASURE> ")
    output_str = output_str.replace("km/giờ", " <MEASURE>ki lô mét trên giờ</MEASURE> ")
    output_str = output_str.replace("m/giờ", " <MEASURE>mét trên giờ</MEASURE> ")

    # Others
    output_str = output_str.replace("/giây", " <MEASURE>trên giây</MEASURE> ")
    output_str = output_str.replace("/tấn", " <MEASURE>trên tấn</MEASURE> ")
    output_str = output_str.replace("/thùng", " <MEASURE>trên thùng</MEASURE> ")
    output_str = output_str.replace("/căn", " <MEASURE>trên căn</MEASURE> ")
    output_str = output_str.replace("/cái", " <MEASURE>trên cái</MEASURE> ")
    output_str = output_str.replace("/con", " <MEASURE>trên con</MEASURE> ")
    output_str = output_str.replace("/năm", " <MEASURE>trên năm</MEASURE> ")
    output_str = output_str.replace("/tháng", " <MEASURE>trên tháng</MEASURE> ")
    output_str = output_str.replace("/ngày", " <MEASURE>trên ngày</MEASURE> ")
    output_str = output_str.replace("/giờ", " <MEASURE>trên giờ</MEASURE> ")
    output_str = output_str.replace("/phút", " <MEASURE>trên phút</MEASURE> ")
    output_str = output_str.replace("/người", " <MEASURE>một người</MEASURE> ")
    output_str = output_str.replace("đ/CP", " <MEASURE>đồng trên cổ phiếu</MEASURE> ")
    output_str = output_str.replace("đ/lít", " <MEASURE>đồng trên lít</MEASURE> ")
    output_str = output_str.replace("đ/lượt", " <MEASURE>đồng trên lượt</MEASURE> ")
    output_str = output_str.replace("người/", " <MEASURE>người trên</MEASURE> ")
    output_str = output_str.replace("giờ/", " <MEASURE>giờ trên</MEASURE> ")
    output_str = output_str.replace('%', ' <MEASURE>phần trăm</MEASURE> ')
    output_str = output_str.replace('mAh ', ' <MEASURE>mi li am pe</MEASURE> ')
    output_str = output_str.replace(" lít/", " <MEASURE>lít trên</MEASURE> ")
    output_str = output_str.replace("./", "")
    output_str = output_str.replace("Nm", " <MEASURE>Niu tơn mét</MEASURE> ")
    output_str = output_str.replace("º", " <MEASURE>độ</MEASURE> ")
    output_str = output_str.replace("vòng 1/", " <MEASURE>vòng 1</MEASURE> ")
    output_str = output_str.replace("mmol/l", " <MEASURE>mi li mon trên lít</MEASURE> ")
    output_str = output_str.replace("mg/", " <MEASURE>mi li gam trên</MEASURE> ")
    output_str = output_str.replace("triệu/", " <MEASURE>triệu trên</MEASURE> ")
    output_str = output_str.replace("g/km", " <MEASURE>gam trên ki lô mét</MEASURE> ")
    output_str = output_str.replace("ounce", " <MEASURE>ao</MEASURE> ")
    output_str = output_str.replace("m3/s", " <MEASURE>mét khối trên giây</MEASURE> ")
    
    return input_str, output_str

def money2words(input_str):
    number = input_str.split('k')[0]

    return num2words_fixed(number) + ' ngàn'
    
def multiple1(input_str):

    return input_str.replace('x', ' nhân ')

def version2words(input_str):
    # Androi 2.2, 4.2.1...
    
    return input_str.replace('.', ' chấm ')

def num2words_float(input_str):
    # Fix num2words for reading vietnamese float numbers
    l_part = input_str.split(',')[0]
    r_part = input_str.split(',')[1]
    l_part_str = num2words_fixed(l_part)
    
    if len(r_part) < 3:
        r_part_str = num2words_fixed(r_part)
        return l_part_str + ' phẩy ' + r_part_str
    else:
        r_part_str = ''
        for num in r_part:
            r_part_str += num2words(int(num), lang='vi') + ' '
        r_part_str.rstrip()

    return l_part_str + ' phẩy ' + r_part_str

def num2words_fixed(input_str):
    # Fix num2words for reading vietnamese numbers
    input_str = input_str.translate(str.maketrans('', '', string.punctuation))
    num2words_ = num2words(int(input_str), lang='vi')
    
    # Cases: 205-'hai tram le nam' --> 'hai tram linh nam'
    if 'trăm lẻ' in num2words_:
        num2words_ = num2words_.replace('trăm lẻ', 'trăm linh')
        # Cases: 2005-'hai nghin le nam' --> 'hai nghin khong tram linh nam'
    
    special_terms = ['lẻ một', 'lẻ hai', 'lẻ ba', 'lẻ bốn', 'lẻ năm', 'lẻ sáu', 'lẻ bảy','lẻ tám','lẻ chín']
    for term in special_terms:
        if num2words_.endswith(term):
            num2words_ = num2words_.replace('lẻ', 'không trăm linh')
            break
    
    # Cases: 2035-'hai nghin le ba muoi lam' --> 'hai nghin khong tram ba muoi lam'
    if 'lẻ' in num2words_:
        num2words_ = num2words_.replace('lẻ', 'không trăm')
    
    return num2words_


def date_dmy2words(input_str):
    day, month, year = re.findall(r'[\d]+', input_str)
    day_words = num2words_fixed(day)

    special_dates = ['một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy','tám','chín','mười']
    if day_words in special_dates:
        day_words = 'mùng ' + day_words

    month_words = num2words_fixed(month)
    
    if len(year) == 4:
        year_words = num2words(int(year), lang='vi')
    elif len(year) == 2:
        year_words = num2words(int('20'+year), lang='vi')
   
    year_words = num2words_fixed(year)
    output_str = day_words + ' tháng ' + month_words + ' năm ' + year_words
    
    return output_str

def date_dm2words(input_str):
    day, month = re.findall(r'[\d]+', input_str)
    day_words = num2words_fixed(day)
    month_words = num2words_fixed(month)
    special_dates = ['một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy','tám','chín','mười']
    if day_words in special_dates:
        day_words = 'mùng ' + day_words

    output_str = day_words + ' tháng ' + month_words
    
    return output_str

def date_my2words(input_str):
    month, year = re.findall(r'[\d]+', input_str)
    month_words = num2words_fixed(month)
    year_words = num2words_fixed(year)
    return month_words + ' năm ' + year_words

def phone2words(phone_number):
    phone_digits = re.findall(r'[0-9]', phone_number)
    for index, phone_digit in enumerate(phone_digits):
        phone_digit_str = num2words(int(phone_digit), lang='vi')
        phone_digits[index] = phone_digit_str

    phone_number_str = ' '.join(phone_digits)
    
    return phone_number_str

# def time2words(time):
#     if (time.find('h') != -1):
#         time_hour = time.split('h')[0] 
#         time_minute = time.split('h')[1] 
#     elif (time.find(':') != -1):
#         time_hour = time.split(':')[0] 
#         time_minute = time.split(':')[1]
#     elif (time.find('g') != -1):
#         time_hour = time.split('g')[0] 
#         time_minute = time.split('g')[1]
#     time_hour_str = num2words(int(time_hour), lang='vi')
#     if time_minute == '' or time_minute == '00':
#         return time_hour_str + ' giờ '
#     else:
#         time_minute_str = num2words(int(time_minute), lang='vi')
    
#     time_str = time_hour_str + ' giờ ' + time_minute_str + ' phút'

#     return time_str

def time2words(time):
    if (time.find(':',3,6) != -1):
        time_hour = time.split(':')[0] 
        time_minute = time.split(':')[1]
        time_second = time.split(':')[2]
        time_hour_str = num2words(int(time_hour), lang='vi')
        time_minute_str = num2words(int(time_minute), lang='vi')
        time_second_str = num2words(int(time_second), lang='vi')
        time_str = time_hour_str + ' giờ ' + time_minute_str + ' phút ' + time_second_str + ' giây'


    elif (time.find('p') != -1):
        time_hour = time.split('h')[0] 
        time_minute = time.split('h')[1]
        time_minute = time_minute.replace('p', '')
        time_hour_str = num2words(int(time_hour), lang='vi')
        if time_minute == '' or time_minute == '00':
            return time_hour_str + ' giờ '
        else:
            time_minute_str = num2words(int(time_minute), lang='vi')
            time_str = time_hour_str + ' giờ ' + time_minute_str + ' phút' 

    elif (time.find('h') != -1):
        time_hour = time.split('h')[0] 
        time_minute = time.split('h')[1]
        time_hour_str = num2words(int(time_hour), lang='vi')
        if time_minute == '' or time_minute == '00':
            return time_hour_str + ' giờ '
        else:
            time_minute_str = num2words(int(time_minute), lang='vi')
            time_str = time_hour_str + ' giờ ' + time_minute_str + ' phút'     
    

    elif (time.find(':') != -1):
        time_hour = time.split(':')[0] 
        time_minute = time.split(':')[1]
        time_hour_str = num2words(int(time_hour), lang='vi')
        if time_minute == '' or time_minute == '00':
            return time_hour_str + ' giờ '
        else:
            time_minute_str = num2words(int(time_minute), lang='vi')
            time_str = time_hour_str + ' giờ ' + time_minute_str + ' phút'

    return time_str