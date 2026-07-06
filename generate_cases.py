#!/usr/bin/env python3
"""Generate deterministic Zig writer-interface test cases."""
import json

cases = []

def add(cid, category, **kw):
    c = {"case_id": cid, "category": category}
    c.update(kw)
    cases.append(c)

def base(**kw):
    d = dict(
        fake_record_name="toy_interface_case",
        synthetic_input_bytes="fake_message",
        synthetic_output_preview="toy_output",
        requested_write_length=16,
        writer_policy_label="anytype_policy",
        expected_writer_type_label="anytype",
        expected_stored_writer_policy="n/a",
        expected_error_set_label="typed_error",
        expected_partial_write_behavior="n/a",
        expected_output_bytes=16,
        operation_label="write",
        zig_feature_needed="std.io.Writer",
        context_label="anytype_policy",
        expected_status="success",
        expected_zig_harness_observation="write_ok",
        expected_anytype_observation="anytype_ok",
        expected_anywriter_observation="n/a",
        expected_generic_writer_observation="n/a",
        expected_write_writeall_observation="write_ok",
        expected_fixed_buffer_observation="n/a",
        expected_arraylist_observation="n/a",
        expected_fmt_observation="n/a",
        expected_wrapper_observation="n/a",
        expected_version_compatibility_truth="local_only",
        expected_production_logger_truth="not_tested",
        expected_fail_reason="",
        naive_expected_to_fail=False,
    )
    d.update(kw)
    return d

# anytype writer cases
add("writer_anytype_accepts_arraylist_writer_01", "anytype_policy", **base(
    fake_record_name="demo_writer",
    synthetic_input_bytes="example_log_line",
    synthetic_output_preview="example_log_line",
    requested_write_length=16,
    writer_policy_label="anytype_arraylist",
    expected_writer_type_label="anytype",
    expected_anytype_observation="anytype_ok",
    expected_arraylist_observation="arraylist_ok",
    context_label="anytype_policy"))

add("writer_anytype_accepts_fixed_buffer_writer_01", "anytype_policy", **base(
    fake_record_name="demo_writer",
    synthetic_input_bytes="sample_payload",
    synthetic_output_preview="sample_payload",
    requested_write_length=14,
    writer_policy_label="anytype_fixed_buffer",
    expected_writer_type_label="anytype",
    expected_fixed_buffer_observation="fixed_buffer_ok",
    context_label="anytype_policy"))

add("writer_anytype_missing_method_compile_context_not_run_01", "interface_documentation_context", **base(
    fake_record_name="toy_interface_case",
    synthetic_input_bytes="fake_message",
    writer_policy_label="anytype_missing_method",
    expected_status="skip",
    expected_zig_harness_observation="not_run_compile_error",
    expected_anytype_observation="not_run",
    expected_fail_reason="anytype_missing_method_compile_context_not_run",
    context_label="interface_documentation_context"))

# write vs writeAll
add("write_vs_writeAll_partial_write_marker_01", "partial_write_policy", **base(
    fake_record_name="toy_partial_write",
    synthetic_input_bytes="synthetic_chunk",
    requested_write_length=15,
    writer_policy_label="write_partial",
    expected_partial_write_behavior="may_write_less",
    expected_write_writeall_observation="partial_write_ok",
    context_label="partial_write_policy"))

add("writeAll_loops_until_complete_marker_01", "partial_write_policy", **base(
    fake_record_name="toy_partial_write",
    synthetic_input_bytes="synthetic_chunk",
    requested_write_length=15,
    writer_policy_label="writeAll_complete",
    expected_partial_write_behavior="loops_until_complete",
    expected_write_writeall_observation="writeAll_ok",
    context_label="partial_write_policy"))

add("writeAll_stops_on_error_marker_01", "partial_write_policy", **base(
    fake_record_name="synthetic_error_case",
    synthetic_input_bytes="fake_message",
    requested_write_length=12,
    writer_policy_label="writeAll_error",
    expected_error_set_label="WriteError",
    expected_partial_write_behavior="stops_on_error",
    expected_write_writeall_observation="error_handled",
    expected_status="error",
    expected_fail_reason="writeAll_stops_on_error",
    context_label="partial_write_policy"))

# custom writers
add("custom_counting_writer_records_bytes_marker_01", "anytype_policy", **base(
    fake_record_name="fake_counter_writer",
    synthetic_input_bytes="example_log_line",
    requested_write_length=16,
    writer_policy_label="counting_writer",
    expected_writer_type_label="counting_writer",
    expected_wrapper_observation="bytes_counted",
    context_label="anytype_policy"))

