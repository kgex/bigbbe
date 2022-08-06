import enum


class TaskEnum(enum.Enum):
    learning = "learning"
    project = "project"
    others = "others"


class GrievanceEnum(enum.Enum):
    harrassment = "harrassment"
    abuse = "abuse"
    discriminitation = "discriminitation"
    others = "others"

class PriorityEnum(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"
    critical = "critical"
    none = "none"

class StatusEnum(enum.Enum):
    open = "open"
    in_progress = "in_progress"
    stuck = "stuck"
    closed = "closed"
    none = "none"