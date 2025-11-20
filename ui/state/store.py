from dataclasses import dataclass, field

@dataclass
class AppState:
    user: str | None = None
    role: str | None = None
    cache: dict = field(default_factory=dict)

STATE = AppState()
