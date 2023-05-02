import requests
import datetime

url = 'https://api.github.com/search/repositories'
url += '?q=language:python&sort=stars:>100000'
headers = {'Accept': 'application/vnd.github.v3+json'}
r = requests.get(url, headers=headers)

response_dict = r.json()
repo_dicts = response_dict['items']

rate_limit_url = 'https://api.github.com/rate_limit'
r_limit = requests.get(rate_limit_url, headers=headers)
limit_dict = r_limit.json()
search_limit = limit_dict["resources"]["search"]

print(
    f"""Make an API call and store the response:
    Status code: {r.status_code}
    Response to API call: {response_dict.keys()}

    Total repositories: {response_dict['total_count']}
    Complete result: {response_dict["incomplete_results"]}
    Repositories returned: {len(repo_dicts)}

API Rate Limits:
    Search Limit: {search_limit["limit"]}
    Remaining: {search_limit["remaining"]}
    Reset in: {datetime.datetime.fromtimestamp(search_limit["reset"])}"""
)

first_repo = repo_dicts[0]
print(
    f"""\nExamine the first repository:
    Keys: {len(first_repo)}
    {first_repo.keys()}"""
)

print(
    f"""\nSelected information about first repository:
    Name: {first_repo['name']}
    Owner: {first_repo['owner']['login']}
    Stars: {first_repo['stargazers_count']}
    Repository: {first_repo['html_url']}
    Created: {first_repo['created_at']}
    Updated: {first_repo['updated_at']}
    Description: {first_repo['description']}"""
)
