"""
Scrapes the data required for my Analysis of UK School Performance project

Scrapes the parliamentary constituencies from wikipedia [1] and stores them 
in the .txt file 'uk_parliamentary_constituencies.txt'. 

Aquires the following data for all primary schools in the UK:
    - school name
    - school unique reference number (URN)
    - parliamentary_constituency
    - reading band
    - reading progress score
    - reading progress score confidence interval
    - writing band
    - writing progress score
    - writing progress score confidence interval
    - maths band
    - maths progress score
    - maths progress score confidence interval
    - percentage of pupils meeting the expected standard in reading, writing and maths (school)
    - percentage of pupils meeting the expected standard in reading, writing and maths (local authority average)
    - percentage of pupils meeting the expected standard in reading, writing and maths (england average)
    - percentage of pupils achieving at a higher standard in reading, writing and maths (school)
    - percentage of pupils achieving at a higher standard in reading, writing and maths (local authority average)
    - percentage of pupils achieving at a higher standard in reading, writing and maths (england average)
    - average score in reading (school)
    - average score in reading (local authority average)
    - average score in reading (england average)
    - average score in maths (school)
    - average score in maths (local authority average)
    - average score in maths (england average)
    - overall absence (school)
    - persistent absence (school)
    - total number of pupils on roll (school)
    - total number of pupils on roll (england - mainstream primary schools) 
    - the percentage of girls (school)
    - the percentage of girls (england - mainstream primary schools)
    - the percentage of boys (school)
    - the percentage of boys (england - mainstream primary schools)
    - the percentage of pupils with SEN Education, Health and Care Plan (school)
    - the percentage of pupills with SEN Education, Health and Care Plan (england - mainstream primary schools)
    - the percentage of pupils with SEN Support (school)
    - the percentage of pupils with SEN Support (england - mainstream primary schools)
    - the percentage of EAL students (school)
    - the percentage of EAL students (england - mainstream primary schools)
    - the percentage of pupils eligible for free school means at any time during the past 6 years (school)
    - the percentage of pupils eligible for free school means at any time during the past 6 years (england - mainstream primary schools)
    
At the time of writing the pupil absence data is from the academic year
2021/2022. Due to the uneven impact of the pandemic on 2021/2022 
school absence data, I will not make any comparisons with local and 
national averages.
    
Creates the file 'uk_primary_school_data.csv'. If the file already exists,
it will output a message saying that the file already exists before 
rewriting the file. 

TODO: Take into account additional measures
TODO: Take into account results by pupil characteristics 

Parameters
----------
user_agent : str
    The user agent to be used when making html requests.

Notes
-----
The user agent in the example below is obtained from 
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent [2].    

Examples
--------
>>> python DataAquisition.py "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"

References
----------

[1] Wikipedia contributors. (2024, February 6). Constituencies of the 
    Parliament of the United Kingdom. In Wikipedia, The Free Encyclopedia.
    Retrieved 15:46, February 11, 2024, from 
    https://en.wikipedia.org/w/index.php?title=Constituencies_of_the_Parliament_of_the_United_Kingdom&oldid=1204196556

[2] gregbirch, iigmir, mfuji09, darby, Tigit, ExE-Boss, fscholz, 
    an_editor, wbamberg, hamishwillee, queengooborg, teoli2003, nshonni,
    rubiesonthesky, Josh-Cena, shaedrich, dipikabh, sideshowbarker. 
    "User - Agent - HTTP | MDN". mdn web doc.
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent
    (accessed Dec. 30, 2023).  
    
"""

from typing import List, Tuple
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
from joblib import Parallel, delayed

def get_user_agent() -> str:
    """
    Returns the user agent to be used when making html requests. 

    Reads the user agent from the file 'user_agent.txt' and returns it.
    If the file 'user_agent.txt' does not exist, then a FileNotFoundError
    is raised.

    Returns
    -------
    user_agent : str
        The user agent to be used when making html requests.
    """

    try:
        with open('data/user_agent.txt', 'r') as file:
            user_agent = file.read()
    except FileNotFoundError:
        raise FileNotFoundError("The file 'user_agent.txt' does not exist. Please create a file 'user_agent.txt' in the 'data' directory and enter your user agent.")

    return user_agent

