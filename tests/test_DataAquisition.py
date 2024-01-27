import pytest 
import DataAquisition
from typing import List

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
    - Amber Valley
    - Arundel and South Downs 
    - Ashfield
    - Ashford
    - Ashton-under-Lyne
    - Aylesbury
    - Banbury

    Scotland: 
    - Aberdeen North
    - Aberdeen South
    - Airdrie and Shotts
    - Angus
    - Argyll and Bute
    - Ayr, Carrick and Cumnock
    - Banff and Buchan
    - Berwickshire, Roxburgh and Selkirk
    - Caithness, Sutherland and Easter Ross
    - Central Ayrshire

    Nothern Ireland: 
    - Belfast East
    - Belfast North
    - Belfast South 
    - Belfast West
    - East Antrim
    - East Londonderry
    - Fermanagh and South Tyrone
    - Foyle 
    - Langan Valley
    - Mid Ulster
    
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

    test_get_parliamentary_constituents_file_does_not_exist_creates_nonempty_file()
        Tests that calling the function 'get_parliamentary_constituents'
        when the file 'uk_parliamentary_constituencies.txt' does not 
        exist creates a non-empty file: 
        'uk_parliamentary_constituencies.txt'.

    test_scrape_parliamentary_constituencies_correct_return()
        Tests that the list returned by the function 
        'scrape_parliamentary_constituencies()' is correct.

    """

   
        
    