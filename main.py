from pathlib import WindowsPath
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from requests.api import head
import streamlit as st
import requests
from bokeh.plotting import figure
from bokeh.models import CrosshairTool

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

# ==============================
API_URL = 'http://178.154.215.108/solar/panels'

all_panels = requests.get(API_URL).json()

pv_list = []
for panel in all_panels:
    pv_list.append(panel['label'])

def get_ivc(panel_label):
    for panel in all_panels:
        if panel['label']==panel_label:
            result = requests.get(panel['url'])
            return result.json()

works = ['Introduction', 
        'Work #1: The first work', 
        'Work #2: The second work', 
        'Work #3: The third work',
        'Futher investigation']

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
        pass
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
        [Unom, Inom, Pnom] = [None, None, None]
        result = {'label':'', 
                'cell_area':'',
                'cell_count':''}

        if st.sidebar.button('Calculate'):
            result = get_ivc(selected_panel)
            [Unom, Inom, Pnom] = calculate_ivc(I_max=result['I_max'], 
                                            U_max=result['U_max'], 
                                            Isc=result['Isc'],
                                            Uoc=result['Uoc'], 
                                            cell_area=result['cell_area'],
                                            cell_count=result['cell_count']
                                            )
            Inom *= result['cell_area']
            Unom *= result['cell_count']
            Pnom = Inom*Unom
        
        '**Selected panel: **', result['label']
        '**Number of cells in the solar module: **', result['cell_count']
        '**The area of one cell in the solar module: **', result['cell_area']
        p = figure(title = "I-V curve", plot_height=300, 
                    x_axis_label='Voltage (U), V ', y_axis_label='Current (I), A')
        p.line(Unom, Inom, line_width=2)
        p.add_tools(CrosshairTool())
        st.bokeh_chart(p, use_container_width=True)

        p2 = figure(title = "P-V curve", plot_height=300, 
                    x_axis_label='Voltage (U), V ', y_axis_label='Power (P), W')
        p2.line(Unom, Pnom, line_width=2)
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
                st.number_input('Specific short current value (I sc, A/cm2)')
                st.number_input('Specific max operation current (I nominal, A/cm2)')
            with col2:
                st.number_input('Open circuit voltage (U oc, V)')
                st.number_input('Max operation voltage (U nominal, V)')
            with col3:
                st.number_input('Calculated fill factor, %')
                st.number_input('Calculated efficiency, %')
            if st.button('Add to results'):
                st.session_state.journal[result['label']]=[0,0,0,0,0,0]             # here to change
            '''
            ---
            '''
            st.button('Clear all results')
            st.button('Clear last result')

        test = st.dataframe(st.session_state.journal)

        st.write(result)
        '''
        ---
        '''
    with conclusions_container:
        '''
        ### Conclusions  
        '''
          

if tab_selected == works[2]:
    introduction_container = st.container()

if tab_selected == works[3]:
    introduction_container = st.container()

if tab_selected == works[4]:
    introduction_container = st.container()



