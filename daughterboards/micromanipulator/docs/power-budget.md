# Logic supply review

The board draws 12 V and 5 V from the existing DIN96 contacts. U2 converts the existing 5 V rail to 3.3 V. It is now **AP2112M-3.3TRG1 in SO-8**, replacing the smaller AP2112K package. No rail, backplane contact or external connector changed.

## Current allocation

| Load on 3.3 V | Allocation | Basis |
| --- | ---: | --- |
| Four MT6835 encoders | 112 mA | Four times the manufacturer's 28 mA maximum supply current |
| RP2350B, including core conversion and I/O | 100 mA | Engineering allowance; not a measured or guaranteed workload maximum |
| Flash, bridge logic, pull-ups and margin | 38 mA | Remaining provisional allocation; check with final parts and firmware |
| **Design budget** | **250 mA** | To be confirmed on assembled hardware with all sensors attached |

The encoder limit comes from the [MT6835 electrical characteristics](https://www.magntek.com.cn/upload/pdf/202407/MT6835_Rev.1.3.pdf). Additional sensor-board LEDs or loads must fit inside the remaining allowance. Motor, heater and pump currents are separate 12 V/5 V loads and are not included here. Their combined demand must respect the host supply and connector limits.

## Thermal estimate

For an assumed high input of 5.25 V and low output of 3.25 V, U2 dissipates approximately `2.0 × Iout` watts. The [AP2112 datasheet](https://www.diodes.com/assets/Datasheets/AP2112.pdf) lists junction-to-ambient thermal resistance of 114 °C/W for SO-8, versus 184 °C/W for SOT25. Using those figures:

| 3.3 V current | Dissipation | Estimated SO-8 junction at 50 °C ambient |
| --- | ---: | ---: |
| 100 mA | 0.20 W | 73 °C |
| 250 mA | 0.50 W | 107 °C |
| 350 mA | 0.70 W | 130 °C |

At 250 mA the old SOT25 estimate was 142 °C. SO-8 therefore provides useful margin against a 125 °C design target. These are first-order estimates using datasheet thermal resistance, not measured board temperatures or a guaranteed ambient rating. The regulator's 600 mA electrical rating is **not** this board's continuous thermal rating. Measure the 3.3 V current and regulator temperature under the final worst-case workload, with adjacent cards and enclosure airflow represented. Revisit the package/cooling if current exceeds the allocation or local ambient exceeds 50 °C.

Both U2 ground pins have short, solid copper connections to a local ground via and the filled ground network. C1 connects directly to VIN8 and C2 directly to VOUT1 on F.Cu. The SO-8 pin assignment was checked against the manufacturer: VOUT1, NC2/3/4, EN5, GND6/7, VIN8.

## Local capacitor selection

C1 and C2 now use **4.7 µF / 16 V / X5R / 0603 Samsung CL10A475KO8NNNC**, replacing their unselected 1 µF values. C10 uses the same part at its existing 4.7 µF nominal value. All three footprints and their direct traces remain unchanged. The AP2112 datasheet specifies operation with a 1 µF capacitor and recommends X5R/X7R ceramics; the larger local values provide allowance for capacitance loss under bias. C3's separate output bulk capacitor remains.

Samsung's [published typical bias data](https://product.samsungsem.com/mlcc/CL10A475KO8NNN.do), interpolated at the design voltages, gives:

| Location | Bias | Typical biased capacitance | Engineering screening estimate |
| --- | ---: | ---: | ---: |
| C1, regulator input | 5.25 V | 2.25 µF | 1.23 µF |
| C2, regulator output | 3.40 V | 3.21 µF | 1.75 µF |

The screening estimate multiplies the typical biased value by 0.90 for initial tolerance, 0.85 for temperature, 0.79 for small-signal reduction and an additional 0.90 aging allowance. The latter two are engineering allowances informed by the typical data, not guaranteed combined-condition limits. This supports the selection; it does not replace startup/load-step checks on hardware. The part is listed as [JLCPCB C19666](https://jlcpcb.com/partdetail/CL10A475KO8NNNC/C19666). No arbitrary same-value substitution is approved without checking bias behavior.

The exact SO-8 regulator is listed for assembly as [JLCPCB C5290219](https://jlcpcb.com/partdetail/DiodesIncorporated-AP2112M_33TRG1/C5290219). Catalog identity and package were checked on 2026-11-07; inventory and assembly availability at ordering time are not confirmed.

## Gate-driver supply and an open load fuse

U11 (TC4427A) and its C64/C65 bypass capacitors now use **+5V_BP**, ahead of F1. The load outputs and the rotation drivers' motor supply remain on **+5V_LOAD**, after F1. The [Microchip datasheet](https://ww1.microchip.com/downloads/en/DeviceDoc/20001423J.pdf), page 3, limits either input to VDD + 0.3 V. With the previous connection, an open F1 could remove U11's supply while the RP2350 still drove its inputs at 3.3 V. Taking U11's supply from the same upstream 5 V source as the logic regulator removes that particular fault condition. The driver draws logic/gate-charge current, not load current, from this rail.

Only U11.6, C64.1 and C65.1 change electrical net membership. The ToolOutputs hierarchy now explicitly shows its existing backplane 5 V feed; no physical connector or backplane contact changes. The 1.795 mm C64-to-U11 trace and both capacitors' local ground returns are retained. A manually routed 0.4 mm supply feed uses In1 with short front/back bridges and four additional 0.6/0.3 mm through vias. This keeps all inner power regions and the ground plane connected without moving the local bypass components or existing signal traces.

Native netlist and board comparisons check the three intended pin changes and preserve all other electrical assignments, footprint placement, pad geometry and existing copper geometry. `scripts/check_power_domains.py` checks this fuse-domain requirement. Full supply removal/brownout behavior and final load currents still require bring-up verification; this change is not a general power-sequencing qualification.
