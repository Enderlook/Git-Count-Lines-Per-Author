from subprocess import Popen, PIPE
from re import compile
from collections import defaultdict
from multiprocessing import Pool

def basic_process(name, email):
    user_process = Popen(f'git log --author="{name}" --pretty=tformat: --shortstat', stdout=PIPE, shell = False)
    total_insertions = total_deletions = 0
    for line_user in user_process.stdout:
        line = str(line_user)
        insert = insertions.search(line)
        if insert:
            total_insertions += int(insert.group(1))
        delete = deletions.search(line)
        if delete:
            total_deletions += int(delete.group(1))
    result = total_insertions - total_deletions
    print(f"{name} {email}: + {total_insertions} - {total_deletions} = {result}")

def advanced_process(name, email):
    user_process = Popen(f'git log --author="{name}" --pretty=tformat:"%H" --numstat --oneline', stdout=PIPE, shell = False)
    files = defaultdict(lambda: defaultdict(int))
    total_insertions = total_deletions = 0
    for line_user in user_process.stdout:
        line = line_user.decode()
        attributes = line.split("\t");
        if len(attributes) == 3 and (attributes[0] is not "-" or attributes[1] is not "-"):
            extension = attributes[2].split(".")[-1].strip()
            insertions = int(attributes[0])
            files[extension]["+"] += insertions
            total_insertions += insertions
            deletions = int(attributes[1])
            files[extension]["-"] += deletions
            total_deletions += int(attributes[1])
    print(f"{name} {email}: + {total_insertions} - {total_deletions} = {total_insertions - total_deletions}")    
    for k, v in files.items():
        print(f"\t.{k}: + {v['+']} - {v['-']} = {v['+'] - v['-']}")

def get_authors():
    main_process = Popen("git shortlog -s -n --all -e", stdout=PIPE)
    for line_user in main_process.stdout:
        line = line_user.rstrip().decode()
        yield line.split("\t")[1].rsplit(" ", 1)

def main():
    insertions = compile("(\d+) insertions?\(\+\)")
    deletions = compile("(\d+) deletions?\(\-\)")

    with Pool() as pool:
        pool.starmap(advanced_process, get_authors())

if __name__ == "__main__":
    main()
