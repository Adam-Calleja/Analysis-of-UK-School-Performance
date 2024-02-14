import sys

sys.path.append('..')

import pytest 
import shutil
from pathlib import Path
import os
import pandas as pd
from io import StringIO

import DataAcquisition
from typing import List

EXPECTED_PARLIAMENTARY_CONSTITUENT_LIST = {'Aldershot', 'Aldridge-Brownhills', 'Altrincham and Sale West', 'Ashton-under-Lyne', 'Banbury', 
                                           'Aberdeen North', 'Aberdeen South', 'Angus', 'Ayr, Carrick and Cumnock', 'Argyll and Bute', 
                                           'Belfast East', 'Belfast North', 'Fermanagh and South Tyrone', 'Foyle', 'East Antrim'}

EXPECTED_SINGLE_SCHOOL_PRIMARY_URL = "https://www.compare-school-performance.service.gov.uk/school/104241/st-anne's-catholic-primary-school%2c-streetly/primary"

EXPECTED_SINGLE_SCHOOL_ABSENCE_AND_PUPIL_URL = "https://www.compare-school-performance.service.gov.uk/school/104241/st-anne's-catholic-primary-school%2c-streetly/absence-and-pupil-population"

EXPECTED_ERROR_MESSAGE = "The file 'user_agent.txt' does not exist. Please create a file 'user_agent.txt' in the 'data' directory and enter your user agent."

