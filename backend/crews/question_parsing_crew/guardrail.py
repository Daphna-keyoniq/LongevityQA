from typing import Any, Tuple


def validate_and_trasform(
    answer: Any,
) -> Tuple[bool, Any]:
    """Call multiple functions to validate the input and transform it to match the ontology."""
    # full_profile_pydantic = full_profile.pydantic  # first convert to pydantic model

    # if type(answer) is not str:
    #     return False, "Answer must be a string"
    # if len(answer) == 0:
    #     return False, "Answer cannot be empty"
    return True, answer


# def map_terms_to_ontology(
#     full_profile: ParsedProfile,
# ) -> ParsedProfile:
#     """Matches the terms in the input to the ontology."""
#     # Match terms to the ontology
#     ontology_crew = OntologyCrew(pydantic_type=ParsedProfile).crew()
#     full_profile = ontology_crew.kickoff(
#         inputs={"data": full_profile.model_dump_json(indent=2)}
#     ).pydantic

#     return full_profile


# def validate(
#     full_profile: ParsedProfile,
# ) -> Tuple[bool, Union[ParsedProfile, str]]:
#     """Validates a full profile by checking if it contains the required
#     fields (height, weight etc..).
#     If it doesn't contain the required fields, it returns a message with the
#     missing fields so that the agent can attempt to recompute the profile.
#     """

#     error_msg = None

#     if not full_profile.patient:
#         error_msg = "Missing patient"
#     if not full_profile.patient.weight:
#         error_msg = "Missing weight"
#     if not full_profile.patient.height:
#         error_msg = "Missing height"
#     if not (full_profile.patient.age or full_profile.patient.birth_date):
#         error_msg = "Missing age or birth_date"
#     if not full_profile.patient.gender:
#         error_msg = "Missing gender"
#     if len(full_profile.lab_results) == 0:
#         error_msg = "Missing test results"

#     if error_msg:
#         return False, error_msg

#     return True, full_profile
