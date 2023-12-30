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

# TODO: Write docstring according to https://numpydoc.readthedocs.io/en/latest/format.html
# TODO: convert this file from OOP to functional programming (only include function headers)

class DataAcquisition:
    """
    A class used to aquire the data required for my 'Analysis of UK School Performance' project.

    Attributes
    ----------
    user_agent : str
        The user agent to be used when making html requests. 

    Methods
    -------
    get_school_names() -> List[str]
        Returns a list of the names of all the schools in the UK.
    get_school_urns() -> List[str]
        Returns a list of the URN's of all the schools in the UK.
    get_parliamentary_constituencies() -> List[str]
        Returns a list of all the parliamentary constituencies in the UK. 
    get_school_data(rows: List[str], school_name: str, school_urn: str) -> List[Untion[str, int]]
        Returns a list containing the school name, the school's URN and all of the specified data for that school. 
    get_all_data(rows: List[str]) -> pd.DataFrame
        Returns a Pandas DataFrame containing all of the specified data for all of the schools in the UK. 
    """

    def __init__(self, user_agent):
        self.user_agent = user_agent

    def get_school_names() -> List[str]:
        """
        Returns a list of the names of all the schools in the UK. 

        First checks if there exists a file called 'uk_school_names.csv'. 
        If such a file exists, it is read and a list of all the school names contained within the file is returned. 
        If such a file does not exist, the .gov website it scraped to obtain and return a list of the names of all the schools in the UK.

        Returns
        -------
        uk_school_names: List[str]
            A list of the names of all the schools in the UK.
        """

    def get_parliamentary_constituencies() -> List[str]:
        """
        Returns a list of all the parliamentary constituencies in the UK. 

        First checks if there exists a file called 'uk_parliamentary_constituencies.csv'
        If such a file exists, it is read and a list of all the UK parliamentary constituencies is returned. 
        If such a file does not exist, wikipedia.org is scraped to obtain and return  a list of all the UK parliamentary constituencies. 

        Returns
        -------
        uk_parliamentary_constituencies() -> List[str]
            A list of all the parliamentary constituencies in the UK.
        """

        uk_parliamentary_constituencies_path = "data/uk_parliamentary_constituencies.csv"

        if os.path.isfile(uk_parliamentary_constituencies_path):
            constituencies = list(pd.read_csv(uk_parliamentary_constituencies_path)['constituencies'])
            
            return constituencies

        wikipedia_url = "https://en.wikipedia.org/wiki/Constituencies_of_the_Parliament_of_the_United_Kingdom"

        uk_parliamentary_constituencies = []

        page = requests.get(wikipedia_url)
        soup = BeautifulSoup(page.content, 'html.parser')

        for row_index in range(len(rows)):
            pass

        return(soup)
    

if __name__ == "__main__":
    soup = DataAcquisition.get_parliamentary_constituencies()


