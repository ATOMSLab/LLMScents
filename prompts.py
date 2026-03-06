def PromptOne(
    testMol: dict,
    targetLabel: str,
) -> str:
    return f"""
Make a prediction about this molecule.

Molecule: {testMol["odorname"]}
SMILES: {testMol["canonicalsmiles"]}
Concentration: {testMol["odor_dilution"]}

On a scale of 0-100, how {targetLabel} is this molecule at this concentration?

Provide:
- Your rating (0-100)
- Which molecule (if any) you used as reference
- Brief explanation
"""


def PromptTwo(
    testMol: dict,
    highExemplars,
    lowExemplars,
    targetLabel: str,
    includeRatings: bool,
) -> str:
    if includeRatings:
        highList = "\n".join(
            [
                f"  {m['odorname']} (SMILES: {m['canonicalsmiles']}, Concentration: {m['odor_dilution']}, {targetLabel}: {m[targetLabel]:.1f})"
                for m in highExemplars
            ]
        )
        lowList = "\n".join(
            [
                f"  {m['odorname']} (SMILES: {m['canonicalsmiles']}, Concentration: {m['odor_dilution']}, {targetLabel}: {m[targetLabel]:.1f})"
                for m in lowExemplars
            ]
        )
    else:
        highList = "\n".join(
            [
                f"  {m['odorname']} (SMILES: {m['canonicalsmiles']}, Concentration: {m['odor_dilution']})"
                for m in highExemplars
            ]
        )
        lowList = "\n".join(
            [
                f"  {m['odorname']} (SMILES: {m['canonicalsmiles']}, Concentration: {m['odor_dilution']})"
                for m in lowExemplars
            ]
        )

    return f"""
Make a prediction about this molecule, and use these data.

Molecule: {testMol["odorname"]}
SMILES: {testMol["canonicalsmiles"]}
Concentration: {testMol["odor_dilution"]}

Reference molecules:

HIGH {targetLabel}:
{highList}

LOW {targetLabel}:
{lowList}

On a scale of 0-100, how {targetLabel} is this molecule at this concentration?

Provide:
- Your rating (0-100)
- Which molecule (if any) you used as reference
- An explanation
"""


def PromptThree(testMol: dict, highExemplars, lowExemplars, targetLabel: str) -> str:
    highList = "\n".join(
        [
            f"  CID {m['cid']}: {m['odorname']} (SMILES: {m['canonicalsmiles']}, Concentration: {m['odor_dilution']})"
            for m in highExemplars
        ]
    )

    lowList = "\n".join(
        [
            f"  CID {m['cid']}: {m['odorname']} (SMILES: {m['canonicalsmiles']}, Concentration: {m['odor_dilution']})"
            for m in lowExemplars
        ]
    )

    return f"""
Make a prediction about this molecule; find one analogue among these in order to do so.

Molecule: {testMol["odorname"]}
SMILES: {testMol["canonicalsmiles"]}
Concentration: {testMol["odor_dilution"]}

Reference molecules:

HIGH {targetLabel}:
{highList}

LOW {targetLabel}:
{lowList}

On a scale of 0-100, how {targetLabel} is this molecule at this concentration?

Find the most similar molecule from the list and use it as your analogue.

Provide:
- Your rating (0-100)
- Which molecule you used as analogue (include CID)
- Why you chose that molecule
"""


if __name__ == "__main__":
    pass
