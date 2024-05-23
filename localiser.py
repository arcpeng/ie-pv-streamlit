langs = ["RU","ENG"]

td = {
    'name': {
        'ENG':'PV cloud model',
        'RU':'Солнечная энергетика',
    },
    'sidebar_selector': {
        'ENG':'Choose the work: ',
        'RU':'Выберете работу: ',
    },
    'works': {
        'ENG': [
                'Introduction',
                'Work #1: I-V curves', 
                'Work #2: Influence of different light conditions on the solar cell work', 
                'Work #3: Influence of temperature on the solar cell work',
                'Work №4: Влияние температуры на выработку солнечных панелей',
                'Further reading'
                ],
        'RU': [
                'Введение', 
                'Работа №1: Характеристические кривые солнечных панелей', 
                'Работа №2: Влияние различных световых условий на выработку солнечных панелей', 
                'Работа №3: Влияние температуры на выработку солнечных панелей',
                'Работа №4: Влияние температуры на выработку солнечных панелей',
                'Полезная литература'
                ],
    },
    'work0': {
        'introduction':{
            'ENG':[ '''
                    The earliest living organisms on earth that learned to directly absorb 
                    solar energy and accumulate it were most likely plants. Plants use 
                    the energy carried by sunlight from the only one star in our system, 
                    the Sun, during photosynthesis, capturing carbon dioxide from 
                    the atmosphere and returning oxygen into it. At the same time, carbon 
                    remains in the plant, forming its *"green mass"*. But solar energy 
                    is converted not only into the energy of chemical bonds in plants. 
                    Almost all the energy on our planet is somehow connected with solar 
                    activity and man has learned to convert it into electrical energy.
                    ''',
                    '''
                    Due to the temperature difference of the air masses a pressure difference 
                    arises and wind that can twist the blades of the wind generator appears. 
                    By heating the earth and the planet's water resources the sun evaporates 
                    into the atmosphere a huge amount of water, which is transported for 
                    hundreds and thousands of kilometers, falling in the form of precipitation 
                    or freezing in glaciers. Streams of water form rivers and people again 
                    benefit from this by using hydroelectric power plants.
                    ''',
                    '''
                    Since the end of **the XIX century**, when scientists discovered the 
                    photoelectric effect, mankind has had a way to directly convert sunlight 
                    into electricity. The importance of the electricity generating technology 
                    directly from sunlight and an understanding of the principles underlying 
                    it are reflected in perhaps the most famous award in the field of 
                    science – the Nobel Prize. During **the XX century** various scientists 
                    whose work is important for this technology have been awarded the Nobel 
                    Prize several times. By the end of **the 50s of the XX century**, solar 
                    panels, which allowed to receive electricity in sufficient quantity for 
                    the operation of low-power devices, were developed. Almost immediately 
                    solar panels found their application in a variety of space vehicles. 
                    In this area they proved their irreplaceability. By the beginning of 
                    **the XXI century**, solar panel technologies had developed sufficiently 
                    to find industrial application in terrestrial conditions. Today 
                    there are some regions (for example, some territories of India) where 
                    the construction of a solar panel power plant is the cheapest and most 
                    effective way to electrify the area. Even in our rather northern and 
                    not the sunniest country, a number of solar power plants have been put 
                    into operation.  
                    ***
                    ''',
                ],
            'RU': [ '''
                    Первыми живыми организмами на земле, которые научились напрямую поглощать 
                    солнечную энергию и накапливать её, были, скорее всего, растения. Энергию, 
                    которую переносит солнечный свет от единственной звезды нашей системы – 
                    Солнца, – растения используют при фотосинтезе, улавливая углекислый газ 
                    из атмосферы и возвращая в неё кислород. Углерод при этом остается в 
                    растении, формирую его *«зелёную массу»*. Но солнечная энергия преобразуется 
                    не только в энергию химических связей в растениях. Практически вся энергия 
                    на нашей планете так или иначе связана с солнечной активностью, и человек 
                    научился преобразовывать её в электрическую.
                    ''',
                    '''
                    Из-за разницы температур воздушных масс возникает разность давления и 
                    появляется ветер, который может крутить лопасти ветрогенератора. Нагревая 
                    землю и водные ресурсы планеты, солнце в атмосферу выпаривает огромное 
                    количество воды, которая переносится на сотни и тысячи километров, 
                    выпадая в виде осадков или замерзая в ледниках. Потоки воды образуют 
                    реки, а человек снова извлекает из этого пользу, используя гидроэлектростанции.
                    ''',
                    '''
                    С конца **XIX века**, когда учёные открыли фотоэлектрический эффект, у 
                    человечества появился способ прямого преобразования солнечного света в 
                    электричество. Важность технологии получения электричества напрямую от 
                    солнечного света и понимание принципов, лежащих в её основе, нашли своё 
                    отражение и в, пожалуй, самой известной награде в области науки – 
                    Нобелевской премии. В течение **XX века** различные учёные, работы 
                    которых важны для данной технологии, несколько раз становились лауреатами 
                    Нобелевской премии. К концу **50-х годов XX века** были разработаны солнечные 
                    панели, которые позволяли получать электроэнергию в достаточном количестве 
                    для работы маломощных устройств. Практически сразу же солнечные панели нашли 
                    своё применение в разнообразных космических аппаратах. В этой области они 
                    оказались незаменимыми. К началу **XXI века** технологии солнечных панелей 
                    развились достаточно для того, чтобы найти себе промышленное применение в 
                    земных условиях. По состоянию на сегодняшний день есть отдельные регионы 
                    например, некоторые территории Индии), где строительство электростанции, 
                    на солнечных панелях, является самым дешевым и эффективным способом 
                    электрификации местности. Даже в нашей, казалось бы, достаточно северной 
                    и не самой солнечной стране введён в эксплуатацию целый ряд солнечных электростанций.
                    ***
                    '''
                ]
        },
        'basics':{
            'ENG': [ '''
                    ### The principle of solar cell operation  
                    ''',
                    '''
                    Let's take a look at how a solar cell works.   
                    ''',
                    '''
                    Figure 1. Schematic diagram of a solar cell
                    ''',
                ],
            'RU': [ '''
                    ### Принцип работы солнечной панели  
                    ''',
                    '''
                    Давайте разберём, как же работает солнечная панель.    
                    ''',
                    '''
                    Рисунок 1. Принципиальная схема фотоэлемента
                    ''',
                ],
        },
        'theory':{
            'ENG': ['''
                    A semiconductor-based photocell consists of two very thin layers (they 
                    must be permeable to photons), thickness **~0.2 mm**, with different types 
                    of conductivity, together forming a so-called *p-n-junction*. Metal contacts 
                    connected to the external circuit are wired to the layers from different sides. 
                    The role of the cathode is played by a layer with *n-conductivity* (a material 
                    with an excess of valence electrons is used, so characterized by electronic 
                    conductivity), the role of the anode is played by a layer with *p-conductivity* 
                    (a material with hole conductivity is used; a "hole" is a quasiparticle, in 
                    this context, it is a conditional "place" in a substance where there is no 
                    electron, but in which an electron can be; the directional movement of electrons 
                    when they occupy such "free" places, is commonly called an electric current 
                    in a substance with hole conductivity).
                    ''',
                    '''
                    When a photon is absorbed, a "pair" consisting of a "valence" electron and a 
                    "hole" may appear in the substance. Simplistically, we can assume that when a 
                    photon is absorbed, its energy goes to "knock out" the electron from the "place" 
                    which it occupied in the substance, as a result of which such a "pair" is formed. 
                    There is a small electric field at the boundary inside the *p-n-junction*. Such 
                    an effect occurs when any two substances come into contact and in the case of 
                    conductors is called a contact potential difference. In the area where such an 
                    electric field operates, the "pair" can "disintegrate" and under the influence 
                    of the electric field the electron and the "hole" will be on different sides 
                    of the border.
                    ''',
                    '''
                    As a result of this process, electrons and holes accumulate in the *n-* and 
                    *p-regions* respectively, it means that there is a potential difference between 
                    these regions. An electric current can be obtained by closing the circuit with 
                    the help of metal contacts and an external circuit.
                    ''',
                    '''
                    The potential value achieved on a single silicon-based photocell is small and 
                    is **~0.5 V** and the current through the photocell varies in proportion to its 
                    area and the number of photons absorbed by it. To obtain solar panels with sufficient 
                    voltage for practical purposes single solar cells are connected in series in the 
                    right amount (usually several dozen elements) and to increase the current single 
                    solar cells are connected in parallel or a solar cell with a large surface area 
                    is produced immediately. Thus, by combining connections, it is possible to achieve 
                    the required values of current and voltage, and therefore power.
                    ''',
                ],
            'RU': [ '''
                    Фотоэлемент на основе полупроводников состоит из двух очень тонких слоёв  
                    (чтобы они были проницаемы для фотонов) толщиной обычно  **~0,2 мм** с 
                    разным типом проводимости, совместно образующих так называемый *p-n-переход*. 
                    К слоям с разных сторон подведены металлические контакты, которые подключены 
                    к внешней цепи. Роль катода играет слой с *n-проводимостью* (применяется 
                    материал с избытком валентных электронов, то есть характеризуемый электронной 
                    проводимостью), роль анода – *p-слой* (материал с дырочной проводимостью; 
                    «дырка» – это квазичастица, в данном контексте это условное «место» в веществе, 
                    где нет электрона, но в котором электрон может оказаться; направленное движение 
                    электронов, когда они занимают такие «свободные» места, принято называть 
                    электрическим током в веществе с дырочной проводимостью). 
                    ''',
                    '''
                    При поглощении фотона в веществе может появится «пара» - «валентный» электрон 
                    и «дырка». Упрощённо можно считать, что при поглощении фотона его энергия 
                    идет на то, чтобы «выбить» электрон из того «места», которое он занимал в 
                    веществе, в результате чего и образуется такая «пара». На границе внутри 
                    *p-n-перехода* есть небольшое электрическое поле. Такой эффект имеет место 
                    при контакте между любыми двумя веществами и в случае проводников называется 
                    контактной разностью потенциалов. Оказавшись в области, где действует такое 
                    электрическое поле, «пара» может «распасться» и под действием электрического 
                    поля электрон и «дырка» окажутся по разные стороны от границы.
                    ''',
                    '''
                    В результате такого процесса в *n-* и *p-областях* накапливаются электроны 
                    и дырки соответственно, что означает, что между этими областями есть разность 
                    потенциалов. Замкнув цепь с помощью металлических контактов и внешней цепи, 
                    можно получить электрический ток.
                    ''',
                    '''         
                    Величина потенциала, достигаемая на одном фотоэлементе на основе кремния, 
                    маленькая и составляет **~0,5 В**, а сила тока через фотоэлемент изменяется 
                    пропорционально его площади и количеству поглощённых им фотонов. Для получения 
                    солнечных панелей с достаточным для практических целей напряжением единичные 
                    фотоэлементы соединяют последовательно в нужном количестве (обычно несколько 
                    десятков элементов), а для повышения силы тока параллельно или сразу производят 
                    фотоэлемент с большой площадью поверхности. Таким образом, комбинацией соединений 
                    можно добиться требуемых значений силы тока и напряжения, а следовательно, и мощности. 
                    ***
                    ''',
                ],
        },
        'what_next':{
            'ENG':[ '''
                    ### Further steps
                    ''',
                    '''
                    Please select a work from the sidebar.
                    Recommended reference list and useful web-links can be found in the "Further reading" tab.
                    ''',
                ],
            'RU':[  '''
                    ### Дальнейшие шаги
                    ''',
                    '''
                    Пожалуйста, выберете работу на панели слева.  
                    Рекомендуемый список литературы и полезные web-ресурсы можно найти во вкладке «Полезная литература».
                    ''',
                ],
        },
    },
    'work1': {
        'sidebar_subheader':{
            'ENG':'Model parameters',
            'RU':'Параметры модели',
        },
        'sidebar_selectbox':{
            'ENG':'Choose the solar panel: ',
            'RU':'Выберете солнечную панель: ',
        },
        'sidebar_button':{
            'ENG':'Calculate',
            'RU':'Расчёт',
        },
        'introduction':{
            'ENG':['''
                    ### Introduction and theory basics
                    ''',
                    '''
                    The main characteristic of solar cell is current-voltage characteristic 
                    or I-V curve (IVC).
                    ''',
                    '''
                    The **current-voltage characteristic (IVC)** is a function (as well as 
                    its graph) that defines the dependence of the current flowing through 
                    a two-pole network on the voltage on it. A two-pole network is any element 
                    of an electrical circuit containing two contacts for connection to other 
                    electrical circuits.
                    ''',
                    '''
                    The main operating characteristic of a solar battery is the maximum power, 
                    which is expressed in Watts (W). This characteristic shows the output power 
                    of the battery under optimal conditions: solar radiation of *1 kW/m2*, ambient 
                    temperature of 25 °C, standardized solar spectrum AM1.5 (solar spectrum at 
                    latitude 45°). Under normal conditions, it is extremely rare to achieve such 
                    parameters, because the illumination is lower and the module is heated higher 
                    (up to 60–70 °C).
                    ''',
                    '''
                    К характеристикам солнечных панелей также относятся следующие:  
                    - The **open circuit voltage** is the maximum voltage generated by a solar cell 
                    that occurs at zero current. It is equal to the forward bias corresponding to the 
                    change in the voltage of the p-n-junction when a light current appears. The 
                    idling voltage of the solar cell changes little when the illumination changes.  
                    - The **short-circuit current** is the current flowing through the solar cell 
                    when the voltage is zero (when the solar cell is shorted). The short-circuit 
                    current can be considered the maximum current that a solar cell can produce. 
                    In addition, it is directly proportional to the intensity of light.  
                    - The ** fill factor** is a parameter that, in combination with the open circuit 
                    voltage and the short-circuit current, determines the maximum power of the solar 
                    cell. It is calculated as the ratio of the maximum power of the solar cell to 
                    the product of the open circuit voltage and short-circuit current. The IVC 
                    filling factor is one of the main parameters by which the quality of a photoelectric 
                    converter can be evaluated. The higher the fill factor of the IVC the less losses 
                    in the element because of internal resistance.  
                    - The **efficiency coefficient (efficiency)** is the most common parameter by which 
                    the productivity of two solar cells can be compared. It is defined as the ratio of 
                    the power generated by the solar cell to the power of the incident solar radiation. 
                    In addition to the actual productivity of the solar cell, the **efficiency** also 
                    depends on the spectrum and intensity of the incident solar radiation and the 
                    temperature of the solar cell. Therefore, in order to compare two solar cells, 
                    it is necessary to carefully fulfill the accepted standard conditions. The efficiency 
                    of the solar cell is defined as part of the incident energy converted into electricity.  
                    ''',
                    '''
                    Monocrystalline solar panel
                    ''',
                    '''
                    The undoubted advantages are compactness and efficiency. Monocrystalline modules 
                    are still confident leaders in values of power, efficiency and durability. This 
                    is reflected in the cost: their price is high. Artificially grown silicon crystals 
                    are cut into thin plates. The module is based on purified silicon. The surface is 
                    more like a honeycomb or small cells that are interconnected into a single structure. 
                    The finished small plates are interconnected by a grid of electrical connections. In 
                    this case, the production process is the most labor-intensive and energy-consuming 
                    which effects on the final cost of the solar battery. But monocrystalline elements 
                    have better productivity, their average efficiency is around 22–25%.
                    ''',
                    '''
                    Polycrystalline solar panel
                    ''',
                    '''
                    They are made of silicon having a polycrystalline structure. Polycrystals are obtained 
                    as a result of gradual cooling of molten silicon. This method is simple, so such 
                    solar cells are rather cheap. Although their technical characteristics, including 
                    productivity, are quite lower (this is due to the "impurity" of the resulting silicon 
                    plates and their internal structure) – around 20%, but they are much cheaper than 
                    monocrystalline ones. Thanks to this, solar panels have ceased to be something 
                    inaccessible to ordinary people. A person with an average level of wealth may well 
                    take advantage of this offer. Polycrystalline solar battery has an inhomogeneous 
                    surface which is why it absorbs light worse and its efficiency respectively is lower. 
                    Such solar panels have a characteristic difference, it is the dark blue color of the coating.
                    ''',
                    '''
                    Organic solar panel
                    ''',
                    '''
                    In addition to silicon-based technologies, other areas are also developing, including 
                    those where the photoactive layer consists of organic substances. Panels made using this 
                    technology are lighter than silicon panels that is a great advantage for many applications. 
                    Another advantage is that organic solar panels have less impact on the environment. 
                    However, this circumstance is also associated with the disadvantage of organic panels, 
                    this is that their efficiency decreases relatively quickly because of environmental influences. 
                    Another disadvantage is the relatively low efficiency.      
                    ''',
                    '''
                    ---
                    ''',

            ],
            'RU':[ '''
                    ### Введение и элементы теории  
                    ''',
                    '''
                    Основной характеристикой солнечных панелей является их вольт-амперная характеристика (ВАХ).
                    ''',
                    '''
                    **Вольт-амперной характеристикой (ВАХ)** называют функцию (а также её график), 
                    задающую зависимость тока, протекающего через двухполюсник, от напряжения на нём. 
                    Двухполюсником называют любой элемент электрической цепи, содержащий два контакта 
                    для соединения с другими электрическими цепями.  
                    ''',
                    '''
                    Основной рабочей характеристикой солнечной батареи является максимальная мощность, 
                    которую выражают в Ваттах (Вт). Эта характеристика показывает выходную мощность 
                    батареи в оптимальных условиях: солнечном излучении *1 кВт/м²*, температуре окружающей 
                    среды 25 °C, стандартизованном солнечном спектре АМ1,5 (солнечный спектр на широте 45°). 
                    В обычных условиях достичь таких показателей удается крайне редко, т.к. освещенность ниже, 
                    а модуль нагревается выше (до 60–70 °C).
                    ''',
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
                    ''',
                    '''
                    Монокристаллическая солнечная панель
                    ''',
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
                    ''',
                    '''
                    Поликристаллическая солнечная панель
                    ''',
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
                    ''',
                    '''
                    Органическая солнечная панель
                    ''',
                    '''
                    Помимо технологий основанных на использовании кремния развиваются и другие направления, 
                    в том числе, когда фотоактивный слой состоит из органических веществ. Панели изготовленные 
                    по такой технологии легче кремниевых, что является большим преимуществом для многих прикладных 
                    задач. Еще одним плюсом является то, что органические солнечные панели оказывают меньшее 
                    воздействие на окружающую среду. Однако это обстоятельство сопряжено и с недостатком органических 
                    панелей - их эффективность относительно быстро падает из-за воздействия окружающей среды. Еще одним 
                    недостатком является относительно невысокий КПД.         
                    ''',
                    '''
                    ---
                    ''',
            ]
        },
        'work_description':{
            'ENG': ['''
                    ### Work objective
                     ** Objective ** of the work is to understand the principle of obtaining polarization or 
                    current-voltage curves for solar panels. During this work you will also learn about the 
                    key differences between different types of solar panels.  
                    ''',
                    '''
                    ---            
                    ''',
                    ],
            'RU': ['''
                    ### Цель работы
                    **Цель** работы заключается в понимании принципа построения 
                    поляризационных или вольт-амперных кривых для солнечных панелей.  
                    В ходе выполнения работы Вы также узнаете про ключевые отличия 
                    различных типов солнечных панелей.  
                    ''',
                    '''
                    ---            
                    ''',
                    ]
        },
        'practice':{
            'ENG': ['''
                    ### Practice
                    First of all, choose the solar panel you are interested in on 
                    the left sidebar. After clicking on the "Calculate" button the main 
                    parameters of the selected solar panel, the IVC and PWC curves will be displayed.
                    ''',
                    '**Selected panel: **',
                    '**Number of cells in the solar panel: **',
                    '**Area of one cell: **',
                    'I-V curve',
                    'Voltage (U), В ',
                    'Current (I), А',
                    'P-V curve',
                    'Power (P), Вт',
                    '''
                    According to the PVC graph determine the point corresponding to the maximum 
                    operating power of the selected solar panel. This point gives the maximum 
                    operating voltage in volts (V). To find the maximum operating current for 
                    this panel select the appropriate point on the IVC graph.
                    ''',
                    '''
                    To calculate the specific voltage and current density it is necessary to 
                    consider the serial connection of cells in the solar panel, as well as 
                    their area (shown above the graphs). After calculating these parameters, 
                    you can proceed to determining the values of the fill factor of the 
                    IVC and the efficiency of the selected solar panel.
                    ''',
                    '''
                    For more information refer to the section **"Introduction and theory basics"**
                    ''',
                    '''
                    Perform the proposed study for other types of solar panels and enter 
                    the results in the table below.    
                    ''',
                    '''Make a conclusion.''',
                    'Enter/edit results',
                    '''
                    ### Add a new result: 
                    ''',
                    'Specific short-circuit current (I sc, A/cm2)',
                    'Specific maximum operating current (I nominal, A/cm2)',
                    'Specific open circuit voltage (U oc, V)',
                    'Maximum operating voltage (U nominal, V)',
                    'Calculated panel fill factor, (Fill factor, %)',
                    'Calculated panel efficiency, (Efficiency, %)',
                    'Add results',
                    'Clear all results',
                    'Clear last result',
                    '''
                    ---            
                    ''',
                    ],
            'RU': ['''
                    ### Практическая часть
                    В первую очередь выберите интересующую вас солнечную панель слева. 
                    После нажатия на кнопку «Расчёт» будут выведены основные параметры 
                    выбранной солнечной панели, зависимости силы тока от напряжения 
                    и мощности от напряжения.
                    ''',
                    '**Выбранная панель: **',
                    '**Количество ячеек в солнечной панели: **',
                    '**Площадь одной ячейки: **',
                    'I-V зависимость',
                    'Напряжение (U), В ',
                    'Сила тока (I), А',
                    'P-V зависимость',
                    'Мощность (P), Вт',
                    '''
                    По графику зависимости мощности от напряжения определите точку, соответствующую максимуму 
                    рабочей мощности выбранной солнечной панели. Данная точка даёт максимум рабочего напряжения 
                    в вольтах (В). Чтобы найти максимальный рабочий ток для данной панели, на графике зависимости 
                    тока от напряжения необходимо выбрать соответствующую точку.
                    ''',
                    '''
                    Для расчёта удельного напряжения и плотности тока, необходимо учитывать 
                    последовательное соединение ячеек в солнечной панели, а также их площадь 
                    (приведено над графиками). После расчёта данных параметров можно перейти 
                    к определению величин коэффициента заполнения вольт-амперной характеристики 
                    и эффективности выбранной солнечной панели.
                    ''',
                    '''
                    Для получения дополнительной информации обратитесь к разделу **«Введение и элементы теории»**
                    ''',
                    '''
                    Проведите предложенное исследование для других типов солнечных панелей и введите полученные результаты
                    в таблицу ниже.    
                    ''',
                    '''Сделайте вывод.''',
                    'Ввести / изменить результаты',
                    '''
                    ### Добавить новый результат: 
                    ''',
                    'Удельная сила тока короткого замыкания (I sc, A/cm2)',
                    'Удельная максимальная рабочая сила тока (I nominal, A/cm2)',
                    'Напряжение открытой цепи (U oc, V)',
                    'Максимальное рабочее напряжение (U nominal, V)',
                    'Рассчитаный фактор заполнения, Fill factor, %',
                    'Рассчитанный коэффициент полезного действия, Efficiency, %',
                    'Добавить результаты',
                    'Очистить все результаты',
                    'Очистить последний результат',
                    '''
                    ---            
                    ''',
                    ]
        },
        'conclusions':{
            'ENG': ['Edit conclusions',
                    'Save',
                    '''
                    ### Conclusions  
                    ''',
                    '''
                    ---            
                    ''',
                    '''
                    *You can perform auto check results.*
                    ''',
                    'Auto check results',
                    '> Conclusions are not detailed enough!',
                    '> Not enough data. Explore more types of solar panels!',
                    '''
                    > #### Auto tests passed successfully.  
                    ''',
                    '''
                    *If required, you can print the report using Ctrl + P (Windows) or Cmd + P (MacOS)*
                    ''',
                    ],
            'RU': [
                    'Редактировать выводы',
                    'Сохранить',
                    '''
                    ### Выводы  
                    ''',
                    '''
                    ---            
                    ''',
                    '''
                    *Вы можете выполнить автоматическую проверку результатов.*
                    ''',
                    'Проверка результатов',
                    '> Выводы не достаточно развернуты!',
                    '> Мало данных. Исследуйте больше типов солнечных панелей',
                    '''
                    > #### Автоматические тесты успешно пройдены.  
                    ''',
                    '''
                    *Если требуется, можно распечатать отчет при помощи Ctrl+P (Windows) или Cmd+P (MacOS)*
                    ''',
                    ]
        },
    },
    'work2': {
        'sidebar_subheader':{
            'ENG':'Model parameters',
            'RU':'Параметры модели',
        },
        'sidebar_selectbox':{
            'ENG':'Choose the solar panel: ',
            'RU':'Выберете солнечную панель: ',
        },
        'sidebar_button':{
            'ENG':'Calculate',
            'RU':'Расчёт',
        },
        'introduction':{
            'ENG':['''
                    ### Introduction and theory basics
                    Sunlight travels from the Sun to the Earth in a straight line. When it reaches 
                    the atmosphere, part of the light is refracted, part reaches the Earth in a 
                    straight line and the other part is absorbed by the atmosphere. Refracted light 
                    is what is commonly referred to as diffuse radiation or scattered light. The part 
                    of sunlight that reaches the Earth's surface without scattering or absorption is 
                    direct radiation, and it is the most intense radiation. Solar panels produce 
                    electricity even in the absence of direct sunlight. So even in cloudy weather 
                    the photovoltaic system will produce electricity. However, the best conditions 
                    for generating electricity will be when the sun is bright and when the panels 
                    are oriented perpendicular to sunlight. For the northern hemisphere the panels 
                    should be oriented to the South, for the southern hemisphere - to the North.
                    ''',
                    '''
                    The Sun moves across the sky from East to West. The position of the Sun on the 
                    sky is determined by two coordinates - declination and azimuth (Fig. 1). 
                    Declination is the angle between the line connecting the observer and the Sun 
                    and the horizontal surface. Azimuth is the angle between the direction to the 
                    Sun and the direction to the South.
                    ''',
                    'Figure 1. Coordinates that determine Sun position on the sky',
                    '''
                    In practice, solar panels should be oriented at a certain angle to the horizontal 
                    surface. Small deviations from this orientation do not play a significant role, 
                    because during the day the Sun moves across the sky from East to West. 
                    For example, the share of energy generation by a photovoltaic system at 45° tilt angle 
                    for a latitude of 52° N:
                    - to the West – 78% 
                    - to the South-West – 94%
                    - to the South – 97%  
                    - to the South-East – 94%  
                    - to the East – 78%   
                    ''',
                    '''
                    Usually solar panels are located on the roof or supporting structure in a fixed 
                    position and cannot monitor the position of the Sun during the day. Therefore, 
                    they are not at the optimal angle (90°) throughout the day.
                    ''',
                    '''
                    The angle between the horizontal plane and the solar panel is called the tilt angle.
                    ''',
                    '''
                    Due to the movement of the Earth around the Sun, there are also seasonal variations 
                    in the tilt angle. In winter the Sun does not reach the same angle as in summer. 
                    Ideally, solar panels should be positioned more horizontally in summer than in winter. 
                    Therefore, the tilt angle for work in summer is chosen less than for work in winter. 
                    If it is not possible to change the tilt angle twice a year, then the panels should 
                    be positioned at the optimal angle, the value of which lies somewhere in the middle 
                    between the optimal angles for summer and winter. For each latitude there is an 
                    optimal tilt angle of the panels. Only near the equator should the solar 
                    panels be positioned horizontally.
                    ''',
                    '''
                    For spring and autumn the optimal tilt angle of solar panels is assumed to be equal 
                    to the latitude of the terrain, for winter 10−15° is added to this value, and in summer 
                    10−15° is subtracted from this value. Small deviations up to 5° from this optimum have 
                    a negligible effect on the productivity of the panels. The difference in weather 
                    conditions has a greater impact on electricity generation.  
                    For autonomous systems the optimal tilt angle of solar panels depends on the monthly 
                    load schedule: if more energy is consumed in a given month, then the tilt angle 
                    should be chosen optimal for that month. You also need to consider what kind of shading 
                    there is during the day. For example, if there is a tree on the East side and 
                    everything is clean on the West, then it makes sense to shift the orientation from the 
                    exact South to the South-West.                   
                    ''',
                    '''
                    ---
                    ''',

            ],
            'RU':[  '''
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
                    ''',
                    '''
                    Солнце двигается по небу с Востока на Запад. Положение Солнца на небосклоне 
                    определяется двумя координатами – склонением и азимутом (рис. 1). Склонение 
                    − это угол между линией, соединяющей наблюдателя и Солнце, и горизонтальной 
                    поверхностью. Азимут − это угол между направлением на Солнце и направлением на юг.
                    ''',
                    'Рисунок 1. Координаты, определяющие положение Солнца на небосклоне',
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
                    ''',
                    '''
                    Солнечные панели обычно располагаются на крыше или поддерживающей конструкции 
                    в фиксированном положении и не могут следить за положением Солнца в течение дня. 
                    Поэтому они не находятся под оптимальным углом (90°) в течение всего дня.
                    ''',
                    '''
                    Угол между горизонтальной плоскостью и солнечной панелью называют углом наклона. 
                    ''',
                    '''
                    Вследствие движения Земли вокруг Солнца имеют место также сезонные вариации угла 
                    наклона. Зимой Солнце не достигает того же угла, что и летом. В идеале солнечные 
                    панели должны располагаться летом более горизонтально, чем зимой. Поэтому угол 
                    наклона для работы летом выбирается меньше, чем для работы зимой. Если нет возможности 
                    менять угол наклона дважды в год, то панели должны располагаться под оптимальным углом, 
                    значение которого лежит где-то посередине между оптимальными углами для лета и зимы. 
                    Для каждой широты есть свой оптимальный угол наклона панелей. Только около экватора 
                    солнечные панели должны располагаться горизонтально. 
                    ''',
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
                    ''',
                    '''
                    ---
                    ''',
            ]
        },
        'work_description':{
            'ENG': ['''
                    ### Work objective
                    ** Objective ** of the work is to determine the dependence of the output 
                    haracteristics of the solar panel on its location on our planet, basically, 
                    on the tilt angle of the solar panel relative to the incident sunlight and 
                    the power of solar radiation. 
                    ''',
                    '''
                    ---            
                    ''',
                    ],
            'RU': ['''
                    ### Цель работы
                    **Цель** работы заключается в определении зависимости выходных характеристик солнечной 
                    панели от её местоположения на нашей планете, а именно от угла наклона солнечной панели 
                    относительно падающих солнечных лучей и мощности солнечного излучения.  
                    ''',
                    '''
                    ---            
                    ''',
                    ]
        },
        'practice':{
            'ENG': ['''
                    ### Practice
                    First of all, select the solar panel you are interested in on the sidebar and put
                    the tilt angle relative to the incident sun rays. Also set coordinates of the area 
                    you are interested in.
                    ''',
                    '''
                    After pushing the "Calculate" button, the IVC and PVC will be displayed, as 
                    well as the energy received under given conditions for each month of the year.
                    ''',
                    '''
                    Next, solve a few problems.
                    Make your own conclusion.
                    ''',
                    'Longitude',
                    'Latitude',
                    'Set the position',
                    'Tilt angle',
                    '** Selected panel: **',
                    'I-V curve',
                    'Voltage (U), V',
                    'Current (I), A',
                    'P-V curve',
                    'Power (P), W',
                    'Average monthly energy generation',
                    'Energy, kW * h',
                    'Maximum',
                    'Calculated',

                    'Task 1',
                    '''
                    Assume that in Skolkovo with coordinates:
                    > * 55.69553° N *
                    > * 37.35298° E *

                    one wants to build a new building with the roof equipped with monocrystalline
                    solar panels. There are four building designs, which, among other things, 
                    differ in angle. The slope of the roof can be: 16°, 24°, 32° and 43°. 
                    Determine which option is the most optimal in terms of the efficiency 
                    of solar panels. Consider sunny weather and the same tilt angle for all the panels.
                    ''',
                    'Answer as an integer:',

                    'Task 2',
                    '''
                    A hypothetically existing company "Friends of the Sun" is engaged in the construction of solar
                    power plants. The company uses organic solar panels that are mounted on racks, 
                    ensuring the position of the panel at an angle of 45° to the horizon. 
                    For the construction of another power plant with 500 solar panels, 
                    the company is considering several possible sites, basically:
                    (1) Near "Smena" center
                    ''',
                    '''
                    > *44.7831° N*  
                    > *37.3946° E*  

                    (2) Near Orenburg city  
                    > *51.8643° N*  
                    > *55.1015° E*  

                    (3) Near Gorno-Altaysk city  
                    > *51.9791° N*  
                    > *85.9813° E*  
                    ''',
                    '''
                    Estimate, during construction at which of these sites, the average 
                    annual capacity generated by the power plant will be maximum.
                    ''',
                    'Select answer:',

                    'Task 3',
                    '''
                    The Peterhof fountains are known for their beauty and diversity 
                    not only in Russia, but also far beyond its borders. Millions of tourists 
                    admire them every year. However, to ensure the operation of the fountains pumps, 
                    it is necessary to maintain the Peterhof electrical networks in very good condition, 
                    which is quite difficult to do in a city where such a high density of architectural 
                    monuments and cultural heritage sites. Suppose that to increase energy security, 
                    it was decided to install solar panels on some roofs of Peterhof buildings. Insofar as
                    the area of ​​the panels is very limited, it is necessary to install the most effective ones.
                    They should give the maximum amount of electricity during the operating period of the 
                    fountains - from May to September. Determine what type of solar panels are worth
                    use in this project.  
                    Approximate coordinates of buildings on which solar panels are planned to be placed:
                    > *59.879° N*  
                    > *29.898° E* 

                    Consider the tilt angle equals to 30°
                    ''',
                    'Selected solar panel:',
                    
                    'Task 4',
                    '''
                    You need to design a power system that consists of polycrystalline solar panels,
                    and can be installed in the area of Rostov-on-Don city:  
                    > *47.15623° N*  
                    > *39.56059° E*  

                    The power plant shoud provide the following output:  
                    > Constant voltage - *400 V*  
                    > Power - *2 kW*  

                    Estimate what is the minimum number of polycrystalline panels you need for this 
                    project and how they should be connected together.
                    ''',
                    'Enter the total number of panels:',
                    'Number of panels, connected in series in one unit:',
                    'Number of units connected in parallel:',
                    '''
                    *Note:*
                    The panels are connected in units, consisting of panels, connected * in series *.
                    These units are connected * in parallel *
                    ''',
                    '''
                    ---            
                    ''',
                    ],
            'RU': ['''
                    ### Практическая часть
                    В первую очередь выберите слева интересующую Вас солнечную панель и определите 
                    угол наклона солнечной панели относительно падающих солнечных лучей, а также установите 
                    координаты интересующей Вас местности.  
                    ''',
                    '''
                    После нажатия на кнопку «Расчёт» будут выведены зависимости силы тока от напряжения 
                    и мощности от напряжения, а также полученная при заданных условиях энергия за каждый месяц года.
                    ''',
                    '''
                    Далее решите несколько задач.
                    Сделайте вывод.
                    ''',
                    'Долгота',
                    'Широта',
                    'Установить позицию',
                    'Угол поворота',
                    '**Выбранная панель: **',
                    'I-V зависимость',
                    'Напряжение (U), В ',
                    'Сила тока (I), А',
                    'P-V зависимость',
                    'Мощность (P), Вт',
                    "Среднемесячная выработка энергии",
                    'Энергия, кВт*ч',
                    "Максимум",
                    "Расчёт",

                    'Задача 1',
                    '''
                    Предположим, что в Сколково в окрестностях точки с координатами:  
                    > *55.69553° с. ш.*  
                    > *37.35298° в. д.*  

                    планируют построить новое здание, крыша которого будет оборудована монокристаллическими 
                    солнечными панелями. Существует четыре проекта здания, которые в том числе отличаются углом 
                    наклона кровли, а именно: 16°, 24°, 32° и 43°. Определите, какой из вариантов является наиболее 
                    оптимальным с точки зрения эффективности работы солнечных панелей. Считайте, что солнечные 
                    панели находятся под таким же углом наклона, что и кровля.  
                    ''',
                    'Ответ в виде целого числа:',

                    'Задача 2',
                    '''
                    Гипотетически существующая компания «друзья Солнца» занимается строительством солнечных 
                    электростанций. Компания использует органические солнечные панели, которые крепятся на стойках, 
                    обеспечивающих положение панели под углом 45° к горизонту. Для строительства очередной электростанции 
                    с 500 солнечных панелей компания рассматривает несколько возможных площадок, а именно:  
                    ''',
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
                    ''',
                    '''
                    Оцените, при строительстве на какой из этих площадок средняя в течение года генерируемая электростанцией мощность будет максимальной.
                    ''',
                    'Выбранный вариант ответа:',

                    'Задача 3',
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
                    ''',
                    'Выбранная солнечная панель:',

                    'Задача 4',
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
                    ''',
                    'Введите общее количество панелей:',
                    'Из них последовательно соединенных в одном блоке:',
                    'Количество параллельно соединенных блоков:',
                    '''
                    *Примечание:*  
                    Панели соединены в блоки, состоящие из *последовательно* соединенных панелей. 
                    Данные блоки соединены *параллельно*
                    ''',
                    '''
                    ---            
                    ''',
                    ]
        },
        'conclusions':{
            'ENG': [
                    'Edit conclusions',
                    'Save',
                    '''
                    ### Conclusions  
                    ''',
                    '''
                    ---            
                    ''',
                    '''
                    *You can perform auto check results.*
                    ''',
                    'Auto check results',
                    '> Conclusions are not detailed enough!',
                    '> Check the answer to task 1!',
                    '> Check the answer to task 2!',
                    '> Check the answer to task 3!',
                    '> Check the answer to task 4!',
                    '''
                    > #### Auto tests passed successfully.  
                    ''',
                    '''
                    *If required, you can print the report using Ctrl + P (Windows) or Cmd + P (MacOS)*
                    ''',
                    ],
            'RU': [
                    'Редактировать выводы',
                    'Сохранить',
                    '''
                    ### Выводы  
                    ''',
                    '''
                    ---            
                    ''',
                    '''
                    *Вы можете выполнить автоматическую проверку результатов.*
                    ''',
                    'Проверка результатов',
                    '> Выводы не достаточно развернуты!',
                    '> Проверьте ответ к задаче 1!',
                    '> Проверьте ответ к задаче 2!',
                    '> Проверьте ответ к задаче 3!',
                    '> Проверьте ответ к задаче 4!',
                    '''
                    > #### Автоматические тесты успешно пройдены.  
                    ''',
                    '''
                    *Если требуется, можно распечатать отчет при помощи Ctrl+P (Windows) или Cmd+P (MacOS)*
                    ''',
                    ]
        },
    },
    'work3': {
        'sidebar_subheader':{
            'ENG':'Model parameters',
            'RU':'Параметры модели',
        },
        'sidebar_selectbox':{
            'ENG':'Choose the solar panel: ',
            'RU':'Выберете солнечную панель: ',
        },
        'sidebar_button':{
            'ENG':'Calculate',
            'RU':'Расчёт',
        },
        'introduction':{
            'ENG':['''
                    ### Introduction and basic theory
                    Solar panels, like other electronic equipment, operate due to electrical processes 
                    controlled by the laws of thermodynamics. And the laws of thermodynamics say that 
                    with an increase in heat, power decreases. The rise in temperature creates internal 
                    resistance within the solar cell, which reduces its efficiency. That is, with an 
                    increase in temperature, the flow of electrons inside the element increases, which 
                    causes an increase in the current and a drop in voltage. At the same time, the 
                    voltage drop is greater than the increase in current, so the total power decreases, 
                    which leads to the panel operating with less efficiency. In other words, its efficiency 
                    becomes lower. Therefore, the warmer the ambient temperature, the lower the 
                    output power of the solar cells.
                    ''',
                    '''
                    The losses are determined by ** "temperature coefficient" **.  
                    ** Temperature Coefficient ** is the percentage of efficiency degradation with reference
                    to degrees Celsius. It shows how much the efficiency of the solar panels when the air 
                    temperature rises by one degree. Usually this value is obtained empirically by manufacturer 
                    (and indicated in the specifications). Of course, it differs depending on the solar panel model.
                    ''',
                    '''
                    Solar panels are tested at 25 °C and manufacturers usually indicate their efficiency, 
                    considering 25 °C as the norm. If the temperature coefficient of the solar panel is -0.50, 
                    it means that the output power will decrease by 0.50% for each degree above 25 °C. 
                    Despite the fact that such the number seems insignificant, the temperature of the dark 
                    roof, on which the panel is installed, can be well above 25 °C on a hot sunny day. 
                    In the summer, the own temperature of the solar panel can rise to 60-70 °C. Usually 
                    the increase of panel temperature by 20 °C leds to the power loss be about 10%.
                    ''',
                    '''
                    Thermal coefficient of silicon poly- and monocrystalline panels usually ranges from -0.45% 
                    to -0.50%. The thermal coefficient of amorphous solar panels is lower (from -0.20% to -0.25%). 
                    However, their initial efficiency is lower than that of mono- and polycrystalline.
                    If an increase in temperature contributes to a decrease in the efficiency of solar panels,
                    then a slight decrease in temperature can, on the contrary, increase the efficiency of solar
                    panels: voltage may even be higher than nominal.
                    ''',
                    '''
                    ---
                    ''',
            ],
            'RU':[  '''
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
                    ''',
                    '''
                    Потери определяются **«температурным коэффициентом»**. 
                    **Температурный коэффициент** − это процент снижения эффективности с привязкой 
                    к градусам по Цельсию. Он показывает, насколько падает эффективность солнечной 
                    панели при повышении температуры воздуха на градус. Значение коэффициента 
                    производитель панелей получают опытным путем (и указывают в спецификациях). 
                    Оно разнится в зависимости от модели солнечной панели.
                    ''',
                    '''
                    Тестирование параметров солнечных панелей проводится при температуре 25°C и 
                    обычно производители указывают их эффективность, принимая за норму 25°C.
                    Если температурный коэффициент солнечной панели -0.50, это означает, что выход 
                    мощности снизится на 0,50% за каждый градус выше 25°C. Несмотря на то, что такая 
                    цифра кажется незначительной, температура тёмной крыши, на которой установлена панель, 
                    может быть значительно выше 25°C в жаркий солнечный день. В летний период собственная 
                    температура солнечной батареи может подниматься до 60−70°C. В среднем при повышении 
                    температуры панели на 20°C, потери мощности составят порядка 10%. 
                    ''',
                    '''
                    Тепловой коэффициент кремниевых поли- и монокристаллических панелей в среднем 
                    колеблется от -0.45% до -0.50%. Тепловой коэффициент аморфных солнечных панелей ниже 
                    (от -0,20% до -0,25%), однако их изначальная эффективность ниже, чем у моно- и поликристаллических.
                    Если повышение температуры способствует снижению КПД солнечных панелей, 
                    то некоторое понижение температуры может, наоборот, увеличить эффективность солнечных 
                    элементов: напряжение может быть даже выше номинального. 
                    ''',
                    '''
                    ---
                    '''
            ]
        },
        'work_description':{
            'ENG': ['''
                    ### Work objective
                     ** Objective ** of the work is to determine the dependence of the output characteristics of the solar
                     panels from its location on our planet, basically from the tilt angle of the solar panel
                     in relation to incident sunlight, solar radiation power and solar panel temperature.
                    ''',
                    '''
                    ---            
                    ''',
                    ],
            'RU': [ '''
                    ### Цель работы
                    ** Цель работы ** заключается в определении зависимости выходных характеристик солнечной 
                    панели от её местоположения на нашей планете, а именно от угла наклона солнечной панели 
                    относительно падающих солнечных лучей, мощности солнечного излучения и температуры солнечных 
                    панелей.
                    ''',
                    '''
                    ---
                    ''',    
                    ]
        },
        'practice':{
            'ENG': [''' 
                    ### Practice
                    First of all, select the solar panel you are interested in on the sidebar and determine the tilt angle of the solar
                    panel relative to the incident sun rays. Also set the coordinates. After clicking on the "Calculation" button, the 
                    energy, provided under the specified conditions will be displayed for each month of the year.
                    ''',
                    '''
                    Next, solve a few problems.
                    Make your own conclusion.
                    ''',
                    'Longitude',
                    'Latitude',
                    'Set the position',
                    'Tilt angle',
                    '** Selected panel: **',
                    'I-V curve',
                    'Voltage (U), V',
                    'Current (I), A',
                    'P-V curve',
                    'Power (P), W',
                    'Average monthly energy generation',
                    'Energy, kW * h',
                    'Maximum',
                    'Calculated',
                    'Corrected',

                    'Task 1',
                    '''
                    The  solar power plant near Samara city has the following coordinates: 
                    > *53.01° N*  
                    > *49.80° E*  

                    Monocrystalline solar panels are used there. Determine (round to integers),
                    what percentage of electricity is lost in summer due to heating of solar panels from the surrounding
                    air. Consider that the angle of the solar panels is optimal. 
                    ''',
                    'Lost Electricity, % :',

                    'Task 2',
                    '''
                    In the previous work we were trying to solve the problem, in which 
                    hypothetically existing company "Friends of the Sun" is considering the construction 
                    of another power plant with 500 solar panels on several possible sites:
                    (1) Near "Smena" center
                    > *44.7831° N*  
                    > *37.3946° E*  

                    (2) Near Orenburg city  
                    > *51.8643° N*  
                    > *55.1015° E*  

                    (3) Near Gorno-Altaysk city  
                    > *51.9791° N*  
                    > *85.9813° E*  
                    ''',
                    '''
                    Taking into account the influence of ambient air temperature, estimate on which of these sites
                    the average annual capacity generated by the power plant will be maximum. 
                    Consider using organic solar panels, mounted on racks at 45 ° tilt angle (to the horizon). 
                    ''',
                    'Choose the wright answer:',

                    'Task 3',
                    '''
                    Until now, we have a large number of places on the planet that still await its development
                    and where people practically do not live. Among such places, many are of interest
                    for archaeologists. Of course, archaeologists need electricity for their everyday life. 
                    If we are talking about the Arctic expedition, which goes during the "polar day", 
                    then one can consider using solar panels as a main source of electricity.
                    ''',
                    '''
                    Consider a hypothetical expedition to the places of distribution of the Ust-Poluy culture,
                    whose representatives lived on the area of the Yamal Peninsula. This expedition
                    will be held in June, and the camp will be located at the point with coordinates: 
                    > *65.557° N*  
                    > *69.074° E*  

                    Determine what type of solar panels archaeologists should take with them in order to
                    had the highest efficiency, taking into account the influence of the ambient temperature. 
                    Consider that the used tilt angle of solar panels is optimal. 
                    ''',
                    'Choose the solar panel:',
                    '''
                    ---            
                    ''',
                    ],
            'RU': [ '''
                    ### Практическая часть
                    В первую очередь выберите слева интересующую Вас солнечную панель и определите угол наклона солнечной 
                    панели относительно падающих солнечных лучей, а также установите координаты интересующей 
                    Вас местности. После нажатия на кнопку «Расчёт» будет выведена полученная при заданных условиях 
                    энергия за каждый месяц года.
                    ''',
                    '''
                    Далее решите несколько задач.
                    Сделайте вывод.
                    ''',
                    'Долгота',
                    'Широта',
                    'Установить позицию',
                    'Угол поворота',
                    '**Выбранная панель: **',
                    'I-V зависимость',
                    'Напряжение (U), В ',
                    'Сила тока (I), А',
                    'P-V зависимость',
                    'Мощность (P), Вт',
                    "Среднемесячная выработка энергии",
                    'Энергия, кВт*ч',
                    "Максимум",
                    "Расчёт",
                    'Коррекция',

                    'Задача 1',
                    '''
                    На Самарской солнечной электростанции с координатами:  
                    > *53.01° с. ш.*  
                    > *49.80° в. д.*  

                    используются монокристаллические солнечные панели. Определите (с точностью до единиц), 
                    какой процент электроэнергии теряется летом за счет нагрева солнечный панелей окружающим 
                    воздухом. Считайте, что угол положения солнечных панелей оптимальный. 
                    ''',
                    'Процент потерянной электроэнергии:',

                    'Задача 2',
                    '''
                    В предыдущей работе рассматривалась задача, в которой гипотетически существующая 
                    компания «друзья Солнца» рассматривает для строительства очередной электростанции 
                    с 500 солнечных панелей несколько возможных площадок, а именно:
                    (1) В окрестностях ВДЦ «Смена»
                    > *44.7831° с. ш.*  
                    > *37.3946° в. д.*  

                    (2) в окрестностях города Оренбург  
                    > *51.8643° с. ш.*  
                    > *55.1015° в. д.*  

                    (3) в окрестностях города Горно-Алтайск  
                    > *51.9791° с. ш.*  
                    > *85.9813° в. д.*  
                    ''',
                    '''
                    Оцените, при строительстве на какой из этих площадок с учетом влияния температуры 
                    окружающего воздуха средняя в течение года генерируемая электростанцией мощность будет 
                    максимальной. На электростанции планируется использовать органические солнечные панели, 
                    которые крепятся на стойках, обеспечивающих положение панели под углом 45° к горизонту. 
                    ''',
                    'Выбранный вариант ответа:',

                    'Задача 3',
                    '''
                    До сих пор у нас на планете есть большое количество мест, которые еще ждут своего 
                    освоения и где практически не живут люди. Среди таких мест многие представляют интерес 
                    для археологов, которые отправляются в экспедиции в такие места. Для обеспечения 
                    быта археологов им необходима электроэнергия. Если речь идет об Арктической экспедиции, 
                    которая выпадает на “полярный день”, то можно рассмотреть возможность использования 
                    солнечных панелей в качестве источника электроэнергии.  
                    ''',
                    '''
                    Рассмотрим гипотетическую экспедицию в места распространения Усть-полуйской культуры, 
                    представители которой проживали на территории полуострова Ямал. Считая, что экспедиция 
                    будет проводится в июне, а лагерь археологов будет находится в точке с координатами: 
                    > *65.557° с. ш.*  
                    > *69.074° в. д.*  

                    определите, какого типа солнечные панели стоит взять археологам для того, чтобы они 
                    обладали наибольшей эффективностью с учетом влияния температуры окружающего воздуха 
                    на их работу. Считайте, что угол положения солнечных панелей оптимальный. 
                    ''',
                    'Выбранная солнечная панель:',
                    '''
                    ---            
                    ''',
                    ]
        },
        'conclusions':{
            'ENG': [
                    'Edit conclusions',
                    'Save',
                    '''
                    ### Conclusions  
                    ''',
                    '''
                    ---            
                    ''',
                    '''
                    *You can perform auto check results.*
                    ''',
                    'Auto check results',
                    '> Conclusions are not detailed enough!',
                    '> Check the answer to task 1!',
                    '> Check the answer to task 2!',
                    'Monocrystal',
                    '> Check the answer to task 3!',
                    '''
                    > #### Auto tests passed successfully.  
                    ''',
                    '''
                    *If required, you can print the report using Ctrl + P (Windows) or Cmd + P (MacOS)*
                    ''',
                    ],
            'RU': [
                    'Редактировать выводы',
                    'Сохранить',
                    '''
                    ### Выводы  
                    ''',
                    '''
                    ---            
                    ''',
                    '''
                    *Вы можете выполнить автоматическую проверку результатов.*
                    ''',
                    'Проверка результатов',
                    '> Выводы не достаточно развернуты!',
                    '> Проверьте ответ к задаче 1!',
                    '> Проверьте ответ к задаче 2!',
                    'Монокристаллическая',
                    '> Проверьте ответ к задаче 3!',
                    '''
                    > #### Автоматические тесты успешно пройдены.  
                    ''',
                    '''
                    *Если требуется, можно распечатать отчет при помощи Ctrl+P (Windows) или Cmd+P (MacOS)*
                    ''',
                    ]
        },
    },
    'work4': {
        'ENG':[ '''
                ### Literature
                ''',
                '''
                - *Renewable Energy in the Modern World: A Study Guide* /
                 O.S. Popel, V.E. Fortov - 2nd ed., Publishing house
                 MEI, 2018 - 450 p.
                - *Energetics in the Modern World: Scientific Edition* / V.E. Fortov,
                 O.S. Popel - Dolgoprudny: Intellect Publishing House, 2011 - 168 p.
                 - *Study of solar photovoltaic cells: Educational-methodological
                 edition* / Bessel V.V., Kucherov V.G., Mingaleeva R.D., Publishing
                 Center of the Russian State University of Oil and Gas (NRU), 2016 - 90 p.
                ''',
                '''
                ### Web-links
                ''',
                '''
                - [Post.Science: Solar Energy](https://postnauka.ru/themes/solnechnaya-energiya)  
                - [Wiki: Solar Power](https://en.wikipedia.org/wiki/Solar_power)  
                - [Wiki: Solar Cell](https://en.wikipedia.org/wiki/Solar_panel)
                - [Wiki: Organic Solar Cell](https://en.wikipedia.org/wiki/Organic_solar_cell)
                - [Richard Komp: How do solar panels work?](https://www.youtube.com/watch?v=xKxrkht7CpY)
                - [Lesics: How do solar cells work?](https://www.youtube.com/watch?v=L_q6LRgKpTw)
                '''

        ],
        'RU':[  '''
                ### Литература
                ''',
                '''
                - *Возобновляемая энергетика в современном мире: Учебное пособие* / 
                О. С. Попель, В. Е. Фортов – 2-е изд., стер. – М: Издательский дом 
                МЭИ, 2018. – 450 с.: ил.  
                - *Энергетика в современном мире: Научное издание* / В. Е. Фортов, 
                О. С. Попель – Долгопрудный: Издательский Дом «Интеллект», 2011. – 168 с.  
                - *Изучение солнечных фотоэлектрических элементов: Учебно-методическое 
                пособие* / Бессель В. В., Кучеров В. Г., Мингалеева Р. Д. – М.: Издательский 
                центр РГУ нефти и газа (НИУ) имени И. М. Губкина, 2016. – 90 с.  
                ''',
                '''
                ### Web-ресурсы
                ''',
                '''
                - [Пост.Наука: Солнечная энергия](https://postnauka.ru/themes/solnechnaya-energiya)  
                - [Wiki: Солнечная энергетика](https://ru.wikipedia.org/wiki/Солнечная_энергетика)  
                - [Wiki: Солнечная генерация](https://ru.wikipedia.org/wiki/Солнечная_генерация)  
                - [Wiki: Солнечная батарея](https://ru.wikipedia.org/wiki/Солнечная_батарея)
                - [Wiki: Полимерная солнечная батарея](https://ru.wikipedia.org/wiki/Полимерные_солнечные_батареи)
                - [Richard Komp: How do solar panels work?](https://www.youtube.com/watch?v=xKxrkht7CpY)
                - [Lesics: How do solar cells work?](https://www.youtube.com/watch?v=L_q6LRgKpTw)
                '''
        ]
        
    }
}