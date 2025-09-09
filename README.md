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

Lox is a learning language written by Robert Nystrom, the "learn to create a programming language" GOAT<br/>

Pylox is a python interpreter for Lox.

## Running the Interpreter
After cloning the repository, run:
```
python3 main.py lox_file.lox
```
I've included a file called `test.lox` with a myriad of different scenarios to make sure everything is working.  There is not a simple `lox` command available on the command line, as this project is meant to be mainly educational and does not need any more additions for usability.

## Notes on The Interpreter's Design
The interpreter is built in Python, using only Python's standard library.  It uses the "recursive descent" pattern for parsing the tokens into a usable AST for both the resolver and the interpreter; a pattern that is useful when developing an interpreter as a one-man-show since it does not require using any fancy libraries.

### Use of the Visitor Pattern
The interpreter and resolver rely heavily on the "visitor pattern" - an incredibly useful pattern for adding functionality, in this case new "types" (such as a class that represents a function declaration), without needing to handle functionality (such as being interpreted, or resolved) in the class itself. <br/>
As a more concrete example (in Python):

```
class Fork():
  def accept(self, visitor):
    return visitor.visit_fork()

class Spoon():
  def accept(self, visitor):
    return visitor.visit_spoon()
```

The `Fork` and `Spoon` classes can now change their behavior based on the classes that they are called from, instead of having to implement functionality multiple times within themselves:

```
class DiningPerson():
  def visit_spoon():
    pass # implement method for using a spoon when eating

  def visit_fork():
    pass # implement method for using a fork when eating

class DishWasher():
  def visit_spoon():
    pass # implement method for washing a spoon

  def visit_fork():
    pass # implement method for washing a fork
```
Now if we need to add a new utensil such as a knife, we only need to add a knife visitor function (`visit_knife`, probably) in the `DishWasher` and `DiningPerson` classes.  Within these classes, we can simply call the `accept` method on whatever object we encounter and the behavior is determined by the calling class.<br/>

This pattern was particularly useful in the case where a new feature needed to be added - such as classes or functions and instead of adding a massive class that handles how it is interpreted or resolved, it could be added with a simple `accept` method and that logic could be offloaded onto the interpreter and resolver.<br/>

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

### Classes
Classes are simple; they support methods and properties.  Use the special method `init` to set behavior at initialization. Class methods do not use the `fun` keyboard when adding methods.  Inheritance is not supported

```
class Beets {
  init() {
    this.property = "special property";
  }

  eat() {
    print "yum, that is a tasty beet";
  }
}
```

### Built-In Functions
Lox has one built in function: `clock()`, which returns unix time stamp.


