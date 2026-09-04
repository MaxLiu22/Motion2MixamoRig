# Release checklist

## Repository

- [ ] Working tree is clean
- [x] Version numbers are consistent
- [x] No gated models, weights, Mixamo assets, or user inputs are tracked
- [x] README instructions match the current CLI
- [x] CHANGELOG is updated
- [x] Release notes are prepared

## Validation

- [x] Package imports successfully
- [x] CLI help works
- [x] `m2mr doctor` runs and reports environment status
- [x] Video pipeline smoke test completed
- [x] Image pipeline smoke test completed
- [x] Generated NPZ files load successfully
- [x] Generated GLB imports into Blender

## Publishing

- [ ] Release preparation commit is pushed
- [ ] Annotated tag is created
- [ ] Tag is pushed
- [ ] GitHub Release is created
- [ ] Release URL opens successfully