add("failing_writer_records_error_marker_01", "anytype_policy", **base(
    fake_record_name="synthetic_error_case",
    synthetic_input_bytes="fake_message",
    requested_write_length=12,
    writer_policy_label="failing_writer",
    expected_error_set_label="WriteError",
    expected_status="error",
    expected_zig_harness_observation="error_recorded",
    expected_fail_reason="failing_writer_records_error",
    context_label="anytype_policy"))

add("partial_writer_records_short_write_marker_01", "partial_write_policy", **base(
    fake_record_name="toy_partial_write",
    synthetic_input_bytes="synthetic_chunk",
    requested_write_length=20,
    writer_policy_label="partial_writer",
    expected_partial_write_behavior="short_write",
    expected_write_writeall_observation="short_write_ok",
    context_label="partial_write_policy"))

# fixed buffer writer
add("fixed_buffer_writer_exact_fit_marker_01", "fixed_buffer_policy", **base(
    fake_record_name="demo_buffer",
    synthetic_input_bytes="sample_payload",
    requested_write_length=14,
    writer_policy_label="fixed_buffer_exact_fit",
    expected_writer_type_label="fixed_buffer_writer",
    expected_fixed_buffer_observation="exact_fit_ok",
    context_label="fixed_buffer_policy"))

add("fixed_buffer_writer_out_of_space_marker_01", "fixed_buffer_policy", **base(
    fake_record_name="demo_buffer",
    synthetic_input_bytes="sample_payload_that_is_way_too_long",
    requested_write_length=64,
    writer_policy_label="fixed_buffer_oom",
    expected_error_set_label="NoSpaceLeft",
    expected_status="error",
    expected_fixed_buffer_observation="out_of_space_handled",
    expected_fail_reason="fixed_buffer_out_of_space",
    context_label="fixed_buffer_policy"))

# ArrayList writer
add("arraylist_writer_grows_with_allocator_marker_01", "arraylist_policy", **base(
    fake_record_name="demo_writer",
    synthetic_input_bytes="example_log_line",
    requested_write_length=16,
    writer_policy_label="arraylist_writer",
    expected_writer_type_label="arraylist_writer",
    expected_arraylist_observation="arraylist_grow_ok",
    context_label="arraylist_policy"))

# fmt
add("fmt_format_writes_to_writer_marker_01", "fmt_policy", **base(
    fake_record_name="synthetic_format_case",
    synthetic_input_bytes="demo {}",
    synthetic_output_preview="demo 42",
    requested_write_length=7,
    writer_policy_label="fmt_format",
    expected_fmt_observation="fmt_ok",
    operation_label="format",
    context_label="fmt_policy"))

add("fmt_print_context_not_run_01", "fmt_policy", **base(
    fake_record_name="synthetic_format_case",
    synthetic_input_bytes="fake_message",
    writer_policy_label="fmt_print",
    expected_status="skip",
    expected_zig_harness_observation="not_run_fmt_print",
    expected_fmt_observation="not_run",
    expected_fail_reason="fmt_print_context_not_run",
    context_label="fmt_policy"))

# json
add("json_stringify_writer_context_marker_01", "json_context", **base(
    fake_record_name="fake_json_value",
    synthetic_input_bytes='{"key":"value"}',
    synthetic_output_preview='{"key":"value"}',
    requested_write_length=15,
    writer_policy_label="json_stringify",
    expected_fmt_observation="json_ok",
    operation_label="json",
    expected_production_logger_truth="not_tested",
    expected_status="not_tested",
    expected_zig_harness_observation="not_tested",
    expected_anytype_observation="not_tested",
    expected_anywriter_observation="not_tested",
    expected_generic_writer_observation="not_tested",
    expected_write_writeall_observation="not_tested",
    expected_fixed_buffer_observation="not_tested",
    expected_arraylist_observation="not_tested",
    expected_wrapper_observation="not_tested",
    context_label="json_context",
    expected_fail_reason="json_stringify_writer_context_not_tested"))

