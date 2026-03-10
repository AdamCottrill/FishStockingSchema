import niquests as requests
from enum import Enum
import os



def data_to_enum(data, name, key_name, value_name):
    tmp = {x[value_name]:x[key_name] for x in data}
    return Enum(name, tmp)

def get_strain_enum(data, species):
    tmp = [x for x in data if x['strain_species']['abbrev']==species]
    return data_to_enum(tmp, 'Strain', 'strain_code', 'slug')


def get_mark_enum(data, what):
    if what == 'clips':
        tmp = [x for x in data if x['mark_type']=='finclip']
        name = 'FinClip'
    elif what=='tags':
        tmp = [x for x in data if x['mark_type'] in ['tag', 'unknown']  or x['mark_code']=='NONE']
    else:
        tmp = [x for x in data if x['mark_type'] in ['chemical', 'unknown']  or x['mark_code']=='NONE']
        name = 'Mark'
    return data_to_enum(tmp, 'name', 'mark_code', 'description')



def get_grid10_enum(data, lake):
    tmp = [x for x in data if x['lake']['abbrev']==lake ]
    return data_to_enum(tmp, 'Grid10', 'grid', 'grid')

def get_man_unit_enum(data, lake):
    tmp = [x for x in data if x['lake']['abbrev']==lake and x['primary']]
    return data_to_enum(tmp, 'ManUnit', 'label', 'slug')




def get_base_url():
    """override locally by setting FSDVIZ_API to in shell"""

    BASE_URL = os.getenv("FSDVIZ_API","https://fsis.glfc.org/api/v1/")
    return BASE_URL


# common  end points:

def get_lakes():

    url = get_base_url() + "common/lake"

    r = requests.get(url)
    return r.json()


def get_agencies():

    url = get_base_url() + "common/agency"
    r = requests.get(url)
    return r.json()

def get_state_provinces():

    url = get_base_url() + "common/state_province"

    r = requests.get(url)
    return r.json()


def get_marks():

    url = get_base_url() + "common/mark"

    r = requests.get(url)
    return r.json()

def get_species():

    url = get_base_url() + "common/species"

    r = requests.get(url)
    return r.json()

def get_strains():

    url = get_base_url() + "common/strain"

    r = requests.get(url)
    return r.json()

def get_strainraws():
    """soon to be strain_agency"""
    url = get_base_url() + "common/strainraw"

    r = requests.get(url)
    return r.json()


def get_grid10s():

    url = get_base_url() + "common/grid10"

    r = requests.get(url)
    return r.json()


def get_management_units():
    """"""
    url = get_base_url() + "common/management_unit"

    r = requests.get(url)
    return r.json()


# stocking  end points:


def get_stocking_mortalities():
    """soon to be renamed 'stocking mortality'"""
    url = get_base_url() + "stocking/stocking_mortality"
    r = requests.get(url)
    if r.status_code == 400:
        url = get_base_url() + "stocking/condition"
        r = requests.get(url)
    return r.json()

def get_lifestages():
    """"""
    url = get_base_url() + "stocking/lifestage"

    r = requests.get(url)
    return r.json()

def get_stocking_methods():
    """"""
    url = get_base_url() + "stocking/stocking_method"

    r = requests.get(url)
    return r.json()

def get_hatcheries():
    """"""
    url = get_base_url() + "stocking/hatchery"

    r = requests.get(url)
    return r.json()
