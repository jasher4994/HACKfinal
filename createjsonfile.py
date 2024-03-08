import json
import random
from jinja2 import Environment, BaseLoader

# Sample list of words to be used for variable names
word_list = [
    "data", "value", "count", "total", "sum", "item", "number",
    "result", "score", "text", "user",
    "player", "size", "length", "width", "height", "depth",
    "position", "angle", "velocity", "time", "message"
]

# Helper function to generate unique variable names from the word list
def generate_variable_name(used_names):
    name = random.choice(word_list)
    while name in used_names:
        name = random.choice(word_list)
    used_names.add(name)
    return name

# Templates for different kinds of function operations
function_templates = [
    {
        "operation": "add",
        "parameters": [("num1", "int"), ("num2", "int")],
        "return_type": "int",
        "description": "Adds two integers.",
        "implementation": lambda x, y: f"return {x} + {y}"
    },
    {
        "operation": "concatenate",
        "parameters": [("str1", "str"), ("str2", "str")],
        "return_type": "str",
        "description": "Concatenates two strings.",
        "implementation": lambda x, y: f"return {x} + {y}"
    },
    
    # Add more templates as needed up to 20...
]
# Additional templates added to the function_templates list
additional_templates = [
    {
        "operation": "find_max",
        "parameters": [("numbers", "List[int]")],
        "return_type": "int",
        "description": "Finds the maximum value in a list of integers.",
        "implementation": lambda numbers: f"return max({numbers})"
    },
    {
        "operation": "calculate_area_circle",
        "parameters": [("radius", "float")],
        "return_type": "float",
        "description": "Calculates the area of a circle given its radius.",
        "implementation": lambda radius: f"return 3.14159 * {radius} ** 2"
    },
    {
        "operation": "is_palindrome",
        "parameters": [("text", "str")],
        "return_type": "bool",
        "description": "Checks if the given string is a palindrome.",
        "implementation": lambda text: f"return {text} == {text}[::-1]"
    },
    {
        "operation": "merge_dictionaries",
        "parameters": [("dict1", "Dict"), ("dict2", "Dict")],
        "return_type": "Dict",
        "description": "Merges two dictionaries into one.",
        "implementation": lambda dict1, dict2: f"return {{**{dict1}, **{dict2}}}"
    },
    {
        "operation": "count_characters",
        "parameters": [("text", "str")],
        "return_type": "Dict[str, int]",
        "description": "Counts the occurrences of each character in a string.",
        "implementation": lambda text: f"return {{char: {text}.count(char) for char in set({text})}}"
    },
    {
        "operation": "generate_primes",
        "parameters": [("n", "int")],
        "return_type": "List[int]",
        "description": "Generates a list of prime numbers up to n.",
        "implementation": lambda n: f"primes = []\n    for num in range(2, {n} + 1):\n        for prime in primes:\n            if num % prime == 0:\n                break\n        else:\n            primes.append(num)\n    return primes"
    },
    {
        "operation": "fibonacci_sequence",
        "parameters": [("n", "int")],
        "return_type": "List[int]",
        "description": "Generates the first n numbers of the Fibonacci sequence.",
        "implementation": lambda n: f"fib = [0, 1]\n    for i in range(2, {n}):\n        fib.append(fib[-1] + fib[-2])\n    return fib[:{n}]"
    },
    {
        "operation": "sort_list_descending",
        "parameters": [("numbers", "List[int]")],
        "return_type": "List[int]",
        "description": "Sorts a list of integers in descending order.",
        "implementation": lambda numbers: f"return sorted({numbers}, reverse=True)"
    },
    {
        "operation": "remove_list_duplicates",
        "parameters": [("items", "List[int]")],
        "return_type": "List[int]",
        "description": "Removes duplicates from a list of integers.",
        "implementation": lambda items: f"return list(set({items}))"
    },
    {
        "operation": "convert_seconds_to_hms",
        "parameters": [("seconds", "int")],
        "return_type": "Tuple[int, int, int]",
        "description": "Converts seconds to hours, minutes, and seconds.",
        "implementation": lambda seconds: f"hours = {seconds} // 3600\n    minutes = ({seconds} % 3600) // 60\n    secs = {seconds} % 60\n    return hours, minutes, secs"
    },
]

function_templates.extend(additional_templates)


def generate_example_data(num_examples: int) -> list:
    example_data = []
    for _ in range(num_examples):
        template = random.choice(function_templates)
        used_names = set()
        params = [(generate_variable_name(used_names), t) for _, t in template["parameters"]]
        
        # Format parameters for function definition and docstring
        parameters_str = ", ".join([f"{name}: {ptype}" for name, ptype in params])
        parameter_types = {name: ptype for name, ptype in params}
        
        # Generate implementation
        var_names = [name for name, _ in params]
        implementation = template["implementation"](*var_names)
        
        example_data.append({
            "function_name": f"{template['operation']}",
            "parameters": parameters_str,
            "parameter_types": parameter_types,
            "return_type": template["return_type"],
            "description": template["description"],
            "implementation": implementation,
        })
    return example_data

def generate_code_examples(data: list) -> list:
    template_str = """
def {{ function_name }}({{ parameters }}) -> {{ return_type }}:
    \"\"\"{{ description }}

    Args:
        {% for param, type in parameter_types.items() %}
        {{ param }} ({{ type }}): Description of {{ param }}.
        {% endfor %}
    
    Returns:
        {{ return_type }}: Description of return value.
    
    🔥🔥🔥 Created to LBG standards 🔥🔥🔥
    \"\"\"
    {{ implementation }}
    """

    env = Environment(loader=BaseLoader())
    env.trim_blocks = True
    env.lstrip_blocks = True

    generated_examples = []
    
    for item in data:
        template = env.from_string(template_str)
        generated_code = template.render(item)
        generated_examples.append({"input_text": "Create me a function that " + item["description"], "output_text": generated_code})
    
    return generated_examples

if __name__ == "__main__":
    data = generate_example_data(500)  # Generate 20 diverse examples
    examples = generate_code_examples(data)

    output_file_path = "code_examples.jsonl"
    with open(output_file_path, "w") as file:
        for example in examples:
            file.write(json.dumps(example) + '\n')

    print(f"Code examples generated and exported successfully to {output_file_path}.")
    print(examples[345]['output_text'])
