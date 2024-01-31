"""
Scrapes the data required for my Analysis of UK School Performance project

Aquires the data specified by the data_rows parameter for each school in
the UK. Creates the file 'uk_school_data.csv'. Asks the user if the 
program should continue and rewrite the file if the file already exists.
The file 'uk_school_data.csv' contains the columns: 'school_name', 
'school_urn', 'parliamentary_constituency' as well as any columns 
specified by the data_rows parameter.

Parameters
----------
user_agent : str
    The user agent to be used when making html requests.
data_rows : List[str]
    A list of the data rows to be aquired for each school. 

Notes
-----
The user agent in the example below is obtained from 
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent [1].    

Examples
--------
>>> python DataAquisition.py "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"

References
----------
[1] gregbirch, iigmir, mfuji09, darby, Tigit, ExE-Boss, fscholz, 
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
    
    return None

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
    uk_parliamentary_constituencies() : List[str]
        A list of all the parliamentary constituencies in the UK.
    """
    
    return None

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

    return None

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

    return None

def scrape_school_identification_information() -> List[str]:
    """
    Returns a pd.DataFrame containing the name and URN of all UK schools. 

    This function is only called if the file
    'uk_school_identification_information.csv' does not exist. 
    It scrapes the gov.uk website to obtain and return a pd.DataFrame 
    containing the name and Unique Identification Number (URN) for every
    school in the UK.

    Returns
    -------
    uk_school_identification_information : pd.DataFrame
        A pd.DataFrame containing the name and URN of every UK school.
    """

def get_school_identification_information() -> List[str]:
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

    return None

def get_single_school_data(school_name, school_urn, data_rows) -> pd.DataFrame:
    """
    Returns a pd.DataFrame containing the data required for the school.

    Scrapes the gov.uk website to obtain the required information for the
    school specified. Returns this information as a pd.DataFrame with 
    columns for the school's name, Unique Identification Number (URN) and
    parliamentary constituency as well as the required information.

    Parameters
    ----------
    school_name : str
        The name of the school whose data is to be obtained. 
    school_urn : str
        The Unique Identification Number (URN) of the school whose data
        is to be obtained.
    data_rows : List[str]
        A list of the data rows to be aquired for the school.

    Returns
    -------
    single_school_data : pd.DataFrame
        A pd.DataFrame containing the required data for the school specified. 
    """

    return None

def get_all_school_data(data_rows) -> pd.DataFrame:
    """
    Returns a pd.DataFrame containing the required data for all UK schools

    Calls the function 'get_single_school_data()' for each school returned
    by 'get_school_identification_information()' concatenating the 
    pd.DataFrame returned to obtain a single pd.DataFrame containing the
    information required for all schools in the UK. This DataFrame
    contains columns for the school's name, Unique Identification Number 
    (URN) and parliamentary consitituency as well as the required
    information.

    Parameters
    ----------
    data_rows : List[str]
        A list of the data rows to be aquired for the schools.

    Returns
    -------
    all_school_data : pd.DataFrame
        A pd.DataFRame containing the required data for all UK schools.  
    
    """

    return None