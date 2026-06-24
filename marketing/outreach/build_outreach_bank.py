#!/usr/bin/env python3
"""
Single source of truth for the Pearl/PRL Wallet grassroots-outreach response bank.

Emits three consistent artifacts into marketing/outreach/:
  1. outreach_response_bank.csv   - tabular (opens in Sheets / Excel / Numbers)
  2. outreach_response_bank.db    - SQLite database (queryable)
  3. outreach_response_bank.md    - human-readable report (strategy + per-target responses)

Why one script? So the URL, metadata, and drafted response for each opportunity
live in exactly one place and can never drift across the three formats.

NOTE on tone/ethics: every drafted response includes an honest disclosure that
the author is the developer/maintainer. This is required by Reddit's
self-promotion rules (and Bitcointalk norms), and it converts better than
covert "astroturf" posting -- which also gets accounts shadowbanned. See the
Strategy section in the generated Markdown.
"""
import csv
import sqlite3
import os
from pathlib import Path

LINK = "https://pearl-wallet-showcase.netlify.app"
VERSION = "v1.99.1331"
SHA = "e98636e984fcfff2bb71cffdd47512d6524f4047ad924fb9f58327a48ed452b3"
CANONICAL_DL = "https://prldroid-wallet.robin.mba/"

# --------------------------------------------------------------------------
# The why-it's-an-APK explanation, reused (lightly reworded) across responses
# --------------------------------------------------------------------------
WHY_APK = (
    "Heads-up on where to get it: it isn't on Google Play and won't be. "
    "Google only lets *organizations* publish crypto wallets, and as a sole-prop "
    "REALTOR-Broker who has to file every business activity with RECO (reco.on.ca), "
    "I have no intention of incorporating just to tick that box. So it ships as a "
    "directly-installed, signed APK -- info and download are at {LINK}, including "
    "the SHA256 so you can verify the file before installing."
)


def fill(s: str) -> str:
    return s.replace("{LINK}", LINK).replace("{VERSION}", VERSION).replace("{SHA}", SHA)


