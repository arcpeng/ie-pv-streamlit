from pathlib import WindowsPath
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from requests.api import head
import streamlit as st
import requests
from bokeh import events
from bokeh.plotting import figure
from bokeh.models import CrosshairTool, CustomJS, ColumnDataSource, LabelSet, FactorRange
from bokeh.transform import dodge
from bokeh.tile_providers import CARTODBPOSITRON_RETINA, get_provider
from panels import panels
from itertools import cycle
from bokeh.palettes import Dark2_5 as palette
import localiser

from nasaModel import sendNasaRequest, Tilt_Value, calculateTiltIrr, calculate_month_ivc, calculate_ivc, LatLongToMerc, correct_panel_spec

# customization
#st.set_page_config(page_title=None, page_icon=None, layout='wide', initial_sidebar_state='auto')
colors = cycle(palette)

# ==============================
# Session init
# ==============================
empty_panel = { # spec parameters
                'label':None,
                'I_max':None, 'U_max':None, 'Isc':None, 'Uoc':None,
                'cell_area':None, 'cell_count':None,
                'tC':None,
                # calculated parameters
                'IVC':{
                    'nom':{'I':None, 'U':None, 'P':None},
                    'month':{}                                        
                    },
                'Efficiency': None,
                'E_month': {}
                }

def init_session():
    for key in st.session_state.keys():
        del st.session_state[key]
    if 'journal' not in st.session_state:
        st.session_state.journal = pd.DataFrame({'':['','','','', '', '']}, columns = [''], 
                                                index=['I sc, A/cm2',
                                                        'U oc, V',
                                                        'I nominal, A/cm2',
                                                        'U nominal, V',
                                                        'Fill factor, %',
                                                        'Efficiency, %'])
    if 'current_panel' not in st.session_state:
        st.session_state.current_panel = empty_panel
    if 'comparison_panel' not in st.session_state:
        st.session_state.comparison_panel = empty_panel
    if 'results' not in st.session_state:
        st.session_state.results = {}
    if 'coordinates' not in st.session_state:
        st.session_state.coordinates = {'lon':0.00,
                                        'lat':0.00,
                                        'x_Merc':0.00,
                                        'y_Merc':0.00
                                        }
    if 'temperature' not in st.session_state:
        st.session_state.temperature = {

                                        }

# ==============================

local_label = 'local'           #'local' or 'web' in case of using server with api

if local_label == 'web':
    API_URL = 'http://178.154.215.108/solar/panels'
    all_panels = requests.get(API_URL).json()
elif local_label == 'local':
    all_panels = panels

pv_list = []
for panel in all_panels:
    pv_list.append(panel['label'])

def get_ivc(panel_label):
    result = empty_panel.copy()
    if local_label == 'web':
        for panel in all_panels:
            if panel['label']==panel_label:
                req = requests.get(panel['url']).json()
                result.update(req)
                return result
    if local_label == 'local':
        for panel in all_panels:
            if panel['label']==panel_label:
                req = panel["prop"]
                result.update(req)
                return result

# ==============================
# Sidebar
# ==============================
st.sidebar.image('./Images/logo.png')

col1, col2 = st.sidebar.columns([2,1])
col1.markdown(r"<div style='margin-top:55px;text-align:right;'><hr /></div>", unsafe_allow_html=True)
lang = col2.selectbox("", localiser.langs)
text = localiser.td

st.sidebar.markdown('**'+text['name'][lang]+'**')
works = text['works'][lang]
tab_selected = st.sidebar.selectbox(text['sidebar_selector'][lang], works, on_change=init_session)

    
# ==============================
# Main page
# ==============================

header_container = st.container()
for item in works:
    if tab_selected == item:
        with header_container:
            st.title(item)
            '''***'''

if tab_selected == works[0]:
    introduction_container = st.container()
    basics_container = st.container()
    theory_container = st.container()
    whatnext_container = st.container()

    with introduction_container:
        st.markdown(text['work0']['introduction'][lang][0])
        st.markdown(text['work0']['introduction'][lang][1])
        st.markdown('<p style="text-align: center; padding-right:0%; padding-left:0%"><img src="https://raw.githubusercontent.com/MelnikovAP/pv-streamlit/stage_ru/Images/0_Picture_0.png", width=100%/></p>', 
            unsafe_allow_html=True)
        st.markdown(text['work0']['introduction'][lang][2])

    with basics_container:
        st.markdown(text['work0']['basics'][lang][0])
        st.markdown(text['work0']['basics'][lang][1])
        with st.expander(text['work0']['basics'][lang][2]):
            st.markdown('<p style="text-align: center; padding-right:10%; padding-left:10%"><img src="https://raw.githubusercontent.com/MelnikovAP/pv-streamlit/stage_ru/Images/0_Picture_1.png", width=90%/></p>', 
                    unsafe_allow_html=True)
    
    with theory_container:
        st.markdown(text['work0']['theory'][lang][0])
        st.markdown(text['work0']['theory'][lang][1])
        st.markdown(text['work0']['theory'][lang][2])
        st.markdown(text['work0']['theory'][lang][3])
    
    with whatnext_container:
        st.markdown(text['work0']['what_next'][lang][0])
        st.markdown(text['work0']['what_next'][lang][1])

