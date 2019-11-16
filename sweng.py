import math
import time

from github import Github
import plotly.express as px
# import plotly.graph_objects as go
import operator
import numpy as np
import pandas as pd
import statistics


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
    prev_std_dev = 0.0
    std_dev = 0.0
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
            #churn_rate = min(commit.stats.additions, commit.stats.deletions) / commit.stats.total
            churn_rate = (commit.stats.additions - commit.stats.deletions) / commit.stats.total
            churn = churn + churn_rate
            impact = commit.stats.total
        avg_churn = churn / length
        avg_impact = impact / length
        if avg_impact > 100:
            avg_impact = 100

        # pot_impact = avg_impacts
        # pot_impact.append(avg_impact)
        # pot_std_dev = statistics.stdev(pot_impact)

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


main()

# def visualiseData():

# commits_list = []
# x = 0
# while len(commits_list) < 10:
#     if commits[x].author:
#         if commits[x].author.login == contributor_list[0]:
#             commits_list.append(commits[x])
#             print(len(commits_list))
#     x = x + 1
#
# impact = 0
# churn = 0
# avgChurns = []
# avgImpacts = []
#
# for commit in commits_list:
#     churnRate = min(commit.stats.additions, commit.stats.deletions) / commit.stats.total
#     churn = churn + churnRate
#     impactRate = commit.stats.total
#     impact = impact + impactRate
#     print("churn rate ", churnRate)
#     print(commit.stats.additions)
#     print(commit.stats.deletions)
#     print(commit.stats.total)
#
# avgImpacts.append(impactRate)
# avgChurns.append(churnRate)
#
# layout = go.Layout(
#     title="Impact vs Churn",
#     xaxis=dict(
#         title="Impact"
#     ),
#     yaxis=dict(
#         title="Churn"
#     )
# )
#
# fig = go.Figure(layout=layout)
#
# fig.add_trace(go.Scatter(
#     x=impacts,
#     y=churns,
#     mode='markers'
# ))
#
# # fig = px.scatter(impacts, x="impacts", y="churns")
#
# fig.show()
