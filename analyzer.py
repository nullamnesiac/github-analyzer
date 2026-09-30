
import urllib.request
import urllib.error
import ssl
import json


def fetch_github_data(username):
    """Fetches repository data from the public GitHub API."""
    url = f"https://api.github.com/users/{username}/repos?per_page=100"
    req = urllib.request.Request(url, headers={'User-Agent': 'Python-Analyzer'})

    # Create an SSL context that bypasses the missing local macOS certificate bundle
    context = ssl._create_unverified_context()

    try:
        with urllib.request.urlopen(req, context=context) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: The user '{username}' was not found.")
        else:
            print(f"HTTP Error: {e.code}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

def analyze_repositories(repos, username):
    """Analyzes the repository data for language frequency and total stars."""
    total_stars = 0
    language_counts = {}

    for repo in repos:
        # Tally stars
        total_stars += repo.get('stargazers_count', 0)

        # Tally languages
        lang = repo.get('language')
        if lang:
            language_counts[lang] = language_counts.get(lang, 0) + 1

    # Sort languages by the number of repositories using them (descending)
    sorted_languages = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)

    # Display the results cleanly
    print(f"\n" + "=" * 40)
    print(f"📊 GITHUB STATS FOR: {username.upper()}")
    print("=" * 40)
    print(f"Total Public Repositories: {len(repos)}")
    print(f"Total Stargazers (Stars):  {total_stars}")

    print("\nTop Programming Languages Used:")
    if not sorted_languages:
        print("  No primary languages detected.")
    else:
        for lang, count in sorted_languages:
            print(f"  - {lang}: {count} repos")
    print("=" * 40 + "\n")


if __name__ == "__main__":
    print("Welcome to the Python GitHub Analyzer!")
    # Using your GitHub username as the default example
    target_user = input("Enter a GitHub username (e.g., nullamnesiac) or press Enter to quit: ").strip()

    if target_user:
        print(f"\nFetching data for '{target_user}' from the GitHub API...")
        repo_data = fetch_github_data(target_user)

        if repo_data:
            analyze_repositories(repo_data, target_user)
    else:
        print("Exiting program.")