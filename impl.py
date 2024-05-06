import os
import pandas as pd

"""
GENERAL ROADMAP (for dummies):
 you can have 2 data formats to be uploaded: JSON (Process data) and CSV (Meta data)

PROCESS DATA:
    for JSON upload:
        read JSON file and transform data for relational database model and then upload to SQL Lite database server, make sure it is in the format of the UML schema for Activity and Aquisition

    for JSON query:
        have pre defined SQL queries that retrieve the data according to the datastructure (see the UML schema)

META DATA:
    for CSV upload:
        read CSV file and transform data for graph database (RDF data) and then upload to blazegraph database, make sure it is in the format of the UML schema for CulturalHeritageObject, Person, Identiable Entity
    for CSV query:
        have pre defined SPARQL queries that retrieve the data according to the datastructure (see the UML schema)
"""


# this class can set and get the path or URL of the database (initially set as an empty string)
class Handler:
    def __init__(self):
        self.dbPathOrUrl = ""

    def setDbPathOrUrl(self, value: str):
        self.dbPathOrUrl = value
        return

    def getDbPathOrUrl(self) -> str:
        if self.dbPathOrUrl == "":
            raise Exception(
                "No database path or url was given, please use setDbPathOrUrl() first."
            )

        return self.dbPathOrUrl


######### UPLOAD HANDLING ###############


# this class will handle uploading data to the BlazeGraph or SQL Lite databases
class UploadHandler:
    def __init__(self):
        self.file_path = None

    # takes in file path and uploads data to database.
    def pushDataToDb(self, file_path: str):
        self.file_path = file_path
        # split filepath for file extension
        _, extension = os.path.splitext(file_path)

        # TODO: check if file exists otherwise throw exception

        if extension == ".json":
            # TODO: process json data for SQL database -> upload data to SQL Lite data base
            process_data_upload = ProcessDataUploadHandler()
            process_data_upload.something(file_path)

        if extension == ".csv":
            # TODO: process csv data & turn into RDF -> upload RDF data to blazegraph store
            meta_data_upload = MetadataUploadHandler()
            meta_data_upload.something(file_path)

        else:
            raise Exception("Only .json or .csv files can be uploaded!")

        print("Finished uploading data! ✅")
        return


"""
This class will handle JSON files as input and stores the data in a SQLite relational database
TODO: read the data, transform the data for SQL Lite database according to UML schema, and then upload the data
"""


class ProcessDataUploadHandler(Handler, UploadHandler):
    def __init__(self):
        super()


"""
This class will handle CSV files as input and stores the data in a Blazegraph graph database
TODO: read the data, transform the data for Blazegraph database according to UML schema, and then upload the data
"""


class MetadataUploadHandler(Handler, UploadHandler):
    def __init__(self):
        super()

    def csv_to_rdf(self):
        # Read the CSV file into a DataFrame
        # cols in csv: Id,Type,Title,Date,Author,Owner,Place
        df = pd.read_csv(self.file_path)
        # Loop over the rows per column
        for column_name, column_values in df.items():
            print(f"Column: {column_name}")
            for index, value in column_values.items():
                if column_name == "Id":
                    triple = f"https://www.katya.com/id/{value}"

                if column_name == "Type":
                    triple = f"https://www.katya.com/id/{value}"

                print(f"Row {index}: {value}")
            print()


# p = ProcessDataUploadHandler()
# p.setDbPathOrUrl('xxx')
# p.getDbPathOrUrl()
# p.pushDataToDb('something.json')

# m = MetadataUploadHandler()
# m.setDbPathOrUrl('xxx')
# m.getDbPathOrUrl()
# m.pushDataToDb('something.json')

########## QUERY HANDLING ###############


class QueryHandler:
    def __init__(self):
        self.query = ""

    # returns a data frame with all the identifiable entities (i.e. cultural heritage objects and people) matching the input identifier (i.e. maximum one entity if there exists one with the input id).
    # EASY EXPLANATION:
    # given an id, it should get the cultural heritage objects and people with that ID
    # should be a SPARQL query that retrieves these according to a given ID
    def getById(self, id):
        rq = f"prefix ex:https://example.com/{id}"

        # TODO: use query on blazGraph database to get the elements and return these

        return


