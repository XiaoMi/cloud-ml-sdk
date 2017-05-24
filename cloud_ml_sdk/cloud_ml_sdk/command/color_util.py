
class Colors:
  HEADER = "\033[95m"
  BLUE = "\033[94m"
  GREEN = "\033[92m"
  YELLOW = "\033[93m"
  RED = "\033[91m"
  ENDC = "\033[0m"
  BOLD = "\033[1m"
  UNDERLINE = "\033[4m"

class States:
  SUCCESS_STATES = ("running", "completed")
  WARNING_STATES = ("validated", "enqueuing", "enqueued", "creating", "processing")
  ERROR_STATES = ("deleting", "error")

def colorize_state(state):
  if state in States.SUCCESS_STATES:
    return Colors.GREEN + state + Colors.ENDC
  elif state in States.WARNING_STATES:
    return Colors.YELLOW + state + Colors.ENDC
  elif state in States.ERROR_STATES:
    return Colors.RED + state + Colors.ENDC
  else:
    return state

def colorize_warning(content):
  return Colors.RED + content + Colors.ENDC
