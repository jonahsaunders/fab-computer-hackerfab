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

Both U2 ground pins have short, solid copper connections to a local ground via and the filled ground network. C1 connects directly to VIN8 and C2 directly to VOUT1 on F.Cu. The SO-8 pin assignment was checked against the manufacturer: VOUT1, NC2/3/4, EN5, GND6/7, VIN8. The existing 1 µF X7R input/output capacitors are retained. Their final ordering parts must retain sufficient effective capacitance under bias.

The exact SO-8 regulator is listed for assembly as [JLCPCB C5290219](https://jlcpcb.com/partdetail/DiodesIncorporated-AP2112M_33TRG1/C5290219). Catalog identity and package were checked on 2026-11-07; inventory and assembly availability at ordering time are not confirmed.
