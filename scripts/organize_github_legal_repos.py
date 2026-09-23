"""
APEX Holographic Mesh - GitHub Legal Repositories Organization Engine
----------------------------------------------------------------------
Categorizes, tags, and organizes all 160 legal repositories across the GlacierEQ
organization on GitHub into 8 Holographic Mesh Pillars:

  Pillar 1: Core Litigation, Federal RICO & Court Strike Engines
  Pillar 2: Broad Case Master Catalog Individual Matters (CASE-01 to CASE-69)
  Pillar 3: Cherry Chan Recovery & Asset Restitution
  Pillar 4: Hospital Fraud, EMTALA & Kekoa Child Safety
  Pillar 5: Consumer Finance, Insurance Bad Faith & USAA Repossession
  Pillar 6: Judicial Conduct & Institutional Integrity Audits
  Pillar 7: Legal AI Engines, Quantum Reasoning & Docket Automation
  Pillar 8: Legal MCP Connectors, Forensic Vaults & Research Arsenals

Epistemic Standard: L0–L5 Holographic Mesh (Byte-Level Provenance & Zero-Fake-Truth)
"""

import subprocess
import json
import time
from pathlib import Path
from collections import defaultdict

NON_LEGAL_EXCLUSIONS = {
    'job-app-helix', 'job-application', 'openrouter-free-gateway', 'activepieces',
    'anything-llm', 'apple-mcp', 'awesome-devops-mcp-servers', 'awesome-mcp-clients',
    'awesome-mcp-servers', 'jupyter-mcp-server__public_fork_archive', 'mem0',
    'command-center', 'Genius-Code', 'Genius-Mastery', 'Genius-Verification',
    'Pro-iOS', 'Pro-Memory', 'airi', 'openclaw', 'agentclaw-extension',
    'apex-telecommunications', 'apex-ish-mobile-nexus', 'claude-mcp-workspace',
    'mega-mcp', 'colossus-gateway', 'mcp-master-server'
}

PILLAR_METADATA = {
    'PILLAR_1_CORE_LITIGATION': {
        'num': 1,
        'title': 'Core Litigation, Federal Civil RICO & Court Strike Engines',
        'tags': ['core-litigation', 'case-1fdv-23-0001009', 'federal-rico', 'litigation-offensive'],
        'description': 'Flagship federal and state court filings, pleadings, strike packages, and core litigation engines.'
    },
    'PILLAR_2_CASE_CATALOG_MATTERS': {
        'num': 2,
        'title': 'Broad Case Master Catalog Individual Matters (CASE-01 to CASE-69)',
        'tags': ['broad-case-catalog', 'case-matter'],
        'description': 'Individual case dossiers, workstreams, discovery files, and litigation packets for cataloged matters.'
    },
    'PILLAR_3_CHERRY_RECOVERY': {
        'num': 3,
        'title': 'Cherry Chan Recovery & Asset Restitution Portfolio',
        'tags': ['cherry-chan-recovery', 'asset-recovery', 'restitution'],
        'description': 'Recovery of stolen assets, Nevada UI/MEUC claims, physical Camaro conversion, and banking restitution.'
    },
    'PILLAR_4_HEALTHCARE_CHILD_SAFETY': {
        'num': 4,
        'title': 'Hospital Healthcare Fraud, EMTALA & Kekoa Child Safety',
        'tags': ['healthcare-fraud', 'emtala-inquest', 'child-safety', 'pediatric-trauma'],
        'description': 'Inquests against Queen\'s Medical Center (EMTALA) and Kapiʻolani (pediatric records suppression), plus Kekoa safety.'
    },
    'PILLAR_5_CONSUMER_FINANCE_USAA': {
        'num': 5,
        'title': 'Consumer Finance, Insurance Bad Faith & USAA Repossession',
        'tags': ['consumer-finance', 'usaa-repossession', 'insurance-bad-faith', 'fdcpa'],
        'description': 'USAA wrongful repossession, insurance policy cancellation, unauthorized EFT, and debt collection challenges.'
    },
    'PILLAR_6_JUDICIAL_ETHICS_AUDIT': {
        'num': 6,
        'title': 'Judicial Conduct & Institutional Integrity Audits',
        'tags': ['judicial-conduct-audit', 'ethics-complaint', 'court-integrity'],
        'description': 'Audits of judicial decisions, conflict disclosures, Commission on Judicial Conduct complaints, and court accountability.'
    },
    'PILLAR_7_LEGAL_AI_ENGINES': {
        'num': 7,
        'title': 'Legal AI Engines, Quantum Reasoning & Docket Automation',
        'tags': ['legal-ai', 'quantum-forensics', 'docket-automation', 'brief-pipeline'],
        'description': 'Autonomous legal reasoning systems, automated docket scrapers, pleading draft engines, and adversarial matrix generators.'
    },
    'PILLAR_8_LEGAL_MCP_AND_VAULTS': {
        'num': 8,
        'title': 'Legal MCP Connectors, Forensic Vaults & Research Arsenals',
        'tags': ['legal-mcp', 'evidence-vault', 'fre-601-verified', 'legal-research'],
        'description': 'Live Model Context Protocol (MCP) servers, cryptographic evidence vaults, case law citators, and statutes databases.'
    }
}


