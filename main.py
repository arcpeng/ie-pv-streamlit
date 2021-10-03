from pathlib import WindowsPath
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from requests.api import head
import streamlit as st
import requests
from bokeh import events
from bokeh.plotting import figure
from bokeh.models import CrosshairTool, CustomJS, ColumnDataSource, LabelSet
from bokeh.tile_providers import CARTODBPOSITRON_RETINA, get_provider
from panels import panels
from itertools import cycle
from bokeh.palettes import Dark2_5 as palette

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
                    'month':{}                                        },
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

works = ['Введение', 
        'Работа №1: Понимание поляризационных кривых', 
        'Работа №2: Влияние координат', 
        'Работа №3: Изучение эффекта температуры',
        'Работа №4: Спектральный эффект',
        'Рекомендации']

# ==============================
# Sidebar
# ==============================
st.sidebar.image('./Images/logo.png')
st.sidebar.markdown('***')
st.sidebar.markdown('''
Цифровой стенд  
**Солнечная энергетика**
''')
tab_selected = st.sidebar.selectbox('Выберете работу:', works, on_change=init_session)

if tab_selected != works[0]:
    st.sidebar.subheader('Параметры модели')
    selected_panel = st.sidebar.selectbox('Выберете солнечную панель:', pv_list)
    
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
    scheme_container = st.container()
    basics_container = st.container()
    theory_container = st.container()
    whatnext_container = st.container()

    with introduction_container:
        '''
        Первыми живыми организмами на земле, которые научились напрямую 
        поглощать солнечную энергию и накапливать ее, были, скорее всего, 
        растения. Энергию, которую переносит солнечный свет от единственной 
        звезды нашей системы — Солнца, растения используют при фотосинтезе, 
        улавливая углекислый газ из атмосферы и возвращая в нее кислород. 
        Углерод при этом остается в растении, формирую его *«зеленую массу»*. 
        Но солнечная энергия преобразуется не только в энергию химических 
        связей в растениях. Практически вся энергия на нашей планете так или 
        иначе связана с солнечной активностью, и человек научился преобразовывать 
        её в электрическую.  
        '''
        '''
        Из-за разницы температур воздушных масс возникает разность давления и 
        появляется ветер, который может крутить лопасти ветрогенератора. Нагревая 
        землю и водные ресурсы планеты, солнцем в атмосферу выпаривается огромное 
        количество воды, которая переносится на сотни и тысячи километров, выпадая 
        в виде осадков или замерзая в ледниках. Потоки воды образуют реки, а человек 
        снова извлекает из этого пользу, используя гидроэлектростанции.
        '''
        st.markdown('<p style="text-align: center; padding-right:0%; padding-left:0%"><img src="https://raw.githubusercontent.com/MelnikovAP/pv-streamlit/stage_ru/Images/0_Picture_0.png", width=100%/></p>', 
            unsafe_allow_html=True)
        '''
        С конца **XIX века**, когда учёные открыли фотоэлектрический эффект, у 
        человечества появился способ прямого преобразования солнечного света 
        в электричество. Важность технологии получения электричества напрямую 
        от солнечного света и понимание принципов, лежащих в ее основе, нашли 
        свое отражение и в, пожалуй, самой известной награде в области науки – 
        Нобелевской премии. В течение **XX века** различные учёные, работы которых 
        важны для данной технологии, несколько раз получали Нобелевские премии. 
        К концу **50-х годов XX века** были разработаны устройства – солнечные панели, 
        которые позволяли получать электроэнергию в достаточном количестве для работы 
        маломощных устройств. Практически сразу же солнечные панели нашли свое 
        применение в разнообразных космических аппаратах. В этой области солнечные 
        панели оказались незаменимыми. К началу **XXI века** технологии солнечных панелей 
        развились достаточно для того, чтобы найти себе промышленное применение в 
        земных условиях. По состоянию на сегодняшний день есть отдельные регионы 
        (например, на некоторых территориях Индии), где строительство электростанции, 
        состоящей из солнечных панелей, является самым дешевым и эффективным способом 
        электрификации местности. Даже в нашей, казалось бы, достаточно северной и не 
        самой солнечной стране введен в эксплуатацию целый ряд электростанций на 
        солнечных панелях.
        ***
        '''
        
        '''
        ### Принцип работы солнечной панели  
        '''
        '''
        Давайте разберём, как же работает солнечная панель.  
        '''
        
    with basics_container:
        '''
        Принцип работы фотоэлементов, из которых состоит солнечная панель основан 
        на фотогальваническом эффекте, который заключается в возникновении напряжения 
        или электрического тока в веществе под действием света.  
        '''
    with scheme_container:
        with st.expander('Рисунок 1. Принципиальная схема фотоэлемента'):
            st.markdown('<p style="text-align: center; padding-right:10%; padding-left:10%"><img src="https://raw.githubusercontent.com/MelnikovAP/pv-streamlit/stage_ru/Images/0_Picture_1.png", width=90%/></p>', 
                    unsafe_allow_html=True)
        
    with theory_container:
        '''
        Фотоэлемент на основе полупроводников состоит из двух очень тонких слоев 
        (чтобы они были проницаемы для фотонов) толщиной обычно порядка 0,2 мм с 
        разным типом проводимости, совместно образующих так называемый *p-n-переход*. 
        К слоям с разных сторон подведены металлические контакты, которые подключены 
        к внешней цепи. Роль катода играет слой с *n-проводимостью* (применяется 
        материал с избытком валентных электронов, то есть характеризуемый электронной 
        проводимостью), роль анода – *p-слой* (материал с дырочной проводимостью; 
        «дырка» – это квазичастица, в данном контексте это условное «место» в веществе 
        где нет электрона, но в котором электрон может оказаться; направленное движение 
        электронов, когда они занимают такие «свободные» места, принято называть 
        электрическим током в веществе с дырочной проводимостью).
        '''
        '''
        При поглощении фотона в веществе может появится «пара» - «валентный» электрон 
        и «дырка». Упрощенно можно считать, что при поглощении фотона его энергия 
        идет на то, чтобы «выбить» электрон из того «места», которое он занимал в 
        веществе, в результате чего и образуется такая «пара». На границе внутри 
        *p-n-перехода* есть небольшое электрическое поле. Такой эффект имеет место 
        при контакте между любыми двумя веществами и в случае проводников называется 
        контактной разностью потенциалов. Оказавшись в области, где действует такое 
        электрическое поле, «пара» может «распасться» и под действием электрического 
        поля электрон и «дырка» окажутся по разные стороны от границы.
        '''
        '''
        В результате такого процесса в *n-* и *p-областях* накапливаются электроны 
        и дырки соответственно, что означает, что между этими областями есть разность 
        потенциалов. Замкнув цепь с помощью металлических контактов и внешней цепи 
        можно получить электрический ток.
        '''
        '''
        Величина потенциала, достигаемая на одном фотоэлементе на основе кремния, 
        маленькая и составляет около **0,5 В**, а сила тока через фотоэлемент изменяется 
        пропорционально его площади и количеству поглощенных им фотонов. 
        Для получения солнечных панелей с достаточным для практических целей напряжением, 
        единичные фотоэлементы соединяют последовательно в нужном количестве 
        (обычно несколько десятков элементов), а для повышения силы тока – параллельно 
        или сразу производят фотоэлемент с большой площадью поверхности. Таким образом,
        комбинируя соединения, можно добиться требуемых параметров по силе тока и 
        напряжению, а следовательно, и по мощности.  
        ***
        '''
    with whatnext_container:
        '''
        ### Дальнейшие шаги
        '''
        '''
        Пожалуйста, выберете работу на панели слева.  
        рекомендуемый список литературы и полезные web-ресурсы можно найти во вкладке "Рекомендации"
        '''