def read_parliamentary_constituencies() -> List[str]:
    """
    Returns a list of all the parliamentary constituencies in the UK. 

    This function is only called if the file 
    'uk_parliamentary_constituencies.txt' exists. It reads the file 
    'uk_parliamentary_constituencies.txt' and returns a list of all the 
    parliamentary constituencies contained within the file. 

    Returns
    -------
    uk_parliamentary_constituencies() : List[str]
        A list of all the parliamentary constituencies in the UK.
    """

    with open('data/uk_parliamentary_constituencies.txt', 'r') as file:
        uk_parliamentary_constituencies = file.readlines() 

    uk_parliamentary_constituencies = [constituency.strip('\n') for constituency in uk_parliamentary_constituencies]
    
    return uk_parliamentary_constituencies

def scrape_parliamentary_constituencies() -> List[str]:
    """
    Returns a list of all the parliamentary constituencies in the UK. 

    This function is only called if the file 
    'uk_parliamentary_constituencies.txt' does not exists. It scrapes 
    wikipedia to obtain and return a list of all the parliamentary 
    constituencies in the UK and creates the file 
    'uk_parliamentary_constituencies.txt'. 

    Returns
    -------
    uk_parliamentary_constituencies : List[str]
        A list of all the parliamentary constituencies in the UK.
    """

    PARLIAMENTARY_DATA_URL = "https://en.wikipedia.org/w/index.php?title=Constituencies_of_the_Parliament_of_the_United_Kingdom&oldid=1204196556"

    soup = get_soup(PARLIAMENTARY_DATA_URL)

    rows = soup.select("table#England tr")

    uk_parliamentary_constituencies = []

    for row in rows[1:]:
        cells = row.select("td")
        constituency = cells[0].text.strip()
        uk_parliamentary_constituencies.append(constituency)

    with open('data/uk_parliamentary_constituencies.txt', 'w') as file:
        for constituency in uk_parliamentary_constituencies:
            file.write(constituency + '\n')

    return uk_parliamentary_constituencies

def get_parliamentary_constituencies() -> List[str]:
    """
    Returns a list of all the parliamentary constituencies in the UK. 

    First checks if there exists a file called 
    'uk_parliamentary_constituencies.txt' If such a file exists, it is 
    calls the function 'read_parliamentary_constituencies(). If such a 
    file does not exist, it calls the function
    'scrape_parliamentary_constituencies()'.

    Returns
    -------
    uk_parliamentary_constituencies() : List[str]
        A list of all the parliamentary constituencies in the UK.
    """

    with open('data/uk_parliamentary_constituencies.txt', 'a+') as file:
        uk_parliamentary_constituencies = file.readlines()

        if not uk_parliamentary_constituencies:
            uk_parliamentary_constituencies = scrape_parliamentary_constituencies()
        else:
            uk_parliamentary_constituencies = read_parliamentary_constituencies()

    return uk_parliamentary_constituencies

def read_school_identification_information() -> pd.DataFrame:
    """
    Returns a pd.DataFrame containing the name and URN of all UK schools. 

    This function is only called if the file 
    'uk_school_identification_information.csv' exists. 
    It returns the pd.DataFrame stored within the
    'uk_school_identification_information.csv' file.
    This pd.DataFrame contains the name and Unique Identification Number
    (URN) for every school in the UK.

    Returns
    -------
    uk_school_identification_information : pd.DataFrame
        A pd.DataFrame containing the name and URN of every UK school.
    """

    with open('data/uk_school_identification_information.csv', 'r') as file:
        uk_school_identification_information = pd.read_csv(file, index_col=0)

    return uk_school_identification_information

def scrape_school_identification_information() -> pd.DataFrame:
    """
    Returns a pd.DataFrame containing the name and URN of all UK schools. 

    This function is only called if the file
    'uk_school_identification_information.csv' does not exist. 
    It scrapes the gov.uk website to obtain and return a pd.DataFrame 
    containing the name and Unique Identification Number (URN) for every
    school in the UK. It then saves this pd.DataFrame in the file 
    'uk_school_identification_information.csv'.S

    Returns
    -------
    uk_school_identification_information : pd.DataFrame
        A pd.DataFrame containing the name and URN of every UK school.
    """

    parliamentary_constituencies = get_parliamentary_constituencies()

    parliamentary_constituency_subsets = [parliamentary_constituencies[i:i+10] for i in range(0, len(parliamentary_constituencies), 10)]

    school_identification_dataframes = Parallel(n_jobs=-2)(delayed(scrape_school_identification_information_subset_of_constituencies)(parliamentary_constituency_subset) for parliamentary_constituency_subset in parliamentary_constituency_subsets)

    if school_identification_dataframes:
        filtered_dataframes = [df for df in school_identification_dataframes if df is not None]

    uk_school_identification_information = pd.concat(filtered_dataframes)

    uk_school_identification_information.to_csv('data/uk_school_identification_information.csv')

    uk_school_identification_information['school_urn'] = uk_school_identification_information['school_urn'].astype('int64')

    return uk_school_identification_information

