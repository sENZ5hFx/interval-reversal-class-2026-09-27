#!/usr/bin/env python3
"""Substrate-Export Class (SEC) — iterate after IRC.

IRC owns numbers whose interval contains two worlds.
IRC cannot own a *predicate* that travels to a new substrate.
That leftover is SEC.

SEC: a predicate invented for substrate S0 is applied to substrate S1.
The remainder is neither missing data, nor a wrong constitutive sense
(SBC), nor an omitted interval (IRC). It is the predicate traveling.

Kill: if the operational definition was always substrate-neutral, this
is not export — it is the original definition applying.

Author: Haley Bird. Session 2026-09-27-irc iterate.
Research-stage. Not a physical discovery.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone

OUTDIR = os.path.dirname(os.path.abspath(__file__))
SESSION_ID = "2026-09-27-irc-sec-iterate"


@dataclass
class SecCase:
    id: str
    realm: str
    predicate: str
    s0: str
    s1: str
    operational_was_neutral: bool  # if True, kill
    signature_specific: float  # 0-1: effect specific to the named predicate
    evidence: float
    spoken: float
    prior_overlap: float
    reclaim: bool
    status: str
    source: str
    notes: str

    def score(self) -> float:
        if self.reclaim or self.operational_was_neutral or self.status in {"RETAIN", "CONTROL"}:
            return 0.0
        return round(
            40.0
            * self.signature_specific
            * self.evidence
            * (1.0 - self.spoken)
            * (1.0 - self.prior_overlap),
            4,
        )


CASES = [
    SecCase(
        id="plant_anesthesia",
        realm="land",
        predicate="anaesthetised state (of consciousness)",
        s0="brains / nervous systems",
        s1="plants without a brain (IIT Mandi, 30 Jun 2026)",
        operational_was_neutral=False,  # they exported 'consciousness' language, not just reversible unresponsiveness
        signature_specific=0.72,  # cellular reorganisation claimed as anaesthesia signature; specificity still open
        evidence=0.70,
        spoken=0.15,
        prior_overlap=0.22,  # SBC refused consciousness; this is the leftover of that refusal
        reclaim=False,
        status="UNPROVED",  # signature claimed; consciousness-export unproved
        source="IIT Mandi / PTI 30 Jun 2026: cellular signature of anaesthetised state in plants; synchronised nuclear reorganisation without a nervous system.",
        notes="Refuse 'plants are conscious'. SEC remainder: a brain-state NAME plus a cellular signature in a brainless substrate.",
    ),
    SecCase(
        id="o2_as_photosynthetic_biosignature",
        realm="space",
        predicate="atmospheric O2 as a photosynthetic biosignature",
        s0="Earth photic biosphere",
        s1="exoplanet atmospheres / crustal & groundwater O2",
        operational_was_neutral=False,
        signature_specific=0.80,
        evidence=0.88,
        spoken=0.55,
        prior_overlap=0.65,  # NASA ExEP gap 16; CIP/EFC biosignature templates; TAC crustal O2
        reclaim=False,
        status="GAP",
        source="NASA ExEP Science Gap List 2025 item 16: complete inventory of remotely observable biosignatures and false positives. Ruff groundwater dark oxygen (microbial) distinct from Sweetman nodules (CLOSED).",
        notes="Heavily overlapped with CIP/EFC. Eligible remainder: the predicate 'O2 means photosynthesis' traveling off Earth.",
    ),
    SecCase(
        id="phi_to_mycelium",
        realm="land",
        predicate="IIT phi as consciousness",
        s0="cortex",
        s1="mycelium TSP 'oracles' (Zenodo 2026)",
        operational_was_neutral=False,
        signature_specific=0.20,
        evidence=0.15,
        spoken=0.10,
        prior_overlap=0.40,
        reclaim=True,  # low-quality; do not load-bear
        status="CONTROL",
        source="Chowdhury & Kumar, Zenodo March 2026. Not peer-reviewed. Do not load-bear.",
        notes="CONTROL. Quality too low to carry SEC.",
    ),
    SecCase(
        id="h0_as_constant",
        realm="space",
        predicate="H0 is a constant of nature",
        s0="local physics",
        s1="cosmic expansion history",
        operational_was_neutral=False,
        signature_specific=0.5,
        evidence=0.9,
        spoken=0.95,
        prior_overlap=0.95,
        reclaim=True,
        status="RETAIN",
        source="Hubble tension. FAC/CIC. ZERO.",
        notes="Spoken two-clock, not substrate export.",
    ),
    SecCase(
        id="gut_cognition",
        realm="humans",
        predicate="cognition as a brain process",
        s0="cortex / CNS",
        s1="host–microbe holobiont (Frontiers Neurosci 2026)",
        operational_was_neutral=False,
        signature_specific=0.60,
        evidence=0.68,
        spoken=0.35,
        prior_overlap=0.40,  # SBC interoception; Dark Biosphere-ish
        reclaim=False,
        status="SYNTHESIS",
        source="Frontiers in Neuroscience 2026-06-03: gut microbiota as constitutive co-constructor of embodied cognition. Signaling dark matter of low-abundance molecules remains unmapped.",
        notes="Not 'the second brain' metaphor. The predicate 'who thinks' traveling into the holobiont. Consciousness still refused.",
    ),
    SecCase(
        id="anesthesia_as_unresponsiveness",
        realm="land",
        predicate="anesthesia = reversible loss of responsiveness",
        s0="animals",
        s1="plants",
        operational_was_neutral=True,  # KILL: this definition never required a brain
        signature_specific=0.5,
        evidence=0.6,
        spoken=0.1,
        prior_overlap=0.2,
        reclaim=False,
        status="CONTROL",
        source="Control for plant_anesthesia. If IIT Mandi only showed reversible unresponsiveness, SEC is wrong.",
        notes="KILL CONTROL. Operational unresponsiveness was always substrate-neutral. SEC lives only in the extra claim (consciousness / identical cellular signature).",
    ),
]


def run() -> dict:
    rows = []
    for c in CASES:
        rows.append(
            {
                "id": c.id,
                "realm": c.realm,
                "predicate": c.predicate,
                "s0": c.s0,
                "s1": c.s1,
                "score": c.score(),
                "status": c.status,
                "zeroed": c.score() == 0.0,
                "source": c.source,
                "notes": c.notes,
                "operational_was_neutral": c.operational_was_neutral,
            }
        )
    rows.sort(key=lambda r: (-r["score"], r["id"]))
    live = [r for r in rows if not r["zeroed"]]
    assert any(r["id"] == "anesthesia_as_unresponsiveness" and r["zeroed"] for r in rows)
    assert any(r["id"] == "phi_to_mycelium" and r["zeroed"] for r in rows)
    primary = live[0] if live else None
    result = {
        "session_id": SESSION_ID,
        "class_name": "Substrate-Export Class (SEC)",
        "parent_class": "Interval-Reversal Class (IRC)",
        "why_iterate": (
            "IRC cannot own plant anaesthesia or holobiont cognition: they are not numbers. "
            "SBC refused consciousness. The leftover is a predicate traveling to a new substrate."
        ),
        "class_one_liner": (
            "A predicate invented for substrate S0 is applied to substrate S1; "
            "the remainder is the predicate traveling, not missing data."
        ),
        "falsification": (
            "If the operational definition was always substrate-neutral, SEC is wrong. "
            "Control row anesthesia_as_unresponsiveness must score 0."
        ),
        "primary": primary,
        "live_ranking": live,
        "zeroed": [r["id"] for r in rows if r["zeroed"]],
        "what_is_not_claimed": [
            "Not that plants are conscious.",
            "Not that mycelium computes IIT-phi.",
            "Not that gut microbes think.",
            "Not a reclaim of SBC, IRC, TAC, or Dark Biosphere.",
        ],
        "novelty_capped": 0.33,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    stable = json.dumps({k: v for k, v in result.items() if k != "sha256"}, indent=2, sort_keys=True)
    result["sha256"] = hashlib.sha256(stable.encode()).hexdigest()
    return result


if __name__ == "__main__":
    result = run()
    path = os.path.join(OUTDIR, "sec_result.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write("\n")
    print(f"SEC iterate  {SESSION_ID}")
    print(f"SHA-256 {result['sha256']}")
    print(result["class_one_liner"])
    print("LIVE")
    for i, r in enumerate(result["live_ranking"], 1):
        print(f"  {i:02d}. {r['score']:7.2f}  {r['realm']:8s}  {r['id']}")
        print(f"       {r['predicate']}")
        print(f"       {r['s0']}  →  {r['s1']}")
    print("ZEROED", result["zeroed"])
    print("PRIMARY", result["primary"]["id"] if result["primary"] else None)
    print("wrote", path)
