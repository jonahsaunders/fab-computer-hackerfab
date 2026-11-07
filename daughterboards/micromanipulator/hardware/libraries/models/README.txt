Models used by the current 116-component board are bundled here.
KiCad standard STEP models retain their original geometry and transforms.
RP2350B, DRV8837C and TB6612FNG have explicitly approximate, nominal VRML models.
The Toshiba SSOP24 model uses a 5.6 x 7.8 mm body, 0.65 mm lead pitch and
7.6 mm lead span; see docs/controller-parts-review.md for drawing provenance.
HRO USB-C uses the community STEP model documented in Connector_USB.3dshapes/README.txt.
The earlier HRO envelope file is retained but is not used by the current board.
The DIN plug uses the WingTAT-specific STEP extracted unchanged from the host
library; see Connector_DIN.3dshapes/README.txt for provenance and alignment.
USB-C opening faces the left card edge. JST PH connectors mate above the component face.
L2 retains its embedded upstream STEP model in the footprint/PCB.
These are visual assembly aids; exact mating tolerances remain defined by manufacturer drawings.
See the project licenses/kicad-library-attribution.txt and docs/model-inventory.csv.
