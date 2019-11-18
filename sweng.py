import time

from github import Github
import plotly.express as px
import operator
import pandas as pd


def get_top_n_authors_from_last_m_commits(N, m_commits, commits):  # from past nCommits commits
    authors = {}
    for i in range(min(m_commits, commits.totalCount)):  # range(commits.totalCount):
        if commits[i].author:
            if commits[i].author.login in authors:
                authors[commits[i].author.login] = authors[commits[i].author.login] + 1
            else:
                authors[commits[i].author.login] = 1
    sorted_x = sorted(authors.items(), key=operator.itemgetter(1), reverse=True)
    # nlist = [i[0] for i in sorted_x]
    print(sorted_x)

    # return nlist[:N]
    return sorted_x[:N]


# def get_top_n_contributors_to_repo(N, repo):
#     contributors = repo.get_contributors()
#     contributor_list = []
#     for i in range(contributors.totalCount):
#         if repoName not in contributors[i].login:
#             if contributors[i].login not in contributor_list:
#                 contributor_list.append(contributors[i].login)
#
#     return contributor_list


def initialise_commits_dict(contributors):
    commits_dict = {}
    for i in range(len(contributors)):
        commits_dict[contributors[i]] = []

    return commits_dict


def initialise_commits_count_dict(contributors):
    commits_count_dict = {}
    for i in range(len(contributors)):
        commits_count_dict[contributors[i]] = 0
    return commits_count_dict


# N is number of commits from each contributor
# nCommits to search
def get_n_commits_from_top_contributors(n, n_commits, contributors, commits):
    commits_dict = initialise_commits_dict(contributors)
    for i in range(min(n_commits, commits.totalCount)):
        if commits[i].author:
            if commits[i].author.login in contributors:
                if len(commits_dict[commits[i].author.login]) < n:
                    commits_dict[commits[i].author.login].append(commits[i])
                    if commits_finished(commits_dict, n):
                        break
    return commits_dict


def print_dict(dicto):
    for key in dicto:
        print(key)
        print(dicto[key])


def commits_finished(commits_dict, N):
    for key in commits_dict:
        if len(commits_dict[key]) < N:
            return False
    return True


def main():
    g = Github("2e828516d36b5c317c601a5c5160ca5882eef366")
    ownerRepo = ownerName + "/" + repoName
    repo = g.get_repo(ownerRepo)
    # conts = get_top_n_contributors_to_repo(1000, repo)
    # for cont in conts:
    #     print(cont)
    start = time.time()
    authrs = get_top_n_authors_to_repo(10, 1000, repo)
    end = time.time()
    print(end - start)
    for auth in authrs:
        print(auth)
    # Then for each author in here, find 10 commits + average out churn/impact then add to graph?


def process_data(data, freq):
    avg_impacts = []
    avg_churns = []
    author_name = []
    freqs = []
    for key in data:
        num_commits = getNumCommits(freq, key)
        if num_commits <= 4:
            continue
        churn = 0
        impact = 0
        length = len(data[key])

        for i in range(length):
            commit = data[key][i]
            if commit.stats.total == 0:
                continue
            # churn_rate = min(commit.stats.additions, commit.stats.deletions) / commit.stats.total
            churn_rate = (commit.stats.additions - commit.stats.deletions) / commit.stats.total
            churn = churn + churn_rate
            impact = commit.stats.total
        avg_churn = churn / length
        avg_impact = impact / length
        if avg_impact > 100:
            avg_impact = 100

        avg_churns.append(avg_churn)
        avg_impacts.append(avg_impact)
        author_name.append(key)
        freqs.append(num_commits)

    data_dict = {'Impact': avg_impacts, 'Churn': avg_churns, 'Author': author_name, "Freqs": freqs}
    df = pd.DataFrame(data_dict, columns=["Author", "Impact", "Churn", "Freqs"])

    return df


def getNumCommits(freqs, name):
    for f in freqs:
        if f[0] == name:
            return f[1]
    return -1


def visualise_data(df):
    fig = px.scatter(df, x="Impact", y="Churn", size="Freqs",
                     hover_name="Author", hover_data=["Author"])

    fig.show()


def main():
    git_token = ""
    repo_owner = "mysupersuit"
    repo_name = "githubsweng"
    commits_to_search = 1000
    n_authors = 20
    commits_per_author = 5

    start(git_token, repo_owner, repo_name, commits_to_search,
          n_authors, commits_per_author)


main()
