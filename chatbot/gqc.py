from postag import NLTKPOSTag
from genericquestion import GenericQuestion
from errors import BadQuestionException

class GenericQuestionConstruction():
    def __init__(self, question, db):
        self.question = question
        self.db = db
        self.tag_list = []

    def getgenericquestion(self):
        postag_class = NLTKPOSTag()
        self.tag_list = postag_class.getpostag(self.question)
        rep_list = self.findrepresentation()

        if len(rep_list) == 0:
            raise BadQuestionException()
        #replace nouns with their genericRepresentations
        paddedquestion = self.question
        for key, value in rep_list.items():
            paddedquestion = paddedquestion.replace(value, '(' + key + ')')
        #create returned object which contains a string and a dictionary 
        #whose keys are nouns in original question and values are generic 
        #representations of the keys
        returnedobject = GenericQuestion()
        returnedobject.paddedquestion = paddedquestion
        returnedobject.rep_list = rep_list
        return returnedobject

    def findrepresentation(self):
        #retrieve all nouns
        noun_list = []
        count = 0
        while count < len(self.tag_list):
            tup = self.tag_list[count]
            if tup[1][0].lower() == 'n':
                noun = tup[0]
                if tup[1][:3].lower() == 'nnp':
                    while self.tag_list[count + 1][1][:3].lower() == 'nnp':
                        count = count + 1
                        noun = noun + ' ' + self.tag_list[count][0]
                noun_list.append(noun)
            count = count + 1
        rep_list = {}
        for noun in noun_list:
            rep = ""
            #get a dictionary from from database whose keys are 
            #'property' and values are generic representation
            query_string = """
            prefix cb: <http://drexelchatbot.com/rdf/>

                        SELECT ?property
            WHERE
            {
                ?s cb:name \"%s\" .
                ?s cb:property ?property .
            }
            """ % noun

            rep = self.db.query(query_string)

            #for testing purpose
            #rep = "**test**"

            #store tuples
            if rep:
                rep_list[rep['property']] = noun
        return rep_list