if tab_selected == works[1]:
    introduction_container = st.container()
    work_description_container = st.container()
    practice_container = st.container()
    conclusions_container = st.container()

    with introduction_container:
        '''
        ### Введение и элементы теории  
    
        *Here add text*  
        '''
        with st.expander('Монокристаллическая солнечная панель'):
            '''
            *Here add text* 
            '''
        with st.expander('Поликристаллическая солнечная панель'):
            '''
            *Here add text*  
            '''
        with st.expander('Органическая солнечная панельl'):
            '''
            *Here add text*  
            '''
        '''  
        ---
        '''
    with work_description_container:
        '''
        ### Цель работы
        **Цель** работы заключается в понимании принципа построения 
        поляризационных или вольт-амперных кривых для солнечных панелей.  
        В ходе выполнения работы Вы также узнаете про ключевые отличия 
        различных типов солнечных панелей.

        *Here add text*  
          
        ---
        '''
    with practice_container:
        '''
        ### Практическая часть
        В первую очередь, выберете интересующую солнечную панель слева.  
        После нажатия на кнопку "Расчет" будут выведены основные параметры 
        выбранной солнечной панели, зависимость напряжения от тока и мощности от тока. 
        '''

        if st.sidebar.button('Расчет'):
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
        
        '**Выбранная панель: **', st.session_state.current_panel['label']
        '**Количество ячеек в солнечной панели: **', st.session_state.current_panel['cell_count']
        '**Площадь одной ячейки: **', st.session_state.current_panel['cell_area']
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
        рабочей мощности выбранной солнечной панели. Данная точка дает максимум рабочего напряжения в Вольтах.
        Чтобы найти максимальный рабочий ток для данной панели, на графике зависимости тока от напряжения 
        необходимо выбрать соответствующую точку.  

        Для рассчета удельного напряжения и плотности тока, необходимо учитывать последовательное соединение
        ячеек в солнечной панели, а также их площадь (приведено над графиками). После расчета данных параметров можно перейти к определнию величин коэффициента заполнения 
        вольт-амперной характеристики и эффективности выбранной солнечной панели.  
        '''
        '''
        Для дополнительной информации обратитесь к разделу **"Введение и элементы теории"**
        '''
        '''
        Проведите предложенное исследование для других типов солнечных панелей и введите полученные результаты
        в таблицу ниже.    
        '''

        with st.expander('Ввести / изменить результаты'):
            '''
            ### Добавить новый результат: 
            '''
            col1, col2, col3 = st.columns(3)
            with col1:
                Isc = st.number_input('Удельная сила тока короткого замыкания (I sc, A/cm2)')
                Inom = st.number_input('Удельный максимальная рабочая сила тока (I nominal, A/cm2)')
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

    introduction_container = st.container()
    work_description_container = st.container()
    practice_container = st.container()
    conclusions_container = st.container()

    with introduction_container:
        '''
        ### Введение и элементы теории   
        Данная работа...
    
        *Here add text*  
        '''
        '''
        ---
        '''
    with work_description_container:
        '''
        ### Цель работы
        **Цель** работы заключается в ...

        *Here add text*  
          
        ---
        '''
    with practice_container:
        '''
        ### Практическая часть
        В первую очередь... 
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
        

        if st.sidebar.button('Расчет'):
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
        p.line(st.session_state.current_panel['IVC']['nom']['U'], st.session_state.current_panel['IVC']['nom']['I'], 
                line_width=2, legend_label='MAX')
        for key, value in st.session_state.current_panel['IVC']['month'].items():
            p.line(value['U'], value['I'], color=next(colors), legend_label=key)
        p.legend.location = "top_left"
        p.legend.click_policy="hide"
        p.add_tools(CrosshairTool())
        st.bokeh_chart(p, use_container_width=True)

        p2 = figure(title = "P-V зависимость", plot_height=400, 
                    x_axis_label='Напряжение (U), V ', y_axis_label='Мощность (P), W')
        p2.line(st.session_state.current_panel['IVC']['nom']['U'], st.session_state.current_panel['IVC']['nom']['P'], 
                line_width=2, legend_label='MAX')
        for key, value in st.session_state.current_panel['IVC']['month'].items():
            p2.line(value['U'], value['P'], color=next(colors), legend_label=key)
        p2.legend.location = "top_left"
        p2.legend.click_policy="hide"
        p2.add_tools(CrosshairTool())
        st.bokeh_chart(p2, use_container_width=True)
        

        E_max = []; E_avg = []; months = {}; x = []; i=1        
        for key, value in st.session_state.current_panel['E_month'].items():
            E_max.append(value['E_max'])
            E_avg.append(value['E'])
            months[i]=key
            x.append(i); i+=1
        source = ColumnDataSource(data=dict(
                                            x=x,
                                            y1=E_max,
                                            y2=E_avg
                                            ))
        p3 = figure(title = "Среднемесячная выработка энергии", plot_height=400, x_axis_label='Месяц', 
                        y_axis_label='Энергия, кВт*ч')
        p3.vbar_stack(['y1', 'y2'], x='x', width= 0.9, color=("grey", "lightgrey"), source=source)
        p3.xaxis.ticker = x
        p3.xaxis.major_label_overrides = months
        p3.add_tools(CrosshairTool())
        st.bokeh_chart(p3, use_container_width=True)

        with st.expander('Задача 1'):
            '''
            **Задача на определение угла**
            '''
            '''
            Предположим, что в Сколково в окрестностях точки с координатами:  
            > *55.69553° с. ш.*  
            > *37.35298° в. д.*  

            планируется построить новое здание, крыша которого будет оборудована монокристаллическими 
            солнечными панелями. Существует четыре проекта здания, которые в том числе отличаются углом 
            наклона кровли, а именно: 16°, 24°, 32° и 43°. Определите, какой из вариантов является наиболее 
            оптимальным с точки зрения эффективности работы солнечных панелей. Считайте, что солнечные 
            панели находятся под таким же углом наклона, что и кровля.  
            '''

            answer_1 = st.number_input('Ответ в виде целого числа:', step=1)
            st.session_state.results['answer_1'] = answer_1
        with st.expander('Задача 2'):
            '''
            **Задача на выбор географической точки**
            '''
            '''
            Гипотетически существующая компания «друзья Солнца» занимается строительством солнечных 
            электростанций. Компания использует аморфные солнечные панели, которые крепятся на стойках, 
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
            **Задача на выбор лучшего типа солнечной панели**
            '''
            '''
            Фонтаны Петергофа известны своей красотой и разнообразием не только у нас в стране, но и далеко за ее пределами. 
            Ежегодно ими любуются миллионы туристов. Однако, для обеспечения работы насосов фонтанов, необходимо регулярно 
            поддерживать электрические сети Петергофа в очень хорошем состоянии, что достаточно сложно сделать в городе, где 
            такая высокая плотность архитектурных памятников и объектов культурного наследия. Предположим, что для повышения 
            энергетической безопасности на некоторых кровлях зданий Петергофа решено установить солнечные панели. Поскольку 
            площадь панелей сильно ограничена, необходимо установить самые эффективные, дающие максимальное количество 
            электроэнергии в период работы фонтанов - с мая по сентябрь. Определите, какого типа солнечные панели стоит 
            использовать в этом проекте.  
            Примерные географические координаты зданий, на которых планируется разместить солнечные панели:
            > *59.879° с. ш.*  
            > *29.898° в. д.*  
            
            Угол наклона крыш, который совпадает с углом наклона солнечных панелей считайте равным 30°.  
            '''
            answer_3 = st.selectbox('Выбранная солнечная панель:', pv_list)
            st.session_state.results['answer_3'] = answer_3
        with st.expander('Задача 4'):
            '''
            **Задача на ВАХ**
            '''
            '''
            Вам необходимо разработать энергосистему, которая состоит из поликристаллических солнечных панелей, 
            может быть установлена в окрестностях города Ростов-на-Дону:  
            > *47.15623° с. ш.*  
            > *39.56059° в. д.*  

            и обеспечивает следующие средние выходные параметры:  
            > Постоянное напряжение - *400 В*  
            > Мощность - *2 кВт*  

            Оцените, какое минимальное количество поликристаллических панелей вам для этого необходимо и
            как необходимо соединить их между собой. 
            '''
            answer_4 = st.number_input('Введите общее количество панелей:', step=1)
            st.session_state.results['answer_4'] = answer_4
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
            if st.session_state.results['answer_1']!=777:
                st.write('> Проверьте ответ к задаче 1!')
            if st.session_state.results['answer_2']!=777:
                st.write('> Проверьте ответ к задаче 2!')
            if st.session_state.results['answer_3']!=777:
                st.write('> Проверьте ответ к задаче 3!')
            if st.session_state.results['answer_4']!=777:
                st.write('> Проверьте ответ к задаче 4!')           
            else:
                '''> #### Автоматические тесты успешно пройдены.  
                '''
                '''
                *Если требуется, можно распечатать отчет при помощи Ctrl+P (Windows) или Cmd+P (MacOS)*
                '''

