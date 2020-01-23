from enum import Enum

class Network(Enum):
    staging = "STAGING"
    production = "PRODUCTION"

class SymbolicVersion(Enum):
    latest = "LATEST"
    staging = Network.staging
    production = Network.production
