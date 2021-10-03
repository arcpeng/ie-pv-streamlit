import json
import requests
import math
from datetime import datetime
from typing import Sequence
from scipy.optimize import curve_fit
import numpy as np

months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
daysAmount = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def sendNasaRequest(lon, lat):
    apiUrl = "https://power.larc.nasa.gov/api/temporal/climatology/point?" +\
            "start=2000&end=2005&" +\
            "latitude={lat}&longitude={lon}" +\
            "&community=re&" +\
            "parameters=SI_EF_TILTED_SURFACE%2CALLSKY_SFC_SW_DWN%2CALLSKY_SFC_SW_DIFF%2CALLSKY_SRF_ALB%2CT2M&" +\
            "format=json&header=false"

    url = apiUrl.format(lat=lat, lon=lon)
    response = requests.get(url)

    nasaData = response.json()
    nasaData = nasaData['properties']['parameter']
    
    # need to convert dict from Nasa to list
    insolationIncident = list(nasaData['ALLSKY_SFC_SW_DWN'].values())
    diffuseRadiation = list(nasaData['ALLSKY_SFC_SW_DIFF'].values())
    surfAlbedo = list(nasaData['ALLSKY_SRF_ALB'].values())
    optSolIrradiance = list(nasaData['SI_EF_TILTED_SURFACE_OPTIMAL'].values())
    optSolAngle = list(nasaData['SI_EF_TILTED_SURFACE_OPTIMAL_ANG'].values())
    avgTemp = list(nasaData['T2M'].values())

    return {'SI_EF_OPTIMAL' : optSolIrradiance,                         # Solar Irradiance Optimal, kW-hr/m^2/day, 12 months + annual avg
            'SI_EF_OPTIMAL_ANG' : optSolAngle,                          # Solar Irradiance Optimal Angle, Degrees, 12 months + annual avg
            'ALLSKY_SFC_SW_DWN' : insolationIncident,                   # All Sky Insolation Incident on a Horizontal Surface, kW-hr/m^2/day, 12 months + annual avg
            'DIFF' : diffuseRadiation,                                  # Diffuse Radiation On A Horizontal Surface, kW-hr/m^2/day, 12 months + annual avg
            'SRF_ALB' : surfAlbedo,                                     # Surface Albedo, dimensionless, 12 months + annual avg
            'AVG_TEMP' : avgTemp
            }


