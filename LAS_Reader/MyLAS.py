import numpy as np

class Header:
    def __init__(self, string=None):
        """
        Stores LAS Header Lines.\n
        
        Parameters
        ----------
        string = String to convert to Header.\n  
               = None to create empty Header.\n
        
        Attributes
        ----------
        Mnemonic = Header Mnemonic.\n
        Unit =  Header Unit.\n
        Data = Header Data.\n
        Description = Header Description.\n
        """
        self.__string = string
        self.Mnemonic = ""
        self.Unit = ""
        self.Data = ""
        self.Description = ""

        #if string is provided to extract header
        if(self.__string != None):
            self.__read()
        else:
            pass

    def __str__(self):
        return "Mnemonic = " + self.Mnemonic + " \nUnit = " + self.Unit + \
                " \nData = " + str(self.Data) + " \nDesription = " + self.Description

    def __read(self):
        """
        Read LAS Header from the string according to LAS specifications.
        """
        point = space = colon = False
        for char in self.__string:
            if (not point):
                if(char == '.'):
                    point = True
                    continue
                self.Mnemonic += char

            elif(not space):
                if(char == ' '):
                    space = True
                    continue
                self.Unit += char
            elif(not colon):
                if(char == ':'):
                    colon = True
                    continue
                self.Data += char
            else:
                self.Description += char
        self.Mnemonic = self.Mnemonic.rstrip().lstrip()
        self.Unit = self.Unit.rstrip().lstrip()
        self.Data = self.Data.rstrip().lstrip()
        self.Description = self.Description.rstrip().lstrip()
        if self.Unit == "":
            self.Unit = "none"
        else:
            pass

class WellHeader:
    def __init__(self):
        """
        Attributes
        ----------
        STRT = Header for the first depth (or time, or index number) in the file.\n
        STOP = Header for the last depth (or time, or index number) in the file.\n
        STEP = Header for the the actual difference between every successive depth \n(or time, or index number) in the file.\n
        NULL = Header for the Null values.\n
        COMP = Header for Company name.\n
        WELL = Header for the Well name.\n
        FLD = Header for the Field name.\n
        LOC = Header for the Well location.\n
        PROV = Header for the Province.\n
        CNTY = Header for the County.\n
        STAT = Header for the State.\n
        CTRY = Header for the Country.\n
        SRVC = Header for the Logging/Service company.\n
        DATE = Header for the Date logged.\n
        UWI = Header for Unique Well Identifier.\n
        API = Header for the API Number.\n
        LIC = Header for the Regulatory Licence Number.\n
        """
        self.STRT = None
        self.STOP = None
        self.STEP = None
        self.NULL = None 
        self.COMP = None
        self.WELL = None
        self.FLD = None
        self.LOC = None
        self.PROV = None
        self.CNTY = None
        self.STAT = None
        self.CTRY = None
        self.SRVC = None
        self.DATE = None
        self.UWI = None
        self.API = None
        self.LIC = None


class Log:
    def __init__(self):
        """
        Stores Log data inculding Headers and Sample Values.\n

        Attributes
        ----------
        Header = Header object containing Curve Information for a Log.\n
        Data = Numpy array containing curve values.\n
        Name = Name of the Log as described in Well Curve Info. 
        """
        self.Name = None
        self.Header = None
        self.Data = None

    def __str__(self):
        print(self.Name)
        print(self.Header)
        for i in self.Data:
            print(i)
        return "End of Log"

    def __len__(self):
        return len(self.Data)

    def __getitem__(self, index):
        return self.Data[index]


