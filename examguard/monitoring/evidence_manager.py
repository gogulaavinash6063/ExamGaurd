from datetime import datetime
from database import get_db


def save_evidence(
    candidate_id,
    session_id,
    evidence_type,
    filename,
    mime_type,
    file_data,
    sha256_hash
):
    """
    Store examination evidence in the database.
    """

    connection = get_db()

    try:
        created_at = datetime.now().isoformat()

        connection.execute("""
            INSERT INTO evidence
            (
                candidate_id,
                session_id,
                evidence_type,
                filename,
                mime_type,
                file_data,
                sha256_hash,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            candidate_id,
            session_id,
            evidence_type,
            filename,
            mime_type,
            file_data,
            sha256_hash,
            created_at
        ))

        connection.commit()

        print("================================")
        print("EVIDENCE SAVED")
        print("================================")
        print("Candidate ID :", candidate_id)
        print("Session ID   :", session_id)
        print("Evidence     :", evidence_type)
        print("Filename     :", filename)
        print("MIME Type    :", mime_type)
        print("Hash         :", sha256_hash)
        print("Created At   :", created_at)
        print("================================")

        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

if __name__ == "__main__":

    test_data = b"TEST SCREENSHOT DATA"

    result = save_evidence(
        candidate_id=1,
        session_id="test-evidence-session",
        evidence_type="screenshot",
        filename="test_screenshot.jpg",
        mime_type="image/jpeg",
        file_data=test_data,
        sha256_hash="test-hash"
    )

    print("Evidence result:", result)


# flow

# Screenshot
    # ↓
# JPEG/PNG bytes
    # ↓
# file_data
    # ↓
# SQLite BLOB