from __future__ import annotations

import os
import sys
import time

import httpx


# ============================================================
# GEOSHIELD SENTINEL-2 RESUMABLE DOWNLOADER
# Copernicus Data Space Ecosystem
#
# Features:
# - CDSE authentication
# - Resumable HTTP downloads
# - HTTP Range support
# - Automatic retries
# - Preserves partial downloads
# - Progress reporting
# - Safe handling of server responses
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

# Sentinel-2 product UUID
PRODUCT_UUID = "c11a86f5-30a9-4de1-995d-8977f7f5085b"

MAX_RETRIES = 10
CHUNK_SIZE = 4 * 1024 * 1024

TIMEOUT = httpx.Timeout(
    connect=60.0,
    read=300.0,
    write=60.0,
    pool=60.0,
)


# ============================================================
# AUTHENTICATION
# ============================================================

def authenticate() -> str:
    print("===== GEOSHIELD SENTINEL-2 RESUMABLE DOWNLOADER =====")
    print("Authenticating with Copernicus Data Space...")

    if not USERNAME or not PASSWORD:
        print()
        print("ERROR: CDSE credentials are not set.")
        print()
        print('Run:')
        print('$env:CDSE_USERNAME="your_email"')
        print('$env:CDSE_PASSWORD="your_password"')
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

def download_product(token: str) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_file = os.path.join(
        OUTPUT_DIR,
        f"{PRODUCT_UUID}.zip",
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

    if os.path.exists(output_file):
        downloaded = os.path.getsize(output_file)

        print()
        print(
            f"Existing partial file: "
            f"{downloaded / 1024 / 1024:.2f} MB"
        )
        print("Attempting to resume download...")
    else:
        downloaded = 0

        print()
        print("No partial file found.")
        print("Starting new download.")

    for attempt in range(1, MAX_RETRIES + 1):

        print()
        print(
            f"===== DOWNLOAD ATTEMPT "
            f"{attempt}/{MAX_RETRIES} ====="
        )

        headers = {
            "Authorization": f"Bearer {token}",
            "User-Agent": "GeoShield-AI/0.1",
        }

        # Always initialize mode so Pylance and runtime
        # can prove it has a value.
        mode = "wb"

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

                print("HTTP:", response.status_code)
                print(
                    "Content-Type:",
                    response.headers.get("content-type"),
                )

                # ------------------------------------------------
                # Determine whether the server accepted resume
                # ------------------------------------------------

                if downloaded > 0:

                    if response.status_code == 206:
                        print("Resume support: ACCEPTED")
                        mode = "ab"

                    elif response.status_code == 200:
                        print(
                            "WARNING: Server returned "
                            "200 instead of 206."
                        )
                        print(
                            "Restarting download from zero."
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

                total_size: int | None = None

                if content_length:
                    remaining = int(content_length)

                    if response.status_code == 206:
                        total_size = downloaded + remaining
                    else:
                        total_size = remaining

                print()

                if total_size:
                    print(
                        "Total size:",
                        f"{total_size / 1024 / 1024:.2f} MB",
                    )
                else:
                    print("Total size: Unknown")

                # ------------------------------------------------
                # Write data
                # ------------------------------------------------

                with open(output_file, mode) as file:

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
                                    downloaded
                                    / total_size
                                    * 100
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

                final_size = os.path.getsize(output_file)

                print(
                    "File size:",
                    f"{final_size / 1024 / 1024:.2f} MB",
                )

                if total_size is None:
                    print()
                    print(
                        "Download finished, but the server "
                        "did not provide a total size."
                    )
                    print(
                        "File preserved for verification."
                    )

                    return output_file

                if final_size >= total_size:
                    print()
                    print("DOWNLOAD COMPLETE.")

                    return output_file

                print()
                print("Download incomplete.")
                print("Will resume...")

                downloaded = final_size

        except (
            httpx.ReadTimeout,
            httpx.ConnectTimeout,
            httpx.NetworkError,
            httpx.RemoteProtocolError,
        ) as error:

            print()
            print("NETWORK ERROR:")
            print(error)

            if os.path.exists(output_file):
                downloaded = os.path.getsize(output_file)

                print()
                print("Partial file preserved:")
                print(
                    f"{downloaded / 1024 / 1024:.2f} MB"
                )

            if attempt < MAX_RETRIES:

                wait_time = min(attempt * 10, 60)

                print(
                    f"Retrying in "
                    f"{wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                print()
                print("Maximum retries reached.")
                sys.exit(1)

        except httpx.HTTPStatusError as error:

            print()
            print("HTTP ERROR:")
            print(error)

            if hasattr(error, "response"):
                print(
                    "HTTP status:",
                    error.response.status_code,
                )

                print(
                    "Response:",
                    error.response.text[:1000],
                )

            sys.exit(1)

        except Exception as error:

            print()
            print("UNEXPECTED ERROR:")
            print("Error type:", type(error).__name__)
            print("Error:", error)

            sys.exit(1)

    return output_file


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    token = authenticate()

    output_file = download_product(token)

    print()
    print(
        "SENTINEL-2 RESUMABLE DOWNLOADER COMPLETE"
    )
    print("File:", output_file)


if __name__ == "__main__":
    main()
