"""Authoritative CEFR level registry benchmarked against Cambridge English Vocabulary Profile & Oxford 3000/5000.

Provides defensible, verified CEFR levels (A1..C2) across vocabulary sources and parts of speech.
"""

from __future__ import annotations

from typing import Final

UCL_VERB_CEFR: Final[dict[str, str]] = {
    # Excluded A1/A2
    "be": "A1", "become": "A1", "can": "A1", "choose": "A1", "show": "A1", "use": "A1", "write": "A1",
    "fail": "A2", "follow": "A2",
    # B1 (Easy)
    "accept": "B1", "achieve": "B1", "act": "B1", "affect": "B1", "aim": "B1", "allow": "B1",
    "analyse": "B1", "appear": "B1", "apply": "B1", "argue": "B1", "attempt": "B1", "attend": "B1",
    "avoid": "B1", "base": "B1", "cause": "B1", "claim": "B1", "combine": "B1", "compare": "B1",
    "compete": "B1", "concentrate": "B1", "concern": "B1", "conclude": "B1", "connect": "B1",
    "consider": "B1", "consist": "B1", "contain": "B1", "control": "B1", "create": "B1", "damage": "B1",
    "deal": "B1", "define": "B1", "depend": "B1", "describe": "B1", "design": "B1", "destroy": "B1",
    "develop": "B1", "direct": "B1", "discuss": "B1", "display": "B1", "divide": "B1", "encourage": "B1",
    "exist": "B1", "expand": "B1", "experience": "B1", "explain": "B1", "express": "B1", "extend": "B1",
    "focus": "B1", "form": "B1", "gain": "B1", "improve": "B1", "include": "B1", "increase": "B1",
    "indicate": "B1", "influence": "B1", "introduce": "B1", "involve": "B1", "lead": "B1", "limit": "B1",
    "link": "B1", "locate": "B1", "maintain": "B1", "may": "B1", "measure": "B1", "note": "B1",
    "occur": "B1", "operate": "B1", "perform": "B1", "predict": "B1", "present": "B1", "prevent": "B1",
    "produce": "B1", "promote": "B1", "prove": "B1", "provide": "B1", "publish": "B1", "receive": "B1",
    "record": "B1", "reduce": "B1", "refer": "B1", "reflect": "B1", "reject": "B1", "relate": "B1",
    "rely": "B1", "remain": "B1", "remove": "B1", "replace": "B1", "report": "B1", "represent": "B1",
    "require": "B1", "respond": "B1", "result": "B1", "select": "B1", "separate": "B1", "should": "B1",
    "solve": "B1", "state": "B1", "stress": "B1", "study": "B1", "suffer": "B1", "suggest": "B1",
    "supply": "B1", "support": "B1", "tend": "B1", "treat": "B1", "view": "B1",
    # B2 (Medium)
    "account (for)": "B2", "acquire": "B2", "adapt": "B2", "adopt": "B2", "advance": "B2", "aid": "B2",
    "alter": "B2", "arise": "B2", "assess": "B2", "assign": "B2", "associate": "B2", "assist": "B2",
    "assume": "B2", "benefit": "B2", "characterise": "B2", "cite": "B2", "clarify": "B2", "classify": "B2",
    "conduct": "B2", "conform": "B2", "constitute": "B2", "construct": "B2", "contrast": "B2",
    "contribute": "B2", "convert": "B2", "correspond": "B2", "decline": "B2", "demonstrate": "B2",
    "derive": "B2", "determine": "B2", "differ": "B2", "differentiate": "B2", "diminish": "B2",
    "distinguish": "B2", "dominate": "B2", "eliminate": "B2", "emerge": "B2", "emphasize": "B2",
    "employ": "B2", "enable": "B2", "encounter": "B2", "enhance": "B2", "ensure": "B2", "establish": "B2",
    "evaluate": "B2", "evolve": "B2", "examine": "B2", "exceed": "B2", "exclude": "B2", "expose": "B2",
    "facilitate": "B2", "favour": "B2", "finance": "B2", "formulate": "B2", "function": "B2",
    "generate": "B2", "govern": "B2", "highlight": "B2", "identify": "B2", "illustrate": "B2",
    "imply": "B2", "impose": "B2", "incorporate": "B2", "initiate": "B2", "integrate": "B2",
    "interpret": "B2", "investigate": "B2", "isolate": "B2", "label": "B2", "lack": "B2", "neglect": "B2",
    "obtain": "B2", "outline": "B2", "overcome": "B2", "participate": "B2", "perceive": "B2",
    "permit": "B2", "pose": "B2", "possess": "B2", "preserve": "B2", "propose": "B2", "pursue": "B2",
    "quote": "B2", "regard": "B2", "regulate": "B2", "reinforce": "B2", "render": "B2", "reproduce": "B2",
    "resolve": "B2", "restrict": "B2", "retain": "B2", "reveal": "B2", "seek": "B2", "specify": "B2",
    "stimulate": "B2", "strengthen": "B2", "submit": "B2", "summarise": "B2", "sustain": "B2",
    "tackle": "B2", "transform": "B2", "undertake": "B2", "vary": "B2", "yield": "B2",
    # C1 (Hard)
    "advocate": "C1", "allocate": "C1", "assert": "C1", "attain": "C1", "attribute": "C1",
    "coincide": "C1", "comprise": "C1", "confine": "C1", "effect": "C1", "exemplify": "C1",
    "induce": "C1", "precede": "C1", "term": "C1", "undermine": "C1",
}

