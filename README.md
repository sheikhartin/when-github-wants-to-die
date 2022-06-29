## When GitHub Wants to Die

![GitHub repo status](https://img.shields.io/badge/status-active-green?style=flat)
![GitHub license](https://img.shields.io/github/license/sheikhartin/when-github-wants-to-die)
![GitHub contributors](https://img.shields.io/github/contributors/sheikhartin/when-github-wants-to-die)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/sheikhartin/when-github-wants-to-die)
![GitHub repo size](https://img.shields.io/github/repo-size/sheikhartin/when-github-wants-to-die)

GitHub is a platform for collaborating on code. It's a place to share code, to discuss ideas, and to help each other. Millions of people use GitHub to build their projects, and collaborating with others.

However, this small project saved you from possible disasters that may befall GitHub or even vice versa. For example, respectable governments may not want sanctioned countries to have programmers!

Some links that may help you understand the situation:

- [Microsoft to Acquire GitHub for $7.5 Billion](https://news.microsoft.com/2018/06/04/microsoft-to-acquire-github-for-7-5-billion/)
- [GitHub and Trade Controls](https://docs.github.com/en/site-policy/other-site-policies/github-and-trade-controls)
- [GitHub Confirms it has Blocked Developers in Iran, Syria and Crimea](https://techcrunch.com/2019/07/29/github-ban-sanctioned-countries/)
<!-- - [GitHub vs GitLab vs Bitbucket](https://jelvix.com/blog/bitbucket-vs-github-vs-gitlab) -->

![Not to the death of GitHub](https://media.giphy.com/media/59bo7PVAiXHV59QCFG/giphy.gif)

### Usage

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Clone all the repositories and gists in a account:

```bash
python core.py "sheikhartin"
```

<!-- <i>Note: The script puts the repositories and gists in the current directory.</i> -->

Only some special repositories:

```bash
python core.py "microsoft" -r "data-science-for-beginners" "ml-for-beginners"
```

Clone a specific branch:

```bash
python core.py "openai" -r "gym@benchmark"
```

Download gists by their IDs:

```bash
python core.py "roachhd" -g "dce54bec8ba55fb17d3a"
```

Suppress the output:

```bash
python core.py "google" -q
```

<i>Note: When faced with a large number of repositories in one account, the program selects the top 100 based on the stars... Unfortunately, the GitHub API does not work well with this feature yet!</i>

### License

This project is licensed under the MIT license found in the [LICENSE](LICENSE) file in the root directory of this repository.
