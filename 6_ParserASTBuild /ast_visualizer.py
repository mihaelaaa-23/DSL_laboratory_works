from ast_nodes import (
    BinaryOpNode,
    UnaryOpNode,
    NumberNode,
    VariableNode,
    AssignmentNode,
    FunctionCallNode,
    AbsoluteValueNode
)


class TextASTVisualizer:
    def __init__(self):
        self.indent_size = 2

    def visualize(self, node, indent=0):

        if node is None:
            return "None"

        lines = []
        self._visualize_node(node, lines, indent)
        return "\n".join(lines)

    def _visualize_node(self, node, lines, indent=0):
        if node is None:
            return

        indent_str = ' ' * (indent * self.indent_size)
        node_type = node.__class__.__name__

        # Handle different node types with more readable formatting
        if isinstance(node, NumberNode):
            lines.append(f"{indent_str}NumberNode")
            lines.append(f"{indent_str}  value: {node.value}")

        elif isinstance(node, VariableNode):
            lines.append(f"{indent_str}VariableNode")
            lines.append(f"{indent_str}  name: {node.name}")

        elif isinstance(node, BinaryOpNode):
            op_value = node.op.value if hasattr(node.op, 'value') else node.op
            lines.append(f"{indent_str}BinaryOpNode")
            lines.append(f"{indent_str}  operator: {op_value}")

            lines.append(f"{indent_str}  left:")
            self._visualize_node(node.left, lines, indent + 1)

            lines.append(f"{indent_str}  right:")
            self._visualize_node(node.right, lines, indent + 1)

        elif isinstance(node, UnaryOpNode):
            op_value = node.op.value if hasattr(node.op, 'value') else node.op
            lines.append(f"{indent_str}UnaryOpNode")
            lines.append(f"{indent_str}  operator: {op_value}")

            lines.append(f"{indent_str}  expression:")
            self._visualize_node(node.expr, lines, indent + 1)

        elif isinstance(node, AssignmentNode):
            lines.append(f"{indent_str}AssignmentNode")

            lines.append(f"{indent_str}  variable:")
            if isinstance(node.variable, str):
                lines.append(f"{indent_str}    name: {node.variable}")
            else:
                self._visualize_node(node.variable, lines, indent + 1)

            lines.append(f"{indent_str}  value:")
            self._visualize_node(node.value, lines, indent + 1)

        elif isinstance(node, FunctionCallNode):
            lines.append(f"{indent_str}FunctionCallNode")
            lines.append(f"{indent_str}  name: {node.name}")

            lines.append(f"{indent_str}  arguments:")
            self._visualize_node(node.args, lines, indent + 1)

        elif isinstance(node, AbsoluteValueNode):
            lines.append(f"{indent_str}AbsoluteValueNode")

            lines.append(f"{indent_str}  expression:")
            self._visualize_node(node.expr, lines, indent + 1)

        else:
            # Generic fallback
            lines.append(f"{indent_str}{node_type}")
            for attr_name, attr_value in node.__dict__.items():
                if attr_name.startswith('_'):
                    continue

                if isinstance(attr_value, list):
                    lines.append(f"{indent_str}  {attr_name}:")
                    for i, item in enumerate(attr_value):
                        lines.append(f"{indent_str}    [{i}]:")
                        if hasattr(item, '__dict__'):
                            self._visualize_node(item, lines, indent + 2)
                        else:
                            lines.append(f"{indent_str}      {item}")

                elif hasattr(attr_value, '__dict__'):
                    lines.append(f"{indent_str}  {attr_name}:")
                    self._visualize_node(attr_value, lines, indent + 1)

                else:
                    lines.append(f"{indent_str}  {attr_name}: {attr_value}")


class ASCIITreeVisualizer:
    def __init__(self):
        self.result = []

    def visualize(self, node):
        self.result = []
        self._build_tree(node, "", "", "")
        return "\n".join(self.result)

    def _build_tree(self, node, prefix, connector, label):
        if node is None:
            return

        # Get node display text based on type
        if isinstance(node, NumberNode):
            node_text = f"Number({node.value})"
        elif isinstance(node, VariableNode):
            node_text = f"Variable({node.name})"
        elif isinstance(node, BinaryOpNode):
            op_value = node.op.value if hasattr(node.op, 'value') else node.op
            node_text = f"BinaryOp({op_value})"
        elif isinstance(node, UnaryOpNode):
            op_value = node.op.value if hasattr(node.op, 'value') else node.op
            node_text = f"UnaryOp({op_value})"
        elif isinstance(node, AssignmentNode):
            node_text = "Assignment"
        elif isinstance(node, FunctionCallNode):
            node_text = f"Function({node.name})"
        elif isinstance(node, AbsoluteValueNode):
            node_text = "AbsoluteValue"
        else:
            node_text = str(node)

        # Add label if present
        if label:
            node_text = f"{label}: {node_text}"

        # Print current node
        self.result.append(f"{prefix}{connector}{node_text}")

        # Prepare for children
        child_prefix = prefix + "│   " if connector.startswith("├") else prefix + "    "

        # Process children based on node type
        children = []

        if isinstance(node, BinaryOpNode):
            children = [("left", node.left), ("right", node.right)]
        elif isinstance(node, UnaryOpNode):
            children = [("expr", node.expr)]
        elif isinstance(node, AssignmentNode):
            if isinstance(node.variable, str):
                children = [("variable", VariableNode(node.variable)), ("value", node.value)]
            else:
                children = [("variable", node.variable), ("value", node.value)]
        elif isinstance(node, FunctionCallNode):
            children = [("args", node.args)]
        elif isinstance(node, AbsoluteValueNode):
            children = [("expr", node.expr)]

        # Process all children with proper branch connectors
        for i, (child_label, child) in enumerate(children):
            is_last = (i == len(children) - 1)
            connector_char = "└── " if is_last else "├── "
            self._build_tree(child, child_prefix, connector_char, child_label)

def visualize_ast(ast_node, mode="text"):
    if mode == "text":
        visualizer = TextASTVisualizer()
        result = visualizer.visualize(ast_node)
        print(result)
        return result

    elif mode == "ascii":
        visualizer = ASCIITreeVisualizer()
        result = visualizer.visualize(ast_node)
        print(result)
        return result

    else:
        raise ValueError(f"Unknown visualization mode: {mode}")
