"""Canonical posture row shape for sequence storage and APIs."""


def canonical_posture_row(posture_doc: dict, *, posture_intent: str, recommended_modification: str) -> dict:
    """
    Map a posture document from the database to the uniform six-field shape.

    Expects flat `name` (English string) and `sanskrit_name` on the posture doc.
    Returns _id, name, sanskrit_name, client_id, posture_intent, recommended_modification.
    Does not include aliases on this row.
    """
    english = posture_doc.get("name") or "Unknown"
    sanskrit = posture_doc.get("sanskrit_name") or ""

    oid = posture_doc.get("_id") or posture_doc.get("id") or posture_doc.get("client_id")

    return {
        "_id": str(oid),
        "name": english,
        "sanskrit_name": sanskrit,
        "client_id": posture_doc.get("client_id", ""),
        "posture_intent": posture_intent,
        "recommended_modification": recommended_modification,
    }
