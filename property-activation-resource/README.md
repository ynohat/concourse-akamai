# Property Activation Resource

Tracks property activations (and de-activations).

## Source Configuration

* `property`: name of the property
* `network`: `STAGING` or `PRODUCTION` (default: `PRODUCTION`)
* `activationType`: `ACTIVATE` or `DEACTIVATE` (default: `ACTIVATE`)
* `status`: see enumeration below (default: `ACTIVE`)

```
ACTIVE
INACTIVE
NEW
PENDING
ZONE_1
ZONE_2
ZONE_3
ABORTED
PENDING_DEACTIVATION
DEACTIVATED
```

* `host`: Edgegrid API client host
* `access_token`: Edgegrid API access token
* `client_token`: Edgegrid API client token
* `client_secret`: Edgegrid API client secret

## Behavior

### `check`: check for new activation events

List activations filtered by the values specified in `source`.

### `in`: retrieve an activation

Retrieves activation metadata, e.g.:

```json
{
  "version": {
    "activationId": "8053264",
    "propertyVersion": 4
  },
  "metadata": [
    {
      "name": "propertyName",
      "value": "golden-master"
    },
    {
      "name": "activationType",
      "value": "ACTIVATE"
    },
    {
      "name": "status",
      "value": "ACTIVE"
    },
    {
      "name": "submitDate",
      "value": "2020-01-23T17:53:36Z"
    },
    {
      "name": "updateDate",
      "value": "2020-01-23T18:02:42Z"
    },
    {
      "name": "updatedByUser",
      "value": "johndoe"
    },
    {
      "name": "note",
      "value": "ttl 29d"
    }
  ]
}
```

Additionally, retrieves the JSON rule tree, version `etag` and variables into the output dir.

```
variables.json
rules.json
etag
```

### `out`: unsupported for now
