def aggregrate_party_and_score(qs) -> list:
    final = {}

    for polling_unit in qs:
        if polling_unit["party_abbreviation"] in final.keys():
            final[polling_unit["party_abbreviation"]] = (
                final[polling_unit["party_abbreviation"]] + polling_unit["party_score"]
            )
        else:
            final[polling_unit["party_abbreviation"]] = polling_unit["party_score"]

    return [{"party_abbreviation": k, "total_votes": v} for k, v in final.items()]