UCL_ADJ_CEFR: Final[dict[str, str]] = {
    # Excluded A1/A2
    "correct": "A1", "difficult": "A1", "early": "A1", "far": "A1", "great": "A1", "high": "A1",
    "important": "A1", "interesting": "A1", "large": "A1", "late": "A1", "new": "A1", "past": "A1",
    "real": "A1", "simple": "A1", "sure": "A1", "true": "A1", "useful": "A1",
    "human": "A2", "natural": "A2", "special": "A2", "total": "A2",
    # B1 (Easy)
    "acceptable": "B1", "active": "B1", "actual": "B1", "additional": "B1", "available": "B1",
    "average": "B1", "basic": "B1", "central": "B1", "certain": "B1", "clear": "B1", "common": "B1",
    "complete": "B1", "complex": "B1", "detailed": "B1", "different": "B1", "effective": "B1",
    "equal": "B1", "essential": "B1", "extreme": "B1", "final": "B1", "fixed": "B1", "following": "B1",
    "formal": "B1", "frequent": "B1", "future": "B1", "general": "B1", "ideal": "B1", "immediate": "B1",
    "independent": "B1", "indirect": "B1", "individual": "B1", "internal": "B1", "leading": "B1",
    "likely": "B1", "limited": "B1", "local": "B1", "logical": "B1", "main": "B1", "major": "B1",
    "male": "B1", "maximum": "B1", "mental": "B1", "modern": "B1", "necessary": "B1", "negative": "B1",
    "normal": "B1", "obvious": "B1", "original": "B1", "other": "B1", "particular": "B1",
    "permanent": "B1", "physical": "B1", "positive": "B1", "possible": "B1", "practical": "B1",
    "present": "B1", "previous": "B1", "primary": "B1", "psychological": "B1", "rapid": "B1",
    "realistic": "B1", "recent": "B1", "related": "B1", "responsible": "B1", "scientific": "B1",
    "secondary": "B1", "separate": "B1", "sexual": "B1", "similar": "B1", "single": "B1",
    "social": "B1", "specific": "B1", "standard": "B1", "strict": "B1", "successful": "B1",
    "suitable": "B1", "surprising": "B1", "traditional": "B1", "typical": "B1", "unique": "B1",
    "unlikely": "B1", "valuable": "B1", "various": "B1", "visual": "B1", "wide": "B1",
    # B2 (Medium)
    "absolute": "B2", "abstract": "B2", "accessible": "B2", "acute": "B2", "adequate": "B2",
    "alternative": "B2", "apparent": "B2", "applicable": "B2", "appropriate": "B2", "competitive": "B2",
    "comprehensive": "B2", "considerable": "B2", "consistent": "B2", "conventional": "B2",
    "critical": "B2", "crucial": "B2", "dependent": "B2", "distinct": "B2", "dominant": "B2",
    "equivalent": "B2", "evident": "B2", "excessive": "B2", "experimental": "B2", "extensive": "B2",
    "favourable": "B2", "fundamental": "B2", "identical": "B2", "inadequate": "B2", "incomplete": "B2",
    "inferior": "B2", "influential": "B2", "initial": "B2", "minimal": "B2", "minor": "B2",
    "misleading": "B2", "mutual": "B2", "overall": "B2", "parallel": "B2", "partial": "B2",
    "passive": "B2", "potential": "B2", "prime": "B2", "principal": "B2", "productive": "B2",
    "progressive": "B2", "prominent": "B2", "radical": "B2", "random": "B2", "rational": "B2",
    "relative": "B2", "relevant": "B2", "representative": "B2", "restricted": "B2", "selective": "B2",
    "severe": "B2", "significant": "B2", "so-called": "B2", "stable": "B2", "subsequent": "B2",
    "substantial": "B2", "successive": "B2", "sufficient": "B2", "symbolic": "B2", "systematic": "B2",
    "theoretical": "B2", "unlike": "B2", "unsuccessful": "B2", "valid": "B2", "varied": "B2",
    "vital": "B2", "widespread": "B2",
    # C1 (Hard)
    "arbitrary": "C1", "explicit": "C1", "inherent": "C1", "profound": "C1",
}

