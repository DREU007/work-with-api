from operator import itemgetter
from plotly import offline
import requests


url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f"Log:\n{'-' * 4}\nStatus code: {r.status_code}")

submission_ids = r.json()
submission_dicts = []

for submission_id in submission_ids[:30]:
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)

    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()

    try:
        submission_dict = {
            'title': response_dict['title'],
            'hn_links': f"http://news.ycombinator.com/item?id={submission_id}",
            'comments': response_dict['descendants'],
        }

    except KeyError:
        print(KeyError)
        submission_dict = {
            'title': response_dict['title'],
            'hn_links': f"http://news.ycombinator.com/item?id={submission_id}",
            'comments': 0,
        }

    submission_dicts.append(submission_dict)

submission_dicts = sorted(
    submission_dicts, key=itemgetter('comments'), reverse=True
)

for submission_dict in submission_dicts:
    print(
        f"""\nTitle: {submission_dict['title']}
Discussion link: {submission_dict['hn_links']}
Comments: {submission_dict['comments']}"""
    )

titles, num_comments, discn_links = [], [], []

for subdict in submission_dicts:
    title = subdict['title']
    hn_link = subdict['hn_links']
    titles.append(title)
    discn_links.append(f"<a href='{hn_link}'>{title:15}...</a>")
    num_comments.append(subdict['comments'])

data = [{
    'type': 'bar',
    'x': discn_links,
    'y': num_comments,
    'hovertext': titles,
    'marker': {
        'color': 'rgb(60, 100, 150)',
        'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'},
    },
    'opacity': 0.6,
}]

my_layout = {
    'title': 'Active discussion @ Hacker News',
    'titlefont': {'size': 28},
    'xaxis': {
        'title': 'Topics',
        'titlefont': {'size': 20},
        'tickfont': {'size': 8},
    },
    'yaxis': {
        'title': 'Amount of comments',
        'titlefont': {'size': 20},
        'tickfont': {'size': 14},
    },
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='hn_active_comments.html')
