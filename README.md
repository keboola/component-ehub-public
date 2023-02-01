eHUB Public Extractor
=============

eHub is an Internet marketing service. It is used for affiliate marketing

This component allows you to fetch data from the Public endpoints of the eHUB marketing service

**Table of contents:**

[TOC]


Supported endpoints
===================

* Campaigns
* Vouchers

If you need more endpoints, please submit your request to
[ideas.keboola.com](https://ideas.keboola.com/)

Configuration
=============

##extractor configuration

- Fetch Campaigns (fetch_campaigns) - [REQ] boolean value , if true component will fetch all public campaign data
- Fetch Vouchers (fetch_vouchers) - [REQ] boolean value , if true component will fetch all public voucher data
- Destination (destination_settings)
    - Flatten Campaigns (flatten_campaigns) - [REQ] boolean value , if true campaign data will by flattened by
      commissions
    - Load Mode (load_mode) - [REQ] - If Full load is used, the destination table will be overwritten every run. If
      incremental load is used, data will be upserted into the destination table. Tables with a primary key will have
      rows updated, tables without a primary key will have rows appended.

Sample Configuration
=============

```json
{
  "parameters": {
    "fetch_campaigns": true,
    "fetch_vouchers": true,
    "destination_settings": {
      "flatten_campaigns": true,
      "load_mode": "full_load"
    }
  },
  "action": "run"
}
```

Output
======

List of tables, foreign keys, schema.

Development
-----------

If required, change local data folder (the `CUSTOM_FOLDER` placeholder) path to your custom path in
the `docker-compose.yml` file:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    volumes:
      - ./:/code
      - ./CUSTOM_FOLDER:/data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone this repository, init the workspace and run the component with following command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
docker-compose build
docker-compose run --rm dev
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the test suite and lint check using this command:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
docker-compose run --rm test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Integration
===========

For information about deployment and integration with KBC, please refer to the
[deployment section of developers documentation](https://developers.keboola.com/extend/component/deployment/)