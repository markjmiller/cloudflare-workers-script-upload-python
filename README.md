# Cloudflare Worker Script Upload with Python

Ideally you can use the [cloudflare-python](https://github.com/cloudflare/cloudflare-python) API library to upload a [Cloudflare Worker](https://workers.cloudflare.com/). Here is an example of a direct approach using Python [requests](https://pypi.org/project/requests/).

Check out the example script here: [src/cloudflare_workers_script_upload_python](src/cloudflare_workers_script_upload_python/__init__.py).

## Try it out

1. Create a [Cloudflare Workers account](https://dash.cloudflare.com/sign-up/workers)
2. Install [Rye](https://rye.astral.sh/guide/installation/)
3. Create an `.env` environment file like this:
   ```
   CLOUDFLARE_API_TOKEN='replace_me'
   CLOUDFLARE_ACCOUNT_ID='replace_me'
   ```
   - Cloudflare docs: [Create API token](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/)
   - Cloudflare docs: [Find zone and account IDs](https://developers.cloudflare.com/fundamentals/setup/find-account-and-zone-ids/)
4. Run sync
   ```bash
   rye sync
   ```
5. You can change the name of the Worker (i.e. script name) [here](src/cloudflare_workers_script_upload_python/__init__.py), or leave it as `my-hello-world-script`
   ```
   SCRIPT_NAME = "my-hello-world-script"
   ```
6. Run the `upload-worker` script
   ```bash
   rye --env-file ./.env run upload-worker
   ```

Alternatively, you can run the script by making it executible:
```bash
chmod +x ./src/cloudflare_workers_script_upload_python/__init__.py
```
And running it like:
```bash
./src/cloudflare_workers_script_upload_python/__init__.py
```

After your script is deployed, go to `https://dash.cloudflare.com/<account_id>/workers/services/view/<script_name>/production/settings` (replace with your `account_id` and `script_name`). You can "enable" the `workers.dev` route to see the live deployment at your [workers.dev subdomain](https://developers.cloudflare.com/workers/configuration/routing/workers-dev/). You should see "Hello World!".
