
from .main import getPDF,sys,os

def hasSuffix(name: str) -> bool:
    result: bool = False

    for suffix in ['.jpg', '.png']:
        if (result := name.endswith(suffix)):
            break

    return result

def main() -> int:
    """Entry point for the application script"""

    images: list[str] = list(filter(hasSuffix, sys.argv))

    return getPDF(images)
