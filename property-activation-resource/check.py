#!/usr/bin/env python3

import sys
import json
from os import path

from akamai.concourse.property_activation import PropertyActivationCheck
from akamai.requests import EdgeGridSession
from akamai.papi import PropertyDescriptor, get_property_descriptor, get_property_activations
from akamai.shared import Network

try:
    queryData = sys.stdin.read()
    print(queryData, file=sys.stderr)
    query = json.loads(queryData)
    check = PropertyActivationCheck(query)
except KeyError as e:
    print("Expecting option: {0}".format(e), file=sys.stderr)
    sys.exit(1)

try:
    source = check.source
    session = EdgeGridSession(
        host=source.host,
        access_token=source.access_token,
        client_token=source.client_token,
        client_secret=source.client_secret
    )

    result = []
    pd = get_property_descriptor(session, source.property)
    if isinstance(pd, PropertyDescriptor):
        atvs = get_property_activations(session, pd.contractId, pd.groupId, pd.propertyId)
        filtered = filter(source.match, atvs)
        latest = filter(lambda atv: atv.get("activationId") >= str(check.activationId), filtered)
        atv_ids = map(lambda atv: dict(
            activationId=str(atv["activationId"]),
            propertyVersion=str(atv["propertyVersion"]),
            updateDate=str(atv["updateDate"]),
        ), latest)
        result = sorted(atv_ids, key=lambda atv: atv.get("activationId"))
    print(json.dumps(result))
except Exception as e:
    print("{0}: {1}".format(type(e).__name__, " ".join(e.args)), file=sys.stderr)
    sys.exit(2)
