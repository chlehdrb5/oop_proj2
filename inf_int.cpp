#include "inf_int.h"
#include <cmath>
#include <string.h>
#include <algorithm>

//
// to be filled by students
//
// example :
//
// bool operator==(const inf_int& a , const inf_int& b)
// {
//     // we assume 0 is always positive.
//     if ( (strcmp(a.digits , b.digits)==0) && a.thesign==b.thesign )
//         return true;
//     return false;
// }
//

void inf_int::swap(inf_int& n1, inf_int& n2) {
    inf_int tmp = n1;
    n1 = n2;
    n2 = tmp;
}

int inf_int::compare_abs(const inf_int& n1, const inf_int& n2) {
    if (strcmp(n1.digits, n2.digits) == 0) return 0;
    else if (n1.length > n2.length) return 1;
    else if (n2.length > n1.length) return -1;

    for (int i = n1.length - 1; i > -1; i--) {
        if (n1.digits[i] > n2.digits[i]) return 1;
        else if (n2.digits[i] > n1.digits[i]) return -1;
    }
    return 0;
}

inf_int::inf_int() {
    length = 1;
    digits = new char[length + 1];
    digits[0] = '0';
    digits[1] = 0;
    the_sign = true;
}

inf_int::inf_int(int n) {
    length = (int)log10(std::abs(n)) + 1;
    digits = new char[length + 1];
    digits[length] = 0;
    the_sign = n >= 0;
    int idx = 0;
    while (n != 0) {
        int digit = n % 10;
        n /= 10;
        digits[idx++] = digit + '0';
    }
}

inf_int::inf_int(const char* n) {
    the_sign = true;
    if (n[0] == '-') {
        the_sign = false;
        n++;
    }
    length = strlen(n);
    digits = new char[length + 1];
    digits[length] = 0;
    strcpy_s(digits, length + 1, n); // 정건우, strcpy->strcpy_s
    std::reverse(digits, digits + length);
}

inf_int::inf_int(const inf_int& origin) {
    length = origin.length;
    the_sign = origin.the_sign;
    digits = new char[length + 1];
    digits[length] = 0;
    strcpy_s(digits, length + 1, origin.digits);  // 정건우, strcpy->strcpy_s
}

inf_int::~inf_int() {
    delete digits;
}

inf_int& inf_int::operator=(const inf_int& source) {
    if (this == &source) return *this;

    delete digits;
    length = source.length;
    the_sign = source.the_sign;
    digits = new char[length + 1];
    digits[length] = 0;
    strcpy_s(digits, length+1, source.digits); // 정건우, strcpy->strcpy_s

    return *this;
}

bool operator==(const inf_int& n1, const inf_int& n2) {
    if (n1.the_sign != n2.the_sign || n1.length != n2.length || strcmp(n1.digits, n2.digits) != 0) return false;
    return true;
}

bool operator!=(const inf_int& n1, const inf_int& n2) {
    return !(n1 == n2);
}

bool operator>(const inf_int& n1, const inf_int& n2) {
    if (n1 == n2) return false;
    return (n1 - n2).the_sign;
}

bool operator<(const inf_int& n1, const inf_int& n2) {
    if (n1 == n2) return false;
    return !(n1 - n2).the_sign;
}

inf_int operator+(const inf_int& n1, const inf_int& n2) {
    if (n1.the_sign ^ n2.the_sign) return n1 - n2;
    int carry = 0;
    int length = std::max(n1.length, n2.length) + 1;
    char* tmp = new char[length + 1];
    tmp[length] = 0;
    for (int i = 0; i < length; i++) {
        int n1_digit = n1.length > i ? n1.digits[i] - '0' : 0;
        int n2_digit = n2.length > i ? n2.digits[i] - '0' : 0;
        tmp[i] = (carry + n1_digit + n2_digit) % 10 + '0';
        carry = (carry + n1_digit + n2_digit) / 10;
    }
    std::reverse(tmp, tmp + length);
    int i = 0;
    while (tmp[i] == '0') i++;
    inf_int ret = { tmp + i };
    ret.the_sign = n1.the_sign;

    delete[] tmp;
    return ret;
}

inf_int operator-(const inf_int& n1, const inf_int& n2) {
    if (n1.the_sign ^ n2.the_sign) {
        inf_int tmp = n2;
        tmp.the_sign = !tmp.the_sign;
        return n1 + tmp;
    }
    int borrow = 0;
    inf_int _n1 = n1, _n2 = n2;
    if (inf_int::compare_abs(n2, n1) > 0) {
        inf_int::swap(_n1, _n2);
    }
    int length = std::max(n1.length, n2.length);
    char* tmp = new char[length + 1];
    tmp[length] = 0;
    for (int i = 0; i < length; i++) {
        int n1_digit = _n1.length > i ? _n1.digits[i] - '0' : 0;
        int n2_digit = _n2.length > i ? _n2.digits[i] - '0' : 0;
        int tmp_digit = (n1_digit - n2_digit - borrow);
        tmp[i] = (tmp_digit >= 0 ? tmp_digit : 10 + tmp_digit) + '0';
        borrow = tmp_digit < 0 ? 1 : 0;
    }

    std::reverse(tmp, tmp + length);
    int i = 0;
    while (tmp[i] == '0') i++;
    inf_int ret = { tmp + i };
    ret.the_sign = (inf_int::compare_abs(n1, n2) < 0) ? false : true;

    delete[] tmp;
    return ret;
}

std::ostream& operator<<(std::ostream& os, const inf_int& n) {
    std::reverse(n.digits, n.digits + n.length);
    os << ((!n.the_sign) ? "-" : "") << n.digits;
    std::reverse(n.digits, n.digits + n.length);
    return os;
}

inf_int operator*(const inf_int& n1, const inf_int& n2) {
    inf_int sum;
    int length = n1.length + 1;
    for (int i = 0; i < n2.length; i++) {
        char* tmp = new char[length + i + 1];
        tmp[length + i] = 0;
        std::fill(tmp, tmp + length + i, '0');
        int carry = 0;
        for (int j = 0; j < length; j++) {
            int n1_digit = n1.length > j ? n1.digits[j] - '0' : 0;
            int n2_digit = n2.digits[i] - '0';
            tmp[j + i] = (n1_digit * n2_digit + carry) % 10 + '0';
            carry = (n1_digit * n2_digit + carry) / 10;
        }
        std::reverse(tmp, tmp + length + i);
        int idx = 0;
        while (idx < length + i - 1 && tmp[idx] == '0') idx++;
        sum = sum + inf_int(tmp + idx);
        delete[] tmp; // 정건우, free -> delelte
    }
    return sum;
}
