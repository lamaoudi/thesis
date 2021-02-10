## Master's Thesis Project

Objective: Develop a tool/pipeline to synthesize all required inputs for electrification planning models from publiclly available data. This will imporve electrifican planning models' scalability and enable large-region analyses. 

Obtaining the necessary data to run the planning models can be broadly classified into four parts: 

(1) Identfication of number and location of ALL households. 

(2) Delineation of productive loads or households as electrified or unelectrified (unelectrified includes infrastructure under, but not connected, to the grid).

(3) Estimation of the current medium voltage network.

(4) Identification of demand and location of ALL productive loads via. Google Maps API Search 

**Description of how to run each part:** 


**Part 1** "1_loadHHLD.py" 

**Publicly Available Data Needed (for respective country):**

(1) **GADM Country Boundaries:** https://gadm.org/data.html
   *-- Format required: ESRI Shp file*
   
   SAVE: data/gadm/gadm36_'country-code'_shp/
    
(2) **Facebook Settlement Data:** https://www.ciesin.columbia.edu/data/hrsl/
    *-- Fromat required: .csv file
    
    SAVE: data/fb_pop/population_'country-code'/population_'country-code'.csv
  
**Functions:** utils/functions_1.py
    
**OUTPUT:** outputs/_1/---  < Shapefile of LV households



**Part 2** "2_electrification-statis.py" 

**Publicly Available Data Needed (for respective country):**

(1) **GADM Country Boundaries** 
    
(2) **Falchetta Demand Tier Raster:** https://github.com/giacfalk/Electrification_SSA_data
    *-- Fromat required: .netcdf file (script alreadyran to convert to geotiff)
    
    SAVE: data/falchetta_tier/tierofaccess_SSA_2018.tiff
    
(3) **Country's Multi-Tier Framework:** [link manually searched]
    *-- Format required: .csv file (template available - manually input values)
 
    Functions: utils/functions_2.py
    
    OUTPUT: outputs/_2/---  < 2 Shapefiles assigning (1) tier and (2) extracting only electrified (i.e. tier >0) to LV households or any load. 



**Part 3** 

**3.1** Create Reference Network Model Input Files for LVC in python: "3_create-LVC.py" 

    OUTPUT: outputs/_3/---  < .csv file < manually convert in Excel to txt.file 



TODO: **3.2** Create Reference Network Model Input Files for MVC in python: "3-2_create-MVC.py" 

-- Only Available in "scratch" Jupyter Notebook Files -- 



TODO: **3.3** Automate Transmission / HV Substations Identification from OpenStreetMaps API and converting them to RNM inputs 
            OR (if unavailable) manually plot location of substations from publicly available sketch/layout of grid network 
            
 -- Only Available in "scratch" Jupyter Notebook Files -- 


    Run RNM with (1) LVC, (2) MVC, (3) Catalog, (4) Substations 

    OUTPUT:** outputs/_4/---  < .shape file 



TODO: **Part 4** "4_extractMVC.py"

NEEDED: 

    (1) Google Maps Places API Key
    (2) Raster of country w/ centroid coordinates available 
    (3) .csv file of searchable list of businesses 

 -- To be Finalized, but method has been validated- find in Jupyter Notebook scratch -- 


