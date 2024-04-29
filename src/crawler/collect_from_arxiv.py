import arxiv
import json
import os
import time
from urllib.error import ContentTooShortError


def main():
    client = arxiv.Client()

    query = "RAG"
    if " " in query:
        query = query.replace(" ", " AND ")
    dir_path = f"../data/{query}"
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    else:
        pass

    search = arxiv.Search(
        query=query, sort_by=arxiv.SortCriterion.SubmittedDate)
    results = client.results(search)
    max_retries = 3
    retry_delay = 5
    title_summary = {}
    error_titles = []
    for r in results:
        for i in range(max_retries):
            try:
                paper_name = r.title.replace("/", " ")
                r.download_pdf(dirpath=dir_path, filename=paper_name+".pdf")
                title_summary[r.title] = r.summary
                time.sleep(3)
                break
            except ContentTooShortError:
                if i < max_retries - 1:
                    print(f"ダウンロードが不完全です。{retry_delay}秒後に再試行します")
                    time.sleep(retry_delay)
                else:
                    print("複数回のダウンロードに失敗しました")
                    error_titles.append(r.title)

    with open(f"../data/title_abst_{query}_en.json", "w") as f:
        json.dump(title_summary, f)
    with open(f"../data/error_titles_{query}.txt", "w") as f:
        f.writelines(error_titles)


if __name__ == "__main__":
    main()
