import time
from rich import print

from schemas import StockingEventFactory
from schemas.utils import validate

from xls_utils import xls2dicts

from http_utils import (
    data_to_enum,
    get_species,
    get_strains,
    get_lakes,
    get_agencies,
    get_hatcheries,
    get_state_provinces,
    get_marks,
    get_grid10s,
    get_mark_enum,
    get_management_units,
    get_grid10_enum,
    get_man_unit_enum,
    get_stocking_mortalities,
    get_lifestages,
    get_stocking_methods,
    get_strain_enum
)

start_time = time.perf_counter()


SRC_XLS = "C:/Users/COTTRILLAD/Downloads/GLFSD_NewDataSubmission_Template_2025_09_11.xlsx"
#SRC_XLS = "C:/Users/COTTRILLAD/Downloads/GLFSD_NewDataSubmission_Template_2025-12-08.xlsx"


# fetch our lookup values from the api and convert them it enums that will be used by
# the pydantic validator

agencies = get_agencies()
agency_enum = data_to_enum(agencies, "Agency", "abbrev", "agency_name")

lakes = get_lakes()
lake_enum = data_to_enum(lakes, "Lake", "abbrev", "lake_name")

hatcheries = get_hatcheries()
# hatcheries are formatted "Hatchery Name [abbrev]"
hatchery_dicts = [{"abbrev":x['abbrev'], "label":f"{x['hatchery_name']} [{x['abbrev']}]"} for x in hatcheries]

hatchery_enum = data_to_enum(hatchery_dicts, "Hatchery", "label", "abbrev")


state_provinces = get_state_provinces()
state_province_enum = data_to_enum(
    state_provinces, "StateProvince", "abbrev", "name"
)

species = get_species()
species_enum = data_to_enum(species, "Species", "abbrev", "common_name")

conditions = get_stocking_mortalities()

if "condition" in conditions[0]:
    condition_enum = data_to_enum(conditions, "Condition", "condition", "description")
else:
    condition_enum = data_to_enum(conditions, "Condition", "value", "description")

life_stages = get_lifestages()
life_stage_enum = data_to_enum(life_stages, "LifeStage", "abbrev", "description")

stocking_methods = get_stocking_methods()
stocking_method_enum = data_to_enum(
    stocking_methods, "StockingMethod", "stk_meth", "description"
)


strains = get_strains()
# this will be filtered by species:

marks = get_marks()
# split into marks and pys-chem marks

clip_enum  = get_mark_enum(marks, 'clips')
mark_enum  = get_mark_enum(marks, 'marks')
tag_enum  = get_mark_enum(marks, 'tags')

grid10s = get_grid10s()



# grid 10 should be filtered by lake (and even management unit):

# managememnt unit should be filtered by lake
man_units = get_management_units()


fetching_time = time.perf_counter()


# read in out stocking data - convert it to a dict and then validate it.  because some
# of the fields are depenent on other fields, the enums will be created dynamically on
# each iteration depending on the data in the current record:

events = xls2dicts(SRC_XLS)


results = []

for event in events:
    lake = event['LAKE']
    man_unit_enum  = get_man_unit_enum(man_units, lake)
    grid10_enum  = get_grid10_enum(grid10s, lake)

    spc = event['SPECIES']
    strain_enum  = get_strain_enum(strains, spc)

    grid = event['GRID_10MIN']
    event['GRID_10MIN'] = str(grid)

    validator = StockingEventFactory(
        AgencyEnum = agency_enum,
        LakeEnum = lake_enum,
        StateProvinceEnum = state_province_enum,
        StatDistEnum = man_unit_enum,
        Grid10Enum = grid10_enum,
        StockingMethodEnum = stocking_method_enum,
        SpcEnum = species_enum,
        StrainEnum = strain_enum,
        LifeStageEnum = life_stage_enum,
        ClipEnum = clip_enum,
        MarkEnum = mark_enum,
        TagTypeEnum = tag_enum,
        MortalityEnum = condition_enum,
        HatcheryEnum = hatchery_enum
    )
    result = validate(event, validator)
    results.append(result)

print(f"{len(results)} stocking records validated.")


errors = [x for x in results if x['errors']]

if errors:
    print(f"{len(errors)} records had  at least one error")
    print("For Example")
    for item in errors[:5]:
        print(item)
else:
    print(f"All records were considered valid and no errors were found.")

end_time = time.perf_counter()

elapsed_time = end_time - start_time
print(f"Total Elapsed time: {elapsed_time:.2f} seconds")

fetching = fetching_time - start_time
print(f" {fetching:.2f} seconds fetching data")

validating = end_time - fetching_time
print(f" {validating:.2f} seconds validating data")
