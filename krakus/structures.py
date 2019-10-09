from collections import namedtuple

# Basic representation of a measurement station
Station = namedtuple('Station', ['id', 'pm10_code', 'pm25_code'], defaults=[None])

# Map of location - representation
STATION_MAP = {
    'os. Wadów': Station(id='161', pm10_code='1921'),
    'os. Piastów': Station(id='152', pm10_code='1747'),
    'Aleja Krasińskiego': Station(id='6', pm10_code='46', pm25_code='202'),
    'os. Swoszowice': Station(id='173', pm10_code='2176'),
    'ul. Złoty Róg': Station(id='153', pm10_code='1752'),
    'Kurdwanów': Station(id='16', pm10_code='148', pm25_code='242'),
    'ul. Dietla': Station(id='149', pm10_code='1723'),
}
