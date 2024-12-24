Reentrancy
Reentrancy vulnerability is considered as an invocation to call.value that can call back to itself through a chain of calls.

How to label the reentrancy vulnerability?
We refer to several expert patterns to label the reentrancy vulnerability.

callValueInvocation that checks whether there exists an invocation to call.value in the function.
balanceDeduction checks whether the user balance is deducted after money transfer using call.value, which considers the fact that the money stealing can be avoided if user balance is deducted each time before money transfer.
zeroParameter checks whether the parameter of the call.value function itself is zero.
ModifierConstrain checks whether the function is constrained by the onlyOwner modifier. We consider a function as suspicious to have a reentrancy vulnerability if it fulfills the combined pattern: callValueInvocation ∧ balanceDeduction ∧ zeroParameter ∧ (!ModifierConstrain).
callValueInvocation
Note that we treat those functions with an invocation to call.value as the target functions. As such, we first utilize the pattern callValueInvocation to filter those functions without an invocation to call.value.

zeroParameter
Case 1: When the call.value exists in the function and the parameter of the call.value is zero, we label the corresponding function to have no reentrancy vulnerability, i.e., label = 0.

 ```
    1.contract HiroyukiCoinDark {
    2.    mapping(address => uint256) public balanceOf;
    3.    function transfer(address _to, uint _value, bytes _data) public returns (bool) {
    4.        require(balanceOf[msg.sender] >= _value);
    5.        balanceOf[msg.sender] = balanceOf[msg.sender] - _value;
    6.        balanceOf[_to] = balanceOf[_to] + _value;
    7.        assert(msg.sender.call.value(0)());
    8.        return true;
    9.    }
    10.}
```
As can be seen, the parameter of call.value is zero (line 7). Thus, we label that the function transfer dose not exist the reentrancy vulnerability, i.e., label = 0.

balanceDeduction
Case 1: When the parameter of call.value is not zero and the user balance is deducted before money transfer using call.value, we label the corresponding function to have no reentrancy vulnerability, i.e., label = 0.

```
    1.contract NIZIGEN {
    2.    mapping (address => uint) balances;  
    3.    function transfer(uint _value, bytes _data) public returns (bool) { 
    4.      if(true) {
    5.          if (balances[msg.sender] < _value) revert();
    6.          balances[msg.sender] = balances[msg.sender] - _value;
    7.          assert(msg.sender.call.value(_value)(_data));
    8.          return true;
    9.      }
    10.      else {
    11.          return false;
    12.      }
    13.    }
    14.}
```
It can be observed, the user balance balances[msg.sender](line 6) is deducted before money transfer using call.value (line 7). Thus, we label the corresponding function to have no reentrancy vulnerability, i.e., label = 0.

modifierDeclaration
Case 1: When a function has the onlyOwner modifier constraint, we label the corresponding function to have no reentrancy vulnerability.

```
    1.contract CrowdsaleWPTByRounds {
    2.  mapping (address => uint) balances;
    3.  address wallet;
    4.  address owner;
    5.  modifier onlyOwner() {
    6.    require(msg.sender == owner);
    7.    _;
    8.  }   
    9.  function forwardFunds() internal onlyOwner {
    10.     wallet.call.value(msg.value).gas(10000000)();
    11.     balances[wallet] -= msg.value;
    12.  }
    13.}
```
As can be seen, the function forwardFunds is constrained by the onlyOwner modifier(line 9). Thus, we label the function forwardFunds to have no reentrancy vulnerability, i.e., label = 0.

Case 2: When a function has not the onlyOwner modifier constraint, we label the corresponding function to have the reentrancy vulnerability.

  ```
    1.contract CrowdsaleWPTByRounds {
    2.  mapping (address => uint) balances;
    3.  address wallet;
    4.  function forwardFunds() internal {
    5.    wallet.call.value(msg.value).gas(10000000)();
    6.    balances[wallet] -= msg.value;
    7.  }
    8.}
```
It can be observed, the function forwardFunds is not constrained by the onlyOwner modifier(line 9). Thus, we label the function forwardFunds to have the reentrancy vulnerability, i.e., label = 1.