if tab_selected == works[1]:
    st.sidebar.subheader(text['work1']['sidebar_subheader'][lang])
    selected_panel = st.sidebar.selectbox(text['work1']['sidebar_selectbox'][lang], pv_list)

    introduction_container = st.container()
    work_description_container = st.container()
    practice_container = st.container()
    conclusions_container = st.container()

    with introduction_container:
        st.markdown(text['work1']['introduction'][lang][0])
        st.markdown(text['work1']['introduction'][lang][1])
        st.markdown(text['work1']['introduction'][lang][2])
        st.markdown(text['work1']['introduction'][lang][3])
        st.markdown(text['work1']['introduction'][lang][4])
        with st.expander(text['work1']['introduction'][lang][5]):
            st.markdown(text['work1']['introduction'][lang][6])
        with st.expander(text['work1']['introduction'][lang][7]):
            st.markdown(text['work1']['introduction'][lang][8])
        with st.expander(text['work1']['introduction'][lang][9]):
            st.markdown(text['work1']['introduction'][lang][10])
        st.markdown(text['work1']['introduction'][lang][11])
    with work_description_container:
        st.markdown(text['work1']['work_description'][lang][0])
        st.markdown(text['work1']['work_description'][lang][1])

    with practice_container:
        st.markdown(text['work1']['practice'][lang][0])

        if st.sidebar.button(text['work1']['sidebar_button'][lang]):
            st.session_state.current_panel = get_ivc(selected_panel)
            [st.session_state.current_panel['IVC']['nom']['U'], 
            st.session_state.current_panel['IVC']['nom']['I'], 
            st.session_state.current_panel['IVC']['nom']['P']] = calculate_ivc(I_max=st.session_state.current_panel['I_max'], 
                                            U_max=st.session_state.current_panel['U_max'], 
                                            Isc=st.session_state.current_panel['Isc'],
                                            Uoc=st.session_state.current_panel['Uoc'], 
                                            cell_area=st.session_state.current_panel['cell_area'],
                                            cell_count=st.session_state.current_panel['cell_count']
                                            )
            st.session_state.current_panel['IVC']['nom']['I'] *= st.session_state.current_panel['cell_area']
            st.session_state.current_panel['IVC']['nom']['U'] *= st.session_state.current_panel['cell_count']
            st.session_state.current_panel['IVC']['nom']['P'] = st.session_state.current_panel['IVC']['nom']['I']*st.session_state.current_panel['IVC']['nom']['U']
        
        text['work1']['practice'][lang][1], st.session_state.current_panel['label']
        text['work1']['practice'][lang][2], st.session_state.current_panel['cell_count']
        text['work1']['practice'][lang][3], st.session_state.current_panel['cell_area']
        p = figure(title = "I-V зависимость", plot_height=300, 
                    x_axis_label='Напряжение (U), В ', y_axis_label='Сила тока (I), А')
        p.line(st.session_state.current_panel['IVC']['nom']['U'], st.session_state.current_panel['IVC']['nom']['I'], line_width=2)
        p.add_tools(CrosshairTool())
        st.bokeh_chart(p, use_container_width=True)

        p2 = figure(title = "P-V зависимость", plot_height=300, 
                    x_axis_label='Напряжение (U), В ', y_axis_label='Мощность (P), Вт')
        p2.line(st.session_state.current_panel['IVC']['nom']['U'], st.session_state.current_panel['IVC']['nom']['P'], line_width=2)
        p2.add_tools(CrosshairTool())
        st.bokeh_chart(p2, use_container_width=True)

        '''
        По графику зависимости мощности от напряжения определите точку, соответствующую максимуму 
        рабочей мощности выбранной солнечной панели. Данная точка даёт максимум рабочего напряжения 
        в вольтах (В). Чтобы найти максимальный рабочий ток для данной панели, на графике зависимости 
        тока от напряжения необходимо выбрать соответствующую точку.
        '''
        '''
        Для расчёта удельного напряжения и плотности тока, необходимо учитывать 
        последовательное соединение ячеек в солнечной панели, а также их площадь 
        (приведено над графиками). После расчёта данных параметров можно перейти 
        к определению величин коэффициента заполнения вольт-амперной характеристики 
        и эффективности выбранной солнечной панели.
        '''
        '''
        Для получения дополнительной информации обратитесь к разделу **«Введение и элементы теории»**
        '''
        '''
        Проведите предложенное исследование для других типов солнечных панелей и введите полученные результаты
        в таблицу ниже.    
        '''
        '''Сделайте вывод.'''
        with st.expander('Ввести / изменить результаты'):
            '''
            ### Добавить новый результат: 
            '''
            col1, col2, col3 = st.columns(3)
            with col1:
                Isc = st.number_input('Удельная сила тока короткого замыкания (I sc, A/cm2)')
                Inom = st.number_input('Удельная максимальная рабочая сила тока (I nominal, A/cm2)')
            with col2:
                Uoc = st.number_input('Напряжение открытой цепи (U oc, V)')
                Unom = st.number_input('Максимальное рабочее напряжение (U nominal, V)')
            with col3:
                FF = st.number_input('Рассчитаный фактор заполнения, %')
                Eff = st.number_input('Рассчитанный КПД, %')
            if st.button('Добавить результаты'):
                st.session_state.journal[st.session_state.current_panel['label']] = [Isc, Inom, Uoc, Unom, FF, Eff]
            '''
            ---
            '''
            if st.button('Очистить все результаты'):
                st.session_state.journal = pd.DataFrame({'':['','','','', '', '']}, columns = [''], 
                                        index=['I sc, A/cm2',
                                                'U oc, V',
                                                'I nominal, A/cm2',
                                                'U nominal, V',
                                                'Fill factor, %',
                                                'Efficiency, %'])
            if st.button('Очистить последний результат'):
                if st.session_state.current_panel['label'] in st.session_state.journal.keys():
                    del st.session_state.journal[st.session_state.current_panel['label']]

        st.write(st.session_state.journal)
        '''
        ---
        '''
    with conclusions_container:
        with st.expander('Редактировать выводы'):
            entered_conclusion = st.text_input('')
            if st.button('Сохранить'):
                st.session_state.results['conclusion'] = entered_conclusion
        '''
        ### Выводы  
        '''
        if 'conclusion' in st.session_state.results:
            st.write(st.session_state.results['conclusion'])
        '''
        ---
        '''
        '''
        *Вы можете выполнить автоматическую проверку результатов.*
        '''
        if st.button('Проверка результатов'):
            st.session_state.results['conclusion'] = entered_conclusion
            if len(st.session_state.results['conclusion']) < 300:
                st.write('> Выводы не достаточно развернуты!')
            if (len(st.session_state.journal.columns)-1) < 3:
                st.write('> Мало данных. Исследуйте больше типов солнечных панелей')
            else:
                '''> #### Автоматические тесты успешно пройдены.  
                '''
                '''
                *Если требуется, можно распечатать отчет при помощи Ctrl+P (Windows) или Cmd+P (MacOS)*
                '''

