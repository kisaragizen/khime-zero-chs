import re

command_convert = [
    ("005E67",          "++1".encode("gbk").hex().upper()),      # ?^g
    ("5E6E00",          "++2".encode("gbk").hex().upper()),      # ^n?
    ("5E6E",            "++3".encode("gbk").hex().upper()),      # ^n
    ("005E666D",        "++4".encode("gbk").hex().upper()),      # ?^fm
    ("5E6372",          "++5".encode("gbk").hex().upper()),      # ^cr
    ("005E6667",        "++6".encode("gbk").hex().upper()),      # ^fg
    ("00000000000000",  "++7".encode("gbk").hex().upper()),      # EOF
]
with open("translated_text.txt", "rt", encoding="gbk") as fc, \
     open("extract_text.txt", "rt", encoding="shift-jis") as fj:
    sc = fc.read()
    sj = fj.read()
sc = sc.split("\n\n")
sj = sj.split("\n\n")
hex_str_list = []
def checkcommand(c, j):
    flag1 = True if re.findall("\d\d\d", c) == re.findall("\d\d\d", j) else False
    flag2 = True if re.findall("\+\+\d", c) == re.findall("\+\+\d", j) else False
    flag3 = len(j) >= len(c)
    if flag1 and flag2 and flag3: return True
    else: return False
i = 1
for c, j in zip(sc, sj):
    if "++6" in c:
        chex = c.encode("gbk").hex()
        hex_str_list.append(chex)
        continue
    if checkcommand(c, j): print(f"\nline {i*2-1} checked:\n                  {j}\n                  {c}")
    else: raise Exception(f"\nline {i*2-1} check failed(command):\n{j}\n{c}")
    c_lines_list = c.replace("++2", "++3").replace("++1", "++3")[3:].split("++3")
    if any(len(x)>19 for x in c_lines_list): raise Exception(f"\nline {i*2-1} check failed(line-length): {c}")
    if "++2" not in c:
        chex = c.encode("gbk").hex()
        jhex = j.encode("shift-jis").hex()
        len_diff = len(jhex) - len(chex)
        chex = chex[:-6] + "0"*len_diff + "2B2B31"
        hex_str_list.append(chex)
    else:
        c_first_half_hex, c_second_half_hex = [x.encode("gbk").hex() for x in c.split("++2")]
        j_first_half_hex, j_second_half_hex = [x.encode("shift-jis").hex() for x in j.split("++2")]
        len_diff_first_half = len(j_first_half_hex) - len(c_first_half_hex)
        len_diff_second_half = len(j_second_half_hex) - len(c_second_half_hex)
        chex = c_first_half_hex + "20"*(len_diff_first_half//2) + "2B2B32" + c_second_half_hex[:-6] + "0"*len_diff_second_half + "2B2B31"
        hex_str_list.append(chex)
    i += 1
len_trans = len("".join(hex_str_list))
for j in sj[len(sc):]:
    hex_str_list.append(j.encode("shift-jis").hex())
tt = "".join(hex_str_list).upper()
len_tt = len(tt)
for replacement, pattern in command_convert:
    tt = tt.replace(pattern, replacement)
tt = bytes.fromhex(tt)
with open("extract_code.txt", "rb") as code, \
     open("2001.gsc", "wb") as total:
    total.write(code.read())
    total.write(tt)
print(f"{len(sc)}/{len(sj)} lines, {len_trans/len_tt:.2%} text translated.")
input("done.")