add("custom_jsonStringify_context_marker_01", "json_context", **base(
    fake_record_name="fake_json_value",
    synthetic_input_bytes='{"x":1}',
    writer_policy_label="custom_jsonStringify",
    expected_production_logger_truth="not_tested",
    expected_status="not_tested",
    expected_zig_harness_observation="not_tested",
    expected_anytype_observation="not_tested",
    expected_anywriter_observation="not_tested",
    expected_generic_writer_observation="not_tested",
    expected_write_writeall_observation="not_tested",
    expected_fixed_buffer_observation="not_tested",
    expected_arraylist_observation="not_tested",
    expected_fmt_observation="not_tested",
    expected_wrapper_observation="not_tested",
    context_label="json_context",
    expected_fail_reason="custom_jsonStringify_context_not_tested"))

# AnyWriter / GenericWriter
add("anywriter_stored_in_struct_marker_01", "anywriter_policy", **base(
    fake_record_name="sample_struct_field",
    synthetic_input_bytes="example_log_line",
    writer_policy_label="anywriter_struct_field",
    expected_writer_type_label="AnyWriter",
    expected_stored_writer_policy="anywriter_stored",
    expected_anywriter_observation="anywriter_ok",
    context_label="anywriter_policy"))

add("generic_writer_not_single_interface_marker_01", "generic_writer_policy", **base(
    fake_record_name="toy_interface_case",
    synthetic_input_bytes="fake_message",
    writer_policy_label="generic_writer",
    expected_writer_type_label="GenericWriter",
    expected_generic_writer_observation="generic_writer_ok",
    context_label="generic_writer_policy"))

add("any_conversion_marker_01", "anywriter_policy", **base(
    fake_record_name="demo_any_writer",
    synthetic_input_bytes="sample_payload",
    writer_policy_label="any_conversion",
    expected_writer_type_label="AnyWriter",
    expected_anywriter_observation="any_conversion_ok",
    context_label="anywriter_policy"))

# Error handling
add("anyerror_erasure_context_marker_01", "typed_error_context", **base(
    fake_record_name="synthetic_error_case",
    synthetic_input_bytes="fake_message",
    writer_policy_label="anyerror_erasure",
    expected_error_set_label="anyerror",
    expected_anywriter_observation="error_erased",
    context_label="typed_error_context"))

add("typed_error_preservation_marker_01", "typed_error_context", **base(
    fake_record_name="synthetic_error_case",
    synthetic_input_bytes="fake_message",
    writer_policy_label="typed_error_preserved",
    expected_error_set_label="WriteError",
    expected_generic_writer_observation="typed_error_ok",
    context_label="typed_error_context"))

add("error_cast_context_marker_01", "typed_error_context", **base(
    fake_record_name="synthetic_error_case",
    synthetic_input_bytes="fake_message",
    writer_policy_label="error_cast",
    expected_error_set_label="anyerror",
    context_label="typed_error_context"))

# Helper methods
add("writeByte_marker_01", "anytype_policy", **base(
    fake_record_name="demo_writer",
    synthetic_input_bytes="X",
    requested_write_length=1,
    writer_policy_label="writeByte",
    operation_label="writeByte",
    context_label="anytype_policy"))

add("writeByteNTimes_or_version_fallback_marker_01", "anytype_policy", **base(
    fake_record_name="demo_writer",
    synthetic_input_bytes="AAAA",
    requested_write_length=4,
    writer_policy_label="writeByteNTimes",
    operation_label="writeByteNTimes",
    context_label="anytype_policy"))

add("helper_method_default_behavior_marker_01", "anytype_policy", **base(
    fake_record_name="demo_writer",
    synthetic_input_bytes="sample_payload",
    writer_policy_label="helper_default",
    context_label="anytype_policy"))

add("optimized_helper_not_proved_marker_01", "performance_context_not_tested", **base(
    fake_record_name="demo_writer",
    synthetic_input_bytes="sample_payload",
    writer_policy_label="optimized_helper",
    expected_production_logger_truth="not_tested",
    expected_status="not_tested",
    expected_zig_harness_observation="not_tested",
    expected_anytype_observation="not_tested",
    expected_anywriter_observation="not_tested",
    expected_generic_writer_observation="not_tested",
    expected_write_writeall_observation="not_tested",
    expected_fixed_buffer_observation="not_tested",
    expected_arraylist_observation="not_tested",
    expected_fmt_observation="not_tested",
    expected_wrapper_observation="not_tested",
    context_label="performance_context_not_tested",
    expected_fail_reason="optimized_helper_not_proved"))