if tab_selected == works[2]:
    st.sidebar.subheader('Параметры модели')
    selected_panel = st.sidebar.selectbox('Выберете солнечную панель:', pv_list)
    introduction_container = st.container()
    work_description_container = st.container()
    practice_container = st.container()
    conclusions_container = st.container()

    with introduction_container:
        '''
        ### Введение и элементы теории   
        Солнечный свет проходит путь от Солнца до Земли по прямой линии. Когда 
        он достигает атмосферы, часть света преломляется, часть достигает Земли 
        по прямой линии, а другая часть поглощается атмосферой. Преломлённый 
        свет – это то, что обычно называется диффузной радиацией или рассеянным 
        светом. Та часть солнечного света, которая достигает поверхности Земли 
        без рассеяния или поглощения, является прямой радиацией. Она наиболее 
        интенсивная. Солнечные панели производят электричество и в отсутствие 
        прямого солнечного света. Поэтому даже при облачной погоде фотоэлектрическая 
        система будет производить электричество. Однако наилучшие условия для 
        генерации электроэнергии будут при ярком солнце и при ориентации панелей 
        перпендикулярно солнечному свету. Для северного полушария панели должны 
        быть ориентированы на юг, для южного – на север.
        '''
        '''
        Солнце двигается по небу с Востока на Запад. Положение Солнца на небосклоне 
        определяется двумя координатами – склонением и азимутом (рис. 1). Склонение 
        − это угол между линией, соединяющей наблюдателя и Солнце, и горизонтальной 
        поверхностью. Азимут − это угол между направлением на Солнце и направлением на юг.
        '''
        with st.expander('Рисунок 1. Координаты, определяющие положение Солнца на небосклоне'):
            st.markdown('<p style="text-align: center; padding-right:20%; padding-left:20%"><img src="https://raw.githubusercontent.com/MelnikovAP/pv-streamlit/stage_ru/Images/2_Picture_1.png", width=100%/></p>', 
                unsafe_allow_html=True)
        '''
        На практике солнечные панели должны быть ориентированы под определенным углом 
        к горизонтальной поверхности. Небольшие отклонения от этой ориентации не играют 
        существенной роли, потому что в течение дня Солнце двигается по небу с Востока на 
        Запад. Например, доля выработки энергии фотоэлектрической системой при наклоне 45° 
        для широты местности 52° северной широты:  
        - на запад – 78% 
        - на юго-запад – 94%
        - на юг – 97%  
        - на юго-восток – 94%  
        - на восток – 78%  
        '''
        '''
        Солнечные панели обычно располагаются на крыше или поддерживающей конструкции 
        в фиксированном положении и не могут следить за положением Солнца в течение дня. 
        Поэтому они не находятся под оптимальным углом (90°) в течение всего дня.
        '''
        '''
        Угол между горизонтальной плоскостью и солнечной панелью называют углом наклона. 
        '''
        '''
        Вследствие движения Земли вокруг Солнца имеют место также сезонные вариации угла 
        наклона. Зимой Солнце не достигает того же угла, что и летом. В идеале солнечные 
        панели должны располагаться летом более горизонтально, чем зимой. Поэтому угол 
        наклона для работы летом выбирается меньше, чем для работы зимой. Если нет возможности 
        менять угол наклона дважды в год, то панели должны располагаться под оптимальным углом, 
        значение которого лежит где-то посередине между оптимальными углами для лета и зимы. 
        Для каждой широты есть свой оптимальный угол наклона панелей. Только около экватора 
        солнечные панели должны располагаться горизонтально. 
        '''
        '''
        Для весны и осени оптимальный угол наклона солнечных панелей принимается равным 
        значению широты местности, для зимы − к этому значению прибавляется 10−15°, а летом 
        − от этого значения отнимается 10−15°. Небольшие отклонения до 5о от этого оптимума 
        оказывают незначительный эффект на производительность панелей. Различие в погодных 
        условиях в большей степени влияет на выработку электричества.  
        Для автономных систем оптимальный угол наклона солнечных панелей зависит от месячного 
        графика нагрузки: если в данном месяце потребляется больше энергии, то угол наклона 
        нужно выбирать оптимальным именно для этого месяца. Также нужно учитывать, какое 
        есть затенение в течение дня. Например, если с восточной стороны стоит дерево, а 
        с западной все чисто, то имеет смысл сместить ориентацию с точного юга на юго-запад. 
        '''
        '''
        ---
        '''
    with work_description_container:
        '''
        ### Цель работы
        **Цель** работы заключается в определении зависимости выходных характеристик солнечной 
        панели от её местоположения на нашей планете, а именно от угла наклона солнечной панели 
        относительно падающих солнечных лучей и мощности солнечного излучения.  
        '''
        '''
        ---
        '''
    with practice_container:
        '''
        ### Практическая часть
        В первую очередь выберите слева интересующую Вас солнечную панель и определите 
        угол наклона солнечной панели относительно падающих солнечных лучей, а также установите 
        координаты интересующей Вас местности.  
        '''
        '''
        После нажатия на кнопку «Расчёт» будут выведены зависимости силы тока от напряжения 
        и мощности от напряжения, а также полученная при заданных условиях энергия за каждый месяц года.
        '''
        '''
        Далее решите несколько задач.
        Сделайте вывод.
        '''

        col1, col2 = st.columns(2)
        with col1:
            lon_inp = st.number_input('Долгота', min_value=0.00, max_value=180.00, value=0.00, step=1.0)
        with col2:
            lat_inp = st.number_input('Широта', min_value=-85.00, max_value=85.00, value=0.00, step=1.0)


        if st.button('Установить позицию'):
            st.session_state.coordinates['lon'] = lon_inp
            st.session_state.coordinates['lat'] = lat_inp
            [st.session_state.coordinates['x_Merc'], st.session_state.coordinates['y_Merc']] = LatLongToMerc(lon_inp, lat_inp)   

        tile_provider = get_provider(CARTODBPOSITRON_RETINA)
        # range bounds supplied in web mercator coordinates
        p = figure(x_range=(st.session_state.coordinates['x_Merc']-7000000, st.session_state.coordinates['x_Merc']+7000000), 
                    y_range=(st.session_state.coordinates['y_Merc']-7000000, st.session_state.coordinates['y_Merc']+7000000),
                    x_axis_type="mercator", y_axis_type="mercator")
        p.add_tile(tile_provider)
        p.scatter(x=st.session_state.coordinates['x_Merc'], y=st.session_state.coordinates['y_Merc'], marker="circle", size=25, alpha=0.3, color='red')
        p.scatter(x=st.session_state.coordinates['x_Merc'], y=st.session_state.coordinates['y_Merc'], marker="cross", size=35, color='red')
        p.scatter(x=st.session_state.coordinates['x_Merc'], y=st.session_state.coordinates['y_Merc'], marker="circle", size=10, alpha=0.3, color='red')
        p.add_tools(CrosshairTool())
        # add here callback event https://docs.bokeh.org/en/latest/docs/user_guide/interaction/callbacks.html
        # p.js_on_event(events.DoubleTap, callback)
        st.bokeh_chart(p, use_container_width=True)  

        input_ang = st.sidebar.number_input('Угол поворота', min_value=0.0, max_value=90.0, value=0.0, step = 1.0)
        

        if st.sidebar.button('Расчёт'):
            st.session_state.current_panel = get_ivc(selected_panel)
            [st.session_state.current_panel['IVC']['nom']['U'], 
            st.session_state.current_panel['IVC']['nom']['I'], 
            st.session_state.current_panel['IVC']['nom']['P']] = calculate_ivc(I_max=st.session_state.current_panel['I_max'], 
                                            U_max=st.session_state.current_panel['U_max'], 
                                            Isc=st.session_state.current_panel['Isc'],
                                            Uoc=st.session_state.current_panel['Uoc'], 
                                            cell_area=st.session_state.current_panel['cell_area'],
                                            cell_count=st.session_state.current_panel['cell_count']
                                            )
            st.session_state.current_panel['IVC']['nom']['P'] = st.session_state.current_panel['IVC']['nom']['I']*st.session_state.current_panel['IVC']['nom']['U']
        
            new_panel = calculate_month_ivc(input_lon=st.session_state.coordinates['lon'], 
                                        input_lat=st.session_state.coordinates['lat'], 
                                        input_ang=input_ang,
                                        Inom=st.session_state.current_panel['IVC']['nom']['I'], 
                                        Unom=st.session_state.current_panel['IVC']['nom']['U'],
                                        tC = 0
                                        )
            st.session_state.current_panel.update(new_panel)


        '**Выбранная панель: **', st.session_state.current_panel['label']
        p = figure(title = "I-V зависимость", plot_height=400, 
                    x_axis_label='Напряжение (U), V ', y_axis_label='Сила тока (I), A')
        p2 = figure(title = "P-V зависимость", plot_height=400, 
                    x_axis_label='Напряжение (U), V ', y_axis_label='Мощность (P), W')
        
        p.line(st.session_state.current_panel['IVC']['nom']['U'], st.session_state.current_panel['IVC']['nom']['I'], 
                line_width=2, legend_label='MAX')
        p2.line(st.session_state.current_panel['IVC']['nom']['U'], st.session_state.current_panel['IVC']['nom']['P'], 
                line_width=2, legend_label='MAX')

        for key, value in st.session_state.current_panel['IVC']['month'].items():
            color = next(colors)
            p.line(value['U'], value['I'], color=color, legend_label=key)
            p2.line(value['U'], value['P'], color=color, legend_label=key)
        
        for i in [p, p2]:
            i.legend.location = "top_left"
            i.legend.click_policy="hide"
            i.add_tools(CrosshairTool())
            st.bokeh_chart(i, use_container_width=True)    

        if len(st.session_state.current_panel['E_month']) > 0:
            [E_max, E_avg, months] = zip(*[(value['E_max'], value['E'], key) for key, value in st.session_state.current_panel['E_month'].items()])
        else: [E_max, E_avg, months] = [[],[],[]]
        data = {'months':months, 'E_max':E_max, 'E_avg':E_avg}
        source = ColumnDataSource(data=data)
        
        p3 = figure(x_range=months, plot_height=400, title="Среднемесячная выработка энергии",
                    x_axis_label='Месяц', y_axis_label='Энергия, кВт*ч')
        p3.vbar(x=dodge('months', -0.2, range=p3.x_range), top='E_max', width=0.4, source=source,
                    color="#c9d9d3", legend_label="Максимум")
        p3.vbar(x=dodge('months', 0.2, range=p3.x_range), top='E_avg', width=0.4, source=source,
                    color="#718dbf", legend_label="Расчёт")
        p3.x_range.range_padding = 0.1
        p3.y_range.start = 1
        if len(E_max)>0: p3.y_range.end = max(E_max)*1.2 
        p3.legend.click_policy="hide"
        p3.legend.orientation = "horizontal"
        p3.add_tools(CrosshairTool())
        st.bokeh_chart(p3, use_container_width=True)

        with st.expander('Задача 1'):
            '''
            Предположим, что в Сколково в окрестностях точки с координатами:  
            > *55.69553° с. ш.*  
            > *37.35298° в. д.*  

            планируют построить новое здание, крыша которого будет оборудована монокристаллическими 
            солнечными панелями. Существует четыре проекта здания, которые в том числе отличаются углом 
            наклона кровли, а именно: 16°, 24°, 32° и 43°. Определите, какой из вариантов является наиболее 
            оптимальным с точки зрения эффективности работы солнечных панелей. Считайте, что солнечные 
            панели находятся под таким же углом наклона, что и кровля.  
            '''

            answer_1 = st.number_input('Ответ в виде целого числа:', step=1)
            st.session_state.results['answer_1'] = answer_1
        with st.expander('Задача 2'):
            '''
            Гипотетически существующая компания «друзья Солнца» занимается строительством солнечных 
            электростанций. Компания использует органические солнечные панели, которые крепятся на стойках, 
            обеспечивающих положение панели под углом 45° к горизонту. Для строительства очередной электростанции 
            с 500 солнечных панелей компания рассматривает несколько возможных площадок, а именно:  '''
            '''
            (1) В окрестностях ВДЦ «Смена»
            > *44.7831° с. ш.*  
            > *37.3946° в. д.*  

            (2) в окрестностях города Оренбург  
            > *51.8643° с. ш.*  
            > *55.1015° в. д.*  

            (3) в окрестностях города Горно-Алтайск  
            > *51.9791° с. ш.*  
            > *85.9813° в. д.*  
            '''
            '''
            Оцените, при строительстве на какой из этих площадок средняя в течение года генерируемая электростанцией мощность будет максимальной.
            '''
            answer_2 = st.selectbox('Выбранный вариант ответа:', [1,2,3])
            st.session_state.results['answer_2'] = answer_2
        with st.expander('Задача 3'):
            '''
            Фонтаны Петергофа известны своей красотой и разнообразием не только у нас в стране, но и далеко за её пределами. 
            Ежегодно ими любуются миллионы туристов. Однако для обеспечения работы насосов фонтанов, необходимо регулярно 
            поддерживать электрические сети Петергофа в очень хорошем состоянии, что достаточно сложно сделать в городе, где 
            такая высокая плотность архитектурных памятников и объектов культурного наследия. Предположим, что для повышения 
            энергетической безопасности на некоторых кровлях зданий Петергофа решено установить солнечные панели. Поскольку 
            площадь панелей сильно ограничена, необходимо установить самые эффективные, дающие максимальное количество 
            электроэнергии в период работы фонтанов - с мая по сентябрь. Определите, какого типа солнечные панели стоит 
            использовать в этом проекте.  
            Примерные географические координаты зданий, на которых планируется разместить солнечные панели:
            > *59.879° с. ш.*  
            > *29.898° в. д.*  
            
            Угол наклона крыш, который совпадает с углом наклона солнечных панелей к солнцу, считайте равным 30°.  
            '''
            answer_3 = st.selectbox('Выбранная солнечная панель:', pv_list)
            st.session_state.results['answer_3'] = answer_3
        with st.expander('Задача 4'):
            '''
            Вам необходимо разработать энергосистему, которая состоит из поликристаллических солнечных панелей, 
            может быть установлена в окрестностях города Ростов-на-Дону:  
            > *47.15623° с. ш.*  
            > *39.56059° в. д.*  

            и обеспечивает следующие средние выходные параметры:  
            > Постоянное напряжение - *400 В*  
            > Мощность - *2 кВт*  

            Оцените, какое минимальное количество поликристаллических панелей Вам для этого необходимо и
            как необходимо соединить их между собой. 
            '''
            answer_4_1 = st.number_input('Введите общее количество панелей:', step=1)
            st.session_state.results['answer_4_1'] = answer_4_1
            answer_4_2 = st.number_input('Из них последовательно соединенных в одном блоке:', step=1)
            st.session_state.results['answer_4_2'] = answer_4_2
            answer_4_3 = st.number_input('Количество параллельно соединенных блоков:', step=1)
            st.session_state.results['answer_4_3'] = answer_4_3
            '''
            *Примечание:*  
            Панели соединены в блоки, состоящие из *последовательно* соединенных панелей. 
            Данные блоки соединены *параллельно*
            '''
        '''
        ---
        '''
    with conclusions_container:
        with st.expander('Редактировать выводы'):
            entered_conclusion = st.text_input('')
            if st.button('Сохранить'):
                st.session_state.results['conclusion'] = entered_conclusion
        '''
        ### Выводы  
        '''
        if 'conclusion' in st.session_state.results:
            st.write(st.session_state.results['conclusion'])
        '''
        ---
        '''
        '''
        *Вы можете выполнить автоматическую проверку результатов.*
        '''
        if st.button('Проверка результатов'):
            st.session_state.results['conclusion'] = entered_conclusion
            if len(st.session_state.results['conclusion']) < 300:
                st.write('> Выводы не достаточно развернуты!')
            elif st.session_state.results['answer_1']!=1:
                st.write('> Проверьте ответ к задаче 1!')
            elif st.session_state.results['answer_2']!=1:
                st.write('> Проверьте ответ к задаче 2!')
            elif st.session_state.results['answer_3']!='Монокристаллическая':
                st.write('> Проверьте ответ к задаче 3!')
            elif st.session_state.results['answer_4_1']!=1 and \
            st.session_state.results['answer_4_2']!=1 and \
            st.session_state.results['answer_4_3']!=1:
                st.write('> Проверьте ответ к задаче 4!')           
            else:
                '''> #### Автоматические тесты успешно пройдены.  
                '''
                '''
                *Если требуется, можно распечатать отчет при помощи Ctrl+P (Windows) или Cmd+P (MacOS)*
                '''