# CSV data aka BlazeGraph SPARQL data
class MetadataQueryHandler(QueryHandler, MetadataUploadHandler):
    def __init__(self, value):
        super()
        self.value = value

    # it returns a data frame containing all the people included in the database.
    def getAllPeople(self):
        return self.value

    # it returns a data frame with all the cultural heritage objects described in it.
    def getAllCulturalHeritageObjects(self, new_value):
        self.value = new_value

    # it returns a data frame with all the authors of the cultural heritage objects identified by the input id.
    def getAuthorsOfCulturalHeritageObject(self, new_value):
        self.value = new_value

    # it returns a data frame with all the cultural heritage objects authored by the person identified by the input id.
    def getCulturalHeritageObjectsAuthoredBy(self, new_value):
        self.value = new_value


# JSON data aka SQL data
class ProcessDataQueryHandler(QueryHandler, ProcessDataUploadHandler):
    def __init__(self, value):
        super()
        self.value = value

    # it returns a data frame with all the activities included in the database.
    def getAllActivities(self):
        return self.value

    # it returns a data frame with all the activities that have, as responsible institution, any that matches (even partially) with the input string.
    def getActivitiesByResponsibleInstitution(self, new_value):
        self.value = new_value

    # it returns a data frame with all the activities that have, as responsible person, any that matches (even partially) with the input string.
    def getActivitiesByResponsiblePerson(self, new_value):
        self.value = new_value

    # it returns a data frame with all the activities that have, as a tool used, any that matches (even partially) with the input string.
    def getActivitiesUsingTool(self, new_value):
        self.value = new_value

    # it returns a data frame with all the activities that started either exactly on or after the date specified as input.
    def getActivitiesStartedAfter(self, new_value):
        self.value = new_value

    # it returns a data frame with all the activities that ended either exactly on or before the date specified as input.
    def getActivitiesEndedBefore(self, new_value):
        self.value = new_value

    # it returns a data frame with all the acquisitions that have, as a technique used, any that matches (even partially) with the input string.
    def getAcquisitionsByTechnique(self, new_value):
        self.value = new_value