# Performance / interface context
for cid, cat, label, reason, status in [
    ("dynamic_dispatch_context_marker_01", "performance_context_not_tested", "dynamic_dispatch", "dynamic_dispatch_context_not_tested", "not_tested"),
    ("function_pointer_overhead_context_marker_01", "performance_context_not_tested", "function_pointer_overhead", "function_pointer_overhead_context_not_tested", "not_tested"),
    ("monomorphization_context_marker_01", "performance_context_not_tested", "monomorphization", "monomorphization_context_not_tested", "not_tested"),
    ("code_bloat_context_not_measured_01", "performance_context_not_tested", "code_bloat", "code_bloat_context_not_measured", "not_tested"),
    ("interface_documentation_context_marker_01", "interface_documentation_context", "interface_documentation", "interface_documentation_context", "success"),
    ("rust_trait_comparison_context_not_tested_01", "interface_documentation_context", "rust_trait_comparison", "rust_trait_comparison_context_not_tested", "not_tested"),
]:
    add(cid, cat, **base(
        fake_record_name="toy_interface_case",
        synthetic_input_bytes="fake_message",
        writer_policy_label=label,
        expected_production_logger_truth="not_tested" if status=="not_tested" else "not_tested",
        expected_status=status if status in ("success","error","skip","not_tested") else "not_tested",
        expected_zig_harness_observation="interface_doc_ok" if status=="success" else "not_tested",
        expected_anytype_observation="not_tested" if status!="success" else "anytype_ok",
        expected_anywriter_observation="not_tested",
        expected_generic_writer_observation="not_tested",
        expected_write_writeall_observation="not_tested" if status!="success" else "write_ok",
        expected_fixed_buffer_observation="not_tested",
        expected_arraylist_observation="not_tested",
        expected_fmt_observation="not_tested",
        expected_wrapper_observation="not_tested",
        context_label=cat,
        expected_fail_reason=reason if status!="success" else ""))

# Composition / storage
add("composition_policy_marker_01", "interface_documentation_context", **base(
    fake_record_name="toy_interface_case",
    synthetic_input_bytes="fake_message",
    writer_policy_label="composition_policy",
    expected_anytype_observation="anytype_ok",
    context_label="interface_documentation_context"))

add("struct_field_anytype_not_allowed_context_marker_01", "interface_documentation_context", **base(
    fake_record_name="sample_struct_field",
    synthetic_input_bytes="fake_message",
    writer_policy_label="struct_field_anytype",
    expected_status="skip",
    expected_zig_harness_observation="not_run_compile_error",
    expected_anytype_observation="not_run",
    expected_fail_reason="struct_field_anytype_not_allowed",
    context_label="interface_documentation_context"))

add("tagged_union_interface_context_not_required_01", "interface_documentation_context", **base(
    fake_record_name="toy_interface_case",
    synthetic_input_bytes="fake_message",
    writer_policy_label="tagged_union_interface",
    expected_production_logger_truth="not_tested",
    expected_status="not_tested",
    expected_zig_harness_observation="not_tested",
    expected_anytype_observation="not_tested",
    expected_anywriter_observation="not_tested",
    expected_generic_writer_observation="not_tested",
    expected_write_writeall_observation="not_tested",
    expected_fixed_buffer_observation="not_tested",
    expected_arraylist_observation="not_tested",
    expected_fmt_observation="not_tested",
    expected_wrapper_observation="not_tested",
    context_label="interface_documentation_context",
    expected_fail_reason="tagged_union_interface_context_not_required"))

# Version / stdlib churn
add("stdlib_churn_new_io_context_marker_01", "version_compatibility", **base(
    fake_record_name="toy_interface_case",
    synthetic_input_bytes="fake_message",
    writer_policy_label="stdlib_churn_io",
    expected_version_compatibility_truth="local_only",
    context_label="version_compatibility"))

add("zig_version_compatibility_marker_01", "version_compatibility", **base(
    fake_record_name="toy_interface_case",
    synthetic_input_bytes="fake_message",
    writer_policy_label="zig_version_compat",
    expected_version_compatibility_truth="local_only",
    context_label="version_compatibility"))

# No real IO markers
for cid, cat, label, reason in [
    ("no_real_file_io_marker_01", "safety_scope", "no_real_file_io", "no_real_file_io"),
    ("no_network_writer_marker_01", "safety_scope", "no_network_writer", "no_network_writer"),
    ("no_unbounded_output_marker_01", "safety_scope", "no_unbounded_output", "no_unbounded_output"),
    ("no_attacker_format_string_marker_01", "safety_scope", "no_attacker_format_string", "no_attacker_format_string"),
]:
    add(cid, cat, **base(
        fake_record_name="fictional_sink",
        synthetic_input_bytes="fake_message",
        writer_policy_label=label,
        context_label=cat,
        expected_fail_reason=reason))

