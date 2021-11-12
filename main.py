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
                'label':0,
                'I_max':0, 'U_max':0, 'Isc':0, 'Uoc':0,
                'cell_area':0, 'cell_count':0,
                'tC':0,
                # calculated parameters
                'IVC':{
                    'nom':{'I':0, 'U':0, 'P':0},
                    'month':{}                                        
                    },
                'Efficiency': 0,
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
        p = figure(title = text['work1']['practice'][lang][4], plot_height=300, 
                    x_axis_label=text['work1']['practice'][lang][5], 
                    y_axis_label=text['work1']['practice'][lang][6])
        p.line(st.session_state.current_panel['IVC']['nom']['U'], st.session_state.current_panel['IVC']['nom']['I'], line_width=2)
        p.add_tools(CrosshairTool())
        st.bokeh_chart(p, use_container_width=True)

        p2 = figure(title = text['work1']['practice'][lang][7], plot_height=300, 
                    x_axis_label=text['work1']['practice'][lang][5], 
                    y_axis_label=text['work1']['practice'][lang][8])
        p2.line(st.session_state.current_panel['IVC']['nom']['U'], st.session_state.current_panel['IVC']['nom']['P'], line_width=2)
        p2.add_tools(CrosshairTool())
        st.bokeh_chart(p2, use_container_width=True)

        st.markdown(text['work1']['practice'][lang][9])
        st.markdown(text['work1']['practice'][lang][10])
        st.markdown(text['work1']['practice'][lang][11])
        st.markdown(text['work1']['practice'][lang][12])
        st.markdown(text['work1']['practice'][lang][13])
        
        with st.expander(text['work1']['practice'][lang][14]):
            st.markdown(text['work1']['practice'][lang][15])
            col1, col2, col3 = st.columns(3)
            with col1:
                Isc = st.number_input(text['work1']['practice'][lang][16])
                Inom = st.number_input(text['work1']['practice'][lang][17])
            with col2:
                Uoc = st.number_input(text['work1']['practice'][lang][18])
                Unom = st.number_input(text['work1']['practice'][lang][19])
            with col3:
                FF = st.number_input(text['work1']['practice'][lang][20])
                Eff = st.number_input(text['work1']['practice'][lang][21])
            if st.button(text['work1']['practice'][lang][22]):
                st.session_state.journal[st.session_state.current_panel['label']] = [Isc, Inom, Uoc, Unom, FF, Eff]
            
            st.markdown(text['work1']['practice'][lang][25])
            
            if st.button(text['work1']['practice'][lang][23]):
                st.session_state.journal = pd.DataFrame({'':['','','','', '', '']}, columns = [''], 
                                        index=['I sc, A/cm2',
                                                'U oc, V',
                                                'I nominal, A/cm2',
                                                'U nominal, V',
                                                'Fill factor, %',
                                                'Efficiency, %'])
            if st.button(text['work1']['practice'][lang][24]):
                if st.session_state.current_panel['label'] in st.session_state.journal.keys():
                    del st.session_state.journal[st.session_state.current_panel['label']]

        st.write(st.session_state.journal)
        st.markdown(text['work1']['practice'][lang][25])

    with conclusions_container:
        with st.expander(text['work1']['conclusions'][lang][0]):
            entered_conclusion = st.text_input('')
            if st.button(text['work1']['conclusions'][lang][1]):
                st.session_state.results['conclusion'] = entered_conclusion
        st.markdown(text['work1']['conclusions'][lang][2])
        if 'conclusion' in st.session_state.results:
            st.write(st.session_state.results['conclusion'])
        st.markdown(text['work1']['conclusions'][lang][3])
        st.markdown(text['work1']['conclusions'][lang][4])
        if st.button(text['work1']['conclusions'][lang][5]):
            st.session_state.results['conclusion'] = entered_conclusion
            if len(st.session_state.results['conclusion']) < 300:
                st.write(text['work1']['conclusions'][lang][6])
            if (len(st.session_state.journal.columns)-1) < 3:
                st.write(text['work1']['conclusions'][lang][7])
            else:
                st.write(text['work1']['conclusions'][lang][8])
                st.write(text['work1']['conclusions'][lang][9])

