# .github/scripts/update_tools_inventory.py
import os
import re
import requests
from datetime import datetime
import time
import json
from typing import Dict, Tuple, Optional, List

class GithubDataFetcher:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.api_url = "https://api.github.com/repos/{owner}/{repo}"

    def get_total_contributors(self, repo_url: str) -> int:
        owner, repo = repo_url.split('/')[-2:]
        url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
        contributors = 0
        page = 1
        
        while True:
            response = requests.get(url, headers=self.headers, params={'page': page, 'per_page': 100})
            if response.status_code == 200:
                page_contributors = len(response.json())
                if page_contributors == 0:
                    break
                contributors += page_contributors
                page += 1
            elif response.status_code == 403:
                print("Rate limit exceeded. Waiting...")
                time.sleep(60)
                continue
            else:
                print(f"Error fetching contributors: {response.status_code}")
                return 0
            
            time.sleep(1)
        
        return contributors

    def get_repo_info(self, url: str) -> Tuple[str, str, str, str, str, str]:
        parts = url.strip().split("/")
        owner, repo = parts[-2], parts[-1]
        
        response = requests.get(self.api_url.format(owner=owner, repo=repo), headers=self.headers)
        
        try:
            if response.status_code == 200:
                data = response.json()
                stars = data["stargazers_count"]
                forks = data["forks_count"]
                created_at = datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y")
                contributors = self.get_total_contributors(url)
                
                # Get latest release
                releases_url = data["releases_url"].split("{")[0]
                releases_response = requests.get(releases_url, headers=self.headers)
                latest_release = "N/A"
                if releases_response.status_code == 200 and releases_response.json():
                    latest_release = datetime.strptime(
                        releases_response.json()[0]["published_at"],
                        "%Y-%m-%dT%H:%M:%SZ"
                    ).strftime("%d/%m/%Y")
                
                # Get latest commit
                commits_url = data["commits_url"].split("{")[0]
                commits_response = requests.get(commits_url, headers=self.headers, params={"per_page": 1})
                latest_commit = "N/A"
                if commits_response.status_code == 200 and commits_response.json():
                    latest_commit = datetime.strptime(
                        commits_response.json()[0]["commit"]["committer"]["date"],
                        "%Y-%m-%dT%H:%M:%SZ"
                    ).strftime("%d/%m/%Y")
                
                return stars, forks, contributors, latest_release, latest_commit, created_at
                
            return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"
            
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
            return "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"

class MarkdownUpdater:
    def __init__(self, github_token: str):
        self.fetcher = GithubDataFetcher(github_token)
        self.files_to_update = {
            '01.ingestion_and_transport.md': ['Data Replication', 'Event/Stream Processing','Log Collection and Processing', 'Change Data Capture'],
            '02.storage.md': ['File Layer', 'Metadata Layer', 'Data Modeling'],
            '03.query_and_processing.md': ['Batch Processing', 'Stream Processing', 'Query Engine', 'Dataframe Processing', 'Datawarehouse & OLAP'],
            '04.analysis_and_output.md': ['Framework', 'High-code', 'Low-code', 'No-code', 'Web Analytics'],
            '05.platform_management.md': ['Data Quality', 'Governance', 'Workflow manager', 'Automation', 'Green IT']
        }

    def extract_table_data(self, content: str, section: str) -> Tuple[List[Dict], int, int]:
        """Extrait les données d'une table markdown d'une section spécifique."""
        lines = content.split('\n')
        section_start = None
        table_start = None
        table_end = None
        
        # Trouver la section
        for i, line in enumerate(lines):
            if f"### {section}" in line:
                section_start = i
                break
        
        if section_start is None:
            return [], -1, -1
        
        # Trouver la table
        for i in range(section_start, len(lines)):
            if '|' in lines[i] and '---|' in lines[i]:
                table_start = i - 1
                break
        
        if table_start is None:
            return [], -1, -1
        
        # Trouver la fin de la table
        for i in range(table_start + 2, len(lines)):
            if not lines[i].strip().startswith('|'):
                table_end = i
                break
        
        if table_end is None:
            table_end = len(lines)
        
        # Parser les données de la table
        headers = [h.strip() for h in lines[table_start].split('|')[1:-1]]
        table_data = []
        
        for line in lines[table_start + 2:table_end]:
            if line.strip():
                values = [v.strip() for v in line.split('|')[1:-1]]
                row_data = dict(zip(headers, values))
                table_data.append(row_data)
        
        return table_data, table_start, table_end

    def update_file(self, file_path: str, sections: List[str]):
        """Met à jour un fichier markdown avec les dernières données GitHub."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            new_content = content
            for section in sections:
                table_data, table_start, table_end = self.extract_table_data(content, section)
                
                if not table_data:
                    continue
                
                # Mettre à jour les données
                for row in table_data:
                    if 'Link' in row:
                        stars, forks, contributors, latest_release, latest_commit, created_at = (
                            self.fetcher.get_repo_info(row['Link'])
                        )
                        row['Stars'] = str(stars)
                        row['Forks'] = str(forks)
                        row['Contributors'] = str(contributors)
                        row['Last Release'] = latest_release
                        row['Latest Commit'] = latest_commit
                        row['Creation Date'] = created_at
                
                # Reconstruire la table
                table_lines = []
                headers = list(table_data[0].keys())
                
                # En-tête
                table_lines.append('| ' + ' | '.join(headers) + ' |')
                table_lines.append('|' + '|'.join(['---' for _ in headers]) + '|')
                
                # Données
                for row in table_data:
                    table_lines.append('| ' + ' | '.join(str(row[h]) for h in headers) + ' |')
                
                # Remplacer l'ancienne table
                content_lines = new_content.split('\n')
                new_content = '\n'.join(content_lines[:table_start] + table_lines + content_lines[table_end:])
            
            # Sauvegarder les modifications
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            print(f"✅ {file_path} mis à jour avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour de {file_path}: {str(e)}")

    def update_all_files(self):
        """Met à jour tous les fichiers configurés."""
        for file_path, sections in self.files_to_update.items():
            self.update_file(file_path, sections)

def main():
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        raise ValueError("GitHub token non trouvé dans les variables d'environnement")
    
    updater = MarkdownUpdater(github_token)
    updater.update_all_files()

if __name__ == "__main__":
    main()