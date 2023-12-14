from typing import List
from bs4 import BeautifulSoup
import requests

class DataAquisition:
    """
    A class used to aquire the data required for my 'Analysis of UK School Performance' project.

    Attributes
    ----------
    user_agent : str
        The user agent to be used when making html requests. 

    Methods
    -------
    get_school_names()
        Returns a list of the names of all the schools in the UK.
    get_school_urns()
        Returns a list of the URN's of all the schools in the UK.
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

    def get_parliamentry_constituencies() -> List[str]:
        """
        Returns a list of all the parliamentary constituencies in the UK. 

        First checks if there exists a file called 'uk_parliamentary_constituencies.csv'
        If such a file exists, it is read and a list of all the UK parliamentary constituencies is returned. 
        If such a file does not exist, wikipedia.org is scraped to obtain and return  a list of all the UK parliamentary constituencies. 

        Returns
        -------
        uk_parliamentry_constituencies() -> List[str]
            A list of all the parliamentary constituencies in the UK.
        """

        # Below the user agent is changed since the wikipedia.org website blocks requests with a user agent of python-requests.
        # headers = {'User-Agent': self.user_agent}

        wikipedia_url = "https://en.wikipedia.org/wiki/Constituencies_of_the_Parliament_of_the_United_Kingdom"

        uk_parliamentry_constituencies = []

        page = requests.get(wikipedia_url)
        soup = BeautifulSoup(page.content, 'html.parser')