# --------------------------------------------------------------------------
# Opportunities. Each: url + metadata + a tailored, disclosed, non-salesy reply.
# --------------------------------------------------------------------------
OPPORTUNITIES = [
    {
        "id": "01",
        "platform": "Reddit",
        "community": "r/gpumining",
        "thread_title": "What is Pearl and why is it so profitable?",
        "url": "https://www.reddit.com/r/gpumining/comments/1tr5z34/what_is_pearl_and_why_it_is_so_profitable/",
        "angle": "self-custody + selling",
        "relevance": "Strong",
        "posting_notes": "Top thread on PRL. Reply to the self-custody sub-discussion. Keep it to one comment; answer follow-ups genuinely.",
        "response": (
            "Great breakdown -- the part most people sleep on is getting coins into your own custody fast instead of leaving them on a pool. "
            "Worth adding: until now that meant firing up the desktop wallet, which is awkward when you're away from the rig. "
            "(Full disclosure: I mine PRL and got tired of that, so I built a native Android wallet for the Pearl chain -- first one I'm aware of.) "
            "It does the basics (watch balances, sign sends, import an existing seed) plus a few things aimed at miners: keep an eye on payouts from your phone, and see the live OTC PRL/USDC rate without bouncing to a browser. "
            "Seed import is camera-based -- you point it at the phrase, it OCRs it and wipes the image immediately, so there's never a photo of your seed sitting in your gallery. "
            "{WHY_APK}".replace("{WHY_APK}", fill(WHY_APK)),
        ),
    },
    {
        "id": "02",
        "platform": "Reddit",
        "community": "r/gpumining",
        "thread_title": "Is PRL (Pearl) really the answer?",
        "url": "https://www.reddit.com/r/gpumining/comments/1u6mass/is_prl_pearl_really_the_answer/",
        "angle": "miner skepticism / custody",
        "relevance": "Strong",
        "posting_notes": "Thread is skeptical ('dead project by end of month'). Don't get defensive; validate the caution and position the wallet as a custody tool that's useful regardless of price.",
        "response": (
            "Honest take: nobody knows the longevity, so the sensible play is mining it but sweeping coins into your own custody quickly rather than letting them sit on a pool/exchange. "
            "That part's been annoying on mobile though -- the official wallet is desktop-only. "
            "(Full disclosure: I mine PRL and wanted to check balances and move coins from my phone, so I built a native Android wallet for the Pearl chain.) "
            "It's not going to make PRL moon, but it does remove the desktop dependency for day-to-day custody and sends, and it shows the live OTC rate so you can decide when to move. "
            "{WHY_APK}".replace("{WHY_APK}", fill(WHY_APK)),
        ),
    },
    {
        "id": "03",
        "platform": "Reddit",
        "community": "r/cryptomining",
        "thread_title": "Pearl Mining?!",
        "url": "https://www.reddit.com/r/cryptomining/comments/1tyn4xc/pearl_mining/",
        "angle": "profitability thinning / custody",
        "relevance": "Strong",
        "posting_notes": "General mining sub. Focus on the custody + rate-visibility angle, not price predictions.",
        "response": (
            "Margins thinning is the real signal to get serious about custody and exits rather than chasing the next spike. "
            "One gap that's been painful: there's no native mobile wallet for PRL, so checking payouts or moving coins means the desktop app. "
            "(Full disclosure: I mine PRL and built an Android wallet for the Pearl chain to fix exactly that.) "
            "Watch balances, sign sends, import an existing seed, and see the live OTC PRL/USDC rate in-app. Seed import is camera-based and the photo is wiped on the spot -- no seed phrase pictures in your gallery. "
            "{WHY_APK}".replace("{WHY_APK}", fill(WHY_APK)),
        ),
    },
    {
        "id": "04",
        "platform": "Reddit",
        "community": "r/gpumining",
        "thread_title": "Pearl miner (PRL) for Pascal GPUs -- mine Pearl with...",
        "url": "https://www.reddit.com/r/gpumining/comments/1u41c42/pearl_miner_prl_for_pascal_gpus_mine_pearl_with/",
        "angle": "tool-builder / power-user",
        "relevance": "Good",
        "posting_notes": "Audience respects people who ship tools. Frame as a peer sharing a tool, not a vendor. Compliment the Pascal miner work.",
        "response": (
            "Nice work getting Pascal cards earning on PRL -- the tooling layer for this chain is still thin, so anything that widens access helps everyone. "
            "Adding to the tool pile in case it's useful: I mine PRL and built a native Android wallet for the Pearl chain (full disclosure, I'm the dev). "
            "First native mobile wallet I've seen for PRL -- watch balances, sign sends, import an existing seed by camera (image wiped instantly, nothing lands in your gallery), plus a live OTC PRL/USDC rate. "
            "It's a signed APK, not on Play (Google requires an org to publish wallets and I'm a sole-prop REALTOR-Broker filing with RECO, so I'm not incorporating for it). Info + download + SHA256 at {LINK}.".replace("{LINK}", LINK),
        ),
    },
    {
        "id": "05",
        "platform": "Reddit",
        "community": "r/EtherMining",
        "thread_title": "Mine Pearl, Get Paid in Bitcoin! Kryptex Pool Setup Guide",
        "url": "https://www.reddit.com/r/EtherMining/comments/1txm5lb/mine_pearl_get_paid_in_bitcoin_kryptex_pool_setup/",
        "angle": "pool payouts / holding PRL vs auto-exchange",
        "relevance": "Good",
        "posting_notes": "Frame: auto-exchange to BTC is convenient, but if you'd rather hold the actual PRL you mined, you need a wallet to receive it.",
        "response": (
            "Useful guide. One thing worth flagging for people who'd rather hold the PRL they mine instead of auto-exchanging to BTC: you'll want a wallet to receive direct PRL payouts. "
            "Until recently that meant the desktop wallet. (Full disclosure: I mine PRL and built a native Android wallet for the Pearl chain.) "
            "Receive direct PRL, watch balances, sign sends, and see the live OTC rate from your phone. Seed import is camera-based and the image is wiped immediately. "
            "{WHY_APK}".replace("{WHY_APK}", fill(WHY_APK)),
        ),
    },
    {
        "id": "06",
        "platform": "Reddit",
        "community": "r/kryptex",
        "thread_title": "Pearl (PRL) mining with auto-exchange is now live!",
        "url": "https://www.reddit.com/r/kryptex/comments/1tx13i6/pearl_prl_mining_with_autoexchange_is_now_live/",
        "angle": "pool / hold-vs-swap",
        "relevance": "Good",
        "posting_notes": "Kryptex-native audience. Keep the hold-PRL option visible.",
        "response": (
            "Good to see auto-exchange live. For anyone who'd rather keep the PRL itself, you can mine to your ID and then sweep to a wallet. "
            "(Full disclosure: I built a native Android wallet for the Pearl chain because the desktop-only status was the friction.) "
            "Receives PRL, signs sends, shows the live OTC PRL/USDC rate, and imports your existing seed by camera -- photo wiped on the spot, nothing stored in your gallery. "
            "{WHY_APK}".replace("{WHY_APK}", fill(WHY_APK)),
        ),
    },
    {
        "id": "07",
        "platform": "Reddit",
        "community": "r/vastai",
        "thread_title": "vast.ai and $PRL",
        "url": "https://www.reddit.com/r/vastai/comments/1trsvxg/vastai_and_prl/",
        "angle": "compute-earners / custody",
        "relevance": "Moderate",
        "posting_notes": "Thread is cautious and disclaimer-heavy. Post only if holding PRL earned via compute is genuinely on-topic. Lower priority.",
        "response": (
            "For folks earning PRL through compute and wanting to self-custody what they earn: the gap has been no native mobile wallet. "
            "(Full disclosure: I built an Android wallet for the Pearl chain.) Watch balances, sign sends, see the live OTC rate, import a seed by camera with the image wiped instantly. "
            "Not on Play -- Google requires an org to publish wallets and I'm a sole-prop REALTOR-Broker filing with RECO, so it's a signed APK. Info + download + SHA256 at {LINK}.".replace("{LINK}", LINK),
        ),
    },
    {
        "id": "08",
        "platform": "BitcoinTalk",
        "community": "BitcoinTalk [ANN]",
        "thread_title": "[ANN] (PRL) Pearl network - Proof-of-Useful-Work L1 protocol",
        "url": "https://bitcointalk.org/index.php?topic=5584502.0",
        "angle": "ecosystem tool / dev-to-dev",
        "relevance": "Strong",
        "posting_notes": "ANN threads are the canonical home for ecosystem tools. Longer, more technical tone is fine here. Disclose dev status up front (Bitcointalk bans undisclosed alt-account promotion).",
        "response": (
            "Adding an ecosystem tool in case it's useful to the community -- full disclosure, I'm the developer.\n\n"
            "PRL Wallet for Android {VERSION}: the first native Android wallet for the Pearl chain. The official wallet has been desktop-only, which leaves mobile miners/traders relying on exchanges or firing up a PC to move coins.\n\n"
            "What it does:\n"
            "- Native PRL: watch balances, sign and broadcast sends, import an existing Pearl seed.\n"
            "- Camera-based seed import with on-the-spot image wipe -- your recovery phrase is never stored as a photo, never screenshotted, never written to the gallery.\n"
            "- Address book with labels, so you're not pasting the wrong address on a tiny screen.\n"
            "- Live OTC PRL/USDC rate pulled from lordofpearls.xyz, in-app.\n"
            "- Built on the Oyster wallet engine (ISC) via gomobile.\n\n"
            "Distribution: direct signed APK only. It is not on Google Play and won't be -- Google only permits organizations to publish crypto wallets, and as a sole-proprietor REALTOR-Broker required to file every business activity with RECO (reco.on.ca), I have no intention of incorporating just to satisfy that. The APK is release-signed; please verify the SHA256 ({SHA}) before installing.\n\n"
            "Info, screenshots, and download: {LINK}".replace("{VERSION}", VERSION).replace("{SHA}", SHA).replace("{LINK}", LINK),
        ),
    },
    {
        "id": "09",
        "platform": "BitcoinTalk",
        "community": "BitcoinTalk (mining)",
        "thread_title": "Pearl (PEARL) mining thread",
        "url": "https://bitcointalk.org/index.php?topic=5583531.0",
        "angle": "miner custody",
        "relevance": "Good",
        "posting_notes": "Miner-focused thread. Keep it shorter than the ANN post.",
        "response": (
            "For miners wanting to self-custody PRL from a phone: I built a native Android wallet for the Pearl chain (full disclosure, I'm the dev -- first native mobile wallet I've seen for PRL). "
            "Watch rig payouts, sign sends, import an existing seed by camera (image wiped instantly), and see the live OTC PRL/USDC rate. "
            "Direct signed APK, not on Play (Google requires an org to publish wallets; I'm a sole-prop REALTOR-Broker filing with RECO and won't incorporate for it). Verify the SHA256 before installing. Info + download: {LINK}.".replace("{LINK}", LINK),
        ),
    },
    {
        "id": "10",
        "platform": "Hub",
        "community": "SafeTrade (exchange) community / Discord",
        "thread_title": "PRL/USDT is the primary listed pair",
        "url": "https://safetrade.com/exchange/PRL-USDT",
        "angle": "traders / withdrawal custody",
        "relevance": "Good",
        "posting_notes": "No single thread URL. Action: join SafeTrade's Discord/community and help in the PRL withdrawal/custody questions. Use the short reusable block. Disclose dev status in your profile/intro.",
        "response": (
            "When you withdraw PRL off SafeTrade to self-custody, you currently need the desktop wallet. "
            "(Full disclosure: I built a native Android wallet for the Pearl chain.) It receives PRL, signs sends, shows the live OTC rate, and imports a seed by camera with the image wiped instantly. "
            "Direct signed APK (not on Play -- Google requires an org to publish wallets; I'm a sole-prop REALTOR-Broker filing with RECO). Info + download + SHA256: {LINK}.".replace("{LINK}", LINK),
        ),
    },
    {
        "id": "11",
        "platform": "Hub",
        "community": "GitHub Discussions (pearl-research-labs/pearl)",
        "thread_title": "Open a 'Show and tell' discussion for the Android wallet",
        "url": "https://github.com/pearl-research-labs/pearl",
        "angle": "devs / power users",
        "relevance": "Good",
        "posting_notes": "This is a *post you author*, not a reply. Use the Discussions 'Show and tell' category. Disclose dev status (it's your repo's sibling). Technical tone. Link the ISC Oyster-engine lineage.",
        "response": (
            "Show and tell: PRL Wallet for Android {VERSION} -- the first native Android wallet for the Pearl chain.\n\n"
            "Motivation: the official wallet is desktop-only, so mobile miners/traders had no native self-custody option.\n\n"
            "Highlights: native PRL send/receive + seed import; camera-based seed OCR with immediate image wipe (no seed ever stored as a photo); labeled address book; live OTC PRL/USDC rate from lordofpearls.xyz; built on the Oyster wallet engine (ISC) via gomobile.\n\n"
            "Not on Google Play (Google requires an org to publish wallets; I'm a sole-prop REALTOR-Broker filing with RECO and won't incorporate for it) -- direct signed APK. Verify SHA256 ({SHA}). Info + download: {LINK}".replace("{VERSION}", VERSION).replace("{SHA}", SHA).replace("{LINK}", LINK),
        ),
    },
    {
        "id": "12",
        "platform": "Hub",
        "community": "X / Twitter (@prlnet and OTC posters)",
        "thread_title": "Reply to wallet/mining/OTC posts from @prlnet and OTC rate posters",
        "url": "https://x.com/prlnet",
        "angle": "OTC visibility / awareness",
        "relevance": "Moderate",
        "posting_notes": "Reply (don't cold-DM) to posts about PRL wallets/mining/OTC. Disclose 'I built this'. Keep to ~280 chars + a reply thread. Low-pressure.",
        "response": (
            "If you're moving PRL around and the desktop-only wallet is the friction: I built a native Android wallet for the Pearl chain (full disclosure, dev). Live OTC rate in-app, camera seed import that wipes the photo, signed APK (not on Play -- Google needs an org; I'm a sole-prop REALTOR-Broker filing with RECO). {LINK}".replace("{LINK}", LINK),
        ),
    },
]

