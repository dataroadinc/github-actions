# Publish tested crate

Call after all checks pass, from the exact validated revision with the generated
Cargo.lock present. Supply `CARGO_REGISTRY_TOKEN` through the calling step's env.
The action publishes via Cargo. If that version already exists (for example when
npm failed after Rust publication), it checks the published archive's VCS revision
against the validated SHA. An unrelated existing version or registry error fails.

The crate must retain `.cargo_vcs_info.json` in its package. Release completion
belongs after all registry publications; leave the GitHub release draft until then.
