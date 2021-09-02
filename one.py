import xml.etree.ElementTree as ET
import urllib.request as urlreq
import urllib.parse as urlpar
import logging


FORMAT = '%(levelname)s %(message)s'

logging.basicConfig(filename='script_log_one.log', level=logging.INFO, format=FORMAT)

i = 0
path = input("Enter the path to XML file(exp. C:/Users/file.xml): ")
tree = ET.parse(path)
root = tree.getroot()

print("Script is working...")
for elem in root.findall('УдостоверяющийЦентр'):
    name = elem.find('КраткоеНазвание')
    compleks_i = elem.find('ПрограммноАппаратныеКомплексы')
    for compleks in compleks_i.findall('ПрограммноАппаратныйКомплекс'):
        for man_key in compleks.findall('КлючиУполномоченныхЛиц'):
            for key in man_key.findall('Ключ'):
                for sert in key.findall('Сертификаты'):
                    for sert_data in sert.findall('ДанныеСертификата'):
                        sert_date = sert_data.find('ПериодДействияС')
                        if sert_date.text[0:4] == "2020" or sert_date.text[0:4] == "2019" or sert_date.text[0:4] == "2021":
                            new_name = name.text.replace('"', '«')
                            new_name = new_name.replace('"', '»')
                            for data in sert_data.findall('Данные'):
                                file = open('C:/Users/a.karpihin/Desktop/certs/рабочие сертификаты/' + new_name + ".crt"
                                            ,"w+")
                                file.write(data.text + '\n')
                                file.close()

                            back_address = key.find('АдресаСписковОтзыва')
                            for url_link in back_address.findall('Адрес'):
                                try:
                                    urlreq.urlretrieve(url_link.text,
                                                       'C:/Users/a.karpihin/Desktop/certs/отозванные/' + new_name + '.crl')
                                    logging.info(f'Page {url_link.text} was SELECTED because it SATISFIES condition 2019|2020|2021')
                                except:
                                    logging.exception(f'Error for link {url_link.text}')
                                    continue

file = open("C:/Users/a.karpihin/Desktop/xml.txt", "w+")
for elem in root.findall('УдостоверяющийЦентр'):
    name = elem.find('КраткоеНазвание')
    accredidation_status = (elem.find('СтатусАккредитации')).find('Статус')
    file.write(name.text + "\t" + accredidation_status.text + "\n")
file.close()
print("\n\nScript finished.")
#C:/Users/a.karpihin/Downloads/tsl.xml
