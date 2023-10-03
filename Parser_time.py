import requests
import matplotlib.pyplot as plt
import time


def to_hour(t):
    h, mins, seconds, m_seconds = map(int, t.split(':'))
    right_hour = h + (mins + (seconds + m_seconds / 60) / 60) / 60
    return right_hour


k = ([] for _ in range(7))
dd, mm, year, hour, latitude, longitude, height = k
lst = [dd, mm, year, hour, latitude, longitude, height]

# hour = [to_hour(t) for t in hour]
# for i in range(len(hour)):
#     hour[i] = to_hour(hour[i])

with open('data.txt', encoding='utf-8') as file:
    for s in file:
        for spicok, stroka in zip(lst, s.strip().split()):
            spicok.append(stroka)

hour = [to_hour(t) for t in hour]

whichIri = int(input('IRI Version\n0 - IRI 2016\n1 - IRI 2020\n2 - IRI 2012\n3 - IRI 2007\n'))
geoFlag = int(input(
    'Coordinate Type\n0 - Geographic\n1 - Geomagnetic(magnetic field coordinate calculated using the IGRF model)\n'))
profileType = int(input(
    'Profile Type\n1 - Height [0 - 1000 km]\n2 - Latitude [-90 - 90 deg]\n3 - Longitude [0 - 360 deg]\n4 - Year [1961 - 2021]\n5 - Month [1 - 12]\n6 - Day of month [1 - 31]\n7 - Day of year [1 - 366]\n8 - Hour of day [1 - 24]\n'))
start = input('Start\n')
stop = input('Stop\n')
stepSize = input('Step Size\n')
dataOptions = int(input(
    'Data Options(Select what type of data is returned)\n0 - Standard table of IRI parameters\n1 - List of peak heights and densities\n2 - Plasma frequencies, B0, M3000, Valley, Width and Depth\n'))
outputOptions = int(
    input('Output Options(Select how the data is returned to you)\n0 - Display Data\n1 - Download Data\n2 - Plot\n'))
tecHeight = input(
    'Upper Height (km) for TEC Integration (0 for no TEC)(Determines what you are modeling against Upper height for TEC integration: the altitude used to calculate TEC. For example, if it is 2000 km, TEC is obtained by numerical integration in 1 km step from 50 km to 2000 km.)\n')
print('...WAIT...')

url = "https://kauai.ccmc.gsfc.nasa.gov/ir_server/iri/submitForm"
headers = {"Accept": "application/json, text/plain, */*",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "ru-RU,ru;q=0.9,de-DE;q=0.8,de;q=0.7,en-US;q=0.6,en;q=0.5,fr;q=0.4,kn;q=0.3,ja;q=0.2,zh-TW;q=0.1,zh-CN;q=0.1,zh;q=0.1",
           "Connection": "keep-alive",
           "Content-Length": "237",
           "Content-Type": "application/json",
           "Cookie": "_ga=GA1.5.117804746.1676636483; _gid=GA1.2.1392216211.1677508963; _gid=GA1.5.1392216211.1677508963; _ga_L952YR87SS=GS1.1.1677526001.7.0.1677526003.0.0.0; _gat=1; _gat_GSA_ENOR0=1; _ga=GA1.1.117804746.1676636483; _ga_CW9J2XG88Y=GS1.1.1677526003.7.0.1677526014.0.0.0",
           "Host": "kauai.ccmc.gsfc.nasa.gov",
           "Origin": "https://kauai.ccmc.gsfc.nasa.gov",
           "Referer": "https://kauai.ccmc.gsfc.nasa.gov/instantrun/iri",
           "Sec-Fetch-Dest": "empty",
           "Sec-Fetch-Mode": "cors",
           "Sec-Fetch-Site": "same-origin",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
           'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
           "sec-ch-ua-mobile": "?0",
           'sec-ch-ua-platform': '"Windows"'}
for count in range(len(mm)):
    print(f'\nТаблица №{count + 1}\n')
    data = {"whichIri": whichIri, "geoFlag": geoFlag, "latitude": latitude[count], "longitude": longitude[count],
            "year": str(int(year[count]) - 2),
            "mmdd": mm[count] + dd[count],
            "timeFlag": 1,
            "hour": hour[count], "height": height[count], "profileType": profileType, "start": start, "stop": stop,
            "stepSize": stepSize,
            "dataOptions": dataOptions, "outputOptions": outputOptions, "tecHeight": tecHeight}
    answer = requests.post(url=url, headers=headers, json=data).json()
    if dataOptions == 0:
        alfabet = ['PROFILE_OPTION', 'NE_CM3', 'NE_NMF2', 'TN_K', 'TI_K', 'TE_K', 'O_ION', 'N_ION', 'H_ION', 'HE_ION',
                   'O2_ION', 'NO_ION', 'CLUST', 'TEC', 'TOP']
        print(*map(lambda x: x.rjust(14), alfabet))
        for i in range(len(answer)):
            print(*map(lambda x: x.rjust(14), [(answer[i][letter]) for letter in alfabet]))

    if dataOptions == 2:
        alfabet = ['PROFILE_OPTION', 'M3000', 'B0', 'B1', 'W_KM', 'DEPTH', 'FOF2', 'FOF1', 'FOE', 'FOD']
        print(*map(lambda x: x.rjust(14), alfabet))
        for i in range(len(answer)):
            print(*map(lambda x: x.rjust(14), [(answer[i][letter]) for letter in alfabet]))

    if dataOptions == 0:

        k = ([] for _ in range(15))
        profile_option, ne_cm3, ne_nmf2, tn_k, ti_k, te_k, o_ion, n_ion, h_ion, he_ion, o2_ion, no_ion, clust, tec, top = k
        plt_lst = [profile_option, ne_cm3, ne_nmf2, tn_k, ti_k, te_k, o_ion, n_ion, h_ion, he_ion, o2_ion, no_ion,
                   clust, tec, top]
        plt_names = ['PROFILE_OPTION', 'NE_CM3', 'NE_NMF2', 'TN_K', 'TI_K', 'TE_K', 'O_ION', 'N_ION', 'H_ION',
                     'HE_ION', 'O2_ION', 'NO_ION', 'CLUST', 'TEC', 'TOP']

        for i in range(len(answer)):

            for spicok, name in zip(plt_lst, plt_names):
                spicok.append(float(answer[i][name]))

        for spisok, name in zip(plt_lst[1:], plt_names[1:]):
            plt.figure().add_subplot().plot(profile_option, spisok)
            plt.title(name)

    if dataOptions == 2:

        profile_option, m3000, b0, b1, w_km, depth, fof2, fof1, foe, fod = ([] for _ in range(10))
        plt_lst = [profile_option, m3000, b0, b1, w_km, depth, fof2, fof1, foe, fod]
        plt_names = ['PROFILE_OPTION', 'M3000', 'B0', 'B1', 'W_KM', 'DEPTH', 'FOF2', 'FOF1', 'FOE', 'FOD']
        for i in range(len(answer)):
            for spicok, name in zip(plt_lst, plt_names):
                spicok.append(float(answer[i][name]))

        for spicok, name in zip(plt_lst[1:], plt_names[1:]):
            plt.figure().add_subplot().plot(profile_option, spicok)
            plt.title(name)

    plt.show()
    time.sleep(1)
