import xml.etree.ElementTree as ET
import urllib.request as urlreq
import logging
from tqdm import tqdm


FORMAT = '%(asctime)s %(levelname)s %(message)s'

logging.basicConfig(filename='script_log_one.log', level=logging.INFO, format=FORMAT)

user = input("Enter user's name: ")
path = input("Enter the path to XML file(exp. C:/Users/file.xml): ")
tree = ET.parse(path)
root = tree.getroot()
print("Script is working...")
check_list = ["Контур", "КРИПТО-ПРО", "Минкомсвязь России", "МО ПНИЭИ - КрасКрипт", "Сертум-Про", "СПб ИАЦ", "ИИТ",
              "ИНФИНИТУМ", "Холдинговая компания Гарант", "Криптотелеком", "ЦИБ-Сервис", "ГНИВЦ", "Е-Портал", "ИТК", "Айтиком",
              "АО ВТБ Специализированный депозитарий", "БСС-Безопасность", "Сервер-Центр", "УЦ Сибири", "ТИМЕР БАНК", "ЕЭТП",
              "АйТи Мониторинг", "УЦ ГИС", "Санкт-Петербургская Валютная Биржа", "ЦИС ПО", "УНЦИБ", "Выбор", "АСТРАЛ-М",
              "ЦЭК", "Элбис", "ОТС", "Раздолье", "КриптоЦентр", "Банк «Санкт-Петербург»", "Сбербанк", "ПАО «МТС»",
              "ФНС России", "Консалтинговый центр", "Электронный экспресс", "Тензор", "СКБ-банк", "Такском", "ЦентрИнформ", "Екей УЦ",
              "Ижинформпроект", "МАСКОМ-ТЕХЛАЙН", "КриптоСтандарт", "Белинфоналог", "НТСсофт", "Русь-Телеком",
              "УДОСТОВЕРЯЮЩИЙ ЦЕНТР"]
for elem in tqdm(root.findall('УдостоверяющийЦентр')):
    name = elem.find('КраткоеНазвание')
    for word in check_list:
        if word in name.text:
            compleks_i = elem.find('ПрограммноАппаратныеКомплексы')
            for compleks in compleks_i.findall('ПрограммноАппаратныйКомплекс'):
                for man_key in compleks.findall('КлючиУполномоченныхЛиц'):
                    for key in man_key.findall('Ключ'):
                        sert = key.find('Сертификаты')
                        sert_data_list = sert.findall('ДанныеСертификата')
                        for i in range(len(sert_data_list)):
                            sert_date = sert_data_list[i].find('ПериодДействияС')
                            if sert_date.text[0:4] == "2020" or sert_date.text[0:4] == "2019" or sert_date.text[0:4] == "2021":
                                new_name = name.text.replace('"', '«')
                                new_name = new_name.replace('"', '»')
                                data = sert_data_list[i].find('Данные')
                                file = open(f'C:/Users/{user}/Desktop/certs/рабочие сертификаты/{new_name}({str(i)}).crt'
                                            ,"w+")
                                file.write(data.text + '\n')
                                file.close()
                                back_address = key.find('АдресаСписковОтзыва')
                                for url_link in back_address.findall('Адрес'):
                                    try:
                                        file1 = open(f'C:/Users/{user}/Desktop/certs/отозванные/links.txt', 'a')
                                        file1.write(name.text + '\t' + url_link.text + '\n')
                                        urlreq.urlretrieve(url_link.text,
                                                           f'C:/Users/{user}/Desktop/certs/отозванные/{new_name}.crl')
                                        logging.info(f'Page {url_link.text} was SELECTED because it SATISFIES condition 2019|2020|2021')
                                        file1.close()
                                    except:
                                        logging.exception(f'Error for link {url_link.text}')
                                        continue
            else:
                continue

file = open(f'C:/Users/{user}/Desktop/xml.txt', "w+")
for elem in root.findall('УдостоверяющийЦентр'):
    name = elem.find('КраткоеНазвание')
    accredidation_status = (elem.find('СтатусАккредитации')).find('Статус')
    file.write(name.text + "\t" + accredidation_status.text + "\n")
file.close()
print("\n\nScript finished.")
#C:/Users/a.karpihin/Downloads/tsl.xml
#C:/Users/andrew/Downloads/tsl.xml
