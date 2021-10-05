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

works = ['Введение', 
        'Работа №1: Характеристические кривые солнечных панелей', 
        'Работа №2: Влияние координат', 
        'Работа №3: Изучение эффекта температуры',
        'Полезная литература']

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
    st.sidebar.subheader('Параметры модели')
    selected_panel = st.sidebar.selectbox('Выберете солнечную панель:', pv_list)

    introduction_container = st.container()
    work_description_container = st.container()
    practice_container = st.container()
    conclusions_container = st.container()

    with introduction_container:
        '''
        ### Введение и элементы теории  
        '''
        '''
        Основной характеристикой солнечных панелей является их вольт-амперная характеристика (ВАХ).
        '''
        '''
        **Вольт-амперной характеристикой (ВАХ)** называют функцию (а также её график), 
        задающую зависимость тока, протекающего через двухполюсник, от напряжения на нём. 
        Двухполюсником называют любой элемент электрической цепи, содержащий два контакта 
        для соединения с другими электрическими цепями.  
        '''
        '''
        Основной рабочей характеристикой солнечной батареи является максимальная мощность, 
        которую выражают в Ваттах (Вт). Эта характеристика показывает выходную мощность 
        батареи в оптимальных условиях: солнечном излучении *1 кВт/м²*, температуре окружающей 
        среды 25 °C, стандартизованном солнечном спектре АМ1,5 (солнечный спектр на широте 45°). 
        В обычных условиях достичь таких показателей удается крайне редко, т.к. освещенность ниже, 
        а модуль нагревается выше (до 60–70 °C).
        '''
        '''
        К характеристикам солнечных панелей также относятся следующие:  
        - **Напряжение открытой цепи** − это максимальное напряжение, создаваемое солнечным элементом, 
        возникающее при нулевом токе. Оно равно прямому смещению, соответствующему изменению напряжения 
        p–n-перехода при появлении светового тока. Напряжение холостого хода солнечного элемента мало 
        меняется при изменении освещенности. 
        - **Ток короткого замыкания** − это ток, протекающий через солнечный элемент, когда напряжение 
        равно нулю (то есть когда солнечный элемент замкнут накоротко). Ток короткого замыкания можно 
        считать максимальным током, который способен создать солнечный элемент. Кроме того, он прямо 
        пропорционально зависит от интенсивности света.
        - **Фактор заполнения** - параметр, который в сочетании с напряжением холостого хода и током 
        короткого замыкания определяет максимальную мощность солнечного элемента. Он вычисляется, 
        как отношение максимальной мощности солнечного элемента к произведению напряжения холостого 
        хода и тока короткого замыкания. Фактор заполнения ВАХ является одним из основных параметров, 
        по которому можно судить о качестве фотоэлектрического преобразователя. Чем больше коэффициент 
        заполнения ВАХ, тем меньше потери в элементе из-за внутреннего сопротивления.
        - **Коэффициент полезного действия (КПД)** является самым распространенным параметром, по которому 
        можно сравнить производительность двух солнечных элементов. Он определяется как отношение мощности, 
        вырабатываемой солнечным элементом, к мощности падающего солнечного излучения. Кроме собственно 
        производительности солнечного элемента, **КПД** также зависит от спектра и интенсивности падающего 
        солнечного излучения и температуры солнечного элемента. Поэтому для сравнения двух солнечных 
        элементов нужно тщательно выполнять принятые стандартные условия. КПД солнечного элемента 
        определяется как часть падающей энергии, преобразованной в электричество.
        '''

        with st.expander('Монокристаллическая солнечная панель'):
            '''
            Несомненные плюсы – компактность и эффективность. Монокристаллические модули и по сей день 
            являются уверенными лидерами по показателям мощности, КПД и долговечности. Это отражается 
            и на стоимости: цена их высока. Искусственно выращенные кремниевые кристаллы нарезаются 
            на тонкие пластины. В основу модуля входит очищенный чистый кремний. Поверхность больше 
            похожа на пчелиные соты или небольшие ячейки, которые соединяются между собой в единую структуру. 
            Готовые маленькие пластинки соединяются между собой сеткой из электроводов. В данном случае 
            процесс производства наиболее трудоёмкий и энергозатратный, что отражается на конечной стоимости 
            солнечной батареи. Но монокристаллические элементы обладают лучшей производительностью, 
            их средний КПД составляет около 22–25%.
            '''
        with st.expander('Поликристаллическая солнечная панель'):
            '''
            Производятся из кремния, имеющего поликристаллическую структуру. Поликристаллы получаются 
            в результате постепенного охлаждения расплавленного кремния. Метод этот прост, поэтому такие 
            фотоэлементы и стоят недорого. Хотя их технические характеристики, в том числе и производительность, 
            уже ниже (связано это с «нечистотой» получаемых кремниевых пластин и внутренней их структурой) – 
            примерно на уровне 20%, но стоят они намного дешевле монокристаллических. Благодаря этому солнечные 
            панели перестали быть чем-то недоступным для обычных людей. Человек со средним уровнем достатка вполне 
            может воспользоваться именно этим предложением. Поликристаллическая солнечная батарея имеет 
            неоднородную поверхность, из-за чего хуже поглощает свет, и её КПД, соответственно, ниже. 
            Такие солнечные панели имеют характерное отличие – тёмно-синий цвет покрытия.  
            '''
        with st.expander('Органическая солнечная панельl'):
            '''
            Помимо технологий основанных на использовании кремния развиваются и другие направления, 
            в том числе, когда фотоактивный слой состоит из органических веществ. Панели изготовленные 
            по такой технологии легче кремниевых, что является большим преимуществом для многих прикладных 
            задач. Еще одним плюсом является то, что органические солнечные панели оказывают меньшее 
            воздействие на окружающую среду. Однако это обстоятельство сопряжено и с недостатком органических 
            панелей - их эффективность относительно быстро падает из-за воздействия окружающей среды. Еще одним 
            недостатком является относительно невысокий КПД. 
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
        '''
        '''  
        ---
        '''
    with practice_container:
        '''
        ### Практическая часть
        В первую очередь выберите интересующую вас солнечную панель слева. 
        После нажатия на кнопку Расчет будут выведены основные параметры 
        выбранной солнечной панели, зависимости силы тока от напряжения 
        и мощности от напряжения.
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
        По графику зависимости мощности от напряжения определите точку, 
        соответствующую максимуму рабочей мощности выбранной солнечной 
        панели. Данная точка дает максимум рабочего напряжения в вольтах (В). 
        Чтобы найти максимальный рабочий ток для данной панели, на графике 
        зависимости тока от напряжения необходимо выбрать соответствующую точку.
        '''
        '''
        Для рассчета удельного напряжения и плотности тока, необходимо учитывать 
        последовательное соединение ячеек в солнечной панели, а также их площадь 
        (приведено над графиками). После расчета данных параметров можно перейти 
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
                    color="#718dbf", legend_label="Расчет")
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
            elif st.session_state.results['answer_1']!=777:
                st.write('> Проверьте ответ к задаче 1!')
            elif st.session_state.results['answer_2']!=777:
                st.write('> Проверьте ответ к задаче 2!')
            elif st.session_state.results['answer_3']!=777:
                st.write('> Проверьте ответ к задаче 3!')
            elif st.session_state.results['answer_4_1']!=777 and \
            st.session_state.results['answer_4_2']!=777 and \
            st.session_state.results['answer_4_3']!=777:
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
                    color="#718dbf", legend_label="Расчет")
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
            elif st.session_state.results['answer_1']!=777:
                st.write('> Проверьте ответ к задаче 1!')
            elif st.session_state.results['answer_2']!=777:
                st.write('> Проверьте ответ к задаче 2!')
            elif st.session_state.results['answer_3']!=777:
                st.write('> Проверьте ответ к задаче 3!')
            elif st.session_state.results['answer_4_1']!=777 and \
            st.session_state.results['answer_4_2']!=777 and \
            st.session_state.results['answer_4_3']!=777:
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

