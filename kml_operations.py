from lxml import etree
from pykml.factory import KML_ElementMaker as KML



def create(lat, lon):
    n_lat,n_lon=convert_position(lat, lon)
    # 使用第一个点创建Folder
    fold = KML.Folder(KML.Placemark(
        KML.Point(KML.coordinates(str(n_lon[0]) + ',' + str(n_lat[0]) + ',0'))
    )
    )

    # 将剩余的点追加到Folder中
    for i in range(1, len(n_lon)):
        fold.append(KML.Placemark(
            KML.Point(KML.coordinates(str(n_lon[i]) + ',' + str(n_lat[i]) + ',0')))
        )

    # 使用etree将KML节点输出为字符串数据
    content = etree.tostring(etree.ElementTree(fold), pretty_print=True)

    # 保存到文件，然后就可以在Google地球中打开了
    with open('gen.kml', 'w') as fp:
        fp.write(str(content))
