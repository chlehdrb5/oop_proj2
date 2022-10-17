#include "inf_int.h"
#include <cmath>
#include <cstring>
#include <algorithm>
#include <vector>


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

void inf_int::swap(inf_int& n1, inf_int &n2) {
    inf_int tmp = n1;
    n1 = n2;
    n2 = tmp;
}

int inf_int::compare_abs(const inf_int &n1, const inf_int &n2) {
    if(strcmp(n1.digits, n2.digits) == 0) return 0;
    else if(n1.length > n2.length) return 1;
    else if(n2.length > n1.length) return -1;

    for(int i=n1.length - 1;i>-1;i--) {
        if(n1.digits[i] > n2.digits[i]) return 1;
        else if(n2.digits[i] > n1.digits[i]) return -1;
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
    length = (int) log10(std::abs(n)) + 1;
    digits = new char[length + 1];
    digits[length] = 0;
    the_sign = n >= 0;
    n = std::abs(n);
    int idx = 0;
    while(n != 0) {
        int digit = n % 10;
        n /= 10;
        digits[idx++] = digit + '0';
    }
}

inf_int::inf_int(const char *n) {
    the_sign = true;
    if(n[0] == '-') {
        the_sign = false;
        n++;
    }
    length = strlen(n);
    digits = new char[length + 1];
    digits[length] = 0;
    strcpy(digits, n);
    std::reverse(digits, digits + length);
}

inf_int::inf_int(const inf_int &origin) {
    length = origin.length;
    the_sign = origin.the_sign;
    digits = new char[length + 1];
    digits[length] = 0;
    strcpy(digits, origin.digits);
}

inf_int::~inf_int() {
    delete digits;
}

inf_int &inf_int::operator=(const inf_int &source) {
    if(this == &source) return *this;

    delete digits;
    length = source.length;
    the_sign = source.the_sign;
    digits = new char[length + 1];
    digits[length] = 0;
    strcpy(digits, source.digits);

    return *this;
}

bool operator==(const inf_int &n1, const inf_int &n2) {
    if(n1.the_sign != n2.the_sign || n1.length != n2.length || strcmp(n1.digits, n2.digits) != 0) return false;
    return true;
}

bool operator!=(const inf_int &n1, const inf_int &n2) {
    return !(n1 == n2);
}

bool operator>(const inf_int &n1, const inf_int &n2) {
    if(n1 == n2) return false;
    return (n1 - n2).the_sign;
}

bool operator<(const inf_int &n1, const inf_int &n2) {
    if(n1 == n2) return false;
    return !(n1 - n2).the_sign;
}

inf_int operator+(const inf_int &n1, const inf_int &n2) {
    if(n1.the_sign ^ n2.the_sign) return n1 - n2;
    int carry = 0;
    int length = std::max(n1.length, n2.length) + 1;
    char *tmp = new char[length + 1];
    tmp[length] = 0;
    for(int i=0;i<length;i++){
        int n1_digit = n1.length > i ? n1.digits[i]  - '0' : 0;
        int n2_digit = n2.length > i ? n2.digits[i] - '0' : 0;
        tmp[i] = (carry + n1_digit + n2_digit) % 10 + '0';
        carry = (carry + n1_digit + n2_digit) / 10;
    }
    std::reverse(tmp, tmp + length);
    int i = 0;
    while(tmp[i] == '0') i++;
    inf_int ret = {tmp + i};
    ret.the_sign = n1.the_sign;

    delete[] tmp;
    return ret;
}

inf_int operator-(const inf_int &n1, const inf_int &n2) {
    if(n1.the_sign ^ n2.the_sign) {
        inf_int tmp = n2;
        tmp.the_sign = !tmp.the_sign;
        return n1 + tmp;
    }
    int borrow = 0;
    inf_int _n1 = n1, _n2 = n2;
    if(inf_int::compare_abs(n2, n1) > 0) {
        inf_int::swap(_n1, _n2);
    }
    int length = std::max(n1.length, n2.length);
    char *tmp = new char[length + 1];
    tmp[length] = 0;
    for(int i=0;i<length;i++){
        int n1_digit = _n1.length > i ? _n1.digits[i]  - '0' : 0;
        int n2_digit = _n2.length > i ? _n2.digits[i] - '0' : 0;
        int tmp_digit = (n1_digit - n2_digit - borrow);
        tmp[i] = (tmp_digit >= 0 ? tmp_digit : 10 + tmp_digit) + '0';
        borrow = tmp_digit < 0 ? 1 : 0;
    }

    std::reverse(tmp, tmp + length);
    int i = 0;
    while(tmp[i] == '0') i++;
    inf_int ret = {tmp + i};
    ret.the_sign = (inf_int::compare_abs(n1, n2) < 0) ? false : true;

    delete[] tmp;
    return ret;
}

std::ostream &operator<<(std::ostream &os, const inf_int &n) {
    std::reverse(n.digits, n.digits + n.length);
    os << ((!n.the_sign) ? "-" : "") << n.digits;
    std::reverse(n.digits, n.digits + n.length);
    return os;
}

inf_int operator*(const inf_int& n1, const inf_int& n2) {
    std::vector<int> a;
    std::vector<int> b;

    for(int i=0;i<n1.length;i++) a.push_back(n1.digits[i] - '0');
    for(int i=0;i<n2.length;i++) b.push_back(n2.digits[i] - '0');

    std::vector<int> ret = inf_int::multiply(a, b);
    int i = 0;
    while (i < ret.size()) {
        if (ret[i] >= 10) {
            if (i == ret.size() - 1)
                ret.push_back(ret[i] / 10);
            else
                ret[i + 1] += ret[i] / 10;
            ret[i] %= 10;
        }
        ++i;
    }

    while(!ret.empty() && ret.back() == 0) ret.pop_back();

    inf_int res;
    res.length = ret.size();
    res.digits = new char[res.length];
    for(int i=0;i<res.length;i++) res.digits[i] = ret[i] + '0';

    res.the_sign = !(n1.the_sign ^ n2.the_sign);
    return res;
}

//inf_int operator*(const inf_int &n1, const inf_int &n2) {
//    inf_int sum;
//    int length = n1.length + 1;
//    for(int i=0;i<n2.length;i++){
//        char *tmp = new char[length + i + 1];
//        tmp[length + i] = 0;
//        std::fill(tmp, tmp + length + i, '0');
//        int carry = 0;
//        for(int j=0;j<length;j++){
//            int n1_digit = n1.length > j ? n1.digits[j] - '0' : 0;
//            int n2_digit = n2.digits[i] - '0';
//            tmp[j + i] = (n1_digit * n2_digit + carry) % 10 + '0';
//            carry = (n1_digit * n2_digit + carry) / 10;
//        }
//        std::reverse(tmp, tmp + length + i);
//        int idx=0;
//        while(idx < length + i - 1 && tmp[idx] == '0') idx++;
//        sum = sum + inf_int(tmp + idx);
//        free(tmp);
//    }
//    return sum;
//}

void fft(std::vector<base> &a, bool inv) {
    int n = (int)a.size();
    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        while (!((j ^= bit) & bit)) bit >>= 1;
        if (i < j) std::swap(a[i], a[j]);
    }
    for (int i = 1; i < n; i <<= 1) {
        double x = (inv ? 1 : -1) * M_PI / i;
        base w = { cos(x), sin(x) };
        for (int j = 0; j < n; j += i << 1) {
            base th(1);
            for (int k = 0; k < i; k++) {
                base tmp = a[i + j + k] * th;
                a[i + j + k] = a[j + k] - tmp;
                a[j + k] += tmp;
                th *= w;
            }
        }
    }
    if (inv) {
        for (int i = 0; i < n; i++) a[i] /= n;
    }
}

int power_of_2_ge_than(int n) {
    int ret = 1;
    while (n > ret) ret <<= 1;
    return ret;
}

std::vector<int> inf_int::multiply(std::vector<int> &A, std::vector<int> &B) {
    std::vector<base> a(A.begin(), A.end());
    std::vector<base> b(B.begin(), B.end());
    int n = power_of_2_ge_than(std::max(a.size(), b.size())) * 2;

    a.resize(n);	b.resize(n);
    fft(a, false);	fft(b, false);

    for (int i = 0; i < n; i++)
        a[i] *= b[i];
    fft(a, true);

    std::vector<int> ret(n);
    for (int i = 0; i < n; i++)
        ret[i] = (int)round(a[i].real());
    return ret;
}