class Well:
    def __init__(self, FileName=None):
        """
        Creates a Well object from given file name.\n

        Parameters
        ----------
        FileName = Name of the LAS file.\n

        Attributes
        ----------
        FileName = LAS Filename.\n 
        LasVersion = LAS version of the file.\n
        Wrap = Wrap info of the LAS file.\n
        WellInfo = `Well.WellHeader` object containing "~W" Block of LAS file.\n 
        CurveInfo = List containing "~C" Block of LAS file.\n 
        ParameterInfo = List containing "~P" Block of LAS file.\n 
        OtherInfo = List containing "~O" Block of LAS file.\n 
        Logs = List Containing `well.Log` objects for every Log in "~A" Block of LAS file.\n
        API = Well API. \n
        UWI = Unique Well Identity.\n
        """
        self.FileName = FileName
        self.WellInfo = WellHeader()
        self.CurveInfo = []
        self.ParameterInfo = []
        self.OtherInfo = []
        self.Logs = []
        self.API = None
        self.UWI = None
        self.LASVersion = None
        self.Wrap = None

        if(FileName != None):
            self.__ReadVersion()
            self.__ReadWellInfo()
            self.__ReadCurveInfo()
            self.__ReadParameterInfo()
            self.__ReadOtherInfo()
        else:
            pass

    def __ReadVersion(self):
        file = open(self.FileName, 'r')
        for i,line in enumerate(file):
            h = Header(line)
            if i==1:
                self.LASVersion = float(h.Data)
            elif i==2:
                if h.Data =="Yes":
                    self.Wrap = True
                else:
                    pass
            elif i>2:
                break
        file.close()


    def __ReadWellInfo(self):
        file = open(self.FileName, 'r')
        flag = False
        for line in file:
            if line[0:2]=="~W":
                flag = True
                continue
            if flag:
                h = Header(line)
                if line[0] == '#':
                    continue
                elif h.Mnemonic == "STRT":
                    h.Data = float(h.Data)
                    self.WellInfo.STRT = h
                elif h.Mnemonic == "STOP":
                    h.Data = float(h.Data)
                    self.WellInfo.STOP == h
                elif h.Mnemonic == "STEP":
                    h.Data = float(h.Data)
                    self.WellInfo.STEP = h
                elif h.Mnemonic == "NULL":
                    h.Data = float(h.Data)
                    self.WellInfo.NULL = h
                elif h.Mnemonic == "COMP":
                    self.WellInfo.COMP = h
                elif h.Mnemonic == "WELL":
                    self.WellInfo.WELL = h
                elif h.Mnemonic == "FLD":
                    self.WellInfo.LOC = h
                elif h.Mnemonic == "PROV":
                    self.WellInfo.PROV = h
                elif h.Mnemonic == "CNTY":
                    self.WellInfo.CNTY = h
                elif h.Mnemonic == "STAT":
                    self.WellInfo.STAT = h
                elif h.Mnemonic == "CTRY":
                    self.WellInfo.CTRY = h
                elif h.Mnemonic == "SRVC":
                    self.WellInfo.SRVC = h
                elif h.Mnemonic == "DATE":
                    self.WellInfo.DATE = h
                elif h.Mnemonic == "UWI":
                    self.WellInfo.UWI = h
                    self.UWI = h.Data
                elif h.Mnemonic == "API":
                    self.WellInfo.API = h
                    self.API = h.Data
                elif h.Mnemonic == "LIC":
                    self.WellInfo.LIC = h
                elif line[0]=="~":
                    flag = False
                    break
            else:
                continue
    def __ReadCurveInfo(self):
        file = open(self.FileName, 'r')
        flag = False
        for line in file:
            if line[0:2]=="~C":
                flag = True
                continue        
            if flag:
                h = Header(line)
                if line[0] == '#':
                    continue
                elif line[0]=="~":
                    flag = False
                    break
                else:
                    self.CurveInfo.append(h)
            else:
                continue
    def __ReadParameterInfo(self):
        file = open(self.FileName, 'r')
        flag = False
        for line in file:
            if line[0:2]=="~P":
                flag = True
                continue        
            if flag:
                h = Header(line)
                if line[0] == '#':
                    continue
                elif line[0]=="~":
                    flag = False
                    break
                else:
                    self.ParameterInfo.append(h)
            else:
                continue
    
    def __ReadOtherInfo(self):
        file = open(self.FileName, 'r')
        flag = False
        for line in file:
            if line[0:2]=="~O":
                flag = True
                continue        
            if flag:
                h = Header(line)
                if line[0] == '#':
                    continue
                elif line[0]=="~":
                    flag = False
                    break
                else:
                    self.OtherInfo.append(h)
            else:
                continue
        
    def ReadLogs(self):
        self.Logs.clear()
        index = 0
        with open(self.FileName, 'r') as file:
            for line in file:
                index+=1
                if(line[0:2] == '~A'):
                    break
                else:
                    continue
            file.close()
        Data = np.loadtxt(self.FileName,skiprows=index).T
        n_samples,n_logs = Data.shape
        for i in range(n_logs):
            Data[:,i] = np.where(Data[:,i]==self.WellInfo.NULL.Data,None , Data[:,i])
        for i,array in enumerate(Data):
            log = Log()
            log.Data = array
            log.Header = self.CurveInfo[i]
            log.Name = log.Header.Mnemonic
            self.Logs.append(log)
