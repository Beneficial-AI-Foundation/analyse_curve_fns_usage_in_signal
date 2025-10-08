# curve25519-dalek Public API Functions with libsignal Call Graphs

This file lists only the curve25519-dalek public functions that have non-empty call graphs 
showing relationships with libsignal code.


Total functions with graphs: 528


## Module: ``


### Type: `DalekBits[Display]`
- `fmt()`

## Module: `backend`

### Functions
- `get_selected_backend()`
- `pippenger_optional_multiscalar_mul()`
- `straus_multiscalar_mul()`
- `straus_optional_multiscalar_mul()`
- `variable_base_mul()`
- `vartime_double_base_mul()`

### Type: `VartimePrecomputedStraus`
- `new()`
- `optional_mixed_multiscalar_mul()`

## Module: `backend/cpuid_avx2`

### Functions
- `init()`

### Type: `InitToken`
- `get()`

## Module: `backend/serial/curve_models`


### Type: `AffineNielsPoint[ConditionallySelectable]`
- `conditional_assign()`
- `conditional_select()`

### Type: `AffineNielsPoint[Debug]`
- `fmt()`

### Type: `AffineNielsPoint[Default]`
- `default()`

### Type: `AffineNielsPoint[Identity]`
- `identity()`

### Type: `AffineNielsPoint[Zeroize]`
- `zeroize()`

### Type: `CompletedPoint`
- `as_extended()`
- `as_projective()`

### Type: `CompletedPoint[Debug]`
- `fmt()`

### Type: `ProjectiveNielsPoint[ConditionallySelectable]`
- `conditional_assign()`
- `conditional_select()`

### Type: `ProjectiveNielsPoint[Debug]`
- `fmt()`

### Type: `ProjectiveNielsPoint[Default]`
- `default()`

### Type: `ProjectiveNielsPoint[Identity]`
- `identity()`

### Type: `ProjectiveNielsPoint[Zeroize]`
- `zeroize()`

### Type: `ProjectivePoint`
- `as_extended()`
- `double()`

### Type: `ProjectivePoint[Debug]`
- `fmt()`

### Type: `ProjectivePoint[Identity]`
- `identity()`

### Type: `ProjectivePoint[ValidityCheck]`
- `is_valid()`

### Type: ``&AffineNielsPoint`[Neg]`
- `neg()`

### Type: ``&EdwardsPoint`[`Add<&AffineNielsPoint>`]`
- `add()`

### Type: ``&EdwardsPoint`[`Add<&ProjectiveNielsPoint>`]`
- `add()`

### Type: ``&EdwardsPoint`[`Sub<&AffineNielsPoint>`]`
- `sub()`

### Type: ``&EdwardsPoint`[`Sub<&ProjectiveNielsPoint>`]`
- `sub()`

### Type: ``&ProjectiveNielsPoint`[Neg]`
- `neg()`

## Module: `backend/serial/scalar_mul/pippenger`


### Type: `Pippenger[VartimeMultiscalarMul]`
- `optional_multiscalar_mul()`

## Module: `backend/serial/scalar_mul/pippenger/test`

### Functions
- `test_vartime_pippenger()`

## Module: `backend/serial/scalar_mul/precomputed_straus`


### Type: `VartimePrecomputedStraus[VartimePrecomputedMultiscalarMul]`
- `new()`
- `optional_mixed_multiscalar_mul()`

## Module: `backend/serial/scalar_mul/straus`


### Type: `Straus[MultiscalarMul]`
- `multiscalar_mul()`

### Type: `Straus[VartimeMultiscalarMul]`
- `optional_multiscalar_mul()`

## Module: `backend/serial/scalar_mul/variable_base`

### Functions
- `mul()`

## Module: `backend/serial/scalar_mul/vartime_double_base`

### Functions
- `mul()`

## Module: `backend/serial/u64/field`

### Functions
- `m()`

### Type: `FieldElement51`
- `as_bytes()`
- `from_bytes()`
- `from_limbs()`
- `negate()`
- `pow2k()`
- `reduce()`
- `square()`
- `square2()`

### Type: `FieldElement51[ConditionallySelectable]`
- `conditional_assign()`
- `conditional_select()`
- `conditional_swap()`

### Type: `FieldElement51[Debug]`
- `fmt()`

### Type: `FieldElement51[Zeroize]`
- `zeroize()`

