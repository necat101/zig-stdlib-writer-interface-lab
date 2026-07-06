const std = @import("std");

const CountingWriter = struct {
    bytes_written: usize = 0,
    fn writer(self: *CountingWriter) Writer {
        return .{ .context = self };
    }
    const Writer = std.io.Writer(*CountingWriter, error{}, countWrite);
    fn countWrite(self: *CountingWriter, bytes: []const u8) error{}!usize {
        self.bytes_written += bytes.len;
        return bytes.len;
    }
};

const FailingWriter = struct {
    fn writer(self: *FailingWriter) Writer {
        return .{ .context = self };
    }
    const Writer = std.io.Writer(*FailingWriter, error{WriteFailed}, failWrite);
    fn failWrite(self: *FailingWriter, bytes: []const u8) error{WriteFailed}!usize {
        _ = self; _ = bytes;
        return error.WriteFailed;
    }
};

const PartialWriter = struct {
    bytes_written: usize = 0,
    fn writer(self: *PartialWriter) Writer {
        return .{ .context = self };
    }
    const Writer = std.io.Writer(*PartialWriter, error{}, partialWrite);
    fn partialWrite(self: *PartialWriter, bytes: []const u8) error{}!usize {
        const n = @min(bytes.len / 2 + 1, bytes.len);
        self.bytes_written += n;
        return n;
    }
};

fn writeAny(w: anytype, bytes: []const u8) !usize {
    return try w.write(bytes);
}

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    const allocator = gpa.allocator();

    const args = try std.process.argsAlloc(allocator);
    defer std.process.argsFree(allocator, args);
    if (args.len < 2) return error.MissingArg;
    const case_path = args[1];
    const case_file = try std.fs.cwd().readFileAlloc(allocator, case_path, 1 << 20);
    defer allocator.free(case_file);

    // crude json parse – extract synthetic_input_bytes, requested_write_length, writer_policy_label
    var input_bytes: []const u8 = "fake_message";
    var write_len: usize = 16;
    var policy: []const u8 = "anytype_policy";

    if (std.mem.indexOf(u8, case_file, "\"synthetic_input_bytes\"")) |i| {
        const p = case_file[i..];
        if (std.mem.indexOf(u8, p, ":")) |c| {
            var j = c + 1;
            while (j < p.len and (p[j] == ' ' or p[j] == '\t' or p[j] == '"')) : (j += 1) {}
            const start = j;
            while (j < p.len and p[j] != '"' and p[j] != ',' and p[j] != '\n' and p[j] != '}') : (j += 1) {}
            if (j > start) input_bytes = std.mem.trim(u8, p[start..j], "\" \t\r\n");
        }
    }
    if (std.mem.indexOf(u8, case_file, "\"requested_write_length\"")) |i| {
        const p = case_file[i..];
        if (std.mem.indexOfScalar(u8, p, ':')) |c| {
            var j = c + 1;
            while (j < p.len and (p[j] == ' ' or p[j] == '\t')) : (j += 1) {}
            var k = j;
            while (k < p.len and p[k] >= '0' and p[k] <= '9') : (k += 1) {}
            if (k > j) write_len = std.fmt.parseInt(usize, p[j..k], 10) catch 16;
        }
    }
    if (std.mem.indexOf(u8, case_file, "\"writer_policy_label\"")) |i| {
        const p = case_file[i..];
        if (std.mem.indexOf(u8, p, ":")) |c| {
            const q = p[c..];
            if (std.mem.indexOfScalar(u8, q, '"')) |q1| {
                const r = q[q1+1..];
                if (std.mem.indexOfScalar(u8, r, '"')) |q2| {
                    policy = r[0..q2];
                }
            }
        }
    }

    // anytype writer test – ArrayList
    {
        var list = std.ArrayList(u8).init(allocator);
        defer list.deinit();
        const w = list.writer();
        const n = @min(write_len, input_bytes.len);
        _ = try writeAny(w, input_bytes[0..n]);
    }

    // fixed buffer writer
    {
        var buf: [4096]u8 = undefined;
        var fbs = std.io.fixedBufferStream(&buf);
        const w = fbs.writer();
        const n = @min(write_len, input_bytes.len);
        const to_write = input_bytes[0..@min(n, buf.len)];
        _ = w.write(to_write) catch 0;
    }

    // counting writer
    {
        var cw = CountingWriter{};
        const w = cw.writer();
        const n = @min(write_len, input_bytes.len);
        _ = try writeAny(w, input_bytes[0..n]);
    }

    // failing writer – expect error, catch it
    if (std.mem.indexOf(u8, policy, "failing") != null or std.mem.indexOf(u8, policy, "fail") != null) {
        var fw = FailingWriter{};
        const w = fw.writer();
        _ = w.write(input_bytes) catch {};
    }

    // partial writer + writeAll simulation
    {
        var pw = PartialWriter{};
        const w = pw.writer();
        var remaining = input_bytes[0..@min(write_len, input_bytes.len)];
        while (remaining.len > 0) {
            const n = try w.write(remaining);
            if (n == 0) break;
            remaining = remaining[n..];
        }
    }

    // fmt.format test
    {
        var list = std.ArrayList(u8).init(allocator);
        defer list.deinit();
        const w = list.writer();
        try std.fmt.format(w, "wrote {d} bytes", .{write_len});
    }

    std.debug.print("{{\"zig_harness_status\":\"ok\",\"write_len\":{d},\"policy\":\"{s}\"}}\n", .{ write_len, policy });
}
