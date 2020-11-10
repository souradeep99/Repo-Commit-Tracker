import requests

repo_url = "https://api.github.com/search/repositories?q=org:{organization}&sort=forks&order=desc&per_page={per_page}&page={page_no}"
contributors_url = (
    "https://api.github.com/repos/{organization}/{repo_name}/contributors"
)

token = "5a9be6f06fd6051d91a43253a140726f4e383fcb"
headers = {"Authorization": token}

page_url = "/list?org={}&N={}&M={}&page_no={}"
per_page = 5


def query_organization(org, n, m, page_no):

    g = int(page_no)
    val = min(per_page, n - (g - 1) * per_page)
    if val < 0:
        val = 0

    repos = requests.get(
        repo_url.format(organization=org, per_page=per_page, page_no=str(page_no)),
        headers=headers,
    ).json()
    forks = []

    repo_count_per_page = 0
    for i in repos["items"]:
        if ("forks_count" in i) and ("html_url" in i) and ("name" in i):
            if repo_count_per_page == val:
                break
            forks.append((i["forks_count"], i["html_url"], i["name"]))
            repo_count_per_page += 1

    next_page_link = "#"
    previous_page_link = "#"

    next_page = int(page_no) + 1
    pervious_page = int(page_no) - 1

    if per_page * int(page_no) < n:
        next_page_link = page_url.format(org, n, m, str(next_page))
    if int(page_no) > 1:
        previous_page_link = page_url.format(org, n, m, str(pervious_page))

    final = []
    for i in range(len(forks)):
        commit = []
        cmt = requests.get(
            contributors_url.format(organization=org, repo_name=forks[i][2]),
            headers=headers,
        ).json()
        count = m
        rank = 1
        for j in cmt:
            if ("contributions" in j) and ("html_url" in j) and ("login" in j):
                commit.append((j["contributions"], j["html_url"], j["login"], rank))
                count -= 1
                rank += 1
                if count == 0:
                    break

        final.append((forks[i][0], forks[i][1], forks[i][2], commit))

    return final, next_page_link, previous_page_link


def get(org, n, m, page_no):
    if n <= 0 or m <= 0:
        return "404"
    final = query_organization(org, int(n), int(m), page_no)
    if len(final) == 0:
        return "404"
    return final
