# Tag tested release

Call only after every validation/build job succeeds, using the revision output
from `prepare-cargo-release`. Requires a full checkout and `contents: write`.
Validates the manifest at that revision and creates/pushes its annotated version
tag. An existing tag must resolve to exactly that commit; conflicts are fatal.
Create a draft GitHub release afterward and finalize it only after publication.
