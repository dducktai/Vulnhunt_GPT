Integer Overflow/Underflow
Integer overflow/underflow vulnerability happens when an arithmetic operation attempts to create a numeric value that is outside the range of the integer type..

How to label the integer overflow/underflow vulnerability?
We refer to several expert patterns to label the integer overflow/underflow vulnerability.

arithmeticOperation that checks whether there is arithmetic operation between variables.
safeLibraryInvocation that checks whether the arithmetic operations between variables are constrained by a security library function.
conditionDeclaration that checks whether the variable for the arithmetic operation is judged by the conditional statement. We consider a function as suspicious to have a integer overflow or underflow vulnerability if it fulfills the combined pattern: ArithmeticOperation ∧ (SafeLibraryInvoc ∨ ConditionDeclaration).
arithmeticOperation
Note that we treat those functions with the arithmetic operations (e.g., +, -, *) as the target functions. As such, we first utilize the pattern arithmeticOperation to filter those functions without the arithmetic operations.

safeLibraryInvoc
Case 1: When there are arithmetic operations between the variables and the arithmetic operations are constrained by the security library function, we label the corresponding function to have no integer overflow/underflow vulnerability.

```
    1.library SafeMath {
    2.    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    3.      assert(b <= a);
    4.      return a - b;
    5.    }
    6.    function add(uint256 a, uint256 b) internal pure returns (uint256 c) {
    7.      c = a + b;
    8.      assert(c >= a);
    9.      return c;
    10.    }
    11.}
    12.contract StandardToken {
    13.    using SafeMath for uint256;
    14.    mapping(address => uint256) balances; 
    15.    function transfer(address to, uint256 value) public returns (bool) {
    16.        balances[msg.sender] = balances[msg.sender].sub(value);
    17.        balances[to] = balances[to].add(value);
    18.        return true;
    19.    }
    20.}
```
As can be seen, the subtraction operation between the balances[msg.sender] and the value (line 16) is constrained by the security library function (line 2). Thus, we label the corresponding function transfer to have no integer overflow/underflow vulnerability, i.e., label = 0.

conditionDeclaration
case 1: When the arithmetic operations and corresponding variables appear in the strict conditional statements (e.g., assert, require), we label the corresponding function to have no integer overflow/underflow vulnerability.

```
    1.contract Overflow_fixed_assert {
    2.    uint8 sellerBalance = 0;
    3.    function add(uint8 value) returns (uint) {
    4.        sellerBalance += value;
    5.        assert(sellerBalance >= value);
    6.        return sellerBalance;
    7.    }
    8.}
```
It can be observed, there is an addition operation between the sellerBalance and the value (line 4), and assert statement contains the comparison between the r_sellerBalance_ and the value (line 5). Thus, we label the corresponding function add to have no integer overflow/underflow vulnerability, i.e., label = 0.

Case 2: When the subtraction operation appears in the strict conditional statement (e.g., assert, require) for comparison and the conditional statement appears before the subtraction operation, we label the corresponding function to have no integer overflow/underflow vulnerability.

```
    1.contract HiroyukiCoinDark {
    2.    mapping(address => uint256) public balanceOf;
    3.    function transfer(address to, uint value, bytes data) public returns (bool) {
    4.        require(balanceOf[msg.sender] >= value);
    5.        balanceOf[msg.sender] = balanceOf[msg.sender] - value;
    6.        balanceOf[to] = balanceOf[_to] + value;
    7.        assert(msg.sender.call.value(value)());
    8.        return true;
    9.    }
    10.}
```
As can be seen, there is a subtraction operation between the balanceOf[msg.sender] and the value (line 5), and the require statement contains the comparison between the balanceOf[msg.sender] and the value (line 4). Thus, we label the corresponding function to have no integer overflow/underflow vulnerability, i.e., label = 0.

Case 3: When the function does not satisfy case 1 and case 2, we label the corresponding function to have integer overflow/underflow vulnerability.

```
    1. contract Overflow_add {
    2.    uint8 sellerBalance = 0;
    3.    function add(uint8 value) returns (uint) {
    4.        sellerBalance += value;
    5.        return sellerBalance;
    6.    }
    7. }
```
It can be observed, there is an addition operation between the sellerBalance and the value (line 4), and no conditional statement used to constrain the two variables after the addition operation. Thus, we label the corresponding function add to have the integer overflow/underflow vulnerability, i.e., label = 1.