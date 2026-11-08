# System architecture

The unchanged backplane distributes power and shared buses to three DIN96 slots. Its RP2350B host coordinates the system. The [motion daughtercard](../daughterboards/micromanipulator/) uses one bare RP2350B for local motion feedback, rotation and tool control; a shallow encoder card in another slot breaks out the shared SPI0 bus to three existing sensor PCBs.

The motion controller is the only SPI0 master. Host GPIO16–21 and other slot users must remain undriven, with host pulls disabled. The host can still use SPI1. Host J1/J2 provide UART; J3 does not. No connector contacts or host circuitry were changed. The [bus/contact map](../daughterboards/micromanipulator/docs/backplane-encoder-bus.md) gives the exact allocation and firmware constraints.

Both cards obtain 3.3 V locally from the existing 5 V rail. Motion also uses existing 12 V for its axis drivers. The 5 V mux's 2.5 A system limit includes host, cards, sensors and tools. See [power limits](../daughterboards/micromanipulator/docs/load-power-review.md). This is development hardware; firmware migration, signal integrity, physical mating and actual load validation remain open.
