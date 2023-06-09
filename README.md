# Aircraft Wildlife Strike Damage Prediction Project
 
# Project Description
 
Wildlife strikes with aircraft are a safety hazard. Damage to aircraft is not only costly to the airline industry and aircraft owners, but also can result in catastrophic loss of life in rare instances. The wildlife struck by aircraft are primarily birds. Though the majority of bird strikes with aircraft cause very little damage, the number of bird strikes is increasing, likely due to increased flight operations throughout the world. Thus, understanding what drives a damaging bird strike is useful to help mitigate the risk to the public.
 
# Project Goal
 
* Discover drivers of damaging wildlife (bird) strikes
* Use drivers to develop a machine learning model to classify damage level as None/Minor/Substantial/Destroyed (N/M/S/D), as captured in the Federal Aviation Administration (FAA) Wildlife Strike Database
* Damage Level Definition
    * N (None): No damage was reported. 
    * M (Minor): Aircraft can be rendered airworthy by simple repairs or replacements and an extensive inspection is not necessary
    * M? (Undetermined): Aircraft was damaged but details were lacking
    * S (Substantial): Aircraft incurs damage or structural failure which adversely affects the structure strength, performance, or flight characteristics of the aircraft and which normally would require major repair or replacement of the affected component. Bent fairings or cowlings; small dents or puncture holes in the skin;  damage to wing tips, antennae, tires or brakes; and engine blade damage not requiring blade replacement are specifically excluded.
    * D (Destroyed): Damage sustained makes it inadvisable to restore the aircraft to an airworthy condition

* This information could be used to assist aircrew, airport managers, and the FAA in mitigating damaging wildlife strikes
 
# Initial Thoughts
 
My initial hypothesis is that wildlife strikes are more likely to cause damage with larger species of wildlife and higher speeds. Additionally, bird strikes are more likely during dusk and dawn, during lower altitudes and the phases of flight associated with lower altitudes.
 
# The Plan
 
* Aquire data from the FAA Wildlife Strike Database
 
* Prepare data
    * Examine database's columns and keep those with the greatest utility in predicting damage level
    * For initial phase, remove rows with null values
    * For subsequent phases, handle nulls by replacing with a value for 'Unknown'
 
* Explore data in search of drivers of damage
   * Answer the following initial questions
       * What is the distribution of damage levels (N/M/S/D)?
       * Does size of species affect damage level?
       * Does aircraft speed affect damage level?
       * Does the type or mass of the aircraft affect damage level?
       * Does the engine type and/or number of engines affect damage level?
       * Does time of day affect damage level?
       * Does phase of flight affect damage level? 
      
* Develop a Model to predict what damage level will result from a bird strike
   * Use drivers identified in explore to build predictive models of different types
   * Evaluate models on train and validate data
   * Select the best model based on highest accuracy
   * Evaluate the best model on test data
 
* Draw conclusions
 
# Data Dictionary

| Feature | Definition |
|:--------|:-----------|
|damage_level| Level of damage resulting from strike; None / Minor / Substantial / Destroyed|
|time_of_day| Day/Night/Dusk/Dawn|
|airport_id| 4-letter International Civil Aviation Organization (ICAO) identifier for airport, e.g. KSAT|
|airport| Name of airport, e.g. SAN ANTONIO INTL|
|runway| Runway in use at airport, e.g. 12R|
|state| state, e.g. TX|
|opid| operator code (PVT - Private, BUS - Business, SWA - Southwest, etc.)|
|operator| operator name corresponding to opid, e.g. SOUTHWEST AIRLINES|
|aircraft| type of aircraft, e.g. B-737-800|
|ac_class| class of aicraft: A- Airplane / B- Helicopter / C- Glider / J- Ultralight / Y- Other / Z- Unknown|
|ac_mass| mass category of aircraft: 1- 0-2250 kg / 2- 2251-5700 kg / 3- 5701-27000 kg / 4- 27001-272000 kg / 5- >272000 kg|
|type_eng| type of engine: A- piston / B- turbojet / C- turboprop / D- turbofan / E- none (glider) / F- turboshaft (helicopter) / Y- other|
|num_engs| number of engines|
|phase_of_flight| phase of flight in which the strike occurred, e.g. Takeoff|
|speed| speed in nautical miles per hour (knots)|
|species_id| short form representing species of wildlife|
|species| long form for species of wildlife|
|size_of_species| size of species struck, Small / Medium / Large / Unknown|
|num_struck| number of wildlife struck|
|precipitation| type of precipitation present at time of strike, e.g. None / Rain / Snow|

## Data Dictionary Notes
* FAA Wildlife Strike Database contains records of reported wildlife strikes since 1990. Wildlife strike reporting is often voluntary. The database represents only the information received from airlines, airports, pilots, Mandatory Occurrence Reports (MOR), incident/accident information, and other sources.
* About 272,000 wildlife strikes were reported in the USA between 1990 and 2022 (about 17,000 strikes at 693 U.S. airports in 2022). An additional 4,800 strikes were reportetd by U.S. Air Carriers at foreign airports, 1990-2022 (about 230 stikes at 91 airports in 53 countries in 2022).
* Raw database downloaded 1 Jun 2023 contained data current up to 20 May 2023
* Raw database contained 297,947 rows and 100 columns

# Steps to Reproduce
1) Clone this repo.
2) Acquire the data
    - EITHER Download May 2023 csv from [here](https://drive.google.com/file/d/13Lee9Ux_FXOhzhHB2WfhPHQRYXUXOyYF/view?usp=sharing)
    - OR Download Access Database from [FAA](https://wildlife.faa.gov/search). Open in Access and save as .csv file
3) Save 'strike_reports.csv' in folder with notebook
4) Run notebook.
 
# Takeaways and Conclusions
* The vast majority of bird strikes cause no damage (>90%)
* Larger wildlife are associated with greater damage levels
* Smaller aircraft generally incurred greater damage than larger aircraft
* Slower speeds are associated with greater damage -- requires more investigation. My initial hypothesis is that most bird strikes occur at lower altitudes when generally, aircraft are flying at lower airspeeds. It could also be that bird strikes are more likely to cause damage to smaller aircraft (such as a Cessna-172) which are flying at lower airspeeds generally than larger aircraft like Boeing 737s.
* Helicopters are more likely to incur damage than airplanes
 
# Recommendations
* For pilots, smaller aircraft are more at risk for bird strike hazards. Most private pilots are flying small aircraft, and they should pay greater attention to bird watch conditions. When checking the weather and the NOTAMS, check the bird condition as well. If your local airpor doesn't broadcast this, check www.usahas.com
* For airport managers, pair data from this database with bird mitigation efforts to analyze effectiveness. The FAA in combination with the USDA have excellent recommendations for hazard mitigation, but each airport has specific hazards which can change over time. Vigilance is required.
