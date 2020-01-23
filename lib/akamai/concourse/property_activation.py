from ..shared import Network
from ..papi import PropertyActivationStatus, PropertyActivationType


class PropertyActivationCheck(object):
    def __init__(self, kv):
        self.source = PropertyActivationSource(kv.get("source"))
        version = kv.get("version", {})
        self.activationId = version.get("activationId", None)
        self.propertyVersion = version.get("propertyVersion", None)

class PropertyActivationIn(PropertyActivationCheck):
    def __init__(self, kv):
        super().__init__(kv)
        self.params = {}

class PropertyActivationSource(object):
    def __init__(self, kv):
        self.property = kv.get("property")
        self.network = Network(kv.get("network", Network.production.value))
        self.activationType = PropertyActivationType(kv.get("activationType", PropertyActivationType.ACTIVATE.value))
        self.status = PropertyActivationStatus(kv.get("status", PropertyActivationStatus.ACTIVE.value))

        self.host = kv.get("host")
        self.access_token = kv.get("access_token")
        self.client_token = kv.get("client_token")
        self.client_secret = kv.get("client_secret")

    def match(self, atv):
        return (self.network == Network(atv.get("network")) and
            self.activationType == PropertyActivationType(atv.get("activationType")) and
            self.status == PropertyActivationStatus(atv.get("status")))
