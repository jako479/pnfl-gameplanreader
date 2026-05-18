# fbpro98-gameplanreader — Test Status

**Test Status: Tests Complete**

## Covered by automated tests

- `GamePlanReader` get/write methods for normal and custom special plays, against golden text fixtures for both offense and defense gameplans.
- Slot-order and name-order sorting, including blank-slot handling and fixed counts (64 normal, 10 special).
- CLI argparse contract: required path, sort choices, `-` stdout token, and rejection of identical output file paths.
- All `main()` output modes — headered stdout, headerless single/combined `-` stdout, file output, and mixed dash/file routing — pinned to fixtures.

## Needs tests

- Nothing outstanding for the current scope.
