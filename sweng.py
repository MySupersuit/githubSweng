import time

from github import Github
#import plotly.express as px
import plotly.graph_objects as go
import operator

ownerName = "tensorflow"
repoName = "tensorflow"


def get_top_n_authors_to_repo(N, nCommits, repo): # from past nCommits commits
    authors = {}
    commits = repo.get_commits()
#   for commit in commits:
    for i in range(nCommits): #range(commits.totalCount):
        if commits[i].author:
            if commits[i].author.login in authors:
                authors[commits[i].author.login] = authors[commits[i].author.login] + 1
            else:
                authors[commits[i].author.login] = 1
    sorted_x = sorted(authors.items(), key=operator.itemgetter(1), reverse=True)
    nlist = [i[0] for i in sorted_x]
    print(sorted_x)

    return nlist[:N]

def get_top_n_contributors_to_repo(N, repo):
    contributors = repo.get_contributors()
    contributor_list = []
    j = 0
    # while i >= 0:
    #     if repoName not in contributors[j].login:
    #         if contributors[j].login not in contributor_list:
    #             contributor_list.append(contributors[j].login)
    #     i = i - 1
    #     j += 1
    for i in range(contributors.totalCount):
        if repoName not in contributors[i].login:
            if contributors[i].login not in contributor_list:
                contributor_list.append(contributors[i].login)

    return contributor_list


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
def get_commits_from_top_contributors(N, contributors, repo):
    commits = repo.get_commits()
    commits_dict = initialise_commits_dict(contributors)
    commits_count_dict = initialise_commits_count_dict(contributors)
    commits_list = []
    finished = False

    for i in range(commits.totalCount):
        if commits[i].author:
            if commits[i].author.login in contributors:
                if len(commits_dict[commits[i].author.login]) < N:
                    commits_dict[commits[i].author].append(commits[i])
                    if commits_finished(commits_dict, N):
                        break
    return commits_dict




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

    # contributors = get_top_n_contributors_to_repo(2, repo)
    # commits_dict = get_commits_from_top_contributors(2, conts, repo)

main()
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
