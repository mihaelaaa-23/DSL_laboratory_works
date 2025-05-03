class ASTVisualizer:
    def __init__(self):
        self.indent_level = 0
        self.indent_size = 2

    def visualize(self, node):
        if node is None:
            return "None"

        result = []
        self._visualize_node(node, result)
        return "\n".join(result)

    def _visualize_node(self, node, result):
        indent = " " * (self.indent_level * self.indent_size)

        # add the current node's representation
        result.append(f"{indent}{node.__class__.__name__}")

        # increase indentation for child nodes
        self.indent_level += 1

        # handle different node types
        if hasattr(node, 'value') and not hasattr(node, 'left') and not hasattr(node, 'right'):
            result.append(f"{indent}  Value: {node.value}")

        if hasattr(node, 'name'):
            result.append(f"{indent}  Name: {node.name}")

        if hasattr(node, 'op'):
            result.append(f"{indent}  Operator: {node.op.value}")

        if hasattr(node, 'variable'):
            result.append(f"{indent}  Variable:")
            self._visualize_node(node.variable, result)

        if hasattr(node, 'left'):
            result.append(f"{indent}  Left:")
            self._visualize_node(node.left, result)

        if hasattr(node, 'right'):
            result.append(f"{indent}  Right:")
            self._visualize_node(node.right, result)

        if hasattr(node, 'expr'):
            result.append(f"{indent}  Expression:")
            self._visualize_node(node.expr, result)

        if hasattr(node, 'args'):
            result.append(f"{indent}  Arguments:")
            self._visualize_node(node.args, result)

        # decrease indentation after processing all children
        self.indent_level -= 1