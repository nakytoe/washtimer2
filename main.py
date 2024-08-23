# for local dev / test 
import numpy as np
import pandas as pd
from pathlib import Path
from washtimer import porssisahko as pool
from washtimer.consumption import min_max_hours
from washtimer.page_html import get_page_html
from gitutil.gitutil import RepoUtil

GITCONFIG = "git_repo_config.yaml"

def main():

    # Clone repo, reset head
    repo = RepoUtil(config_path=GITCONFIG)
    repo.clone().reset_head_hard()
    clone_dir = repo.get_clone_dir()

    # Calculate cheapest hours
    price_df = pool.request_latest_prices()
    program = 3
    df = min_max_hours(price_df, power_hours=[program])
    begin_hours = int(df[np.logical_and(df.power_hours==program, df.minmax == "min")].hours_to_start[0])
    end_hours = begin_hours + program
    
    # Format html page
    html_content = get_page_html(begin_hours, end_hours)
    html_path = Path().cwd() / clone_dir / "index.html"
    with open(html_path, 'w') as f:
        f.write(html_content)

    # Add, commit, push
    repo.add(html_path).commit().push()

    # Remove local clone
    repo.remove_clone()

if __name__=="__main__":

    main()