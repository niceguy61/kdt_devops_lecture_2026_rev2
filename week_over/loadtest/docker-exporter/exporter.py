import json
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import quote

SOCKET_PATH = "/var/run/docker.sock"


def docker_get(path):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.settimeout(5)
        client.connect(SOCKET_PATH)
        client.sendall(
            f"GET {path} HTTP/1.0\r\nHost: docker\r\nConnection: close\r\n\r\n".encode()
        )
        response = b""
        while True:
            chunk = client.recv(65536)
            if not chunk:
                break
            response += chunk
    header, body = response.split(b"\r\n\r\n", 1)
    headers = header.lower()
    if b"transfer-encoding: chunked" in headers:
        decoded = bytearray()
        offset = 0
        while offset < len(body):
            line_end = body.find(b"\r\n", offset)
            if line_end < 0:
                break
            size = int(body[offset:line_end].split(b";", 1)[0], 16)
            offset = line_end + 2
            if size == 0:
                break
            decoded.extend(body[offset:offset + size])
            offset += size + 2
        body = bytes(decoded)
    return json.loads(body)


def label(value):
    return str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def metric(name, value, labels):
    rendered = ",".join(f'{key}="{label(val)}"' for key, val in labels.items())
    suffix = f"{{{rendered}}}" if rendered else ""
    return f"{name}{suffix} {value}\n"


def collect():
    lines = [
        "# HELP docker_container_cpu_usage_seconds_total Cumulative CPU time used by a Docker container.",
        "# TYPE docker_container_cpu_usage_seconds_total counter",
        "# HELP docker_container_memory_working_set_bytes Current Docker container working set memory.",
        "# TYPE docker_container_memory_working_set_bytes gauge",
        "# HELP docker_container_memory_limit_bytes Docker container memory limit.",
        "# TYPE docker_container_memory_limit_bytes gauge",
        "# HELP docker_container_network_receive_bytes_total Cumulative bytes received by a Docker container.",
        "# TYPE docker_container_network_receive_bytes_total counter",
        "# HELP docker_container_network_transmit_bytes_total Cumulative bytes transmitted by a Docker container.",
        "# TYPE docker_container_network_transmit_bytes_total counter",
        "# HELP docker_container_pids Number of processes in a Docker container.",
        "# TYPE docker_container_pids gauge",
    ]
    for container in docker_get("/containers/json?all=0"):
        container_id = container["Id"]
        names = container.get("Names") or [container_id[:12]]
        container_name = names[0].lstrip("/")
        labels = {"container": container_name, "image": container.get("Image", "")}
        try:
            stats = docker_get(f"/containers/{quote(container_id, safe='')}/stats?stream=false")
            cpu = stats.get("cpu_stats", {}).get("cpu_usage", {}).get("total_usage", 0)
            cpu_seconds = cpu / 1_000_000_000
            memory = stats.get("memory_stats", {})
            inactive_file = memory.get("stats", {}).get("inactive_file", 0)
            working_set = max(memory.get("usage", 0) - inactive_file, 0)
            networks = stats.get("networks", {}).values()
            receive = sum(item.get("rx_bytes", 0) for item in networks)
            transmit = sum(item.get("tx_bytes", 0) for item in networks)
            pids = stats.get("pids_stats", {}).get("current", 0)
            lines.extend([
                metric("docker_container_cpu_usage_seconds_total", cpu_seconds, labels),
                metric("docker_container_memory_working_set_bytes", working_set, labels),
                metric("docker_container_memory_limit_bytes", memory.get("limit", 0), labels),
                metric("docker_container_network_receive_bytes_total", receive, labels),
                metric("docker_container_network_transmit_bytes_total", transmit, labels),
                metric("docker_container_pids", pids, labels),
            ])
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
            continue
    return "".join(lines).encode()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/metrics":
            self.send_response(404)
            self.end_headers()
            return
        try:
            body = collect()
            self.send_response(200)
        except (OSError, ValueError, json.JSONDecodeError):
            body = b"# exporter_collection_error 1\n"
            self.send_response(503)
        self.send_header("Content-Type", "text/plain; version=0.0.4")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):
        pass


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
