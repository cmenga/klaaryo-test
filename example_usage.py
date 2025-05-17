from requests import post, get
from json import dumps
from time import sleep

superuser_email = "example@test.com"
superuser_password = "Ciao1234"

HOST: str = "http://127.0.0.1:8000/api/"


def main():
    access_token = get_access_token()
    candidate = create_candidate(access_token)
    candidate = get_candidate(access_token, uuid=candidate["id"])


def get_access_token():
    """
    The function `get_access_token` sends a POST request to a specified URL with user credentials to
    obtain an access token.
    """
    response = post(
        url=f"{HOST}token/",
        json={"email": superuser_email, "password": superuser_password},
        headers={"Content-Type": "application/json"},
    )
    access_token = response.json()["access"]
    print(
        "Request for access forwarded with code: ",
        response.status_code,
        "\n\n Access Token:\n",
        access_token,
    )
    return access_token


def create_candidate(access_token: str):
    """
    The function `create_candidate` sends a POST request to create a candidate with the provided access
    token, full name, and email.
    """
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = post(
        url=f"{HOST}candidate",
        headers=headers,
        json={"full_name": "pippo pluto", "email": "pippo_pluto@test.com"},
    )
    content_json = response.json()
    print("\n\nCreated the candidate:\n", dumps(content_json, indent=3))
    return content_json


def get_candidate(access_token: str, uuid: str):
    """
    The function `get_candidate` retrieves candidate information using an access token and UUID, and
    prints the candidate's screening details.
    """
    sleep(1)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }
    response = get(url=f"{HOST}candidate/{uuid}", headers=headers)
    content_json = response.json()

    print(f"\n\nCandidate {uuid} with screening:\n", dumps(content_json, indent=3))
    return content_json


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(ex.__str__())
