import xml.etree.ElementTree as ET
import urllib.request as urlreq
import urllib.parse as urlpar
import logging


#logger = logging.getLogger(name)
#
#stream_handler = logging.StreamHandler()
#logger.addHandler(stream_handler)

logging.basicConfig(filename='script_log.log', level=logging.INFO)

i = 0
path = input("Enter the path to XML file(exp. C:/Users/file.xml): ")
tree = ET.parse(path)
root = tree.getroot()
file = open("C:/Users/a.karpihin/Desktop/xml.txt", "w+")

for elem in root.findall('УдостоверяющийЦентр'):
    name = elem.find('КраткоеНазвание')
    address = elem.find('Адрес')
    region = address.find('Регион')
    region_number = region.find('Код')
    region_name = region.find('Название')
    compleks_i = elem.find('ПрограммноАппаратныеКомплексы')
    compleks = compleks_i.find('ПрограммноАппаратныйКомплекс')

    if compleks is not None:
        keys = compleks.find('КлючиУполномоченныхЛиц')
        key = keys.find('Ключ')
        certs = key.find('Сертификаты')
        data_certs = certs.find('ДанныеСертификата')
        data = data_certs.find('Данные')
        date = data_certs.find('ПериодДействияС')

        #if date.text[0:4] == "2020" or date.text[0:4] == "2019" or date.text[0:4] == "2021":
        new_name = name.text.replace('"', '«')
        new_name = new_name.replace('"', '»')
        file_cert = open('C:/Users/a.karpihin/Desktop/certs/рабочие сертификаты/' + new_name + ".crt", "w+")
        file_cert.write(data.text + '\n')
        file_cert.close()
        back_address = key.find('АдресаСписковОтзыва')
        url_link = back_address.find('Адрес')
        try:
            urlreq.urlretrieve(url_link.text, 'C:/Users/a.karpihin/Desktop/certs/отозванные/' + new_name + '.crl')
        except:
            #logging.error(f'Error for link {url_link.text}')
            logging.exception(f'Error for link {url_link.text}')
            continue

    i = i + 1

    file.write(str(i) + '."' + name.text + '"' + "\t" + region_name.text + "\t" + region_number.text + "\n")
file.close()


#C:/Users/a.karpihin/Downloads/tsl.xml