def scrape_school_identification_information_subset_of_constituencies(parliamentary_constituencies: list[str]) -> pd.DataFrame:
    """
    Returns a pd.DataFrame containing the name and URN of all primary schools in the given parliamentary constituencies.

    Calls the scrape_single_parliamentary_constituency_school_identification_information() function for each parliamentary constituency
    in the given list of parliamentary constituencies and concatenates the resulting pd.DataFrames to obtain a single pd.DataFrame 
    containing the name and URN of every primary school in the given parliamentary constituencies.

    Parameters
    ----------
    parliamentary_constituencies : list[str]
        A list of the parliamentary constituencies whose data is to be obtained.

    Returns
    -------
    parliamentary_constituency_school_identification_information : pd.DataFrame
        A pd.DataFrame containing the name and URN of every primary school in the given parliamentary constituencies.
    """

    parliamentary_constituency_school_identification_information = pd.DataFrame()

    for parliamentary_constituency in parliamentary_constituencies:
        parliamentary_constituency_school_identification_information = pd.concat([parliamentary_constituency_school_identification_information, scrape_single_parliamentary_constituency_school_identification_information(parliamentary_constituency)])

    return parliamentary_constituency_school_identification_information

def get_single_parliamentary_constituency_url(parliamentary_constituency: str) -> str:
    """
    Returns the URL to the .gov Web page containing the list of primary schools in the specified parliamentary constituency.

    Parameters
    ----------
    parliamentary_constituency : str
        The name of the parliamentary constituency whose data is to be obtained. 

    Returns
    -------
    parliamentary_constituency_url : str
        The url to the Web page containing the list of primary schools in the specified parliamentary constituency.

    """
    parliamentary_constituency_words = parliamentary_constituency.split()
    formatted_parliamentary_constituency = '+'.join(parliamentary_constituency_words)

    parliamentary_constituency_url = f'https://www.compare-school-performance.service.gov.uk/schools-by-type?step=default&table=schools&parliamentary={formatted_parliamentary_constituency}&geographic=parliamentary&for=primary'

    return parliamentary_constituency_url

def scrape_single_parliamentary_constituency_school_identification_information(parliamentary_constituency: str) -> pd.DataFrame:
    """
    Returns a pd.DataFrame containing the name and URN of all primary schools in the specified parliamentary constituency. 

    Scrapes the gov.uk website to obtain and return a pd.DataFrame containing the name and Unique Identification Number (URN) for every primary school in the specified parliamentary constituency.

    Parameters
    ----------
    parliamentary_constituency : str
        The name of the parliamentary constituency whose data is to be obtained. 

    Returns
    -------
    parliamentary_constituency_school_identification_information : pd.DataFrame
        A pd.DataFrame containing the name and URN of every primary school in the specified parliamentary constituency.
    """

    parliamentary_constituency_url = get_single_parliamentary_constituency_url(parliamentary_constituency)

    soup = get_soup(parliamentary_constituency_url)

    rows = soup.select("table#establishment-list-view tbody tr")

    school_names = []
    school_urns = []
    school_types = []

    for row in rows:
        if len(row['class']) > 0:
            continue

        school_urn = row['data-urn']
        school_name = row.select('th a')[0].text.strip()
        school_type = row.select('td[data-title="Type of school"] span.value')[0].text.strip()

        school_urns.append(school_urn)
        school_names.append(school_name)
        school_types.append(school_type)

    parliamentary_constituency_school_identification_information = pd.DataFrame({'school_name': school_names, 'school_urn': school_urns, 'type_of_school': school_types})

    return parliamentary_constituency_school_identification_information

def get_school_identification_information() -> pd.DataFrame:
    """
    Returns a pd.DataFrame containing the name and URN of all UK schools. 

    First checks if there exists a file called
    'uk_school_identification_information.csv'. 
    If such a file exists, it calls the function 
    'read_school_identification_information()'.
    If such a file does not exist, it calls the function
    'scrape_school_identification_information()'

    Returns
    -------
    uk_school_identification_information : pd.DataFrame
        A pd.DataFrame containing the name and URN of every UK school.
    """

    if os.path.isfile('data/uk_school_identification_information.csv'):
        uk_school_identification_information = read_school_identification_information()
    else:
        uk_school_identification_information = scrape_school_identification_information()

    return uk_school_identification_information

