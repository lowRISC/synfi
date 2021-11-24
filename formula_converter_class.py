# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

import ray
from sympy import Symbol, false, sympify, true
from sympy.logic.boolalg import is_cnf, simplify_logic, to_cnf


@ray.remote
class FormulaConverter:
    """ Class for performing distributed formula conversions.

    This class provides functionality to convert formulas of the cell library
    to boolean formulas, which can be handed to a SAT solver.

    """
    def __init__(self, cells):
        """ Inits the formula converter class.

        Args:
            cells: The cells of the cell library.
        """
        self.cells = cells

    def _simplify_expression(self, expr: Symbol) -> Symbol:
        """ Simplify the CNF expression.

        The simplify_logic functionality of sympy is used to simplify the given
        expression. As the output needs to be in CNF, a check is conducted.

        Args:
            expr: The boolean expression to simplify.

        Returns:
            The simplified boolean expression in CNF.
        """
        simplified = simplify_logic(expr, 'cnf', True)
        if is_cnf(simplified):
            return simplified
        else:
            return expr

    def _convert_cnf(self, expr: Symbol, out_symbol: Symbol,
                     gate: str) -> Symbol:
        """ Convert the given boolean expression to CNF.

        The logical biconditional of the boolean expression of the gate is converted
        to CNF using the sympy library.

        Args:
            expr: The boolean expression to convert.
            out_symbol: The output variable of the boolean expression.
            gate: The name of the current gate.

        Returns:
            The boolean expression in CNF.
        """
        cnf = to_cnf((out_symbol & expr) | (~out_symbol & ~expr))
        if not is_cnf(cnf):
            raise Exception(f"Failed to convert {gate} to CNF.")
        return cnf

    def _replace_pin(self, inputs: list, outputs: list, target_char: str,
                     replace_char: str) -> str:
        """ Replace a pin name.

        Sympy uses some predefined symbols (I, S), which need to be replaced in the
        input and output pins.

        Args:
            inputs: The inputs of the cell.
            outputs: The outputs of the cell.
            target_char: The char to replace.
            replace_char: The rename char.

        Returns:
            The formula, input, and output with the replaced pin name.
        """
        inputs = [
            in_pin.replace(target_char, replace_char) for in_pin in inputs
        ]
        for out_pin in outputs:
            out_pin.name.replace(target_char, replace_char)

        return inputs, outputs

    def _convert_string(self, formula: str, output: str, gate: str) -> Symbol:
        """ Convert the formula string to a sympy Symbol.

        Args:
            formula: The boolean formula.
            output: The output in name of the boolean expression.
            gate: The current gate.

        Returns:
            The boolean expression in CNF.
        """
        # As sympy requires ~ as a NOT, replace !.
        formula = formula.replace("!", "~")
        # "S" is predefined by sympy, replace with K.
        formula = formula.replace("S", "K")
        # "I" is predefined by sympy, replace with L.
        formula = formula.replace("I", "L")
        # Set 1/0 formula to true/false
        if formula == "1": formula = true
        if formula == "0": formula = false
        try:
            # Convert the string to sympy using sympify. The convert_xor=False
            # converts a ^ to a XOR.
            formula = sympify(formula, convert_xor=False)
            # Use the logical biconditional to induce the output.
            formula = self._convert_cnf(formula, Symbol(output), gate)
            # Simplify CNF formula.
            formula = self._simplify_expression(formula)
        except:
            raise Exception(f"Failed to convert formula for {gate}.")

        return formula

    def convert_formulas(self) -> list:
        """ Converts the boolean function from a string to a clause.

        Returns:
            The list of cells with the converted formulas.
        """
        cells_formula = []
        for cell in self.cells:
            # "S" is predefined by sympy, replace with K.
            cell_formula = cell
            cell_formula.inputs, cell_formula.outputs = self._replace_pin(
                cell_formula.inputs, cell_formula.outputs, "S", "K")
            # "I" is predefined by sympy, replace with L.
            cell.inputs, cell.outputs = self._replace_pin(
                cell_formula.inputs, cell_formula.outputs, "I", "L")
            for output in cell_formula.outputs:
                if output.formula:
                    output.formula_cnf = self._convert_string(
                        output.formula, output.name, cell_formula.name)

            cells_formula.append(cell_formula)

        return cells_formula
