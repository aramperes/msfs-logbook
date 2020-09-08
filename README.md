# MSFS Logbook

A project to reverse-engineer the specification for the Microsoft Flight Simulator's logbook file.

The logbook file is a binary file located in `<Steam Installation>\userdata\<Steam ID>\1250410\remote\kh_logbook`.

The file is updated whenever the player ends a flight.

## Objective

The goal of this repository is to write a spec for the MSFS logbook format.

When the spec is near complete, we should add unit tests with real logbooks to ensure its compatibility.

In the end, this could be used to write proper libraries to read, update, and write logbook files for many purposes, including:

 * Retrieving the list of itineraries to render on a map
 * Removing entries from a logbook
 * Adding missing entries from a logbook

## MSFS Logbook Format Spec

> ⚠️ This is a work-in-progress! Contributions are welcome.

### File Structure

| Field Name    | Field Type                     | Notes  |
|---------------|--------------------------------|--------|
| File Version  | 32-bit Int                     | Not sure without analyzing future versions. Appears to be constant `8` |
| Total Flights | 32-bit Int                     | Appears to be 1 more than the actual size |
| Flights       | Sequence of Flight (see below) |        |

### `ASCII String` Object

| Field Name            | Field Type                     | Notes  |
|-----------------------|--------------------------------|--------|
| Length                | 32-bit Int                     | Size of ASCII Character Array |
| ASCII Character Array | Sequence of bytes              | ASCII characters. May terminate with NULL |


### `Flight` Object

| Field Name    | Field Type              | Notes  |
|---------------|-------------------------|--------|
|                      | 24 bytes         | Unknown fields |
| Player Start Time    | 32-bit Int       | Epoch timestamp |
|                      | 32-bit Int       | Unknown value; appears to be constant `0` |
| Flight Type          | ASCII String     | Example values: `asobo-flight-tutorials-basiccontrols`, `asobo-freeflights` |
| Flight Start Year    | 16-bit Int       | Example value: `2018` |
| Flight Start Month   | 16-bit Int       | Example value: `9` (for September) |
| Flight Start Day     | 16-bit Int       | Example value: `7` (for 7th day of the month) |
| Flight Start Hour    | 16-bit Int       | Example value: `22` (for 22th hour of the day) |
| Flight Start Minute  | 16-bit Int       | Example value: `40` (for 40th minute of the hour) |
|                      | 10 bytes         | Unknown fields |
| Itinerary Departure  | ASCII String     | Example values: `KSEZ`, `CYUL`. TBD: how are custom coordinates encoded? |
| Itinerary Arrival    | ASCII String     | Example values: `KSEZ`, `CYUL`. TBD: how are custom coordinates encoded? |
|                      | 30 bytes         | Unknown fields |
| Plane Model Source   | ASCII String     | Example value: `Asobo Studio` |
|                      | 8 bytes          | Unknown fields |
| Plane Model Type     | ASCII String     | Example value: `PLANETYPE_PROPELLER` |
| Plane Model ID       | ASCII String     | Example value: `asobo-aircraft-c152` |
| Plane Model Name     | ASCII String     | Example value: `Cessna 152 Asobo` |
|                      | 26 bytes         | Unknown fields |
| Weather              | ASCII String     | Example value: `TT:MENU.WEATHERTYPE_3FEW_CLOUDS`. TBD: how is Live Weather encoded? |
|                      | ??? bytes        | Many more fields to research! |

## Missing fields

Some fields are likely stored in the `Flight` object:

* Start Time and End Time (appear to differ from Flight Start Year/Month/Day/Hour/Minute in tutorials)
* Wind Speed and Direction
* Departure Gate or Runway
* Arrival Gate or Runway
* Flight settings (assistance, auto-pilot, etc.)
* Flight events (take-off, taxi, pause, etc.)

## Disclaimer

This repository is licensed under MIT.

This project IS NOT affiliated with Microsoft, Asobo Studios, or MS Flight Simulator in general.
