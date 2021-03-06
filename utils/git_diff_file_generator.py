import argparse

import dateparser
import os
from git_interface import GitInterface

# the following is very helpful in understanding how the git diff format working
# http://stackoverflow.com/questions/2529441/how-to-read-the-output-from-git-diff
currentFile = None
knownFiles = {}


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--data-dir',dest='data_dir',
                        action='store',
                        type=str,
                        default='./data',
                        help="Directory in which to store the data generated from git. This will later be parsed")

    parser.add_argument('--repo_path',dest='path',
                        action='store',
                        type=str,
                        default="./repo",
                        help="path to your git repo")
    parser.add_argument('--stop_commit',dest='stop_commit',
                        action='store',
                        type=str,
                        default=None,
                        help="Commit to stop at (limits processing)")
    parser.add_argument('--branch', dest='branch',
                        action='store',
                        type=str,
                        default='master',
                        help="Branch to operate on")
    parser.add_argument('--repo-url', dest='repo_url',
                        action='store',
                        type=str,
                        default=None,
                        help="Repo URL",
                        required=True)
    args = parser.parse_args()


    if not os.path.exists(args.data_dir):
        os.mkdir(args.data_dir)

    output_dir = args.data_dir + os.sep + args.branch

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # we start parsing the git log directly
    git_if = GitInterface(args.path, args.branch)
    git_if.clone_repo(args.repo_url)
    commit_list =  git_if.get_commit_list(args.stop_commit)

    print commit_list

    for commit in commit_list:
        print commit
        commit_output =  git_if.show_commit(commit)


        for line in commit_output.split('\n'):
            print line
            if line.startswith('Date:'):
                date_str = line[5:]
                parsed_date = dateparser.parse(date_str)
                break

        filename = '%s_%s_%s_%s_%s_%s.txt' % (parsed_date.year,
                                              str(parsed_date.month).zfill(2),
                                              str(parsed_date.day).zfill(2),
                                              str(parsed_date.hour).zfill(2),
                                              str(parsed_date.minute).zfill(2),
                                              commit)
        with open(output_dir + os.sep + filename,'w') as f:
            f.write(commit_output)
    git_if.cleanup_repo()


