import sys

sys.path.append('..')

import pytest 
import shutil
from pathlib import Path

import DataAquisition
from typing import List

EXPECTED_PARLIAMENTARY_CONSTITUENT_LIST = ['Aldershot', 'Aldridge-Brownhills', 'Altrincham and Sale West', 'Ashton-under-Lyne', 'Banbury', 
                                           'Aberdeen North', 'Aberdeen South', 'Angus', 'Ayr, Carrick and Cumnock', 'Argyll and Bute', 
                                           'Belfast East', 'Belfast North', 'Fermanagh and South Tyrone', 'Foyle', 'East Antrim']

class TestDataAcquisition:
    """
    Test class for the DataAquisition.py script

    Rather than test the script on all of the data it will acquire, I will
    use a subset of the data. I have created a sample wikipedia page for
    the parliamentary constituencies in the UK, by modifying the real 
    wikipedia page that I will scrape. This sample page contains only the 
    following 10 parliamentary constituencies for each of England, 
    Scotland and Northern Ireland:

    England:
    - Aldershot
    - Aldridge-Brownhills
    - Altrincham and Sale West
    - Ashton-under-Lyne
    - Banbury

    Scotland: 
    - Aberdeen North
    - Aberdeen South
    - Angus
    - Argyll and Bute
    - Ayr, Carrick and Cumnock

    Nothern Ireland: 
    - Belfast East
    - Belfast North
    - East Antrim
    - Fermanagh and South Tyrone
    - Foyle 
    
    Methods
    -------
    test_read_parliamentary_constituents_correct_return()
        Tests that the list returned by the function 
        'read_parliamentary_constituents()' is correct. 

    test_get_parliamentary_constituencies_file_exists_correct_return()
        Tests that the list returned by the function 
        'get_parliamentary_constituents' is correct when the file 
        'uk_parliamentary_constituencies.txt' exists.

    test_get_parliamentary_constituencies_file_does_not_exist_correct_return()
        Tests that the list returned by the function 
        'get_parliamentary_constituents' is correct when the file 
        'uk_parliamentary_constituencies.txt' does not exist.

    test_get_parliamentary_constituents_file_does_not_exist_creates_correct_file()
        Tests that calling the function 'get_parliamentary_constituents' 
        when the file 'uk_parliamentary_constituencies.txt' does not exist
          creates the correct file: 'uk_parliamentary_constituencies.txt'.

    test_scrape_parliamentary_constituencies_correct_return()
        Tests that the list returned by the function 
        'scrape_parliamentary_constituencies()' is correct.

    """

    @pytest.fixture
    def temp_data_directory(request, tmp_path):
        """
        Creates a temporary 'data' directory to store mock data 
        for unit tests. This directory will be deleted after each 
        unit test. 
        """
        current_directory = Path.cwd()

        data_directory = current_directory / "data"
        data_directory.mkdir()

        yield data_directory

        shutil.rmtree(data_directory)

    def test_read_parliamentary_constituents_correct_return(self):
        """
        Tests that the list returned by the function 
        'read_parliamentary_constituents()' is correct. 

        This list should contain all of the parliamentary constituencies 
        given in the documentation for this test class. 
        """

        # Arrange

        # Act
        parliamentary_constituent_list = DataAquisition.read_parliamentary_constituencies()

        # Assert
        assert parliamentary_constituent_list == EXPECTED_PARLIAMENTARY_CONSTITUENT_LIST, "read_parliamentary_constituents() did not return correct list"

    def test_get_parliamentary_constituencies_file_exists_correct_return(self, temp_data_directory):
        """
        Tests that the list returned by the function 
        'get_parliamentary_constituencies()' is correct when the file 
        'uk_parliamentary_constituencies.txt' exists.

        This list should contain all of the parliamentary constituencies 
        given in the documentation for this test class.
        """
            
        # Arrange
        permanent_mock_data_file = Path.cwd() / "test_data" / "uk_parliamentary_constituents_test.txt"
        temporary_mock_data_file = temp_data_directory / "uk_parliamentary_constituents.txt"
        shutil.copy(permanent_mock_data_file, temporary_mock_data_file)

        # Act
        parliamentary_constituent_list = DataAquisition.get_parliamentary_constituencies()

        # Assert
        assert parliamentary_constituent_list == EXPECTED_PARLIAMENTARY_CONSTITUENT_LIST, "get_parliamentary_constituents() did not return correct list"