# Apply any remaining {placeholders}. (Some response literals are 1-tuples due
# to a trailing comma after the inline .replace(...) -- join them back to a str.)
for o in OPPORTUNITIES:
    r = o["response"]
    if isinstance(r, tuple):
        r = "".join(r)
    o["response"] = fill(r)

# --------------------------------------------------------------------------
# Strategy / compliance sections (Markdown report only)
# --------------------------------------------------------------------------
DISCLAIMER_NOTE = (
    "Every drafted reply above includes an explicit 'full disclosure, I'm the dev' line. "
    "That is deliberate and is doing real work for you, not just ethics:\n"
    "- **Reddit's self-promotion rules** (and the de-facto 9:1 participation ratio) require "
    "disclosure of affiliation; undisclosed self-promotion is the fastest way to get "
    "shadowbanned or post-removed across r/gpumining, r/cryptomining, r/EtherMining.\n"
    "- **Bitcointalk** bans undisclosed alt-account / signature-campaign-style shilling; "
    "ANN-thread regulars spot it instantly and it damages credibility permanently.\n"
    "- It **converts better**. In mining/crypto communities, 'I built this because I had the "
    "same problem' earns trust; pretending to be a random fan gets sniffed out and backfires.\n\n"
    "Before posting anywhere: spend a few minutes being a genuine participant in that sub first "
    "(answer a question, upvote good content). Then your single tool-related comment lands as "
    "a community member, not a drive-by promoter."
)

