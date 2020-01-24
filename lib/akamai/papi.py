import json
from enum import Enum
from .shared import Network

class PAPIError(RuntimeError):
    pass

class PropertyActivationType(Enum):
    ACTIVATE = "ACTIVATE"
    DEACTIVATE = "DEACTIVATE"

class PropertyActivationStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    NEW = "NEW"
    PENDING = "PENDING"
    ZONE_1 = "ZONE_1"
    ZONE_2 = "ZONE_2"
    ZONE_3 = "ZONE_3"
    ABORTED = "ABORTED"
    PENDING_DEACTIVATION = "PENDING_DEACTIVATION"
    DEACTIVATED = "DEACTIVATED"

class PropertyDescriptor(object):
    def __init__(self, contractId, groupId, propertyId, propertyName, **kwargs):
        self.contractId = contractId
        self.groupId = groupId
        self.propertyId = propertyId

def get_property_descriptor(session, propertyName):
    url = "/papi/v1/search/find-by-value"
    result = session.post(url, data=json.dumps({
        "propertyName": propertyName
    }), headers={"Content-Type": "application/json"})
    if result.status_code != 200:
        raise PAPIError("{0} returned status {1}".format(url, result.status_code))
    result = result.json()
    versions = result.get("versions", {}).get("items", [])
    version = next(filter(lambda v: v.get("propertyName") == propertyName, versions), None)
    if version != None:
        return PropertyDescriptor(**version)
    return None

def get_property_activations(session, contractId, groupId, propertyId):
    url = "/papi/v1/properties/{propertyId}/activations".format(
        propertyId=propertyId
    )
    result = session.get(url, params=dict(
        contractId=contractId,
        groupId=groupId
    ))
    if result.status_code == 404:
        return []
    if result.status_code != 200:
        raise PAPIError("{0} returned status {1}".format(url, result.status_code))
    activations = result.json().get("activations", {}).get("items", [])
    return activations

def get_property_activation(session, contractId, groupId, propertyId, activationId):
    url = "/papi/v1/properties/{propertyId}/activations/{activationId}".format(
        propertyId=propertyId,
        activationId=activationId
    )
    result = session.get(url, params=dict(
        contractId=contractId,
        groupId=groupId
    ))
    if result.status_code == 404:
        return None
    if result.status_code != 200:
        raise PAPIError("{0} returned status {1}".format(url, result.status_code))
    activations = result.json().get("activations", {}).get("items", [])
    return activations[0]

def get_property_version(session, contractId, groupId, propertyId, propertyVersion):
    url = "/papi/v1/properties/{propertyId}/versions/{propertyVersion}".format(
        propertyId=propertyId,
        propertyVersion=propertyVersion
    )
    result = session.get(url, params=dict(
        contractId=contractId,
        groupId=groupId
    ))
    if result.status_code == 404:
        return None
    if result.status_code != 200:
        raise PAPIError("{0} returned status {1}".format(url, result.status_code))
    return result.json().get("versions", {}).get("items")[0]

def get_property_rule_tree(session, contractId, groupId, propertyId, propertyVersion):
    url = "/papi/v1/properties/{propertyId}/versions/{propertyVersion}/rules".format(
        propertyId=propertyId,
        propertyVersion=propertyVersion
    )
    result = session.get(url, params=dict(
        contractId=contractId,
        groupId=groupId,
        validateRules=False
    ))
    if result.status_code == 404:
        return None
    if result.status_code != 200:
        raise PAPIError("{0} returned status {1}".format(url, result.status_code))
    return result.json()

def get_symbolic_property_version(session, pd, version):
    url = "/papi/v1/properties/{propertyId}".format(
        propertyId=pd.propertyId
    )
    result = session.get(url, params={
        "contractId": pd.contractId,
        "groupId": pd.groupId
    })
    if result.status_code != 200:
        raise PAPIError("{0} returned status {1}".format(url, result.status_code))
    result = result.json().get("properties", {}).get("items", []).pop(0)
    return result.get("{0}Version".format(version.name))
