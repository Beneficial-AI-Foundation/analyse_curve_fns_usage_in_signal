There are 5 sink nodes that appear in multiple DOT files:

1. backend/serial/curve_models.rs :: as_extended (appears in 2 files)

backend_serial_curve_models_impl__CompletedPoint_as_extended_5.dot
backend_serial_curve_models_impl__ProjectivePoint_as_extended_5.dot

2. backend/vector/avx2/edwards.rs :: from (appears in 4 files)

backend_vector_avx2_edwards_impl__CachedPoint__From<ExtendedPoint>_from_5.dot
backend_vector_avx2_edwards_impl__ExtendedPoint__From<crate_EdwardsPoint>_from_5.dot
backend_vector_avx2_edwards_impl__LookupTable<CachedPoint>__From<&crate_EdwardsPoint>_from_5.dot
backend_vector_avx2_edwards_impl__NafLookupTable5<CachedPoint>__From<&crate_EdwardsPoint>_from_5.dot

3. scalar.rs :: from (appears in 3 files)

scalar_impl__Scalar__From<u32>_from_5.dot
scalar_impl__Scalar__From<u64>_from_5.dot
scalar_impl__Scalar__From<u8>_from_5.dot

4. scalar.rs :: invert (appears in 2 files)

scalar_impl__Scalar_invert_5.dot
scalar_impl__backend_serial_u64_scalar_Scalar52_invert_5.dot

5. window.rs :: select (appears in 2 files)

window_impl__NafLookupTable5<T>_select_5.dot
window_impl__NafLookupTable8<T>_select_5.dot