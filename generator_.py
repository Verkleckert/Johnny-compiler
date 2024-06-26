def templater(operator, operand_1, operand_2, output_index, short_input: bool, short_output: bool):
    if operator == "PLUS":
        template = [[1, operand_1], [2, operand_2], [4, output_index]]
        if short_output:
            template.pop()
        if short_input:
            template.pop(0)
    elif operator == "MINUS":
        template = [[1, operand_1], [3, operand_2], [4, output_index]]
        if short_output:
            template.pop()
        if short_input:
            template.pop(0)
    elif operator == "TIMES":
        pass
    elif operator == "DIVIDE":
        pass
    # if operator == "PLUS":
    #     template = [generate_data(1, operand_1), generate_data(
    #         2, operand_2), generate_data(4, output_index)]
    # elif operator == "MINUS":
    #     template = [generate_data(1, operand_1), generate_data(
    #         3, operand_2), generate_data(4, output_index)]
    return template


def calculate_offset(instruction_structure):
    length = 1
    for element in instruction_structure:
        if element[0] == "PLUS":
            length += 3
        elif element[0] == "MINUS":
            length += 3

    return length


def generate_data(hi, lo):
    lo = str("0" * (3 - len(str(lo)))+str(lo))
    if hi == 0:
        return str(lo)
    else:
        return str(str(hi) + lo)


def parse_ast(node):
    instruction_structure = []
    number_structure = {}
    index_counter = 0

    def traverse(node):
        nonlocal instruction_structure, number_structure, index_counter
        if node.type == 'NUMBER':
            number = node.value
            if number not in number_structure.values():
                number_structure[index_counter] = number
                index_counter += 1
            return list(number_structure.keys())[list(number_structure.values()).index(number)]
        elif node.type in ['PLUS', 'MINUS', 'TIMES', 'DIVIDE']:
            left_index = traverse(node.children[0])
            right_index = traverse(node.children[1])
            output_index = index_counter
            instruction_structure.append(
                [node.type, left_index, right_index, output_index])
            return output_index

    traverse(node)
    return instruction_structure, number_structure


def apply_offset(instruction_structure, number_structure, offset):
    number_structure_ = {}
    for i in range(len(instruction_structure)):
        instruction_structure[i][1] += offset
        instruction_structure[i][2] += offset
        instruction_structure[i][3] += offset
    for key in number_structure:
        number_structure_[key + offset] = number_structure[key]
    return instruction_structure, number_structure_


def generate_assembly(node):
    ram = []
    ram_out = {}
    instruction_structure, number_structure = parse_ast(node)
    print("\nInstruction Structure:")
    print(instruction_structure)
    print("\nNumber Structure:")
    print(number_structure)
    
    for i in range(len(instruction_structure)):
        operator = instruction_structure[i][0]
        operand_1 = instruction_structure[i][1]
        operand_2 = instruction_structure[i][2]
        output_index = instruction_structure[i][3]
        if operator in ['PLUS', 'MINUS']:
            if i == 0:
                short_input = False
            elif instruction_structure[i-1][0] in ['PLUS', 'MINUS']:
                short_input = True
            if i == len(instruction_structure) - 1:
                short_output = False
            elif instruction_structure[i+1][0] in ['PLUS', 'MINUS']:
                short_output = True
        else:
            short_input, short_output = False
        
        template = templater(operator, operand_1, operand_2, output_index, short_input, short_output)
        ram.extend(template)
    print(ram)
    #     for j in range(len(template)):
    #         if len(ram) <= 0:
    #             index = 0
    #         else:
    #             index = max(ram) + 1
    #         ram[index] = template[j]
    # for variable in number_structure:
    #     ram[variable] = str(generate_data(0, number_structure.get(variable)))
    
    
    
    
    
    # offset = calculate_offset(instruction_structure)
    # instruction_structure, number_structure = apply_offset(
    #     instruction_structure, number_structure, offset)
    
    # for i in range(len(instruction_structure)):
    #     operator = instruction_structure[i][0]
    #     operand_1 = instruction_structure[i][1]
    #     operand_2 = instruction_structure[i][2]
    #     output_index = instruction_structure[i][3]
    #     template = templater(operator, operand_1, operand_2, output_index)
    #     for j in range(len(template)):
    #         if len(ram) <= 0:
    #             index = 0
    #         else:
    #             index = max(ram) + 1
    #         ram[index] = template[j]
    # for variable in number_structure:
    #     ram[variable] = str(generate_data(0, number_structure.get(variable)))

    # ram[offset - 1] = int(generate_data(10, 0))
    return ram_out
