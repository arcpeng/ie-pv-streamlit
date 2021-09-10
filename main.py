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

from nasaModel import sendNasaRequest, Tilt_Value, calculateTiltIrr, calculate_month_ivc, calculate_ivc, LatLongToMerc, correct_panel_spec

#st.set_page_config(page_title=None, page_icon=None, layout='wide', initial_sidebar_state='auto')

# ==============================
# Session init
# ==============================
if 'journal' not in st.session_state:
    st.session_state.journal = pd.DataFrame({'':['','','','', '', '']}, columns = [''], 
                                            index=['I sc, A/cm2',
                                                    'U oc, V',
                                                    'I nominal, A/cm2',
                                                    'U nominal, V',
                                                    'Fill factor, %',
                                                    'Efficiency, %'])
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
if 'current_panel' not in st.session_state:
    st.session_state.current_panel = empty_panel
if 'conclusion' not in st.session_state:
    st.session_state.conclusion = ''
if 'coordinates' not in st.session_state:
    st.session_state.coordinates = {'lon':0.00,
                                    'lat':0.00,
                                    'x_Merc':0.00,
                                    'y_Merc':0.00
                                    }
# ==============================

API_URL = 'http://178.154.215.108/solar/panels'

all_panels = requests.get(API_URL).json()

pv_list = []
for panel in all_panels:
    pv_list.append(panel['label'])

def get_ivc(panel_label):
    result = empty_panel
    for panel in all_panels:
        if panel['label']==panel_label:
            req = requests.get(panel['url']).json()
            result.update(req)
            return result

works = ['Introduction', 
        'Work #1: Understanding IVC', 
        'Work #2: Simulating geographics', 
        'Work #3: The third work',
        'Futher investigation']

# ==============================
# Sidebar
# ==============================
st.sidebar.image('./Images/logo.png')
st.sidebar.markdown('***')
st.sidebar.header('PV cloud model')
tab_selected = st.sidebar.selectbox('Select the work:', works)

