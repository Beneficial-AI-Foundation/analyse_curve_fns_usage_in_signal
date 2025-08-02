# curve25519-dalek Public API Reference

## Module: `scalar`

### Type: `Scalar`
- `pub fn from_bytes_mod_order(bytes: [u8; 32]) -> Scalar`
- `pub fn from_bytes_mod_order_wide(input: &[u8; 64]) -> Scalar`
- `pub fn from_canonical_bytes(bytes: [u8; 32]) -> CtOption<Scalar>`
- `pub const fn from_bits(bytes: [u8; 32]) -> Scalar`
- `pub fn random<R: CryptoRng + ?Sized>(rng: &mut R) -> Self`
- `pub fn hash_from_bytes<D>(input: &[u8]) -> Scalar`
- `pub fn from_hash<D>(hash: D) -> Scalar`
- `pub const ZERO: Self`
- `pub const ONE: Self`
- `pub const fn to_bytes(&self) -> [u8; 32]`
- `pub const fn as_bytes(&self) -> &[u8; 32]`
- `pub fn invert(&self) -> Scalar`
- `pub fn batch_invert(inputs: &mut [Scalar]) -> Scalar`

### Type: `UnpackedScalar`
- `pub fn montgomery_invert(&self) -> UnpackedScalar`
- `pub fn invert(&self) -> UnpackedScalar`

### Standalone Function
- `pub const fn clamp_integer(mut bytes: [u8; 32]) -> [u8; 32]`

## Module: `edwards`

### Type: `CompressedEdwardsY`
- `pub const fn as_bytes(&self) -> &[u8; 32]`
- `pub const fn to_bytes(&self) -> [u8; 32]`
- `pub fn decompress(&self) -> Option<EdwardsPoint>`
- `pub fn from_slice(bytes: &[u8]) -> Result<CompressedEdwardsY, TryFromSliceError>`

### Type: `EdwardsPoint`
- `pub fn to_montgomery(&self) -> MontgomeryPoint`
- `pub fn to_montgomery_batch(eds: &[Self]) -> Vec<MontgomeryPoint>`
- `pub fn compress(&self) -> CompressedEdwardsY`
- `pub fn compress_batch(inputs: &[EdwardsPoint]) -> Vec<CompressedEdwardsY>`
- `pub fn hash_to_curve<D>(bytes: &[&[u8]], domain_sep: &[&[u8]]) -> EdwardsPoint`
- `pub fn random<R: RngCore + ?Sized>(rng: &mut R) -> Self`
- `pub fn mul_base(scalar: &Scalar) -> Self`
- `pub fn mul_clamped(self, bytes: [u8; 32]) -> Self`
- `pub fn mul_base_clamped(bytes: [u8; 32]) -> Self`
- `pub fn vartime_double_scalar_mul_basepoint(a: &Scalar, A: &EdwardsPoint, b: &Scalar) -> EdwardsPoint`
- `pub fn mul_by_cofactor(&self) -> EdwardsPoint`
- `pub fn is_small_order(&self) -> bool`
- `pub fn is_torsion_free(&self) -> bool`

## Module: `edwards/affine`

### Type: `AffinePoint`
- `pub fn to_edwards(self) -> EdwardsPoint`
- `pub fn compress(self) -> CompressedEdwardsY`

## Module: `ristretto`

### Type: `CompressedRistretto`
- `pub const fn to_bytes(&self) -> [u8; 32]`
- `pub const fn as_bytes(&self) -> &[u8; 32]`
- `pub fn from_slice(bytes: &[u8]) -> Result<CompressedRistretto, TryFromSliceError>`
- `pub fn decompress(&self) -> Option<RistrettoPoint>`

### Type: `RistrettoPoint`
- `pub fn compress(&self) -> CompressedRistretto`
- `pub fn double_and_compress_batch<'a, I>(points: I) -> Vec<CompressedRistretto>`
- `pub fn random<R: CryptoRng + ?Sized>(rng: &mut R) -> Self`
- `pub fn try_from_rng<R: TryCryptoRng + ?Sized>(rng: &mut R) -> Result<Self, R::Error>`
- `pub fn hash_from_bytes<D>(input: &[u8]) -> RistrettoPoint`
- `pub fn from_hash<D>(hash: D) -> RistrettoPoint`
- `pub fn from_uniform_bytes(bytes: &[u8; 64]) -> RistrettoPoint`
- `pub fn mul_base(scalar: &Scalar) -> Self`
- `pub fn vartime_double_scalar_mul_basepoint(a: &Scalar, A: &RistrettoPoint, b: &Scalar) -> RistrettoPoint`

### Type: `RistrettoBasepointTable`
- `pub fn create(basepoint: &RistrettoPoint) -> RistrettoBasepointTable`
- `pub fn basepoint(&self) -> RistrettoPoint`

## Module: `montgomery`

### Type: `MontgomeryPoint`
- `pub fn mul_base(scalar: &Scalar) -> Self`
- `pub fn mul_clamped(self, bytes: [u8; 32]) -> Self`
- `pub fn mul_base_clamped(bytes: [u8; 32]) -> Self`
- `pub fn mul_bits_be(&self, bits: impl Iterator<Item = bool>) -> MontgomeryPoint`
- `pub const fn as_bytes(&self) -> &[u8; 32]`
- `pub const fn to_bytes(&self) -> [u8; 32]`
- `pub fn to_edwards(&self, sign: u8) -> Option<EdwardsPoint>`

