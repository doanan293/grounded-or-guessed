from flx.templates import clusters, shape, similarity

A = '''
def total(xs):
    s = 0
    for x in xs:
        s += x
    return s
'''
A_RENAMED = '''
def acc(items):
    t = 0
    for it in items:
        t += it
    return t
'''
B = '''
def find(d, k):
    try:
        return d[k]
    except KeyError:
        return None
'''


def test_renamed_copy_same_shape():
    assert shape(A) == shape(A_RENAMED)
    assert similarity(A, A_RENAMED) == 1.0


def test_different_algorithms_low_similarity():
    assert similarity(A, B) < 0.5


def test_clusters_group_copies():
    c = clusters({"a": A, "a2": A_RENAMED, "b": B}, threshold=0.8)
    assert c["a"] == c["a2"] != c["b"]
