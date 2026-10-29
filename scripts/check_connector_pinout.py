#!/usr/bin/env python3
"""Check connector power pins, A/C protocol pairing, and the adjacent UART pair."""
from collections import Counter
import csv
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def pcb_pads(text):
    """Read KiCad's line-indented footprint/pad records without external dependencies."""
    result = {}
    for block in re.split(r'(?m)^\t(?=\(footprint )', text)[1:]:
        ref = re.search(r'\(property "Reference" "([^"]+)"', block)
        if not ref:
            continue
        pads = {}
        for number, body in re.findall(
                r'(?ms)^\t\t\(pad "([^"]+)"(.*?)(?=^\t\t\(pad |^\t\)|\Z)', block):
            net = re.search(r'\(net "([^"]+)"\)', body)
            if net:
                pads[number] = net.group(1)
        result[ref.group(1)] = pads
    return result


def family(signal):
    return next((f for f in ('SPI0', 'SPI1', 'I2C0', 'I2C1', 'AUX', 'UART') if signal.startswith(f)), None)


def check(board_text=None, rows=None):
    if board_text is None:
        board_text = (ROOT / 'hardware/backplane/HackerfabBackplane.kicad_pcb').read_text(encoding='utf-8')
    if rows is None:
        with (ROOT / 'docs/connector-pinout.csv').open(encoding='utf-8', newline='') as stream:
            rows = list(csv.DictReader(stream))
    errors = []
    pads = pcb_pads(board_text)
    manifest = {(r['connector'], r['pad']): r for r in rows}
    expected_keys = {(ref, f'{row}{col}') for ref in ('J1', 'J2', 'J3') for row in 'AC' for col in range(10, 24)}
    if len(rows) != 84 or set(manifest) != expected_keys:
        return ['Connector pinout manifest must contain each of the 84 signal positions exactly once']
    common = {f'SPI{bus}_{signal}' for bus in (0, 1) for signal in ('MISO', 'MOSI', 'CLK', 'CS1', 'CS2', 'CS3')}
    common |= {f'I2C{bus}_{signal}' for bus in (0, 1) for signal in ('SDA', 'SCL')}
    local = {'J1': {'AUX1', 'AUX2', 'AUX3', 'UART_TX', 'UART_RX'},
             'J2': {'AUX4', 'AUX5', 'AUX6'},
             'J3': {'AUX7', 'AUX8', 'AUX9', 'AUX10', 'UART_RX'}}
    for ref in ('J1', 'J2', 'J3'):
        actual = pads.get(ref, {})
        if len(actual) != 96:
            errors.append(f'{ref}: expected 96 numbered connector pads')
        for row in 'ABC':
            for col in range(1, 33):
                pin = f'{row}{col}'
                if row in 'AC' and 10 <= col <= 23:
                    continue
                net = '+24V_P' if row != 'B' and col in (1, 2, 31, 32) else (
                    '+12V' if col in (4, 5, 28, 29) else '+5V' if col in (7, 8, 25, 26) else 'GND')
                if actual.get(pin) != net:
                    errors.append(f'{ref}:{pin}: fixed power/ground pin must remain {net}')
        connected = []
        for row in 'AC':
            for col in range(10, 24):
                pin = f'{row}{col}'
                item = manifest[ref, pin]
                partner = ('C' if row == 'A' else 'A') + str(col)
                if item['paired_pad'] != partner or family(item['function']) is None or family(item['function']) != family(manifest[ref, partner]['function']):
                    errors.append(f'{ref}:{pin}: paired A/C contact must retain its specific protocol')
                expected = f'unconnected-({ref}-Pad{pin})' if item['net'] == 'NC' else '/' + item['function']
                if item['net'] != 'NC' and item['net'] != expected:
                    errors.append(f'{ref}:{pin}: manifest net and function disagree')
                if actual.get(pin) != expected:
                    errors.append(f'{ref}:{pin}: PCB net does not match connector pinout manifest')
                if item['net'] != 'NC':
                    connected.append(item['function'])
                    if item['function'] != 'AUX10' and pads.get(item['jumper'], {}).get('1') != expected:
                        errors.append(f'{ref}:{pin}: source jumper output does not match signal')
        if Counter(connected) != Counter(common | local[ref]):
            errors.append(f'{ref}: original signal set must be preserved without duplicates')
    for pin in (f'{row}{col}' for row in 'AC' for col in range(10, 24)):
        if len({manifest[ref, pin]['function'] for ref in ('J1', 'J2', 'J3')}) != 1:
            errors.append(f'{pin}: reserved function must be consistent across ports')
    return errors


if __name__ == '__main__':
    problems = check()
    if problems:
        raise SystemExit('\n'.join(problems))
    print('OK: 288 connector pads, fixed power/ground, paired protocols, adjacent UART, signal inventory, and jumper outputs.')