if tab_selected == works[3]:
    st.sidebar.subheader('Параметры модели')
    selected_panel = st.sidebar.selectbox('Выберете солнечную панель:', pv_list)
    introduction_container = st.container()
    work_description_container = st.container()
    practice_container = st.container()
    conclusions_container = st.container()

    with introduction_container:
        '''
        ### Введение и элементы теории   
        Солнечные модули, как и остальное электронное оборудование, работают за 
        счёт электрических процессов, подконтрольных законам термодинамики. 
        А законы термодинамики гласят, что с ростом тепла снижается мощность. 
        Повышение температуры создаёт внутреннее сопротивление внутри солнечного 
        элемента, что снижает его эффективность. То есть с ростом температуры поток 
        электронов внутри элемента нарастает, что вызывает увеличение силы тока и падение 
        напряжения. Падение напряжения при этом больше, чем увеличение силы тока, поэтому 
        общая мощность уменьшается, что приводит к тому, что панель работает с меньшей 
        эффективностью, то есть её КПД становится ниже. Поэтому чем теплее температура 
        окружающей среды, тем меньше выходная мощность фотоэлементов. 
        '''
        '''
        Потери определяются **«температурным коэффициентом»**. 
        **Температурный коэффициент** − это процент снижения эффективности с привязкой 
        к градусам по Цельсию. Он показывает, насколько падает эффективность солнечной 
        панели при повышении температуры воздуха на градус. Значение коэффициента 
        производитель панелей получают опытным путем (и указывают в спецификациях). 
        Оно разнится в зависимости от модели солнечной панели.
        '''
        '''
        Тестирование параметров солнечных панелей проводится при температуре 25°C и 
        обычно производители указывают их эффективность, принимая за норму 25°C.
        Если температурный коэффициент солнечной панели -0.50, это означает, что выход 
        мощности снизится на 0,50% за каждый градус выше 25°C. Несмотря на то, что такая 
        цифра кажется незначительной, температура тёмной крыши, на которой установлена панель, 
        может быть значительно выше 25°C в жаркий солнечный день. В летний период собственная 
        температура солнечной батареи может подниматься до 60−70°C. В среднем при повышении 
        температуры панели на 20°C, потери мощности составят порядка 10%. 
        '''
        '''
        Тепловой коэффициент кремниевых поли- и монокристаллических панелей в среднем 
        колеблется от -0.45% до -0.50%. Тепловой коэффициент аморфных солнечных панелей ниже 
        (от -0,20% до -0,25%), однако их изначальная эффективность ниже, чем у моно- и поликристаллических.
        Если повышение температуры способствует снижению КПД солнечных панелей, 
        то некоторое понижение температуры может, наоборот, увеличить эффективность солнечных 
        элементов: напряжение может быть даже выше номинального. 
        '''
        '''
        ---
        '''
    with work_description_container:
        '''
        ### Цель работы
        **Цель** работы заключается в определении зависимости выходных характеристик солнечной 
        панели от её местоположения на нашей планете, а именно от угла наклона солнечной панели 
        относительно падающих солнечных лучей, мощности солнечного излучения и температуры солнечных панелей.
        '''
        '''
        ---
        '''
    with practice_container:
        '''
        ### Практическая часть
        В первую очередь выберите слева интересующую Вас солнечную панель и определите угол наклона солнечной 
        панели относительно падающих солнечных лучей, а также установите координаты интересующей 
        Вас местности. После нажатия на кнопку «Расчёт» будет выведена полученная при заданных условиях 
        энергия за каждый месяц года.
        '''
        '''
        Далее решите несколько задач.
        Сделайте вывод.
        '''

        col1, col2 = st.columns(2)
        with col1:
            lon_inp = st.number_input('Долгота', min_value=0.00, max_value=180.00, value=0.00, step=1.0)
        with col2:
            lat_inp = st.number_input('Широта', min_value=-85.00, max_value=85.00, value=0.00, step=1.0)


        if st.button('Установить позицию'):
            st.session_state.coordinates['lon'] = lon_inp
            st.session_state.coordinates['lat'] = lat_inp
            [st.session_state.coordinates['x_Merc'], st.session_state.coordinates['y_Merc']] = LatLongToMerc(lon_inp, lat_inp)   

        tile_provider = get_provider(CARTODBPOSITRON_RETINA)
        # range bounds supplied in web mercator coordinates
        p = figure(x_range=(st.session_state.coordinates['x_Merc']-7000000, st.session_state.coordinates['x_Merc']+7000000), 
                    y_range=(st.session_state.coordinates['y_Merc']-7000000, st.session_state.coordinates['y_Merc']+7000000),
                    x_axis_type="mercator", y_axis_type="mercator")
        p.add_tile(tile_provider)
        p.scatter(x=st.session_state.coordinates['x_Merc'], y=st.session_state.coordinates['y_Merc'], marker="circle", size=25, alpha=0.3, color='red')
        p.scatter(x=st.session_state.coordinates['x_Merc'], y=st.session_state.coordinates['y_Merc'], marker="cross", size=35, color='red')
        p.scatter(x=st.session_state.coordinates['x_Merc'], y=st.session_state.coordinates['y_Merc'], marker="circle", size=10, alpha=0.3, color='red')
        p.add_tools(CrosshairTool())
        # add here callback event https://docs.bokeh.org/en/latest/docs/user_guide/interaction/callbacks.html
        # p.js_on_event(events.DoubleTap, callback)
        st.bokeh_chart(p, use_container_width=True)  

        input_ang = st.sidebar.number_input('Угол наклона', min_value=0.0, max_value=90.0, value=0.0, step = 1.0)
        

        if st.sidebar.button('Расчёт'):
            st.session_state.current_panel = get_ivc(selected_panel)
            [st.session_state.current_panel['IVC']['nom']['U'], 
            st.session_state.current_panel['IVC']['nom']['I'], 
            st.session_state.current_panel['IVC']['nom']['P']] = calculate_ivc(I_max=st.session_state.current_panel['I_max'], 
                                            U_max=st.session_state.current_panel['U_max'], 
                                            Isc=st.session_state.current_panel['Isc'],
                                            Uoc=st.session_state.current_panel['Uoc'], 
                                            cell_area=st.session_state.current_panel['cell_area'],
                                            cell_count=st.session_state.current_panel['cell_count']
                                            )
            st.session_state.current_panel['IVC']['nom']['P'] = st.session_state.current_panel['IVC']['nom']['I']*st.session_state.current_panel['IVC']['nom']['U']
        
            new_panel = calculate_month_ivc(input_lon=st.session_state.coordinates['lon'], 
                                        input_lat=st.session_state.coordinates['lat'], 
                                        input_ang=input_ang,
                                        Inom=st.session_state.current_panel['IVC']['nom']['I'], 
                                        Unom=st.session_state.current_panel['IVC']['nom']['U'],
                                        tC = st.session_state.current_panel['tC']
                                        )
            st.session_state.current_panel.update(new_panel)

            new_panel_comparison = calculate_month_ivc(input_lon=st.session_state.coordinates['lon'], 
                                        input_lat=st.session_state.coordinates['lat'], 
                                        input_ang=input_ang,
                                        Inom=st.session_state.current_panel['IVC']['nom']['I'], 
                                        Unom=st.session_state.current_panel['IVC']['nom']['U'],
                                        tC = 0
                                        )
            st.session_state.comparison_panel.update(st.session_state.current_panel)
            st.session_state.comparison_panel.update(new_panel_comparison)

        '**Выбранная панель: **', st.session_state.current_panel['label']
        p = figure(title = "I-V зависимость", plot_height=400, 
                    x_axis_label='Напряжение (U), V ', y_axis_label='Сила тока (I), A')
        p2 = figure(title = "P-V зависимость", plot_height=400, 
                    x_axis_label='Напряжение (U), V ', y_axis_label='Мощность (P), W')
        
        for key, value in st.session_state.current_panel['IVC']['month'].items():
            color = next(colors)
            p.line(value['U'], value['I'], color=color, legend_label=key)
            p2.line(value['U'], value['P'], color=color, legend_label=key)
            if st.session_state.comparison_panel['IVC']['month']:
                p.line(st.session_state.comparison_panel['IVC']['month'][key]['U'], 
                        st.session_state.comparison_panel['IVC']['month'][key]['I'], 
                        color=color, legend_label=key, line_dash='dashed')
                p2.line(st.session_state.comparison_panel['IVC']['month'][key]['U'], 
                        st.session_state.comparison_panel['IVC']['month'][key]['P'], 
                        color=color, legend_label=key, line_dash='dashed')
        
        for i in [p, p2]:
            i.legend.location = "top_left"
            i.legend.click_policy="hide"
            i.add_tools(CrosshairTool())
            st.bokeh_chart(i, use_container_width=True)


        if len(st.session_state.current_panel['E_month']) > 0:
            [E_max, E_avg, months] = zip(*[(value['E_max'], value['E'], key) for key, value in st.session_state.comparison_panel['E_month'].items()])
            E_cor = [item['E'] for item in st.session_state.current_panel['E_month'].values()]
        else: [E_max, E_avg, months, E_cor] = [[],[],[],[]]
        data = {'months':months, 'E_max':E_max, 'E_avg':E_avg, 'E_cor':E_cor}
        source = ColumnDataSource(data=data)

        p3 = figure(x_range=months, plot_height=400, title="Среднемесячная выработка энергии",
                    x_axis_label='Месяц', y_axis_label='Энергия, кВт*ч')
        p3.vbar(x=dodge('months', -0.2, range=p3.x_range), top='E_max', width=0.2, source=source,
                    color="#c9d9d3", legend_label="Максимум")
        p3.vbar(x=dodge('months', 0, range=p3.x_range), top='E_avg', width=0.2, source=source,
                    color="#718dbf", legend_label="Расчёт")
        p3.vbar(x=dodge('months', 0.2, range=p3.x_range), top='E_cor', width=0.2, source=source,
                    color="#e84d60", legend_label="Коррекция")

        p3.x_range.range_padding = 0.1
        p3.y_range.start = 1
        if len(E_max)>0: p3.y_range.end = max(E_max)*1.2 
        p3.legend.click_policy="hide"
        p3.legend.orientation = "horizontal"
        p3.add_tools(CrosshairTool())
        st.bokeh_chart(p3, use_container_width=True)

        with st.expander('Задача 1'):
            '''
            На Самарской солнечной электростанции с координатами:  
            > *53.01° с. ш.*  
            > *49.80° в. д.*  

            используются монокристаллические солнечные панели. Определите (с точностью до единиц), 
            какой процент электроэнергии теряется летом за счет нагрева солнечный панелей окружающим 
            воздухом. Считайте, что угол положения солнечных панелей оптимальный. 
            '''

            answer_1 = st.number_input('Процент потерянной электроэнергии:', step=1)
            st.session_state.results['answer_1'] = answer_1
        with st.expander('Задача 2'):
            '''
            В предыдущей работе рассматривалась задача, в которой гипотетически существующая 
            компания «друзья Солнца» рассматривает для строительства очередной электростанции 
            с 500 солнечных панелей несколько возможных площадок, а именно:   '''
            '''
            (1) В окрестностях ВДЦ «Смена»
            > *44.7831° с. ш.*  
            > *37.3946° в. д.*  

            (2) в окрестностях города Оренбург  
            > *51.8643° с. ш.*  
            > *55.1015° в. д.*  

            (3) в окрестностях города Горно-Алтайск  
            > *51.9791° с. ш.*  
            > *85.9813° в. д.*  
            '''
            '''
            Оцените, при строительстве на какой из этих площадок с учетом влияния температуры 
            окружающего воздуха средняя в течение года генерируемая электростанцией мощность будет 
            максимальной. На электростанции планируется использовать органические солнечные панели, 
            которые крепятся на стойках, обеспечивающих положение панели под углом 45° к горизонту. 
            '''
            answer_2 = st.selectbox('Выбранный вариант ответа: ', [1,2,3])
            st.session_state.results['answer_2'] = answer_2
        with st.expander('Задача 3'):
            '''
            До сих пор у нас на планете есть большое количество мест, которые еще ждут своего 
            освоения и где практически не живут люди. Среди таких мест многие представляют интерес 
            для археологов, которые отправляются в экспедиции в такие места. Для обеспечения 
            быта археологов им необходима электроэнергия. Если речь идет об Арктической экспедиции, 
            которая выпадает на “полярный день”, то можно рассмотреть возможность использования 
            солнечных панелей в качестве источника электроэнергии.  
            '''
            '''
            Рассмотрим гипотетическую экспедицию в места распространения Усть-полуйской культуры, 
            представители которой проживали на территории полуострова Ямал. Считая, что экспедиция 
            будет проводится в июне, а лагерь археологов будет находится в точке с координатами: 
            > *65.557° с. ш.*  
            > *69.074° в. д.*  

            определите, какого типа солнечные панели стоит взять археологам для того, чтобы они 
            обладали наибольшей эффективностью с учетом влияния температуры окружающего воздуха 
            на их работу. Считайте, что угол положения солнечных панелей оптимальный. 
            '''
            answer_3 = st.selectbox('Выбранная солнечная панель: ', pv_list)
            st.session_state.results['answer_3'] = answer_3
        '''
        ---
        '''
    with conclusions_container:
        with st.expander('Редактировать выводы'):
            entered_conclusion = st.text_input('')
            if st.button('Сохранить'):
                st.session_state.results['conclusion'] = entered_conclusion
        '''
        ### Выводы  
        '''
        if 'conclusion' in st.session_state.results:
            st.write(st.session_state.results['conclusion'])
        '''
        ---
        '''
        '''
        *Вы можете выполнить автоматическую проверку результатов.*
        '''
        if st.button('Проверка результатов'):
            st.session_state.results['conclusion'] = entered_conclusion
            if len(st.session_state.results['conclusion']) < 300:
                st.write('> Выводы не достаточно развернуты!')
            elif st.session_state.results['answer_1']!=1:
                st.write('> Проверьте ответ к задаче 1!')
            elif st.session_state.results['answer_2']!=1:
                st.write('> Проверьте ответ к задаче 2!')
            elif st.session_state.results['answer_3']!='Монокристаллическая':
                st.write('> Проверьте ответ к задаче 3!')        
            else:
                '''> #### Автоматические тесты успешно пройдены.  
                '''
                '''
                *Если требуется, можно распечатать отчет при помощи Ctrl+P (Windows) или Cmd+P (MacOS)*
                '''