if tab_selected != works[0]:
    st.sidebar.subheader('Model parameters')
    selected_panel = st.sidebar.selectbox('Select the solar panel:', pv_list)
    
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
        ### Photovoltaics (PV)  
        is the conversion of light into electricity using semiconducting materials 
        that exhibit the photovoltaic effect, a phenomenon studied in physics, 
        photochemistry, and electrochemistry. The photovoltaic effect is 
        commercially utilized for electricity generation and as photosensors. 
        Some hope that photovoltaic technology will produce enough affordable 
        sustainable energy to help mitigate global warming caused by CO$_2$. 
        '''
        with st.expander('PV advantages and perspectives'):
            '''
            Solar PV has specific advantages as an energy source:  
            - once installed, its operation generates no pollution and no greenhouse 
            gas emissions;  
            - it shows simple scalability in respect of power needs and material demands.
              
            Other major constraints 
            identified are competition for land use and lack of labor in making 
            funding applications. The use of PV as a main source requires energy 
            storage systems or global distribution by high-voltage direct current 
            power lines causing additional costs, and also has a number of other 
            specific disadvantages such as unstable power generation and the 
            requirement for power companies to compensate for too much solar 
            power in the supply mix by having more reliable conventional power 
            supplies in order to regulate demand peaks and potential undersupply. 
            Production and installation does cause pollution and greenhouse gas 
            emissions and there are no viable systems for recycling the panels 
            once they are at the end of their lifespan after 10 to 30 years.
            '''
            '''
            Photovoltaic systems have long been used in specialized applications 
            as stand-alone installations and grid-connected PV systems have been 
            in use since the 1990s.[2] Photovoltaic modules were first mass-produced 
            in 2000, when German environmentalists and the Eurosolar organization 
            received government funding for a ten thousand roof program.[3]
            Decreasing costs has allowed PV to grow as an energy source. This has 
            been partially driven by massive Chinese government investment in developing 
            solar production capacity since 2000, and achieving economies of scale. Much 
            of the price of production is from the key component polysilicon, and most of 
            the world supply is produced in China, especially in Xinjiang. Beside the 
            subsidies, the low prices of solar panels in the 2010s has been achieved through 
            the low price of energy from coal and cheap labour costs in Xinjiang,[4] as well 
            as improvements in manufacturing technology and efficiency.[5][6] Advances in 
            technology and increased manufacturing scale have also increased the efficiency 
            of photovoltaic installations.[2][7] Net metering and financial incentives, such 
            as preferential feed-in tariffs for solar-generated electricity, have supported 
            solar PV installations in many countries.[8] Panel prices dropped by a factor of 
            4 between 2004 and 2011. Module prices dropped 90% of over the 2010s, but began 
            increasing sharply in 2021.[4][9]
            In 2019, worldwide installed PV capacity increased to more than 635 gigawatts (GW) 
            covering approximately two percent of global electricity demand.[10] After hydro 
            and wind powers, PV is the third renewable energy source in terms of global 
            capacity. In 2019 the International Energy Agency expected a growth by 700 - 880 
            GW from 2019 to 2024.[11] In some instances, PV has offered the cheapest source 
            of electrical power in regions with a high solar potential, with a bid for pricing 
            as low as 0.01567 US$/kWh in Qatar in 2020.[12]

        '''
        '''
        A photovoltaic system employs solar modules, each comprising a number of 
        solar cells, which generate electrical power. PV installations may be 
        ground-mounted, rooftop-mounted, wall-mounted or floating. The mount may 
        be fixed or use a solar tracker to follow the sun across the sky.
        '''
        
    with scheme_container:
        pass
    with basics_container:
        pass
    with theory_container:
        pass
    with whatnext_container:
        '''
        ### What next?
        '''
        '''
        To proceed, select the next section in the left sidebar. 
        '''

if tab_selected == works[1]:
    
    introduction_container = st.container()
    work_description_container = st.container()
    practice_container = st.container()
    conclusions_container = st.container()

    with introduction_container:
        '''
        ### Introduction & theoretical background  
        A **current–voltage characteristic** or **I–V curve** 
        (current–voltage curve) is a relationship, typically represented 
        as a chart or graph, between the electric current through a circuit, 
        device, or material, and the corresponding voltage, or potential 
        difference across it.  
    
        *Here add text*  
        '''
        with st.expander('Monocrystal solar panel'):
            '''
            *Here add text about different types of solar panels* 
            '''
        with st.expander('Polycrystal solar panel'):
            '''
            *Here add text about different types of solar panels* 
            '''
        with st.expander('Organic solar panel'):
            '''
            *Here add text about different types of solar panels* 
            '''
        '''  
        ---
        '''
    with work_description_container:
        '''
        ### The aim of the work
        **The aim** of this work is to understand the main basics of the 
        solar panels **I–V curve**.  
        You will know the difference between some types of solar 
        panels and calculate their main characteristics

        *Here add text*  
          
        ---
        '''
    with practice_container:
        '''
        ### Practice
        First, from the left panel select the type of the solar panel. 
        After pressing "Calculate" button you will display the key parameters 
        of the selected panel, its I-V and P-V curves. Just try it! 
        '''

        if st.sidebar.button('Calculate'):
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
        
        '**Selected panel: **', st.session_state.current_panel['label']
        '**Number of cells in the solar module: **', st.session_state.current_panel['cell_count']
        '**The area of one cell in the solar module: **', st.session_state.current_panel['cell_area']
        p = figure(title = "I-V curve", plot_height=300, 
                    x_axis_label='Voltage (U), V ', y_axis_label='Current (I), A')
        p.line(st.session_state.current_panel['IVC']['nom']['U'], st.session_state.current_panel['IVC']['nom']['I'], line_width=2)
        p.add_tools(CrosshairTool())
        st.bokeh_chart(p, use_container_width=True)

        p2 = figure(title = "P-V curve", plot_height=300, 
                    x_axis_label='Voltage (U), V ', y_axis_label='Power (P), W')
        p2.line(st.session_state.current_panel['IVC']['nom']['U'], st.session_state.current_panel['IVC']['nom']['P'], line_width=2)
        p2.add_tools(CrosshairTool())
        st.bokeh_chart(p2, use_container_width=True)

        '''
        From the P-V plot select the point, corresponding to the maximum power of panel (in Watts). 
        This point shows the maximum possible operation voltage of the panel in Volts. To find the maximum 
        operation current of the panel, go the the I-V plot and select the point with established 
        maximum operation voltage and find the correxponding electric current value in Amperes.
          
        To calculate the specific Volatge and Current density, you should take into account the 
        serial electric connection of the cells in one solar panel. Use the number of cells and the area of 
        one cell, specified above the plots. After this, calclate the fill factor and the efficiency of the selected panel. 
        For more information check the theory.  
          
        Make the same operations with other types of panels and put the results into the table below. 
        '''

        with st.expander('Modify table results'):
            '''
            ### New result: 
            '''
            col1, col2, col3 = st.columns(3)
            with col1:
                Isc = st.number_input('Specific short current value (I sc, A/cm2)')
                Inom = st.number_input('Specific max operation current (I nominal, A/cm2)')
            with col2:
                Uoc = st.number_input('Open circuit voltage (U oc, V)')
                Unom = st.number_input('Max operation voltage (U nominal, V)')
            with col3:
                FF = st.number_input('Calculated fill factor, %')
                Eff = st.number_input('Calculated efficiency, %')
            if st.button('Add to results'):
                st.session_state.journal[st.session_state.current_panel['label']] = [Isc, Inom, Uoc, Unom, FF, Eff]
            '''
            ---
            '''
            if st.button('Clear all results'):
                st.session_state.journal = pd.DataFrame({'':['','','','', '', '']}, columns = [''], 
                                        index=['I sc, A/cm2',
                                                'U oc, V',
                                                'I nominal, A/cm2',
                                                'U nominal, V',
                                                'Fill factor, %',
                                                'Efficiency, %'])
            if st.button('Clear last result'):
                if st.session_state.current_panel['label'] in st.session_state.journal.keys():
                    del st.session_state.journal[st.session_state.current_panel['label']]

        st.write(st.session_state.journal)
        '''
        ---
        '''
    with conclusions_container:
        with st.expander('Modify conclusion'):
            entered_conclusion = st.text_input('')
            if st.button('Save'):
                st.session_state.conclusion = entered_conclusion
        '''
        ### Conclusions  
        '''
        st.write(st.session_state.conclusion)
        '''
        ---
        '''
        '''
        *Here you can make auto-check of your results.*
        '''
        if st.button('Check results'):
            if len(st.session_state.conclusion) < 300:
                st.write('> Not very informative conclusion!')
            if (len(st.session_state.journal.columns)-1) < 3:
                st.write('> To few solar panels examined. Not enough data.')
            else:
                '''> #### Auto tests completed! Seems everything is fine.  
                '''
                '''
                *If you want, you can hide all the expanders above and print the report 
                with Ctrl+P on Windows or Cmd+P on MacOs*
                '''

if tab_selected == works[2]:
    st.session_state.current_panel = empty_panel
    introduction_container = st.container()
    work_description_container = st.container()
    practice_container = st.container()
    conclusions_container = st.container()

    with introduction_container:
        '''
        ### Introduction & theoretical background  
        The work of solar panels depends not only on its type, but also on the surrounding
        environment....
    
        *Here add text*  
        '''
        '''
        ---
        '''
    with work_description_container:
        '''
        ### The aim of the work
        **The aim** of this work is to understand the main basics of the 
        solar panels in terms of working in different conditions/geographics.  
        You will know ....

        *Here add text*  
        '''
        '''
        ---
        '''

    with practice_container:
        '''
        ### Practice
        First, choose coordinates on map and enter them in the fields above the map.  
        Push the button to set up the chosen position.
        '''

        col1, col2 = st.columns(2)
        with col1:
            lon_inp = st.number_input('Longitude', min_value=0.00, max_value=180.00, value=0.00, step=1.0)
        with col2:
            lat_inp = st.number_input('Latitude', min_value=-85.00, max_value=85.00, value=0.00, step=1.0)


        if st.button('Set position'):
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

        input_ang = st.sidebar.number_input('Tilt angle', min_value=0.0, max_value=90.0, value=0.0, step = 1.0)
        
        if st.sidebar.button('Calculate'):
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
                                        Unom=st.session_state.current_panel['IVC']['nom']['U']
                                        )
            st.session_state.current_panel.update(new_panel)
    
        '**Selected panel: **', st.session_state.current_panel['label']
        p = figure(title = "I-V curve", plot_height=400, 
                    x_axis_label='Voltage (U), V ', y_axis_label='Current (I), A')
        p.line(st.session_state.current_panel['IVC']['nom']['U'], st.session_state.current_panel['IVC']['nom']['I'], line_width=2)
        for key, value in st.session_state.current_panel['IVC']['month'].items():
            p.line(value['U'], value['I'])
        p.add_tools(CrosshairTool())
        st.bokeh_chart(p, use_container_width=True)

        p2 = figure(title = "P-V curve", plot_height=400, 
                    x_axis_label='Voltage (U), V ', y_axis_label='Power (P), W')
        p2.line(st.session_state.current_panel['IVC']['nom']['U'], st.session_state.current_panel['IVC']['nom']['P'], line_width=2)
        for key, value in st.session_state.current_panel['IVC']['month'].items():
            p2.line(value['U'], value['P'])
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
        p3 = figure(title = "Month energy", plot_height=400, x_axis_label='month ', 
                        y_axis_label='Avg energy')

        p3.vbar_stack(['y1', 'y2'], x='x', width= 0.9, color=("grey", "lightgrey"), source=source)
        p3.xaxis.ticker = x
        p3.xaxis.major_label_overrides = months
        p3.add_tools(CrosshairTool())
        st.bokeh_chart(p3, use_container_width=True)

        '''
        ---
        '''
    with conclusions_container:
        with st.expander('Modify conclusion'):
            entered_conclusion = st.text_input('')
            if st.button('Save'):
                st.session_state.conclusion = entered_conclusion
        '''
        ### Conclusions  
        '''
        st.write(st.session_state.conclusion)
        '''
        ---
        '''
        '''
        *Here you can make auto-check of your results.*
        '''
        if st.button('Check results'):
            if len(st.session_state.conclusion) < 300:
                st.write('> Not very informative conclusion!')
            else:
                '''> #### Auto tests completed! Seems everything is fine.  
                '''
                '''
                *If you want, you can hide all the expanders above and print the report 
                with Ctrl+P on Windows or Cmd+P on MacOs*
                '''


if tab_selected == works[3]:
    introduction_container = st.container()
    work_description_container = st.container()
    practice_container = st.container()
    conclusions_container = st.container()

    with introduction_container:
        '''
        ### Introduction & theoretical background  
        The work of solar panels depends not only on its type, but also on the surrounding
        environment....
    
        *Here add text*  
        '''
        '''
        ---
        '''
        
    with work_description_container:
        '''
        ### The aim of the work
        **The aim** of this work is to understand the main basics of the 
        solar panels in terms of working in different conditions/geographics.  
        You will know ....

        *Here add text*  
        '''
        '''
        ---
        '''
    with practice_container:
        '''
        ### Practice
        First, from the left panel select the type of the solar panel. 
        '''
        '''
        ---
        '''
    with conclusions_container:
        with st.expander('Modify conclusion'):
            entered_conclusion = st.text_input('')
            if st.button('Save'):
                st.session_state.conclusion = entered_conclusion
        '''
        ### Conclusions  
        '''
        st.write(st.session_state.conclusion)
        '''
        ---
        '''
        '''
        *Here you can make auto-check of your results.*
        '''
        if st.button('Check results'):
            if len(st.session_state.conclusion) < 300:
                st.write('> Not very informative conclusion!')
            else:
                '''> #### Auto tests completed! Seems everything is fine.  
                '''
                '''
                *If you want, you can hide all the expanders above and print the report 
                with Ctrl+P on Windows or Cmd+P on MacOs*
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