OYSTER_WARNING = (
    "**Critical disambiguation -- do NOT engage these threads.** "
    "There is an older, *unrelated* token also tickered **PRL: the 2018 'Oyster Pearl'** "
    "(a file-storage ERC-20 that was exploited/abandoned). It is a completely different project "
    "from the current **Pearl Proof-of-Useful-Work L1** (pearl-research-labs) that this wallet serves. "
    "Example thread to avoid: r/CryptoCurrency 'DO NOT BUY OYSTER PEARL (PRL), THE SMART CONTRACT...' "
    "(https://www.reddit.com/r/CryptoCurrency/comments/9sg08h/). Posting a Pearl-chain wallet there "
    "would read as a scam and confuse people. Only engage threads that are clearly about the "
    "current AI-compute Pearl network (mining via GPU matrix mult, SafeTrade listing, lordofpearls OTC)."
)

SIDELOAD_NOTE = (
    "Because the wallet is a sideloaded APK, the #1 reaction you'll get is "
    "'is this safe / why isn't it on Play?'. Lean into it:\n"
    "- Always mention the **release signature + SHA256** ({SHA}) and tell people to verify before "
    "installing. That single habit flips the trust question from 'random APK' to 'verifiable artifact.'\n"
    "- The Google/organization + RECO explanation is your honest answer to 'why not Play Store?' -- "
    "keep it crisp (one or two sentences). It reads as principled, not evasive.\n"
    "- You can optionally lead with the human angle ('I'm a realtor by day, PRL miner by night') "
    "for warmth; it reinforces the sole-prop / no-org story naturally."
).replace("{SHA}", SHA)

