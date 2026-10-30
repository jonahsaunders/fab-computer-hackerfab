#!/usr/bin/env python3
"""Check connector power pins, A/C protocol pairing, and the adjacent UART pair."""
from collections import Counter
import csv
from pathlib import Path
import re
import argparse
import xml.etree.ElementTree as ET

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
            pads[number] = net.group(1) if net else ''
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
             'J3': {'AUX7', 'AUX8', 'AUX9', 'AUX10'}}
    for row in rows:
        col = int(row['pad'][1:])
        expected_family = ('SPI0' if 10 <= col <= 12 else 'SPI1' if 21 <= col <= 23
                           else 'I2C0' if col == 16 else 'I2C1' if col == 17
                           else 'UART' if col == 20 else 'AUX')
        if family(row['function']) != expected_family:
            errors.append(f"{row['connector']}:{row['pad']}: reserved function must be {expected_family}")
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
                matches = actual.get(pin) == expected
                if item['net'] == 'NC':
                    matches = pin in actual and (not actual[pin] or actual[pin].startswith('unconnected-'))
                if not matches:
                    errors.append(f'{ref}:{pin}: PCB net does not match connector pinout manifest')
                if item['net'] != 'NC':
                    connected.append(item['function'])
                    if item['function'] != 'AUX10' and pads.get(item['jumper'], {}).get('1') != expected:
                        errors.append(f'{ref}:{pin}: source jumper output does not match signal')
        if Counter(connected) != Counter(common | local[ref]):
            errors.append(f'{ref}: V6 signal set must be preserved without duplicates; UART belongs only to J1')
    for pin in (f'{row}{col}' for row in 'AC' for col in range(10, 24)):
        if len({manifest[ref, pin]['function'] for ref in ('J1', 'J2', 'J3')}) != 1:
            errors.append(f'{pin}: reserved function must be consistent across ports')
    positions = {}
    for block in re.split(r'(?m)^\t(?=\(footprint )', board_text)[1:]:
        ref = re.search(r'\(property "Reference" "(J[123])"', block)
        at = re.search(r'(?m)^\t\t\(at ([\d.-]+) ([\d.-]+)', block)
        if ref and at:
            positions[ref.group(1)] = float(at.group(2))
    if set(positions) != {'J1', 'J2', 'J3'} or not positions['J1'] > positions['J2'] > positions['J3']:
        errors.append('Connector order must be J1 nearest MCU, J2 middle, J3 farthest')
    return errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--netlist', type=Path, help='Fresh KiCad XML netlist to compare all 288 connector pads')
    args = parser.parse_args()
    problems = check()
    if args.netlist:
        root = ET.parse(args.netlist).getroot()
        schematic = {(n.get('ref'), n.get('pin')): net.get('name')
                     for net in root.findall('./nets/net') for n in net.findall('node')}
        pcb = pcb_pads((ROOT / 'hardware/backplane/HackerfabBackplane.kicad_pcb').read_text(encoding='utf-8'))
        def normalized(net):
            return '' if not net or net.startswith('unconnected-') else net
        for ref in ('J1', 'J2', 'J3'):
            for row in 'ABC':
                for col in range(1, 33):
                    pin = f'{row}{col}'
                    if normalized(schematic.get((ref, pin))) != normalized(pcb.get(ref, {}).get(pin)):
                        problems.append(f'{ref}:{pin}: schematic and PCB nets differ')
    if problems:
        raise SystemExit('\n'.join(problems))
    print('OK: 288 connector pads, fixed power/ground, V6 protocol columns, UART only on J1, slot order, and jumper outputs.')
    if args.netlist:
        print('OK: all 288 connector pads agree with the supplied schematic netlist.')
