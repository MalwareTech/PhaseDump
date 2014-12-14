import sys

def rc4_crypt(data, key):
	S = list(range(256))
	j = 0
	out = []
 
	for i in range(256):
		j = (j + S[i] + ord( key[i % len(key)] )) % 256
		S[i] , S[j] = S[j] , S[i]
 
	i = j = 0
	for char in data:
		i = ( i + 1 ) % 256
		j = ( j + S[i] ) % 256
		S[i] , S[j] = S[j] , S[i]
		out.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))    
	return ''.join(out)
	
def dump_file(src, dst):
	src_file = open(src, 'rb')
	src_file.seek(16)
	file_content = src_file.read()
	src_file.close()
	
	if ord(file_content[0]) != 0x9F or ord(file_content[1]) != 0x54:
		print("Error: Not a valid Phase module")
		return
	
	decrypted_pe = rc4_crypt(file_content, "Phase")
	
	dst_file = open(dst, 'wb')
	dst_file.write(decrypted_pe)
	dst_file.close()
	
if len(sys.argv) < 3:
	print("use %s input_file output_file" % sys.argv[0]);
else:
	dump_file(sys.argv[1], sys.argv[2])