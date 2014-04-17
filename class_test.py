__author__ = 'Mike'

class A(object):
    def __init__(self):
        self.x = [1,2,3,3]
        self.y = [2,3,4,5]

    def foo(self):
        print 'A'

class B(A):

    def foo(self):
        super(B, self).foo()


class A(object):
    def foo(self):
        print "foo"

class B(A):
    def foo(self):
        super(B, self).foo()

test2 = B()

test2.foo()

test = B()
test.foo()