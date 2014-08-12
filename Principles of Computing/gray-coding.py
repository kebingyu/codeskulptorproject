def make_binary(length):
    if 0 == length:
        return ['']
    else:
        result = []
        previous_result = make_binary(length - 1)
        for number in previous_result:
            result.append('0' + number)
        for number in previous_result:
            result.append('1' + number)
        return result
    
def bin_to_dec(bin_num):
    length = len(bin_num)
    if 0 == length:
        return 0
    else:
        sig_idx = None
        for idx in range(length):
            if '1' == bin_num[idx]:
                sig_idx = idx
                break;
        if sig_idx == None:
            return 0
        else:
            return 2 ** (length - sig_idx - 1) + bin_to_dec(bin_num[sig_idx + 1:])
        
def make_gray(length):
    if 0 == length:
        return ['']
    else:
        result = []
        previous_result = make_gray(length - 1)
        for number in previous_result:
            result.append('0' + number)
        for number in previous_result[::-1]:
            result.append('1' + number)
        return result
    
def gray_to_bin(gray_code):
    bin_code = ''
    sig_found = False
    for idx in range(len(gray_code)):
        if not sig_found:
            bin_code += gray_code[idx]
            if gray_code[idx] == '1':
                sig_found = True
        else:
            bin_code += str(int(gray_code[idx]) ^ int(bin_code[idx - 1]))
    return bin_code
                

#for string in make_binary(4):
#    print bin_to_dec(string)
print make_gray(3)
for code in make_gray(3):
    print bin_to_dec(gray_to_bin(code))