class TestDataAcquisition:
    """
    Test class for the DataAcquisition.py script

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
    test_get_user_agent_file_exists_correct_return()

    test_get_user_agent_file_does_not_exist_correct_output()

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

    test_get_single_school_primary_data_correct_return()

    test_get_single_school_absence_and_pupil_url_correct_return()

    test_get_single_school_absence_and_pupil_data_correct_return()

    test_get_single_school_data_correct_return()

    test_get_all_school_data_correct_return()
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
    def temp_data_directory_with_mock_user_agent_file(request, tmp_path):
        """
        Creates a temporary 'data' directory to store mock data 
        for unit tests. This directory will be deleted after each 
        unit test. 

        This fixture also creates a mock user agent file 'user_agent.txt'
        in the 'data' directory. 
        """
        current_directory = Path.cwd()

        data_directory = current_directory / "data"
        data_directory.mkdir()

        permanent_mock_user_agent_file = current_directory / "test_data" / "mock_user_agent.txt"
        temporary_mock_user_agent_file = data_directory / "user_agent.txt"
        shutil.copy(permanent_mock_user_agent_file, temporary_mock_user_agent_file)
        
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

    @pytest.fixture
    def mock_requests_get_parliamentary_constituent_data(monkeypatch):
        """
        Mocks the 'requests.get()' function 

        This fixture will be used in the test cases that test functions
        that request the parliamentary constituent web page. Rather than
        returning the actual wiki page, this fixture will return the 
        mock wiki page 'uk_constituency_wiki_sample.html'.
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
                
            mock_html_file_path = "test_data/uk_constituency_wiki_sample.html"

            with open(mock_html_file_path, 'r', encoding='utf-8') as mock_data_file:
                mock_html_content = mock_data_file.read()

            return MockResponse(mock_html_content)
        
        monkeypatch.__setattr__('requests.get', mock_get)

    def test_get_user_agent_file_exists_correct_return(self, temp_data_directory):
        """
        Tests that the user agent returned 'get_user_agent' is correct

        Tests that the user agent returned by the function 'get_user_agent'
        is correct when the file 'user_agent.txt' exists. 
        """

        # Arrange
        permanent_mock_user_agent_file = Path.cwd() / "test_data" / "mock_user_agent.txt"
        temporary_mock_user_agent_file = temp_data_directory / "user_agent.txt"
        shutil.copy(permanent_mock_user_agent_file, temporary_mock_user_agent_file)

        with open(temporary_mock_user_agent_file, 'r') as file:
            expected_user_agent = file.read()

        # Act
        user_agent = DataAcquisition.get_user_agent()

        # Assert
        assert user_agent == expected_user_agent, "get_user_agent() did not return the correct user agent."

    def test_get_user_agent_file_does_not_exist_correct_output(self, temp_data_directory):
        """
        Tests that 'get_user_agent' outputs the correct error message

        Tests that the function 'get_user_agent' outputs the correct error
        message when the file 'user_agent.txt' does not exist. 
        """

        # Arrange

        # Act
        with pytest.raises(FileNotFoundError) as error:
            user_agent = DataAcquisition.get_user_agent()

        # Assert
        assert str(error.value) == EXPECTED_ERROR_MESSAGE, "get_user_agent() did not output the correct error message."


    def test_read_parliamentary_constituencies_correct_return(self, temp_data_directory):
        """
        Tests that the list returned by the function 
        'read_parliamentary_constituencies()' is correct. 

        This list should contain all of the parliamentary constituencies 
        given in the documentation for this test class. 
        """

        # Arrange
        permanent_mock_data_file = Path.cwd() / "test_data" / "mock_uk_parliamentary_constituencies_test.txt"
        temporary_mock_data_file = temp_data_directory / "uk_parliamentary_constituencies.txt"
        shutil.copy(permanent_mock_data_file, temporary_mock_data_file)

        # Act
        parliamentary_constituent_list = DataAcquisition.read_parliamentary_constituencies()

        # Assert
        assert set(parliamentary_constituent_list) == EXPECTED_PARLIAMENTARY_CONSTITUENT_LIST, "read_parliamentary_constituencies() did not return correct list"

    def test_get_parliamentary_constituencies_file_exists_correct_return(self, temp_data_directory_with_mock_user_agent_file, mock_requests_get_parliamentary_constituent_data):
        """
        Tests that the list returned by the function 
        'get_parliamentary_constituencies()' is correct when the file 
        'uk_parliamentary_constituencies.txt' exists.

        This list should contain all of the parliamentary constituencies 
        given in the documentation for this test class.
        """
            
        # Arrange
        permanent_mock_data_file = Path.cwd() / "test_data" / "mock_uk_parliamentary_constituencies_test.txt"
        temporary_mock_data_file = temp_data_directory_with_mock_user_agent_file / "uk_parliamentary_constituencies.txt"
        shutil.copy(permanent_mock_data_file, temporary_mock_data_file)

        # Act
        parliamentary_constituent_list = DataAcquisition.get_parliamentary_constituencies()

        # Assert
        assert set(parliamentary_constituent_list) == EXPECTED_PARLIAMENTARY_CONSTITUENT_LIST, "get_parliamentary_constituencies() did not return correct list"

    def test_get_parliamentary_constituencies_file_does_not_exist_correct_return(self, temp_data_directory_with_mock_user_agent_file, mock_requests_get_parliamentary_constituent_data):
        """
        Tests that the list returned by the function 
        'get_parliamentary_constituencies()' is correct when the file 
        'uk_parliamentary_constituencies.txt' does not exist.

        This list should contain all of the parliamentary constituencies 
        given in the documentation for this test class.
        """

        # Arrange 

        # Act
        parliamentary_constituent_list = DataAcquisition.get_parliamentary_constituencies()

        # Assert
        assert set(parliamentary_constituent_list) == EXPECTED_PARLIAMENTARY_CONSTITUENT_LIST, "get_parliamentary_constituencies() did not return correct list"

    def test_get_parliamentary_constituencies_file_does_not_exist_creates_correct_file(temp_data_directory_with_mock_user_agent_file, mock_requests_get_parliamentary_constituent_data):
        """
        Tests that calling the function 'get_parliamentary_constituencies' 
        when the file 'uk_parliamentary_constituencies.txt' does not exist
        creates the correct file: 'uk_parliamentary_constituencies.txt'.
        """

        # Arrange

        # Act 
        DataAcquisition.get_parliamentary_constituencies()

        # Assert
        assert os.path.exists("data/uk_parliamentary_constituencies.txt") == True, "get_parliamentary_constituencies() did not create the file 'uk_parliamentary_constituencies.txt"
        
    def test_scrape_parliamentary_constituencies_file_does_not_exist_creates_correct_file(self, temp_data_directory_with_mock_user_agent_file, mock_requests_get_parliamentary_constituent_data):
        """
        Tests that calling the function 'scrape_parliamentary_constituencies' 
        when the file 'uk_parliamentary_constituencies.txt' does not exist
        creates the correct file: 'uk_parliamentary_constituencies.txt'.
        """

        # Arrange

        # Act 
        DataAcquisition.scrape_parliamentary_constituencies()

        # Assert
        assert os.path.exists("data/uk_parliamentary_constituencies.txt") == True, "scrape_parliamentary_constituencies() did not create the file 'uk_parliamentary_constituencies.txt"

    def test_scrape_parliamentary_constituencies_correct_return(self, temp_data_directory_with_mock_user_agent_file, mock_requests_get_parliamentary_constituent_data):
        """
        Tests that the list returned by the function 
        'scrape_parliamentary_constituencies()' is correct.

        This list should contain all of the parliamentary constituencies 
        given in the documentation for this test class.
        """

        # Arrange 

        # Act
        parliamentary_constituent_list = DataAcquisition.scrape_parliamentary_constituencies()

        # Assert
        assert set(parliamentary_constituent_list) == EXPECTED_PARLIAMENTARY_CONSTITUENT_LIST, "scrape_parliamentary_constituencies() did not return correct list"

    def test_read_school_identification_information_correct_return(self, temp_data_directory):
        """
        Tests that the pd.DataFrame returned by the function
        'read_school_identification_information()' is correct.

        This pd.DataFrame should contain all of the schools in Aldridge-Brownhills, 
        as described in the documentation for this test class.
        """

        # Arrange
        permanent_mock_data_file = Path.cwd() / "test_data" / "mock_uk_school_identification_information_test.csv"
        temporary_mock_data_file = temp_data_directory / "uk_school_identification_information.csv"
        shutil.copy(permanent_mock_data_file, temporary_mock_data_file)

        uk_school_identification_information_mock_dataframe = pd.read_csv('data/uk_school_identification_information.csv', index_col=0)

        # Act
        school_identification_information_dataframe = DataAcquisition.read_school_identification_information()

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
        permanent_mock_data_file = Path.cwd() / "test_data" / "mock_uk_school_identification_information_test.csv"
        temporary_mock_data_file = temp_data_directory / "uk_school_identification_information.csv"
        shutil.copy(permanent_mock_data_file, temporary_mock_data_file)

        uk_school_identification_information_mock_dataframe = pd.read_csv('data/uk_school_identification_information.csv', index_col=0)

        # Act
        school_identification_information_dataframe = DataAcquisition.get_school_identification_information()

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
        permanent_mock_data_file = Path.cwd() / "test_data" / "mock_uk_school_identification_information_test.csv"
        uk_school_identification_information_mock_dataframe = pd.read_csv(permanent_mock_data_file, index_col=0)

        # Act
        school_identification_information_dataframe = DataAcquisition.get_school_identification_information()

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
        school_identification_information_dataframe = DataAcquisition.get_school_identification_information()

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
        school_identification_information_dataframe = DataAcquisition.scrape_school_identification_information()

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
        permanent_mock_data_file = Path.cwd() / "test_data" / "mock_uk_school_identification_information_test.csv"
        uk_school_identification_information_mock_dataframe = pd.read_csv(permanent_mock_data_file, index_col=0)

        # Act
        school_identification_information_dataframe = DataAcquisition.scrape_school_identification_information()

        # Assert
        pd.testing.assert_frame_equal(school_identification_information_dataframe, uk_school_identification_information_mock_dataframe)

    def test_get_soup_correct_return(self, temp_data_directory_with_mock_user_agent_file, mock_requests_get):
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
        soup = DataAcquisition.get_soup(dummy_url)

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
        primary_url = DataAcquisition.get_single_school_primary_url("St Anne's Catholic Primary School, Streetly", "104241")

        # Assert
        assert primary_url == EXPECTED_SINGLE_SCHOOL_PRIMARY_URL, "get_single_school_primary_url() did not return the correct URL."

    def test_get_single_school_primary_data_correct_return(self, temp_data_directory):
        """
        Tests 'get_single_school_primary_data' return is correct

        Tests that the function 'get_single_school_primary_data' returns
        the correct pd.DataFrame. This pd.DataFrame should contain the 
        primary results data for the school 'St Anne's Catholic Primary 
        School, Streetly'  which has the URN '104241'.
        """

        # Arrange
        permanent_mock_data_file = Path.cwd() / "test_data" / "mock_get_single_primary_data_test.csv"
        temporary_mock_data_file = temp_data_directory / "get_single_primary_data_test.csv"
        shutil.copy(permanent_mock_data_file, temporary_mock_data_file)

        mock_school_primary_data = pd.read_csv(temporary_mock_data_file)

        # Act
        school_primary_data = DataAcquisition.get_single_school_primary_data("St Anne's Catholic Primary School, Streetly", "104241")

        # Assert
        pd.testing.assert_frame_equal(school_primary_data, mock_school_primary_data)

    def test_get_single_school_absence_and_pupil_url_correct_return(self):
        """
        Tests 'get_single_school_absence_and_pupil_url' return is correct

        Tests the function 'get_single_school_absence_and_pupil_url' for 
        the school 'St Anne's Catholic Primary School, Streetly' which has
        the URN '104241'
        """

        # Arrange

        # Act
        absence_and_pupil_url = DataAcquisition.get_single_school_absence_and_pupil_url("St Anne's Catholic Primary School, Streetly", "104241")

        # Assert
        assert absence_and_pupil_url == EXPECTED_SINGLE_SCHOOL_ABSENCE_AND_PUPIL_URL, "get_single_school_absence_and_pupil_url() did not return the correct URL."

    def test_get_single_school_absence_and_pupil_data_correct_return(self, temp_data_directory):
        """
        Tests 'get_single_school_absence_and_pupil_data' return is correct

        Tests that the function 'get_single_school_absence_and_pupil_data' 
        returns the correct pd.DataFrame. This pd.DataFrame should contain 
        the absence and pupil data for the school 'St Anne's Catholic 
        Primary School, Streetly'  which has the URN '104241'.
        """

        # Arrange
        permanent_mock_data_file = Path.cwd() / "test_data" / "mock_get_single_school_absence_and_pupil_data_test.csv"
        temporary_mock_data_file = temp_data_directory / "get_single_school_absence_and_pupil_data_test.csv"
        shutil.copy(permanent_mock_data_file, temporary_mock_data_file)

        mock_school_absence_and_pupil_data = pd.read_csv(temporary_mock_data_file)

        # Act
        school_absence_and_pupil_data = DataAcquisition.get_single_school_absence_and_pupil_data("St Anne's Catholic Primary School, Streetly", "104241")

        # Assert
        pd.testing.assert_frame_equal(school_absence_and_pupil_data, mock_school_absence_and_pupil_data)

    def test_get_single_school_data_correct_return(self, temp_data_directory):
        """
        Tests 'get_single_school_data' returns the correct pd.DataFrame

        Tests that the function 'get_single_school_data' 
        returns the correct pd.DataFrame. This pd.DataFrame should contain 
        the absence and pupil data as well as the primary results data for
        the school 'St Anne's Catholic Primary School, Streetly'  which 
        has the URN '104241'.
        """

        # Arrange
        permanent_mock_data_file = Path.cwd() / "test_data" / "mock_get_single_school_data_test.csv"
        temporary_mock_data_file = temp_data_directory / "mock_get_single_school_data_test.csv"
        shutil.copy(permanent_mock_data_file, temporary_mock_data_file)

        mock_school_data = pd.read_csv(temporary_mock_data_file)

        # Act
        school_data = DataAcquisition.get_single_school_data("St Anne's Catholic Primary School, Streetly", "104241")

        # Assert
        pd.testing.assert_frame_equal(school_data, mock_school_data)

    def test_get_all_school_data_correct_return(self, temp_data_directory):
        """
        Tests 'get_all_school_data' returns the correct pd.DataFrame

        Tests that the function 'get_all_school_data' returns the
        correct pd.DataFrame when the file 'uk_school_identification...
        ..._information.csv' contains the following 8 schools only: 
        - St Anne's Catholic Primary School, Streetly
        - St Francis Catholic Primary School
        - Holy Trinity Church of England Primary School
        - St Bernadette's Catholic Primary School
        - Millfield Primary School
        - St James Primary School
        - Leighswood School
        - |Greenfield Primary School

        The pd.DataFrame returned should be the same as the pd.DataFrame
        stored in the file 'mock_get_all_school_data_return.csv'. 
        """

        # Arrange
        permanent_mock_return_data_file = Path.cwd() / "test_data" / "mock_get_all_school_data_return.csv"
        temporary_mock_return_data_file = temp_data_directory / "mock_get_all_school_data_return.csv"
        shutil.copy(permanent_mock_return_data_file, temporary_mock_return_data_file)

        permanent_mock_school_information_data_file = Path.cwd() / "test_data" / "mock_school_identification_information_test_get_all_school_data.csv"
        temporary_mock_school_information_data_file = temp_data_directory / "uk_school_identification_information.csv"
        shutil.copy(permanent_mock_school_information_data_file, temporary_mock_school_information_data_file)

        mock_expected_return_data = pd.read_csv(temporary_mock_return_data_file)

        # Act
        all_school_data = DataAcquisition.get_all_school_data()

        # Assert
        pd.testing.assert_frame_equal(all_school_data, mock_expected_return_data)