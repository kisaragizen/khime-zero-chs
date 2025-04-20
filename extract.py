with open("2001.gsc", "rb") as f:
    data = f.read()
    extracted_code = data[:0xB2F4]
    extracted_data = data[0xB2F4:]
command_convert = [
    ("005E67",          "++1".encode("gbk").hex().upper()),      # ?^g
    ("5E6E00",          "++2".encode("gbk").hex().upper()),      # ^n?
    ("5E6E",            "++3".encode("gbk").hex().upper()),      # ^n
    ("005E666D",        "++4".encode("gbk").hex().upper()),      # ?^fm
    ("5E6372",          "++5".encode("gbk").hex().upper()),      # ^cr
    ("005E6667",        "++6".encode("gbk").hex().upper()),      # ^fg
    ("00000000000000",  "++7".encode("gbk").hex().upper()),      # EOF
]
hex_data = extracted_data.hex().upper()
for pattern, replacement in command_convert:
    hex_data = hex_data.replace(pattern, replacement)
converted_data = bytes.fromhex(hex_data).decode("shift-jis").replace("++1", "++1\n\n")
with open("extract_text.txt", "wt", encoding="shift-jis") as f1, \
     open("extract_code.txt", "wb") as f2:
    f1.write(converted_data)
    f2.write(extracted_code)
input("done.")