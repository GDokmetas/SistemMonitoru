import serial.tools.list_ports
import serial
import PySimpleGUI as sg
import shutil
import psutil
from datetime import datetime 
from urllib import response
import requests
import json
import time
origin_url = "https://api.openweathermap.org/data/2.5/weather?q=Ankara&APPID=API KEY BURAYA YAZILACAK"
ser = serial.Serial()  #Global tanımlanmalı
yazdir = False 
sistem_yazdirma = True
meteoroloji_yazdirma = False
meteoroloji_guncelleme_sayac = 0
yazdirma = ""
sistem_ekran_sayac = 0
yazi_ekran_sayac = 0
meteoroloji_sayac = 0
meteoroloji_yazdir = False 
meteoroloji_verisi = ""
yazdirma_sayac = 0
yazdirma_komut = False
def serial_ports():
    ports = serial.tools.list_ports.comports()
    print(ports)
    seri_port = []
    for p in ports:
        print(p.device)
        seri_port.append(p.device)
    print(seri_port)
    return seri_port
########################
def serial_baglan():
    com_deger = value[0]
    baud_deger = value[1]
    print("Baud Deger", value[1])
    global ser
    ser = serial.Serial(com_deger, baud_deger, timeout=0, parity=serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE , bytesize = serial.EIGHTBITS, rtscts=0)
    window["-BAGLANDI_TEXT-"].update('Bağlandı...')

sg.theme("Reddit")

ekran_layout = [ [sg.Text("Ayarlamak istediğiniz metni girin...")], 
                 [sg.Text("Her Bir Satırda En fazla 20 Karakter Kullanabilirsiniz.")], 
                 [sg.Text("1. Satır:"), sg.Input(size=(40, 1), font=("Consolas", 14), key="giris_text_1")],
                 [sg.Text("2. Satır:"), sg.Input(size=(40, 1), font=("Consolas", 14), key="giris_text_2")],
                 [sg.Text("3. Satır:"), sg.Input(size=(40, 1), font=("Consolas", 14), key="giris_text_3")],
                 [sg.Text("4. Satır:"), sg.Input(size=(40, 1), font=("Consolas", 14), key="giris_text_4")],
                 [sg.Text("Sistem Ekrani")],
                 [sg.Multiline(size=(40,4), font=("Consolas", 14), key="sistem_text")],
                 [sg.Text("Sistem Monitor Sure:"), sg.Spin(initial_value=3, key='sistem-sure', values=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)), 
                 sg.Text("Ekran Yazdirma Sure:"), sg.Spin(initial_value=1, key='ekran-sure', values=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)),
                 sg.Text("Meteoroloji Sure:"), sg.Spin(initial_value=1, key='meteoroloji-sure', values=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)),
                 ],
                 [sg.Button(button_text="Yazdır", font=("Arial Black", 11), key="yazdir"), 
                 sg.Button(button_text="Temizle", font=("Arial Black", 11), key="temizle"), 
                 sg.Button(button_text="Işık", font=("Arial Black", 11), key="isik"),
                 sg.Checkbox("Meteoroloji Verisi Yazdir", key='meteoroloji-check', enable_events=True),
                 sg.Checkbox("Tarih ve Saat Yazdir", key='tarihsaat-check')]  
                ]

layout =[ [sg.Text("Port Seçiniz:"), sg.Combo(serial_ports(), size=(10,1)),
            sg.Text("Baud Seçiniz:"), sg.Combo(["110","300","600","1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200", "128000", "256000"], default_value=9600), 
            sg.Button(button_text="Bağlan", key="-BAGLAN-", size=(10,1)) ],
            [sg.Text("", size=(10,1), key="-BAGLANDI_TEXT-")],
            [sg.Frame("LCD Ekran", ekran_layout)]
        ]

window = sg.Window("Sistem Monitörü - Gökhan DÖKMETAŞ", layout)

