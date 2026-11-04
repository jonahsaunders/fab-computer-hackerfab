# Backplane design audit — 2026-11-04

**Disposition: development hardware; not ready for a manufacturing release.** The static review found issues and missing validation. Zero PCB connectivity errors does not establish correct system behavior. The supplied design, all seven schematic sheets, PCB, library dependencies, connector assignments, power paths, and principal component pinouts were reviewed with KiCad 10.0.6 and manufacturer documentation. No physical board, daughter-board designs, firmware, measured loads, or bench results were available.

The intended operating case is a **current-limited variable bench supply connected through the nominal 24 V input**. No maximum 12 V, 5 V, or 3.3 V loads were specified. A current limit at the 24 V input does not impose the same current limit on a buck converter's output, nor does it protect a separately attached USB source.

## Changes included in this update

- Imported the active files from both supplied ZIPs, retaining portable project library tables. The new source adds R56/R57 and an independent UART on J2. Archive hashes and file-by-file comparisons are in [provenance](provenance.md) and the [import manifest](audit/2026-11-04/import-manifest.json).
- Refilled and saved copper zones. The as-supplied saved fills produced **24 errors**: 14 copper-clearance and 10 drill-to-copper-clearance violations around changed routing. Refill removed all 24. This matters because manufacturing exports use copper fills, not merely net names.
- Corrected the PCB's obsolete `TX/1` and `RX/1` legend to `TX*`, `RX*`, with `J1=UART0; J2=UART1; J3=NC`. The new second UART was already wired in the supplied source.
- Corrected U5's description from “2MB flash” to “external QSPI flash” in the library, cached schematic symbol, placed symbol, and PCB metadata. The part remains RP2350B; U7 remains the external W25Q128JVSIQ.
- Updated the connector reference, added regression checks for UART direction and MCU endpoints, and refreshed previews and validation exports.

No component substitutions, new circuits, trace/via moves, or relaxed design rules were introduced during the audit. Comparing parsed board records against the imported PCB confirmed that all 1,114 trace segments, 267 vias, 148 footprint geometries, and zone definitions are unchanged, apart from the stated U5 description; only derived copper fills and the UART silkscreen changed. Of 41 imported files, 38 remain identical after line-ending normalization. The three deliberate exceptions are the PCB, microcontroller schematic, and `Hack_Chips.kicad_sym`.

## Findings requiring design decisions or measurements

### A1 — I²C has no backplane pull-ups

**Confirmed gap in the supplied backplane; system operation depends on missing daughter-board details.** Each of `/I2C0_SCL`, `/I2C0_SDA`, `/I2C1_SCL`, and `/I2C1_SDA` connects the three slots to a zero-ohm MCU jumper, with no external pull-up resistor on the backplane. Do not assume that enabling the MCU's weak pull-ups will satisfy timing over three connectors.

