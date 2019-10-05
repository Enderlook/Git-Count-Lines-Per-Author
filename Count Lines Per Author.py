import subprocess, re
from collections import defaultdict

def basic_process(user):
    user_process = subprocess.Popen(f'git log --author="{user}" --pretty=tformat: --shortstat', stdout=subprocess.PIPE, shell = False)
    total_insertions = 0
    total_deletions = 0
    for line_user in user_process.stdout:
        line = str(line_user)
        insert = insertions.search(line)
        if insert:
            total_insertions += int(insert.group(1))
        delete = deletions.search(line)
        if delete:
            total_deletions += int(delete.group(1))
    result = total_insertions - total_deletions
    print(f"{user}: + {total_insertions} - {total_deletions} = {result}")

def advanced_process(user):
    user_process = subprocess.Popen(f'git log --author="{user}" --pretty=tformat:"%H" --numstat --oneline', stdout=subprocess.PIPE, shell = False)
    files = defaultdict(lambda: defaultdict(int))
    for line_user in user_process.stdout:
        line = line_user.decode()
        attributes = line.split("\t");
        if len(attributes) == 3 and (attributes[0] is not "-" or attributes[1] is not "-"):
            extension = attributes[2].split(".")[-1].strip()
            files[extension]["+"] += int(attributes[0])
            files[extension]["-"] += int(attributes[1])
    print(user + ":")
    for k, v in files.items():
        print(f"\t.{k}: + {v['+']} - {v['-']} = {v['+'] - v['-']}")

def get_authors():
    main_process = subprocess.Popen("git shortlog -s -n --all", stdout=subprocess.PIPE)
    for line_user in main_process.stdout:
        line = line_user.rstrip()
        yield line.split(b"\t")[1].decode()

if __name__ == "__main__":
    insertions = re.compile("(\d+) insertions?\(\+\)")
    deletions = re.compile("(\d+) deletions?\(\-\)")
    
    main_process = subprocess.Popen("git shortlog -s -n --all", stdout=subprocess.PIPE)

    for author in get_authors():
        advanced_process(author)
