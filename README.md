# Pylox - A Lox Interpreter
Project Complete 03/30/25 <br/>
![100%](https://progress-bar.xyz/100?title=Progress) <br/>
:ballot_box_with_check: Scan Tokens <br/>
:ballot_box_with_check: Generate Abstract Syntax Tree (AST) <br/>
:ballot_box_with_check: Interpret AST (basic - no classes, functions, or variables) <br/>
:ballot_box_with_check: Add support for variables <br/>
:ballot_box_with_check: Add support for loops (for/while) <br/>
:ballot_box_with_check: Add support for functions <br/>
:ballot_box_with_check: Add support for classes <br/>

Lox is a learning language written by Robert Nystrom, the "learn to create a programming language" GOAT (Greatest of All Time)<br/>

## Lox Syntax
The full overview of Lox's syntax can be viewed [here](https://craftinginterpreters.com/the-lox-language.html).
Lox is a high-level, dynamically typed, object-oriented programming language.  Overall, Lox has a C-like syntax.

### Types
The following types are supported out of the box: <br/>
<ul>
  <li>Boolean</li>
  <li>Numbers - Decimal or Integer</li>
  <li>Strings</li>
  <li>"Nil" - Sometimes referred to as Null or None in other languages</li>
</ul>

### Variables
Variables can be declared via the `var` keyword, and can be reassigned as needed.  A variable that is not given an initial value will be "Nil" by default:
```
var a = "hello world!";
print a;  // "hello world!"
a = "yeehaw!";
print a;  // "yeehaw!"
var b;
print b;  // "Nil"
```

### Control Flow
Lox contains if, while, and for loop expressions:

```
if (condition) {
  print "condition is truthy";
else (condition) {
  print "condition is falsy";
}

var a = 1;
while (a < 10) {
  print a;
  a = a + 1;
}

for (var a = 1; a < 10; a = a + 1) {
  print a;
}
```

### Functions & Closures
Functions are declared via the `fun` keyword, because functions are very fun:
```
fun my_function(a) {
  return a + 10;
}
```
Functions may be called by entering the function name followed by parentheses and any arguments required like `my_function(a);`.  For a function with no arguments, only the parentheses are required: `other_function();`. <br/>

Functions are first-class objects, so they can be passed around in variables:
```
fun get_fun(function) {
  return function;
}

fun add(a, b) {
  return a + b;
}

print get_fun(add)(10, 10);  // prints "20"
```

Closures can be added within any function and returned, such as in the following example:
```
fun return_function() {
  var outside = "outside";

  fun inner() {
    print outside;
  }

  return inner;
}

var fn = return_function();
fn();  // "outside"
```