FRESHNESS_NOTE = (
    "Only reply to **currently-active** threads. The PRL mining rush is recent (2026), so the "
    "threads above are likely live, but before you post: open the URL, confirm the thread isn't "
    "archived/locked, and prefer threads with activity in the last ~30-60 days. A reply to a "
    "6-month-old dead thread helps no one and looks like spam. Do **not** paste the identical text "
    "into multiple subs -- rewrite the opener each time (the drafts above are already varied) so "
    "automated spam filters don't link your posts."
)

LINK_NOTE = (
    "All drafts point people to **{LINK}** as you asked. Note for your own bookkeeping: the "
    "canonical signed-APK download origin in the release manifest is **{CANON}** "
    "(pearl-wallet-android v{VERSION}, SHA256 {SHA}). If the showcase site is the friendly front "
    "door and the canonical domain hosts the raw artifact, that's a clean split -- just make sure "
    "the showcase's download button resolves to the verifiable signed APK."
).replace("{LINK}", LINK).replace("{CANON}", CANONICAL_DL).replace("{VERSION}", VERSION).replace("{SHA}", SHA)

# --------------------------------------------------------------------------
# Emitters
# --------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent

def emit_csv():
    path = HERE / "outreach_response_bank.csv"
    cols = ["id", "platform", "community", "thread_title", "url", "angle",
            "relevance", "posting_notes", "response"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_ALL)
        w.writeheader()
        for o in OPPORTUNITIES:
            w.writerow({k: o.get(k, "") for k in cols})
    return path

def emit_sqlite():
    path = HERE / "outreach_response_bank.db"
    if path.exists():
        path.unlink()
    con = sqlite3.connect(path)
    con.execute(
        """CREATE TABLE opportunities (
            id TEXT PRIMARY KEY,
            platform TEXT,
            community TEXT,
            thread_title TEXT,
            url TEXT,
            angle TEXT,
            relevance TEXT,
            posting_notes TEXT,
            response TEXT
        )"""
    )
    con.executemany(
        """INSERT INTO opportunities
           (id,platform,community,thread_title,url,angle,relevance,posting_notes,response)
           VALUES (:id,:platform,:community,:thread_title,:url,:angle,:relevance,:posting_notes,:response)""",
        OPPORTUNITIES,
    )
    con.commit()
    con.close()
    return path

