# zig-stdlib-writer-interface-lab — RESULTS

## Compiler

| Field | Value |
|---|---|
| Zig path | `zig` |
| Zig version | 0.14.1 |
| Compile command | `zig build-exe writer_interface_lab.zig -O ReleaseSafe -femit-bin=./writer_interface_lab` |
| Compile ok | ✅ true |
| Compile time | 19.745s |
| Binary size | 2,734,512 bytes |

## Run summary

| Metric | Value |
|---|---|
| Cases | 51 |
| Methods | 18 |
| Result rows | 348 |
| Python | 3.12.3 |
| Platform | Linux-6.17.0-1009-aws-x86_64-with-glibc2.39 |

## Artifact sizes

| File | Size |
|---|---|
| `cases.json` | 68,041 bytes |
| `writer_interface_lab.zig` | 5,104 bytes |
| `writer_interface_lab` (binary) | 2,734,512 bytes |
| `results_rows.csv` | – |
| `results_rows.json` | – |

## Per-method breakdown

| Method | success | fail | skip | not_tested |
|---|---|---|---|---|
| preserve_original_case_baseline | 30 | 0 | 3 | 13 |
| zig_compiler_discovery_checker | 30 | 0 | 3 | 13 |
| zig_harness_compile_checker | 30 | 0 | 3 | 13 |
| anytype_writer_observer | 9 | 0 | 0 | 0 |
| anywriter_storage_observer | 2 | 0 | 0 | 0 |
| generic_writer_context_marker | 1 | 0 | 0 | 0 |
| write_vs_writeAll_observer | 3 | 0 | 0 | 0 |
| fixed_buffer_writer_observer | 1 | 0 | 0 | 0 |
| arraylist_writer_observer | 1 | 0 | 0 | 0 |
| fmt_writer_observer | 1 | 0 | 1 | 0 |
| json_writer_context_marker | 0 | 0 | 0 | 2 |
| interface_documentation_marker | 2 | 0 | 2 | 2 |
| performance_scope_marker | 0 | 0 | 0 | 6 |
| version_churn_marker | 2 | 0 | 0 | 0 |
| wrapper_policy_marker | 30 | 0 | 3 | 13 |
| copy_size_timing_marker | 30 | 0 | 3 | 13 |
| naive_writer_policy_marker | 30 | 1 | 3 | 13 |
| external_interface_truth_not_tested_marker | 0 | 0 | 0 | 3 |

## Naive failures

Naive writer failed **1 case** (expected).

| Case ID | Fail Reason |
|---|---|
| `naive_writer_policy_expected_fail_01` | naive_writer_policy_expected_fail |

The naive writer policy assumes every writer has every helper method, ignores partial writes, treats `write` like `writeAll`, assumes `anytype` can be stored in a struct field, assumes AnyWriter preserves narrow error sets, assumes helper methods are always optimized, and assumes stdlib writer APIs are stable across versions.

## Skip / not-run matrix

Invalid operations and out-of-scope contexts are intentionally marked `skip` or `not_tested` – never executed.

### Interface / documentation – not run / not tested

| Category | Reason | Count |
|---|---|---|
| `interface_documentation_context` | anytype_missing_method_compile_context_not_run | 7 |
| `interface_documentation_context` | struct_field_anytype_not_allowed | 7 |
| `interface_documentation_context` | rust_trait_comparison_context_not_tested | 7 |
| `interface_documentation_context` | tagged_union_interface_context_not_required | 7 |

### JSON context – not tested

| Category | Reason | Count |
|---|---|---|
| `json_context` | json_stringify_writer_context_not_tested | 7 |
| `json_context` | custom_jsonStringify_context_not_tested | 7 |

### Performance – not measured / not proved

| Category | Reason | Count |
|---|---|---|
| `performance_context_not_tested` | dynamic_dispatch_context_not_tested | 7 |
| `performance_context_not_tested` | function_pointer_overhead_context_not_tested | 7 |
| `performance_context_not_tested` | monomorphization_context_not_tested | 7 |
| `performance_context_not_tested` | code_bloat_context_not_measured | 7 |
| `performance_context_not_tested` | optimized_helper_not_proved | 7 |
| `performance_context_not_tested` | performance_microbenchmark_not_proof | 7 |

### fmt / external – not run / not tested

| Category | Reason | Count |
|---|---|---|
| `fmt_policy` | fmt_print_context_not_run | 7 |
| `external_interface_truth_not_tested` | external_api_truth_not_tested | 7 |
| `production_logger_not_tested` | production_logger_not_tested | 7 |
| `production_logger_not_tested` | serialization_library_not_tested | 7 |

## Environment

| Field | Value |
|---|---|
| Zig path | `zig` |
| Zig version | 0.14.1 |
| Compile ok | ✅ true |
| Binary size | 2,734,512 bytes |
| Peak memory (tracemalloc) | 399,381 bytes |
| Python | 3.12.3 |
| Platform | Linux-6.17.0-1009-aws-x86_64-with-glibc2.39 |

## Scope / Honesty checklist

| Claim | Status |
|---|---|
| HN thread accessed via HN API CLI | ✅ Yes – thread 42849774, before README |
| Network / API / package manager during run | ❌ None (except HN pre-read) |
| Invalid memory executed | ❌ No – compile-error cases marked `not_run` |
| Writer interface scope tested | ✅ anytype, AnyWriter, GenericWriter, write/writeAll |
| Version compatibility tested | ⚠️ Zig 0.14.1 only – local_only |
| Performance proved | ❌ No – performance context markers, not benchmarks |
| Production logger tested | ❌ No – HN discussion context only |

## Conclusions

| Finding | Detail |
|---|---|
| `writer: anytype` | Zero-overhead but implicit; document required methods |
| AnyWriter | Allows storing implementation-independent writers in struct fields; error set erasure to `anyerror` |
| GenericWriter | Preserves typed error sets; different type per implementation |
| `write` vs `writeAll` | `write` may write fewer bytes; `writeAll` loops until complete or error |
| Version churn | Zig writer APIs vary across versions – record exact Zig version |

---

**Artifacts:** [`results_rows.csv`](results_rows.csv) · [`results_rows.json`](results_rows.json) · [`cases.json`](cases.json)
