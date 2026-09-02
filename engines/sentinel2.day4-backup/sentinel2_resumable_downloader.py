import os
import sys
import time
import httpx

# ============================================================
# GEOSHIELD SENTINEL-2 RESUMABLE DOWNLOADER
# Copernicus Data Space Ecosystem
#
# Features:
# - Authentication
# - Resumable HTTP downloads
# - HTTP Range support
# - Automatic retries
# - Preserves partially downloaded files
# - Progress reporting
# ============================================================

USERNAME = os.getenv("CDSE_USERNAME")
PASSWORD = os.getenv("CDSE_PASSWORD")

CLIENT_ID = "cdse-public"

TOKEN_URL = (
    "https://identity.dataspace.copernicus.eu/"
    "auth/realms/CDSE/protocol/openid-connect/token"
)

DOWNLOAD_URL = (
    "https://zipper.dataspace.copernicus.eu/"
    "odata/v1/Products"
)

OUTPUT_DIR = "data/sentinel2"

# Latest Sentinel-2 product discovered by the connector
PRODUCT_UUID = "c11a86f5-30a9-4de1-995d-8977f7f5085b"

MAX_RETRIES = 10
CHUNK_SIZE = 4 * 1024 * 1024

# Long timeout because Sentinel-2 products are large
TIMEOUT = httpx.Timeout(
    connect=60.0,
    read=300.0,
    write=60.0,
    pool=60.0,
)


# ============================================================
# AUTHENTICATION
# ============================================================

def authenticate():

    print("===== GEOSHIELD SENTINEL-2 RESUMABLE DOWNLOADER =====")
    print("Authenticating with Copernicus Data Space...")

    if not USERNAME or not PASSWORD:

        print()
        print("ERROR: CDSE credentials are not set.")
        print()
        print("Run:")
        print('$env:CDSE_USERNAME="your_email"')
        print('$env:CDSE_PASSWORD="your_new_password"')
        sys.exit(1)

    response = httpx.post(
        TOKEN_URL,
        data={
            "grant_type": "password",
            "client_id": CLIENT_ID,
            "username": USERNAME,
            "password": PASSWORD,
        },
        timeout=60,
    )

    print("AUTH:", response.status_code)

    response.raise_for_status()

    token = response.json().get("access_token")

    if not token:

        print("ERROR: No access token returned.")
        sys.exit(1)

    print("TOKEN: True")

    return token


# ============================================================
# DOWNLOAD
# ============================================================

def download_product(token):

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_file = os.path.join(
        OUTPUT_DIR,
        f"{PRODUCT_UUID}.zip"
    )

    url = (
        f"{DOWNLOAD_URL}"
        f"({PRODUCT_UUID})"
        f"/$value"
    )

    print()
    print("===== SENTINEL-2 DOWNLOAD =====")
    print("UUID:", PRODUCT_UUID)
    print("Destination:", output_file)

    existing_size = 0

    if os.path.exists(output_file):

        existing_size = os.path.getsize(output_file)

        print()
        print(
            f"Existing partial file: "
            f"{existing_size / 1024 / 1024:.2f} MB"
        )

        print("Attempting to resume download...")

    else:

        print()
        print("No partial file found.")
        print("Starting new download.")

    downloaded = existing_size

    for attempt in range(1, MAX_RETRIES + 1):

        print()
        print(
            f"===== DOWNLOAD ATTEMPT "
            f"{attempt}/{MAX_RETRIES} ====="
        )

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # ----------------------------------------------------
        # Resume request
        # ----------------------------------------------------

        if downloaded > 0:

            headers["Range"] = f"bytes={downloaded}-"

            print(
                f"Requesting bytes from "
                f"{downloaded:,}..."
            )

        try:

            with httpx.stream(
                "GET",
                url,
                headers=headers,
                timeout=TIMEOUT,
            ) as response:

                print(
                    "HTTP:",
                    response.status_code
                )

                print(
                    "Content-Type:",
                    response.headers.get(
                        "content-type"
                    )
                )

                # ------------------------------------------------
                # Server accepted resume
                # ------------------------------------------------

                if downloaded > 0:

                    if response.status_code == 206:

                        print(
                            "Resume support: ACCEPTED"
                        )

                        mode = "ab"

                    elif response.status_code == 200:

                        print(
                            "WARNING: Server returned "
                            "200 instead of 206."
                        )

                        print(
                            "Restarting download "
                            "from zero."
                        )

                        downloaded = 0

                        mode = "wb"

                    else:

                        response.raise_for_status()

                else:

                    response.raise_for_status()

                    mode = "wb"

                # ------------------------------------------------
                # Determine total size
                # ------------------------------------------------

                content_length = response.headers.get(
                    "content-length"
                )

                if content_length:

                    remaining = int(content_length)

                    if response.status_code == 206:

                        total_size = (
                            downloaded +
                            remaining
                        )

                    else:

                        total_size = remaining

                else:

                    total_size = None

                print()

                if total_size:

                    print(
                        "Total size:",
                        f"{total_size / 1024 / 1024:.2f} MB"
                    )

                # ------------------------------------------------
                # Write data
                # ------------------------------------------------

                with open(
                    output_file,
                    mode
                ) as file:

                    last_report = time.time()

                    for chunk in response.iter_bytes(
                        chunk_size=CHUNK_SIZE
                    ):

                        if not chunk:
                            continue

                        file.write(chunk)

                        downloaded += len(chunk)

                        now = time.time()

                        if now - last_report >= 2:

                            if total_size:

                                percent = (
                                    downloaded /
                                    total_size *
                                    100
                                )

                                print(
                                    f"Downloaded: "
                                    f"{downloaded / 1024 / 1024:.1f} MB "
                                    f"/ "
                                    f"{total_size / 1024 / 1024:.1f} MB "
                                    f"({percent:.1f}%)"
                                )

                            else:

                                print(
                                    f"Downloaded: "
                                    f"{downloaded / 1024 / 1024:.1f} MB"
                                )

                            last_report = now

                print()
                print(
                    "Connection completed successfully."
                )

                # ------------------------------------------------
                # Verify completion
                # ------------------------------------------------

                final_size = os.path.getsize(
                    output_file
                )

                print(
                    "File size:",
                    f"{final_size / 1024 / 1024:.2f} MB"
                )

                if total_size:

                    if final_size >= total_size:

                        print()
                        print(
                            "DOWNLOAD COMPLETE."
                        )

                        return output_file

                    else:

                        print()
                        print(
                            "Download incomplete."
                        )

                        print(
                            "Will resume..."
                        )

                        downloaded = final_size

        except (
            httpx.ReadTimeout,
            httpx.ConnectTimeout,
            httpx.NetworkError,
            httpx.RemoteProtocolError,
        ) as error:

            print()
            print(
                "NETWORK ERROR:"
            )

            print(error)

            if os.path.exists(output_file):

                downloaded = os.path.getsize(
                    output_file
                )

                print()
                print(
                    f"Partial file preserved:"
                )

                print(
                    f"{downloaded / 1024 / 1024:.2f} MB"
                )

            if attempt < MAX_RETRIES:

                wait_time = min(
                    attempt * 10,
                    60
                )

                print(
                    f"Retrying in "
                    f"{wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:

                print()
                print(
                    "Maximum retries reached."
                )

                sys.exit(1)

    return output_file


# ============================================================
# MAIN
# ============================================================

def main():

    token = authenticate()

    download_product(token)

    print()
    print(
        "SENTINEL-2 RESUMABLE DOWNLOADER COMPLETE"
    )


if __name__ == "__main__":
    main()