def Tilt_Value(year, month, day, latitude, longitude, ghi, dhi, albedo, tilt_angle):
    '''
    Creates the solar irradiance value for the equator facing tilted surfaces for a specific a point location and tilt angle. 

    - year: the year value as an integer (required)
    - month: the month value as an integer (required)
    - day: the day value as an integer (required)
    - latitude: the latitude value as an float for the single point data request (required)
    - longitude: the longitude value as an float for the single point data request (required)
    - ghi: the insolation incident on a horizontal surface (ALLSKY_SFC_SW_DWN) value as an float in kW-hr/m^2/day (required)
    - dhi: the diffuse radiation on a horizontal surface (DIFF) value as an float in kW-hr/m^2/day (required)
    - albedo: the surface albedo (SRF_ALB) value as an float (required)
    - tilt_angle: the tilt angle to compute solar irradiance (required)
    '''

    pi = math.acos(-1.0)
    rpd = math.pi/180.0

    def decl(doy):
        return 23.45*math.sin((2*math.pi)*((284.0+float(doy))/365))

    It = int((tilt_angle-(-90.0))/0.5) + 1

    Julian = datetime(1999, month, day).timetuple().tm_yday

    delta = decl(Julian)

    Os = math.acos(max(min(-math.tan(delta*rpd)*math.tan(latitude*rpd), 1.0), -1.0))

    tilt_irradiance = 0.0

    for hour in range(1, 25): # Local Time 1:00 - 24:00
        sunlat = delta
        sunlon = longitude-(hour-12)*15.0
        PHIo = latitude*rpd
        PHIs = sunlat*rpd
        LAMo = longitude*rpd 
        LAMs = sunlon*rpd
        Sx = math.cos(PHIs)*math.sin(LAMs-LAMo)
        Sy = math.cos(PHIo)*math.sin(PHIs)-math.sin(PHIo)*math.cos(PHIs)*math.cos(LAMs-LAMo)
        Sz = math.sin(PHIo)*math.sin(PHIs)+math.cos(PHIo)*math.cos(PHIs)*math.cos(LAMs-LAMo)
        tzh = math.acos(Sz)        # This is the solar zenith angle.
        gsh = math.atan2(-Sx, -Sy) # This is the solar azimuth angle.

        O = (hour-12)*15*rpd

        if(Os-abs(O))>7.5*rpd:  # If 30 min after sunrise and before sunset.
            A = 0.4090+0.5016*math.sin(Os-pi/3)
            B = 0.6609-0.4767*math.sin(Os-pi/3)
            foo = math.sin(Os)-Os*math.cos(Os)

            if foo!=0.0:
                rt = (pi/24)*(A+B*math.cos(O))*(math.cos(O)-math.cos(Os))/foo
                rd = (pi/24)*(math.cos(O)-math.cos(Os))/foo
            else:
                rt = 0.0
                rd = 0.0

            if ghi>0.0 and rt>0.0:
                hrGHI = rt*ghi
            else:
                hrGHI = 0.0

            if dhi>0.0 and rd>0.0 and tzh<(pi/2):
                hrDHI = rd*dhi
                hrBeam = hrGHI-hrDHI
            else:
                hrDHI = 0.0
                hrBeam = 0.0

            bh = (-90.0+(It-1)*0.5)*rpd

            if latitude >= 0.0: # Northern Hemisphere.
                if(bh>=0.0):
                    gh = 0.0
                else:
                    gh = pi

            if latitude < 0.0: # Southern Hemisphere.
                if(bh>=0.0):
                    gh = pi
                else:
                    gh = 0.0

            Kos = math.cos(tzh)*math.cos(abs(bh))+math.sin(tzh)*math.sin(abs(bh))*math.cos(gsh-gh)

            if Kos < 0.0:
                Gc = hrDHI*(1.0+math.cos(abs(bh)))/2+hrGHI*albedo*(1.0-math.cos(abs(bh)))/2
            else:
                Gc = hrBeam*Kos/math.cos(tzh)+hrDHI*(1.0+math.cos(abs(bh)))/2+hrGHI*albedo*(1.0-math.cos(abs(bh)))/2

            if Gc > 0.0:
                tilt_irradiance = tilt_irradiance + Gc
    
    return tilt_irradiance

def calculateTiltIrr(input_lon, input_lat, input_ang, **kwargs):
    nasaData = kwargs.get('nasaData', None)
    if not nasaData:
        nasaData = sendNasaRequest(lon=input_lon, lat=input_lat)
        
    # calculating average tilt angle for each month
    calcIrrMontList = []
    for month in list(range(12)):
        avgCalcTiltIrr = 0
        for day in list(range(daysAmount[month])):
            calcTiltIrr = 1000*Tilt_Value(year=2003,                 # на самом деле, год не влияет на расчет!
                                        month=month+1, 
                                        day=day+1, 
                                        latitude=input_lat, 
                                        longitude=input_lon, 
                                        ghi=nasaData['ALLSKY_SFC_SW_DWN'][month], 
                                        dhi=nasaData['DIFF'][month], 
                                        albedo=nasaData['SRF_ALB'][month], 
                                        tilt_angle=input_ang)
            avgCalcTiltIrr += calcTiltIrr
        avgCalcTiltIrr /= daysAmount[month]
        calcIrrMontList.append(avgCalcTiltIrr)

    return calcIrrMontList, nasaData