while True:
    event, value = window.read(timeout=100) 
    if event == sg.WIN_CLOSED or event == 'Exit':
        break    
    if event == "-BAGLAN-":
        if (value[0] == ""):
            sg.popup("Bir Port Seçiniz!", title="Hata", custom_text="Tamam") 
        elif (value[1] == ""):
            sg.popup("Baud Oranını Seçiniz!", title="Hata", custom_text="Tamam")
        else:
            serial_baglan()
    if event == "yazdir":
        print(value)
        yazdirilacak_1 = value['giris_text_1']
        yazdirilacak_2 = value['giris_text_2']
        yazdirilacak_3 = value['giris_text_3']
        yazdirilacak_4 = value['giris_text_4']
        #yazdirilacak = yazdirilacak[:-1]
        if(len(yazdirilacak_1) > 20):
            sg.Popup("Yazdirilacak Veri Çok Büyük!") 
        if(len(yazdirilacak_2) > 20):
            sg.Popup("Yazdirilacak Veri Çok Büyük!") 
        if(len(yazdirilacak_3) > 20):
            sg.Popup("Yazdirilacak Veri Çok Büyük!") 
        if(len(yazdirilacak_4) > 20):
            sg.Popup("Yazdirilacak Veri Çok Büyük!") 
        
        yazdirilacak_1 = yazdirilacak_1 + ((20 - len(yazdirilacak_1)) * " ") 
        yazdirilacak_2 = yazdirilacak_2 + ((20 - len(yazdirilacak_2)) * " ") 
        yazdirilacak_3 = yazdirilacak_3 + ((20 - len(yazdirilacak_3)) * " ") 
        yazdirilacak_4 = yazdirilacak_4 + ((20 - len(yazdirilacak_4)) * " ") 
        yazdirma = yazdirilacak_1 + yazdirilacak_3 + yazdirilacak_2 + yazdirilacak_4 
        yazdir = True
    if event ==  "meteoroloji-check":
        meteoroloji_yazdir = value['meteoroloji-check']
        print(meteoroloji_yazdir)
    if event == "temizle":
        window['giris_text_1'].update("")
        window['giris_text_2'].update("")
        window['giris_text_3'].update("")
        window['giris_text_4'].update("")
        yazdir = False
        sistem_yazdirma = True
        ser.write('*'.encode('Ascii'))
    if event == "isik":
        isik_string = "\\"
        ser.write(isik_string.encode('Ascii'))
        print("ISIK")
    #? ? lcd_home özelliği...

