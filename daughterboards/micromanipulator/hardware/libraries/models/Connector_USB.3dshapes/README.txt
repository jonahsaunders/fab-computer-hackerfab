HRO TYPE-C-31-M-12 community STEP model

Source: Nabu Casa, Yellow 3D-shapes library
https://github.com/NabuCasa/yellow-3dshapes/blob/main/USB_C_Receptacle_HRO_TYPE-C-31-M-12.step
Nabu Casa's README attributes the original to ai03 and a FreeCAD/KiCadStepUp conversion:
https://github.com/NabuCasa/yellow-3dshapes/blob/main/README.txt
https://github.com/ai03-2725/Type-C.pretty/blob/master/HRO%20TYPE-C-31-M-12.step

Retrieved 2026-11-07. Unmodified STEP contents:
Git blob SHA-1: 5d46208ae29a5c86fb05b1678496a7d2b049c58b
SHA-256: f411d3d68f01cc82e818e0b4f8996ade52079af802cc1fdf169898b9e523423b
The upstream README does not state a standalone license for this model.
This source attribution is retained; the model is not claimed as new project geometry.

KiCad placement in Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12:
Scale 1,1,1; rotation 270,0,0 degrees; offset -4.47,-3.65,0 mm.
The transform only aligns the model. Existing footprint pads and connector position
are unchanged. The model's opening faces local +Y in footprint coordinates,
which faces off the left card edge for J18's -90 degree board rotation.

Geometry review:
- Twelve distinct contact X centres match the footprint (four supply/ground pairs
  are represented by coincident A/B pad numbers in the native footprint).
- Metal contact widths are 0.20/0.40 mm inside the 0.30/0.60 mm lands; contact
  length occupies local Y -4.25 to -3.65 mm, within the 1.45 mm long solder lands.
- Four shell-tab X centres are +/-4.32 mm. Y centres differ from the footprint
  by only 0.005 mm (-3.125 vs -3.13; +1.055 vs +1.05 mm).
- Native KiCad renders confirm shell/contact alignment and outward access.

This is a community reference model, not a manufacturer-certified tolerance model.
Its nominal shell is 8.94 x 7.30 mm and its maximum height is 3.21 mm; HRO's current
product listing gives 8.94 x 7.35 x 3.16 mm. Use the current ordered part's mechanical
drawing for final enclosure tolerances. Manufacturer and assembly references:
https://www.krhro.com/Product-Details/726.html
https://jlcpcb.com/partdetail/C165948
