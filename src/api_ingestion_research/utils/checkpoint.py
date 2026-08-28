import json
from pathlib import Path

CHECKPOINT_FILE = Path("data/checkpoint.json")


def load_checkpoint() -> int | None:
    """Loads the last successfully processed offset from the checkpoint.

    Returns:
        The last successfully processed offset, or None if no checkpoint
        exists.
    """
    if not CHECKPOINT_FILE.exists():
        return None

    with CHECKPOINT_FILE.open("r") as file:
        checkpoint = json.load(file)

    return checkpoint["skip"]


def save_checkpoint(skip: int) -> None:
    """Saves the offset of the last successfully processed batch.

    Args:
        skip: Number of records successfully processed.
    """
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with CHECKPOINT_FILE.open("w") as file:
        json.dump({"skip": skip}, file)