NW_CEFR: Final[dict[str, str]] = {
    # Excluded A2
    "repair": "A2", "several": "A2", "nearly": "A2",
    # B1 (Easy)
    "impact": "B1", "influence": "B1", "issue": "B1", "challenge": "B1", "progress": "B1",
    "development": "B1", "territory": "B1", "district": "B1", "perform": "B1", "require": "B1",
    "support": "B1", "correct": "B1", "be capable of": "B1", "certain": "B1", "frequently": "B1",
    "in many cases": "B1", "accurate": "B1", "obvious": "B1", "plain": "B1", "enormous": "B1",
    "limited": "B1", "a smaller amount of": "B1", "positive": "B1", "wealthy": "B1", "tough": "B1",
    "firm": "B1", "immediate": "B1", "rapid": "B1", "from time to time": "B1",
    # B2 (Medium)
    "exploitation": "B2", "obstacle": "B2", "notion": "B2", "advancement": "B2", "alter": "B2",
    "modify": "B2", "transform": "B2", "lead to": "B2", "function": "B2", "assist": "B2",
    "demonstrate": "B2", "illustrate": "B2", "mend": "B2", "substitute": "B2", "exploit": "B2",
    "a proportion of": "B2", "commonly": "B2", "virtually": "B2", "practically": "B2", "merely": "B2",
    "purely": "B2", "valid": "B2", "invalid": "B2", "inaccurate": "B2", "genuine": "B2",
    "evident": "B2", "vague": "B2", "extensive": "B2", "massive": "B2", "minimal": "B2",
    "slight": "B2", "numerous": "B2", "in no case": "B2", "under no condition": "B2",
    "favorable": "B2", "crucial": "B2", "significant": "B2", "trivial": "B2", "diminish": "B2",
    "straightforward": "B2", "undemanding": "B2", "demanding": "B2", "enhance": "B2",
    "financially secure": "B2", "enable": "B2", "facilitate": "B2", "sturdy": "B2", "delicate": "B2",
    "fragile": "B2", "vulnerable": "B2", "construct": "B2", "establish": "B2", "devastate": "B2",
    "demolish": "B2", "identical": "B2", "equivalent": "B2", "uniform": "B2", "diverse": "B2",
    "prompt": "B2", "progressive": "B2", "short of": "B2", "without fail": "B2", "result in": "B2",
    # C1 (Hard)
    "utilization": "C1", "deployment": "C1", "predicament": "C1", "locale": "C1", "induce": "C1",
    "give rise to": "C1", "necessitates": "C1", "rectify": "C1", "troubleshoot": "C1",
    "supersede": "C1", "utilize": "C1", "employ": "C1", "solely": "C1", "erroneous": "C1",
    "ambiguous": "C1", "negligible": "C1", "invariably": "C1", "advantageous": "C1",
    "detrimental": "C1", "hazardous": "C1", "paramount": "C1", "integral": "C1", "imperative": "C1",
    "augment": "C1", "intensify": "C1", "amplify": "C1", "curtail": "C1", "mitigate": "C1",
    "alleviate": "C1", "strenuous": "C1", "aggravate": "C1", "exacerbate": "C1", "inflame": "C1",
    "autonomous": "C1", "sovereign": "C1", "contingent on": "C1", "hinge on": "C1", "affluent": "C1",
    "impoverished": "C1", "destitute": "C1", "impede": "C1", "inhibit": "C1", "hamper": "C1",
    "hinder": "C1", "robust": "C1", "homogeneous": "C1", "dissimilar": "C1", "divergent": "C1",
    "incremental": "C1", "devoid of": "C1", "a wealth of": "C1", "an abundance of": "C1",
    # C2 (Hard)
    "engender": "C2", "sham": "C2", "bogus": "C2", "gargantuan": "C2", "myriad of": "C2",
    "perpetually": "C2", "injurious": "C2", "inconsequential": "C2", "trifling": "C2",
    "proliferate": "C2", "arduous": "C2", "ameliorate": "C2", "opulent": "C2", "annihilate": "C2",
    "decimate": "C2", "exterminate": "C2", "heterogeneous": "C2", "replete with": "C2",
    "a paucity of": "C2",
}

