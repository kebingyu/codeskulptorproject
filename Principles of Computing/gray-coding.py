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
        for idx in range(0, length):
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
        for number in previous_result.reverse():
            result.append('1' + number)
        return result

#for string in make_binary(4):
#    print bin_to_dec(string)
print make_gray(3)