########### MASHUP DATA ############
class BasicMashup:
    def __init__(self, metadataQuery, processQuery):
        # the variable containing the list of MetadataQueryHandler objects to involve when one of the get methods below (needing metadata) is executed. In practice, every time a get method is executed, the method will call the related method on all the MetadataQueryHandler objects included in the variable metadataQuery, before combining the results with those of other QueryHandler(s) and returning the requested object.
        self.metadataQuery = ""
        # the variable containing the list of ProcessorDataQueryHandler objects to involve when one of the get methods below (needing acquisition and digitisation information) is executed. In practice, every time a get method is executed, the method will call the related method on all the ProcessorDataQueryHandler objects included in the variable processQuery, before combining the results with those of other QueryHandler(s) and returning the requested object.
        self.processQuery = ""

    # it cleans the list `processQuery` from all the `ProcessorDataQueryHandler` objects it includes.
    def cleanMetadataHandlers(self):
        return self.value

    # it appends the input `MetadataQueryHandler` object to the list `metadataQuery`.
    def cleanProcessHandlers(self, new_value):
        self.value = new_value

    # it appends the input `ProcessorDataQueryHandler` object to the list `processQuery`.
    def addMetadataHandler(self, new_value):
        self.value = new_value

    # it returns an object having class `IdentifiableEntity` identifying the entity available in the databases accessible via the query handlers matching the input identifier (i.e. maximum one entity). In case no entity is identified by the input identifier, `None` must be returned. The object returned must belong to the appropriate class – e.g. if the `IdentifiableEntity` to return is actually a person, an instance of the class `Person` (being it a subclass of `IdentifiableEntity`) must be returned.
    def addProcessHandler(self, new_value):
        self.value = new_value

    # it returns a list of objects having class `Person` containing all the people included in the database accessible via the query handlers.
    def getEntityById(self, new_value):
        self.value = new_value

    # it returns a list of objects having class `CulturalHeritageObject` containing all the people included in the database accessible via the query handlers. The objects included in the list must belong to the appropriate class – e.g. if the `CulturalHeritageObject` to return is actually a map, an instance of the class `Map` (being it a subclass of `CulturalHeritageObject`) must be returned.
    def getAllPeople(self, new_value):
        self.value = new_value

    # it returns a list of objects having class `Person` with all the authors of the cultural heritage objects identified by the input id.
    def getAllCulturalHeritageObjects(self, new_value):
        self.value = new_value

    # it returns a list of objects having class `CulturalHeritageObjects` with all the cultural heritage objects authored by the person identified by the input id. The objects included in the list must belong to the appropriate class – e.g. if the `CulturalHeritageObject` to return is actually a map, an instance of the class `Map` (being it a subclass of `CulturalHeritageObject`) must be returned.
    def getAuthorsOfCulturalHeritageObject(self, new_value):
        self.value = new_value

    # it returns a list of objects having class `Activity` with all the activities included in the database. The objects included in the list must belong to the appropriate class – e.g. if the `Activity` to return is actually an optimising activity, an instance of the class `Optimising` (being it a subclass of `Activity`) must be returned.
    def getCulturalHeritageObjectsAuthoredBy(self, new_value):
        self.value = new_value

    # it returns a list of objects having class `Activity` with all the activities that have, as responsible institution, any that matches (even partially) with the input string. The objects included in the list must belong to the appropriate class – e.g. if the `Activity` to return is actually an optimising activity, an instance of the class `Optimising` (being it a subclass of `Activity`) must be returned.
    def getAllActivities(self, new_value):
        self.value = new_value

    # it returns a list of objects having class `Activity` with all the activities that have, as responsible person, any that matches (even partially) with the input string. The objects included in the list must belong to the appropriate class – e.g. if the `Activity` to return is actually an optimising activity, an instance of the class `Optimising` (being it a subclass of `Activity`) must be returned.
    def getActivitiesByResponsibleInstitution(self, new_value):
        self.value = new_value

    # it returns a list of objects having class `Activity` with all the activities that have, as a tool used, any that matches (even partially) with the input string. The objects included in the list must belong to the appropriate class – e.g. if the `Activity` to return is actually an optimising activity, an instance of the class `Optimising` (being it a subclass of `Activity`) must be returned.
    def getActivitiesByResponsiblePerson(self, new_value):
        self.value = new_value

    # it returns a list of objects having class `Activity` with all the activities that started either exactly on or after the date specified as input. The objects included in the list must belong to the appropriate class – e.g. if the `Activity` to return is actually an optimising activity, an instance of the class `Optimising` (being it a subclass of `Activity`) must be returned.
    def getActivitiesUsingTool(self, new_value):
        self.value = new_value

    # it returns a list of objects having class `Activity` with all the activities that ended either exactly on or before the date specified as input. The objects included in the list must belong to the appropriate class – e.g. if the `Activity` to return is actually an optimising activity, an instance of the class `Optimising` (being it a subclass of `Activity`) must be returned.
    def getActivitiesStartedAfter(self, new_value):
        self.value = new_value

    # it returns a list of objects having class `Acquisition` with all the acquisitions that have, as a technique used, any that matches (even partially) with the input string.
    def getActivitiesEndedBefore(self, new_value):
        self.value = new_value

    # it cleans the list `processQuery` from all the `ProcessorDataQueryHandler` objects it includes.
    def getAcquisitionsByTechnique(self, new_value):
        self.value = new_value


class AdvancedMashup:
    def __init__(self, value):
        self.value = value

    # it returns a list of objects having class `Activity` referring to the cultural heritage objects authored by the person specified by the input identifier. The objects included in the list must belong to the appropriate class – e.g. if the `Activity` to return is actually an optimising activity, an instance of the class `Optimising` (being it a subclass of `Activity`) must be returned.
    def getActivitiesOnObjectsAuthoredBy(self):
        return self.value

    # it returns a list of objects having class `CulturalHeritageObject` with all the cultural heritage objects involved in any activity handled by the responsible person that matches (even partially) with the input string. The objects included in the list must belong to the appropriate class – e.g. if the `CulturalHeritageObject` to return is actually a map, an instance of the class `Map` (being it a subclass of `CulturalHeritageObject`) must be returned.
    def getObjectsHandledByResponsiblePerson(self, new_value):
        self.value = new_value

    # it returns a list of objects having class `CulturalHeritageObject` with all the cultural heritage objects involved in any activity handled by the responsible institution that matches (even partially) with the input string. The objects included in the list must belong to the appropriate class – e.g. if the `CulturalHeritageObject` to return is actually a map, an instance of the class `Map` (being it a subclass of `CulturalHeritageObject`) must be returned.
    def getObjectsHandledByResponsibleInstitution(self):
        return self.value

    # it returns a list of objects having class `Person` of the authors of the cultural heritage objects that have been fully acquired in the time window provided as input.
    def getAuthorsOfObjectsAcquiredInTimeFrame(self):
        return self.value