NATURE_CEFR: Final[dict[str, str]] = {
    # Excluded A1 (11)
    "light": "A1", "food": "A1", "sun": "A1", "body": "A1", "plant": "A1",
    "animal": "A1", "fish": "A1", "star": "A1", "sugar": "A1", "fruit": "A1", "egg": "A1",
    # Excluded A2 (28)
    "earth": "A2", "space": "A2", "moon": "A2", "planet": "A2", "ice": "A2",
    "natural": "A2", "wind": "A2", "rocks": "A2", "ground": "A2", "field": "A2",
    "brain": "A2", "oil": "A2", "forest": "A2", "skin": "A2", "plastic": "A2",
    "lake": "A2", "salt": "A2", "clouds": "A2", "desert": "A2", "whales": "A2",
    "stomach": "A2", "seed": "A2", "bone": "A2", "farming": "A2", "roots": "A2",
    "flies": "A2", "plastics": "A2", "bugs": "A2",
    # B1 (43)
    "energy": "B1", "ocean": "B1", "gas": "B1", "atmosphere": "B1", "climate": "B1",
    "force": "B1", "heat": "B1", "population": "B1", "environment": "B1", "wave": "B1",
    "liquid": "B1", "soil": "B1", "solid": "B1", "region": "B1", "global": "B1",
    "layer": "B1", "source": "B1", "mars": "B1", "pollution": "B1", "growth": "B1",
    "environmental": "B1", "disease": "B1", "resources": "B1", "fuel": "B1", "community": "B1",
    "female": "B1", "volcanoes": "B1", "pole": "B1", "behavior": "B1", "volcano": "B1",
    "valley": "B1", "celsius": "B1", "resource": "B1", "shell": "B1", "producers": "B1",
    "landscape": "B1", "generations": "B1", "recycling": "B1", "biology": "B1", "freezing": "B1",
    "crop": "B1", "thermometer": "B1", "lung": "B1",
    # B2 (75)
    "species": "B2", "cells": "B2", "carbon": "B2", "organisms": "B2", "solar": "B2",
    "matter": "B2", "oxygen": "B2", "ecosystem": "B2", "fossil": "B2", "dna": "B2",
    "gravity": "B2", "bacteria": "B2", "motion": "B2", "cycle": "B2", "radiation": "B2",
    "nutrients": "B2", "current": "B2", "greenhouse": "B2", "core": "B2", "coral": "B2",
    "universe": "B2", "warming": "B2", "reef": "B2", "zone": "B2", "minerals": "B2",
    "evolution": "B2", "visible": "B2", "habitat": "B2", "hemisphere": "B2", "conservation": "B2",
    "melting": "B2", "renewable": "B2", "equator": "B2", "atmospheric": "B2", "polar": "B2",
    "latitude": "B2", "depth": "B2", "crystal": "B2", "tide": "B2", "extinction": "B2",
    "geological": "B2", "steam": "B2", "cooling": "B2", "biological": "B2", "nutrient": "B2",
    "comet": "B2", "altitude": "B2", "basin": "B2", "agricultural": "B2", "pollutants": "B2",
    "endangered": "B2", "humidity": "B2", "feeding": "B2", "exposure": "B2", "moisture": "B2",
    "ridge": "B2", "phenomenon": "B2", "elevation": "B2", "limestone": "B2", "colony": "B2",
    "fertilizer": "B2", "seaweed": "B2", "irrigation": "B2", "nonrenewable": "B2", "deposits": "B2",
    "migration": "B2", "circulation": "B2", "geology": "B2", "scales": "B2", "era": "B2",
    "ecological": "B2", "channel": "B2", "cone": "B2", "smog": "B2", "bulbs": "B2",
    # C1 (12)
    "photosynthesis": "C1", "precipitation": "C1", "magma": "C1", "eclipse": "C1", "algae": "C1",
    "respiration": "C1", "evaporation": "C1", "condensation": "C1", "terrestrial": "C1",
    "microbes": "C1", "decomposition": "C1", "geysers": "C1",
}


def lookup_cefr_level(word: str, pos: str | None = None, source_id: str | None = None) -> str | None:
    """Look up the defensible CEFR level for a word, considering POS and source context."""
    w = word.strip().lower()
    p = (pos or "").strip().lower()

    if source_id == "nature":
        if w in NATURE_CEFR:
            return NATURE_CEFR[w]

    if source_id == "new_words":
        if w in NW_CEFR:
            return NW_CEFR[w]

    if source_id == "uclouvain" or not source_id:
        if "verb" in p:
            if w in UCL_VERB_CEFR:
                return UCL_VERB_CEFR[w]
        elif "adj" in p:
            if w in UCL_ADJ_CEFR:
                return UCL_ADJ_CEFR[w]
        if w in UCL_VERB_CEFR:
            return UCL_VERB_CEFR[w]
        if w in UCL_ADJ_CEFR:
            return UCL_ADJ_CEFR[w]

    # Shared fallback
    if w in NATURE_CEFR:
        return NATURE_CEFR[w]
    if w in NW_CEFR:
        return NW_CEFR[w]
    if w in UCL_VERB_CEFR:
        return UCL_VERB_CEFR[w]
    if w in UCL_ADJ_CEFR:
        return UCL_ADJ_CEFR[w]

    return None
