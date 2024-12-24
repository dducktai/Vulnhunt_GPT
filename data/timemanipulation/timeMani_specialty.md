 Time manipulation
The time manipulation vulnerability exists when a smart contract uses the block.timestamp as part of the conditions to perform critical operations.

How to label the time manipulation vulnerability?
We refer to several patterns to label the timestamp dependence vulnerability.

TDInvocation models whether there exists an invocation to block.timestamp in the function.
TDAssign checks whether the value of block.timestamp is assigned to other variables or passed to a condition statement as a parameter, namely whether block.timestamp is actually used.
TDContaminate checks if block.timestamp may contaminate the triggering condition of a critical operation (e.g., money transfer) or the return value. We consider a function as suspicious to have a timestamp dependence vulnerability if it fulfills the combined pattern: TimestampInvoc ∧ (TimestampAssign ∨ TimestampContaminate).
TDInvocation
Note that we treat those functions with the block.timestamp statement as the target functions. As such, we first utilize the pattern timestampInvoc to filter those functions without the statement of block.timestamp.

TDAssign
Case 1: When the block.timestamp is assigned to a variable and the variable is used by the following operations or passed to a condition statement as a parameter, we label the corresponding function to have the time manipulation vulnerability.

```    
    1.contract CrowdsaleWPTByRounds {
    2.    uint256 public closingTime;       
    3.    function closeRound() public returns(uint256) {
    4.        closingTime = block.timestamp + 1;
    5.        return closingTime;
    6.    }
    7.}
```
As can be seen, the block.timestamp is assigned to variable closingTime (line 4), and the variable closingTime is called in the return statement (line 5). Thus, we label the function closeRound to have the time manipulation vulnerability, i.e., label = 1.

Case 2: When the block.timestamp is assigned in the strict condition statements (e.g., require and assert), we label the corresponding function to have no time manipulation vulnerability.

```    
    1.contract Safe {
    2.    address public owner;
    3.    uint256 public lock;        
    4.    function withdrawal( address to, uint value) returns (bool) {
    5.        require(msg.sender == owner);
    6.        uint256 time = block.timestamp;
    7.        require(time >= lock);
    8.        require(to != address(0));
    9.        return true;
    10.    }
    11.}
```
It can be observed, the block.timestamp is assigned to the variable time (line 6), and the variable time is assigned in the require statement (line 7). Thus, we label the function withdrawal to have no time manipulation vulnerability, i.e., label = 0.

TDContaminate
case 1: When the body of the conditional statement (e.g. if and while) involves the return value of the function, we label the corresponding function to have the time manipulation vulnerability.

```
    1.contract CrowdsaleExt {
    2.    uint public startsAt;
    3.    uint public endsAt;
    4.    bool public finalized;
    5.    enum State {PreFunding, Failure, Finalized}
    6.    function getState() public constant returns (State) {
    7.         if(finalized) return State.Finalized;
    8.         else if (block.timestamp < startsAt) return State.PreFunding;
    9.         else return State.Failure;
    10.   }
    11.}
 ``` 
As can be seen, when the conditional statement else if satisfies block.timestamp < startsAt (line8), the return value of the function getState is State.PreFunding. Thus, we label the function getState to have the time manipulation vulnerability, i.e., label = 1.

Case 2: When the body of the conditional statement involves money operations (e.g.,transfers), we label the corresponding function to have the time manipulation vulnerability.

```
    1.contract FreezableToken {
    2.    function releaseAll() public returns (uint tokens) {
    3.         uint release;
    4.         uint balance;
    5.         while (release != 0 && block.timestamp > release) {
    6.                tokens += balance;
    7.                msg.sender.call.value(tokens);
    8.         }
    9.         return tokens;
    10.   }
    11.}
```
It can be observed, when the conditional statement while satisfies release != 0 && block.timestamp > release (line 5), the function executes the call.value transfer operation (line 7). Thus, we label the function releaseAll to have the time manipulation vulnerability, i.e., label = 1.

Case 3: When the body of the conditional statement is not related to the return value of the function or money operations (e.g., transfer), we label the corresponding function to have no time manipulation vulnerability.

```
    1.contract BirthdayGift {
    2.    address public recipient;
    3.    uint public birthday;
    4.    function Take () {
    5         if (msg.sender != recipient) throw;
    6.        if (block.timestamp < birthday) throw;
    7.        if (!recipient.send (this.balance)) throw;
    8.        return;
    9.    }
    10.}
```
As can be seen, when the conditional statement if satisfies block.timestamp < birthday (line 6), the function Take throws an exception. Thus, we label the function Take to have no time manipulation vulnerability, i.e., label = 0.