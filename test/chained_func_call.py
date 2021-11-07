def foo(next=True):
    print('foo')
    return next


def bar():
    print('bar')
    return False


foo(next=True) and bar()
print('=' * 50)
foo(next=False) and bar()
