class Validation:
    @staticmethod
    def validate_player_name(name):
        # Validate player name input
        if not name or not name.strip():
            return False, "❌ Name cannot be empty!"
        name = name.strip()

        if len(name) < 2:
            return False, "Player name must be at least 2 characters❗"

        if len(name) > 20:
            return False, "Player name must be less than 20 characters❗"

        # Check for invalid characters
        if not all(c.isalnum() or c.isspace() for c in name):
            return False, "⚠️ Player name can only contain letters, numbers and spaces"

        # Check if name contains only numbers
        if name.replace(" ", "").isdigit():
            return False, "⚠️ Player name cannot contain only numbers"

        # This return was duplicated and unreachable
        return True, "Valid name, Continue to play! ✅"

    @staticmethod
    def validate_flow_answer(answer):
        # Validate maximum flow answer input
        try:
            flow = int(answer)

            if flow < 0:
                return False, "Flow cannot be negative"

            if flow > 100:
                return False, "Flow seems too large (max 100)"

            return True, "Valid flow"

        except ValueError:
            return False, "Please enter a valid number"
        except Exception as e:
            return False, f"Unexpected validation error: {str(e)}"

    @staticmethod
    def validate_network_graph(graph):
        # Validate the traffic network graph
        required_nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'T']

        # Check all required nodes exist
        for node in required_nodes:
            if node not in graph:
                return False, f"Missing required node: {node}"

        # Check for valid capacities
        for u in graph:
            for v, capacity in graph[u].items():
                if not isinstance(capacity, int) or capacity < 0:
                    return False, f"Invalid capacity between {u} and {v}"

        return True, "Valid network graph"