def get_soup(url: str) -> BeautifulSoup:
    """
    Returns a BeautifulSoup object representing 
    the parsed webpage that was specified. 

    Parameters
    ----------
    url : str
        The url of the website which is to be parsed. 

    Returns
    ------
    soup : BeautifulSoup
        The BeautifulSoup object representing the webpage to be parsed.
    """

    user_agent = get_user_agent()
    headers = {'User-Agent': user_agent}

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup

def get_single_school_primary_url(school_name: str, school_urn: str) -> str:
    """
    Returns the URL to the school's primary page

    Returns the URL to the Web page containing the school's primary 
    results data. At the time of writing, this data is for pupils who
    completed key stage 2 in the summer of 2023.

    Parameters
    ----------
    school_name : str
        The name of the school whose data is to be obtained. 
    school_urn : str
        The Unique Identification Number (URN) of the school whose data
        is to be obtained.

    Returns
    -------
    school_primary_url : str
        The url to the Web page containing the school's primary results 
        data. 
    """

    formatted_school_name = school_name.replace(' ', '-').replace(',', '%2c').lower()

    school_primary_url = f"https://www.compare-school-performance.service.gov.uk/school/{school_urn}/{formatted_school_name}/primary"

    return school_primary_url

def get_single_school_primary_data(school_name: str, school_urn: str) -> pd.DataFrame:
    """
    Returns the results data for a given school

    Scrapes the gov.uk website to obtain the required primary results data
    for the specified school. Returns a pd.DataFrame containing the 
    primary results data for the school.  At the time of writing, this 
    data is for pupils who completed key stage 2 in the summer of 2023.

    Parameters
    ----------
    school_name : str
        The name of the school whose data is to be obtained. 
    school_urn : str
        The Unique Identification Number (URN) of the school whose data
        is to be obtained.

    Returns
    -------
    school_primary_data : pd.DataFrame
        A pd.DataFrame containing the primary results data for the given 
        school. 
    """

    return None

def get_single_school_absence_and_pupil_url(school_name: str, school_urn: str) -> str:
    """
    Returns the URL to the school's absence page

    Returns the URL to the Web page containing the school's absence and 
    pupil population information. At the time of writing, this data is 
    for the 2021/2022 school year.

    Parameters
    ----------
    school_name : str
        The name of the school whose data is to be obtained. 
    school_urn : str
        The Unique Identification Number (URN) of the school whose data
        is to be obtained.

    Returns
    -------
    school_primary_absence_and_pupil_url : str
        The url to the Web page containing the school's absence and 
        pupil population information.
    """

    formatted_school_name = school_name.replace(' ', '-').replace(',', '%2c').lower()

    school_absence_and_pupil_url = f"https://www.compare-school-performance.service.gov.uk/school/{school_urn}/{formatted_school_name}/absence-and-pupil-population"

    return school_absence_and_pupil_url


def get_single_school_absence_and_pupil_data(school_name: str, school_urn: str) -> pd.DataFrame: 
    """
    Returns the population data for the school

    Scrapes the gov.uk website to obtain the required absence and pupil
    population information for the specified school. Returns a 
    pd.DataFrame containing the school's absence and pupil population 
    information. At the time of writing, this data is for the 
    2021/2022 school year.

    Parameters
    ----------
    school_name : str
        The name of the school whose data is to be obtained. 
    school_urn : str
        The Unique Identification Number (URN) of the school whose data
        is to be obtained.

    Returns
    -------
    school_absence_and_pupil_data : pd.DataFrame
        A pd.DataFrame containing the school's absence and pupil 
        population information.
    """

    return None

def get_single_school_data(school_name: str, school_urn: str) -> pd.DataFrame:
    """
    Returns a pd.DataFrame containing the data required for the school.

    Scrapes the gov.uk website to obtain the required information for the
    school specified. Returns this information as a pd.DataFrame with 
    columns for all the data specified in the documentation for this
    class.

    Parameters
    ----------
    school_name : str
        The name of the school whose data is to be obtained. 
    school_urn : str
        The Unique Identification Number (URN) of the school whose data
        is to be obtained.

    Returns
    -------
    single_school_data : pd.DataFrame
        A pd.DataFrame containing the required data for the school specified. 
    """

    return None

def get_all_school_data() -> pd.DataFrame:
    """
    Returns a pd.DataFrame containing the required data for all UK schools

    Calls the function 'get_single_school_data()' for each school returned
    by 'get_school_identification_information()' concatenating the 
    pd.DataFrame returned to obtain a single pd.DataFrame containing the
    information required for all schools in the UK. This DataFrame
    contains the information described in the documentation for this 
    class.

    Returns
    -------
    all_school_data : pd.DataFrame
        A pd.DataFRame containing the required data for all UK schools.  
    
    """

    return None