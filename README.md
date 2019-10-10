<p align="center">
<a href="https://coveralls.io/github/MattBlack85/krakus?branch=master"><img alt="Coverage Status" src="https://coveralls.io/repos/github/MattBlack85/krakus/badge.svg?branch=master"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

Krakus
============
Krakus wants to be a scientific tool to help to determine whether the ban that went live on September 1, 2019, 
is going to solve the pollution problem that affects Kraków (Cracow) or not.



### A bit of history
Air pollution is a big problem in Poland, especially in the rural areas and within the biggest
city agglomerates.
The main source of pollution is home heating; Poland is one of the biggest coal user in the EU and
still a lot of people use coal to heat up houses/flats during the colder months.
Unfortunately, lots of people then, instead of using coal/wood burn whatever they find around which includes:
 - windows
 - plywood
 - diesel fuel
 - used car oil
 - plastic
 - trash
 - tires
 
All these things leave in the air an insane amount of cancerogenics compounds, breathing those is not healthy at all.
Kraków suffered by this for years but since 2019 September, 1st it made burning anything including wood and coal illegal;
this could be a bit controversial but believe somebody which lived there, on the highest pollution days the air
stinks like you never smelled before, so this ban is more than welcome.

### Results
Is still too early to talk about results as per today October 8th there is no real data available to make a conclusion plus
still the coldest period has yet to come.

### What Krakus wants to achieve
The idea behind Krakus is to analyze archived data from the last years and compare those with data after September, 1st.
At a first look it seems to be a quite trivial task but there are other factors that must be taken into account in order
to have clear results and not just guessing, this includes:
 - temperature (hour resolution)
 - wind speed and direction (hour resolution)
 - atmospheric pressure (hour resolution)

### Data source
Data is being gathered from two sources:
 - https://dane.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/terminowe/synop/ (meteorological data)
 - http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/pobierz (PM10 & PM2.5 data)
