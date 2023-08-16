from unittest import TestCase

from retry.retryable import retryable


class Test(TestCase):
    def test_retryable(self):
        self.assertEquals(Foo().bar(), 1)

    def test_retryable_out_of_exceptions(self):
        self.assertRaises(KeyError, Foo().bar2)


class Foo:
    @retryable(exceptions=ValueError, max_attempts=1, recover='recover')
    def bar(self):
        raise ValueError()

    @retryable(exceptions=ValueError, max_attempts=1, recover='recover')
    def bar2(self):
        raise KeyError()

    def recover(self):
        return 1
