# objsnapshot
Create snapshots of python objects and restore them later in time.


## Example

```python
from .objsnapshot import  commit, rollback


class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def inc(self, by=None):
        if by is None:
            by = self.age
        self.age += by


    def __str__(self):
        return "{} {} ".format(self.name, self.age)

    def godangerous(self):
        self.name = "mr x"
        self.age = 90

class MovingBall:
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move2(self, x, y):
        self.x = x
        self.y = y

    __str__ = lambda self: "{} {}".format(self.x, self.y)


### Examples
def test_commit_state():
    h = Human("Ahmed", 50)
    mb = MovingBall(0, 0)

    commit1 = commit(h)
    assert commit1.state['name'] == 'Ahmed'
    assert commit1.state['age'] == 50
    assert len(commit1.state) == 2

    h.inc(20)
    h.inc(2)

    commit2 = commit(h)
    assert commit2.state['name'] == 'Ahmed'
    assert commit2.state['age'] != 50
    assert commit2.state['age'] == 72
    assert len(commit2.state) == 2

    h.godangerous()
    commit3 = commit(h)

    assert commit3.state['name'] == 'mr x'
    assert len(commit3.state) == 2

    ## be good again
    h = rollback(h, commit1)
    assert h.name == 'Ahmed'
    assert h.age == 50

    commit1 = commit(mb)

    assert len(commit1.state) == 2
    assert commit1.state['x'] == 0
    assert commit1.state['y'] == 0


    mb.move2(5, 124)
    commit2 = commit(mb)
    assert commit2.state['x'] == 5
    print(commit2.state)
    assert commit2.state['y'] == 124
    assert len(commit2.state) == 2

    mb = rollback(mb, commit1)

    assert mb.x == 0
    assert mb.y == 0

```