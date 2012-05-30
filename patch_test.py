import patch

def _dump_change(c):
    print "-"*80
    print "Original: "
    print c.old_version()
    print "-"*80
    print "Updated: " 
    print c.new_version()
    print "-"*80

def test_sanity():

    filename = "demo.patch"
    f = open(filename)
    changeset = patch.parse(filename, f.read())

    for change in changeset.changes():
        _dump_change(change)