#Window timeout 100ms --- Buradaki kodlar her timeout süresinde işletilmekte. 
    if ser.isOpen() == True and sistem_yazdirma == True:
        du = shutil.disk_usage("/")
        bos_alan_yuzde = du.free / du.total * 100
        islemci = "CPU:%" + str(int(psutil.cpu_percent(1))).ljust(3)
        islemci_freq= "FRQ:" + str(int(psutil.cpu_freq().current)).rjust(4) + "MHz"
        islemci_satir = islemci + islemci_freq + " "
        toplam_alan = "DSKT:" + (str(int(du.total / 1024 / 1024 / 1024)) + "GB").ljust(6)
        bos_alan = " F:" + (str(int(du.free / 1024 / 1024 / 1024)) + "GB").ljust(6)
        # bos_yuzde = "F%" + str(int(bos_alan_yuzde)).ljust(2) + " "
        ram_total = int(psutil.virtual_memory().total / 1024 / 1024)
        ram_free = int(psutil.virtual_memory().free / 1024 / 1024)
        ram_percent = int(psutil.virtual_memory().percent)
        ram_satir = "M:" + str(ram_total).rjust(5) + "MB " + "F:" + (str(ram_free) + "MB").ljust(8)
        if value['tarihsaat-check']:
            tarihsaat = str(datetime.now())
            tarih = tarihsaat[8:10] + "-" + tarihsaat[5:7] + "-" + tarihsaat[2:4]
            saat = tarihsaat[11:13] + ":" + tarihsaat[14:16] + ":" + tarihsaat[17:19]
            sistem_mesaji = saat + "  " + tarih + "  "
        else:
            sistem_mesaji = "-----SYSTEM OK------"
        ser.write("?".encode('Ascii'))
        ser.write(islemci_satir.encode('Ascii'))
        ser.write(toplam_alan.encode("Ascii"))
        ser.write(bos_alan.encode("Ascii"))
        ser.write(ram_satir.encode("Ascii"))
        ser.write(sistem_mesaji.encode("Ascii"))
        window['sistem_text'].update(islemci_satir + toplam_alan + bos_alan + ram_satir + sistem_mesaji)
        sistem_ekran_sayac += 1
        if sistem_ekran_sayac > value['sistem-sure']:
            sistem_ekran_sayac = 0
            sistem_yazdirma = False
            yazdirma_sayac += 1;
            if yazdir == True and (yazdirma_sayac % 2 == 0):
                yazdirma_komut = True 
                meteoroloji_yazdirma = False
            elif meteoroloji_yazdir == True and (yazdirma_sayac % 2 == 1):
                meteoroloji_yazdirma = True 
                yazdirma_komut = False 
            else:
                sistem_yazdirma = True 
            print(sistem_yazdirma)
    elif yazdirma != "" and yazdir == True and yazdirma_komut == True:
        print("Yazdirilacak", yazdirma)
        ser.write(yazdirma.encode('Ascii'))  
        yazi_ekran_sayac += 1
        if yazi_ekran_sayac > value['ekran-sure'] * 6:
            yazi_ekran_sayac = 0
            sistem_yazdirma = True  
            ser.write('*'.encode('Ascii'))

    elif meteoroloji_yazdir == True and meteoroloji_yazdirma == True:
        # meteoroloji verisi güncelleme
        if(meteoroloji_guncelleme_sayac % 1000 == 0):
            print("Meteoroloji Guncelleme")
            print(meteoroloji_guncelleme_sayac)
            ser.write('*'.encode('Ascii'))
            ser.write("Meteoroloji Verisi  ".encode('Ascii'))
            ser.write("                    ".encode('Ascii'))
            ser.write("Guncelleniyor...".encode('Ascii'))
            time.sleep(2)
            # Meteoroloji verisi güncelleme web scraping kodları
            response = requests.get(origin_url)
            json_response = json.loads(response.text)
            sehir_adi = json_response['name']
            sicaklik = round(json_response['main']['temp'] - 273.15, 2)
            min_sicaklik = round(json_response['main']['temp_min'] - 273.15, 2)
            max_sicaklik = round(json_response['main']['temp_max'] - 273.15, 2)
            basinc = json_response['main']['pressure']
            nem = json_response['main']['humidity']
            hava_durumu = json_response['weather'][0]['description']
            satir_1 = "SICAKLIK:" + "{:02.2f}".format(sicaklik) + "C     "
            satir_2 = "MIN:" + "{:02.2f}".format(min_sicaklik) + "C" + "MAX:" + "{:02.2f}".format(max_sicaklik) + "C"
            satir_3 = "NEM:" + "{:03d}".format(nem) + "% " + "BASINC:" + "{:04d}".format(basinc) 
            satir_4 = hava_durumu.upper()
            satir_4 = satir_4 + ((20 - len(satir_4)) * " ")
            satir_2 = satir_2 + ((20 - len(satir_2)) * " ") 
            satir_3 = satir_3 + ((20 - len(satir_3)) * " ")
            satir_1 = satir_1 + ((20 - len(satir_1)) * " ")
            print(satir_1)
            print(satir_2)
            print(satir_3)
            print(satir_4)
            meteoroloji_verisi = satir_1 + satir_3 + satir_2 + satir_4
            ser.write("*".encode('Ascii'))
        meteoroloji_sayac += 1
        meteoroloji_guncelleme_sayac += 1
        print(meteoroloji_sayac);
        # meteoroloji verisi yazdirma 
        ser.write(meteoroloji_verisi.encode('Ascii'))
        
        
        # meteoroloji yazdirma sonlandirma
        if meteoroloji_sayac > value['meteoroloji-sure'] * 6:
            meteoroloji_sayac = 0
            sistem_yazdirma = True 
            meteoroloji_yazdirma = False
            ser.write('*'.encode('Ascii'))
window.close()