if tab_selected == works[2]:
    st.sidebar.subheader(text['work2']['sidebar_subheader'][lang])
    selected_panel = st.sidebar.selectbox(text['work2']['sidebar_selectbox'][lang], pv_list)
 
    introduction_container = st.container()
    work_description_container = st.container()
    practice_container = st.container()
    conclusions_container = st.container()

    with introduction_container:
        st.markdown(text['work2']['introduction'][lang][0])
        st.markdown(text['work2']['introduction'][lang][1])

        with st.expander(text['work2']['introduction'][lang][2]):
            st.markdown('<p style="text-align: center; padding-right:20%; padding-left:20%"><img src="https://raw.githubusercontent.com/MelnikovAP/pv-streamlit/stage_ru/Images/2_Picture_1.png", width=100%/></p>', 
                unsafe_allow_html=True)
        st.markdown(text['work2']['introduction'][lang][3])
        st.markdown(text['work2']['introduction'][lang][4])
        st.markdown(text['work2']['introduction'][lang][5])
        st.markdown(text['work2']['introduction'][lang][6])
        st.markdown(text['work2']['introduction'][lang][7])
        st.markdown(text['work2']['introduction'][lang][8])

    with work_description_container:
        st.markdown(text['work2']['work_description'][lang][0])
        st.markdown(text['work2']['work_description'][lang][1])
    with practice_container:
        st.markdown(text['work2']['practice'][lang][0])
        st.markdown(text['work2']['practice'][lang][1])
        st.markdown(text['work2']['practice'][lang][2])

        col1, col2 = st.columns(2)
        with col1:
            lon_inp = st.number_input(text['work2']['practice'][lang][3], min_value=0.00, max_value=180.00, value=0.00, step=1.0)
        with col2:
            lat_inp = st.number_input(text['work2']['practice'][lang][4], min_value=-85.00, max_value=85.00, value=0.00, step=1.0)


        if st.button(text['work2']['practice'][lang][5]):
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

        input_ang = st.sidebar.number_input(text['work2']['practice'][lang][6], min_value=0.0, max_value=90.0, value=0.0, step = 1.0)
        

        if st.sidebar.button(text['work2']['sidebar_button'][lang]):
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


        text['work2']['practice'][lang][7], st.session_state.current_panel['label']
        p = figure(title = text['work2']['practice'][lang][8], plot_height=400, 
                    x_axis_label=text['work2']['practice'][lang][9], 
                    y_axis_label=text['work2']['practice'][lang][10])
        p2 = figure(title = text['work2']['practice'][lang][11], plot_height=400, 
                    x_axis_label=text['work2']['practice'][lang][9], 
                    y_axis_label=text['work2']['practice'][lang][12])
        
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
        
        p3 = figure(x_range=months, plot_height=400, title=text['work2']['practice'][lang][13],
                    x_axis_label='Месяц', y_axis_label=text['work2']['practice'][lang][14])
        p3.vbar(x=dodge('months', -0.2, range=p3.x_range), top='E_max', width=0.4, source=source,
                    color="#c9d9d3", legend_label=text['work2']['practice'][lang][15])
        p3.vbar(x=dodge('months', 0.2, range=p3.x_range), top='E_avg', width=0.4, source=source,
                    color="#718dbf", legend_label=text['work2']['practice'][lang][16])
        p3.x_range.range_padding = 0.1
        p3.y_range.start = 1
        if len(E_max)>0: p3.y_range.end = max(E_max)*1.2 
        p3.legend.click_policy="hide"
        p3.legend.orientation = "horizontal"
        p3.add_tools(CrosshairTool())
        st.bokeh_chart(p3, use_container_width=True)

        with st.expander(text['work2']['practice'][lang][17]):
            st.markdown(text['work2']['practice'][lang][18])
            answer_1 = st.number_input(text['work2']['practice'][lang][19], step=1)
            st.session_state.results['answer_1'] = answer_1
        with st.expander(text['work2']['practice'][lang][20]):
            st.markdown(text['work2']['practice'][lang][21])
            st.markdown(text['work2']['practice'][lang][22])
            st.markdown(text['work2']['practice'][lang][23])
            answer_2 = st.selectbox(text['work2']['practice'][lang][24], [1,2,3])
            st.session_state.results['answer_2'] = answer_2
        with st.expander(text['work2']['practice'][lang][25]):
            st.markdown(text['work2']['practice'][lang][26])
            answer_3 = st.selectbox(text['work2']['practice'][lang][27], pv_list)
            st.session_state.results['answer_3'] = answer_3
        with st.expander(text['work2']['practice'][lang][28]):
            st.markdown(text['work2']['practice'][lang][29])
            answer_4_1 = st.number_input(text['work2']['practice'][lang][30], step=1)
            st.session_state.results['answer_4_1'] = answer_4_1
            answer_4_2 = st.number_input(text['work2']['practice'][lang][31], step=1)
            st.session_state.results['answer_4_2'] = answer_4_2
            answer_4_3 = st.number_input(text['work2']['practice'][lang][32], step=1)
            st.session_state.results['answer_4_3'] = answer_4_3
            st.markdown(text['work2']['practice'][lang][33])
        st.markdown(text['work2']['practice'][lang][34])

    with conclusions_container:
        with st.expander(text['work2']['conclusions'][lang][0]):
            entered_conclusion = st.text_input('')
            if st.button(text['work2']['conclusions'][lang][1]):
                st.session_state.results['conclusion'] = entered_conclusion
        st.markdown(text['work2']['conclusions'][lang][2])
        if 'conclusion' in st.session_state.results:
            st.write(st.session_state.results['conclusion'])
        text['work2']['conclusions'][lang][3]
        st.markdown(text['work2']['conclusions'][lang][4])
        if st.button(text['work2']['conclusions'][lang][5]):
            st.session_state.results['conclusion'] = entered_conclusion
            if len(st.session_state.results['conclusion']) < 300:
                st.write(text['work2']['conclusions'][lang][6])
            elif st.session_state.results['answer_1']!=1:
                st.write(text['work2']['conclusions'][lang][7])
            elif st.session_state.results['answer_2']!=1:
                st.write(text['work2']['conclusions'][lang][8])
            elif st.session_state.results['answer_3']!='Монокристаллическая':
                st.write(text['work2']['conclusions'][lang][9])
            elif st.session_state.results['answer_4_1']!=1 and \
            st.session_state.results['answer_4_2']!=1 and \
            st.session_state.results['answer_4_3']!=1:
                st.write(text['work2']['conclusions'][lang][10])           
            else:
                st.markdown(text['work2']['conclusions'][lang][11])
                st.markdown(text['work2']['conclusions'][lang][12])

if tab_selected == works[3]:
    st.sidebar.subheader(text['work3']['sidebar_subheader'][lang])
    selected_panel = st.sidebar.selectbox(text['work3']['sidebar_selectbox'][lang], pv_list)
    
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

