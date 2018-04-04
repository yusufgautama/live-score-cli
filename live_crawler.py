#!/usr/bin/env python
"""live_crawler.py: Real time live score crawler in Command Line Interface"""
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime


def crawl(url, cookies=None):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 " \
                 "(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    headers = {'User-Agent': user_agent}
    resp = requests.get(url, headers=headers, cookies=cookies)
    return resp.content


def find_by_key(lst, key, start=0):
    for i, v in enumerate(lst):
        if key(v) and i > start:
            return i


def get_matches(url, by_nation=None, by_league=None, by_club=None):
    try:
        cookies = {'tz': '7'}
        page = crawl(url, cookies)
        page_soup = bs(page, 'html.parser')
        content = page_soup.select_one('div.content')
        rows = content.find_all('div', {'class': ['row-tall', 'row-gray']})
        flag_rows = [(_, v) for _, v in enumerate(rows)
                     if all([_ in v['class'] for _ in ['row-tall', 'mt4']])]

        match_score_obj = {}
        for i, v in flag_rows:
            left = v.select_one('div.clear > div.left')
            nation = left.select_one('a:nth-of-type(1)').text.strip()
            league = left.select_one('a:nth-of-type(2)').text.strip()
            key_group = "%s - %s" % (nation, league)

            if by_nation:
                by_nation = by_nation.replace("-", " ")
                if not any([by_nation.lower() in nation.lower(), nation.lower() in by_nation.lower()]):
                    continue

            if by_league:
                by_league = by_league.replace("-", " ")
                if not any([by_league.lower() in league.lower(), league.lower() in by_league.lower()]):
                    continue

            match_group = {'nation': nation,
                           'league': league}

            matches = []
            next_flag = find_by_key(rows, lambda x: all([_ in x['class'] for _ in ['row-tall', 'mt4']]), i + 1)
            if next_flag:
                match_data = rows[i + 1: next_flag]
            else:
                match_data = rows[i + 1:]
            for mv in match_data:
                if "row-tall" in mv['class']:
                    continue
                else:
                    status = mv.select_one('div.min').text.strip()
                    if 'Postp.' in status:
                        status = 'Postponed'
                    ply_home = mv.select_one('div[class="ply tright name"]').text.strip()
                    ply_away = mv.select_one('div[class="ply name"]').text.strip()
                    score = mv.select_one('a.scorelink') or mv.select_one('div.sco')
                    if score:
                        score = score.text.strip()
                    else:
                        score = ''
                    match = {'status': status,
                             'ply_home': ply_home,
                             'ply_away': ply_away,
                             'score': score}
                    matches.append(match)

            if by_club:
                by_club = by_club.replace("-", " ")
                # matches = [match for match in matches
                #            if any([by_club.lower() in [m.lower() for m in [match['ply_home'], match['ply_away']]]])]
                matches = [match for match in matches
                           if any([by_club.lower() in m.lower() for m in [match['ply_home'], match['ply_away']]])]

            if matches:
                match_group['matches'] = matches
                match_score_obj[key_group] = match_group
        return match_score_obj
    except Exception as e:
        traceback.print_exc()


def init_parser(parser):
    parser.add_argument('--nation', type=str, help='Show matches for specified nation, eg: england, italy')
    parser.add_argument('--league', type=str, help='Show matches for specified league, eg: serie a')
    parser.add_argument('--club', type=str, help='Show matches for specified nation, eg: juventus')
    parser.add_argument('--date', type=str, help='Show matches for specified date %Y-%m-%d format, eg: 2017-09-13')
    parser.add_argument('--all', action='store_true', help='Show all match for today')
    return parser.parse_args()


def pretty_print(match_obj):
    if not match_obj:
        print("No result")
    else:
        for k, v in match_obj.items():
            print(k.center(60, '-'))
            for m in v['matches']:
                print("{0:<6s} {1:<20s} {2:<15s} {3:<20s}".format(m['status'], m['ply_home'], m['score'], m['ply_away']))
            print("\n")


def is_valid_date(date, fmt):
    try:
        datetime.strptime(date, fmt)
    except Exception as e:
        raise Exception("Invalid date, please use %s format" % fmt)


def main():
    parser = argparse.ArgumentParser()
    args = init_parser(parser)
    date = args.date or ''
    additional_path = ''
    if date:
        is_valid_date(date, '%Y-%m-%d')
        additional_path = '/soccer/%s' % date
        args.all = True
    base_url = 'http://www.livescores.com'
    if args.all:
        url = base_url + additional_path
    else:
        url = base_url + '/soccer/live'
    match_score_obj = get_matches(url, args.nation, args.league, args.club)
    pretty_print(match_score_obj)

if __name__ == '__main__':
    import traceback
    import argparse
    main()