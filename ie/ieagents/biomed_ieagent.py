"""
Implementation of the IEAgent interface for the schoool of biomedical 
engineering science and health systems, located here:
http://drexel.edu/biomed/faculty/core/ and 
http://drexel.edu/biomed/faculty/affiliated/

The order of information:
name
education
title
department
room
phone
email
areas of expertise

"""

__all__ = ['BiomedIEAgent']
__version__ = '0.2'
__author__ = 'Tom Amon'

import requests
from bs4 import BeautifulSoup
import abc
from .ieagent import IEAgent, writeHTMLFile
import ttl
   

class BiomedIEAgent(IEAgent):

    _link1="http://drexel.edu/biomed/faculty/core/"
    _link2="http://drexel.edu/biomed/faculty/affiliated/"
    ttl_filename = "ttl/biomed.ttl"

    def write_ttl(self):
        ttl_file = ttl.TtlFile(self.ttl_filename)

        webpage1 = requests.get(self._link1)
        try:
            webpage1.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup1 = BeautifulSoup(webpage1.text, "html.parser")
        
        webpage2 = requests.get(self._link2)
        try:
            webpage2.raise_for_status()
        except Exception as exc:
            print('There was a problem: %s' % (exc))
        soup2 = BeautifulSoup(webpage2.text, "html.parser")

        self._refreshFromSoup(soup1, ttl_file)
        self._refreshFromSoup(soup2, ttl_file)
    
        ttl_file.close()
        return ttl_file

    def _refreshFromSoup(self, soup, ttl_file):
        elems = soup.findAll('tr', {"class" : "FacultyTableRow"})
        for i in range(0, len(elems)):
            e = elems[i]
            all_text = e.findAll(text=True)
            
            data = list(filter(lambda a: a != "\n", all_text))

            nameEdu = data[0].split(',', 1)

            prof = ttl.TtlFileEntry()

            prof.name = nameEdu[0]
            prof.property = "faculty"
            if len(nameEdu) > 1:
                prof.education = nameEdu[1]
            prof.title = data[1]
            prof.room = data[2]
            if "@" in data[3]:
                prof.email = data[3]
                prof.interests = data[4]
            else:
                prof.interests = data[3]

            prof.write_to(ttl_file)
