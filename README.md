# python-retry

This provides retry support for a class method as a method decorator.

## Usage
```python
@retryable(exceptions=None, max_attempts=2, pre_handler=None, recover=None, allow_log=False)
    :param exceptions: specify a error class or a list of error classes to capture for retry 
    :param max_attempts: number, maximum execution count including first calling
    :param pre_handler: string, a method name which is called before retry 
    :param recover: string, a method name which is called when all attempts failed. A return value of this method is used as a return value.
    :param allow_log: bool, decide if logging or not when retry


# Example;
# This code retries the bar method when ValueError occurs on executing the bar.
from retry.retryable import retryable


class Foo:
    @retryable(exceptions=ValueError, max_attempts=3, recover='recover')
    def bar(self):
        ...

    def recover(self):
        return "recovery value"
```
