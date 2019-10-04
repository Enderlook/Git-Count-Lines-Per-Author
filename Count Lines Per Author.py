import subprocess, re

insertions = re.compile("(\d+) insertions?\(\+\)")
deletions = re.compile("(\d+) deletions?\(\-\)")

main_process = subprocess.Popen("git shortlog -s -n --all", stdout=subprocess.PIPE)

for line_user in main_process.stdout:
    line = line_user.rstrip()
    user = line.split(b"\t")[1].decode("utf-8")
    
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