# Production / external not tested
for cid, cat, label, reason in [
    ("production_logger_not_tested_01", "production_logger_not_tested", "production_logger", "production_logger_not_tested"),
    ("serialization_library_not_tested_01", "production_logger_not_tested", "serialization_library", "serialization_library_not_tested"),
    ("performance_microbenchmark_not_proof_01", "performance_context_not_tested", "performance_microbenchmark", "performance_microbenchmark_not_proof"),
]:
    add(cid, cat, **base(
        fake_record_name="fictional_sink",
        synthetic_input_bytes="fake_message",
        writer_policy_label=label,
        expected_production_logger_truth="not_tested",
        expected_status="not_tested",
        expected_zig_harness_observation="not_tested",
        expected_anytype_observation="not_tested",
        expected_anywriter_observation="not_tested",
        expected_generic_writer_observation="not_tested",
        expected_write_writeall_observation="not_tested",
        expected_fixed_buffer_observation="not_tested",
        expected_arraylist_observation="not_tested",
        expected_fmt_observation="not_tested",
        expected_wrapper_observation="not_tested",
        context_label=cat,
        expected_fail_reason=reason))

# Wrapper result struct
add("writer_wrapper_result_struct_marker_01", "anytype_policy", **base(
    fake_record_name="demo_writer",
    synthetic_input_bytes="sample_payload",
    writer_policy_label="writer_wrapper_result",
    expected_wrapper_observation="wrapper_ok",
    context_label="anytype_policy"))

add("wrapper_records_bytes_requested_marker_01", "anytype_policy", **base(
    fake_record_name="demo_writer",
    synthetic_input_bytes="sample_payload",
    requested_write_length=14,
    writer_policy_label="wrapper_bytes_requested",
    expected_wrapper_observation="bytes_requested_ok",
    context_label="anytype_policy"))

add("wrapper_records_bytes_written_marker_01", "anytype_policy", **base(
    fake_record_name="demo_writer",
    synthetic_input_bytes="sample_payload",
    requested_write_length=14,
    writer_policy_label="wrapper_bytes_written",
    expected_wrapper_observation="bytes_written_ok",
    context_label="anytype_policy"))

add("wrapper_records_error_marker_01", "anytype_policy", **base(
    fake_record_name="synthetic_error_case",
    synthetic_input_bytes="fake_message",
    writer_policy_label="wrapper_records_error",
    expected_error_set_label="WriteError",
    expected_status="error",
    expected_wrapper_observation="error_recorded",
    expected_fail_reason="wrapper_records_error",
    context_label="anytype_policy"))

# Naive writer
add("naive_writer_policy_expected_fail_01", "naive_writer_policy", **base(
    fake_record_name="toy_interface_case",
    synthetic_input_bytes="fake_message",
    writer_policy_label="naive_writer",
    expected_status="error",
    expected_zig_harness_observation="naive_fail",
    expected_anytype_observation="fail",
    expected_fail_reason="naive_writer_policy_expected_fail",
    naive_expected_to_fail=True,
    context_label="naive_writer_policy"))

# External truth not tested
add("external_api_truth_not_tested_01", "external_interface_truth_not_tested", **base(
    fake_record_name="toy_interface_case",
    synthetic_input_bytes="fake_message",
    writer_policy_label="external_api_truth",
    expected_production_logger_truth="not_tested",
    expected_status="not_tested",
    expected_zig_harness_observation="not_tested",
    expected_anytype_observation="not_tested",
    expected_anywriter_observation="not_tested",
    expected_generic_writer_observation="not_tested",
    expected_write_writeall_observation="not_tested",
    expected_fixed_buffer_observation="not_tested",
    expected_arraylist_observation="not_tested",
    expected_fmt_observation="not_tested",
    expected_wrapper_observation="not_tested",
    context_label="external_interface_truth_not_tested",
    expected_fail_reason="external_api_truth_not_tested"))

# Safety caveat
add("safety_caveat_01", "safety_scope", **base(
    fake_record_name="fictional_sink",
    synthetic_input_bytes="fake_message",
    writer_policy_label="safety_caveat",
    context_label="safety_scope",
    expected_fail_reason="toy_lab_safety_caveats"))

with open("cases.json", "w") as f:
    json.dump(cases, f, indent=2)
print(f"Wrote {len(cases)} cases to cases.json")
