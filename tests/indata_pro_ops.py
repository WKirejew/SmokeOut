import pandas as pd

class InData:
    """
    Class for input data, that allows for conversion into input to tables of DataBase, define the datastructure and operations over those tables
    
    Attributes
    ----------
    json : json.object
        loaded json file with user's inpiut data
    username : str
        name of user to whom the data belongs
    open : list of str
        list of strings, containing [SQL - DateTime2(0)] formatted date of device's openings
    switch : list of str
        list of strings, containing [SQL - DateTime2(0)] formatted date of cigarettes' package switching

    Methods
    -------
    extract()
        Extract the information from User Input File [in JSON format] into approperiate attributes of the chosen instance
    adddate()
        Converts date-time into SQL ready format and append it to an attribute specified by boolean variable att 
    """
    def __init__(self, JSON):
         """
        Parameters
        ----------
        JSON : str to JSON file
            Allow of opening and reading from the JSON file containing user input data
        """
         self.json = pd.read_json(JSON)
         self.username = ""
         self.open = []
         self.switch = []

    def adddate(self, att, date):
         """
        Converts date-time into SQL ready format and append it to an attribute specified by boolean variable att 

        Parameters
        ----------
        att : boolean
            value of 0 - type is "opening"
            value of 1 - type is "switch"
        date : str
            Contains date_time information in a format of the JSON file
        """
        # Reading information from "date" string
         try:
             hour = int(date[0:2])
             hour = '0' + str(hour) if hour < 10 else str(hour)
             minute = int(date[3:5])
             minute = '0' + str(minute) if minute < 10 else str(minute)
             second = int(date[6:8])
             second = '0' + str(second) if second < 10 else str(second)
             day = int(date[9:11])
             day = '0' + str(day) if day < 10 else str(day)
             month = int(date[12:14])
             month = '0' + str(month) if month < 10 else str(month)
             year = int(date[15:])
        # Constructing the string of SQL's DateTime2(0) format
             dateSQL = str(year) + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second
         except:
             print("Error occured: wrong datetime")
             raise SystemExit
        # Appending constructed earlier string into approperiate list
         try:
             if att == 0:
                self.open.append(dateSQL)
             elif att == 1:
                self.switch.append(dateSQL)
         except:
             print("An error occured while writing date of choosen type")
             raise SystemExit  
          
    def extract(self):
         """
        Extract information from JSON: username, dates of device opening and package switching from json into self.open and self.switch.
        Decodes the datetime format of input into datetime format of Data, using adddate() function
        """
        # Retriving username, with error handling implemented
         try:
            for i in self.json["username"]:
                self.username = i
                if i != self.json["username"][1]:
                    print("Error occured - username is not consistent")
                    raise SystemExit
         except NameError:
             print("NameError")
             raise SystemExit
        # Retriving opening and switching information from JSON file, returning error when data type is other than "open" or "switch"
         try:
             for i in self.json['operations']:
                if i["type"] == "open":
                  self.adddate( 0, i["date"])
                elif i["type"] == "switch":
                  self.adddate( 1, i["date"])
         except:
             print("An error has occured during date extraction")
             raise SystemExit