def classify_repo(r: dict):
    name = r['name']
    if name in NON_LEGAL_EXCLUSIONS:
        return None
    desc = (r.get('description') or '').lower()
    full_str = f'{name} {desc}'.lower()
    
    # 1. Cherry Recovery
    if any(k in full_str for k in ['cherry', 'camaro', 'chr-003', 'meuc', 'nv-ui']):
        return 'PILLAR_3_CHERRY_RECOVERY'
    
    # 2. Healthcare & Child Safety
    if any(k in full_str for k in ['medical', 'hospital', 'queens', 'kapiolani', 'kekoa', 'micp', 'case-10', 'case-43', 'case-60', 'case-63', 'case-supp-queen', 'arm-injury']):
        return 'PILLAR_4_HEALTHCARE_CHILD_SAFETY'
    
    # 3. USAA & Consumer Finance
    if any(k in full_str for k in ['usaa', 'repossession', 'insurance', 'eft', 'deficiency', 'case-44', 'case-45', 'case-46', 'case-48', 'case-54', 'case-56', 'case-57', 'case-40']):
        return 'PILLAR_5_CONSUMER_FINANCE_USAA'
    
    # 4. Judicial & Ethics Audits
    if any(k in full_str for k in ['judge', 'shaw', 'naso', 'brown', 'dowd', 'judicial conduct', 'case-12', 'case-24', 'case-34', 'case-66', 'case-67', 'case-68', 'case-69', 'book-of-breach']):
        return 'PILLAR_6_JUDICIAL_ETHICS_AUDIT'
        
    # 5. Core Litigation & Strikes
    if any(k in full_str for k in ['1fdv', 'denial', 'warfare', 'cataclysm', 'beast', 'casebuilder', 'forensics-suite', 'case-homes', 'fiat-justitia', 'steamroller']):
        return 'PILLAR_1_CORE_LITIGATION'
        
    # 6. Broad Case Catalog
    if name.startswith(('CASE-', 'case-')):
        return 'PILLAR_2_CASE_CATALOG_MATTERS'
        
    # 7. Legal AI
    if any(k in full_str for k in ['solomon', 'yin', 'nexus', 'intelligence', 'powerhouse', 'xai-legal', 'quantum-legal', 'legal-ai', 'agentdevlaw', 'ai-legal', 'docket-automation', 'brief-pipeline', 'motion-automation', 'jefs-legal', 'legal-case', 'legal-ops', 'legal-brief', 'legal-aid']):
        return 'PILLAR_7_LEGAL_AI_ENGINES'
        
    # 8. Legal MCP
    if any(k in full_str for k in ['mcp', 'constellation', 'evidence', 'law-library', 'arsenal', 'forensics', 'deadline-tracker', 'email-evidence', 'supabase', 'aspen-grove-legal', 'legal-warfare', 'archEYEvist']):
        return 'PILLAR_8_LEGAL_MCP_AND_VAULTS'
        
    return None


def tag_github_repo(repo_name: str, topics: list, dry_run: bool = False) -> bool:
    if dry_run:
        print(f"[DRY-RUN] gh repo edit GlacierEQ/{repo_name} --add-topic {' --add-topic '.join(topics)}")
        return True
    
    cmd = ['gh', 'repo', 'edit', f'GlacierEQ/{repo_name}']
    for t in topics:
        cmd.extend(['--add-topic', t])
    
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if res.returncode == 0:
            return True
        else:
            print(f"Error tagging {repo_name}: {res.stderr.strip()}")
            return False
    except Exception as e:
        print(f"Exception tagging {repo_name}: {e}")
        return False


