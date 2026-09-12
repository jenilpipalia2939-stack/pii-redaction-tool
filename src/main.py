from detectors import detect_ip_addresses


text_file_path = "output/extracted_text.txt"

with open(text_file_path, "r", encoding="utf-8") as file:
    text = file.read()


ips = detect_ip_addresses(text)

print(f"IP addresses detected: {len(ips)}")

for ip in ips:
    print(ip)