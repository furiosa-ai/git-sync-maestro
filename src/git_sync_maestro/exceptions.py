class ExecutionError(Exception):
    def __init__(self, action_name: str, action_line: int, original_error: Exception):
        self.action_name = action_name
        self.action_line = action_line
        self.original_error = original_error
        super().__init__(f"Error in {action_name} (line {action_line}): {str(original_error)}")


class InvalidEnvironmentValueError(Exception):
    """Raised when an environment variable value is not a string."""

    def __init__(self, action_name: str, action_line: int, original_error: Exception):
        self.action_name = action_name
        self.action_line = action_line
        self.original_error = original_error
        super().__init__(f"Error in {action_name} (line {action_line}): {str(original_error)}")


class ActionExecutionError(Exception):
    """Raised when an action execution fails."""

    pass


class WorkflowValidationError(Exception):
    """Raised when workflow validation fails."""

    pass