Specify one effective pull-up network per bus, to a compatible 3.3 V source, and size it from total bus capacitance, operating speed, and sink-current limits. Account for parallel pull-ups if daughter boards provide them. The DIN connectors do not distribute a 3.3 V rail, so a daughter-board implementation needs its own suitable source. Verify SCL/SDA rise times with the actual boards attached. [NXP I²C specification, section 7.1](https://cache.nxp.com/docs/en/user-guide/UM10204.pdf)

### A2 — AUX10 is not implemented as an MCU signal

**Confirmed incomplete connection.** `/AUX10` has only one electrical endpoint: J3:C19. There is no corresponding MCU connection or jumper. Its isolated-label ERC warning is meaningful, even though PCB DRC reports zero unrouted items: a single-pad net requires no route.

Treat AUX10 as reserved/unavailable in daughter boards until a suitable GPIO is selected and connected in both schematic and layout. AUX1–9 have MCU jumper paths. Do not infer ten working GPIO channels from the connector legend.

### A3 — The shared 5 V rail is constrained by U6, including during USB fallback

**Confirmed topology and rating constraint; operating load remains unknown.** U2 feeds U6 through R11. U6's output supplies the three slots' 5 V pins, J6, and U3. TPS2116 is specified for **2.5 A maximum continuous current**; the upstream TPS5450's 5 A headline rating does not make this a 5 A backplane rail. U6 must not be treated as a programmable load-current limiter. Budget the aggregate load with thermal margin and verify the zero-ohm jumpers, connectors, copper, and fuse against it. [TI TPS2116 datasheet](https://www.ti.com/lit/ds/symlink/tps2116.pdf)

When the 24 V supply is absent or its 5 V converter falls below the selection threshold, USB can supply the **entire same 5 V rail**, including daughter boards. R53/R54 set a nominal 4.3 V priority threshold; using the reference tolerance and 1% divider tolerances gives approximately 3.90–4.72 V. Current limiting the bench supply can therefore trigger a transfer to USB during a load transient. Source capability must be established before using this fallback with daughter boards. The two 5.1 kΩ CC resistors identify a USB-C sink; they do not by themselves establish a usable high-current allocation.

Decide whether USB should power all 5 V loads or only the controller. If the present topology is retained, document and enforce a load limit compatible with every selected source, including USB. No assumption that USB is controller-only was made.

### A4 — The RP2350 core regulator needs layout and startup validation

**Validation risk, not a demonstrated failure.** L3 is Murata DFE252012F-3R3M=P2; C32/C36 are 4.7 µF, 6.3 V in 0603. R55/C42 provide the 33 Ω / 4.7 µF VREG_AVDD filter. The core regulator's nominal connections are correct.

Raspberry Pi's hardware guide specifically discusses regulator sensitivity to inductor magnetic orientation and local layout, illustrates an orientation-marked Abracon part, and recommends compact capacitor placement. Matching inductance alone does not validate this alternate part and layout. Check the actual L3 orientation and loop geometry against the guide, then scope 1.1 V startup, ripple, and load transients over the intended input and temperature range. Include repeated cold starts and maximum MCU activity. [Raspberry Pi hardware design guide](https://datasheets.raspberrypi.com/rp2350/hardware-design-with-rp2350.pdf), [Murata DFE252012F series](https://www.murata.com/~/media/webrenewal/products/inductor/chip/tokoproducts/wirewoundmetalalloychiptype/m_dfe252012f.ashx)

### A5 — Both buck converters need stability and thermal validation

**Unvalidated design margin.** Each output uses two parallel 220 µF polymer capacitors, nominally 440 µF total. The supplied capacitor metadata specifies 35 mΩ maximum ESR per capacitor; two in parallel give at most 17.5 mΩ under the same measurement conditions. This places the nominal ESR zero at approximately 20.7 kHz or higher. That calculation is not a stability proof: capacitance, ESR versus frequency/temperature, tolerances, and operating point matter.

TPS5450 uses internal compensation with output-capacitor/ESR selection requirements. Validate both converters with an appropriate loop analysis or measured loop gain and load-step response, including startup, no-load, current-limited-input operation, and maximum planned loads. Check effective capacitance of the 50 V ceramic input capacitors at 24 V bias. [TI TPS5450 datasheet](https://www.ti.com/lit/ds/symlink/tps5450.pdf)

L1/L2 are 15 µH CDRH127/LD parts. Their listed saturation-current rating does not independently establish a permissible continuous rail current; include ripple, ambient temperature, copper loss, and diode/regulator heating. [Sumida CDRH127/LD data](https://products.sumida.com/products/pdf/CDRH127LD%20(en).pdf)

### A6 — USB behavior while powered from 24 V is incomplete

**No VBUS sensing path was found.** `+5V_USB` connects J7, C38, and U6 VIN2, without a MCU detector. The MCU can remain powered from 24 V after host VBUS disappears. A self-powered USB device needs a way to observe VBUS and control its attach/pull-up behavior; no firmware or external sensing circuit establishing that behavior is supplied. Add an appropriate voltage-safe detector and firmware policy before claiming compliant self-powered USB behavior. [ST USB hardware guidance, sections 2.6 and 3.1.1](https://www.st.com/resource/en/application_note/an4879-introduction-to-usb-hardware-and-pcb-guidelines-using-stm32-mcus-stmicroelectronics.pdf)

U4's USBLC6 VBUS/clamp-reference pin is tied to 3.3 V, not to `+5V_USB`. D+/D− are routed through its protection channels, but that connection does not protect USB's incoming 5 V net directly. No separate USB VBUS clamp or external current-limiting device is shown. Assess the chosen clamp reference, injection into 3.3 V, connector ESD, cable hot-plug, and source switching as a system. This is not a claim that U4 pin 5 must simply be moved to 5 V. [ST USBLC6-2 datasheet](https://www.st.com/resource/en/datasheet/usblc6-2.pdf)

### A7 — Thermal/current limits are not established for all rails

The AP2112's nominal 600 mA capability is not a safe load budget at every voltage drop. At 5 V to 3.3 V and 600 mA, U3 alone dissipates about **1.02 W**. Its SOT-25 package thermal resistance under the datasheet test conditions is approximately 184 °C/W; that would imply roughly 188 °C junction rise. Actual board conditions differ, but this is enough to reject an unqualified 600 mA system claim. Measure the real 3.3 V load and temperature. [Diodes AP2112 datasheet](https://www.diodes.com/assets/Datasheets/AP2112.pdf)

F1 is a nominal 5 A input fuse, not a precise current regulator. No documented per-slot fault limits, aggregate rail budget, or copper temperature-rise analysis is present. Record maximum continuous and transient loads before assigning bench supply limits. Protect the weakest downstream branch rather than relying only on total 24 V input current.

### A8 — Manufacturing rules and assembly details still need release review

The custom-rule header says four layers with 1 oz outer / 0.5 oz inner copper, while the PCB stackup declares 0.035 mm copper on all four layers. Only the default net class is configured; no USB differential-impedance target is encoded. Reconcile the actual fabricator stackup with clearance rules, copper-weight assumptions, and USB geometry. The supplied generic clearance rule permits 0.09 mm; successful DRC against that rule is not a fabricator approval.

The final saved board still reports **362 silkscreen/text warnings**. Two are silk-to-edge clearance warnings. Review clipping, legibility, and component/pad overlap before assembly. A stricter review also found three track endpoints not centered on their vias and a stale crystal footprint filter. None creates an unrouted item, but they should be resolved or intentionally documented for a release. Critical IC/protection pad numbering was cross-checked; a complete procurement and mechanical sign-off of every passive and connector variant remains outstanding. Check physical mating orientation, housing clearances, mounting hardware, and component height with the actual daughter boards.

## Checks that passed or explain apparent errors

| Area | Result and limits |
| --- | --- |
| Schematic/PCB agreement | 148 components and 148 footprints; zero normal parity findings; zero unconnected PCB items. All 288 DIN contacts checked against the updated reference and fresh netlist. |
| UARTs | J1 A20 RX → R27 → GPIO1 / U5:78; C20 TX → R26 → GPIO0 / U5:77. J2 A20 RX → R57 → GPIO37 / U5:46; C20 TX → R56 → GPIO36 / U5:45. J3 A20/C20 are NC. |
| UART naming | The design's `UART2` label means the second connector UART. GPIO36/37 select hardware UART1; GPIO0/1 select UART0. RP2350 does not have a hardware UART2. |
| MCU pin mapping | RP2350B QFN-80 pin numbering and exposed pad checked, including IOVDD, DVDD, ADC_AVDD, USB_OTP_VDD, QSPI_IOVDD, VREG pins, and ground. SPI0/1 and I²C0/1 pin-function selections are consistent; additional SPI chip selects need firmware control. |
| External flash and clock | U7 has the expected QSPI signal/power connections. RP2350B needs external flash, supplied by U7. The 12 MHz crystal, 15 pF loads, 1 kΩ XOUT resistor, and BOOTSEL/RUN switch paths were reviewed. Oscillator margin and programming still need physical tests. |
| USB connector | Both receptacle orientations join the proper D+/D− contacts; separate 5.1 kΩ CC pull-downs and 27 Ω data-series resistors are present. This does not constitute USB signal-integrity or compliance testing. |
| Input protection | J4 → F1 → Q1 → protected 24 V is consistent with the P-channel reverse-polarity arrangement. Q1 G1/D2/S3/tab-D and D8 polarity match the intended circuit; D7's IN/GND/exposed-pad assignments match its pinout. |
| Buck topology | U1/U2 power/ground/exposed-pad pins, bootstrap capacitors, catch-diode polarity, inductors, and feedback were checked. Feedback gives about 12.026 V and 5.085 V nominal. Floating TPS5450 ENA is allowed by its internal pull-up; the explicit no-connect symbols are not themselves an error. |
| Power mux | TPS2116 VOUT pins 2 and 7 are intentionally the same output. The ERC power-output conflict is caused by symbol pin types, not two independent supplies being shorted. |
| Local libraries | All referenced custom symbols/footprints resolve through relative project paths. Seven symbol libraries and 24 custom footprints are bundled. The four ordinary library-mismatch warnings concern Q1 and C6/C12/C13 metadata, with matching pin definitions. |

The pin-function and core pinout checks use the [RP2350 datasheet](https://datasheets.raspberrypi.com/rp2350/rp2350-datasheet.pdf). The protection review also used the [DMP6023LE datasheet](https://www.diodes.com/assets/Datasheets/DMP6023LE.pdf) and [TVS2700 datasheet](https://www.ti.com/lit/ds/symlink/tvs2700.pdf).

The protection circuit is intended for nominal 24 V operation. D7's 27 V standoff is not a continuous overvoltage regulator. At nominal 24 V, the 12 V gate clamp and two series 1.13 kΩ resistors draw approximately 5.3 mA and dissipate about 32 mW per resistor. At a hypothetical 36 V steady input this becomes approximately 127 mW per resistor, above the listed 0.1 W rating. Do not interpret the buck IC's input-voltage range as the whole backplane's operating range.

## ERC and rule-setting review

The [validation baseline](validation.md) provides counts and links to machine-readable evidence. The eight `power_pin_not_driven` errors mostly arise because KiCad cannot infer sources through passive fuse, MOSFET, inductor, jumper, or filter paths. Add targeted power flags or improve power pin models only after each real source is verified. The ninth error is U6's duplicate VOUT modeling conflict. None was hidden by a new exclusion.

The six warnings include the meaningful AUX10 isolated label, a `+3V3`/`3V3` naming overlap, and four cached/library metadata mismatches. The audit also enabled every normally ignored ERC/DRC severity in a temporary project: this exposed Y1's stale `RPI_COMPILED` footprint filter and three off-center via endpoints. The actual Y1 footprint resolves from `Hack_Oscillators`. The original project severities were preserved, and all findings are disclosed.

Procurement metadata needs cleanup before ordering. For example, R56/R57's datasheet URL points to a different resistor family than their stated part identifier; R6/R11 lack datasheet links; the core-output capacitors need explicit qualified part numbers and bias/temperature data. A valid footprint reference does not establish a correct purchasing part.

## Bring-up and release exit criteria

1. Resolve A1/A2 and the intended USB fallback behavior; publish maximum rail and per-slot loads. Reconcile the fabrication stackup and remaining rule findings. Freeze the BOM with verified package/pin-1 drawings.
2. Inspect the assembled board unpowered for shorts and polarity. Begin with daughter boards and USB disconnected. Use nominal 24 V with a conservative initial current limit; measure protected input, 12 V, 5 V, 3.3 V, and 1.1 V before attaching loads. Record actual input current and temperatures. Do not increase the limit merely to overcome unexplained heating or repeated startup cycling.
3. Test both bucks and the core regulator with representative load steps, startup/shutdown cycles, and the planned supply range. Capture ripple, overshoot, settling, and temperatures. Validate current-limit recovery and U6 switching without a valuable USB host attached.
4. Program/debug via SWD; verify flash boot, oscillator behavior, both UART directions, all SPI chip selects, AUX1–9, and both I²C buses with measured rise times. Check USB enumeration in both cable orientations and disconnect behavior while 24 V remains present.
5. Test the complete system with the actual daughter boards, cables, and USB source. Confirm total current, fault behavior, signal timing, connector mechanics, and ESD/hot-plug behavior. Archive measurements, firmware revision, assembly BOM, and final fabrication outputs against one exact commit.

This audit is a static engineering review with reproducible design checks. It does not replace these measurements or certify that the hardware has no mistakes.
