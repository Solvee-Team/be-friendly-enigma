from model_utils import Choices

VERBS = Choices("assign", "complete", "due", "create", "have")
TYPES = Choices(
    "Custom",
    "Assessment",
    "Goal",
    "Message",
    "Exercise_Plan",
    "Appointment",
    "Manager_Assign",
    "Member_Assign",
)

TYPES_DISPLAY = {
    TYPES.Custom: "Custom",
    TYPES.Assessment: "Assessment",
    TYPES.Goal: "Goal",
    TYPES.Message: "Message",
    TYPES.Exercise_Plan: "Exercise Plan",
    TYPES.Appointment: "Appointment",
    TYPES.Manager_Assign: "Health Coach Assigned",
    TYPES.Member_Assign: "Member Assigned",
}


def get_display_type(type):
    return TYPES_DISPLAY[type] if type in TYPES_DISPLAY else type