if tab_selected == works[3]:

    introduction_container = st.container()
    work_description_container = st.container()
    practice_container = st.container()
    conclusions_container = st.container()

    with introduction_container:
        '''
        ### Введение и элементы теории   
        Данная работа...
    
        *Here add text*  
        '''
        '''
        ---
        '''
    with work_description_container:
        '''
        ### Цель работы
        **Цель** работы заключается в ...

        *Here add text*  
          
        ---
        '''
    with practice_container:
        '''
        ### Practice
        First, from the left panel select the type of the solar panel. 
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
        

        if st.sidebar.button('Расчет'):
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

        E_max = []; E_avg = []; months = {}; x = []; i=1        
        for key, value in st.session_state.current_panel['E_month'].items():
            E_max.append(value['E_max'])
            E_avg.append(value['E'])
            months[i]=key
            x.append(i); i+=1
        source = ColumnDataSource(data=dict(
                                                                                x=x,
                                                                                y1=E_max,
                                                                                y2=E_avg
                                                                                ))
        p3 = figure(title = "Среднемесячная выработка энергии", plot_height=400, x_axis_label='Месяц', 
                        y_axis_label='Энергия, кВт*ч')
        p3.vbar_stack(['y1', 'y2'], x='x', width= 0.9, color=("grey", "lightgrey"), source=source)
        p3.xaxis.ticker = x
        p3.xaxis.major_label_overrides = months
        p3.add_tools(CrosshairTool())
        st.bokeh_chart(p3, use_container_width=True)

        with st.expander('Задача 1'):
            '''
            **Задача на определение угла**
            '''
            '''
            Предположим, что в Сколково в окрестностях точки с координатами:  
            > *55.69553° с. ш.*  
            > *37.35298° в. д.*  

            планируется построить новое здание, крыша которого будет оборудована монокристаллическими 
            солнечными панелями. Существует четыре проекта здания, которые в том числе отличаются углом 
            наклона кровли, а именно: 16°, 24°, 32° и 43°. Определите, какой из вариантов является наиболее 
            оптимальным с точки зрения эффективности работы солнечных панелей. Считайте, что солнечные 
            панели находятся под таким же углом наклона, что и кровля.  
            '''

            answer_1 = st.number_input('Ответ в виде целого числа:', step=1)
            st.session_state.results['answer_1'] = answer_1
        with st.expander('Задача 2'):
            '''
            **Задача на выбор географической точки**
            '''
            '''
            Гипотетически существующая компания «друзья Солнца» занимается строительством солнечных 
            электростанций. Компания использует аморфные солнечные панели, которые крепятся на стойках, 
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
            **Задача на выбор лучшего типа солнечной панели**
            '''
            '''
            Фонтаны Петергофа известны своей красотой и разнообразием не только у нас в стране, но и далеко за ее пределами. 
            Ежегодно ими любуются миллионы туристов. Однако, для обеспечения работы насосов фонтанов, необходимо регулярно 
            поддерживать электрические сети Петергофа в очень хорошем состоянии, что достаточно сложно сделать в городе, где 
            такая высокая плотность архитектурных памятников и объектов культурного наследия. Предположим, что для повышения 
            энергетической безопасности на некоторых кровлях зданий Петергофа решено установить солнечные панели. Поскольку 
            площадь панелей сильно ограничена, необходимо установить самые эффективные, дающие максимальное количество 
            электроэнергии в период работы фонтанов - с мая по сентябрь. Определите, какого типа солнечные панели стоит 
            использовать в этом проекте.  
            Примерные географические координаты зданий, на которых планируется разместить солнечные панели:
            > *59.879° с. ш.*  
            > *29.898° в. д.*  
            
            Угол наклона крыш, который совпадает с углом наклона солнечных панелей считайте равным 30°.  
            '''
            answer_3 = st.selectbox('Выбранная солнечная панель:', pv_list)
            st.session_state.results['answer_3'] = answer_3
        with st.expander('Задача 4'):
            '''
            **Задача на ВАХ**
            '''
            '''
            Вам необходимо разработать энергосистему, которая состоит из поликристаллических солнечных панелей, 
            может быть установлена в окрестностях города Ростов-на-Дону:  
            > *47.15623° с. ш.*  
            > *39.56059° в. д.*  

            и обеспечивает следующие средние выходные параметры:  
            > Постоянное напряжение - *400 В*  
            > Мощность - *2 кВт*  

            Оцените, какое минимальное количество поликристаллических панелей вам для этого необходимо и
            как необходимо соединить их между собой. 
            '''
            answer_4 = st.number_input('Введите общее количество панелей:', step=1)
            st.session_state.results['answer_4'] = answer_4
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
            if st.session_state.results['answer_1']!=777:
                st.write('> Проверьте ответ к задаче 1!')
            if st.session_state.results['answer_2']!=777:
                st.write('> Проверьте ответ к задаче 2!')
            if st.session_state.results['answer_3']!=777:
                st.write('> Проверьте ответ к задаче 3!')
            if st.session_state.results['answer_4']!=777:
                st.write('> Проверьте ответ к задаче 4!')           
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
        ### What next?
        '''
        '''
        You can refer to the folowing useful information:  
          
        *Here add links* 
        '''