def build_organization_mesh():
    live_json_path = Path("/root/glaciereq_repos_live.json")
    if not live_json_path.exists():
        print("Live repo file missing, please fetch first.")
        return

    with open(live_json_path) as f:
        repos = json.load(f)

    print(f"Analyzing {len(repos)} repositories from GlacierEQ on GitHub...")

    classified = []
    by_pillar = defaultdict(list)

    for r in repos:
        pillar_code = classify_repo(r)
        if not pillar_code:
            continue
        
        meta = PILLAR_METADATA[pillar_code]
        target_topics = ['apex-legal', 'legal-mesh'] + meta['tags']
        existing_topics = [t['name'] for t in (r.get('repositoryTopics') or [])]
        
        entry = {
            'name': r['name'],
            'description': r.get('description') or 'Legal mesh repository.',
            'url': r['url'],
            'is_private': r.get('isPrivate', True),
            'is_archived': r.get('isArchived', False),
            'pushed_at': r.get('pushedAt'),
            'pillar_code': pillar_code,
            'pillar_num': meta['num'],
            'pillar_title': meta['title'],
            'target_topics': target_topics,
            'existing_topics': existing_topics
        }
        classified.append(entry)
        by_pillar[pillar_code].append(entry)

    print(f"Identified {len(classified)} legal repositories across 8 Pillars.")

    # 1. Save Machine-Readable Registry
    registry = {
        'status': 'VERIFIED_ORGANIZED',
        'generated_timestamp': time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        'total_legal_repositories': len(classified),
        'pillars': {}
    }

    for p_code, p_meta in PILLAR_METADATA.items():
        p_repos = by_pillar.get(p_code, [])
        registry['pillars'][p_code] = {
            'pillar_number': p_meta['num'],
            'title': p_meta['title'],
            'description': p_meta['description'],
            'repo_count': len(p_repos),
            'repositories': p_repos
        }

    registry_path = Path("/root/LEGAL_REPOSITORIES_REGISTRY.json")
    registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    print(f"Master Registry saved to: {registry_path}")

    # 2. Save Comprehensive Markdown Map
    map_lines = [
        "# APEX Holographic Mesh - Legal Repositories Organization Map",
        "**Epistemic Standard:** L0–L5 Holographic Mesh (Byte-Level Provenance & Zero-Fake-Truth)  ",
        f"**Last Synchronized:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}  ",
        f"**Total Legal Repositories:** {len(classified)} active / archived nodes  ",
        "**Organization:** [GlacierEQ (GitHub)](https://github.com/GlacierEQ)  ",
        "",
        "---",
        "",
        "## Executive Pillar Index",
        ""
    ]

    for p_code, p_meta in PILLAR_METADATA.items():
        p_repos = by_pillar.get(p_code, [])
        map_lines.append(f"- [**Pillar {p_meta['num']}: {p_meta['title']}**](#pillar-{p_meta['num']}) ({len(p_repos)} repos)")

    map_lines.append("\n---\n")

    for p_code, p_meta in PILLAR_METADATA.items():
        p_repos = by_pillar.get(p_code, [])
        map_lines.append(f"<a id=\"pillar-{p_meta['num']}\"></a>")
        map_lines.append(f"## Pillar {p_meta['num']}: {p_meta['title']}")
        map_lines.append(f"*{p_meta['description']}*\n")
        map_lines.append(f"**Total Repositories:** {len(p_repos)} | **Standard Topics:** `{'`, `'.join(['apex-legal', 'legal-mesh'] + p_meta['tags'])}`\n")
        
        map_lines.append("| Repository Name | Status | Topics | Litigation Purpose / Description |")
        map_lines.append("| :--- | :---: | :--- | :--- |")
        
        for r in sorted(p_repos, key=lambda x: x['name']):
            status_badge = "🔒 Private" if r['is_private'] else "🌐 Public"
            if r['is_archived']:
                status_badge += " (Archived)"
            topic_str = ", ".join(r['target_topics'][:3])
            desc = r['description'].replace("|", "-")
            map_lines.append(f"| [{r['name']}]({r['url']}) | {status_badge} | `{topic_str}` | {desc} |")
        
        map_lines.append("\n---\n")

    map_path = Path("/root/LEGAL_REPOSITORIES_MAP.md")
    map_path.write_text("\n".join(map_lines), encoding="utf-8")
    print(f"Master Map saved to: {map_path}")

    # 3. Synchronize Topics to GitHub Repositories
    print("\n[GITHUB TAGGING] Synchronizing topics across legal repositories on GitHub...")
    updated_count = 0
    for idx, r in enumerate(classified, 1):
        name = r['name']
        topics = r['target_topics']
        # Check if already tagged
        existing = set(r['existing_topics'])
        needed = set(topics)
        if needed.issubset(existing):
            continue
        
        success = tag_github_repo(name, topics, dry_run=False)
        if success:
            updated_count += 1
            print(f"[{idx}/{len(classified)}] ✓ Tagged GlacierEQ/{name} -> {topics}")
        else:
            print(f"[{idx}/{len(classified)}] ✗ Failed GlacierEQ/{name}")
        
        # Bounded pause to avoid GitHub API secondary rate limits
        time.sleep(0.3)

    print(f"\n[COMPLETE] Successfully tagged {updated_count} repositories on GitHub!")
    print(f"All {len(classified)} legal repositories are now indexed and mapped.")


if __name__ == "__main__":
    build_organization_mesh()
