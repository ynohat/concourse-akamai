#!/usr/bin/env python3

import sys
import json
from os import path

from akamai.concourse.property_activation import PropertyActivationIn
from akamai.requests import EdgeGridSession
from akamai.papi import (get_property_descriptor,
    get_property_activation,
    get_property_rule_tree,
    get_property_version)
from akamai.shared import Network

try:
    query = json.loads(sys.stdin.read())
    input = PropertyActivationIn(query)
except KeyError as e:
    print("Expecting option: {0}".format(e), file=sys.stderr)
    sys.exit(1)

try:
    source = input.source
    session = EdgeGridSession(
        host=source.host,
        access_token=source.access_token,
        client_token=source.client_token,
        client_secret=source.client_secret
    )
    pd = get_property_descriptor(session, source.property)
    atv = get_property_activation(
        session, pd.contractId, pd.groupId, pd.propertyId, input.activationId)
    pv = get_property_version(
        session, pd.contractId, pd.groupId, pd.propertyId, atv.get("propertyVersion"))

    # Write rule tree & variables into the output folder
    rules = get_property_rule_tree(
        session, pd.contractId, pd.groupId, pd.propertyId, atv.get("propertyVersion"))
    with open(path.join(sys.argv[1], "etag"), "w") as fd:
        fd.write(rules.get("etag"))
    with open(path.join(sys.argv[1], "variables.json"), "w") as fd:
        fd.write(json.dumps(rules.get("rules").get("variables"), indent="  "))
    with open(path.join(sys.argv[1], "rules.json"), "w") as fd:
        rules = dict(rules=dict(
            name=rules.get("rules").get("name"),
            children=rules.get("rules").get("children"),
            options=rules.get("rules").get("options")
        ))
        fd.write(json.dumps(rules, indent="  "))

    # Output version and metadata
    print(json.dumps(dict(
        version=dict(activationId=input.activationId,
                     propertyVersion=atv.get("propertyVersion")),
        metadata=[
            dict(name="propertyName", value=atv.get("propertyName")),
            dict(name="activationType", value=atv.get("activationType")),
            dict(name="status", value=atv.get("status")),
            dict(name="submitDate", value=atv.get("submitDate")),
            dict(name="updateDate", value=atv.get("updateDate")),
            dict(name="updatedByUser", value=pv.get("updatedByUser")),
            dict(name="note", value=pv.get("note")),

        ]
    )))
except Exception as e:
    print("{0}: {1}".format(type(e).__name__, " ".join(e.args)), file=sys.stderr)
    sys.exit(1)
