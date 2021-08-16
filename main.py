from pathlib import WindowsPath
import numpy as np
from scipy.optimize import curve_fit
from requests.api import head
import streamlit as st
import requests
from bokeh.plotting import figure

st.set_page_config(page_title=None, page_icon=None, layout='wide', initial_sidebar_state='auto')

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

    with introduction_container:
        '''
        ### Introduction & theoretical background  
        A **current–voltage characteristic** or **I–V curve** 
        (current–voltage curve) is a relationship, typically represented 
        as a chart or graph, between the electric current through a circuit, 
        device, or material, and the corresponding voltage, or potential 
        difference across it.
        '''

    if st.sidebar.button('Calculate'):
        st.write(selected_panel)
        result = get_ivc(selected_panel)
        [Unom, Inom, Pnom] = calculate_ivc(I_max=result['I_max'], 
                                           U_max=result['U_max'], 
                                           Isc=result['Isc'],
                                           Uoc=result['Uoc'], 
                                           cell_area=result['cell_area'],
                                           cell_count=result['cell_count']
                                           )
        st.write(result)
        p = figure(plot_width=500, plot_height=300)
        p.line(Unom, Inom)
        st.bokeh_chart(p, use_container_width=True)
        st.line_chart([Unom, Inom])

if tab_selected == works[2]:
    introduction_container = st.container()

if tab_selected == works[3]:
    introduction_container = st.container()

if tab_selected == works[4]:
    introduction_container = st.container()