def calculate_month_ivc(input_lon: float, input_lat: float, input_ang: float,
              Inom: Sequence[float], Unom: Sequence[float], tC : float, **kwargs):

    Pnom = [Inom[i]*Unom[i] for i in list(range(len(Unom)))]
    mpi = Pnom.index(max(Pnom))
    max_P = Pnom[mpi]
    U_max = Unom[mpi]
    I_max = max_P/U_max
    Efficiency = round(max_P/1000,3)
    
    panel = {
        'IVC':{
            'nom': {'I': Inom, 'U': Unom, 'P': Pnom},
            'month': {}
        },
        'tC':tC,
        'U_max': U_max,
        'I_max': I_max,
        'Efficiency': Efficiency
    }

    [calcIrrMontList, nasaData] = calculateTiltIrr(input_lon=input_lon,
                                                    input_lat=input_lat, 
                                                    input_ang=input_ang,
                                                    **kwargs)
    optIrrMonthList = [i*1000 for i in nasaData['SI_EF_OPTIMAL'][:12]]

    # results to graph: 
    # optimal tilt angle,
    # maximum energy per day achievable from this panel,
    # calculated energy per day achievable from this panel for the input_ang

    optAngMonthList = nasaData['SI_EF_OPTIMAL_ANG'][:12]                        #degrees
    maxMonthEnergy = [i * Efficiency * (1 + tC/100 * (nasaData['AVG_TEMP'][ind] - 20)) for ind, i in enumerate(optIrrMonthList)]                  #Wh/m2/day
    calcMonthEnergy = [i * Efficiency * (1 + tC/100 * (nasaData['AVG_TEMP'][ind] - 20)) for ind, i in enumerate(calcIrrMontList)]                 #Wh/m2/day

    dayLength = [(12 - (24/math.pi) * 
                        math.asin(math.tan(math.radians(input_lat)) * 0.4348 * 
                                            math.cos((i+10)*math.pi*2/365.25))) 
                                                        for i in list(range(365))]              #calculation of daylength versus latitude
    pos = 0
    for ind, month in enumerate(months):
        monthAvgDayLenght = sum(dayLength[pos:(pos+daysAmount[ind])])/daysAmount[ind]           #calculation of average daylength for each month
        pos += daysAmount[ind]  
        coeff = (I_max * U_max - maxMonthEnergy[ind] / monthAvgDayLenght) / U_max          #calculation of UI shift in correspondance to nominal UI @1000 W/m2

        i_month = [i - coeff for i in Inom if i - coeff >= 0]
        u_month = Unom[:(len(i_month))]
        p_month = [i_month[i] * u_month[i] * (1 + tC/100 * (nasaData['AVG_TEMP'][ind] - 20)) for i in range(len(i_month))]
        panel['IVC']['month'][month] = {'I': i_month, 'U': u_month, 'P': p_month}

    panel['E_month'] = {}
    for ind, month in enumerate(months):
        month_E = calcMonthEnergy[ind]
        maxMonth_E = maxMonthEnergy[ind]
        #Устранение погрешности, когда расчетная E > E_max
        panel['E_month'][month] = {'E': min(month_E, maxMonth_E), 'E_max': maxMonth_E}

    return panel


def calculate_ivc(I_max: float, U_max: float, Isc: float, Uoc: float, cell_area: float, cell_count: int):
    I_max = I_max/cell_area
    U_max = U_max/cell_count
    Isc = Isc/cell_area
    Uoc = Uoc/cell_count

    k = 1.38*(10**(-23))
    T = 300.15
    q = 1.6*(10**(-19))    
    def fit_func(U, n, I_0, Rsh):
        return Isc - I_0*np.exp((q*U)/(n*k*T)) - U/Rsh
    
    popt, pcov = curve_fit(fit_func, 
                        [ 0, U_max, Uoc ],
                        [ Isc, I_max, 0 ],
                        #p0 = [0.8, 0.000001, 1],
                        method = 'lm',
                        #bounds = ([0.1,10**(-9), 0.00000001], [0.9,10**(-6),2])
                        )

    Unom = np.linspace(0, Uoc, 100)
    Inom = fit_func(Unom, *popt)
    Pnom = Inom * Unom
    
    return [Unom, Inom, Pnom]

def correct_panel_spec(panel):
    mpi = np.where(panel['IVC']['nom']['P'] == np.max(panel['IVC']['nom']['P']))
    panel['U_max'] = panel['IVC']['nom']['U'][mpi].item()
    panel['I_max'] = panel['IVC']['nom']['I'][mpi].item()
    panel['Efficiency'] = panel['U_max']*panel['I_max']/1000
    del panel['cell_area'], panel['cell_count']
    del panel['Isc'], panel ['Uoc']
    
    return panel

# function to convert Mercator to lon lat https://wiki.gis-lab.info/w/Пересчет_координат_из_Lat/Long_в_проекцию_Меркатора_и_обратно
def LatLongToMerc(lon, lat): 
    rLat = math.radians(lat)
    rLong = math.radians(lon)
    a=6378137.0
    x=a*rLong
    y=a*math.log(math.tan(math.pi/4+rLat/2))
    return [x,y]