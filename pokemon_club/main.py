#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask_cors import CORS
from nebula2.gclient.net import ConnectionPool
from nebula2.Config import Config

import os


app = Flask(__name__)
CORS(app, supports_credentials=True)
DEFAULT_NG_CREDENTIAL = ("user", "password")


@app.route("/v1/recommended_friends/<user>", methods=["GET"])
def recommended_friends(user):
    """
    Get Recommended new Friends
    """
    ng_credential = get_nebula_graph_crential()
    session = connection_pool.get_session(*ng_credential)
    try:
        session.execute('USE pokemon_club')
        query = (
            f'GO FROM "{ user }" '
             'OVER owns_pokemon '
             'YIELD owns_pokemon._dst as pokemon_id '
             '| GO FROM $-.pokemon_id '
             'OVER owns_pokemon REVERSELY')
        query_result = session.execute(query)
        trainers = [str(trainer.values[0].get_sVal(), 'utf-8') for trainer in query_result.rows()]
        trainers = list(set(trainers))
        if user in trainers:
            trainers.remove(user)
    finally:
        session.release()

    return jsonify(trainers)


@app.route("/")
def index():
    """
    versions
    """
    return jsonify(
        {"versions": {
            "values": [
                {
                    "status": "stable",
                    "updated": "2017-02-22T00:00:00Z",
                    "media-types": [
                      {
                        "base": "application/json",
                      }
                    ],
                    "id": "v1",
                    "links": [
                      {
                        "href": "v1/",
                        "rel": "self"
                      }
                    ]
                }
            ]
        }})


def access_secret_version(project_id, secret_id, version_id):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    ref:
    https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets
    """

    # Import the Secret Manager client library.
    from google.cloud import secretmanager

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    return response.payload.data.decode("UTF-8")


def get_nebula_graph_crential():
    """
    Get nebula graph credential from GCP secret-manager, if not configured,
    return default credential instead.
    """
    project_id = os.environ.get('NG_GCP_PROPJECT_ID', None)
    user_secret_id = os.environ.get('NG_GCP_USER_SECRET_ID', None)
    password_secret_id = os.environ.get('NG_GCP_PROPJECT_ID', None)

    if all((project_id, user_secret_id, password_secret_id)):
        version_id = os.environ.get('NG_GCP_CREDENTIAL_VERSION',
                                    'latest')
        return (access_secret_version(project_id, secret_id,
                version_id) for secret_id in (user_secret_id,
                password_secret_id))

    return DEFAULT_NG_CREDENTIAL


def parse_nebula_graphd_endpoint():
    ng_endpoints_str = os.environ.get('NG_ENDPOINTS', '127.0.0.1:9669,').split(",")
    ng_endpoints = []
    for endpoint in ng_endpoints_str:
        if endpoint:
            parts = endpoint.split(":") # we dont consider IPv6 now
            ng_endpoints.append((parts[0], int(parts[1])))
    return ng_endpoints


ng_config = Config()
ng_config.max_connection_pool_size = int(
    os.environ.get('NG_MAX_CONN_POOL_SIZE', 10))
ng_endpoints = parse_nebula_graphd_endpoint()
connection_pool = ConnectionPool()

if __name__ == "__main__":
    connection_pool.init(ng_endpoints, ng_config)
    try:
        app.run(host="0.0.0.0", port=5000)
    finally:
        connection_pool.close()
else:
    connection_pool.init(ng_endpoints, ng_config)
