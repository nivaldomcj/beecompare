from bs4 import BeautifulSoup
import requests
import sys
import csv
import time


def get_next_url(base_url, soup):
    next_url = soup.find("div", id="table-paging").ul.find("li", class_="next").a["href"]
    return base_url + next_url if next_url else None


def is_problem(item):
    return item.find("td", class_="id") or item.find("td", class_="wide")


def solved_from(user_code):
    solved_problems = set()

    base_url = "https://beecrowd.com.br"
    next_url = "{}/judge/pt/profile/{}".format(base_url, user_code)

    while next_url is not None:
        print("[DEBUG] (User {}) Fetching URL: {}".format(user_code, next_url))

        html = requests.get(next_url).text
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("div", class_="list").tbody.find_all("tr")

        for item in table:
            if is_problem(item):
                print("[DEBUG] (User {}) Found a problem solved. Trying to parse it...".format(user_code))
                problem_code = item.find("td", class_="id").a.text
                problem_name = item.find("td", class_="wide").a.text
                problem_link = "{}{}".format(base_url, item.find("td", class_="wide").a["href"])

                print("[DEBUG] (User {}) Adding problem {}".format(user_code, problem_code))
                solved_problems.add((problem_code, problem_name, problem_link))

        next_url = get_next_url(base_url, soup)

        # avoid being banned because of scraping
        print("[DEBUG] I will sleep for a while, so they cannot catch me! =]")
        time.sleep(2)


    return solved_problems


def compare(user_codes):
    problems = [solved_from(user_codes[0]), solved_from(user_codes[1])]
    return [problems[1].difference(problems[0]), problems[0].difference(problems[1])]


def username(user_code):
    html = requests.get("https://www.urionlinejudge.com.br/judge/pt/profile/{}".format(user_code)).text
    soup = BeautifulSoup(html, "html.parser")

    return soup.find("p", itemprop="name").text.encode("utf-8").strip().decode("utf-8")


def save(user_names, problems):
    print("[DEBUG] Saving problems from ({})".format(user_names))

    with open("UOJ - {} vs {}.csv".format(user_names[0], user_names[1]), "w", newline="") as file:
        writer = csv.writer(file, delimiter=',', quotechar='"')

        _ = writer.writerow(("Problem Code", "Problem Name", "Problem Link"))
        _ = [writer.writerow((item[0], item[1], item[2])) for item in problems]
    
    print("[DEBUG] Saved files! My job here is done.")


def main(user_codes):
    print("[DEBUG] Ok, here we go. You have set {} and {} User Codes.".format(user_codes[0], user_codes[1]))

    problems = compare(user_codes)
    usernames = [username(user_codes[0]), username(user_codes[1])]

    save([usernames[0], usernames[1]], problems[1])
    save([usernames[1], usernames[0]], problems[0])

    print("[DEBUG] ~~Flies away")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main((sys.argv[1], sys.argv[2]))
