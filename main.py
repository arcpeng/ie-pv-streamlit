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
                'label':{'ENG':0,'RU':0},
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

API_URL = 'http://178.154.215.108/solar/panels'
all_panels = requests.get(API_URL).json()

pv_list = []
for panel in all_panels:
    pv_list.append(panel['label'][lang])

def get_spec(panel_label):
    result = empty_panel
    for panel in all_panels:
        if panel['label']==panel_label:
            panel_URL = API_URL+'/'+str(panel['id'])
            req = requests.get(panel_URL).json()
            result.update(req)
            result['id'] = panel['id']
            return result

def calculate_ivc(panel, flag, params = {'tiltAngle':['0'],
                                        'latitude':['0'],
                                        'longitude':['0'],
                                        'area':['1']
                                        }
                ):
    panel_URL = API_URL+'/'+str(panel['id'])+'/calculate'
    if flag=='nom':               # returning only nominal values
        req = requests.post(panel_URL, params).json()
        panel.update(req)
        Unom = panel['IVC']['nom']['I']
        Inom = panel['IVC']['nom']['U']
        Pnom = panel['IVC']['nom']['P']
        return [Unom, Inom, Pnom]
    elif flag=='all':
        req = requests.post(panel_URL, params).json()
        panel.update(req)
        Unom = panel['IVC']['nom']['I']
        Inom = panel['IVC']['nom']['U']
        Pnom = panel['IVC']['nom']['P']
        return [Unom, Inom, Pnom]

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
        st.markdown('<p style="text-align: center; padding-right:0%; padding-left:0%"><img src="https://raw.githubusercontent.com/MelnikovAP/pv-streamlit/stage/Images/0_Picture_0.png", width=100%/></p>', 
            unsafe_allow_html=True)
        st.markdown(text['work0']['introduction'][lang][2])

    with basics_container:
        st.markdown(text['work0']['basics'][lang][0])
        st.markdown(text['work0']['basics'][lang][1])
        with st.expander(text['work0']['basics'][lang][2]):
            if lang=='ENG':
                st.markdown('<p style="text-align: center; padding-right:10%; padding-left:10%"><img src="https://raw.githubusercontent.com/MelnikovAP/pv-streamlit/stage/Images/0_Picture_1_ENG.png", width=90%/></p>', 
                        unsafe_allow_html=True)
            if lang=='RU':
                st.markdown('<p style="text-align: center; padding-right:10%; padding-left:10%"><img src="https://raw.githubusercontent.com/MelnikovAP/pv-streamlit/stage/Images/0_Picture_1_RU.png", width=90%/></p>', 
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
        '''
        ### Practice
        First, from the left panel select the type of the solar panel. 
        After pressing "Calculate" button you will display the key parameters 
        of the selected panel, its I-V and P-V curves. Just try it! 
        '''

        if st.sidebar.button('Calculate'):
            st.session_state.current_panel = get_spec(selected_panel)
            calculate_ivc(panel=st.session_state.current_panel, flag='nom')
            for key in st.session_state.current_panel['IVC']['nom'].keys():
                st.session_state.current_panel['IVC']['nom'][key] = np.array(st.session_state.current_panel['IVC']['nom'][key])

            st.session_state.current_panel['IVC']['nom']['I'] *= st.session_state.current_panel['cell_area']
            st.session_state.current_panel['IVC']['nom']['U'] *= st.session_state.current_panel['cell_count']
            st.session_state.current_panel['IVC']['nom']['P'] = st.session_state.current_panel['IVC']['nom']['I']*st.session_state.current_panel['IVC']['nom']['U']
        
        '**Selected panel: **', st.session_state.current_panel['label']
        '**Number of cells in the solar module: **', str(st.session_state.current_panel['cell_count'])
        '**The area of one cell in the solar module: **', str(st.session_state.current_panel['cell_area'])
        p = figure(title = "I-V curve", plot_height=300, 
                    x_axis_label='Voltage (U), V ', y_axis_label='Current (I), A')
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
                st.session_state.journal[st.session_state.current_panel['label'][lang]] = [Isc, Inom, Uoc, Unom, FF, Eff]
            
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
                if st.session_state.current_panel['label'][lang] in st.session_state.journal.keys():
                    del st.session_state.journal[st.session_state.current_panel['label'][lang]]

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
            if lang=='ENG':
                st.markdown('<p style="text-align: center; padding-right:20%; padding-left:20%"><img src="https://raw.githubusercontent.com/MelnikovAP/pv-streamlit/stage/Images/2_Picture_1_ENG.png", width=100%/></p>', 
                        unsafe_allow_html=True)
            if lang=='RU':
                st.markdown('<p style="text-align: center; padding-right:20%; padding-left:20%"><img src="https://raw.githubusercontent.com/MelnikovAP/pv-streamlit/stage/Images/2_Picture_1_RU.png", width=100%/></p>', 
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
        
        if st.sidebar.button('Calculate'):
            st.session_state.current_panel = get_spec(selected_panel)
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


        text['work2']['practice'][lang][7], st.session_state.current_panel['label'][lang]
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
        st.markdown(text['work3']['introduction'][lang][0])
        st.markdown(text['work3']['introduction'][lang][1])
        st.markdown(text['work3']['introduction'][lang][2])
        st.markdown(text['work3']['introduction'][lang][3])
        st.markdown(text['work3']['introduction'][lang][4])
    with work_description_container:
        st.markdown(text['work3']['work_description'][lang][0])
        st.markdown(text['work3']['work_description'][lang][1])
    with practice_container:
        st.markdown(text['work3']['practice'][lang][0])
        st.markdown(text['work3']['practice'][lang][1])

        col1, col2 = st.columns(2)
        with col1:
            lon_inp = st.number_input(text['work3']['practice'][lang][2], min_value=0.00, max_value=180.00, value=0.00, step=1.0)
        with col2:
            lat_inp = st.number_input(text['work3']['practice'][lang][3], min_value=-85.00, max_value=85.00, value=0.00, step=1.0)


        if st.button(text['work3']['practice'][lang][4]):
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

        input_ang = st.sidebar.number_input(text['work3']['practice'][lang][5], min_value=0.0, max_value=90.0, value=0.0, step = 1.0)
        
        if st.sidebar.button('Calculate'):
            st.session_state.current_panel = get_spec(selected_panel)
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

        text['work3']['practice'][lang][6], st.session_state.current_panel['label'][lang]
        p = figure(title = text['work3']['practice'][lang][7], plot_height=400, 
                    x_axis_label=text['work3']['practice'][lang][8], y_axis_label=text['work3']['practice'][lang][9])
        p2 = figure(title = text['work3']['practice'][lang][10], plot_height=400, 
                    x_axis_label=text['work3']['practice'][lang][8], y_axis_label=text['work3']['practice'][lang][11])
        
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

        p3 = figure(x_range=months, plot_height=400, title=text['work3']['practice'][lang][12],
                    x_axis_label='Месяц', y_axis_label=text['work3']['practice'][lang][13])
        p3.vbar(x=dodge('months', -0.2, range=p3.x_range), top='E_max', width=0.2, source=source,
                    color="#c9d9d3", legend_label=text['work3']['practice'][lang][14])
        p3.vbar(x=dodge('months', 0, range=p3.x_range), top='E_avg', width=0.2, source=source,
                    color="#718dbf", legend_label=text['work3']['practice'][lang][15])
        p3.vbar(x=dodge('months', 0.2, range=p3.x_range), top='E_cor', width=0.2, source=source,
                    color="#e84d60", legend_label=text['work3']['practice'][lang][16])

        p3.x_range.range_padding = 0.1
        p3.y_range.start = 1
        if len(E_max)>0: p3.y_range.end = max(E_max)*1.2 
        p3.legend.click_policy="hide"
        p3.legend.orientation = "horizontal"
        p3.add_tools(CrosshairTool())
        st.bokeh_chart(p3, use_container_width=True)

        with st.expander(text['work3']['practice'][lang][17]):
            st.markdown(text['work3']['practice'][lang][18])
            answer_1 = st.number_input(text['work3']['practice'][lang][19], step=1)
            st.session_state.results['answer_1'] = answer_1
        with st.expander(text['work3']['practice'][lang][20]):
            st.markdown(text['work3']['practice'][lang][21])
            st.markdown(text['work3']['practice'][lang][22])
            answer_2 = st.selectbox(text['work3']['practice'][lang][23], [1,2,3])
            st.session_state.results['answer_2'] = answer_2
        with st.expander(text['work3']['practice'][lang][24]):
            st.markdown(text['work3']['practice'][lang][25])
            st.markdown(text['work3']['practice'][lang][26])
            answer_3 = st.selectbox(text['work3']['practice'][lang][27], pv_list)
            st.session_state.results['answer_3'] = answer_3
        st.markdown(text['work3']['practice'][lang][28])
    with conclusions_container:
        with st.expander(text['work3']['conclusions'][lang][0]):
            entered_conclusion = st.text_input('')
            if st.button(text['work3']['conclusions'][lang][1]):
                st.session_state.results['conclusion'] = entered_conclusion
        text['work3']['conclusions'][lang][2]
        if 'conclusion' in st.session_state.results:
            st.write(st.session_state.results['conclusion'])
        st.markdown(text['work3']['conclusions'][lang][3])
        st.markdown(text['work3']['conclusions'][lang][4])
        if st.button(text['work3']['conclusions'][lang][5]):
            st.session_state.results['conclusion'] = entered_conclusion
            if len(st.session_state.results['conclusion']) < 300:
                st.write(text['work3']['conclusions'][lang][6])
            elif st.session_state.results['answer_1']!=1:
                st.write(text['work3']['conclusions'][lang][7])
            elif st.session_state.results['answer_2']!=1:
                st.write(text['work3']['conclusions'][lang][8])
            elif st.session_state.results['answer_3']!=text['work3']['conclusions'][lang][9]:
                st.write(text['work3']['conclusions'][lang][10])        
            else:
                st.markdown(text['work3']['conclusions'][lang][11])
                st.markdown(text['work3']['conclusions'][lang][12])

if tab_selected == works[4]:
    whatnext_container = st.container()

    with whatnext_container:
        st.markdown(text['work4'][lang][0])
        st.markdown(text['work4'][lang][1])
        st.markdown(text['work4'][lang][2])
        st.markdown(text['work4'][lang][3])

