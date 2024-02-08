import sys

sys.path.append('..')

import pytest 
import shutil
from pathlib import Path
import os
import pandas as pd

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

    When testing the functions related to obtaining school-specific 
    information, the mock data will only contain primary schools in
    Aldridge-Brownhills. As a result, the mock data will only contain the 
    following 30 schools:
    - St Anne's Catholic Primary School, Streetly
    - Manor Primary School
    - St Michael's Church of England C Primary School
    - St Mary of the Angels Catholic Primary School
    - Walsall Wood School
    - Ryders Hayes School
    - St Francis Catholic Primary School
    - Whetstone Field Primary School
    - Blackwood School
    - Castlefort Junior Mixed and Infant School
    - Holy Trinity Church of England Primary School
    - St John's Church of England Primary School
    - Watling Street Primary School
    - Cooper and Jordan Church of England Primary School
    - St Bernadette's Catholic Primary School
    - Millfield Primary School
    - Radleys Primary School
    - Lindens Primary School
    - St James Primary School
    - Pelsall Village School
    - Greenfield Primary School
    - Leighswood School
    - Brownhills West Primary School
    - Rushall Primary School
    - Oakwood School
    - Blackwood School
    - Brownhills West Primary School
    - Greenfield Primary School
    - St Bernadette's Catholic Primary School
    - Walsall Wood School

    When testing the functions related to obtaining information for a 
    single school only, the mock data will only contain information
    for 'St Anne's Catholic Primary School, Streetly'.
    
    Methods
    -------
    test_read_parliamentary_constituencies_correct_return()

    test_get_parliamentary_constituencies_file_exists_correct_return()

    test_get_parliamentary_constituencies_file_does_not_exist_correct_return()

    test_get_parliamentary_constituencies_file_does_not_exist_creates_correct_file()

    test_scrape_parliamentary_constituencies_file_does_not_exist_creates_correct_file()

    test_scrape_parliamentary_constituencies_correct_return()

    test_read_school_identification_information_correct_return()

    test_get_school_identification_information_file_exists_correct_return()

    test_get_school_identification_information_file_does_not_exist_correct_return()

    test_get_school_identification_information_file_does_not_exist_creates_correct_file()

    test_scrape_school_identification_information_file_does_not_exist_creates_correct_file()

    test_scrape_school_identification_information_correct_return()

    test_get_soup_correct_return()

    test_get_single_school_primary_url_correct_return()

    TODO: test_get_single_school_primary_data_correct_return()

    TODO: test_get_single_school_absence_and_pupil_url_correct_return()

    TODO: test_get_single_school_absence_and_pupil_data_correct_return()

    TODO: test_get_single_school_data_correct_return()

    TODO: test_get_all_school_data_correct_return()

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

    @pytest.fixture
    def mock_requests_get(monkeypatch):
        """
        Mocks the 'requests.get()' function
        """
        def mock_get(url):
            """
            Returns a mocked response object with HTML content
            """
            class MockResponse:
                def __init__(self, content):
                    self.content = content

                def text(self):
                    return self.content
                
            mock_html_content = "<html><body><p>Mock Content</p></body></html>"
            return MockResponse(mock_html_content)
        
        monkeypatch.__setattr__('requests.get', mock_get)


    def test_read_parliamentary_constituencies_correct_return(self, temp_data_directory):
        """
        Tests that the list returned by the function 
        'read_parliamentary_constituencies()' is correct. 

        This list should contain all of the parliamentary constituencies 
        given in the documentation for this test class. 
        """

        # Arrange
        permanent_mock_data_file = Path.cwd() / "test_data" / "uk_parliamentary_constituencies_test.txt"
        temporary_mock_data_file = temp_data_directory / "uk_parliamentary_constituencies.txt"
        shutil.copy(permanent_mock_data_file, temporary_mock_data_file)

        # Act
        parliamentary_constituent_list = DataAquisition.read_parliamentary_constituencies()

        # Assert
        assert parliamentary_constituent_list == EXPECTED_PARLIAMENTARY_CONSTITUENT_LIST, "read_parliamentary_constituencies() did not return correct list"

    def test_get_parliamentary_constituencies_file_exists_correct_return(self, temp_data_directory):
        """
        Tests that the list returned by the function 
        'get_parliamentary_constituencies()' is correct when the file 
        'uk_parliamentary_constituencies.txt' exists.

        This list should contain all of the parliamentary constituencies 
        given in the documentation for this test class.
        """
            
        # Arrange
        permanent_mock_data_file = Path.cwd() / "test_data" / "uk_parliamentary_constituencies_test.txt"
        temporary_mock_data_file = temp_data_directory / "uk_parliamentary_constituencies.txt"
        shutil.copy(permanent_mock_data_file, temporary_mock_data_file)

        # Act
        parliamentary_constituent_list = DataAquisition.get_parliamentary_constituencies()

        # Assert
        assert parliamentary_constituent_list == EXPECTED_PARLIAMENTARY_CONSTITUENT_LIST, "get_parliamentary_constituencies() did not return correct list"

    def test_get_parliamentary_constituencies_file_does_not_exist_correct_return(self, temp_data_directory):
        """
        Tests that the list returned by the function 
        'get_parliamentary_constituencies()' is correct when the file 
        'uk_parliamentary_constituencies.txt' does not exist.

        This list should contain all of the parliamentary constituencies 
        given in the documentation for this test class.
        """

        # Arrange 

        # Act
        parliamentary_constituent_list = DataAquisition.get_parliamentary_constituencies()

        # Assert
        assert parliamentary_constituent_list == EXPECTED_PARLIAMENTARY_CONSTITUENT_LIST, "get_parliamentary_constituencies() did not return correct list"

    def test_get_parliamentary_constituencies_file_does_not_exist_creates_correct_file(temp_data_directory):
        """
        Tests that calling the function 'get_parliamentary_constituencies' 
        when the file 'uk_parliamentary_constituencies.txt' does not exist
        creates the correct file: 'uk_parliamentary_constituencies.txt'.
        """

        # Arrange

        # Act 
        DataAquisition.get_parliamentary_constituencies()

        # Assert
        assert os.path.exists("data/uk_parliamentary_constituencies.txt") == True, "get_parliamentary_constituencies() did not create the file 'uk_parliamentary_constituencies.txt"
        
    def test_scrape_parliamentary_constituencies_file_does_not_exist_creates_correct_file(self, temp_data_directory):
        """
        Tests that calling the function 'scrape_parliamentary_constituencies' 
        when the file 'uk_parliamentary_constituencies.txt' does not exist
        creates the correct file: 'uk_parliamentary_constituencies.txt'.
        """

        # Arrange

        # Act 
        DataAquisition.scrape_parliamentary_constituencies()

        # Assert
        assert os.path.exists("data/uk_parliamentary_constituencies.txt") == True, "scrape_parliamentary_constituencies() did not create the file 'uk_parliamentary_constituencies.txt"

    def test_scrape_parliamentary_constituencies_correct_return(self, temp_data_directory):
        """
        Tests that the list returned by the function 
        'scrape_parliamentary_constituencies()' is correct.

        This list should contain all of the parliamentary constituencies 
        given in the documentation for this test class.
        """

        # Arrange 

        # Act
        parliamentary_constituent_list = DataAquisition.scrape_parliamentary_constituencies()

        # Assert
        assert parliamentary_constituent_list == EXPECTED_PARLIAMENTARY_CONSTITUENT_LIST, "scrape_parliamentary_constituencies() did not return correct list"

    def test_read_school_identification_information_correct_return(self, temp_data_directory):
        """
        Tests that the pd.DataFrame returned by the function
        'read_school_identification_information()' is correct.

        This pd.DataFrame should contain all of the schools in Aldridge-Brownhills, 
        as described in the documentation for this test class.
        """

        # Arrange
        permanent_mock_data_file = Path.cwd() / "test_data" / "uk_school_identification_information_test.csv"
        temporary_mock_data_file = temp_data_directory / "uk_school_identification_information.csv"
        shutil.copy(permanent_mock_data_file, temporary_mock_data_file)

        uk_school_identification_information_mock_dataframe = pd.read_csv('data/uk_school_identification_information.csv', index_col=0)

        # Act
        school_identification_information_dataframe = DataAquisition.read_school_identification_information()

        # Assert
        pd.testing.assert_frame_equal(school_identification_information_dataframe, uk_school_identification_information_mock_dataframe)

    def test_get_school_identification_information_file_exists_correct_return(self, temp_data_directory):
        """
        Tests that the pd.DataFrame returned by the function
        'get_school_identification_information()' is correct when the 
        file 'uk_school_identification_information.csv' exists.

        This pd.DataFrame should contain all of the schools in Aldridge-Brownhills, 
        as described in the documentation for this test class.
        """

        # Arrange
        permanent_mock_data_file = Path.cwd() / "test_data" / "uk_school_identification_information_test.csv"
        temporary_mock_data_file = temp_data_directory / "uk_school_identification_information.csv"
        shutil.copy(permanent_mock_data_file, temporary_mock_data_file)

        uk_school_identification_information_mock_dataframe = pd.read_csv('data/uk_school_identification_information.csv', index_col=0)

        # Act
        school_identification_information_dataframe = DataAquisition.get_school_identification_information()

        # Assert
        pd.testing.assert_frame_equal(school_identification_information_dataframe, uk_school_identification_information_mock_dataframe)

    def test_get_school_identification_information_file_does_not_exist_correct_return(self, temp_data_directory):
        """
        Tests that the pd.DataFrame returned by the function
        'get_school_identification_information()' is correct when the 
        file 'uk_school_identification_information.csv' does not exist.

        This pd.DataFrame should contain all of the schools in Aldridge-Brownhills, 
        as described in the documentation for this test class.
        """

        # Arrange
        permanent_mock_data_file = Path.cwd() / "test_data" / "uk_school_identification_information_test.csv"
        uk_school_identification_information_mock_dataframe = pd.read_csv(permanent_mock_data_file, index_col=0)

        # Act
        school_identification_information_dataframe = DataAquisition.get_school_identification_information()

        # Assert
        pd.testing.assert_frame_equal(school_identification_information_dataframe, uk_school_identification_information_mock_dataframe)

    def test_get_school_identification_information_file_does_not_exist_creates_correct_file(self, temp_data_directory):
        """
        Tests that calling the function 'get_school_identification_information()'
        when the file 'uk_school_identification_information.csv' does not exist
        creates the correct file: 'uk_school_identification_information.csv'.
        """

        # Arrange

        # Act 
        school_identification_information_dataframe = DataAquisition.get_school_identification_information()

        # Assert
        assert os.path.exists("data/uk_school_identification_information.csv") == True, "get_school_identification_information() did not create the file 'uk_school_identification_information.csv"

    def test_scrape_school_identification_information_file_does_not_exist_creates_correct_file(self, temp_data_directory):
        """
        Tests that calling the function 'scrape_school_identification_information()'
        when the file 'uk_school_identification_information.csv' does not exist
        creates the correct file: 'uk_school_identification_information.csv'.
        """

        # Arrange

        # Act 
        school_identification_information_dataframe = DataAquisition.scrape_school_identification_information()

        # Assert
        assert os.path.exists("data/uk_school_identification_information.csv") == True, "scrape_school_identification_information() did not create the file 'uk_school_identification_information.csv"

    def test_scrape_school_identification_information_correct_return(self, temp_data_directory):
        """
        Tests that the pd.DataFrame returned by the function
        'scrape_school_identification_information()' is correct.

        This pd.DataFrame should contain all of the schools in Aldridge-Brownhills, 
        as described in the documentation for this test class.
        """

        # Arrange
        permanent_mock_data_file = Path.cwd() / "test_data" / "uk_school_identification_information_test.csv"
        uk_school_identification_information_mock_dataframe = pd.read_csv(permanent_mock_data_file, index_col=0)

        # Act
        school_identification_information_dataframe = DataAquisition.scrape_school_identification_information()

        # Assert
        pd.testing.assert_frame_equal(school_identification_information_dataframe, uk_school_identification_information_mock_dataframe)

    def test_get_soup_correct_return(self, mock_requests_get):
        """
        Tests that 'get_soup' returns the correct BeautifulSoup object

        Calls 'get_soup' with a dummy URL to obtain the returned 
        BeautifulSoup object. Verifies that the correct BeautifulSoup 
        object is returned by checking if it contains the expected 
        content. In this case, we will check whether it contains a '<p>' 
        tag with the text 'Mock Content' since this is the HTML content
        returned by the 'mock_requests_get' fixture. 
        """

        # Arrange
        dummy_url = 'http://dummy.com'

        # Act
        soup = DataAquisition.get_soup(dummy_url)

        # Assert
        assert soup.find("p").text == "Mock Content", "get_soup() did not return the correct BeautifulSoup object."

    def test_get_single_school_primary_url_correct_return(self):
        """
        Tests that 'get_single_school_primary_url' returns the corerct url

        Tests the function 'get_single_school_primary_url' for the 
        school 'St Anne's Catholic Primary School, Streetly' which has the
        URN '104241'
        """

        # Arrange

        # Act 
        primary_url = DataAquisition.get_single_school_primary_url("St Anne's Catholic Primary School, Streetly", "104241")

        # Assert
        assert primary_url == "https://www.compare-school-performance.service.gov.uk/school/104241/st-anne's-catholic-primary-school%2c-streetly", "get_single_school_primary_url() did not return the correct URL."

    def test_get_single_school_primary_data_correct_return(self, temp_data_directory):
        """
        Tests 'get_single_school_primary_data' return is correct

        Tests that the function 'get_single_school_primary_data' returns
        the correct pd.DataFrame. This pd.DataFrame should contain the 
        primary results data for the school 'St Anne's Catholic Primary 
        School, Streetly'  which has the URN '104241'.
        """

        # Arrange
        permanent_mock_data_file = Path.cwd() / "test_data" / "get_single_primary_data_test.csv"
        temporary_mock_data_file = temp_data_directory / "get_single_primary_data_test.csv"
        shutil.copy(permanent_mock_data_file, temporary_mock_data_file)

        mock_school_primary_data = pd.read_csv(temporary_mock_data_file)

        # Act
        school_primary_data = DataAquisition.get_single_school_primary_data("St Anne's Catholic Primary School, Streetly", "104241")

        # Assert
        pd.testing.assert_frame_equal(school_primary_data, mock_school_primary_data)