def emit_markdown(csv_path, db_path):
    path = HERE / "outreach_response_bank.md"
    n = len(OPPORTUNITIES)
    L = []
    L.append("# Pearl/PRL Wallet -- Grassroots Outreach Response Bank\n")
    L.append(f"**Product:** PRL Wallet for Android (v{VERSION}) -- the first native Android wallet ")
    L.append("for the Pearl (PRL) Proof-of-Useful-Work L1 blockchain. Monitor rigs, move PRL, see live OTC rates.\n")
    L.append(f"**Showcase / download:** {LINK}  |  **Canonical APK origin:** {CANONICAL_DL}  |  ")
    L.append(f"**SHA256:** `{SHA}`\n")
    L.append(f"**Targets in this bank:** {n}  |  ")
    L.append("Formats: `outreach_response_bank.csv` (tabular) + `outreach_response_bank.db` (SQLite)\n")
    L.append("---\n")

    L.append("## How to read this\n")
    L.append("Each target has a real URL and a ready-to-adapt reply. Replies are written to be **personal, ")
    L.append("not salesy, and honest** -- each discloses that the author is the developer. Read the ")
    L.append("Strategy section before posting anything.\n")

    L.append("## Strategy & compliance (read first)\n")
    L.append("### 1. Disclosure -- non-negotiable, and it helps you\n")
    L.append(DISCLAIMER_NOTE + "\n")
    L.append("### 2. Oyster PRL disambiguation -- avoid these\n")
    L.append(OYSTER_WARNING + "\n")
    L.append("### 3. Sideload safety = your trust story\n")
    L.append(SIDELOAD_NOTE + "\n")
    L.append("### 4. Thread freshness + anti-spam\n")
    L.append(FRESHNESS_NOTE + "\n")
    L.append("### 5. Link / download plumbing\n")
    L.append(LINK_NOTE + "\n")

    L.append("## Reusable core block\n")
    L.append("Paste/adapt this as the closing of any reply where you need the why-APK explanation:\n")
    L.append("> " + fill(WHY_APK).replace("\n", "\n> ") + "\n")

    L.append("## Opportunity table\n")
    L.append("| # | Platform | Community | Angle | Relevance | URL |")
    L.append("|---|----------|-----------|-------|-----------|-----|")
    for o in OPPORTUNITIES:
        title = o["thread_title"]
        L.append(f"| {o['id']} | {o['platform']} | {o['community']} | {o['angle']} | {o['relevance']} | [{title}]({o['url']}) |")
    L.append("")

    L.append("## Drafted responses (one per target)\n")
    for o in OPPORTUNITIES:
        L.append(f"### {o['id']}. {o['platform']} -- {o['community']}")
        L.append(f"**Thread:** [{o['thread_title']}]({o['url']})  ")
        L.append(f"**Angle:** {o['angle']}  |  **Relevance:** {o['relevance']}\n")
        L.append(f"*Posting notes:* {o['posting_notes']}\n")
        L.append("**Drafted reply:**\n")
        L.append("> " + o["response"].replace("\n", "\n> ") + "\n")
        L.append("---\n")

    L.append("## Files\n")
    L.append(f"- `{csv_path.name}` -- open in Sheets/Excel; columns: id, platform, community, ")
    L.append("thread_title, url, angle, relevance, posting_notes, response.\n")
    L.append(f"- `{db_path.name}` -- SQLite; table `opportunities`, same columns. Query e.g. ")
    L.append("`sqlite3 outreach_response_bank.db \"SELECT id, community, url FROM opportunities WHERE relevance='Strong';\"`\n")
    L.append("- `build_outreach_bank.py` -- this bank's source of truth; edit responses here and re-run ")
    L.append("to regenerate all three files in sync.\n")

    path.write_text("\n".join(L), encoding="utf-8")
    return path

def main():
    csv_path = emit_csv()
    db_path = emit_sqlite()
    md_path = emit_markdown(csv_path, db_path)
    print("WROTE:")
    for p in (csv_path, db_path, md_path):
        print(f"  {p}  ({p.stat().st_size} bytes)")
    print(f"\nRows: {len(OPPORTUNITIES)}")

if __name__ == "__main__":
    main()