### Type: `FieldElement51[`AddAssign<&FieldElement51>`]`
- `add_assign()`

### Type: `FieldElement51[`MulAssign<&FieldElement51>`]`
- `mul_assign()`

### Type: `FieldElement51[`SubAssign<&FieldElement51>`]`
- `sub_assign()`

### Type: ``&FieldElement51`[Neg]`
- `neg()`

### Type: ``&FieldElement51`[`Add<&FieldElement51>`]`
- `add()`

### Type: ``&FieldElement51`[`Mul<&FieldElement51>`]`
- `mul()`

### Type: ``&FieldElement51`[`Sub<&FieldElement51>`]`
- `sub()`

## Module: `backend/serial/u64/scalar`

### Functions
- `black_box()`
- `m()`
- `part1()`
- `part2()`

### Type: `Scalar52`
- `add()`
- `as_bytes()`
- `as_montgomery()`
- `from_bytes()`
- `from_bytes_wide()`
- `from_montgomery()`
- `montgomery_mul()`
- `montgomery_reduce()`
- `montgomery_square()`
- `mul()`
- `mul_internal()`
- `square()`
- `square_internal()`
- `sub()`

### Type: `Scalar52[Debug]`
- `fmt()`

### Type: `Scalar52[Zeroize]`
- `zeroize()`

### Type: `Scalar52[`Index<usize>`]`
- `index()`

### Type: `Scalar52[`IndexMut<usize>`]`
- `index_mut()`

## Module: `backend/serial/u64/scalar/test`

### Functions
- `add()`
- `from_bytes_wide()`
- `montgomery_mul()`
- `montgomery_mul_max()`
- `montgomery_square_max()`
- `mul()`
- `mul_max()`
- `square_max()`
- `sub()`

## Module: `backend/vector/avx2/edwards`


### Type: `CachedPoint[ConditionallySelectable]`
- `conditional_assign()`
- `conditional_select()`

### Type: `CachedPoint[Default]`
- `default()`

### Type: `CachedPoint[Identity]`
- `identity()`

### Type: `CachedPoint[`From<ExtendedPoint>`]`
- `from()`

### Type: `ExtendedPoint`
- `double()`
- `mul_by_pow_2()`

### Type: `ExtendedPoint[ConditionallySelectable]`
- `conditional_assign()`
- `conditional_select()`

### Type: `ExtendedPoint[Default]`
- `default()`

### Type: `ExtendedPoint[Identity]`
- `identity()`

### Type: `ExtendedPoint[`From<crate::EdwardsPoint>`]`
- `from()`

### Type: ``&CachedPoint`[Neg]`
- `neg()`

### Type: ``&ExtendedPoint`[`Add<&CachedPoint>`]`
- `add()`

### Type: ``&ExtendedPoint`[`Sub<&CachedPoint>`]`
- `sub()`

### Type: ``LookupTable<CachedPoint>`[`From<&crate::EdwardsPoint>`]`
- `from()`

### Type: ``NafLookupTable5<CachedPoint>`[`From<&crate::EdwardsPoint>`]`
- `from()`

### Type: ``NafLookupTable8<CachedPoint>`[`From<&crate::EdwardsPoint>`]`
- `from()`

### Type: ``crate::EdwardsPoint`[`From<ExtendedPoint>`]`
- `from()`

## Module: `backend/vector/avx2/field`

### Functions
- `blend_lanes()`
- `m()`
- `m_lo()`
- `repack_pair()`
- `shuffle_lanes()`
- `unpack_pair()`

### Type: `FieldElement2625x4`
- `blend()`
- `diff_sum()`
- `negate_lazy()`
- `new()`
- `reduce()`
- `reduce64()`
- `shuffle()`
- `splat()`
- `split()`
- `square_and_negate_D()`

### Type: `FieldElement2625x4[ConditionallySelectable]`
- `conditional_assign()`
- `conditional_select()`

### Type: `FieldElement2625x4[Neg]`
- `neg()`

### Type: `FieldElement2625x4[`Add<Self>`]`
- `add()`

### Type: `FieldElement2625x4[`Mul<(u32, u32, u32, u32)>`]`
- `mul()`

### Type: ``&FieldElement2625x4`[`Mul<Self>`]`
- `mul()`

## Module: `backend/vector/packed_simd`


### Type: `u32x8`
- `extract()`
- `mul32()`
- `new()`
- `new_const()`
- `shl()`
- `splat()`
- `splat_const()`

