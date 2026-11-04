"""Regression checks for the independent UART added to J2."""
import copy
import csv
import unittest
from unittest.mock import patch
from check_connector_pinout import ROOT, check, pcb_pads


class ConnectorChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.board = (ROOT / 'hardware/backplane/HackerfabBackplane.kicad_pcb').read_text(encoding='utf-8')
        with (ROOT / 'docs/connector-pinout.csv').open(encoding='utf-8', newline='') as stream:
            cls.rows = list(csv.DictReader(stream))
        cls.pads = pcb_pads(cls.board)

    def test_current_design(self):
        self.assertEqual(check(self.board, self.rows), [])

    def test_old_j2_nc_manifest_rejected(self):
        rows = copy.deepcopy(self.rows)
        for row in rows:
            if row['connector'] == 'J2' and row['pad'] in ('A20', 'C20'):
                row.update(net='NC', jumper='')
        self.assertTrue(check(self.board, rows))

    def test_swapped_j2_uart_rejected_even_if_manifest_agrees(self):
        rows, pads = copy.deepcopy(self.rows), copy.deepcopy(self.pads)
        for row in rows:
            if row['connector'] == 'J2' and row['pad'] in ('A20', 'C20'):
                rx = row['pad'] == 'C20'
                row.update(function='UART2_RX' if rx else 'UART2_TX',
                           net='/UART2_RX' if rx else '/UART2_TX', jumper='R57' if rx else 'R56')
                pads['J2'][row['pad']] = row['net']
        with patch('check_connector_pinout.pcb_pads', return_value=pads):
            self.assertTrue(any('UART direction' in e for e in check(self.board, rows)))

    def test_wrong_mcu_uart_pin_rejected(self):
        pads = copy.deepcopy(self.pads)
        pads['R56']['2'] = 'Net-(U5-GPIO35)'
        with patch('check_connector_pinout.pcb_pads', return_value=pads):
            self.assertTrue(any('R56: UART MCU endpoint' in e for e in check(self.board, self.rows)))

    def test_changed_power_pin_rejected(self):
        pads = copy.deepcopy(self.pads)
        pads['J2']['B25'] = 'GND'
        with patch('check_connector_pinout.pcb_pads', return_value=pads):
            self.assertTrue(any('J2:B25' in e for e in check(self.board, self.rows)))


if __name__ == '__main__':
    unittest.main()
