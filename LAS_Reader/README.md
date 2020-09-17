# MyLAS 
It is a script to interact with **LAS Well Log Data**. It currently supports [LAS version 2.0](http://www.cwls.org/wp-content/uploads/2014/09/LAS_20_Update_Jan2014.pdf) read and data access including Various Headers using custom `Header` objects and Curve data in the
form of [`numpy.ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html).

Detailed Examples and uses cases included in `MyLAS_Examples.ipynb` file.

## `Header` Class
Stores LAS Header Data.
        
        Parameters
        ----------
        string = String to convert to Header. 
               = None to create empty Header.
        
        Attributes
        ----------
        Mnemonic = Header Mnemonic.
        Unit =  Header Unit.
        Data = Header Data.
        Description = Header Description.
It can be used to Create Empty Headers too.


## `WellHeader` Class
Stores `Well Info` Block.

		Attributes
        ----------
        STRT = Header for the first depth (or time, or index number) in the file.
        STOP = Header for the last depth (or time, or index number) in the file.
        STEP = Header for the the actual difference between every successive depth (or time, or index number) in the file.
        NULL = Header for the Null values.
        COMP = Header for Company name.
        WELL = Header for the Well name.
        FLD = Header for the Field name.
        LOC = Header for the Well location.
        PROV = Header for the Province.
        CNTY = Header for the County.
        STAT = Header for the State.
        CTRY = Header for the Country.
        SRVC = Header for the Logging/Service company.
        DATE = Header for the Date logged.
        UWI = Header for Unique Well Identifier.
        API = Header for the API Number.
        LIC = Header for the Regulatory Licence Number.
Empty ``WellHeader` object can be created to manually write header data as required.
 
## `Log` Class
Stores Log data inculding Headers and Sample Values.\n

        Attributes
        ----------
        Header = Header object containing Curve Information for a Log.
        Data = Numpy array containing curve values.
        Name = Name of the Log as described in Well Curve Info. 
        
Empty Log object can be created to manually generate Log curve data and write Curve Headers.

## `Well` Class
Creates a Well object from given file name.

        Parameters
        ----------
        FileName = Name of the LAS file.

        Attributes
        ----------
        FileName = LAS Filename.
        LasVersion = LAS version of the file.
        Wrap = Wrap info of the LAS file.
        WellInfo = `WellHeader` object containing "~W" Block of LAS file.
        CurveInfo = List containing "~C" Block of LAS file. 
        ParameterInfo = List containing "~P" Block of LAS file.
        OtherInfo = List containing "~O" Block of LAS file.
        Logs = List Containing `well.Log` objects for every Log in "~A" Block of LAS file.
        API = Well API. 
        UWI = Unique Well Identity.
        
Empty `Well` object can be created to assign values to Attributes manually.