### Type: `u32x8[`From<u64x4>`]`
- `from()`

### Type: `u64x4`
- `new()`
- `new_const()`
- `shl()`
- `shr()`
- `splat()`
- `splat_const()`

## Module: `backend/vector/scalar_mul/pippenger/spec_avx2`


### Type: `Pippenger[VartimeMultiscalarMul]`
- `optional_multiscalar_mul()`

## Module: `backend/vector/scalar_mul/precomputed_straus/spec_avx2`


### Type: `VartimePrecomputedStraus[VartimePrecomputedMultiscalarMul]`
- `new()`
- `optional_mixed_multiscalar_mul()`

## Module: `backend/vector/scalar_mul/straus/spec_avx2`


### Type: `Straus[MultiscalarMul]`
- `multiscalar_mul()`

### Type: `Straus[VartimeMultiscalarMul]`
- `optional_multiscalar_mul()`

## Module: `backend/vector/scalar_mul/variable_base/spec_avx2`

### Functions
- `mul()`

## Module: `backend/vector/scalar_mul/vartime_double_base/spec_avx2`

### Functions
- `mul()`

## Module: `constants/test`

### Functions
- `test_d_vs_ratio()`
- `test_eight_torsion()`
- `test_four_torsion()`
- `test_sqrt_ad_minus_one()`
- `test_sqrt_constants_sign()`
- `test_sqrt_minus_one()`
- `test_two_torsion()`

## Module: `deterministic`

### Functions
- `determine_curve25519_dalek_bits()`
- `determine_curve25519_dalek_bits_warning()`

## Module: `edwards`


### Type: `CompressedEdwardsY`
- `as_bytes()`
- `decompress()`
- `from_slice()`
- `to_bytes()`

### Type: `CompressedEdwardsY[ConstantTimeEq]`
- `ct_eq()`

### Type: `CompressedEdwardsY[Debug]`
- `fmt()`

### Type: `CompressedEdwardsY[Default]`
- `default()`

### Type: `CompressedEdwardsY[Identity]`
- `identity()`

### Type: `CompressedEdwardsY[Zeroize]`
- `zeroize()`