### Type: `ProjectivePoint`
- `pub fn as_affine(&self) -> MontgomeryPoint`

## Module: `field`

### Type: `FieldElement`
- `pub fn hash_to_field<D>(bytes: &[&[u8]], domain_sep: &[&[u8]]) -> Self`

## Module: `window`

### Type: `LookupTableRadix16<T>`
- `pub fn select(&self, x: i8) -> T`

### Type: `NafLookupTable5<T>`
- `pub fn select(&self, x: usize) -> T`

### Type: `NafLookupTable8<T>`
- `pub fn select(&self, x: usize) -> T`

## Module: `backend`

### Standalone Functions
- `pub fn pippenger_optional_multiscalar_mul<I, J>(scalars: I, points: J) -> Option<EdwardsPoint>`
- `pub fn straus_multiscalar_mul<I, J>(scalars: I, points: J) -> EdwardsPoint`
- `pub fn straus_optional_multiscalar_mul<I, J>(scalars: I, points: J) -> Option<EdwardsPoint>`
- `pub fn variable_base_mul(point: &EdwardsPoint, scalar: &Scalar) -> EdwardsPoint`
- `pub fn vartime_double_base_mul(a: &Scalar, A: &EdwardsPoint, b: &Scalar) -> EdwardsPoint`

### Type: `VartimePrecomputedMultiscalarMul`
- `pub fn new<I>(static_points: I) -> Self`
- `pub fn len(&self) -> usize`
- `pub fn is_empty(&self) -> bool`
- `pub fn optional_mixed_multiscalar_mul<I, J, K>(&self, static_scalars: I, dynamic_scalars: J, dynamic_points: K) -> Option<EdwardsPoint>`

## Module: `constants`

### Public Constants
- `pub const ED25519_BASEPOINT_COMPRESSED: CompressedEdwardsY`
- `pub const X25519_BASEPOINT: MontgomeryPoint`
- `pub const RISTRETTO_BASEPOINT_COMPRESSED: CompressedRistretto`
- `pub const RISTRETTO_BASEPOINT_POINT: RistrettoPoint`
- `pub static RISTRETTO_BASEPOINT_TABLE: &RistrettoBasepointTable` (when `precomputed-tables` feature is enabled)

## Module: `backend/serial/u64/field`

### Type: `FieldElement51`
- `pub const fn from_bytes(bytes: &[u8; 32]) -> FieldElement51`
- `pub fn to_bytes(self) -> [u8; 32]`
- `pub fn pow2k(&self, mut k: u32) -> FieldElement51`
- `pub fn square(&self) -> FieldElement51`
- `pub fn square2(&self) -> FieldElement51`
- `pub fn negate(&mut self)`

## Module: `backend/serial/u32/field`

### Type: `FieldElement2625`
- `pub const fn from_bytes(data: &[u8; 32]) -> FieldElement2625`
- `pub fn to_bytes(self) -> [u8; 32]`
- `pub fn pow2k(&self, k: u32) -> FieldElement2625`
- `pub fn square(&self) -> FieldElement2625`
- `pub fn square2(&self) -> FieldElement2625`
- `pub fn negate(&mut self)`

## Module: `backend/serial/u64/scalar`

### Type: `Scalar52`
- `pub fn from_bytes(bytes: &[u8; 32]) -> Scalar52`
- `pub fn from_bytes_wide(bytes: &[u8; 64]) -> Scalar52`
- `pub fn to_bytes(self) -> [u8; 32]`
- `pub fn add(a: &Scalar52, b: &Scalar52) -> Scalar52`
- `pub fn sub(a: &Scalar52, b: &Scalar52) -> Scalar52`
- `pub fn mul(a: &Scalar52, b: &Scalar52) -> Scalar52`
- `pub fn square(&self) -> Scalar52`
- `pub fn montgomery_mul(a: &Scalar52, b: &Scalar52) -> Scalar52`
- `pub fn montgomery_square(&self) -> Scalar52`
- `pub fn as_montgomery(&self) -> Scalar52`
- `pub fn from_montgomery(&self) -> Scalar52`

## Module: `backend/serial/u32/scalar`

### Type: `Scalar29`
- `pub fn from_bytes(bytes: &[u8; 32]) -> Scalar29`
- `pub fn from_bytes_wide(bytes: &[u8; 64]) -> Scalar29`
- `pub fn to_bytes(self) -> [u8; 32]`
- `pub fn add(a: &Scalar29, b: &Scalar29) -> Scalar29`
- `pub fn sub(a: &Scalar29, b: &Scalar29) -> Scalar29`
- `pub fn mul(a: &Scalar29, b: &Scalar29) -> Scalar29`
- `pub fn square(&self) -> Scalar29`
- `pub fn montgomery_mul(a: &Scalar29, b: &Scalar29) -> Scalar29`
- `pub fn montgomery_square(&self) -> Scalar29`
- `pub fn as_montgomery(&self) -> Scalar29`
- `pub fn from_montgomery(&self) -> Scalar29`