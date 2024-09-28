import yaml


class RuleEngine:
    def __init__(self, rules_file):
        self.rules = self.load_rules(rules_file)

    # Load rules from YAML
    def load_rules(self, file_path):
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)['rules']

    # Evaluate conditions based on defined variables
    def evaluate_conditions(self, conditions, defined_variables):
        for condition in conditions:
            name = condition['name']
            operator = condition['operator']
            value = condition['value']
            variable_value = defined_variables.get(name)

            if operator == 'greater_than' and not (variable_value > value):
                return False
            elif operator == 'less_than' and not (variable_value < value):
                return False
            elif operator == 'equal' and not (variable_value == value):
                return False
        return True

    # Execute actions
    def execute_actions(self, actions, row):
        for action in actions:
            action_name = action['name']
            params = action.get('params', {})
            if action_name == 'print_row':
                print(f"Row data: {row}")
            else:
                print(f"Executing action: {action_name} with params: {params}")
            print(f"Executing action: {action_name} with params: {params}")

    # Main function to run the rules
    def run_rules(self, defined_variables):
        for rule in self.rules:
            conditions = rule['conditions']
            actions = rule['actions']
            if self.evaluate_conditions(conditions, defined_variables):
                self.execute_actions(actions, defined_variables)


# Example of extending the base class
class CustomRuleEngine(RuleEngine):
    def __init__(self, rules_file):
        super().__init__(rules_file)

    # You can add custom methods or override existing ones here


if __name__ == '__main__':
    df = {
        'expected_return': 0.06,
        'annual_volatility': 0.09
    }

    # Initialize the rule engine
    engine = CustomRuleEngine('rules.yaml')
    engine.run_rules(df)