### Type: `CompressedEdwardsY[`TryFrom<&[u8]`
- `>`]try_from()`

### Type: `EdwardsBasepointTableRadix128[BasepointTable]`
- `create()`

### Type: `EdwardsBasepointTableRadix256[BasepointTable]`
- `create()`

### Type: `EdwardsBasepointTableRadix32[BasepointTable]`
- `create()`

### Type: `EdwardsBasepointTableRadix64[BasepointTable]`
- `create()`

### Type: `EdwardsBasepointTable[BasepointTable]`
- `basepoint()`
- `create()`

### Type: `EdwardsPoint`
- `as_affine_niels()`
- `as_projective()`
- `as_projective_niels()`
- `compress()`
- `double()`
- `is_small_order()`
- `is_torsion_free()`
- `mul_base()`
- `mul_base_clamped()`
- `mul_by_cofactor()`
- `mul_by_pow_2()`
- `mul_clamped()`
- `nonspec_map_to_curve()`
- `to_montgomery()`
- `vartime_double_scalar_mul_basepoint()`

### Type: `EdwardsPoint[ConditionallySelectable]`
- `conditional_select()`

### Type: `EdwardsPoint[ConstantTimeEq]`
- `ct_eq()`

### Type: `EdwardsPoint[Debug]`
- `fmt()`

### Type: `EdwardsPoint[Default]`
- `default()`

### Type: `EdwardsPoint[Identity]`
- `identity()`

### Type: `EdwardsPoint[MultiscalarMul]`
- `multiscalar_mul()`

### Type: `EdwardsPoint[Neg]`
- `neg()`

### Type: `EdwardsPoint[ValidityCheck]`
- `is_valid()`

### Type: `EdwardsPoint[VartimeMultiscalarMul]`
- `optional_multiscalar_mul()`

### Type: `EdwardsPoint[Zeroize]`
- `zeroize()`

### Type: `EdwardsPoint[`AddAssign<&EdwardsPoint>`]`
- `add_assign()`

### Type: `EdwardsPoint[`MulAssign<&Scalar>`]`
- `mul_assign()`

### Type: `EdwardsPoint[`PartialEq<Self>`]`
- `eq()`

### Type: `EdwardsPoint[`SubAssign<&EdwardsPoint>`]`
- `sub_assign()`

### Type: `EdwardsPoint[`Sum<T>`]`
- `sum()`

### Type: `VartimeEdwardsPrecomputation[VartimePrecomputedMultiscalarMul]`
- `new()`
- `optional_mixed_multiscalar_mul()`

### Type: ``&EdwardsPoint`[Neg]`
- `neg()`

### Type: ``&EdwardsPoint`[`Add<&EdwardsPoint>`]`
- `add()`

### Type: ``&EdwardsPoint`[`Mul<&Scalar>`]`
- `mul()`

### Type: ``&EdwardsPoint`[`Sub<&EdwardsPoint>`]`
- `sub()`

### Type: ``&Scalar`[`Mul<&EdwardsPoint>`]`
- `mul()`

## Module: `edwards/decompress`

### Functions
- `step_1()`
- `step_2()`

## Module: `edwards/test`

### Functions
- `basepoint16_vs_mul_by_pow_2_4()`
- `basepoint_decompression_compression()`
- `basepoint_double_vs_basepoint2()`
- `basepoint_mult_by_basepoint_order()`
- `basepoint_mult_one_vs_basepoint()`
- `basepoint_mult_two_vs_basepoint2()`
- `basepoint_mult_vs_ed25519py()`
- `basepoint_plus_basepoint_affine_niels_vs_basepoint2()`
- `basepoint_plus_basepoint_projective_niels_vs_basepoint2()`
- `basepoint_plus_basepoint_vs_basepoint2()`
- `basepoint_projective_extended_round_trip()`
- `basepoint_table_basepoint_function_correct()`
- `basepoint_tables()`
- `basepoint_tables_unreduced_scalar()`
- `compressed_identity()`
- `conditional_assign_for_affine_niels_point()`
- `decompression_sign_handling()`
- `elligator_signal_test_vectors()`
- `extended_point_equality_handles_scaling()`
- `impl_sum()`
- `is_identity()`
- `is_small_order()`
- `monte_carlo_overflow_underflow_debug_assert_test()`
- `mul_base_clamped()`
- `multiscalar_consistency_iter()`
- `multiscalar_consistency_n_100()`
- `multiscalar_consistency_n_1000()`
- `multiscalar_consistency_n_250()`
- `multiscalar_consistency_n_500()`
- `scalar_mul_vs_ed25519py()`
- `scalarmult_extended_point_works_both_ways()`
- `test_precomputed_basepoint_mult()`
- `test_vectors()`
- `to_affine_niels_clears_denominators()`
- `vartime_precomputed_vs_nonprecomputed_multiscalar()`

## Module: `edwards/test/vartime`

### Functions
- `double_scalar_mul_basepoint_vs_ed25519py()`
- `multiscalar_mul_vartime_vs_consttime()`
- `multiscalar_mul_vs_ed25519py()`

## Module: `edwards_benches`

### Functions
- `compress()`
- `consttime_fixed_base_scalar_mul()`
- `consttime_variable_base_scalar_mul()`
- `decompress()`
- `edwards_benches()`
- `vartime_double_base_scalar_mul()`

## Module: `field`


### Type: ``crate::lizard::lizard_constants::FieldElement51``
- `batch_invert()`
- `invert()`
- `invsqrt()`
- `is_negative()`
- `is_zero()`
- `pow22501()`
- `pow_p58()`
- `sqrt_ratio_i()`

### Type: ``crate::lizard::lizard_constants::FieldElement51`[ConstantTimeEq]`
- `ct_eq()`

### Type: ``crate::lizard::lizard_constants::FieldElement51`[`PartialEq<Self>`]`
- `eq()`

## Module: `field/test`

### Functions
- `a_invert_vs_inverse_of_a_constant()`
- `a_mul_a_vs_a_squared_constant()`
- `a_p58_vs_ap58_constant()`
- `a_square2_vs_a_squared_constant()`
- `a_square_vs_a_squared_constant()`
- `batch_invert_a_matches_nonbatched()`
- `batch_invert_empty()`
- `conditional_negate()`
- `encoding_is_canonical()`
- `equality()`
- `from_bytes_highbit_is_ignored()`
- `sqrt_ratio_behavior()`

## Module: `lizard/jacobi_quartic`


### Type: `JacobiPoint`
- `dual()`
- `elligator_inv()`

## Module: `lizard/lizard_constants/test`

### Functions
- `test_lizard_constants()`

## Module: `lizard/lizard_ristretto`


### Type: `RistrettoPoint`
- `decode_253_bits()`
- `elligator_ristretto_flavor_inverse()`
- `encode_253_bits()`
- `from_uniform_bytes_single_elligator()`
- `lizard_decode()`
- `lizard_encode()`
- `to_jacobi_quartic_ristretto()`
- `xcoset4()`

## Module: `lizard/lizard_ristretto/test`

### Functions
- `test_elligator_inv()`
- `test_lizard_encode()`
- `test_lizard_encode_helper()`

## Module: `lizard/u64_constants`

### Functions
- `field_element()`

## Module: `montgomery`

### Functions
- `differential_add_and_double()`
- `elligator_encode()`

### Type: `MontgomeryPoint`
- `as_bytes()`
- `mul_base()`
- `mul_base_clamped()`
- `mul_bits_be()`
- `mul_clamped()`
- `to_bytes()`
- `to_edwards()`

### Type: `MontgomeryPoint[ConstantTimeEq]`
- `ct_eq()`

### Type: `MontgomeryPoint[Hash]`
- `hash()`

### Type: `MontgomeryPoint[Identity]`
- `identity()`

### Type: `MontgomeryPoint[Zeroize]`
- `zeroize()`

### Type: `MontgomeryPoint[`MulAssign<&Scalar>`]`
- `mul_assign()`

### Type: `MontgomeryPoint[`PartialEq<Self>`]`
- `eq()`

### Type: `ProjectivePoint`
- `as_affine()`

### Type: `ProjectivePoint[ConditionallySelectable]`
- `conditional_select()`

### Type: `ProjectivePoint[Default]`
- `default()`

### Type: `ProjectivePoint[Identity]`
- `identity()`

### Type: ``&MontgomeryPoint`[`Mul<&Scalar>`]`
- `mul()`

### Type: ``&Scalar`[`Mul<&MontgomeryPoint>`]`
- `mul()`

## Module: `montgomery/test`

### Functions
- `basepoint_edwards_to_montgomery()`
- `basepoint_montgomery_to_edwards()`
- `bytestring_bits_le()`
- `eq_defined_mod_p()`
- `identity_in_different_coordinates()`
- `identity_in_different_models()`
- `montgomery_elligator_correct()`
- `montgomery_elligator_zero_zero()`
- `montgomery_ladder_matches_edwards_scalarmult()`
- `montgomery_mul_bits_be()`
- `montgomery_mul_bits_be_twist()`
- `montgomery_to_edwards_rejects_twist()`
- `mul_base_clamped()`
- `rand_prime_order_point()`

## Module: `montgomery_benches`

### Functions
- `consttime_fixed_base_scalar_mul()`
- `montgomery_benches()`
- `montgomery_ladder()`

## Module: `multiscalar_benches`

### Functions
- `construct_points()`
- `construct_scalars()`
- `consttime_multiscalar_mul()`
- `multiscalar_benches()`
- `vartime_multiscalar_mul()`
- `vartime_precomputed_helper()`
- `vartime_precomputed_pure_static()`

## Module: `ristretto`


### Type: `BatchCompressState`
- `efgh()`

### Type: `BatchCompressState[`From<&RistrettoPoint>`]`
- `from()`

### Type: `CompressedRistretto`
- `as_bytes()`
- `decompress()`
- `from_slice()`
- `to_bytes()`

### Type: `CompressedRistretto[ConstantTimeEq]`
- `ct_eq()`

### Type: `CompressedRistretto[Debug]`
- `fmt()`

### Type: `CompressedRistretto[Default]`
- `default()`

### Type: `CompressedRistretto[Identity]`
- `identity()`

### Type: `CompressedRistretto[Zeroize]`
- `zeroize()`

### Type: `CompressedRistretto[`TryFrom<&[u8]`
- `>`]try_from()`

### Type: `RistrettoBasepointTable`
- `basepoint()`
- `create()`

### Type: `RistrettoPoint`
- `compress()`
- `coset4()`
- `double_and_compress_batch()`
- `elligator_ristretto_flavor()`
- `from_hash()`
- `from_uniform_bytes()`
- `hash_from_bytes()`
- `mul_base()`
- `random()`
- `vartime_double_scalar_mul_basepoint()`

### Type: `RistrettoPoint[ConditionallySelectable]`
- `conditional_select()`

### Type: `RistrettoPoint[ConstantTimeEq]`
- `ct_eq()`

### Type: `RistrettoPoint[Debug]`
- `fmt()`

### Type: `RistrettoPoint[Default]`
- `default()`

### Type: `RistrettoPoint[Identity]`
- `identity()`

### Type: `RistrettoPoint[MultiscalarMul]`
- `multiscalar_mul()`

### Type: `RistrettoPoint[Neg]`
- `neg()`

### Type: `RistrettoPoint[VartimeMultiscalarMul]`
- `optional_multiscalar_mul()`

### Type: `RistrettoPoint[Zeroize]`
- `zeroize()`

### Type: `RistrettoPoint[`Add<Self>`]`
- `add()`

### Type: `RistrettoPoint[`AddAssign<&RistrettoPoint>`]`
- `add_assign()`

### Type: `RistrettoPoint[`MulAssign<&Scalar>`]`
- `mul_assign()`

### Type: `RistrettoPoint[`PartialEq<Self>`]`
- `eq()`

### Type: `RistrettoPoint[`SubAssign<&RistrettoPoint>`]`
- `sub_assign()`

### Type: `RistrettoPoint[`Sum<T>`]`
- `sum()`

### Type: `VartimeRistrettoPrecomputation[VartimePrecomputedMultiscalarMul]`
- `new()`
- `optional_mixed_multiscalar_mul()`

### Type: ``&RistrettoBasepointTable`[`Mul<&Scalar>`]`
- `mul()`

### Type: ``&RistrettoPoint`[Neg]`
- `neg()`

### Type: ``&RistrettoPoint`[`Add<&RistrettoPoint>`]`
- `add()`

### Type: ``&RistrettoPoint`[`Mul<&Scalar>`]`
- `mul()`

### Type: ``&RistrettoPoint`[`Sub<&RistrettoPoint>`]`
- `sub()`

### Type: ``&Scalar`[`Mul<&RistrettoBasepointTable>`]`
- `mul()`

### Type: ``&Scalar`[`Mul<&RistrettoPoint>`]`
- `mul()`

## Module: `ristretto/decompress`

### Functions
- `step_1()`
- `step_2()`

## Module: `ristretto/test`

### Functions
- `basepoint_roundtrip()`
- `compress_id()`
- `decompress_id()`
- `decompress_negative_s_fails()`
- `double_and_compress_1024_random_points()`
- `elligator_vs_ristretto_sage()`
- `encodings_of_small_multiples_of_basepoint()`
- `four_torsion_basepoint()`
- `four_torsion_random()`
- `impl_sum()`
- `one_way_map()`
- `random_roundtrip()`
- `scalarmult_ristrettopoint_works_both_ways()`
- `vartime_precomputed_vs_nonprecomputed_multiscalar()`

## Module: `ristretto_benches`

### Functions
- `compress()`
- `decompress()`
- `double_and_compress_batch()`
- `elligator()`
- `ristretto_benches()`

## Module: `root`

### Functions
- `is_capable_simd()`
- `main()`

## Module: `scalar`

### Functions
- `bot_half()`
- `clamp_integer()`
- `read_le_u64_into()`
- `square_multiply()`
- `top_half()`

### Type: `Scalar`
- `as_bytes()`
- `as_radix_16()`
- `as_radix_2w()`
- `batch_invert()`
- `bits_le()`
- `from_bytes_mod_order()`
- `from_bytes_mod_order_wide()`
- `from_canonical_bytes()`
- `from_hash()`
- `hash_from_bytes()`
- `invert()`
- `is_canonical()`
- `non_adjacent_form()`
- `random()`
- `reduce()`
- `to_bytes()`
- `to_radix_2w_size_hint()`
- `unpack()`

### Type: `Scalar[ConditionallySelectable]`
- `conditional_select()`

### Type: `Scalar[ConstantTimeEq]`
- `ct_eq()`

### Type: `Scalar[Debug]`
- `fmt()`

### Type: `Scalar[Default]`
- `default()`

### Type: `Scalar[Neg]`
- `neg()`

### Type: `Scalar[Serialize]`
- `serialize()`

### Type: `Scalar[Zeroize]`
- `zeroize()`

### Type: `Scalar[`AddAssign<&Scalar>`]`
- `add_assign()`

### Type: `Scalar[`Deserialize<'de>`]`
- `deserialize()`

### Type: `Scalar[`From<u128>`]`
- `from()`

### Type: `Scalar[`From<u16>`]`
- `from()`

### Type: `Scalar[`From<u32>`]`
- `from()`

### Type: `Scalar[`From<u64>`]`
- `from()`

### Type: `Scalar[`From<u8>`]`
- `from()`

### Type: `Scalar[`Index<usize>`]`
- `index()`

### Type: `Scalar[`MulAssign<&Scalar>`]`
- `mul_assign()`

### Type: `Scalar[`PartialEq<Self>`]`
- `eq()`

### Type: `Scalar[`Product<T>`]`
- `product()`

### Type: `Scalar[`SubAssign<&Scalar>`]`
- `sub_assign()`

### Type: `Scalar[`Sum<T>`]`
- `sum()`

### Type: ``&Scalar`[Neg]`
- `neg()`

### Type: ``&Scalar`[`Add<&Scalar>`]`
- `add()`

### Type: ``&Scalar`[`Mul<&Scalar>`]`
- `mul()`

### Type: ``&Scalar`[`Sub<&Scalar>`]`
- `sub()`

### Type: ``backend::serial::u64::scalar::Scalar52``
- `invert()`
- `montgomery_invert()`
- `pack()`

## Module: `scalar/test`

### Functions
- `add_reduces()`
- `batch_invert_consistency()`
- `batch_invert_empty()`
- `batch_invert_with_a_zero_input_panics()`
- `canonical_decoding()`
- `from_bytes_mod_order_wide()`
- `from_u64()`
- `fuzzer_testcase_reduction()`
- `impl_add()`
- `impl_mul()`
- `impl_product()`
- `impl_sum()`
- `invert()`
- `montgomery_reduce_matches_from_bytes_mod_order_wide()`
- `neg_twice_is_identity()`
- `non_adjacent_form_iter()`
- `non_adjacent_form_random()`
- `non_adjacent_form_test_vector()`
- `reduce()`
- `scalar_mul_by_one()`
- `square()`
- `sub_reduces()`
- `test_mul_reduction_invariance()`
- `test_pippenger_radix()`
- `test_pippenger_radix_iter()`
- `test_read_le_u64_into()`
- `test_read_le_u64_into_should_panic_on_bad_input()`
- `test_scalar_clamp()`
- `test_scalar_from_int()`
- `to_bytes_from_bytes_roundtrips()`

## Module: `scalar_benches`

### Functions
- `batch_scalar_inversion()`
- `scalar_arith()`
- `scalar_benches()`

## Module: `traits`

### Functions
- `BasepointTable#basepoint()`
- `BasepointTable#create()`
- `BasepointTable#mul_base()`
- `BasepointTable#mul_base_clamped()`
- `Identity#identity()`
- `IsIdentity#is_identity()`
- `MultiscalarMul#multiscalar_mul()`
- `ValidityCheck#is_valid()`
- `VartimeMultiscalarMul#optional_multiscalar_mul()`
- `VartimeMultiscalarMul#vartime_multiscalar_mul()`
- `VartimePrecomputedMultiscalarMul#new()`
- `VartimePrecomputedMultiscalarMul#optional_mixed_multiscalar_mul()`
- `VartimePrecomputedMultiscalarMul#vartime_mixed_multiscalar_mul()`
- `VartimePrecomputedMultiscalarMul#vartime_multiscalar_mul()`

### Type: `T[IsIdentity]`
- `is_identity()`

## Module: `window`


### Type: ``LookupTable<ProjectiveNielsPoint>`[`From<&EdwardsPoint>`]`
- `from()`

### Type: ``LookupTable<T>``
- `select()`

### Type: ``NafLookupTable5<AffineNielsPoint>`[`From<&EdwardsPoint>`]`
- `from()`

### Type: ``NafLookupTable5<ProjectiveNielsPoint>`[`From<&EdwardsPoint>`]`
- `from()`

### Type: ``NafLookupTable5<T>``
- `select()`

### Type: ``NafLookupTable5<T>`[Debug]`
- `fmt()`

### Type: ``NafLookupTable8<AffineNielsPoint>`[`From<&EdwardsPoint>`]`
- `from()`

### Type: ``NafLookupTable8<ProjectiveNielsPoint>`[`From<&EdwardsPoint>`]`
- `from()`

### Type: ``NafLookupTable8<T>``
- `select()`

### Type: ``NafLookupTable8<T>`[Debug]`
- `fmt()`