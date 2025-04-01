#!/usr/bin/env -S rye run python
"""Upload a Cloudflare Worker"""

import json
import os
import requests

class MissingEnvironmentVariable(Exception):
    pass

API_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN")
if API_TOKEN is None:
    raise MissingEnvironmentVariable("Please set envar CLOUDFLARE_API_TOKEN")

ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
if ACCOUNT_ID is None:
    raise MissingEnvironmentVariable("Please set envar CLOUDFLARE_ACCOUNT_ID")

SCRIPT_NAME = "my-hello-world-script"

def main() -> None:
    # https://developers.cloudflare.com/api/resources/workers/subresources/scripts/methods/update/
    url =\
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{SCRIPT_NAME}"

    # https://blog.cloudflare.com/workers-javascript-modules/
    script_file_name = f"{SCRIPT_NAME}.mjs"
    script_content = \
    """
    export default {
        async fetch(request, env, ctx) {
            return new Response(env.MESSAGE, { status: 200 });
        }
    };
    """

    # https://developers.cloudflare.com/workers/configuration/multipart-upload-metadata/
    metadata = {
        "bindings": [
            {
                "type": "plain_text",
                "name": "MESSAGE",
                "text": "Hello World!",
            }
        ],
        "main_module": script_file_name,
    }

    # With multipart/form-data, we add each file we need
    # For Workers, we need "metadata" and the javascript module(s)
    files = {}
    files[script_file_name] = (script_file_name, script_content, "application/javascript+module")
    files["metadata"] = ("metadata.json", json.dumps(metadata), "application/json")

    # https://developers.cloudflare.com/fundamentals/api/get-started/create-token/
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }

    request = requests.request("PUT", url, headers=headers, files=files, timeout=10)
    print(f"Response status: {request.status_code}")
    print(json.dumps(json.loads(request.text), indent=2))

if __name__=="__main__":
    main()
