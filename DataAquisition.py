from typing import List
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

        First checks if there exists a file called 'uk_school_names.txt'. 
        If such a file exists, it is read and a list of all the school names contained within the file is returned. 
        If such a file does not exist, the .gov website it scraped to obtain a list of the names of all the schools in the UK.

        Returns
        -------
        uk_school_names: List[str]
            A list of the names of all the schools in the UK.
        """