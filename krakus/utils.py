import urllib
import zipfile

def download (month,year):

    r = urllib.request.urlopen(f'https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/terminowe/synop/{year}/{year}_{month}_s.zip')

    with open('response.zip', 'wb+') as myzip:
        myzip.write(r.read())

    with zipfile.ZipFile('response.zip') as myzip:
        with myzip.open('s_t_01_2019.csv') as myfile:
            print(myfile.read())

def filtrfile (origial,new):
    f1 = open(original, "rb")
    f2 = open(new, "wb") 
    for n in original:
        line = f1.readline()
        if line == "":
            break
        if line[0] == "350190566":
            continue
        f2.write(line)
    f1.close()
    f2.close()
    return





    # dezippare contenuto s_t_01_2019.csv dentro a response.zip

    # leggere il contenuto del file CSV e creare un nuovo file CSV con dentro solo i dati di cracovia