if tab_selected == works[4]:
    whatnext_container = st.container()

    with whatnext_container:
        '''
        ### Литература
        '''
        '''
        - *Возобновляемая энергетика в современном мире: Учебное пособие* / 
        О. С. Попель, В. Е. Фортов – 2-е изд., стер. – М: Издательский дом 
        МЭИ, 2018. – 450 с.: ил.  
        - *Энергетика в современном мире: Научное издание* / В. Е. Фортов, 
        О. С. Попель – Долгопрудный: Издательский Дом «Интеллект», 2011. – 168 с.  
        - *Изучение солнечных фотоэлектрических элементов: Учебно-методическое 
        пособие* / Бессель В. В., Кучеров В. Г., Мингалеева Р. Д. – М.: Издательский 
        центр РГУ нефти и газа (НИУ) имени И. М. Губкина, 2016. – 90 с.  
        '''
        '''
        ### Web-ресурсы
        '''
        '''
        - [Пост.Наука: Солнечная энергия](https://postnauka.ru/themes/solnechnaya-energiya)  
        - [Wiki: Солнечная энергетика](https://ru.wikipedia.org/wiki/Солнечная_энергетика)  
        - [Wiki: Солнечная генерация](https://ru.wikipedia.org/wiki/Солнечная_генерация)  
        - [Wiki: Солнечная батарея](https://ru.wikipedia.org/wiki/Солнечная_батарея)
        - [Wiki: Полимерная солнечная батарея](https://ru.wikipedia.org/wiki/Полимерные_солнечные_батареи)
        - [Richard Komp: How do solar panels work?](https://www.youtube.com/watch?v=xKxrkht7CpY)
        - [Lesics: How do solar cells work?](https://www.youtube.com/watch?v=L_q6LRgKpTw)
        '''

